# import numpy as np
# import cv2
import imutils

# frame = cv2.imread("imagen_recortada67-SinCirculos.png")

# altoOG, anchoOG = frame.shape[:2]
# greenLower = np.array([29, 50, 110])
# greenUpper = np.array([64, 255, 255])

# greenLower = np.array([35, 50, 50])
# greenUpper = np.array([85, 255, 255])

# frame = imutils.resize(frame, anchoOG * 3, altoOG * 3)

# blurred = cv2.medianBlur(frame, 5)
# hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# mascara = cv2.inRange(hsv, greenLower, greenUpper)
# kernel = np.ones((5, 5), np.uint8)
# mascara = cv2.dilate(mascara, kernel, iterations=2)

# contornos, _ = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# frame = imutils.resize(frame, height= 500)
# mascara = imutils.resize(mascara, height= 500)

# cv2.imshow("Frame", frame)
# cv2.imshow("Mask", mascara)

# while True:
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord("q"):
#         break

# cv2.destroyAllWindows()

import cv2
import numpy as np

# Carga la imagen desde la ubicación especificada
imagen = cv2.imread("Frame67.jpg")

resizer = 3

# Verifica si la imagen se cargó correctamente
if imagen is None:
    print("No se pudo cargar la imagen. Asegúrate de especificar la ruta correcta.")
else:  
    altoOG, anchoOG = imagen.shape[:2]
    print("Alto", altoOG, "ancho", anchoOG)

    #imagen = imutils.resize(imagen, anchoOG * resizer, altoOG * resizer)
    print(imagen.shape[:2])
    
    # Definir las coordenadas del rectángulo de recorte
    x1, y1, x2, y2 = 2854, 1723, 3254, 2123

    imagen_recortada = imagen[y1:y2, x1:x2]
    cv2.imwrite("ImagenRecortadaGreenTracker.png", imagen_recortada)

    imagen_recortada = imutils.resize(imagen_recortada, imagen_recortada.shape[1] * resizer, imagen_recortada.shape[0] * resizer)
    imagen_gris = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.medianBlur(imagen_gris, 5)
    blurred = cv2.GaussianBlur(imagen_gris, (11, 11), 0)
    
    # Convierte la imagen a espacio de color HSV
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Define el valor del color verde en HSV
    verde = np.uint8([[[0, 255, 0]]])
    verde_hsv = cv2.cvtColor(verde, cv2.COLOR_BGR2HSV)[0][0]

    # Encuentra los contornos y los círculos en la imagen
    contornos, _ = cv2.findContours(cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40, param1=50, param2=25, minRadius=5, maxRadius=100)

    if circles is not None:
        for (x, y, r) in circles[0]:
            #if abs(r - radioDeteccionPorCirculo * 3) < 10: cv2.circle(imagen_recortada, (x, y), r, (0, 255, 0), 2)
            cv2.circle(imagen_recortada, (np.round(x).astype(int), np.round(y).astype(int)), np.round(r).astype(int), (0, 255, 0), 2)

    print("Número de contornos encontrados:", len(contornos))

    # Inicializa variables para almacenar el contorno más cercano al verde y su distancia
    contorno_mas_cercano = None
    distancia_mas_cercana = float('inf')

    # Crea una máscara en blanco del mismo tamaño que la imagen original
    mascara = np.zeros(imagen.shape[:2], dtype=np.uint8)

    # Itera a través de los contornos y encuentra el más cercano al verde
    for contorno in contornos:
        # Calcula el color promedio del contorno
        mask = np.zeros(imagen.shape[:2], np.uint8)
        cv2.drawContours(mask, [contorno], -1, 255, thickness=cv2.FILLED)
        promedio_color = cv2.mean(hsv, mask=mask)[:3]

        # Calcula la distancia entre el color promedio y el verde en el espacio HSV
        distancia = np.sqrt(np.sum((promedio_color - verde_hsv) ** 2))

        # Actualiza el contorno más cercano si la distancia actual es menor
        if distancia < distancia_mas_cercana:
            distancia_mas_cercana = distancia
            contorno_mas_cercano = contorno

        # Dibuja todos los contornos en la máscara
        cv2.drawContours(mascara, [contorno], -1, 255, thickness=cv2.FILLED)

    # Dibuja el contorno más cercano al verde en la imagen original
    if contorno_mas_cercano is not None:
        #cv2.drawContours(imagen, [contorno_mas_cercano], -1, (0, 255, 0), 3)
        circle = cv2.minEnclosingCircle(contorno_mas_cercano)

        cv2.circle(imagen, (int(circle[0][0]), int(circle[0][1])), int(circle[1]), (0, 255, 0), 3)

        # Muestra la imagen con el contorno verde
        imagen = imutils.resize(imagen, height= 500)
        mascara = imutils.resize(mascara, height= 500)
        imagen_recortada = imutils.resize(imagen_recortada, height= 500)

        cv2.imshow("Imagen", imagen)
        cv2.imshow("Mascara de Contornos", mascara)
        cv2.imshow("Imagen Recortada", imagen_recortada)

        # Espera hasta que se presione la tecla 'q' o la tecla ESC para cerrar la ventana
        while True:
            tecla = cv2.waitKey(0)
            if tecla == ord('q') or tecla == 27:  # 'q' o ESC
                break

        # Cierra la ventana
        cv2.destroyAllWindows()
    else:
        print("No se encontraron contornos en la imagen.")
