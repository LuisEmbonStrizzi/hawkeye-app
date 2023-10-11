from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time
from tqdm import tqdm
from scipy.optimize import curve_fit
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Argumentos del programa
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", # Dirección del video a analizar
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, # Longitud del trazado de la trayectoria
	help="max buffer size")
args = vars(ap.parse_args())

# Función principal
def main(frame):
    global TiempoDeteccionUltimaPelota
    global primeraVez
    global preCentro
    global TiempoTresCentrosConsecutivos
    global TiempoDifPiques
    global posiblePique
    global ult_posible_pique
    global TiempoDifVelocidad
    global es_pique
    global velocidad
    global afterVelocidad
    global radio
    global diferente
    global x
    global y
    global punto1Velocidad  
    global velocidadFinal
    global casiCentro
    global numeroFrame
    global radioDeteccionPorCirculo
    global circulosAIgnorar
    global preCentroConDecimales
    global centroConDecimales
    global deteccionPorColor
    global corregir
    global color_pre_centro
    global ultimosCentrosGlobales
    global pre_centro_lista

    # Agrandamos el frame para ver más la pelota
    

    frameCopia = frame.copy()

    # if numeroFrame == 332:
    #     frameCopia2 = frame.copy()
    #     lista = [(3139, 1599), (3138, 1599), (3138, 1600), (3139, 1600), (3140, 1599), (3140, 1600), (3137, 1599), (3137, 1600), (3137, 1601), (3138, 1601), (3139, 1601), (3140, 1601), (3141, 1599), (3141, 1600), (3141, 1601), (3136, 1599), (3136, 1600), (3136, 1601), (3138, 1602), (3139, 1602), (3140, 1602), (3142, 1599), (3142, 1600), (3142, 1601), (3135, 1599), (3135, 1600), (3135, 1601), (3138, 1603), (3139, 1603), (3140, 1603), (3143, 1599), (3143, 1600), (3143, 1601), (3138, 1604), (3139, 1604), (3140, 1604)]
    #     for punto in lista:
    #         frameCopia2[punto[1], punto[0]] = (0, 0, 0)
    #     cv2.imwrite("FrameCopia2-332.jpg", frameCopia2)


    ultimosFrames.append(frameCopia)

    # if numeroFrame == 100:
    #     # Agrandamos el frame para ver más la pelota
    #     frame3 = frame
    #     frame3 = imutils.resize(frame3, frame3.shape[1] * resizer, frame3.shape[0] * resizer)

    #     # Convertir la imagen a escala de grises
    #     imagen_gris3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)

    #     # Aplicar un suavizado si es necesario
    #     blurred3 = cv2.GaussianBlur(imagen_gris3, (11, 11), 0)

    #     # Buscamos los círculos en la imágen
    #     circles3 = cv2.HoughCircles(blurred3, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40, param1=50, param2=25, minRadius=5, maxRadius=100)

    #     for circle in circles3[0]:
    #         cv2.circle(frame3, (int(circle[0]), int(circle[1])), int(circle[2]), (255, 255, 255), 2)
        
    #     cv2.imwrite("Todos_Circulos_Frame_5.jpg", frame3)

    # if numeroFrame == 1:
    #     frame3 = frame
    #     frame3 = imutils.resize(frame3, frame3.shape[1] * resizer, frame3.shape[0] * resizer)
    #     for circle in circulosAIgnorar:
    #         cv2.circle(frame3, (int(circle[0]), int(circle[1])), int(circle[2]), (255, 255, 255), 2)
    #     cv2.imwrite("Todos_Circulos.jpg", frame3)


    if circulosAIgnorar is None:
        if (numeroFrame == 1 or numeroFrame == 2 or numeroFrame == 3 or numeroFrame == 4 or numeroFrame == 5):
            # Hacemos una copia del frame
            frame2 = frame.copy()

            # Agrandamos el frame para ver más la pelota
            frame2 = imutils.resize(frame2, frame2.shape[1] * resizer, frame2.shape[0] * resizer)

            # Convertir la imagen a escala de grises
            imagen_gris2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            # Aplicar un suavizado si es necesario
            blurred2 = cv2.GaussianBlur(imagen_gris2, (11, 11), 0)

            # Buscamos los círculos en la imágen
            circles = cv2.HoughCircles(blurred2, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40, param1=50, param2=25, minRadius=5, maxRadius=100)

            circulosInmoviles(circles)

    # Cámara lenta para mayor análisis
    #cv2.waitKey(100)
    
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # Filtra los tonos verdes de la imagen
    #mascara = cv2.inRange(hsv, greenLower, greenUpper)
    #mascara = cv2.erode(mascara, None, iterations=2)
    #mascara = cv2.dilate(mascara, None, iterations=2)
    
    # Toma todos los contornos de la imagen
    #contornos = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #contornos = imutils.grab_contours(contornos)

    # GaussianBlur reduce el ruido de alta frecuencia
    # MedianBlur elimina el ruido impulsivo

    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    blurred = cv2.medianBlur(frame, 5)

    # Convertir la imagen a formato HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Aplicar una máscara para detectar el color verde. En la máscara se muestran en color blanco todos los contornos detectados que sean de color verde
    mascara = cv2.inRange(hsv, greenLower, greenUpper)

    # Aplicar operaciones de morfología
    kernel = np.ones((5, 5), np.uint8)
    # Eliminar los píxeles de los objetos que están en los bordes de las regiones.
    #mascara = cv2.erode(mascara, kernel, iterations=2)
    # Dilatar los píxeles para que se vean mejor
    mascara = cv2.dilate(mascara, kernel, iterations=2)

    #mascara = cv2.erode(mascara, None, iterations=2)
    #mascara = cv2.dilate(mascara, None, iterations=2)

    # Encontrar los contornos en la máscara
    casi_contornos, _ = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar los contornos en la imagen original
    #cv2.drawContours(frame, contornos, -1, (0, 255, 0), 2)

    # Dibujar los contornos en la imagen original
    #cv2.drawContours(frame, contornos, -1, (0, 255, 0), 2)

    # # Convertir el frame a escala de grises
    # gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # suavizado = cv2.GaussianBlur(gris, (5, 5), 0)

    # # Busca los círculos en la imagen utilizando HoughCircles
    # circles = cv2.HoughCircles(suavizado, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=30)
    
    # # Si se encuentran círculos, dibújalos en la imagen original
    # if circles is not None:
    #     circles = np.round(circles[0, :]).astype(int)
    #     for (x, y, r) in circles:
    #         cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

    centro = None
    
    # Cada 5 segundos elimina los contornos que no son tan frecuentes, es decir, los contornos parecidos que no aparecen tanto a lo largo del video
    if (TiempoSegundosEmpezoVideo % 5 == 0):
        eliminarContornosInservibles(todosContornos)
    
    if len(casi_contornos) > 0:
        contornos = []
        for contorno in casi_contornos:
            M = cv2.moments(contorno)
            if M["m00"] > 0: centroPosible = (M["m10"] / M["m00"], M["m01"] / M["m00"])
            if len(ultimosFrames) >= 5 and pixelColorIgual(centroPosible, list(ultimosFrames)[-5:], False) == False: contornos.append(contorno)
            elif len(ultimosFrames) < 5: contornos.append(contorno)

        # Vemos cuales son los contornos casi inmóviles y si lo que considera que es la pelota no se está moviendo (o sea no es la pelota) se ignoran estos contornos.
        contornosQuietos(contornos, todosContornos, contornosIgnorar)
        if len(ultimosCentros) >= 5 and seEstaMoviendo(ultimosCentros, 7) == False or len(ultimosCentros) == 10 and deteccionNoEsLaPelota(ultimosCentros, 15, False):
            contornos = ignorarContornosQuietos(contornos, contornosIgnorar)
            primeraVez = True
            preCentro = None
            TiempoDeteccionUltimaPelota += 1/fps
            TiempoTresCentrosConsecutivos = 0

        if len(contornos) > 0:
            deteccionColorEsteFrame = []
            for contorno in contornos:
                ((x, y), radio) = cv2.minEnclosingCircle(contorno)
                M = cv2.moments(contorno)
                if M["m00"] > 0: centroConDecimales = (M["m10"] / M["m00"], M["m01"] / M["m00"]), radio
                deteccionColorEsteFrame.append(centroConDecimales)
            
            deteccionColorUltimosFrames.append(deteccionColorEsteFrame)
            # Cuando empezó el video o pasaron 0.3 segundos desde que no se encuentra la pelota
            if primeraVez:
                # Busca el contorno más grande y encuentra su posición (x, y). Determina el centro de la pelota
                casiCentro = max(contornos, key=cv2.contourArea)
                ((x, y), radio) = cv2.minEnclosingCircle(casiCentro)
                M = cv2.moments(casiCentro)
                if M["m00"] > 0: 
                    centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), int(radio)
                    centroConDecimales = (M["m10"] / M["m00"], M["m01"] / M["m00"]), radio
                primeraVez = False
                #preCentro = centro
                TiempoDeteccionUltimaPelota = 0
                TiempoTresCentrosConsecutivos = 0
                deteccionPorColor = True

                print("Deteccion por color")

                if centro is not None: ultimosCentros.appendleft(centroConDecimales)

            # Si se detectó un centro hace menos de 0.3 segundos
            else:
                # Corre la función tp_fix para determinar cual es el contorno detectado que está mas cerca de la pelota del frame anterior, es decir, encuentra la peltoa a través de su posición en el frame anterior
                if preCentro is not None: casiCentro = tp_fix(contornos, preCentro, TiempoDeteccionUltimaPelota, False, None, None, False, False)
                
                # Encuentra la posición x, y del contorno más cercano a la pelota del frame anterior. Determina el centro de la pelota
                if casiCentro is not None:
                    ((x, y), radio) = cv2.minEnclosingCircle(casiCentro)
                    M = cv2.moments(casiCentro)
                    if M["m00"] > 0: 
                        centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), int(radio)
                        centroConDecimales = (M["m10"] / M["m00"], M["m01"] / M["m00"]), radio
                    #preCentro = centro
                    TiempoTresCentrosConsecutivos += TiempoDeteccionUltimaPelota
                    TiempoDeteccionUltimaPelota = 0
                    deteccionPorColor = True

                    print("Deteccion por color")

                    if centro is not None: ultimosCentros.appendleft(centroConDecimales)
                
                # Si no se encuentra la pelota, se cambian algunas variables para poder determinar mejor su posición en los siguientes frame
                else:
                    if TiempoDeteccionUltimaPelota >= 0.3:
                        primeraVez = True
                        preCentro = None
                    TiempoDeteccionUltimaPelota += 1/fps
                    TiempoTresCentrosConsecutivos = 0
                
            # Sigue si el contorno tiene cierto tamaño
            if radio > 0 and casiCentro is not None and centro is not None:
                # Dibuja el círculo en la pelota
                cv2.circle(frame, (int(x), int(y)), int(radio), (0, 255, 255), 2)
                #cv2.circle(frame, (centro[0][0], centro[0][1]), 5, (0, 0, 255), -1)
        
        # Si no se encuentra la pelota, se cambian algunas variables para poder determinar mejor su posición en los siguientes frame
        else:
            if TiempoDeteccionUltimaPelota >= 0.3:
                primeraVez = True
                preCentro = None
            TiempoDeteccionUltimaPelota += 1/fps
            TiempoTresCentrosConsecutivos = 0
            deteccionColorUltimosFrames.append(None)
    
    # Si no se encuentra la pelota, se cambian algunas variables para poder determinar mejor su posición en los siguientes frame
    else:
        if TiempoDeteccionUltimaPelota >= 0.3:
            primeraVez = True
            preCentro = None
        TiempoDeteccionUltimaPelota += 1/fps
        TiempoTresCentrosConsecutivos = 0
        deteccionColorUltimosFrames.append(None)

    if numeroFrame == 317: cv2.imwrite("Frame317.jpg", frame)
    #if numeroFrame == 51: cv2.imwrite("Frame51.jpg", frame)
    #if numeroFrame == 52: cv2.imwrite("Frame52.jpg", frame)
    #if numeroFrame == 53: cv2.imwrite("Frame53.jpg", frame)
    #if numeroFrame == 54: cv2.imwrite("Frame54.jpg", frame)
    #if numeroFrame == 55: cv2.imwrite("Frame55.jpg", frame)
    #if numeroFrame == 56: cv2.imwrite("Frame56.jpg", frame)

    #if numeroFrame == 18: cv2.imwrite("Frame18.jpg", frame)
    #if numeroFrame == 19: cv2.imwrite("Frame19.jpg", frame)

    #ultFrames.appendleft(imutils.resize(frame, anchoOG, altoOG))
    ultFrames.appendleft(frame)

    #if numeroFrame == 54: cv2.imwrite("FrameCopia54.jpg", frameCopia)

    if centro is None and preCentro is not None:
        centro = deteccionPorCirculos(preCentro, frame, recorteCerca, False, color_pre_centro, 3)

        if len(ultimosCentrosGlobales) == 14 and len(ultimosCentrosCirculo) >= 8:
            if seEstaMoviendo(list(ultimosCentrosCirculo)[:5], 7) == False and corregir[1] == 0 or deteccionNoEsLaPelota(ultimosCentrosCirculo, 5, False) and corregir[1] == 0:
                corregir = (True, numeroFrame + 2)
                print(f"{bcolors.FAIL}Warning: No active frommets remain. Continue?{bcolors.ENDC}")
        
        elif len(ultimosCentrosCirculo) >= 8:
            if seEstaMoviendo(list(ultimosCentrosCirculo)[:5], 7) == False or deteccionNoEsLaPelota(ultimosCentrosCirculo, 5, False):
                primeraVez = True
                preCentro = None
                TiempoDeteccionUltimaPelota += 1/fps
                TiempoTresCentrosConsecutivos = 0
        
    else: 
        if radio is not None: 
            radioDeteccionPorCirculo = radio
    
    if corregir[0] == True and numeroFrame == corregir[1]:
        #corregirPosicionPelota(ultimosCentrosGlobales)
        corregir = (False, 0)
        #primeraVez = True
        ultimosCentrosCirculo.clear()

    #if len(ultimosCentrosGlobales) >= 10 and abs(ultimosCentrosGlobales[0][1] - ultimosCentrosGlobales[1][1]) > 2:

    # if centro is None:
    #     if TiempoDeteccionUltimaPelota >= 0.3:
    #         primeraVez = True
    #         preCentro = None
    #     TiempoDeteccionUltimaPelota += 1/fps
    #     TiempoTresCentrosConsecutivos = 0
    
    # Actualiza los puntos para trazar la trayectoria de la pelota
    pts_pelota_norm.appendleft(centro)

    for i in range(1, len(pts_pelota_norm)):
        # Ignora los puntos de trayectoria inexistentes
        if pts_pelota_norm[i - 1] is None or pts_pelota_norm[i] is None:
            continue
        
        # Traza la trayectoria
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts_pelota_norm[i - 1][0], pts_pelota_norm[i][0], (0, 0, 255), thickness)
    
    bajando = False

    # Determina si la pelota está bajando o subiendo.
    if centro is not None:
        centros_para_determinar_pique.appendleft(centro[0][1])
        if (len(centros_para_determinar_pique) >= 2):
            if (centros_para_determinar_pique[0] - centros_para_determinar_pique[1] > 0):
                bajando = True
            if (centros_para_determinar_pique[0] - centros_para_determinar_pique[1] != 0):
                # Agrega todos los booleanos de bajando a una lista para luego determinar si hay un posiblePique
                bajandos.appendleft((bajando, numeroFrame))
            else: bajando = None
    
    TiempoDifPiques += 1/fps
    posiblePique = False
    # Cuando la pelota esta bajando y empieza a subir, significa que hay un posiblePique, es decir se detectó un pique o golpe. Luego se hará la diferenciación
    if (len(bajandos) >= 2):
        if bajandos[0][0] == False and bajandos[1][0] == True and preCentro is not None and bajandos[0][1] - bajandos[1][1] <= fps/6 and centro is not None:
            posiblePique = True
            if len(posiblesPiques) % 2 == 1: TiempoDifPiques = 0
    
    # Entra a este if cuando se determina que hay un posiblePique, es decir, que se detectó algo que no se puede determinar si es un pique o un golpe
    if posiblePique:
        if (len(bajandos) >= 2):
            # Determina si el preCentro está sobre el plano 2D
            pre_esta_en_cancha = estaEnCancha(preCentro, False)
            # Entra a este if cuanda la pelota no esté en la cancha. Al no estar en la cancha, solo puedo determinar si está por encima o por debajo de la red para luego determinar si un posiblePique es pique o golpe.
            if not pre_esta_en_cancha:
                # Abajo es True o False dependiendo de su coordenada Y (Abajo se refiere a por debajo de la red al pasar la cancha a un plano 2D)
                mitadDeCancha = (puntoMaximoAbajoCancha - puntoMaximoArribaCancha) / 2
                if preCentro[0][1] <= mitadDeCancha: abajo = False
                else: abajo = True

                # En caso que la lista de posiblesPiques esté vacía o no se repita un punto de posiblePique, se agrega a esa lista si la pelota está abajo o arriba, la coordenada de la pelota pasada a un plano 2D y el número de Frame 
                if posiblesPiques == []:
                    posiblesPiques.appendleft((abajo, coordenadaPorMatriz(preCentro), numeroFrame))
                    ult_posible_pique = preCentro[0]
                elif preCentro[0] != ult_posible_pique:
                    posiblesPiques.appendleft((abajo, coordenadaPorMatriz(preCentro), numeroFrame))
                    ult_posible_pique = preCentro[0]

                # Si hay más de dos posiblesPiques podemos determinar piques y golpes
                if len(posiblesPiques) >= 2:
                    # Corremos la función pica para determinar si el anteúltimo posiblePique detectado es un pique o un golpe
                    es_pique = pica(TiempoDifPiques)
                    # Vemos si el posiblePique analizado se encuentra adentro del plano 2D
                    # Debemos determinar que el tipo de posiblesPiques[1][0] no sea un booleano porque eso significaría que sería el booleano abajo que fue agregado a la lista. Como el abajo significa que la pelota está fuera de la cancha, entonces no se puede determinar si es un pique no un golpe.
                    if type(posiblesPiques[1][0]) is not bool: esta_en_cancha_posible_pique = estaEnCancha(posiblesPiques[1], True)
                    
                    # Entra cuando se detectó un pique que se encuentra en el plano 2D.
                    if es_pique and type(posiblesPiques[1][0]) is not bool and esta_en_cancha_posible_pique:                     
                        pts_piques_finales.append([posiblesPiques[1][0], float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                    
                    # Entra cuando se detectó un pique que no se encuentra en el plano 2D.    
                    elif es_pique and type(posiblesPiques[1][0]) is not bool and not esta_en_cancha_posible_pique:                     
                        pts_piques_finales_afuera.append([posiblesPiques[1][0], float("{:.2f}".format(posiblesPiques[1][1] / fps))])

                    # Entra cuando se detectó un golpe
                    elif es_pique == False and type(posiblesPiques[1][0]) is not bool:
                        pts_golpes_finales.append([posiblesPiques[1][0], float("{:.2f}".format(posiblesPiques[1][1] / fps))])

                    # En cada caso, se agrega a la lista correspondiente el punto de pique o golpe sobre el plano 2D.
            
            # Entra a este if cuando la pelota está en la perspectiva. 
            elif pre_esta_en_cancha:
                # En caso que la lista de posiblesPiques esté vacía o no se repita un punto de posiblePique, se agrega a esa lista la coordenada de la pelota pasada a un plano 2D y el número de Frame 
                if posiblesPiques == []:
                    posiblesPiques.appendleft((coordenadaPorMatriz(preCentro), numeroFrame))
                    ult_posible_pique = preCentro[0]
                elif ult_posible_pique != preCentro[0]:
                    posiblesPiques.appendleft((coordenadaPorMatriz(preCentro), numeroFrame))
                    ult_posible_pique = preCentro[0]
                
                # Si hay más de dos posiblesPiques podemos determinar piques y golpes
                if len(posiblesPiques) >= 2:
                    # Corremos la función pica para determinar si el anteúltimo posiblePique detectado es un pique o un golpe
                    es_pique = pica(TiempoDifPiques)
                    
                    # Vemos si el posiblePique analizado se encuentra adentro del plano 2D
                    # Debemos determinar que el tipo de posiblesPiques[1][0] no sea un booleano porque eso significaría que sería el booleano abajo que fue agregado a la lista. Como el abajo significa que la pelota está fuera de la cancha, entonces no se puede determinar si es un pique no un golpe.
                    if type(posiblesPiques[1][0]) is not bool: esta_en_cancha_posible_pique = estaEnCancha(posiblesPiques[1], True)

                    velocidad = True
                    punto1Velocidad = preCentro
                    TiempoDifVelocidad += 1/fps
                    
                    # Entra cuando se detectó un pique que se encuentra en el plano 2D.
                    if es_pique and type(posiblesPiques[1][0]) is not bool and esta_en_cancha_posible_pique:
                        pts_piques_finales.append([posiblesPiques[1][0], float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                    
                    # Entra cuando se detectó un pique que no se encuentra en el plano 2D.  
                    elif es_pique and type(posiblesPiques[1][0]) is not bool and not esta_en_cancha_posible_pique:                     
                        pts_piques_finales_afuera.append([posiblesPiques[1][0], float("{:.2f}".format(posiblesPiques[1][1] / fps))])

                    # Entra cuando se detectó un golpe
                    elif es_pique == False and type(posiblesPiques[1][0]) is not bool:
                        pts_golpes_finales.append([posiblesPiques[1][0], float("{:.2f}".format(posiblesPiques[1][1] / fps))])

                    # En cada caso, se agrega a la lista correspondiente el punto de pique o golpe sobre el plano 2D.

                    TiempoDifPiques = 0
    
    # Si no se detectó ni un pique ni golpe, entonces es_pique es None. 
    if es_pique is not None:
        es_pique = None
    
    # Determino si el centro está dentro del plano 2D.
    centro_esta_en_cancha = estaEnCancha(centro, False)

    # Se detecta la velocidad cuando hay un pique o un golpe.
    if velocidad and centro_esta_en_cancha and punto1Velocidad is not None:
        # Cuando los puntos para calcular la velocidad son diferentes.
        if punto1Velocidad[0] != centro[0] or punto1Velocidad[0][1] != centro[0][1]:
            diferente = True
    
    # Calculamos la velocidad de la pelota
    if velocidad and centro_esta_en_cancha and diferente:
        velocidadFinal = velocidadPelota(punto1Velocidad, centro, TiempoDifVelocidad)
        velocidad = False
        punto1Velocidad = None
        TiempoDifVelocidad = 0
        diferente = False
        afterVelocidad = True

    # Si no encuentro el segundo punto para calcular la velocidad.
    elif velocidad:
        TiempoDifVelocidad += 1/fps

    # En caso de que el tiempo que haya pasado entre la detección de los dos puntos sea muy grande.
    elif TiempoDifVelocidad >= 0.5:
        TiempoDifVelocidad = 0
        velocidad = False
        punto1Velocidad = None
        diferente = False

    # Cuando calculé la velocidad
    if afterVelocidad and centro is not None:
        afterVelocidad = False

    #if numeroFrame == 338: cv2.imwrite("Frame338Copia.jpg", frameCopia)
    #if numeroFrame == 339: cv2.imwrite("Frame339Copia.jpg", frameCopia)
    #if numeroFrame == 340: cv2.imwrite("Frame340Copia.jpg", frameCopia)
    #if numeroFrame == 341: cv2.imwrite("Frame341Copia.jpg", frameCopia)
    #if numeroFrame == 342: cv2.imwrite("Frame342Copia.jpg", frameCopia)

    if centro is not None:
        centro, centroConDecimales, radioDeteccionPorCirculo, color_pre_centro, pre_centro_lista = circuloPorCentro(frameCopia, centro, False, pre_centro_lista)

    if centro is not None: ultimosCentrosGlobales.append((centroConDecimales, deteccionPorColor, frameCopia, color_pre_centro, preCentro))

    if centro is not None:
        preCentro = centro
        preCentroConDecimales = centroConDecimales

    if deteccionPorColor == False: ultimosCentrosCirculo.appendleft(centroConDecimales)
        
    print("Color centro", color_pre_centro)
    print("Centro", centro)
    print("Centro con decimales", centroConDecimales)
    print("Len centro lista", len(pre_centro_lista))

    #if numeroFrame == 339: 
    #    for centro, *_ in ultimosCentrosGlobales:
    #        print("Centro", centro)
    #print("Radio de la pelota", radio)
    #print("Radio de la pelota de verdad", radioDeteccionPorCirculo)

    #if len(ultimosCentrosGlobales) == 14: print("CambiosDeDireccion", cambiosDeDireccion(ultimosCentrosGlobales))
    if len(ultimosCentrosGlobales) >= 7: cambiosDeDireccion(list(ultimosCentrosGlobales)[-7:], False, ultimosCentrosGlobales)
    #print("Ultimos Centros Globales", ultimosCentrosGlobales)

    #if numeroFrame == 14 or numeroFrame == 15 or numeroFrame == 16 or numeroFrame == 17 or numeroFrame == 18 or numeroFrame == 19 or numeroFrame == 20:
    #    cv2.imwrite("Frame" + str(numeroFrame) + "---AAA" +".jpg", frame)
    
    # Resizea el frame al tamaño original y lo muestra
    frame = imutils.resize(frame, anchoOG, altoOG)
    frame = imutils.resize(frame, height= 700)
    frameCopia = imutils.resize(frameCopia, anchoOG, altoOG)
    frameCopia = imutils.resize(frameCopia, height= 700)
    mascara = imutils.resize(mascara, anchoOG, altoOG)
    mascara = imutils.resize(mascara, height= 700)
    
    # También muestra la máscara
    cv2.imshow("Mascara Normal", mascara)
    cv2.imshow("Copia", frameCopia)
    cv2.imshow("Normal", frame)

    return frame


# Función que recibe el centro de la pelota y pasa sus coordenadas a un plano 2D de la cancha de tenis
def coordenadaPorMatriz(centro, *args):
    # Adapto la variable centro para que sea siempre de esta forma ((x, y), r)
    if type(centro) is list:
        centro = (centro, 0)
    pts1 = np.float32([[topLeftX, topLeftY],[topRightX, topRightY],[bottomLeftX, bottomLeftY],[bottomRightX, bottomRightY]])
    pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

    # Pasamos las esquinas a perspectiva
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    perspectiva = cv2.warpPerspective(frame, matrix, (164, 474))

    if args is not None:
        cords_medio = np.array([[0 / resizer], [237 / resizer], [1]])
        cords_medio_pers = np.dot(matrix, cords_medio)
        cords_medio_pers = (int(np.rint(cords_medio_pers[0]/cords_medio_pers[2])), int(np.rint(cords_medio_pers[1]/cords_medio_pers[2])))
        return cords_medio_pers

    # Determinamos la posición de la pelota en la perspectiva
    cords_pelota = np.array([[centro[0][0] / resizer], [centro[0][1] / resizer], [1]])
    cords_pelota_pers = np.dot(matrix, cords_pelota)
    cords_pelota_pers = (int(np.rint(cords_pelota_pers[0]/cords_pelota_pers[2])), int(np.rint(cords_pelota_pers[1]/cords_pelota_pers[2])))

    perspectiva = cv2.circle(perspectiva, cords_pelota_pers, 3, (0, 0, 255), -1)
    cv2.imshow("Perspectiva", perspectiva)

    # Devolvemos el punto pasado al plano 2D.
    return cords_pelota_pers

# Función que elimina los contornos que no son tan frecuentes, es decir, los contornos parecidos que no aparecen tanto a lo largo del video
def eliminarContornosInservibles(todosContornos):
    count = 0
    aBorrar = []
    for circulos_cercanos in todosContornos:
        # Si los círculos cercanos detectados no son tan frecuentes (detecté menos de 5 parecidos)
        if (len(circulos_cercanos) <= 5):
            # Agrego en la lista el index de aquellos contornos que tengo que borrar de todosContornos (lista que contiene todos los contornos de todos los frames)
            aBorrar.append(count)
        count += 1
    
    # Borramos de todosContornos los no frecuentes a partir de su posición.
    n = 0
    for i in aBorrar:
        todosContornos.pop(i - n)
        n += 1

# Define todos los contornos que no se mueven, es decir, que no pueden ser la pelota
def contornosQuietos(cnts, todosContornos, contornosIgnorar):
    # todosContornos es una lista que contiene todos los contornos de todo el video.
    # Está dividida de la siguiente manera: Contiene listas adentro de todosContornos, cada una de estas listas contiene círculos que están cerca entre si.
    centrosCerca = False
    # Analizo cada contorno del frame actual.
    for contorno in cnts:
        count = 0
        # Círculo del contorno
        (x, y), radius = cv2.minEnclosingCircle(contorno)
        x, y, radius = int(x), int(y), int(radius)
        for circulos_cercanos in todosContornos:
            for circulo in circulos_cercanos:
                # Si el círculo de una lista dentro de todosContornos está cerca del contorno siendo analizado, entonces centrosCerca es True, de lo contrario, es False.
                if x - circulo[0][0] >= -10 and x - circulo[0][0] <= 10 and y - circulo[0][1] >= -10 and y - circulo[0][1] <= 10:
                    centrosCerca = True
                else:
                    centrosCerca = False
                    break
            # Cuando está cerca, entonces agrego a la lista dentro de todosContornos que está cerca al contorno siendo analizado el centro de la pelota
            if centrosCerca:
                todosContornos[count].append([(x, y, radius)])
                break
            count += 1
        # Si no está cerca, entonces creo una nueva lista en todosContornos con el centro de la pelota.
        if centrosCerca == False:
            todosContornos.append([[(x, y, radius)]])
    
    # Luego de agregar los círuclos en todosContornos en donde corresponda
    for circulos_cercanos in todosContornos:
        ContornoExiste = False
        # Cuando una lista dentro de todosContornos tiene más de 10 círculos cercanos.
        if (len(circulos_cercanos) >= 10):
            # Se calcula el promedio en x, y de cada una de las listas que tienen más de 10 círuclos cercanos
            promedioIgnorarX = 0
            promedioIgnorarY = 0
            for circulo in circulos_cercanos:
                promedioIgnorarX += circulo[0][0]
                promedioIgnorarY += circulo[0][1]
            promedioIgnorarX /= len(circulos_cercanos)
            promedioIgnorarY /= len(circulos_cercanos)
            promedioIgnorarX, promedioIgnorarY = int(np.rint(promedioIgnorarX)), int(np.rint(promedioIgnorarY))
            # Se agregan los contornos que se deben ignorar (el promedio) a contornosIgnorar
            if (len(contornosIgnorar) == 0): contornosIgnorar.append((promedioIgnorarX, promedioIgnorarY))
            # Si el contorno no existe en la lista
            for contorno in contornosIgnorar:
                if (contorno[0] == promedioIgnorarX and contorno[1] == promedioIgnorarY):
                    ContornoExiste = True
            if ContornoExiste == False:
                contornosIgnorar.append((promedioIgnorarX, promedioIgnorarY))

# Ignora los contornos quietos encontrados en la función anterior
def ignorarContornosQuietos(cnts, contornosIgnorar):
    new_cnts = []
    Ignorar = False
    for cnt in cnts:
        (x, y), _ = cv2.minEnclosingCircle(cnt)
        # Por cada contorno del frame actual, verifico si es parecido a algún valor de la lista de contornosIgnorar.
        for cnt_a_ignorar in contornosIgnorar:
            if x - cnt_a_ignorar[0] >= -20 and x - cnt_a_ignorar[0] <= 20 and y - cnt_a_ignorar[1] >= -20 and y - cnt_a_ignorar[1] <= 20:
                Ignorar = True
                break
            else:
                Ignorar = False
        
        # En caso de que no tenga que ignorar el contorno siendo analizado, es decir, que no esté cerca de ninguno de los puntos de contornosIgnorar, lo agrego a una nueva lista 
        if Ignorar == False: new_cnts.append(cnt)
    
    # Luego devuelvo esa nueva lista
    return new_cnts

# Fución que determina si la pelota se está moviendo
def seEstaMoviendo(ultCentros, rango):
    #print("AAAAAAAAAAAAA")
    print("ultCentros", ultCentros)

    movimiento = False
    # Si la suma de las restas de los últimos centros es mayor a 15, significa que la pelota se está moviendo, de lo contrario no lo está.
    for i in range(2):
        restaA = abs(ultCentros[4][0][i] - ultCentros[3][0][i])
        restaB = abs(ultCentros[3][0][i] - ultCentros[2][0][i])
        restaC = abs(ultCentros[2][0][i] - ultCentros[1][0][i])
        restaD = abs(ultCentros[1][0][i] - ultCentros[0][0][i])
        #print("Resta A: ", restaA)
        #print("Resta B: ", restaB)
        #print("Resta C: ", restaC)
        #print("Resta D: ", restaD)
        if restaA + restaB + restaC + restaD >= rango:
            movimiento = True
            break
        else:
            movimiento = False
    
    #restaA = abs(ultCentros[4][1] - ultCentros[3][1])
    #restaB = abs(ultCentros[3][1] - ultCentros[2][1])
    #restaC = abs(ultCentros[2][1] - ultCentros[1][1])
    #restaD = abs(ultCentros[1][1] - ultCentros[0][1])

    #if restaA + restaB + restaC + restaD >= 3:
    #    movimiento = True
    #else:
    #    movimiento = False
    
    # Devuelve True o False dependiendo de si la pelota se mueve o no
    if movimiento:
        return True
    return False

# Función que arregla el problema de "la zapatilla verde"
def tp_fix(contornos, pre_centro, count, circulo, imagen_recortada, xy1, correcion, verdeCerca):
    cnts_pts = []
    medidorX = 100
    medidorY = 103
    for contorno in contornos:
        if circulo == False:
            if verdeCerca == False: ((x, y), _) = cv2.minEnclosingCircle(contorno)
            else: ((x, y), _) = contorno
            # cnts_pts tiene aquellos contornos del frame actual que están cerca del pre_centro en las coordenadas x,y. 
            if x - pre_centro[0][0] > medidorX * resizer or pre_centro[0][0] - x > medidorX * resizer or y - pre_centro[0][1] > medidorY * resizer or pre_centro[0][1] - y > medidorY * resizer and count <= 0.5:
                continue
            cnts_pts.append(contorno)
        elif correcion: cnts_pts.append(contorno)
        else:
            x, y, radius = contorno
            ignorar = False
            for circulo in circulosAIgnorar:
                if xy1[0] * resizer + x == circulo[0] and xy1[1] * resizer + y == circulo[1] and radius == circulo[2]:
                    ignorar = True
                    break
            if not ignorar:
                #if numeroFrame > 52 and numeroFrame < 57: 
                    #cv2.imwrite("imagen_recortada55.png", imagen_recortada)
                    #print("X, y, radius", x, y, radius)
                    #if abs(radius - 15) > 15 and count <= 0.5:
                        #continue
                #else:  
                if abs(radius - pre_centro[1]) > 15 and count <= 0.5:
                    continue
                #if imagen_recortada is not None: cv2.circle(imagen_recortada, (int(x), int(y)), int(radius + 20), (255, 255, 255), 5)
                cnts_pts.append(contorno)
    if cnts_pts != []:
        #print("Len cnts_pts: ", len(cnts_pts))
        # Devuelve la función cualEstaMasCerca con los parametros obtenidos en la función
        return cualEstaMasCerca(pre_centro, cnts_pts, circulo, verdeCerca, correcion)
    return None

# Define qué candidato a pelota es el punto más cercano al anterior. Toma los puntos de tp_fix y analiza cual está mas cerca al pre_centro (centro anterior).
def cualEstaMasCerca(punto, lista, circulo, verdeCerca, correcion):
    suma = []
    suma2 = []
    for i in lista:
        # Obtenemos las diferencias entre el preCentro y el círculo a comparar que proviene del contorno.
        if circulo: xCenter, yCenter, radius = i
        else: 
            if verdeCerca: (xCenter, yCenter), radius = i 
            else: (xCenter, yCenter), radius = cv2.minEnclosingCircle(i)
        difEnX = abs(int(xCenter) - int(punto[0][0]))
        difEnY = abs(int(yCenter) - int(punto[0][1]))
        difRadio = abs(int(radius) - int(punto[1]))
        
        # Guardamos los valores en listas
        if correcion and difRadio <= 15:
            suma.append(difEnX + difEnY + difRadio * 3)
            suma2.append(i)

        if correcion == False:
            suma.append(difEnX + difEnY + difRadio * 3)
            suma2.append(i)

    # Devolvemos el valor más chico que representa el círculo a menor distancia del preCentro
    if len(suma2) > 0: return suma2[suma.index(min(suma))]
    return None

# Función que determina si es un pique o un golpe
def pica (count):
    # Tengo que descubrir si la variable "b" es un pique o un golpe
    # Si es un pique, se devuelve True, de lo contrario se devuelve False
    # A partir de la posición de los dos últimos posiblesPiques se determina si el anteútimo es pique o golpe

    if type(posiblesPiques[0][0]) is not bool and type(posiblesPiques[1][0]) is not bool:
        abajoA = False
        abajoB = False
        a = posiblesPiques[0][0][1]
        b = posiblesPiques[1][0][1]
        if a >= 474 / 2: abajoA = True
        if b >= 474 / 2: abajoB = True
        if abajoB and abajoA and a > b and count <= 1:
            return True
        elif abajoB and abajoA and a > b and count >= 1:
            return True
        elif abajoB and abajoA and a < b and count >= 2.5:
            return True
        elif abajoB and abajoA and a < b and count <= 2.5:
            return False
        elif abajoB and not abajoA and a < b and count <= 1.2:
            return True
        elif abajoB and not abajoA and a < b and count <= 2.5:
            return False
        elif abajoB and not abajoA and a < b and count >= 2.5:
            return True
        elif not abajoB and abajoA and a > b and count >= 1:
            return True
        elif not abajoB and abajoA and a > b and count <= 1:
            return False
        elif not abajoB and not abajoA and a > b and count <= 2:
            return False
        elif not abajoB and not abajoA and a > b and count >= 2:
            return True
        elif not abajoB and not abajoA and a < b and count >= 2:
            return False
        elif not abajoB and not abajoA and a < b and count <= 1.5:
            return True
        elif not abajoB and not abajoA and a < b and count <= 2:
            return False

    elif type(posiblesPiques[0][0]) is bool and type(posiblesPiques[1][0]) is bool:
        a = posiblesPiques[0][0]
        b = posiblesPiques[1][0]
        a2 = posiblesPiques[0][1]
        b2 = posiblesPiques[1][1]

        if a and b and a2 > b2 and count <= 2:
            return True
        elif a and b and a2 > b2 and count >= 2:
            return False
        elif a and b and a2 < b2 and count <= 6.5:
            return False
        elif a and b and a2 < b2 and count >= 6.5:
            return True
        elif a and not b and a2 > b2 and count <= 4:
            return False
        elif a and not b and a2 > b2 and count >= 4:
            return True
        elif not a and b and a2 < b2 and count <= 4:
            return False
        elif not a and b and a2 < b2 and count >= 4:
            return False
        elif not a and not b and a2 > b2 and count <= 6.5:
            return False
        elif not a and not b and a2 > b2 and count >= 6.5:
            return True
        elif not a and not b and a2 < b2 and count <= 2:
            return True
        elif not a and not b and a2 < b2 and count >= 2:
            return False
        
    elif type(posiblesPiques[0][0]) is bool:
        abajoB = False
        b = posiblesPiques[1][0][1]
        if b >= 474 / 2: abajoB = True

        a = posiblesPiques[0][0]

        if a and abajoB and count <= 2:
            return True
        elif a and abajoB and count >= 2:
            return True
        elif a and not abajoB and count <= 2.25:
            return False
        elif a and abajoB and count >= 2.25:
            return True
        elif not a and abajoB and count <= 1.5:
            return True
        elif not a and abajoB and count >= 1.5:
            return True
        elif not a and not abajoB and count <= 2:
            return True
        elif not a and not abajoB and count >= 2:
            return False

    elif type(posiblesPiques[1][0]) is bool:
        abajoA = False
        a = posiblesPiques[0][0][1]
        if a >= 474 / 2: abajoA = True

        b = posiblesPiques[1][0]

        if abajoA and b and count <= 5:
            return False
        elif abajoA and b and count >= 5:
            return True
        elif abajoA and not b and count <= 5:
            return False
        elif abajoA and not b and count >= 5:
            return True
        elif not abajoA and b and count <= 2.5:
            return False
        elif not abajoA and b and count >= 2.5:
            return True
        elif not abajoA and not b and count <= 5:
            return False
        elif not abajoA and not b and count >= 5:
            return True

def velocidadPelota(punto1, punto2, tiempo):
    # FALTA PASAR PUNTOS A PERSPECTIVA PARA CALCULAR LA VELOCIDAD

    # Calculamos distancias entre coordenadas de puntos
    punto1X = punto1[0][0] / (resizer * 20)
    punto1Y = punto1[0][1] / (resizer * 20)
    punto2X = punto2[0][0] / (resizer * 20)
    punto2Y = punto2[0][1] / (resizer * 20)

    # Hacemos pitagoras para calcular la hipotenusa entre ambos puntos
    if punto1X >= punto2X: movimientoX = punto1X - punto2X
    elif punto1X <= punto2X: movimientoX = punto2X - punto1X

    if punto1Y >= punto2Y: movimientoY = punto1Y - punto2Y
    elif punto1Y <= punto2Y: movimientoY = punto2Y - punto1Y

    distancia = np.sqrt(movimientoX * movimientoX + movimientoY * movimientoY)

    # Hacemos distancia / tiempo y obtenemos la velocidad
    return int(np.rint(distancia / tiempo * 3.6))

# Función para determinar si una pelota se encuentra dentro del plano 2D de la cancha
def estaEnCancha(centro_pelota, perspectiva):
    # Si cumple ciertos parametros está dentro, sino está fuera
    if perspectiva:
        if centro_pelota is not None and centro_pelota[0][1] <= 474 and centro_pelota[0][1] >= 0 and centro_pelota[0][0] <= 164 and centro_pelota[0][0] >= 0:
            return True
        elif centro_pelota is not None: 
            return False
        return None

    if centro_pelota is not None and centro_pelota[0][1] < puntoMaximoAbajoCancha * resizer and centro_pelota[0][1] > puntoMaximoArribaCancha * resizer and centro_pelota[0][0] < puntoMaximoDerechaCancha * resizer and centro_pelota[0][0] > puntoMaximoIzquierdaCancha * resizer:
        return True
    elif centro_pelota is not None: 
        return False
    return None

contadorCorreccion = 0

def deteccionPorCirculos(preCentro, frame, recorteCerca, correccion, color_pre_centro, resizer):
    global primeraVez
    global TiempoDeteccionUltimaPelota
    global radioDeteccionPorCirculo
    global centro
    global ultimosCentrosCirculo
    global centroConDecimales
    global deteccionPorColor
    global checkRecorteCerca
    global contadorCorreccion
    global radio

    # Ajustar los puntos de recorte si están fuera de rango
    x1 = max(preCentro[0][0] - recorteCerca, 0)
    y1 = max(preCentro[0][1] - recorteCerca, 0)
    x2 = min(preCentro[0][0] + recorteCerca, anchoOG * 3)
    y2 = min(preCentro[0][1] + recorteCerca, altoOG * 3)

    # Recortar la región de interés de la imagen original
    imagen_recortada = frame[int(y1):int(y2), int(x1):int(x2)]

    imagen_recortada_copia = imagen_recortada.copy()

    centro = None

    if numeroFrame == 317: cv2.imwrite("imagen_recortada317-SinCirculos.png", imagen_recortada)

    color_pre_centro = np.array([color_pre_centro[0], color_pre_centro[1], color_pre_centro[2]])
    
    # Inicializar una variable para el color más cercano y la distancia más corta
    color_mas_cercano = None
    distancia_mas_corta = float('inf')

    colores = {}
    pixelesColoresCercanos = []
    
    for i in range(imagen_recortada_copia.shape[1]):
        for h in range(imagen_recortada_copia.shape[0]):
            color = imagen_recortada_copia[h, i]
            #distancia = np.linalg.norm(color - color_pre_centro)
            distancia = abs(int(color[0]) - int(color_pre_centro[0])) + abs(int(color[1]) - int(color_pre_centro[1])) + abs(int(color[2]) - int(color_pre_centro[2]))

            colores[(i, h)] = color
            #if x1 + i == 3110 and y1 + h == 1540: print("Color", color)
            if distancia <= 30: pixelesColoresCercanos.append(((i, h), distancia, (np.sqrt(abs(imagen_recortada_copia.shape[1] / 2 - h) ** 2 + abs(imagen_recortada_copia.shape[0] / 2 - i) ** 2))))

            # Si la distancia actual es menor que la distancia más corta encontrada hasta ahora
            #if distancia < distancia_mas_corta:
            #    _, _, posibleNuevoRadio, _ = circuloPorCentro(ultimosFrames[-1], ((x1 + i, y1 + h), 5))
            #    if abs(posibleNuevoRadio - radioDeteccionPorCirculo) < 3:
            #        if len(ultimosFrames) >= 5 and pixelColorIgual((x1 + i, y1 + h), list(ultimosFrames)[-5:], False) == False:
            #            distancia_mas_corta = distancia
            #            color_mas_cercano = color
            #            pixel = (i, h)

            #        elif len(ultimosFrames) < 5:
            #            distancia_mas_corta = distancia
            #            color_mas_cercano = color
            #            pixel = (i, h)
    
    pixelesColoresCercanos = sorted(pixelesColoresCercanos, key=lambda x: x[2])
    #print("AAAAA", pixelesColoresCercanos[0:40])

    pixelesAnalizados = []
    centrosPosibles = []
    contador = 0
    pixel = None
    color_mas_cercano = None
    distancia_mas_corta = float('inf')

    for pixelCercano in pixelesColoresCercanos:
        if contador == 3: break
        if pixelCercano[0] in pixelesAnalizados: continue
        #print("Pixel Cercano", pixelCercano)
        posibleCentro, posibleCentroConDecimales, posibleNuevoRadio, posibleColorPreCentro, posibleCentroLista = circuloPorCentro(ultimosFrames[-1], ((x1 + pixelCercano[0][0], y1 + pixelCercano[0][1]), 5), False, pre_centro_lista)
        for i in posibleCentroLista: pixelesAnalizados.append((i[0] - x1, i[1] - y1))
        #print("Posible Nuevo Radio", posibleNuevoRadio)
        #print("Len posibleCentroLista", posibleCentroLista)
        if abs(posibleNuevoRadio - radioDeteccionPorCirculo) < 4:
            if len(ultimosFrames) >= 5 and pixelColorIgual((x1 + pixelCercano[0][0], y1 + pixelCercano[0][1]), list(ultimosFrames)[-5:], False) == False:
                if contador == 0:
                    distancia_mas_corta = pixelCercano[1]
                    color_mas_cercano = colores[pixelCercano[0]]
                    pixel = pixelCercano[0]
                centrosPosibles.append((posibleCentro, posibleColorPreCentro, posibleCentroLista))
                contador += 1

            elif len(ultimosFrames) < 5:
                if contador == 0:
                    distancia_mas_corta = pixelCercano[1]
                    color_mas_cercano = colores[pixelCercano[0]]
                    pixel = pixelCercano[0]
                centrosPosibles.append((posibleCentro, posibleColorPreCentro, posibleCentroLista))
                contador += 1
    
    if pixel is not None:
        ultimosPosiblesCentrosCirculo.append(centrosPosibles)

        print("Pixel Detectado", pixel)
        print("El color más cercano a", color_pre_centro, "es", color_mas_cercano)
        print("Distancia más corta", distancia_mas_corta)
    
        print(pixelColorIgual((x1 + pixel[0], y1 + pixel[1]), list(ultimosFrames)[-5:], True))
        #print("Centros posibles", centrosPosibles)

    if not correccion: ultimosSimilitudesCoseno.append(distancia_mas_corta)

    #if numeroFrame == 93: cv2.imwrite("imagen_recortada93SinCirculos.png", imagen_recortada_copia)

    # centro_lista = [(pixel)]
    # contador = 1

    # while contador > 0:
    #     contador = 0
    #     for pxl in centro_lista: 
    #         for i in range(-1, 2):
    #             for h in range(-1, 2):
    #                 #print("pxl: ", pxl[0] + i, pxl[1] + h)
    #                 if (pxl[0] + i, pxl[1] + h) not in centro_lista:
    #                     color = imagen_recortada_copia[pxl[1] + h, pxl[0] + i]
    #                     #print("Color", color)
    #                     distancia = abs(int(color[0]) - int(color_mas_cercano[0])) + abs(int(color[1]) - int(color_mas_cercano[1])) + abs(int(color[2]) - int(color_mas_cercano[2]))
    #                     if distancia <= 15: 
    #                         centro_lista.append((pxl[0] + i, pxl[1] + h))
    #                         contador += 1

    # print("Centro lista", centro_lista)

    if color_mas_cercano is not None:
        circuloDetectado = [pixel[0], pixel[1], 5]
        #circuloDetectado = cv2.minEnclosingCircle(np.array(centro_lista))
        
        if circuloDetectado is not None:
            cv2.circle(imagen_recortada_copia, (pixel[0], pixel[1]), 5, (0, 0, 255), 5)
            cv2.circle(imagen_recortada, (int(circuloDetectado[0]), int(circuloDetectado[1])), 50, (0, 255, 0), thickness = 2)
            #cv2.circle(imagen_recortada, (int(circuloDetectado[0][0]), int(circuloDetectado[0][1])), int(circuloDetectado[1]), (0, 255, 0), thickness = 2)

            xr = int(x1 + circuloDetectado[0])
            yr = int(y1 + circuloDetectado[1])
            rr = int(circuloDetectado[2])

            #xr = int(x1 + circuloDetectado[0][0])
            #yr = int(y1 + circuloDetectado[0][1])
            #rr = int(circuloDetectado[1])

            cv2.circle(frame, (xr, yr), rr, (255, 255, 0), thickness = 2)

            centro = ((xr, yr), rr)
            
            if correccion: return centro, distancia_mas_corta, color_mas_cercano
            
            centroConDecimales = ((x1 + circuloDetectado[0], y1 + circuloDetectado[1]), circuloDetectado[2])
            #centroConDecimales = ((x1 + circuloDetectado[0][0], y1 + circuloDetectado[0][1]), circuloDetectado[1])
            #ultimosCentrosCirculo.appendleft(centroConDecimales)
            radioDeteccionPorCirculo = circuloDetectado[2]
            #radioDeteccionPorCirculo = circuloDetectado[1]
            TiempoDeteccionUltimaPelota = 0
            deteccionPorColor = False
            checkRecorteCerca = False

        else: 
            radioDeteccionPorCirculo = radio
            if not checkRecorteCerca:
                checkRecorteCerca = True
                deteccionPorCirculos(preCentro, frame, recorteCerca + 100, False, color_pre_centro, 3)

    else: 
        radioDeteccionPorCirculo = radio
        if not checkRecorteCerca:
            checkRecorteCerca = True
            deteccionPorCirculos(preCentro, frame, recorteCerca + 100, False, color_pre_centro, 3)

    #if numeroFrame == 68: cv2.imwrite("imagen_recortada68.png", imagen_recortada)
    #if numeroFrame == 312: cv2.imwrite("imagen_recortada312ConCirculo.png", imagen_recortada_copia)

    #imagen_recortada = imutils.resize(imagen_recortada, int(imagen_recortada.shape[1] / resizer), int(imagen_recortada.shape[0] / resizer))
    cv2.imshow("Imagen recortada", imagen_recortada)
    cv2.imshow("Imagen recortada copia", imagen_recortada_copia)
        
    a = False
    
    if a:
        pausado = True

        if numeroFrame > 40:
            while True:
                # Verificar si se debe pausar la imagen
                if pausado:
                    # Esperar hasta que se presione cualquier tecla
                    cv2.waitKey(0)
                    pausado = False
                else:
                    # Esperar 1 milisegundo y obtener el código de tecla
                    key = cv2.waitKey(1)
                    
                    # Verificar si se debe pausar la imagen
                    if key == ord('p'):
                        pausado = True
                    # Verificar si se debe salir del bucle
                    elif key == ord('q'):
                        break
    
    return centro

def deteccionNoEsLaPelota(ultCentros, valorSumaEjeY, correccion):
    #print("BBBBBBBBBBB")
    #print("ultCentros", ultCentros)
    #print("valorSumaEjeY", valorSumaEjeY)
    #print("correccion", correccion)

    if correccion == False:
        sumaRadios = 0
        for i in range(len(ultCentros) - 1):
            sumaRadios += abs(ultCentros[i][1] - ultCentros[i + 1][1])

        if sumaRadios <= 0.5:
            return True
    
    sumaEjeY = 0
    for i in range(len(ultCentros) - 1):
        sumaEjeY += abs(ultCentros[i][0][1] - ultCentros[i + 1][0][1])
    
    if sumaEjeY <= valorSumaEjeY:
        return True

    if correccion:
        contador1 = 0
        contador2 = 0
        for centro in ultCentros:
            contador1 += 1
            contador2 = 0
            for centro2 in ultCentros:
                contador2 += 1
                if abs(centro[0][0] - centro2[0][0]) <= 1 and abs(centro[0][1] - centro2[0][1]) <= 1 and abs(centro[1] - centro2[1]) <= 1 and contador1 != contador2:
                    return True
                if abs(centro[0][1] - centro2[0][1]) <= 2 and contador1 != contador2:
                    return True
    
    return False

# Función cuadrática
def quadratic_func(x, a, b, c):
        return a * x ** 2 + b * x + c

def regresionCuadratica(ultCentros):
    # Puntos de datos
    #x_data = np.array([2901, 2800, 2730, 2690, 2656, 2656, 2633, 2616, 2605, 2605])
    #y_data = np.array([1007, 956, 928, 906, 899, 899, 899, 898, 905, 887])

    x_data = np.array(sublista[0][0] for sublista in ultCentros)
    y_data = np.array(sublista[0][1] for sublista in ultCentros)

    # Ajuste de la curva cuadrática
    params, _ = curve_fit(quadratic_func, x_data, y_data)

    # Parámetros de la regresión cuadrática
    a, b, c = params

    # Predecir el siguiente valor
    next_x = x_data[-1] + (x_data[-1] - x_data[-2])
    next_y = quadratic_func(next_x, a, b, c)

    return next_x, next_y

def circulosInmoviles(circles):
    global listaCirculosNoSeMueven1
    global listaCirculosNoSeMueven2
    global listaCirculosNoSeMueven3
    global listaCirculosNoSeMueven4
    global circulosGlobalesInmoviles
    
    if numeroFrame == 1:
        listaCirculosNoSeMueven1 = circles
    elif numeroFrame == 2:
        listaCirculosNoSeMueven2 = circles
    elif numeroFrame == 3:
        listaCirculosNoSeMueven3 = circles
    elif numeroFrame == 4:
        listaCirculosNoSeMueven4 = circles
    else: 
        for circulo in circles[0]:
            if circulo in listaCirculosNoSeMueven1 and circulo in listaCirculosNoSeMueven2 and circulo in listaCirculosNoSeMueven3 and circulo in listaCirculosNoSeMueven4:
                circulosGlobalesInmoviles.append(circulo)
                cv2.circle(frame, (int(circulo[0] / resizer), int(circulo[1] / resizer)), int(circulo[2] / resizer), (0, 0, 255), thickness = 2)

def corregirPosicionPelota(ultCentrosGlobales):
    #global deteccionColorUltimosFrames

    ultCentrosGlobales = list(ultCentrosGlobales)
    #cv2.imwrite("frame1.png", ultCentrosGlobales[0][2])
    diferenciaX = abs(ultCentrosGlobales[0][0][0][0] - ultCentrosGlobales[1][0][0][0])
    diferenciaY = abs(ultCentrosGlobales[0][0][0][1] - ultCentrosGlobales[1][0][0][1])
    ultCentrosGlobales.pop(0)

    contador = 0
    for centro, deteccionPorColor, _ in ultCentrosGlobales:
        contador += 1
        print(contador, ": Centro", centro, "DetecionPorColor", deteccionPorColor)

    numeroFramePelotaIncorrecta = 0
    # Intentamos detectar si el algortimo se rompió con respecto al círculo2 (centro2, deteccionPorColor2, frame2)
    for (centro1, deteccionPorColor1, frame1), (centro2, deteccionPorColor2, frame2) in zip(ultCentrosGlobales, ultCentrosGlobales[1:]):
        numeroFramePelotaIncorrecta += 1
        if abs(centro1[0][0] - centro2[0][0]) < 3 and diferenciaX > 5 and deteccionPorColor2 == False:
            print("Centro1", centro1)
            print("Centro2", centro2)
            break
        elif abs(centro1[0][1] - centro2[0][1]) < 3 and diferenciaY > 5 and deteccionPorColor2 == False:
            break
        elif abs(abs(centro1[0][0] - centro2[0][0]) - diferenciaX) > 50 and deteccionPorColor2 == False:
            break
        elif abs(abs(centro1[0][1] - centro2[0][1]) - diferenciaY) > 50 and deteccionPorColor2 == False:
            break

        diferenciaX = abs(centro1[0][0] - centro2[0][0])
        diferenciaY = abs(centro1[0][1] - centro2[0][1])
    
    print("NumeroFramePelotaIncorrecta", numeroFramePelotaIncorrecta + 1)
    if numeroFramePelotaIncorrecta > 8: numeroFramePelotaIncorrecta = 8
    
    #contador2 = numeroFramePelotaIncorrecta
    #for i in range(1, len(ultCentrosGlobales) - numeroFramePelotaIncorrecta + 1):
    #    correccionUltimosCirculos.append([deteccionPorCirculos(ultCentrosGlobales[numeroFramePelotaIncorrecta - 1][0], ultCentrosGlobales[contador2][2], i * 200, True)])
    #    contador2 += 1

    #for h in range(len(correccionUltimosCirculos)):
    #    x1 = max(ultCentrosGlobales[numeroFramePelotaIncorrecta - 1][0][0][0] - ((h + 1) * 200), 0)
    #    y1 = max(ultCentrosGlobales[numeroFramePelotaIncorrecta - 1][0][0][1]- ((h + 1) * 200), 0)
    #    for j in range(len(correccionUltimosCirculos[h][0][0])):
    #        correccionUltimosCirculos[h][0][0][j][0] = correccionUltimosCirculos[h][0][0][j][0] / 3 + x1
    #        correccionUltimosCirculos[h][0][0][j][1] = correccionUltimosCirculos[h][0][0][j][1] / 3 + y1
    #        correccionUltimosCirculos[h][0][0][j][2] = correccionUltimosCirculos[h][0][0][j][2] / 3

    print(f"{bcolors.FAIL}Warning: No active frommets remain. Continue?{bcolors.ENDC}")
    #print("BBBBBBBBBBBBBBBBBBBB", correccionUltimosCirculos[0])
    #print("CCCCCCCCCCc", correccionUltimosCirculos[0][0][0])

    #for i in range(len(ultCentrosGlobales) - numeroFramePelotaIncorrecta):
    #    if i == 0: preCentroCorrecion = ultCentrosGlobales[numeroFramePelotaIncorrecta - 1][0]
    #    if type(preCentroCorrecion) is not tuple: preCentroCorrecion = ((preCentroCorrecion[0], preCentroCorrecion[1]), preCentroCorrecion[2])
    #    print("preCentroCorrecion", preCentroCorrecion)
    #    preCentroCorrecion = tp_fix(correccionUltimosCirculos[i][0][0], preCentroCorrecion, 0.2, True, None, None, True)
    #    if i == 4: break

    correccionUltimosCirculos = []
    primerosCirculosCorreccion = []
    preCentrosCorrecion = []
    contador2 = numeroFramePelotaIncorrecta
    correccion = False

    while correccion == False:
        contador2 = numeroFramePelotaIncorrecta
        for i in range(len(ultCentrosGlobales) - numeroFramePelotaIncorrecta):
            #if primerosCirculosCorreccion is not None: continue
            if i == 0:
                preCentroCorrecion = ultCentrosGlobales[numeroFramePelotaIncorrecta - 1][0]
                print("preCentroCorrecion", preCentroCorrecion)
            if type(preCentroCorrecion) is not tuple and preCentroCorrecion is not None: preCentroCorrecion = ((preCentroCorrecion[0], preCentroCorrecion[1]), preCentroCorrecion[2])
            
            correccionUltimosCirculos = deteccionPorCirculos(preCentroCorrecion, ultCentrosGlobales[contador2][2], 200, True, color_pre_centro, 3)

            if correccionUltimosCirculos is not None:
                x1 = max(preCentroCorrecion[0][0] - 200, 0)
                y1 = max(preCentroCorrecion[0][1] - 200, 0)
                for h in range(len(correccionUltimosCirculos[0])):
                    correccionUltimosCirculos[0][h][0] = correccionUltimosCirculos[0][h][0] / 3 + x1
                    correccionUltimosCirculos[0][h][1] = correccionUltimosCirculos[0][h][1] / 3 + y1
                    correccionUltimosCirculos[0][h][2] = correccionUltimosCirculos[0][h][2] / 3

                if i == 0 and len(primerosCirculosCorreccion) == 0:
                    primerosCirculosCorreccion = correccionUltimosCirculos.tolist()
                    primerosCirculosCorreccion = primerosCirculosCorreccion[0]
                
                if i == 0:
                    print("len PrimerosCirculosCorreccion", len(primerosCirculosCorreccion))
                    # Ordena la lista de puntos en base a la distancia personalizada al preCentro
                    #puntos_ordenados = sorted(primerosCirculosCorreccion, key=lambda punto: distancia_personalizada(punto, preCentroCorrecion[0], preCentroCorrecion[1]))

                    # Imprime la lista ordenada
                    #print("Puntos Ordenados", puntos_ordenados)
                    #print("PrimerosCirculosCorreccion", primerosCirculosCorreccion)

                #print("deteccionColorUltimosFrames[contador2]", deteccionColorUltimosFrames[contador2])
                #print("preCentroCorrecion", preCentroCorrecion)
                
                verdeCerca = None

                if deteccionColorUltimosFrames[contador2] is not None:
                    verdeCerca = tp_fix(deteccionColorUltimosFrames[contador2], preCentroCorrecion, 0.2, False, None, (1,0), False, True)
                    #print("Verde Cerca", verdeCerca)

                if verdeCerca is not None:
                    preCentroCorrecion = verdeCerca
                    preCentroCorrecion = (preCentroCorrecion[0][0], preCentroCorrecion[0][1], preCentroCorrecion[1])
                
                else:
                    #preCentroCorrecion = ((preCentroCorrecion[0][0], preCentroCorrecion[0][1]), preCentroCorrecion[1] * 3)
                    if i == 0 and len(primerosCirculosCorreccion) == 0: preCentroCorrecion = tp_fix(correccionUltimosCirculos[0], preCentroCorrecion, 0.2, True, None, (1,0), True, False)
                    elif i == 0 and len(primerosCirculosCorreccion) != 0: preCentroCorrecion = tp_fix(primerosCirculosCorreccion, preCentroCorrecion, 0.2, True, None, (1,0), True, False)
                    else: preCentroCorrecion = tp_fix(correccionUltimosCirculos[0], preCentroCorrecion, 0.2, True, None, (1,0), True, False)

                print("preCentroCorrecion1", preCentroCorrecion)
                if preCentroCorrecion is not None: preCentrosCorrecion.append(((preCentroCorrecion[0], preCentroCorrecion[1]), preCentroCorrecion[2]))
                #print("PreCentroCorrecion2", ((preCentroCorrecion[0], preCentroCorrecion[1]), preCentroCorrecion[2]))
            #if i == 5: break
            if i == len(ultCentrosGlobales) - numeroFramePelotaIncorrecta - 1:
                if seEstaMoviendo(preCentrosCorrecion[-5:], 25) == False or deteccionNoEsLaPelota(preCentrosCorrecion[-5:], 5, True):
                    #print("ABorrar", [preCentrosCorrecion[0][0][0], preCentrosCorrecion[0][0][1], preCentrosCorrecion[0][1]])
                    #print("primerosCirculosCorreccion", primerosCirculosCorreccion)
                    #print("AAAAAAAAAAAAAAAAAA", [preCentrosCorrecion[0][0][0], preCentrosCorrecion[0][0][1], preCentrosCorrecion[0][1]] in primerosCirculosCorreccion)
                    primerosCirculosCorreccion.remove([preCentrosCorrecion[0][0][0], preCentrosCorrecion[0][0][1], preCentrosCorrecion[0][1]])
                    #print("PreCentrosCorrecion", preCentrosCorrecion)
                    print("Se Esta Moviendo", seEstaMoviendo(preCentrosCorrecion[-5:], 25))
                    print("Deteccion No Es La Pelota", deteccionNoEsLaPelota(preCentrosCorrecion[-5:], 5, True))
                    #print("primerosCirculosCorreccion", primerosCirculosCorreccion)
                    preCentrosCorrecion = []
                    correccion = False
                    if len(primerosCirculosCorreccion) == 0: numeroFramePelotaIncorrecta += 1
                    break
                else:
                    print("Se Esta Moviendo", seEstaMoviendo(preCentrosCorrecion[-5:], 25))
                    print("Deteccion No Es La Pelota", deteccionNoEsLaPelota(preCentrosCorrecion[-5:], 5, True))
                    correccion = True
                    #print("Deteccion Color Ultimos Frames", deteccionColorUltimosFrames)
                    break
            contador2 += 1

# Función para calcular la distancia entre dos puntos
def distancia_personalizada(punto, centro, radio):
    xCenter, yCenter = centro
    radius = radio

    difEnX = abs(int(xCenter) - int(punto[0]))
    difEnY = abs(int(yCenter) - int(punto[1]))
    difRadio = abs(int(radius) - int(punto[2]))

    return difEnX + difEnY + difRadio * 3

def cambiosDeDireccion(ultCentros, correccion, ultCentrosExtendidos):
    global primeraVez
    global preCentro
    global radioDeteccionPorCirculo
    global centroConDecimales
    global color_pre_centro
    global ultimosCentrosGlobales

    cambios_de_direccion = 0
    movimiento_en_x = []
    movimiento_en_y = []
    deteccionesPorColor = []
    deteccionesPorColorCambio = []
    referencia_x = None
    referencia_y = None
    for i in range(len(ultCentros) - 1):
        if referencia_x is not None:
            comparador1_x = referencia_x
            referencia_x = None
        else: comparador1_x = ultCentros[i][0][0][0]
        comparador2_x = ultCentros[i + 1][0][0][0]

        if abs(comparador2_x - comparador1_x) <= 10 and len(movimiento_en_x) > 0: 
            derecha = movimiento_en_x[-1]
            referencia_x = comparador1_x
        elif comparador2_x < comparador1_x: derecha = False
        elif comparador2_x > comparador1_x: derecha = True
        else: derecha = None

        if referencia_y is not None:
            comparador1_y = referencia_y
            referencia_y = None
        else: comparador1_y = ultCentros[i][0][0][1]
        comparador2_y = ultCentros[i + 1][0][0][1]

        if abs(comparador2_y - comparador1_y) <= 10 and len(movimiento_en_y) > 0: 
            abajo = movimiento_en_y[-1]
            referencia_y = comparador1_y
        elif comparador2_y < comparador1_y: abajo = False
        elif comparador2_y > comparador1_y: abajo = True
        else: abajo = None

        #print("Comparador1_x", comparador1_x, "Comparador2_x", comparador2_x)
        #print("Comparador1_y", comparador1_y, "Comparador2_y", comparador2_y)

        movimiento_en_x.append(derecha)
        movimiento_en_y.append(abajo)
        if i != 0: deteccionesPorColor.append(ultCentros[i][1])
    
    deteccionesPorColor.append(ultCentros[-1][1])

    for i in range(len(movimiento_en_x) - 1):
        if movimiento_en_x[i + 1] != movimiento_en_x[i] or movimiento_en_y[i + 1] != movimiento_en_y[i]:
            deteccionesPorColorCambio.append(deteccionesPorColor[i + 1])
            cambios_de_direccion += 1
    
    print("Movimiento en x", movimiento_en_x)
    print("Movimiento en y", movimiento_en_y)
    print("Detecciones por color", deteccionesPorColor)
    print("Detecciones por color cambio", deteccionesPorColorCambio)

    # if cambios_de_direccion >= 3 and deteccionesPorColorCambio.count(False) >= 2:
    #     diferenciaX = abs(ultCentros[0][0][0][0] - ultCentros[1][0][0][0])
    #     diferenciaY = abs(ultCentros[0][0][0][1] - ultCentros[1][0][0][1])
    #     ultCentros.pop(0)

    #     contador = 0
    #     for centro, deteccionPorColor, _ in ultCentros:
    #         contador += 1
    #         print(contador, ": Centro", centro, "DetecionPorColor", deteccionPorColor)

    #     numeroFramePelotaIncorrecta = 0
    #     # Intentamos detectar si el algortimo se rompió con respecto al círculo2 (centro2, deteccionPorColor2, frame2)
    #     for (centro1, *_), (centro2, *_) in zip(ultCentros, ultCentros[1:]):
    #         numeroFramePelotaIncorrecta += 1
    #         if abs(centro1[0][0] - centro2[0][0]) < 3 and diferenciaX > 5:
    #             print("Centro1", centro1)
    #             print("Centro2", centro2)
    #             break
    #         elif abs(centro1[0][1] - centro2[0][1]) < 3 and diferenciaY > 5:
    #             break
    #         elif abs(abs(centro1[0][0] - centro2[0][0]) - diferenciaX) > 50:
    #             break
    #         elif abs(abs(centro1[0][1] - centro2[0][1]) - diferenciaY) > 50:
    #             break

    #         diferenciaX = abs(centro1[0][0] - centro2[0][0])
    #         diferenciaY = abs(centro1[0][1] - centro2[0][1])
        
    #     print("NumeroFramePelotaIncorrecta", numeroFramePelotaIncorrecta + 1)

    print("Cambios de Dirección", cambios_de_direccion)

    #if cambios_de_direccion >= 3 and deteccionesPorColorCambio.count(False) >= 2 and not correccion:
    if cambios_de_direccion >= 3 and not correccion:
        ultCentrosGlobales = list(ultCentrosExtendidos)
        #cv2.imwrite("frame1.png", ultCentrosGlobales[0][2])
        diferenciaX = abs(ultCentrosGlobales[0][0][0][0] - ultCentrosGlobales[1][0][0][0])
        diferenciaY = abs(ultCentrosGlobales[0][0][0][1] - ultCentrosGlobales[1][0][0][1])
        ultCentrosGlobales.pop(0)

        contador = 0
        for centro, deteccionPorColor, *_ in ultCentrosGlobales:
            contador += 1
            print(contador, ": Centro", centro, "DetecionPorColor", deteccionPorColor)

        numeroFramePelotaIncorrecta = 0
        # Intentamos detectar si el algortimo se rompió con respecto al círculo2 (centro2, deteccionPorColor2, frame2)
        for (centro1, *_), (centro2, *_) in zip(ultCentrosGlobales, ultCentrosGlobales[1:]):
            numeroFramePelotaIncorrecta += 1
            if abs(centro1[0][0] - centro2[0][0]) < 3 and diferenciaX > 5:
                print("A")
                print("Centro1", centro1)
                print("Centro2", centro2)
                break
            elif abs(centro1[0][1] - centro2[0][1]) < 3 and diferenciaY > 5:
                print("B")
                print("Centro1", centro1)
                print("Centro2", centro2)
                break
            elif abs(abs(centro1[0][0] - centro2[0][0]) - diferenciaX) > 50:
                print("C")
                print("Centro1", centro1)
                print("Centro2", centro2)
                break
            elif abs(abs(centro1[0][1] - centro2[0][1]) - diferenciaY) > 50:
                print("D")
                print("Centro1", centro1)
                print("Centro2", centro2)
                break
            elif centro1[0][0] - centro2[0][0] == 0:
                print("E")
                print("Centro1", centro1)
                print("Centro2", centro2)
                numeroFramePelotaIncorrecta -= 1
                break

            diferenciaX = abs(centro1[0][0] - centro2[0][0])
            diferenciaY = abs(centro1[0][1] - centro2[0][1])
        
        print("NumeroFramePelotaIncorrecta", numeroFramePelotaIncorrecta + 1)

        primeraVez = True
        return cambios_de_direccion

        circulosCorreccion = []
        color_preCentro = None
        contador = -7
        #print("Deteccion Color Ultimos Frames", list(deteccionColorUltimosFrames)[-7:])
        for i in ultCentros:
            verdeCerca = None
            if i[1] == True:
                if len(circulosCorreccion) != 0: preCentroCorreccion2 = circulosCorreccion[-1][0] 
                else: preCentroCorreccion2 = i[4]
                circulosCorreccion.append((i[0], True, i[2], i[3], preCentroCorreccion2))
            else:
                if len(circulosCorreccion) == 0 and i[4] is not None: preCentroCorreccion = i[4]
                elif len(circulosCorreccion) != 0: preCentroCorreccion = circulosCorreccion[-1][0]
                else: continue
                if deteccionColorUltimosFrames[contador] is not None: verdeCerca = tp_fix(deteccionColorUltimosFrames[contador], preCentroCorreccion, 0.2, False, None, (1,0), False, True)
                if verdeCerca is None:
                    if color_preCentro is None: color_preCentro = i[3]
                    correccionCirculos, coseno, casi_color_preCentro = deteccionPorCirculos(preCentroCorreccion, i[2], 300, True, color_preCentro, 4)
                    if coseno > ultimosSimilitudesCoseno[contador]:
                        #print("AAAAAAAAAAAAAAAAAAA")
                        if len(circulosCorreccion) != 0: preCentroCorreccion2 = circulosCorreccion[-1][0] 
                        else: preCentroCorreccion2 = i[4]
                        circulosCorreccion.append((correccionCirculos, False, i[2], casi_color_preCentro, preCentroCorreccion2))
                        color_preCentro = casi_color_preCentro
                    else:
                        #print("BBBBBBBBBBBBBBBBBB", correccionCirculos)
                        if len(circulosCorreccion) != 0: preCentroCorreccion2 = circulosCorreccion[-1][0] 
                        else: preCentroCorreccion2 = i[4]
                        circulosCorreccion.append((i[0], False, i[2], i[3], preCentroCorreccion2))
                        color_preCentro = i[3]
                    #circulosCorreccion.append(deteccionPorCirculos(i[4], i[2], 300, True, i[3], 4))
                else:
                    pixeles = []
                    pixeles_colores = []

                    if verdeCerca[0][0] < i[2].shape[1] and verdeCerca[0][1] < i[2].shape[0]: pixeles.append((verdeCerca[0][0], verdeCerca[0][1]))

                    for i in range(1, int(verdeCerca[1]) + 1):
                        if verdeCerca[0][0] + i < i[2].shape[1] and verdeCerca[0][1] < i[2].shape[0]: pixeles.append((verdeCerca[0][0] + i, verdeCerca[0][1]))
                        if verdeCerca[0][0] - i < i[2].shape[1] and verdeCerca[0][1] < i[2].shape[0]: pixeles.append((verdeCerca[0][0] - i, verdeCerca[0][1]))

                    for i in range(1, int(verdeCerca[1]) + 1):
                        if verdeCerca[0][0] < i[2].shape[1] and verdeCerca[0][1] + i < i[2].shape[0]: pixeles.append((verdeCerca[0][0], verdeCerca[0][1] + i))
                        if verdeCerca[0][0] < i[2].shape[1] and verdeCerca[0][1] - i < i[2].shape[0]: pixeles.append((verdeCerca[0][0], verdeCerca[0][1] - i))

                    for i in range(1, int(verdeCerca[1]) + 1):
                        for h in range(1, verdeCerca[1] + 1):
                            if math.sqrt(h **2 + i **2) <= verdeCerca[1]:
                                if verdeCerca[0][0] + h < i[2].shape[1] and verdeCerca[0][1] + i < i[2].shape[0]: pixeles.append((verdeCerca[0][0] + h, verdeCerca[0][1] + i))
                                if verdeCerca[0][0] - h < i[2].shape[1] and verdeCerca[0][1] + i < i[2].shape[0]: pixeles.append((verdeCerca[0][0] - h, verdeCerca[0][1] + i))
                                if verdeCerca[0][0] + h < i[2].shape[1] and verdeCerca[0][1] - i < i[2].shape[0]: pixeles.append((verdeCerca[0][0] + h, verdeCerca[0][1] - i))
                                if verdeCerca[0][0] - h < i[2].shape[1] and verdeCerca[0][1] - i < i[2].shape[0]: pixeles.append((verdeCerca[0][0] - h, verdeCerca[0][1] - i))
                            else: break
                
                    for pixel in pixeles:
                        color = i[2][pixel[1], pixel[0]]
                        pixeles_colores.append(color)

                    # Calcula el promedio de cada posición utilizando comprensiones de listas
                    promedio_primer_valor = sum(sublista[0] for sublista in pixeles_colores) / len(pixeles_colores)
                    promedio_segundo_valor = sum(sublista[1] for sublista in pixeles_colores) / len(pixeles_colores)
                    promedio_tercer_valor = sum(sublista[2] for sublista in pixeles_colores) / len(pixeles_colores)

                    color_preCentro = (int(promedio_primer_valor), int(promedio_segundo_valor), int(promedio_tercer_valor))
                    if len(circulosCorreccion) != 0: preCentroCorreccion2 = circulosCorreccion[-1][0] 
                    else: preCentroCorreccion2 = i[4]
                    circulosCorreccion.append((verdeCerca, True, i[2], color_preCentro, preCentroCorreccion2))
            
            contador += 1
    
        #print("Circulos Correccion", circulosCorreccion)
        print("Cambios de Direccion Correccion", cambiosDeDireccion(circulosCorreccion, True))
    
        if cambiosDeDireccion(circulosCorreccion, True) >= 3:
            primeraVez = True
            preCentro = None
            ultimosCentrosGlobales.clear()
        else:
            centroConDecimales = circulosCorreccion[-1][0]
            radioDeteccionPorCirculo = circulosCorreccion[-1][0][1]
            ((x, y), radio) = circulosCorreccion[-1][0]
            preCentro = ((int(x), int(y)), int(radio))
            color_pre_centro = color_preCentro
            contador = 0
            for i in range(-7, 0):
                ultimosCentrosGlobales[i] = circulosCorreccion[contador]
                contador += 1
        
        #for i in circulosCorreccion:
        #    print("Circulos Correccion", i[0])
        #for i in ultimosCentrosGlobales:
        #    print("Ultimos Centros Globales", i[0])

        #if centro is not None: ultimosCentrosGlobales.append((centroConDecimales, deteccionPorColor, frameCopia, color_pre_centro, preCentro))

    return cambios_de_direccion

def distancia_bgr(color1, color2):
    """
    Calcula la distancia euclidiana entre dos colores BGR.
    """
    return np.sqrt(np.sum((color1 - color2) ** 2))

def pixelColorIgual(pixel, frames, muestra):
    colores = []
    for frame in frames:
        colores.append(frame[int(pixel[1]), int(pixel[0])])

    if muestra:
        print("Pixel", pixel)
        print("Colores", colores)
    
    for i in range(len(colores) - 1):
        if abs(int(colores[i][0]) - int(colores[i + 1][0])) + abs(int(colores[i][1]) - int(colores[i + 1][1])) + abs(int(colores[i][2]) - int(colores[i + 1][2])) > 30:
            return False
    
    return True

def circuloPorCentro(frameCopia, centro, pintar, pre_Centro_lista):
    color_pre_centro = frameCopia[centro[0][1], centro[0][0]]
    color_pre_centro = (color_pre_centro[0], color_pre_centro[1], color_pre_centro[2])

    centro_lista = [(centro[0])]
    contador = 1
    limite = None
    if pre_Centro_lista is not None: limite = len(pre_Centro_lista) + 150

    #colores_centro = []
    count = 0
    while contador > 0:
        contador = 0
        for pxl in centro_lista:
            if limite is not None and count >= limite: break
            color_a_comparar = frameCopia[pxl[1], pxl[0]]
            for i in range(-1, 2):
                for h in range(-1, 2):
                    if (pxl[0] + i, pxl[1] + h) not in centro_lista:
                        color = frameCopia[pxl[1] + h, pxl[0] + i]
                        #distancia = abs(int(color[0]) - int(color_pre_centro[0])) + abs(int(color[1]) - int(color_pre_centro[1])) + abs(int(color[2]) - int(color_pre_centro[2]))
                        distancia = abs(int(color[0]) - int(color_a_comparar[0])) + abs(int(color[1]) - int(color_a_comparar[1])) + abs(int(color[2]) - int(color_a_comparar[2]))
                        if distancia <= 20:
                            centro_lista.append((pxl[0] + i, pxl[1] + h))
                            #colores_centro.append(color)
                            count += 1
                            contador += 1

    #print("Centro lista", centro_lista)

    centroConDecimales = cv2.minEnclosingCircle(np.array(centro_lista))
    radioDeteccionPorCirculo = centroConDecimales[1]
    centro = ((int(np.rint(centroConDecimales[0][0])), int(np.rint(centroConDecimales[0][1]))), int(np.rint(centroConDecimales[1])))

    M = cv2.moments(casiCentro)
    if M["m00"] > 0: 
        centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), int(radioDeteccionPorCirculo)
        centroConDecimales = (M["m10"] / M["m00"], M["m01"] / M["m00"]), radioDeteccionPorCirculo

    # Calcula el promedio de cada posición utilizando comprensiones de listas
    #promedio_primer_valor = sum(sublista[0] for sublista in colores_centro) / len(colores_centro)
    #promedio_segundo_valor = sum(sublista[1] for sublista in colores_centro) / len(colores_centro)
    #promedio_tercer_valor = sum(sublista[2] for sublista in colores_centro) / len(colores_centro)

    #color_pre_centro = (int(promedio_primer_valor), int(promedio_segundo_valor), int(promedio_tercer_valor))

    color_pre_centro = frameCopia[centro[0][1], centro[0][0]]
    color_pre_centro = (color_pre_centro[0], color_pre_centro[1], color_pre_centro[2])

    #cv2.circle(frameCopia, (centro[0][0], centro[0][1]), centro[1], (0, 0, 255), 1)

    #if pintar and numeroFrame == 319:
    #    for pixel in centro_lista:
    #        frameCopia[pixel[1], pixel[0]] = (0, 0, 0)
    #    frameCopia[centro[0][1], centro[0][0]] = (255, 255, 255)
    #    cv2.imwrite("Frame319CopiaConCirculoPintado.png", frameCopia)

    return centro, centroConDecimales, radioDeteccionPorCirculo, color_pre_centro, centro_lista

def corregirPosicionPelota2(ultCentros, isMoving, detectionNotBall, directionChanges):
    if isMoving == False:
        print("A")
        
# Toma la cámara si no recibe video
if not args.get("video", False):
    vs = cv2.VideoCapture(0)

    # Toma video en caso de haber
else:
    vs = cv2.VideoCapture(args["video"])
    #vs2 = cv2.VideoCapture(args["video"])

# Rango de deteccion de verdes
greenLower = np.array([29, 50, 110])
greenUpper = np.array([64, 255, 255])

# Puntos de esquinas de la cancha
topLeftX = 749
topLeftY = 253
topRightX = 1095
topRightY = 252
bottomLeftX = 206
bottomLeftY = 797
bottomRightX = 1518
bottomRightY = 785

topLeftX = 2544
topLeftY = 1611
topRightX = 3364
topRightY = 1583
bottomLeftX = 1200
bottomLeftY = 2806
bottomRightX = 4956
bottomRightY = 2675

puntoMaximoArribaCancha = min(topLeftY, topRightY)
puntoMaximoAbajoCancha = max(bottomLeftY, bottomRightY)
puntoMaximoIzquierdaCancha = min(topLeftX, bottomLeftX)
puntoMaximoDerechaCancha = max(topRightX, bottomRightX)

pts_piques_finales = []
pts_piques_finales_afuera = []
pts_golpes_finales = []

ult_posible_pique = None

pts_pelota_norm = deque(maxlen=args["buffer"])
pts_pelota_pers = deque(maxlen=args["buffer"])

# preCentro es el centro de la pelota del frame anterior
preCentro = None
preCentroConDecimales = None
primeraVez = True
centro = None
centroConDecimales = None

# Fps, frames totales y duración del video en segundos
fps = int(vs.get(cv2.CAP_PROP_FPS))
frame_count = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
duracion = frame_count / fps

print("FPS: ", fps)
print("Duracion: ", duracion)

#time.sleep(2.0)

# Indica el tiempo que pasó desde que se detectó la última pelota
TiempoDeteccionUltimaPelota = 0

# Indica cuanto tiempo pasa entre tres centros consecutivos. 
# Esto para saber si detectó la pelota correctamente a la hora de determinar el pique
TiempoTresCentrosConsecutivos = 0

# TiempoSegundosEmpezoVideo cuenta cuanto tiempo pasó en segundos desde que empezó el video 
TiempoSegundosEmpezoVideo = 0

ultimosCentros = deque(maxlen=10)
ultimosCentrosCirculo = deque(maxlen=8)
ultimosCentrosGlobales = deque(maxlen=14)
ultimosFrames = deque(maxlen=7)
ultimosSimilitudesCoseno = deque(maxlen=14)

todosContornos = []
contornosIgnorar = []

centros_para_determinar_pique = deque(maxlen=2)
bajandos = deque(maxlen=2)

# Se establece el resizer, sirve para agrandar la imagen y realizar un análisis más profundo, a cambio de más tiempo de procesamiento
# El primer valor corresponde al video original y el segundo a la perspectiva
resizer = 3

altoOG = 0
anchoOG = 0

es_pique = None
posiblePique = False
posiblesPiques = deque()

# TiempoDifVelocidad cuenta cuento tiempo en segundos pasa desde que se encontraron los dos puntos para usar en la velocidad
TiempoDifVelocidad = 0

# TiempoDifPiques cuenta cuanto tiempo pasa desde que se encontró un pique hasta que se encuentra el siguiente
TiempoDifPiques = 0

punto1Velocidad = None
velocidad = False
diferente = False
velocidadFinal = None
afterVelocidad = False

pelotaEstaEnPerspectiva = None

casiCentro = None

recorteCerca = 200
recorteCerca = 150
recorteCerca = 100
recorteCerca = 90
recorteCerca = 200

checkRecorteCerca = False

radioDeteccionPorCirculo = 0

start_time = time.time()
previous_time = start_time

aSaltear = 100
aSaltear = 0
aSaltear = 280
#aSaltear = 0

ultFrames = deque(maxlen=5)

for _ in range(aSaltear):
    vs.read()

# El número del Frame del video
numeroFrame = aSaltear

listaCirculosNoSeMueven1 = []
listaCirculosNoSeMueven2 = []
listaCirculosNoSeMueven3 = []
listaCirculosNoSeMueven4 = []

circulosGlobalesInmoviles = []

ruta_archivo = "circulosIgnorarInkedInked.txt"

circulosAIgnorar = []

deteccionPorColor = None

deteccionColorUltimosFrames = deque(maxlen=13)
deteccionColorEsteFrame = []

#correccionUltimosCirculos = deque(maxlen=13)

radio = None

corregir = (False, 0)

color_pre_centro = None

pre_centro_lista = None

ultimosPosiblesCentrosCirculo = deque(maxlen=10)

# Abrir el archivo en modo de lectura
with open(ruta_archivo, "r") as archivo:
    # Leer el contenido del archivo
    contenido = archivo.read()

    # Procesar el contenido y asignarlo a la lista
    circulosAIgnorar1 = contenido.splitlines()  # Suponiendo que cada línea del archivo corresponde a un elemento de la lista

    for i in circulosAIgnorar1:
        i = i.strip("[]")  # Elimina los corchetes del inicio y el final de la cadena

        lista_str = i.split()  # Divide la cadena en una lista de strings

        lista_enteros = [float(num) for num in lista_str]  # Convierte cada string en un float y luego en un entero

        circulosAIgnorar.append(lista_enteros)

#vs2.read()

mitad_cancha = coordenadaPorMatriz(0, "Primera vez")

# Se corre el for la cantidad de frames que contiene el video
for _ in range(frame_count - aSaltear):
    numeroFrame += 1
    print("Numero de Frame: ", numeroFrame)

    TiempoSegundosEmpezoVideo += 1/fps

    # Toma el frame del video
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    #frameSiguiente = vs2.read()
    #frameSiguiente = frameSiguiente[1] if args.get("video", False) else frameSiguiente

    #for circulo in circulosAIgnorar:
        #cv2.circle(frame, (int(circulo[0] / resizer), int(circulo[1] / resizer)), int(circulo[2] / resizer), (255, 255, 255), 2)

    if numeroFrame == aSaltear + 1:
        # Ancho y alto de la imagen
        altoOG, anchoOG = frame.shape[:2]
        
        ############ VER DE BORRAR ESTO
        estaCercaX = anchoOG * 10/100
        estaCercaY = altoOG * 10/100
        #################

    #frameSiguiente = imutils.resize(frameSiguiente, anchoOG * resizer, altoOG * resizer)

    # Cuando termina las iteraciones y no hay frames. Se usa al no saber la duración del video
    if frame is None:
        break

    # Cuando el frame es un número determinado, le hacmeos un zoom a la imagen, obtenemos esa foto y la guardamos en la carpeta
    if numeroFrame == 84:
        # Coordenadas del punto central para hacer zoom
        x, y = 1023, 247

        # Tamaño del área de zoom
        zoom_width, zoom_height = 200, 200

        # Calcular las coordenadas del área de zoom
        x1, y1 = x - zoom_width // 2, y - zoom_height // 2
        x2, y2 = x + zoom_width // 2, y + zoom_height // 2

        # Recortar el área de zoom
        zoomed_area = frame[y1:y2, x1:x2]

        # Redimensionar el área de zoom a su tamaño original
        zoomed_area = cv2.resize(zoomed_area, (zoom_width, zoom_height))

        # Guardar el área de zoom como una imagen
        #cv2.imwrite('zoomed_image.jpg', zoomed_area)
        #break

    frame = imutils.resize(frame, anchoOG * resizer, altoOG * resizer)
    imagen_cancha = frame[int(mitad_cancha[1]):int(frame.shape[0]), 0:frame.shape[1]]

    main(imagen_cancha)

    #print("pts_piques", pts_piques_finales)
    #print("pts_golpes", pts_golpes_finales)

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