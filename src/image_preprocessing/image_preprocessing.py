import cv2
from image_preprocessing.filters import to_gray, decrease_noise
from image_preprocessing.document_digitalization import digitalize_document
from image_preprocessing.rotations import rotate_90_if_vertical_rectangle


def preprocess_image(image):
    gray_image = to_gray(image)
    filtered_image = decrease_noise(gray_image)
    digitalized_document = digitalize_document(filtered_image)
    return rotate_90_if_vertical_rectangle(digitalized_document)