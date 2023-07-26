
from relevant_info_identification.utils import create_info_dict_from_row, find_text

import re

import pandas as pd


cpf_regex = r'^\d{3}[\,\.]?\d{3}[\,\.]?\d{3}[\,\.\-\/]?\d{2}$'

def find_cpf_text(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    return find_text(find_cpf, identified_texts_df, text_column_name)

def find_cpf(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    for i, row in identified_texts_df.iterrows():
        if is_cpf(row[text_column_name]):
            return format_cpf(row[text_column_name]), create_info_dict_from_row(row, 'cpf')
    return False

def is_cpf(text):
    if not isinstance(text, str):
        return False
    return bool(re.search(cpf_regex, text))

def format_cpf(unformated_cpf: str):
    # Remove todas pontuações da regex, mantendo apenas os digitos
    cpf = re.sub(r'[\-\,\.\/]', '', unformated_cpf)
    # Retorna o CPF com o seu padrão correto
    return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'