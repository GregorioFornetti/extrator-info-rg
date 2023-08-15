import cv2

def rotate_90_if_vertical_rectangle(image):
    if image.shape[0] > image.shape[1]:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image

def rotate_180(image):
    return cv2.rotate(image, cv2.ROTATE_180)