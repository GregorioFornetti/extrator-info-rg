import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def image_to_dataframe(image):
    return pytesseract.image_to_data(image, lang='por', output_type='data.frame')