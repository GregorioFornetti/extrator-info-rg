
from utils import find_text

import pandas as pd


def find_name_text(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    return find_text(find_name, identified_texts_df, text_column_name)

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
    space_width = 6
    for i, row in identified_texts_df.iterrows():
        if isinstance(row[text_column_name], str):
            if row[text_column_name].lower() == 'filiação' or row[text_column_name].lower() == 'filiacao':
                if name == '':
                    return False
                info_dict['width'] -= space_width
                return format_name(name), info_dict

            if nome_found:
                name += row[text_column_name] + ' '
                if info_dict['left'] is None:
                    info_dict['left'] = row['left']
                    info_dict['top'] = row['top']
                    info_dict['height'] = row['height']
                info_dict['width'] += row['width'] + space_width
            
            if row[text_column_name].lower() == 'nome':
                nome_found = True
    return False

def format_name(text):
    if not isinstance(text, str):
        return False
    return text.strip().title()