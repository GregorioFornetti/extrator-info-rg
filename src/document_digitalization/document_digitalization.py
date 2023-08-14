# Código baseado no tutorial disponível em: https://www.makeuseof.com/python-create-document-scanner/

import numpy as np
import cv2


def document_digitalization(image):
    pass

def mark_document_found(image):
    pass


def find_document_edges(image):
    pass

def order_points(rect_edges):
   
    # Lembrando: o sistema de coordenadas de uma imagem começa no ponto superior esquerdo (x=0, y=0)
    # Ao caminhar para direita, o valor de x aumenta e de y aumenta...
    # https://www.mathworks.com/help/images/image-coordinate-systems.html

    rect = np.zeros((4, 2), dtype = "float32")

    # Calcula a soma entre x e y (x+y) para cada ponto
    points_coordinates_sum = rect_edges.sum(axis=1)

    # ponto superior esquerdo será o ponto que possuir menor soma (valor de x + y)
    # já que o valor de x e de y serão mínimos (os outros pontis terão pelo menos uma das duas coordenadas bem superior)
    rect[0] = rect_edges[np.argmin(points_coordinates_sum)]

    # ponto inferior direito terá a maior soma (valor de x + y)
    # já que o valor de x e de y serão máximos (as outras pontis terão pelo menos uma das duas coordenadas bem inferior)
    rect[2] = rect_edges[np.argmax(points_coordinates_sum)]

    # Calcula a diferença entre y e x (y-x) para cada ponto
    diff = np.diff(rect_edges, axis = 1)

    # o ponto superior direito será o ponto em que a diferença entre y e x for a menor (menor valor de y - x)
    # pois, nesse caso, o y terá o seu menor valor e o x o seu maior valor
    rect[1] = rect_edges[np.argmin(diff)]

    # o ponto superior esquerdo será o ponto em que a diferença entre y e x for a maior (menor valor de y - x)
    # pois, nesse caso, o y terá o seu maior valor e o x o seu menor valor
    rect[3] = rect_edges[np.argmax(diff)]

    return rect

def perspective_transform(image, pts):
    # unpack the ordered coordinates individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    '''compute the width of the new image, which will be the
    maximum distance between bottom-right and bottom-left
    x-coordinates or the top-right and top-left x-coordinates'''
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    '''compute the height of the new image, which will be the
    maximum distance between the top-left and bottom-left y-coordinates'''
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    '''construct the set of destination points to obtain an overhead shot'''
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix
    transform_matrix = cv2.getPerspectiveTransform(rect, dst)

    # Apply the transform matrix
    warped = cv2.warpPerspective(image, transform_matrix, (maxWidth, maxHeight))

    # return the warped image
    return warped