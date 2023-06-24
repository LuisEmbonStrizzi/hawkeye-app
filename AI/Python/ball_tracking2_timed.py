from collections import deque
import numpy as np
import cv2
import imutils
import time
# from tqdm import tqdm


def tracking():
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
        # global topLeftX, topLeftY, topRightX, topRightY, bottomLeftX, bottomLeftY, bottomRightX, bottomRightY
        # global estaCercaX
        # global estaCercaY

        anchoOG = frame.shape[1]
        altoOG = frame.shape[0]

        # VER DE BORRAR ESTO
        estaCercaX = anchoOG * 10/100
        estaCercaY = altoOG * 10/100
        #################

        ################################ TIEMPO: 0.1 ###################################
        frame = imutils.resize(frame, anchoOG * resizer, altoOG * resizer)
        ################################ TIEMPO: 0.1 ###################################

        # Cámara lenta para mayor análisis
        # cv2.waitKey(100)

        ################################ TIEMPO: 0.33 ###################################
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        ################################ TIEMPO: 0.33 ###################################

        # Filtra los tonos verdes de la imagen
        ################################ TIEMPO: 0.35 ###################################
        mascara = cv2.inRange(hsv, greenLower, greenUpper)
        mascara = cv2.erode(mascara, None, iterations=2)
        mascara = cv2.dilate(mascara, None, iterations=2)
        ################################ TIEMPO: 0.35 ###################################

        # Toma todos los contornos de la imagen
        ################################ TIEMPO: 0.15 ###################################
        contornos = cv2.findContours(
            mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos = imutils.grab_contours(contornos)
        ################################ TIEMPO: 0.15 ###################################

        centro = None
        ################################ TIEMPO: 0.001 ###################################
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
                        ultimosCentros.appendleft(centro)

                    else:
                        if TiempoDeteccionUltimaPelota >= 0.3:
                            primeraVez = True
                            preCentro = None
                        TiempoDeteccionUltimaPelota += 1/fps
                        TiempoTresCentrosConsecutivos = 0

                # Sigue si el contorno tiene cierto tamaño
                if radio > 0 and casiCentro is not None:
                    # Dibuja el círculo en la pelota
                    cv2.circle(frame, (int(x), int(y)),
                               int(radio), (0, 255, 255), 2)
                    cv2.circle(
                        frame, (centro[0][0], centro[0][1]), 5, (0, 0, 255), -1)
        ################################ TIEMPO: 0.001 ###################################

        else:
            if TiempoDeteccionUltimaPelota >= 0.3:
                primeraVez = True
                preCentro = None
            TiempoDeteccionUltimaPelota += 1/fps
            TiempoTresCentrosConsecutivos = 0
            #pelotaEstaEnPerspectiva = None

        bajando = False

        if centro is not None:
            pique.appendleft(centro[0][1])
            if (len(pique) >= 2):
                if (pique[0] - pique[1] > 0):
                    bajando = True
                if (pique[0] - pique[1] != 0):
                    pique2.appendleft((bajando, numeroFrame))
                else:
                    bajando = None
        # print("Pique", pique)
        # print("Pique 2", pique2)
        # print("Centro", centro)
        # print("PreCentro", preCentro)

        TiempoDifPiques += 1/fps

        ################################ TIEMPO: 0.001 ###################################
        posiblePique = False
        if (len(pique2) >= 2):
            if pique2[0][0] == False and pique2[1][0] == True and preCentro is not None and pique2[0][1] - pique2[1][1] <= fps/6 and centro is not None:
                posiblePique = True
                if len(posiblesPiques) % 2 == 1:
                    TiempoDifPiques = 0

        # Entra a este if cuando se determina que hay un posiblePique, es decir, que se detectó algo que no se puede determinar si es un pique o un golpe
        if posiblePique:
            #centro_pers = coordenadaPorMatriz(centro)
            if (len(pique2) >= 2):
                # Entra a este if cuanda la pelota no esté en la cancha. Al no estar en la cancha, solo puedo determinar si está por encima o por debajo de la red para luego determinar si un posiblePique es pique o golpe.
                pre_esta_en_cancha = estaEnCancha(preCentro, False)
                if not pre_esta_en_cancha:
                    mitadDeCancha = (puntoMaximoAbajoCancha -
                                     puntoMaximoArribaCancha) / 2
                    if preCentro[0][1] <= mitadDeCancha:
                        abajo = False
                    else:
                        abajo = True

                    if posiblesPiques == []:
                        #posiblesPiques.appendleft((abajo, preCentro[0], numeroFrame))
                        posiblesPiques.appendleft(
                            (abajo, coordenadaPorMatriz(preCentro), numeroFrame))
                        ult_posible_pique = preCentro[0]
                    elif preCentro[0] != ult_posible_pique:
                        #posiblesPiques.appendleft((abajo, preCentro[0], numeroFrame))
                        posiblesPiques.appendleft(
                            (abajo, coordenadaPorMatriz(preCentro), numeroFrame))
                        ult_posible_pique = preCentro[0]

                    if len(posiblesPiques) >= 2:
                        es_pique = pica(TiempoDifPiques)
                        # if (preCentro[0][1] > puntoMaximoAbajoCancha * resizer or preCentro[0][1] < puntoMaximoArribaCancha * resizer or preCentro[0][0] > puntoMaximoDerechaCancha * resizer or preCentro[0][0] < puntoMaximoIzquierdaCancha * resizer):
                        # if (posiblesPiques[1][0][0][1] > puntoMaximoAbajoCancha * resizer or preCentro[0][1] < puntoMaximoArribaCancha * resizer or preCentro[0][0] > puntoMaximoDerechaCancha * resizer or preCentro[0][0] < puntoMaximoIzquierdaCancha * resizer):
                        if type(posiblesPiques[1][0]) is not bool:
                            esta_en_cancha_posible_pique = estaEnCancha(
                                posiblesPiques[1], True)
                        if es_pique and type(posiblesPiques[1][0]) is not bool and esta_en_cancha_posible_pique:
                            #pts_piques_finales.append([coordenadaPorMatriz(posiblesPiques[1][0][0]), float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                            pts_piques_finales.append([posiblesPiques[1][0], float(
                                "{:.2f}".format(posiblesPiques[1][1] / fps))])

                        elif es_pique and type(posiblesPiques[1][0]) is not bool and not esta_en_cancha_posible_pique:
                            #pts_piques_finales_afuera.append([coordenadaPorMatriz(posiblesPiques[1][0][0]), float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                            pts_piques_finales_afuera.append(
                                [posiblesPiques[1][0], float("{:.2f}".format(posiblesPiques[1][1] / fps))])

                        elif es_pique == False and type(posiblesPiques[1][0]) is not bool:
                            #pts_golpes_finales.append([coordenadaPorMatriz(posiblesPiques[1][0][0]), float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                            pts_golpes_finales.append([posiblesPiques[1][0], float(
                                "{:.2f}".format(posiblesPiques[1][1] / fps))])

                # if (preCentro[0][1] > puntoMaximoAbajoCancha * resizer or preCentro[0][1] < puntoMaximoArribaCancha * resizer or preCentro[0][0] > puntoMaximoDerechaCancha * resizer or preCentro[0][0] < puntoMaximoIzquierdaCancha * resizer):
                # Entra a este if cuando la pelota está en la perspectiva. Creo que está demás lo de preguntar cosas para que entre al if, fijarse si no está todo ya dado por sentado antes.
                elif pre_esta_en_cancha:
                    if posiblesPiques == []:
                        #posiblesPiques.appendleft((preCentro, numeroFrame))
                        posiblesPiques.appendleft(
                            (coordenadaPorMatriz(preCentro), numeroFrame))
                        ult_posible_pique = preCentro[0]
                    elif ult_posible_pique != preCentro[0]:
                        #posiblesPiques.appendleft((preCentro, numeroFrame))
                        posiblesPiques.appendleft(
                            (coordenadaPorMatriz(preCentro), numeroFrame))
                        ult_posible_pique = preCentro[0]

                    if len(posiblesPiques) >= 2:
                        es_pique = pica(TiempoDifPiques)
                        if type(posiblesPiques[1][0]) is not bool:
                            esta_en_cancha_posible_pique = estaEnCancha(
                                posiblesPiques[1], True)

                        #TiempoDifPiques = 0
                        velocidad = True
                        punto1Velocidad = preCentro
                        TiempoDifVelocidad += 1/fps

                        # if (preCentro[0][1] > puntoMaximoAbajoCancha * resizer or preCentro[0][1] < puntoMaximoArribaCancha * resizer or preCentro[0][0] > puntoMaximoDerechaCancha * resizer or preCentro[0][0] < puntoMaximoIzquierdaCancha * resizer):
                        if es_pique and type(posiblesPiques[1][0]) is not bool and esta_en_cancha_posible_pique:
                            #pts_piques_finales.append([coordenadaPorMatriz(posiblesPiques[1][0][0]), float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                            pts_piques_finales.append([posiblesPiques[1][0], float(
                                "{:.2f}".format(posiblesPiques[1][1] / fps))])

                        elif es_pique and type(posiblesPiques[1][0]) is not bool and not esta_en_cancha_posible_pique:
                            #pts_piques_finales_afuera.append([coordenadaPorMatriz(posiblesPiques[1][0][0]), float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                            pts_piques_finales_afuera.append(
                                [posiblesPiques[1][0], float("{:.2f}".format(posiblesPiques[1][1] / fps))])

                        elif es_pique == False and type(posiblesPiques[1][0]) is not bool:
                            #pts_golpes_finales.append([coordenadaPorMatriz(posiblesPiques[1][0][0]), float("{:.2f}".format(posiblesPiques[1][1] / fps))])
                            pts_golpes_finales.append([posiblesPiques[1][0], float(
                                "{:.2f}".format(posiblesPiques[1][1] / fps))])

                            TiempoDifPiques = 0
        ################################ TIEMPO: 0.001 ###################################

        if es_pique is not None:
            es_pique = None

        ################################ TIEMPO: 0 ###################################
        centro_esta_en_cancha = estaEnCancha(centro, False)
        ################################ TIEMPO: 0 ###################################

        ################################ TIEMPO: 0.001 ###################################
        if velocidad and centro_esta_en_cancha and punto1Velocidad is not None:
            if punto1Velocidad[0] != centro[0] or punto1Velocidad[0][1] != centro[0][1]:
                diferente = True

        if velocidad and centro_esta_en_cancha and diferente:
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
        ################################ TIEMPO: 0.001 ###################################

        # Resizea y Muestra el Frame
        frame = imutils.resize(frame, anchoOG, altoOG)
        frame = imutils.resize(frame, height=768)
        mascara = imutils.resize(mascara, anchoOG, altoOG)
        mascara = imutils.resize(mascara, height=768)

        #cv2.imshow("Mascara Normal", mascara)
        #cv2.imshow("Normal", frame)

    def coordenadaPorMatriz(centro):
        ################################ TIEMPO: 0.002 (llegó a tirar 0.008) ###################################
        if type(centro) is list:
            centro = (centro, 0)
        pts1 = np.float32([[topLeftX, topLeftY], [topRightX, topRightY], [
            bottomLeftX, bottomLeftY], [bottomRightX, bottomRightY]])
        pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        perspectiva = cv2.warpPerspective(frame, matrix, (164, 474))

        cords_pelota = np.array(
            [[centro[0][0] / resizer], [centro[0][1] / resizer], [1]])
        cords_pelota_pers = np.dot(matrix, cords_pelota)
        cords_pelota_pers = (int(
            cords_pelota_pers[0]/cords_pelota_pers[2]), int(cords_pelota_pers[1]/cords_pelota_pers[2]))

        perspectiva = cv2.circle(
            perspectiva, cords_pelota_pers, 3, (0, 0, 255), -1)
        #cv2.imshow("Perspectiva", perspectiva)

        ################################ TIEMPO: 0.002 (llegó a tirar 0.008) ###################################

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
        ################################ TIEMPO: 0.001 ###################################
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
        ################################ TIEMPO: 0.001 ###################################

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
        ################################ TIEMPO: 0 (algunas veces 0.001) ###################################
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
        ################################ TIEMPO: 0 (algunas veces 0.001) ###################################
        if cnts_pts != []:
            return cualEstaMasCerca(pre_centro, cnts_pts)

    # Define qué candidato a pelota es el punto más cercano al anterior. Toma los puntos de tp_fix y analiza cual está mas cerca al pre_centro (centro anterior).

    def cualEstaMasCerca(punto, lista):
        ################################ TIEMPO: 0 (algunas veces 0.001) ###################################
        suma = []
        suma2 = []
        for i in lista:
            (xCenter, yCenter), radius = cv2.minEnclosingCircle(i)
            difEnX = abs(int(xCenter) - int(punto[0][0]))
            difEnY = abs(int(yCenter) - int(punto[0][1]))
            difRadio = abs(int(radius) - int(punto[1]))

            suma.append(difEnX + difEnY + difRadio * 3)
            suma2.append(i)
        ################################ TIEMPO: 0 (algunas veces 0.001) ###################################
        return suma2[suma.index(min(suma))]

    # Función que determina si es un pique o un golpe

    def pica(count):
        # Tengo que descubrir si la variable "b" es un pique o un golpe
        # Si es un pique, se devuelve True, de lo contrario se devuelve False

        ################################ TIEMPO: 0 (algunas veces 0.001) ###################################
        if type(posiblesPiques[0][0]) is not bool and type(posiblesPiques[1][0]) is not bool:
            abajoA = False
            abajoB = False
            a = posiblesPiques[0][0][1]
            b = posiblesPiques[1][0][1]
            if a >= 474 / 2:
                abajoA = True
            if b >= 474 / 2:
                abajoB = True
            # print("a", a)
            # print("b", b)
            # print("abajoA", abajoA)
            # print("abajoB", abajoB)
            # print("count", count)
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
            a = posiblesPiques[0][0][1]
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
        ################################ TIEMPO: 0 (algunas veces 0.001) ###################################

    def velocidadPelota(punto1, punto2, tiempo):
        ################################ TIEMPO: 0 ###################################
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

        ################################ TIEMPO: 0 ###################################
        return int(np.rint(distancia / tiempo * 3.6))

    def estaEnCancha(centro_pelota, perspectiva):
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

    vs = cv2.VideoCapture("./InkedInkedTennisBrothersVideo1080p.mp4")

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
    pts_piques_finales_afuera = []
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

    tiempo_inicial = time.time()
    for _ in range(frame_count):

        numeroFrame += 1
        #print("Numero de Frame: ", numeroFrame)

        TiempoSegundosEmpezoVideo += 1/fps

        ################################ TIEMPO: 0.1 ###################################
        frame = vs.read()[1]
        ################################ TIEMPO: 0.1 ###################################
        #frame = frame[1] if args.get("video", False) else frame

        if frame is None:
            break

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
            cv2.imwrite('zoomed_image.jpg', zoomed_area)
            # break

        pts1 = np.float32([[topLeftX, topLeftY],       [topRightX, topRightY],
                           [bottomLeftX, bottomLeftY], [bottomRightX, bottomRightY]])
        pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

        #matrix = cv2.getPerspectiveTransform(pts1, pts2)
        #result = cv2.warpPerspective(frame, matrix, (164, 474))

        ################################ TIEMPO: 0.1 ###################################
        start_time = time.time()
        main(frame)
        print("Tiempo:", time.time() - start_time, " - Frame:", numeroFrame)
        ################################ TIEMPO: 0.1 ###################################

        # print("pts_piques", pts_piques_finales)
        # print("pts_golpes", pts_golpes_finales)

        # Terminar la ejecución si se presiona la "q"
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if key == ord('p'):
            cv2.waitKey(-1)

    print("Tiempo total:", time.time() - tiempo_inicial)
    print(pts_piques_finales)

    vs.release()

    return pts_piques_finales
# cv2.destroyAllWindows()
