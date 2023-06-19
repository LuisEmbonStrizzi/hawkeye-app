from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time


def tracking(ruta_video):

    def main(frame):
        # global velocidadFinal
        # global topLeftX, topLeftY, topRightX, topRightY, bottomLeftX, bottomLeftY, bottomRightX, bottomRightY
        # global estaCercaX
        # global estaCercaY
        nonlocal TiempoDeteccionUltimaPelota
        nonlocal primeraVez
        nonlocal preCentro
        nonlocal TiempoTresCentrosConsecutivos
        nonlocal TiempoDifPiques
        nonlocal posiblePique
        nonlocal ult_posible_pique
        nonlocal TiempoDifVelocidad
        nonlocal es_pique
        nonlocal velocidad
        nonlocal afterVelocidad
        # nonlocal radio
        nonlocal diferente
        nonlocal punto1Velocidad
        anchoOG = frame.shape[1]
        altoOG = frame.shape[0]

        # VER DE BORRAR ESTO
        estaCercaX = anchoOG * 10/100
        estaCercaY = altoOG * 10/100
        #################

        frame = imutils.resize(frame, anchoOG * resizer, altoOG * resizer)

        # Cámara lenta para mayor análisis
        # cv2.waitKey(100)

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        #blurred = cv2.dilate(frame, None, iterations=2)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Filtra los tonos verdes de la imagen
        mascara = cv2.inRange(hsv, greenLower, greenUpper)
        mascara = cv2.erode(mascara, None, iterations=2)
        mascara = cv2.dilate(mascara, None, iterations=2)

        # Toma todos los contornos de la imagen
        contornos = cv2.findContours(
            mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos = imutils.grab_contours(contornos)

        centro = None

        if (TiempoSegundosEmpezoVideo % 5 == 0):
            eliminarContornosInservibles(todosContornos)

        if len(contornos) > 0:
            # Busca el contorno más grande y encuentra su posición (x, y)
            contornosQuietos(contornos, todosContornos, contornosIgnorar)
            if len(ultimosCentros) == 5 and TiempoDeteccionUltimaPelota >= 0.3 and seEstaMoviendo(ultimosCentros) == False:
                contornos = ignorarContornosQuietos(
                    contornos, contornosIgnorar)

            if len(contornos) > 0:
                if primeraVez:
                    casiCentro = max(contornos, key=cv2.contourArea)
                    ((x, y), radio) = cv2.minEnclosingCircle(casiCentro)
                    M = cv2.moments(casiCentro)
                    centro = (int(M["m10"] / M["m00"]),
                              int(M["m01"] / M["m00"])), int(radio)
                    primeraVez = False
                    preCentro = centro
                    TiempoDeteccionUltimaPelota = 0
                    TiempoTresCentrosConsecutivos = 0

                    pique3.appendleft(centro[0][1])
                    ultimosCentros.appendleft(centro)

                else:
                    casiCentro = tp_fix(contornos, preCentro,
                                        TiempoDeteccionUltimaPelota)

                    if casiCentro is not None:
                        ((x, y), radio) = cv2.minEnclosingCircle(casiCentro)
                        M = cv2.moments(casiCentro)
                        centro = [int(M["m10"] / M["m00"]),
                                  int(M["m01"] / M["m00"])], int(radio)
                        preCentro = centro
                        TiempoTresCentrosConsecutivos += TiempoDeteccionUltimaPelota
                        TiempoDeteccionUltimaPelota = 0
                        pique3.appendleft(centro[0][1])
                        ultimosCentros.appendleft(centro)

                    else:
                        if TiempoDeteccionUltimaPelota >= 0.3:
                            primeraVez = True
                            preCentro = None
                        TiempoDeteccionUltimaPelota += 1/fps
                        TiempoTresCentrosConsecutivos = 0

                # Sigue si el contorno tiene cierto tamaño
                if casiCentro is not None and radio > 0:
                    # Dibuja el círculo en la pelota
                    cv2.circle(frame, (int(x), int(y)),
                               int(radio), (0, 255, 255), 2)
                    cv2.circle(
                        frame, (centro[0][0], centro[0][1]), 5, (0, 0, 255), -1)

                if centro is not None and preCentro[0][1] < puntoMaximoAbajoCancha * resizer and preCentro[0][1] > puntoMaximoArribaCancha * resizer and preCentro[0][0] < puntoMaximoDerechaCancha * resizer and preCentro[0][0] > puntoMaximoIzquierdaCancha * resizer:
                    pelotaEstaEnPerspectiva = True
                elif centro is not None:
                    pelotaEstaEnPerspectiva = False
                else:
                    pelotaEstaEnPerspectiva = None

        else:
            if TiempoDeteccionUltimaPelota >= 0.3:
                primeraVez = True
                preCentro = None
            TiempoDeteccionUltimaPelota += 1/fps
            TiempoTresCentrosConsecutivos = 0
            pelotaEstaEnPerspectiva = None

        bajando = False

        if centro is not None:
            pique.appendleft(centro[0][1])
            if (len(pique) >= 2):
                if (pique[0] - pique[1] > 0):
                    bajando = True
                if (pique[0] - pique[1] != 0):
                    pique2.appendleft((bajando, numeroFrame))
                else:
                    bajando = "Indeterminación"

        TiempoDifPiques += 1/fps
        posiblePique = False
        if (len(pique2) >= 2):
            if pique2[0][0] == False and pique2[1][0] == True and preCentro is not None and pique2[0][1] - pique2[1][1] <= fps/6 and centro is not None:
                posiblePique = True
                TiempoDifPiques = 0

        # Entra a este if cuando se determina que hay un posiblePique, es decir, que se detectó algo que no se puede determinar si es un pique o un golpe
        if posiblePique:
            centro_pers = coordenadaPorMatriz(centro)
            # print(centro_pers)
            if (len(pique2) >= 2):
                #print(centro, "ARY TROL")
                # Entra a este if cuanda la pelota no esté en la cancha. Al no estar en la cancha, solo puedo determinar si está por encima o por debajo de la red para luego determinar si un posiblePique es pique o golpe.
                if (preCentro[0][1] > puntoMaximoAbajoCancha * resizer or preCentro[0][1] < puntoMaximoArribaCancha * resizer or preCentro[0][0] > puntoMaximoDerechaCancha * resizer or preCentro[0][0] < puntoMaximoIzquierdaCancha * resizer):
                    mitadDeCancha = (puntoMaximoAbajoCancha -
                                     puntoMaximoArribaCancha) / 2
                    if preCentro[0][1] <= mitadDeCancha:
                        abajo = False
                    else:
                        abajo = True

                    # Creo que esta parte está mal y se debería apendear preCentro[1] en vez de [0] para que se apendee la coordenada en Y.
                    if posiblesPiques == []:
                        posiblesPiques.appendleft(
                            (abajo, preCentro[0], numeroFrame))
                        ult_posible_pique = preCentro[0]
                    elif preCentro[0] != ult_posible_pique:
                        # print("ENTREEE")
                        posiblesPiques.appendleft(
                            (abajo, preCentro[0], numeroFrame))
                        ult_posible_pique = preCentro[0]

                    if len(posiblesPiques) >= 2:
                        es_pique = pica(TiempoDifPiques)
                        #print("PASO 1", es_pique, type(posiblesPiques[1][0]), posiblesPiques[1][0])
                        if es_pique and type(posiblesPiques[1][0]) is not bool:
                            #print("TRUE", es_pique)
                            pts_piques_finales.append(
                                [centro_pers, float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                        elif es_pique == False and type(posiblesPiques[1][0]) is not bool:
                            #print("FALSE", es_pique)
                            pts_golpes_finales.append(
                                [centro_pers, float("{:.2f}".format(posiblesPiques[1][1] / fps))])

                # Entra a este if cuando la pelota está en la perspectiva. Creo que está demás lo de preguntar cosas para que entre al if, fijarse si no está todo ya dado por sentado antes.
                elif posiblePique and preCentro is not None and centro is not None:
                    #print("ENTRE POSTA")
                    if posiblesPiques == []:
                        posiblesPiques.appendleft((preCentro, numeroFrame))
                        ult_posible_pique = preCentro[0]
                    elif ult_posible_pique != preCentro[0]:
                        posiblesPiques.appendleft((preCentro, numeroFrame))
                        ult_posible_pique = preCentro[0]
                    TiempoDifPiques = 0
                    velocidad = True
                    punto1Velocidad = preCentro
                    TiempoDifVelocidad += 1/fps
                    if len(posiblesPiques) >= 2:
                        es_pique = pica(TiempoDifPiques)
                        #print("PASO 1", es_pique)
                        if es_pique and type(posiblesPiques[1][0]) is not bool:
                            pts_piques_finales.append(
                                [centro_pers, float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                        if es_pique == False and type(posiblesPiques[1][0]) is not bool:
                            pts_golpes_finales.append(
                                [centro_pers, float("{:.2f}".format(posiblesPiques[1][1] / fps))])

        if es_pique is not None:
            es_pique = None

        if velocidad and pelotaEstaEnPerspectiva and punto1Velocidad is not None:
            if punto1Velocidad[0] != centro[0] or punto1Velocidad[0][1] != centro[0][1]:
                diferente = True

        if velocidad and pelotaEstaEnPerspectiva and diferente:
            velocidadFinal = velocidadPelota(
                punto1Velocidad, centro, TiempoDifVelocidad)
            velocidad = False
            punto1Velocidad = None
            TiempoDifVelocidad = 0
            diferente = False
            afterVelocidad = True

        elif velocidad:
            TiempoDifVelocidad += 1/fps

        elif TiempoDifVelocidad >= 0.5:
            TiempoDifVelocidad = 0
            velocidad = False
            punto1Velocidad = None
            diferente = False

        if afterVelocidad and centro is not None:
            afterVelocidad = False

        # Resizea y Muestra el Frame
        frame = imutils.resize(frame, anchoOG, altoOG)
        frame = imutils.resize(frame, height=768)
        mascara = imutils.resize(mascara, anchoOG, altoOG)
        mascara = imutils.resize(mascara, height=768)

    def coordenadaPorMatriz(centro):
        pts1 = np.float32([[topLeftX, topLeftY], [topRightX, topRightY], [
            bottomLeftX, bottomLeftY], [bottomRightX, bottomRightY]])
        pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        cords_pelota = np.array([[centro[0][0]], [centro[0][1]], [1]])
        cords_pelota_pers = np.dot(matrix, cords_pelota)
        cords_pelota_pers = (int(
            cords_pelota_pers[0]/cords_pelota_pers[2]), int(cords_pelota_pers[1]/cords_pelota_pers[2]))

        return cords_pelota_pers

    def eliminarContornosInservibles(todosContornos):
        count = 0
        aBorrar = []
        for i in todosContornos:
            if (len(i) <= 5):
                aBorrar.append(count)
            count += 1

        n = 0
        for i in aBorrar:
            todosContornos.pop(i - n)
            n += 1

    # Define todos los contornos que no se mueven, es decir, que no pueden ser la pelota

    def contornosQuietos(cnts, todosContornos, contornosIgnorar):
        centrosCerca = False
        for contorno in cnts:
            count = 0
            # Círculo del contorno
            (x, y), radius = cv2.minEnclosingCircle(contorno)
            x, y, radius = int(x), int(y), int(radius)
            for circulos_cercanos in todosContornos:
                for circulo in circulos_cercanos:
                    if x - circulo[0][0] >= -10 and x - circulo[0][0] <= 10 and y - circulo[0][1] >= -10 and y - circulo[0][1] <= 10:
                        centrosCerca = True
                    else:
                        centrosCerca = False
                        break
                if centrosCerca:
                    todosContornos[count].append([(x, y, radius)])
                    break
                count += 1
            if centrosCerca == False:
                todosContornos.append([[(x, y, radius)]])

        for circulos_cercanos in todosContornos:
            ContornoExiste = False
            if (len(circulos_cercanos) >= 10):
                promedioIgnorarX = 0
                promedioIgnorarY = 0
                for circulo in circulos_cercanos:
                    promedioIgnorarX += circulo[0][0]
                    promedioIgnorarY += circulo[0][1]
                promedioIgnorarX /= len(circulos_cercanos)
                promedioIgnorarY /= len(circulos_cercanos)
                promedioIgnorarX, promedioIgnorarY = int(
                    np.rint(promedioIgnorarX)), int(np.rint(promedioIgnorarY))
                if (len(contornosIgnorar) == 0):
                    contornosIgnorar.append(
                        (promedioIgnorarX, promedioIgnorarY))
                for contorno in contornosIgnorar:
                    if (contorno[0] == promedioIgnorarX and contorno[1] == promedioIgnorarY):
                        ContornoExiste = True
                if ContornoExiste == False:
                    contornosIgnorar.append(
                        (promedioIgnorarX, promedioIgnorarY))

    # Ignora los contornos quietos encontrados en la función anterior

    def ignorarContornosQuietos(cnts, contornosIgnorar):
        new_cnts = []
        Ignorar = False
        for cnt in cnts:
            (x, y), _ = cv2.minEnclosingCircle(cnt)
            for i in contornosIgnorar:
                if x - i[0] >= -20 and x - i[0] <= 20 and y - i[1] >= -20 and y - i[1] <= 20:
                    Ignorar = True
                    break
                else:
                    Ignorar = False

            if Ignorar == False:
                new_cnts.append(cnt)

        return new_cnts

    def seEstaMoviendo(ultCentros):
        movimiento = False
        for i in range(2):
            restaA = ultCentros[4][0][i] - ultCentros[3][0][i]
            restaB = ultCentros[3][0][i] - ultCentros[2][0][i]
            restaC = ultCentros[2][0][i] - ultCentros[1][0][i]
            restaD = ultCentros[1][0][i] - ultCentros[0][0][i]
            if restaA + restaB + restaC + restaD >= 15:
                movimiento = True
            else:
                movimiento = False
                break

        if movimiento:
            return True
        return False

    # Función que arregla el problema de "la zapatilla verde"

    def tp_fix(contornos, pre_centro, count):
        cnts_pts = []
        medidorX = 100
        medidorY = 103
        #medidorX = estaCercaX
        #medidorY = estaCercaY

        for contorno in contornos:
            ((x, y), _) = cv2.minEnclosingCircle(contorno)
            if x - pre_centro[0][0] > medidorX * resizer or pre_centro[0][0] - x > medidorX * resizer or y - pre_centro[0][1] > medidorY * resizer or pre_centro[0][1] - y > medidorY * resizer and count <= 0.5:
                continue
            cnts_pts.append(contorno)
        if cnts_pts != []:
            return cualEstaMasCerca(pre_centro, cnts_pts)

    # Define qué candidato a pelota es el punto más cercano al anterior. Toma los puntos de tp_fix y analiza cual está mas cerca al pre_centro (centro anterior).

    def cualEstaMasCerca(punto, lista):
        suma = []
        suma2 = []
        for i in lista:
            (xCenter, yCenter), radius = cv2.minEnclosingCircle(i)
            difEnX = abs(int(xCenter) - int(punto[0][0]))
            difEnY = abs(int(yCenter) - int(punto[0][1]))
            difRadio = abs(int(radius) - int(punto[1]))

            suma.append(difEnX + difEnY + difRadio * 3)
            suma2.append(i)
        return suma2[suma.index(min(suma))]

    # Función que determina si es un pique o un golpe

    def pica(count):
        # Tengo que descubrir si la variable "b" es un pique o un golpe
        # Si es un pique, se devuelve True, de lo contrario se devuelve False

        if type(posiblesPiques[0][0]) is not bool and type(posiblesPiques[1][0]) is not bool:
            abajoA = False
            abajoB = False
            a = posiblesPiques[0][0][0][1] / resizer
            b = posiblesPiques[1][0][0][1] / resizer
            #cv2.circle(frame, posiblesPiques[0][0], 40, (255, 255, 255), -1)
            #cv2.circle(frame, posiblesPiques[1][0], 40, (255, 255, 255), -1)
            if a >= 474 / 2:
                abajoA = True
            if b >= 474 / 2:
                abajoB = True
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
            b = posiblesPiques[1][0][0][1] / resizer
            if b >= 474 / 2:
                abajoB = True

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
            a = posiblesPiques[0][0][0][1] / resizer
            if a >= 474 / 2:
                abajoA = True

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
        punto1X = punto1[0][0] / (resizer * 20)
        punto1Y = punto1[0][1] / (resizer * 20)
        punto2X = punto2[0][0] / (resizer * 20)
        punto2Y = punto2[0][1] / (resizer * 20)

        if punto1X >= punto2X:
            movimientoX = punto1X - punto2X
        elif punto1X <= punto2X:
            movimientoX = punto2X - punto1X

        if punto1Y >= punto2Y:
            movimientoY = punto1Y - punto2Y
        elif punto1Y <= punto2Y:
            movimientoY = punto2Y - punto1Y

        distancia = np.sqrt(movimientoX * movimientoX +
                            movimientoY * movimientoY)
        #distancia *= 1.5

        return int(np.rint(distancia / tiempo * 3.6))

    vs = cv2.VideoCapture(ruta_video)

    # Rango de deteccion de verdes
    greenLower = np.array([29, 50, 110])
    greenUpper = np.array([64, 255, 255])

    topLeftX = 749
    topLeftY = 253
    topRightX = 1095
    topRightY = 252
    bottomLeftX = 206
    bottomLeftY = 797
    bottomRightX = 1518
    bottomRightY = 785

    puntoMaximoArribaCancha = min(topLeftY, topRightY)
    puntoMaximoAbajoCancha = max(bottomLeftY, bottomRightY)
    puntoMaximoIzquierdaCancha = min(topLeftX, bottomLeftX)
    puntoMaximoDerechaCancha = max(topRightX, bottomRightX)

    pts_piques_finales = []
    pts_golpes_finales = []

    ult_posible_pique = None

    preCentro = None
    primeraVez = True
    centro = None

    # Fps, frames totales y duración del video en segundos
    fps = int(vs.get(cv2.CAP_PROP_FPS))
    frame_count = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    duracion = frame_count / fps

    time.sleep(2.0)

    # Indica el tiempo que pasó desde que se detectó la última pelota
    TiempoDeteccionUltimaPelota = 0

    # Indica cuanto tiempo pasa entre tres centros consecutivos.
    # Esto para saber si detectó la pelota correctamente a la hora de determinar el pique
    TiempoTresCentrosConsecutivos = 0

    # TiempoSegundosEmpezoVideo cuenta cuanto tiempo pasó en segundos desde que empezó el video
    TiempoSegundosEmpezoVideo = 0

    ultimosCentros = deque(maxlen=5)

    todosContornos = []
    contornosIgnorar = []

    pique = deque(maxlen=4)
    pique2 = deque(maxlen=4)
    pique3 = deque(maxlen=3)

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

    # El número del Frame del video
    numeroFrame = 0

    punto1Velocidad = None
    velocidad = False
    diferente = False
    velocidadFinal = None
    afterVelocidad = False

    pelotaEstaEnPerspectiva = None

    start_time = time.time()
    previous_time = start_time

    for _ in range(frame_count):
        numeroFrame += 1
        #print("Numero de Frame: ", numeroFrame)

        TiempoSegundosEmpezoVideo += 1/fps

        frame = vs.read()
        frame = frame[1]

        if frame is None:
            break

        pts1 = np.float32([[topLeftX, topLeftY],       [topRightX, topRightY],
                           [bottomLeftX, bottomLeftY], [bottomRightX, bottomRightY]])
        pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(frame, matrix, (164, 474))

        main(frame)

        # Terminar la ejecución si se presiona la "q"
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if key == ord('p'):
            cv2.waitKey(-1)

    vs.release()
    return pts_piques_finales
