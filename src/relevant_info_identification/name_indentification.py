
from relevant_info_identification.utils import find_text, find_index

import pandas as pd


def find_name_text(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    return find_text(find_name, identified_texts_df, text_column_name)

def find_name_index(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    return find_index(find_name, identified_texts_df, text_column_name)

def find_name(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    nome_found = False

    name = ''
    info_dict = {
        'left': None,
        'right': None,
        'width': 0,
        'height': 0,
        'name': 'nome'
    }
    indexes = []
    space_width = 6
    for i, row in identified_texts_df.iterrows():
        if isinstance(row[text_column_name], str):
            if row[text_column_name].lower() == 'filiação' or row[text_column_name].lower() == 'filiacao':
                if name == '':
                    return False
                info_dict['width'] -= space_width
                return format_name(name), info_dict, indexes

            if nome_found:
                name += row[text_column_name] + ' '
                if info_dict['left'] is None:
                    info_dict['left'] = row['left']
                    info_dict['top'] = row['top']
                    info_dict['height'] = row['height']
                info_dict['width'] += row['width'] + space_width
                indexes.append(i)
            
            if row[text_column_name].lower() == 'nome':
                nome_found = True
    return False

def format_name(text):
    if not isinstance(text, str):
        return False
    return text.strip().title()