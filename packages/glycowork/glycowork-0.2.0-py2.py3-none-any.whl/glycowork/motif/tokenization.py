import pandas as pd
import re
import copy
from itertools import combinations_with_replacement
from collections import Counter

from glycowork.glycan_data.loader import lib, motif_list, find_nth, unwrap, df_species, Hex, dHex, HexNAc, Sia
from glycowork.motif.processing import small_motif_find, min_process_glycans


def character_to_label(character, libr = None):
  """tokenizes character by indexing passed library\n
  | Arguments:
  | :-
  | character (string): character to index
  | libr (list): list of library items\n
  | Returns:
  | :-
  | Returns index of character in library
  """
  if libr is None:
    libr = lib
  character_label = libr.index(character)
  return character_label

def string_to_labels(character_string, libr = None):
  """tokenizes word by indexing characters in passed library\n
  | Arguments:
  | :-
  | character_string (string): string of characters to index
  | libr (list): list of library items\n
  | Returns:
  | :-
  | Returns indexes of characters in library
  """
  if libr is None:
    libr = lib
  return list(map(lambda character: character_to_label(character, libr), character_string))

def pad_sequence(seq, max_length, pad_label = None):
  """brings all sequences to same length by adding padding token\n
  | Arguments:
  | :-
  | seq (list): sequence to pad (from string_to_labels)
  | max_length (int): sequence length to pad to
  | pad_label (int): which padding label to use\n
  | Returns:
  | :-
  | Returns padded sequence
  """
  if pad_label is None:
    pad_label = len(lib)
  seq += [pad_label for i in range(max_length - len(seq))]
  return seq

def convert_to_counts_glycoletter(glycan, libr = None):
  """counts the occurrence of glycoletters in glycan\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format
  | libr (list): sorted list of unique glycoletters observed in the glycans of our dataset\n
  | Returns:
  | :-
  | Returns dictionary with counts per glycoletter in a glycan
  """
  if libr is None:
    libr = lib
  letter_dict = dict.fromkeys(libr, 0)
  glycan = small_motif_find(glycan).split('*')
  for i in libr:
    letter_dict[i] = glycan.count(i)
  return letter_dict

def glycoletter_count_matrix(glycans, target_col, target_col_name, libr = None):
  """creates dataframe of counted glycoletters in glycan list\n
  | Arguments:
  | :-
  | glycans (list): list of glycans in IUPAC-condensed format as strings
  | target_col (list or pd.Series): label columns used for prediction
  | target_col_name (string): name for target_col
  | libr (list): sorted list of unique glycoletters observed in the glycans of our dataset\n
  | Returns:
  | :-
  | Returns dataframe with glycoletter counts (columns) for every glycan (rows)
  """
  if libr is None:
    libr = lib
  counted_glycans = [convert_to_counts_glycoletter(i, libr) for i in glycans]
  out = pd.DataFrame(counted_glycans)
  out[target_col_name] = target_col
  return out

def find_isomorphs(glycan):
  """returns a set of isomorphic glycans by swapping branches etc.\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format\n
  | Returns:
  | :-
  | Returns list of unique glycan notations (strings) for a glycan in IUPAC-condensed
  """
  out_list = [glycan]
  #starting branch swapped with next side branch
  if '[' in glycan and glycan.index('[') > 0 and not bool(re.search('\[[^\]]+\[', glycan)):
    glycan2 = re.sub('^(.*?)\[(.*?)\]', r'\2[\1]', glycan, 1)
    out_list.append(glycan2)
  #double branch swap
  temp = []
  for k in out_list:
    if '][' in k:
      glycan3 = re.sub('(\[.*?\])(\[.*?\])', r'\2\1', k)
      temp.append(glycan3)
  #starting branch swapped with next side branch again to also include double branch swapped isomorphs
  temp2 = []
  for k in temp:
    if '[' in k and k.index('[') > 0 and not bool(re.search('\[[^\]]+\[', k)):
      glycan4 = re.sub('^(.*?)\[(.*?)\]', r'\2[\1]', k, 1)
      temp2.append(glycan4)
  return list(set(out_list + temp + temp2))

def link_find(glycan):
  """finds all disaccharide motifs in a glycan sequence using its isomorphs\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format\n
  | Returns:
  | :-
  | Returns list of unique disaccharides (strings) for a glycan in IUPAC-condensed
  """
  ss = find_isomorphs(glycan)
  coll = []
  for iso in ss:
    b_re = re.sub('\[[^\]]+\]', '', iso)
    for i in [iso, b_re]:
      b = i.split('(')
      b = [k.split(')') for k in b]
      b = [item for sublist in b for item in sublist]
      b = ['*'.join(b[i:i+3]) for i in range(0, len(b) - 2, 2)]
      b = [k for k in b if (re.search('\*\[', k) is None and re.search('\*\]\[', k) is None)]
      b = [k.strip('[') for k in b]
      b = [k.strip(']') for k in b]
      b = [k.replace('[', '') for k in b]
      b = [k.replace(']', '') for k in b]
      b = [k[:find_nth(k, '*', 1)] + '(' + k[find_nth(k, '*', 1)+1:] for k in b]
      b = [k[:find_nth(k, '*', 1)] + ')' + k[find_nth(k, '*', 1)+1:] for k in b]
      coll += b
  return list(set(coll))

def motif_matrix(df, glycan_col_name, label_col_name, libr = None):
  """generates dataframe with counted glycoletters and disaccharides in glycans\n
  | Arguments:
  | :-
  | df (dataframe): dataframe containing glycan sequences and labels
  | glycan_col_name (string): column name for glycan sequences
  | label_col_name (string): column name for labels; string
  | libr (list): sorted list of unique glycoletters observed in the glycans of our dataset\n
  | Returns:
  | :-
  | Returns dataframe with glycoletter + disaccharide counts (columns) for each glycan (rows)
  """
  if libr is None:
    libr = lib
  matrix_list = []
  di_dics = []
  wga_di = [link_find(i) for i in df[glycan_col_name].values.tolist()]
  lib_di = list(sorted(list(set([item for sublist in wga_di for item in sublist]))))
  for j in wga_di:
    di_dict = dict.fromkeys(lib_di, 0)
    for i in list(di_dict.keys()):
      di_dict[i] = j.count(i)
    di_dics.append(di_dict)
  wga_di_out = pd.DataFrame(di_dics)
  wga_letter = glycoletter_count_matrix(df[glycan_col_name].values.tolist(),
                                          df[label_col_name].values.tolist(),
                                   label_col_name, libr)
  out_matrix = pd.concat([wga_letter, wga_di_out], axis = 1)
  out_matrix = out_matrix.loc[:,~out_matrix.columns.duplicated()]
  temp = out_matrix.pop(label_col_name)
  out_matrix[label_col_name] = temp
  out_matrix.reset_index(drop = True, inplace = True)
  return out_matrix

def get_core(sugar):
  """retrieves core monosaccharide from modified monosaccharide\n
  | Arguments:
  | :-
  | sugar (string): monosaccharide or linkage\n
  | Returns:
  | :-
  | Returns core monosaccharide as string
  """
  easy_cores = ['GlcNAc', 'GalNAc', 'ManNAc', 'FucNAc', 'QuiNAc', 'RhaNAc', 'GulNAc',
                'IdoNAc', 'MurNAc', 'HexNAc', '6dAltNAc', 'AcoNAc', 'GlcA', 'AltA',
                'GalA', 'ManA', 'Tyv', 'Yer', 'Abe', 'GlcfNAc', 'GalfNAc', 'ManfNAc',
                'FucfNAc', 'IdoA', 'GulA', 'LDManHep', 'DDManHep', 'DDGlcHep', 'LyxHep', 'ManHep',
                'DDAltHep', 'IdoHep', 'DLGlcHep', 'GalHep']
  next_cores = ['GlcN', 'GalN', 'ManN', 'FucN', 'QuiN', 'RhaN', 'AraN', 'IdoN' 'Glcf', 'Galf', 'Manf',
                'Fucf', 'Araf', 'Lyxf', 'Xylf', '6dAltf', 'Ribf', 'Fruf', 'Apif', 'Kdof', 'Sedf',
                '6dTal', 'AltNAc', '6dAlt']
  hard_cores = ['Glc', 'Gal', 'Man', 'Fuc', 'Qui', 'Rha', 'Ara', 'Oli', 'Kdn', 'Gul', 'Lyx',
                'Xyl', 'Dha', 'Rib', 'Kdo', 'Tal', 'All', 'Pse', 'Leg', 'Asc',
                'Fru', 'Hex', 'Alt', 'Xluf', 'Api', 'Ko', 'Pau', 'Fus', 'Erwiniose',
                'Aco', 'Bac', 'Dig', 'Thre-ol', 'Ery-ol']
  if bool([ele for ele in easy_cores if(ele in sugar)]):
    return [ele for ele in easy_cores if(ele in sugar)][0]
  elif bool([ele for ele in next_cores if(ele in sugar)]):
    return [ele for ele in next_cores if(ele in sugar)][0]
  elif bool([ele for ele in hard_cores if(ele in sugar)]):
    return [ele for ele in hard_cores if(ele in sugar)][0]
  elif (('Neu' in sugar) and ('5Ac' in sugar)):
    return 'Neu5Ac'
  elif (('Neu' in sugar) and ('5Gc' in sugar)):
    return 'Neu5Gc'
  elif 'Neu' in sugar:
    return 'Neu'
  elif ((sugar.startswith('a')) or sugar.startswith('b')):
    return sugar
  elif re.match('^[0-9]+(-[0-9]+)+$', sugar):
    return sugar
  else:
    return 'Sug'

def get_stem_lib(libr):
  """creates a mapping file to map modified monosaccharides to core monosaccharides\n
  | Arguments:
  | :-
  | libr (list): sorted list of unique glycoletters observed in the glycans of our dataset\n
  | Returns:
  | :-
  | Returns dictionary of form modified_monosaccharide:core_monosaccharide
  """
  return {k:get_core(k) for k in libr}

def stemify_glycan(glycan, stem_lib):
  """removes modifications from all monosaccharides in a glycan\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format
  | stem_lib (dictionary): dictionary of form modified_monosaccharide:core_monosaccharide\n
  | Returns:
  | :-
  | Returns stemmed glycan as string
  """
  clean_list = list(stem_lib.values())
  for k in list(stem_lib.keys())[::-1][:-1]:
    if ((k not in clean_list) and (k in glycan) and not (k.startswith(('a','b'))) and not (re.match('^[0-9]+(-[0-9]+)+$', k))):
      while ((k in glycan) and (sum(1 for s in clean_list if k in s) <= 1)):
        glycan_start = glycan[:glycan.rindex('(')]
        glycan_part = glycan_start
        if k in glycan_start:
          cut = glycan_start[glycan_start.index(k):]
          try:
            cut = cut[:cut.index('(')]
          except:
            pass
          if cut not in clean_list:
            glycan_part = glycan_start[:glycan_start.index(k)]
            glycan_part = glycan_part + stem_lib[k]
          else:
            glycan_part = glycan_start
        try:
          glycan_mid = glycan_start[glycan_start.index(k) + len(k):]
          if ((cut not in clean_list) and (len(glycan_mid)>0)):
            glycan_part = glycan_part + glycan_mid
        except:
          pass
        glycan_end = glycan[glycan.rindex('('):]
        if k in glycan_end:
          if ']' in glycan_end:
            filt = ']'
          else:
            filt = ')'
          cut = glycan_end[glycan_end.index(filt)+1:]
          if cut not in clean_list:
            glycan_end = glycan_end[:glycan_end.index(filt)+1] + stem_lib[k]
          else:
            pass
        glycan = glycan_part + glycan_end
  return glycan

def stemify_dataset(df, stem_lib = None, libr = None,
                    glycan_col_name = 'target', rarity_filter = 1):
  """stemifies all glycans in a dataset by removing monosaccharide modifications\n
  | Arguments:
  | :-
  | df (dataframe): dataframe with glycans in IUPAC-condensed format in column glycan_col_name
  | stem_lib (dictionary): dictionary of form modified_monosaccharide:core_monosaccharide; default:created from lib
  | libr (list): sorted list of unique glycoletters observed in the glycans of our dataset; default:lib
  | glycan_col_name (string): column name under which glycans are stored; default:target
  | rarity_filter (int): how often monosaccharide modification has to occur to not get removed; default:1\n
  | Returns:
  | :-
  | Returns df with glycans stemified
  """
  if libr is None:
    libr = lib
  if stem_lib is None:
    stem_lib = get_stem_lib(libr)
  pool = unwrap(min_process_glycans(df[glycan_col_name].values.tolist()))
  pool_count = Counter(pool)
  for k in list(set(pool)):
    if pool_count[k] > rarity_filter:
      stem_lib[k] = k
  df_out = copy.deepcopy(df)
  df_out[glycan_col_name] = [stemify_glycan(k, stem_lib) for k in df_out[glycan_col_name].values.tolist()]
  return df_out

def match_composition(composition, group, level, df = None,
                      mode = "minimal", libr = None, glycans = None):
    """Given a monosaccharide composition, it returns all corresponding glycans\n
    | Arguments:
    | :-
    | composition (dict): a dictionary indicating the composition to match (for example {"Fuc":1, "Gal":1, "GlcNAc":1})
    | group (string): name of the Species, Genus, Family, Order, Class, Phylum, Kingdom, or Domain used to filter
    | level (string): Species, Genus, Family, Order, Class, Phylum, Kingdom, or Domain
    | df (dataframe): glycan dataframe for searching glycan structures; default:None
    | mode (string): can be "minimal" or "exact" to match glycans that contain at least the specified composition or glycans matching exactly the requirements
    | glycans (list): custom list of glycans to check the composition in; default:None\n
    | Returns:
    | :-
    | Returns list of glycans matching composition in IUPAC-condensed
    """
    if df is None:
      df = df_species
    if libr is None:
      libr = lib
    filtered_df = df[df[level] == group]
        
    exact_composition = {}
    if mode == "minimal":
        for element in libr:
            if element in composition:
                exact_composition[element] = composition.get(element)
        if glycans is None:
          glycan_list = filtered_df.target.values.tolist()
        else:
          glycan_list = glycans
        to_remove = []
        output_list = glycan_list
        for glycan in glycan_list:
            for key in exact_composition:
                glycan_count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(key), glycan))
                if exact_composition[key] != glycan_count :
                    to_remove.append(glycan)
        for element in to_remove:
            try :
                output_list.remove(element)
            except :
                a = 1
        output_list = list(set(output_list))
        #print(str(len(output_list)) + " glycan structures match your composition.")
        #for element in output_list:
        #    print(element)
        
    if mode == "exact":
        for element in libr:
            if element in composition:
                exact_composition[element] = composition.get(element)
        if glycans is None:
          glycan_list = filtered_df.target.values.tolist()
        else:
          glycan_list = glycans
        to_remove = []
        output_list = glycan_list
        for glycan in glycan_list:
            count_sum = 0
            for key in exact_composition :
                glycan_count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(key), glycan))
                count_sum = count_sum + exact_composition[key]
                if exact_composition[key] != glycan_count:
                    to_remove.append(glycan)
            monosaccharide_number_in_glycan = glycan.count("(") + 1
            if monosaccharide_number_in_glycan != count_sum:
                to_remove.append(glycan)
        for element in to_remove:
            try :
                output_list.remove(element)
            except :
                a = 1
        output_list = list(set(output_list))
        #print(str(len(output_list)) + " glycan structures match your composition.")
        #for element in output_list:
        #    print(element)
            
    return output_list

def match_composition_relaxed(composition, group, level, df = None,
                      mode = "minimal", libr = None):
    """Given a coarse-grained monosaccharide composition (Hex, HexNAc, etc.), it returns all corresponding glycans\n
    | Arguments:
    | :-
    | composition (dict): a dictionary indicating the composition to match (for example {"Fuc":1, "Gal":1, "GlcNAc":1})
    | group (string): name of the Species, Genus, Family, Order, Class, Phylum, Kingdom, or Domain used to filter
    | level (string): Species, Genus, Family, Order, Class, Phylum, Kingdom, or Domain
    | df (dataframe): glycan dataframe for searching glycan structures; default:None
    | mode (string): can be "minimal" or "exact" to match glycans that contain at least the specified composition or glycans matching exactly the requirements\n
    | Returns:
    | :-
    | Returns list of glycans matching composition in IUPAC-condensed
    """
    if df is None:
      df = df_species
    if libr is None:
      libr = lib
    original_composition = copy.deepcopy(composition)
    if 'Hex' in composition:
      hex_pool = list(combinations_with_replacement(Hex, composition['Hex']))
      hex_pool = [Counter(k) for k in hex_pool]
      composition.pop('Hex')
      output_list = [match_composition(k, group, level, df = df,
                                     mode = 'minimal', libr = libr) for k in hex_pool]
      output_list = list(set(unwrap(output_list)))
    if 'dHex' in composition:
      dhex_pool = list(combinations_with_replacement(dHex, composition['dHex']))
      dhex_pool = [Counter(k) for k in dhex_pool]
      composition.pop('dHex')
      output_list = [match_composition(k, group, level, df = df,
                                     mode = 'minimal', libr = libr,
                                       glycans = output_list) for k in dhex_pool]
      output_list = list(set(unwrap(output_list)))
    if 'HexNAc' in composition:
      hexnac_pool = list(combinations_with_replacement(HexNAc, composition['HexNAc']))
      hexnac_pool = [Counter(k) for k in hexnac_pool]
      composition.pop('HexNAc')
      output_list = [match_composition(k, group, level, df = df,
                                     mode = 'minimal', libr = libr,
                                       glycans = output_list) for k in hexnac_pool]
      output_list = list(set(unwrap(output_list)))
    if len(composition)>0:
      output_list = match_composition(k, group, level, df = df,
                                     mode = 'minimal', libr = libr,
                                       glycans = output_list)
    if mode == 'exact':
      monosaccharide_count = sum(original_composition.values())
      output_list = [k for k in output_list if k.count('(') == monosaccharide_count-1]
    return output_list
