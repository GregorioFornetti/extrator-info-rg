
from relevant_info_identification.utils import create_info_dict_from_row, find_text

import re

import pandas as pd


date_regex = r'^\d{2}[\/]?\d{2}[\/]?\d{4}$'

def find_birthdate_text(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    return find_text(find_birthdate, identified_texts_df, text_column_name)

def find_birthdate(identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    dates_count = 0
    for i, row in identified_texts_df.iterrows():
        if is_date(row[text_column_name]):
            dates_count += 1
        if dates_count == 2:
            return format_date(row[text_column_name]), create_info_dict_from_row(row, 'nasc.')
    return False


def is_date(text):
    if not isinstance(text, str):
        return False
    return bool(re.search(date_regex, text))

def format_date(unformated_date: str):
    # Remove todas pontuações da regex, mantendo apenas os digitos
    date = re.sub(r'[\/]', '', unformated_date)
    # Retorna a data formatada com o seu padrão correto
    return {
        'formated_date': f'{date[0:2]}/{date[2:4]}/{date[4:]}',
        'day': int(date[0:2]),
        'month': int(date[2:4]),
        'year': int(date[4:])
    }