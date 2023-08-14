# Código baseado no tutorial disponível em: https://www.makeuseof.com/python-create-document-scanner/

import numpy as np
import cv2


def document_digitalization(image):
    # Recebe uma imagem e retorna o maior retângulo digitalizado
    rect_edges = find_document_edges(image)
    return perspective_transform(image, rect_edges)

def mark_document_found(image):
    # Retorna uma imagem com as bordas do retângulo encontrado marcadas
    # Caso não tenha sido encontrado as bordas na imagem, a imagem original será retornada sem nenhuma modificação

    rect_edges = find_document_edges(image)
    if rect_edges is not None:
        img_copy = image.copy()
        for edge in rect_edges:
            cv2.circle(
                img=img_copy, 
                center=edge, 
                radius=3,
                color=(0, 0, 255), 
                thickness=4
            )


def find_document_edges(image):
    # Encontra os pontos dos cantos do maior retângulo encontrado
    # Retorna uma lista contendo esses 4 pontos, sem uma ordem especifica dos pontos
    
    edged_img = cv2.Canny(image, 75, 200)

    cnts, _ = cv2.findContours(edged_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            return [tuple(d[0]) for d in approx]
    return None

def order_points(rect_edges):
    # Recebe como entrada um vetor com 4 pontos (vetores de tamanho 2, com valores de x e y)
    # essa entrada representa pontos de um retângulo, porém não necessariamente eles possuem alguma ordem
    # O retorno será um vetor com esses mesmos 4 pontos só que de forma ordenada, o primeiro será o canto superior esquerdo
    # (tr), o segundo o canto superior direito (tl), o terceiro o canto inferior direito (br) e o último o canto inferior esquerdo (bl)
    # ou seja, retorna: [tr, tl, br, bl]
   
    # Lembrando: o sistema de coordenadas de uma imagem começa no ponto superior esquerdo (x=0, y=0)
    # Ao caminhar para direita, o valor de x aumenta e de y aumenta...
    # https://www.mathworks.com/help/images/image-coordinate-systems.html

    rect = np.zeros((4, 2), dtype = "float32")

    # Calcula a soma entre x e y (x+y) para cada ponto
    points_coordinates_sum = rect_edges.sum(axis=1)

    # ponto superior esquerdo será o ponto que possuir menor soma (valor de x + y)
    # já que o valor de x e de y serão mínimos (os outros pontos terão pelo menos uma das duas coordenadas bem superior)
    rect[0] = rect_edges[np.argmin(points_coordinates_sum)]

    # ponto inferior direito terá a maior soma (valor de x + y)
    # já que o valor de x e de y serão máximos (as outras pontos terão pelo menos uma das duas coordenadas bem inferior)
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
    # Recebe como entrada uma imagem e os pontos das bordas do retângulo encontrado na imagem
    # Retorna uma imagem com apenas a região do retângulo, transformado parecido com uma digitalização

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