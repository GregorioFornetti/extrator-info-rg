
from relevant_info_identification.utils import create_info_dict_from_row, find_text, find_index

import re

import pandas as pd


rg_regex = r'^\d{2}[\,\.]?\d{3}[\,\.]?\d{3}[\,\.\-]?\d$'

def find_rg_text(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    return find_text(find_rg, identified_texts_df, text_column_name)

def find_rg_index(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    return find_index(find_rg, identified_texts_df, text_column_name)

def find_rg(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    for i, row in identified_texts_df.iterrows():
        if is_rg(row[text_column_name]):
            return format_rg(row[text_column_name]), create_info_dict_from_row(row, 'rg'), [i]
    return False
    
def is_rg(text):
    if not isinstance(text, str):
        return False
    return bool(re.search(rg_regex, text))

def format_rg(unformated_rg: str):
    # Remove todas pontuações da regex, mantendo apenas os digitos
    rg = re.sub(r'[\-\,\.]', '', unformated_rg)
    # Retorna o RG com o seu padrão correto
    return f'{rg[0:2]}.{rg[2:5]}.{rg[5:8]}-{rg[8:9]}'