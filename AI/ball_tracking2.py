from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time

# Argumentos del programa
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", # Dirección del video a analizar
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, # Longitud del trazado de la trayectoria
	help="max buffer size")
args = vars(ap.parse_args())

def main(frame, numeroGlob):
    global TiempoDeteccionUltimaPelota
    global primeraVez
    global preCentro
    global TiempoTresCentrosConsecutivos
    # global radius
    # global x
    # global y
    # global Gerard
    # global esGerard
    # global posiblePique
    # global countDifPiques
    # global countDifVelocidad
    # global punto1Velocidad
    # global diferente
    # global velocidad
    # global velocidadFinal
    # global afterVelocidad
    # global topLeftX, topLeftY, topRightX, topRightY, bottomLeftX, bottomLeftY, bottomRightX, bottomRightY
    # global estaCercaX
    # global estaCercaY
    # global ult_posible_pique

    anchoOG = frame.shape[1]
    altoOG = frame.shape[0]
    
    estaCercaX = anchoOG * 10/100
    estaCercaY = altoOG * 10/100

    frame = imutils.resize(frame, anchoOG * resizer, altoOG * resizer)

    # Cámara lenta para mayor análisis
    #cv2.waitKey(100)
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #blurred = cv2.dilate(frame, None, iterations=2)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # Filtra los tonos verdes de la imagen
    mascara = cv2.inRange(hsv, greenLower, greenUpper)
    mascara = cv2.erode(mascara, None, iterations=2)
    mascara = cv2.dilate(mascara, None, iterations=2)
    
    # Toma todos los contornos de la imagen
    contornos = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos = imutils.grab_contours(contornos)
    
    centro = None
    
    if (TiempoSegundosEmpezoVideo % 5 == 0):
        eliminarContornosInservibles(todosContornos)
        #if numeroGlob == 0:
            #eliminarContornosInservibles(todosContornos)
        #else:
            #eliminarContornosInservibles(todosContornos)
    
    if len(contornos) > 0:
        # Busca el contorno más grande y encuentra su posición (x, y)
        # if numeroGlob == 0:
        #     contornosQuietos(cnts, todosContornos_norm, contornosIgnorar_norm)
        #     #if len(ultimosCentros_norm) == 5 and TiempoDeteccionUltimaPelota[numeroGlob] >= 0.3 and not seEstaMoviendo(ultimosCentros_norm):
        #     if len(ultimosCentros_norm) == 5 and TiempoDeteccionUltimaPelota[numeroGlob] >= 0.3 and not seEstaMoviendo(ultimosCentros_norm):
        #         cnts = ignorarContornosQuietos(cnts, contornosIgnorar_norm)
        
        # else:
        #     contornosQuietos(cnts, todosContornos_pers, contornosIgnorar_pers)
        #     if len(ultimosCentros_pers) == 5 and TiempoDeteccionUltimaPelota[numeroGlob] >= 0.3 and not seEstaMoviendo(ultimosCentros_pers):
        #         #print("Count", TiempoDeteccionUltimaPelota[numeroGlob])
        #         #print("Ultimos Centros", ultimosCentros_pers)
        #         cnts = ignorarContornosQuietos(cnts, contornosIgnorar_pers)

        contornosQuietos(contornos, todosContornos, contornosIgnorar)
        if len(ultimosCentros) == 5 and TiempoDeteccionUltimaPelota >= 0.3 and seEstaMoviendo(ultimosCentros) == False:
            contornos = ignorarContornosQuietos(contornos, contornosIgnorar)
                
        if len(contornos) > 0:
            if primeraVez:
                casiCentro = max(contornos, key=cv2.contourArea)
                ((x, y), radio) = cv2.minEnclosingCircle(casiCentro)
                M = cv2.moments(casiCentro)
                centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), int(radio)

                primeraVez = False
                preCentro = centro
                TiempoDeteccionUltimaPelota = 0
                TiempoTresCentrosConsecutivos = 0

                pique3.appendleft(centro[0][1])
                ultimosCentros.appendleft(centro)
            
            else:
                c = tp_fix(contornos, preCentro, TiempoDeteccionUltimaPelota[numeroGlob])
                
                if c is not None:
                    ((x, y), radio) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    centro = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])], int(radio)
                    preCentro = centro
                    TiempoTresCentrosConsecutivos += TiempoDeteccionUltimaPelota[numeroGlob]
                    TiempoDeteccionUltimaPelota[numeroGlob] = 0
                    # if numeroGlob == 0:
                    #     pique3_norm.appendleft(center_glob[numeroGlob][0][1])
                    #     ultimosCentros_norm.appendleft(center_glob[numeroGlob])
                    # else:
                    #     pique3_pers.appendleft(center_glob[numeroGlob][0][1])
                    #     ultimosCentros_pers.appendleft(center_glob[numeroGlob])
                    #if len(pique3) == 3 and count2 <= 0.1:
                        #pica(pique3[2], pique3[1], pique3[0])
                        #count2 = 0
                    pique3.appendleft(centro[0][1])
                    ultimosCentros.appendleft(centro)
                
                else:
                    if TiempoDeteccionUltimaPelota >= 0.3:
                        primeraVez = True
                        preCentro = None
                    TiempoDeteccionUltimaPelota += 1/fps
                    TiempoTresCentrosConsecutivos = 0
                
            # Sigue si el contorno tiene cierto tamaño
            if c is not None:
                # Dibuja el círculo en la pelota
                cv2.circle(frame, (int(x), int(y)), int(radio), (0, 255, 255), 2)
                cv2.circle(frame, (centro[0][0], centro[0][1]), 5, (0, 0, 255), -1)
    
    else:
        if TiempoDeteccionUltimaPelota >= 0.3:
            primeraVez = True
            preCentro = None
        TiempoDeteccionUltimaPelota += 1/fps
        TiempoTresCentrosConsecutivos = 0
    
    # Actualiza los puntos para trazar la trayectoria
    pts_pelota_norm.appendleft(centro)
    pts_pelota_pers.appendleft(centro)

    for i in range(1, len(pts_pelota_norm)):
        # Ignora los puntos de trayectoria inexistentes
        if pts_pelota_norm[i - 1] is None or pts_pelota_norm[i] is None:
            continue
        
        # Traza la trayectoria
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts_pelota_norm[i - 1][0], pts_pelota_norm[i][0], (0, 0, 255), thickness)
    
    for i in range(1, len(pts_pelota_pers)):
        # Ignora los puntos de trayectoria inexistentes
        if pts_pelota_pers[i - 1] is None or pts_pelota_pers[i] is None:
            continue
        
        # Traza la trayectoria
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts_pelota_pers[i - 1][0], pts_pelota_pers[i][0], (0, 0, 255), thickness)
    
    bajando = False
    
    if (center_glob[numeroGlob] is not None):
        #print("Centro", center_glob[numeroGlob][0][1])
        
        if numeroGlob == 0:
            pique_norm.appendleft(center_glob[numeroGlob][0][1])
            if (len(pique_norm) >= 2):
                if (pique_norm[0] - pique_norm[1] > 0):
                    bajando = True
                if (pique_norm[0] - pique_norm[1] != 0):
                    pique2_norm.appendleft((bajando, numeroFrame))
                else: bajando = "Indeterminación"
            print("Bajando", bajando)
        
        else:
            pique_pers.appendleft(center_glob[numeroGlob][0][1])
            if (len(pique_pers) >= 2):
                if (pique_pers[0] - pique_pers[1] > 0):
                    bajando = True
                if (pique_pers[0] - pique_pers[1] != 0):
                    pique2_pers.appendleft((bajando, numeroFrame))
                else: bajando = "Indeterminación"
            print("Bajando", bajando)
    
    #velocidad = False
    
    if numeroGlob == 0:
        countDifPiques += 1/fps
        posiblePique = False
        if (len(pique2_norm) >= 2):
            if pique2_norm[0][0] == False and pique2_norm[1][0] == True and preCentro_glob[numeroGlob] is not None and pique2_norm[0][1] - pique2_norm[1][1] <= fps/6 and center_glob[numeroGlob] is not None:
                #print("Pique 2", pique2_norm)
                print("Gerard")
                posiblePique = True
                posiblesPiques_norm.appendleft(preCentro_glob[numeroGlob])
                if len(posiblesPiques_norm) == 1: countDifPiques = 0
                #frame = cv2.putText(frame, 'Gerard', (preCentro_glob[numeroGlob][0][0], preCentro_glob[numeroGlob][0][1]), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 0, 2)
    
    else:
        if (len(pique2_norm) >= 2):
            puntoMaximoArribaCancha = min(topLeftY, topRightY)
            puntoMaximoAbajoCancha = max(bottomLeftY, bottomRightY)
            puntoMaximoIzquierdaCancha = min(topLeftX, bottomLeftX)
            puntoMaximoDerechaCancha = max(topRightX, bottomRightX)
            if posiblePique and preCentro_glob[0] is not None and center_glob[0] is not None and (preCentro_glob[0][0][1] > puntoMaximoAbajoCancha * resizer_glob[0] or preCentro_glob[0][0][1] < puntoMaximoArribaCancha * resizer_glob[0] or preCentro_glob[0][0][0] > puntoMaximoDerechaCancha * resizer_glob[0] or preCentro_glob[0][0][0] < puntoMaximoIzquierdaCancha * resizer_glob[0]):
                #Gerard = False
                mitadDeCancha = (puntoMaximoAbajoCancha - puntoMaximoArribaCancha) / 2
                print("Center y Mitad de Cancha", preCentro_glob[0], mitadDeCancha)
                if preCentro_glob[0][0][1] <= mitadDeCancha: abajo = False
                else: abajo = True

                if posiblesPiques_pers == []:
                    posiblesPiques_pers.appendleft((abajo, preCentro_glob[0][0], numeroFrame))
                    ult_posible_pique = preCentro_glob[0][0]
                elif preCentro_glob[0][0] != ult_posible_pique:
                    posiblesPiques_pers.appendleft((abajo, preCentro_glob[0][0], numeroFrame))
                    ult_posible_pique = preCentro_glob[0][0]
                
                if len(posiblesPiques_pers) >= 2:
                    Gerard = pica(countDifPiques)
                    print("Gerard", Gerard)
                    if Gerard and type(posiblesPiques_pers[1][0]) is not bool:
                        #if pique2_pers[0][0] == False and pique2_pers[1][0] == True and preCentro_glob[numeroGlob] is not None and pique2_pers[0][1] - pique2_pers[1][1] <= fps/6:
                        #pts_piques_finales.append([[preCentro_glob[numeroGlob][0][0], preCentro_glob[numeroGlob][0][1]], float("{:.2f}".format(numeroFrame / fps))])
                        # pts_piques_finales.append([posiblesPiques_pers[1][0], float("{:.2f}".format(numeroFrame / fps))])
                        pts_piques_finales.append([posiblesPiques_pers[1][0][0], float("{:.2f}".format(posiblesPiques_pers[1][1] / fps))])

                    elif not Gerard and type(posiblesPiques_pers[1][0]) is not bool:
                        #pts_golpes_finales.append([[preCentro_glob[numeroGlob][0][0], preCentro_glob[numeroGlob][0][1]], float("{:.2f}".format(numeroFrame / fps))])
                        pts_golpes_finales.append([posiblesPiques_pers[1][0][0], float("{:.2f}".format(posiblesPiques_pers[1][1] / fps))])
            
            elif posiblePique and preCentro_glob[numeroGlob] is not None and center_glob[numeroGlob] is not None:
                #print("Pique 2", pique2_pers)
                print("Gerard")
                if posiblesPiques_pers == []:
                    posiblesPiques_pers.appendleft((preCentro_glob[numeroGlob], numeroFrame))
                    ult_posible_pique = preCentro_glob[numeroGlob][0]
                elif ult_posible_pique != preCentro_glob[numeroGlob][0]:
                    posiblesPiques_pers.appendleft((preCentro_glob[numeroGlob], numeroFrame))
                    ult_posible_pique = preCentro_glob[numeroGlob][0]
                #print("Posibles Piques", posiblesPiques_pers)
                countDifPiques = 0
                #frame = cv2.putText(frame, 'Gerard', (preCentro_glob[numeroGlob][0][0], preCentro_glob[numeroGlob][0][1]), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 0, 2)
                pts_pique.append([[preCentro_glob[numeroGlob][0][0], preCentro_glob[numeroGlob][0][1]], float("{:.2f}".format(numeroFrame / fps))])
                print("ES ESTE", pts_pique)
                velocidad = True
                punto1Velocidad = preCentro_glob[numeroGlob]
                countDifVelocidad += 1/fps
                if len(posiblesPiques_pers) >= 2:
                    Gerard = pica(countDifPiques)
                    print("Gerard", Gerard)
                    if Gerard and type(posiblesPiques_pers[1][0]) is not bool:
                        #pts_piques_finales.append([[preCentro_glob[numeroGlob][0][0], preCentro_glob[numeroGlob][0][1]], float("{:.2f}".format(numeroFrame / fps))])
                        pts_piques_finales.append([posiblesPiques_pers[1][0][0], float("{:.2f}".format(posiblesPiques_pers[1][1] / fps))])
                    if Gerard is False and type(posiblesPiques_pers[1][0]) is not bool:
                        #pts_golpes_finales.append([[preCentro_glob[numeroGlob][0][0], preCentro_glob[numeroGlob][0][1]], float("{:.2f}".format(numeroFrame / fps))])
                        pts_golpes_finales.append([posiblesPiques_pers[1][0][0], float("{:.2f}".format(posiblesPiques_pers[1][1] / fps))])
    
    if numeroGlob == 0 and Gerard:
        Gerard = None
        #frame = cv2.putText(frame, 'Gerard', (pts_piques_finales[0][0]), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 0, 2)
    elif numeroGlob == 0 and Gerard == False:
        Gerard = None
        #frame = cv2.putText(frame, 'Heatmap', (pts_golpes_finales[0][0]), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 0, 2)
    
    if velocidad and center_glob[numeroGlob] is not None and punto1Velocidad is not None and numeroGlob == 1:
        print("Punto1", punto1Velocidad)
        print("Center", center_glob[numeroGlob])
        if punto1Velocidad[0][0] != center_glob[numeroGlob][0][0] or punto1Velocidad[0][1] != center_glob[numeroGlob][0][1]:
            diferente = True
    
    if velocidad and center_glob[numeroGlob] is not None and numeroGlob == 1 and diferente:
        #print("PreCentro", preCentro_glob[numeroGlob])
        #print("Centro", center_glob[numeroGlob])
        print("Punto1", punto1Velocidad)
        print("Punto2", center_glob[numeroGlob])
        print("Tiempo", countDifVelocidad)
        velocidadFinal = velocidadGolpe(punto1Velocidad, center_glob[numeroGlob], countDifVelocidad)
        print("Velocidad Final", velocidadFinal, "Kilometros por Hora")
        #cv2.circle(frame, (int(punto1Velocidad[0][0]), int(punto1Velocidad[0][1])), 50, (255, 255, 255), -1)
        #cv2.circle(frame, (int(center_glob[numeroGlob][0][0]), int(center_glob[numeroGlob][0][1])), 50, (255, 255, 255), -1)
        velocidad = False
        punto1Velocidad = None
        countDifVelocidad = 0
        diferente = False
        afterVelocidad = True

    elif velocidad and numeroGlob == 1:
        countDifVelocidad += 1/fps

    elif countDifVelocidad >= 0.5 and numeroGlob == 1:
        countDifVelocidad = 0
        velocidad = False
        punto1Velocidad = None
        diferente = False

    if afterVelocidad and numeroGlob == 0 and center_glob[numeroGlob] is not None:
        #frame = cv2.putText(frame, str(velocidadFinal), (center_glob[numeroGlob][0][0], center_glob[numeroGlob][0][1]), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 0, 2)
        afterVelocidad = False
    
    #cv2.circle(frame, (100 * resizer_glob[numeroGlob], 194 * resizer_glob[numeroGlob]), 50, (255, 255, 0), -1)
    #cv2.circle(frame, (88 * resizer_glob[numeroGlob], 164 * resizer_glob), 25, (255, 255, 0), -1)

    # if numeroGlob == 0:
    #     if center_glob[numeroGlob] is not None:
    #         pique3_norm.appendleft(center_glob[numeroGlob][1])
    #     if len(pique3_norm) == 3 and TiempoTresCentrosConsecutivos[numeroGlob] <= 0.1:
    #         pica(pique3_norm[2], pique3_norm[1], pique3_norm[0])
    #         TiempoTresCentrosConsecutivos[numeroGlob] = 0
    # else:
    #     if center_glob[numeroGlob] is not None:
    #         pique3_pers.appendleft(center_glob[numeroGlob][1])
    #     if len(pique3_pers) == 3 and TiempoTresCentrosConsecutivos[numeroGlob] <= 0.1:
    #         pica(pique3_pers[2], pique3_pers[1], pique3_pers[0])
    #         TiempoTresCentrosConsecutivos[numeroGlob] = 0

    # if numeroGlob == 0:
    #     Gerard = False
    #     if center_glob[numeroGlob] is not None:
    #         pique3_norm.appendleft(center_glob[numeroGlob])
    #     if (len(pique2_norm) >= 2):
    #         if pique2_norm[0] == False and pique2_norm[1] == True:
    #             frame = cv2.putText(frame, 'Posible Gerard', pique3_norm[1], cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 0, 2)
    #             Gerard = True
    #             if esGerard:
    #                 print("Picoooooooooooooooooooooooooooooooooo")
    #                 frame = cv2.putText(frame, 'Gerard', pique3_norm[2], cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 0, 2)
    #     esGerard = None

    # else:
    #     if center_glob[numeroGlob] is not None:
    #         pique3_pers.appendleft(center_glob[numeroGlob])
    #     if (len(pique2_pers) >= 2):
    #         if Gerard:
    #             print("Count2: ", TiempoTresCentrosConsecutivos[numeroGlob], "Center", center_glob[numeroGlob])
    #             #if len(pique3_pers) == 3 and TiempoTresCentrosConsecutivos[numeroGlob] <= 0.2 and TiempoTresCentrosConsecutivos[numeroGlob] > 0 and center_glob[numeroGlob] is not None:
    #             if len(pique3_pers) == 3 and TiempoTresCentrosConsecutivos[numeroGlob] <= 0.3 and center_glob[numeroGlob] is not None:
    #                 esGerard = pica(pique3_pers[2][1], pique3_pers[1][1], pique3_pers[0][1])
    #                 #pica(pique3_pers[2][1], pique3_pers[1][1], pique3_pers[0][1])
    #                 TiempoTresCentrosConsecutivos[numeroGlob] = 0
    #             if esGerard:
    #                 print("Picoooooooooooooooooooooooooooooooooo")
    #                 frame = cv2.putText(frame, 'Gerard', pique3_pers[1], cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 0, 2)
    
    # Resizea y Muestra el Frame
    if numeroGlob == 0:

        frame = imutils.resize(frame, anchoOG, altoOG)
        frame = imutils.resize(frame, height= 768)
        mask = imutils.resize(mask, anchoOG, altoOG)
        mask = imutils.resize(mask, height= 768)

        cv2.imshow("Mask Normal", mask)
        cv2.imshow("Normal", frame)

    else:

        frame = imutils.resize(frame, anchoOG, altoOG)
        mask = imutils.resize(mask, anchoOG, altoOG)

        cv2.imshow("Mask Perspectiva", mask)
        cv2.imshow("Perspective", frame)

    print("Centro al terminar la iteración", center_glob[numeroGlob])
    print("Numero Global", numeroGlob)
    print("Puntos Piques Pers", list(posiblesPiques_pers))
    print("Puntos Piques Finales", pts_piques_finales)
    print("Puntos Golpes Finales", pts_golpes_finales)

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
    for i in cnts:
        count = 0
        (x, y), radius = cv2.minEnclosingCircle(i)
        x, y, radius = int(x), int(y), int(radius)
        for l in todosContornos:
            for j in l:
                if x - j[0][0] >= -10 and x - j[0][0] <= 10 and y - j[0][1] >= -10 and y - j[0][1] <= 10:
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
    
    for l in todosContornos:
        existe = False
        if (len(l) >= 10):
            promedioIgnorarX = 0
            promedioIgnorarY = 0
            for j in l:
                promedioIgnorarX += j[0][0]
                promedioIgnorarY += j[0][1]
            promedioIgnorarX /= len(l)
            promedioIgnorarY /= len(l)
            promedioIgnorarX, promedioIgnorarY = int(np.rint(promedioIgnorarX)), int(np.rint(promedioIgnorarY))
            if (len(contornosIgnorar) == 0): contornosIgnorar.append((promedioIgnorarX, promedioIgnorarY))
            for h in contornosIgnorar:
                if (h[0] == promedioIgnorarX and h[1] == promedioIgnorarY):
                    existe = True
            if not existe:
                contornosIgnorar.append((promedioIgnorarX, promedioIgnorarY))
                #print("Encontré un contorno que tengo que ignorar")
    
    #print("Todos los Contornos", todosContornos)
    #print("Contornos a Ignorar", contornosIgnorar)

# Ignora los contornos quietos encontrados en la función anterior
def ignorarContornosQuietos(cnts, contornosIgnorar):
    new_cnts = []
    Ignorar = False
    for cnt in cnts:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        print("Circulo Posible", (int(x), int(y), int(radius)))
        for i in contornosIgnorar:
            if x - i[0] >= -20 and x - i[0] <= 20 and y - i[1] >= -20 and y - i[1] <= 20:
                Ignorar = True
                break
            else:
                Ignorar = False
        
        if Ignorar == False: new_cnts.append(cnt)
    
    for i in new_cnts:
        print("Nueva lista", cv2.minEnclosingCircle(i))
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
    if numeroGlob == 0:
        medidorX = 100
        medidorY = 103
        #medidorX = estaCercaX
        #medidorY = estaCercaY
    else:
        medidorX = 70
        medidorY = 151
    print("Pre Centro", preCentro_glob[numeroGlob])
    for contorno in contornos:
        ((x, y), radius) = cv2.minEnclosingCircle(contorno)
        print("Círculo", (x, y, radius))
        if x - pre_centro[0][0] > medidorX * resizer_glob[numeroGlob] or pre_centro[0][0] - x > medidorX * resizer_glob[numeroGlob] or y - pre_centro[0][1] > medidorY * resizer_glob[numeroGlob] or pre_centro[0][1] - y > medidorY * resizer_glob[numeroGlob] and count <= 0.5:
            continue
        cnts_pts.append(contorno)
    if cnts_pts != []:
        return cualEstaMasCerca(pre_centro, cnts_pts)
    else: print("No se encontró la pelota")

# Define qué candidato a pelota es el punto más cercano al anterior. Toma los puntos de tp_fix y analiza cual está mas cerca al pre_centro (centro anterior).
def cualEstaMasCerca(punto, lista):
    suma = []
    suma2 = []
    for i in lista:
        (xCenter, yCenter), radius = cv2.minEnclosingCircle(i)
        difEnX = int(xCenter) - int(punto[0][0])
        difEnY = int(yCenter) - int(punto[0][1])
        difRadio = int(radius) - int(punto[1])
        
        if difEnX < 0:
            difEnX *= -1
        
        if difEnY < 0:
            difEnY *= -1 
        
        if difRadio < 0:
            difRadio *= -1
        
        suma.append(difEnX + difEnY + difRadio * 3)
        suma2.append(i)
    return suma2[suma.index(min(suma))]

# Toma la cámara si no recibe video
if not args.get("video", False):
    vs = cv2.VideoCapture(0)

    # Toma video en caso de haber
else:
    vs = cv2.VideoCapture(args["video"])

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

pts_pique = []

pts_piques_finales = []
pts_golpes_finales = []

ult_posible_pique = None

pts_pelota_norm = deque(maxlen=args["buffer"])
pts_pelota_pers = deque(maxlen=args["buffer"])

preCentro = None
primeraVez = True
centro = None

# Fps del video
fps = int(vs.get(cv2.CAP_PROP_FPS))

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
resizer= [3, 15]

altoOG = 0
anchoOG = 0

Gerard = None
esGerard = None
posiblePique = False
posiblesPiques = []

# CountDifVelocidad cuenta cuento tiempo en segundos pasa desde que se encontraron los dos puntos para usar en la velocidad
TiempoDifVelocidad = 0

# CountDifPiques cuenta cuanto tiempo pasa desde que se encontró un pique hasta que se encuentra el siguiente
TiempoDifPiques = 0

# El número del Frame del video
numeroFrame = 0

punto1Velocidad = None
velocidad = False
diferente = False
velocidadFinal = None
afterVelocidad = False

while True:
    numeroFrame += 1
    print("Numero de Frame: ", numeroFrame)

    TiempoSegundosEmpezoVideo += 1/fps

    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    if frame is None:
        break

    pts1 = np.float32([[topLeftX, topLeftY],       [topRightX, topRightY],
                         [bottomLeftX, bottomLeftY], [bottomRightX, bottomRightY]])
    pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (164, 474))

    main()

    # Terminar la ejecución si se presiona la "q"
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    if key == ord('p'):
        cv2.waitKey(-1)
    
    #print("Centro al terminar la iteración", center)
    print("Pasé de frame")

if not args.get("video", False):
    vs.stop()

else:
    vs.release()
print("Arotu")
cv2.destroyAllWindows()