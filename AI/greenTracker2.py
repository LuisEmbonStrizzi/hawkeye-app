import cv2
import numpy as np
import imutils

# Cargar la imagen
imagen = cv2.imread('ImagenRecortadaGreenTracker.png')

imagen_recortada = imutils.resize(imagen, imagen.shape[1] * 3, imagen.shape[0] * 3)
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(imagen_gris, (11, 11), 0)

# Buscar círculos en la imagen
circulos = cv2.HoughCircles(imagen_gris, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40, param1=50, param2=25, minRadius=5, maxRadius=100)

for circulo in circulos[0]:
    cv2.circle(imagen, (int(circulo[0]), int(circulo[1])), int(circulo[2]), (0, 255, 0), 2)

if circulos is not None:
    circulos = np.uint16(np.around(circulos))
    colores_promedio = []

    for circulo in circulos[0, :]:
        x, y, radio = circulo

        # Extraer los píxeles dentro del círculo
        mascara = np.zeros_like(imagen_gris)
        cv2.circle(mascara, (x, y), radio, 255, -1)
        píxeles_del_círculo = cv2.bitwise_and(imagen, imagen, mask=mascara)

        # Calcular el color promedio de los píxeles dentro del círculo
        color_promedio = np.mean(píxeles_del_círculo, axis=(0, 1))

        colores_promedio.append(color_promedio)

    # Definir el color verde (ajusta estos valores según tus necesidades)
    color_verde = np.array([0, 255, 0])

    # Calcular las distancias euclidianas entre los colores promedio y el color verde
    distancias = [np.linalg.norm(color - color_verde) for color in colores_promedio]

    # Encontrar el índice del color promedio más cercano al verde
    indice_color_mas_cercano = np.argmin(distancias)

    # Mostrar el círculo más cercano al verde en la imagen original
    cv2.circle(imagen, (circulos[0, indice_color_mas_cercano, 0], circulos[0, indice_color_mas_cercano, 1]),
               circulos[0, indice_color_mas_cercano, 2], (255, 255, 255), 2)

    # Mostrar la imagen con el círculo más cercano al verde resaltado
    cv2.imshow('Imagen con Circulo Mas Cercano al Verde', imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print('No se encontraron círculos en la imagen.')
