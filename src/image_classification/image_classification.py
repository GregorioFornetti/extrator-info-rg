from joblib import load
import cv2


img_size = (150, 112)
model = load('image_classification/lof_model.joblib')


def get_rg_probability(img):
    resized_img = cv2.resize(img, img_size).flatten()
    pred = model.predict([resized_img])[0]
    if pred == -1:
        pred = 'Não é RG'
    else:
        pred = 'É RG'
    return pred