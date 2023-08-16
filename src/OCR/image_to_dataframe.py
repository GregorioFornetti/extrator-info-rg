import pytesseract

def image_to_dataframe(image):
    return pytesseract.image_to_data(image, lang='por', output_type='data.frame')