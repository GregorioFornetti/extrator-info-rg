import cv2
from image_preprocessing.filters import to_gray, decrease_noise
from image_preprocessing.document_digitalization import digitalize_document


def preprocess_image(image):
    gray_image = to_gray(image)
    filtered_image = decrease_noise(gray_image)
    return digitalize_document(filtered_image)
