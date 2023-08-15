import pytesseract
import pandas as pd
import cv2


from relevant_info_identification.birthdate_identification import find_birthdate
from relevant_info_identification.name_indentification import find_name
from relevant_info_identification.rg_identification import find_rg
from relevant_info_identification.cpf_identification import find_cpf

def get_document_info_and_mark_relevant_regions(document_image):
    document_dict, document_bounding_boxes = get_document_info(document_image)
    document_image_with_marked_relevant_regions = add_bounding_boxes(document_image, document_bounding_boxes)
    return document_dict, document_image_with_marked_relevant_regions


def get_document_info(document_image):
    def key_function(rows):
        def get_key(value):
            if isinstance(value, int):
                return value
            else:
                return value[0]
        
        return rows.map(get_key)

    document_dict = {}
    document_bounding_boxes = []

    identified_texts_df = pytesseract.image_to_data(document_image, lang='por', output_type='data.frame')
    identified_texts_df = identified_texts_df.sort_values(by=['top', 'left'], key=key_function).reset_index(drop=True)

    name_response = find_name(identified_texts_df)
    if name_response:
        document_dict['nome'] = name_response[0]
        document_bounding_boxes.append(name_response[1])

    cpf_response = find_cpf(identified_texts_df)
    if cpf_response:
        document_dict['cpf'] = cpf_response[0]
        document_bounding_boxes.append(cpf_response[1])
    
    name_response = find_name(identified_texts_df)
    if name_response:
        document_dict['nome'] = name_response[0]
        document_bounding_boxes.append(name_response[1])
    
    rg_response = find_rg(identified_texts_df)
    if rg_response:
        document_dict['rg'] = rg_response[0]
        document_bounding_boxes.append(rg_response[1])
    
    birthdate_response = find_birthdate(identified_texts_df)
    if birthdate_response:
        document_dict['data de nascimento'] = birthdate_response[0]
        document_bounding_boxes.append(birthdate_response[1])
    
    return document_dict, pd.DataFrame(document_bounding_boxes)

def add_bounding_boxes(document_image, bounding_boxes, padding=5, color=(0, 255, 0)):
    document_image_copy = document_image.copy()
    for i, row in bounding_boxes.iterrows():
        (x, y, w, h) = (row['left'], row['top'], row['width'], row['height'])

        x -= padding
        y -= padding
        w += padding * 2
        h += padding * 2

        cv2.rectangle(
            img=document_image_copy, 
            pt1=(x, y),
            pt2=(x + w, y + h), 
            color=color, 
            thickness=2
        )
        cv2.putText(
            img=document_image_copy,
            text=row['name'], 
            org=(x + w + 10, y + h), 
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=2,
            color=color,
            thickness=2,
            lineType=cv2.LINE_AA
        )
    return document_image_copy