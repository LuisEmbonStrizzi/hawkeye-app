from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time
from tqdm import tqdm

# Argumentos del programa
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", # Dirección del video a analizar
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, # Longitud del trazado de la trayectoria
	help="max buffer size")
args = vars(ap.parse_args())

# Función principal
def main(frame):

    # Agrandamos el frame para ver más la pelota
    frame = imutils.resize(frame, anchoOG * resizer, altoOG * resizer)
    
    # Convertir la imagen a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Filtrar los tonos verdes de la imagen
    mask = cv2.inRange(hsv, greenLower, greenUpper)

    # Aplicar operaciones de morfología para eliminar ruido
    kernel = np.ones((5, 5), np.uint8)
    #mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Inicializar lista para almacenar los círculos detectados
    circles = []

    # Iterar sobre los contornos encontrados
    for contour in contours:
        # Calcular el área del contorno
        area = cv2.contourArea(contour)
        
        # Aproximar el contorno a un polígono
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
        
        # Si el contorno tiene aproximadamente forma circular y el área es suficientemente grande
        if len(approx) >= 1 and area > 100:
            # Encontrar el centro y el radio del círculo
            (x, y), radius = cv2.minEnclosingCircle(contour)
            
            # Agregar el círculo a la lista
            circles.append((int(x), int(y), int(radius)))

    # Dibujar los círculos en la imagen original
    for circle in circles:
        x, y, radius = circle
        cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)

    # Resizea el frame al tamaño original y lo muestra
    frame = imutils.resize(frame, height = 768)
    mask = imutils.resize(mask, height = 768)
    
    # También muestra la máscara
    cv2.imshow("Mascara Normal", mask)
    cv2.imshow("Normal", frame)

vs = cv2.VideoCapture(args["video"])

numeroFrame = 0
resizer = 3

# Definir el rango de tonos verdes en HSV
greenLower = np.array([40, 40, 40])
greenUpper = np.array([70, 255, 255])

greenLower = np.array([29, 50, 110])
greenUpper = np.array([64, 255, 255])

#greenLower = np.array([29, 15, 100])
#greenUpper = np.array([200, 255, 255])

# Se corre el for la cantidad de frames que contiene el video
while True:
    numeroFrame += 1
    print("Numero de Frame: ", numeroFrame)

    # Toma el frame del video
    frame = vs.read()[1]

    # Cuando termina las iteraciones y no hay frames. S
    if frame is None:
        break

    anchoOG = frame.shape[1]
    altoOG = frame.shape[0]

    main(frame)

    if numeroFrame == 14:
        cv2.imwrite('cerca.jpg', frame)
    if numeroFrame == 46:
        cv2.imwrite('medio.jpg', frame)
    if numeroFrame == 59:
        cv2.imwrite('lejos.jpg', frame)
        #break

    # Terminar la ejecución si se presiona la "q"
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # Pausar la ejecución al presionar la "p"
    if key == ord('p'):
        cv2.waitKey(-1)

if not args.get("video", False):
    vs.stop()

else:
    vs.release()

# Destruimos (cerramos) todas las ventanas de opencv
cv2.destroyAllWindows()