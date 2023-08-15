import cv2

def to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def decrease_noise(image):
    return cv2.GaussianBlur(image, (5, 5), 0)