
import pandas as pd

def create_info_dict_from_row(row, name):
    return {
        'left': row['left'],
        'top': row['top'],
        'width': row['width'],
        'height': row['height'],
        'name': name
    }

def find_text(find_function, identified_texts_df: pd.DataFrame, text_column_name: str = 'text'):
    result = find_function(identified_texts_df, text_column_name)
    if result:
        return result[0]
    else:
        return ''