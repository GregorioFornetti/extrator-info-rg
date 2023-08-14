import cv2

def preprocess_image(image):
    gray_image = to_gray(image)
    filtered_image = decrease_noise(gray_image)
    return filtered_image


def to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def decrease_noise(image):
    return cv2.GaussianBlur(image, (5, 5), 0)