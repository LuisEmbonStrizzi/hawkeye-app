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

# Función que determina si es un pique o un golpe
def pica (count):
    # Tengo que descubrir si la variable "b" es un pique o un golpe
    # Si es un pique, se devuelve True, de lo contrario se devuelve False

    if type(posiblesPiques_pers[0][0]) is not bool and type(posiblesPiques_pers[1][0]) is not bool:
        abajoA = False
        abajoB = False
        a = posiblesPiques_pers[0][0][0][1] / resizer_glob[numeroGlob]
        b = posiblesPiques_pers[1][0][0][1] / resizer_glob[numeroGlob]
        #cv2.circle(frame, posiblesPiques_pers[0][0], 40, (255, 255, 255), -1)
        #cv2.circle(frame, posiblesPiques_pers[1][0], 40, (255, 255, 255), -1)
        if a >= 474 / 2: abajoA = True
        if b >= 474 / 2: abajoB = True
        print("a", a)
        print("b", b)
        print("abajoA", abajoA)
        print("abajoB", abajoB)
        print("count", count)
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

    elif type(posiblesPiques_pers[0][0]) is bool and type(posiblesPiques_pers[1][0]) is bool:
        a = posiblesPiques_pers[0][0]
        b = posiblesPiques_pers[1][0]
        a2 = posiblesPiques_pers[0][1]
        b2 = posiblesPiques_pers[1][1]

        print("A", a)
        print("B", b)
        print("A", a2)
        print("B", b2)
        print("Count", count)

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
        
    elif type(posiblesPiques_pers[0][0]) is bool:
        abajoB = False
        b = posiblesPiques_pers[1][0][0][1] / resizer_glob[numeroGlob]
        if b >= 474 / 2: abajoB = True

        a = posiblesPiques_pers[0][0]

        print("A", a)
        print("B", b)
        print("Count", count)

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

    elif type(posiblesPiques_pers[1][0]) is bool:
        abajoA = False
        a = posiblesPiques_pers[0][0][0][1] / resizer_glob[numeroGlob]
        if a >= 474 / 2: abajoA = True

        b = posiblesPiques_pers[1][0]

        print("A", a)
        print("B", b)
        print("Count", count)

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

def velocidadGolpe(punto1, punto2, tiempo):
    punto1X = punto1[0][0] / (resizer_glob[numeroGlob] * 20)
    punto1Y = punto1[0][1] / (resizer_glob[numeroGlob] * 20)
    punto2X = punto2[0][0] / (resizer_glob[numeroGlob] * 20)
    punto2Y = punto2[0][1] / (resizer_glob[numeroGlob] * 20)

    if punto1X >= punto2X: movimientoX = punto1X - punto2X
    elif punto1X <= punto2X: movimientoX = punto2X - punto1X

    if punto1Y >= punto2Y: movimientoY = punto1Y - punto2Y
    elif punto1Y <= punto2Y: movimientoY = punto2Y - punto1Y

    distancia = np.sqrt(movimientoX * movimientoX + movimientoY * movimientoY)
    #distancia *= 1.5

    return int(np.rint(distancia / tiempo * 3.6))

def main(frame, numeroGlob):
    global radius
    global x
    global y
    global Gerard
    global esGerard
    global posiblePique
    global countDifPiques
    global countDifVelocidad
    global punto1Velocidad
    global diferente
    global velocidad
    global velocidadFinal
    global afterVelocidad
    global topLeftX, topLeftY, topRightX, topRightY, bottomLeftX, bottomLeftY, bottomRightX, bottomRightY
    global estaCercaX
    global estaCercaY
    global ult_posible_pique

    anchoOG = frame.shape[1]
    altoOG = frame.shape[0]
    
    estaCercaX = anchoOG * 10/100
    estaCercaY = altoOG * 10/100

    #print("Esta Cerca X", estaCercaX)
    #print("Esta Cerca Y", estaCercaY)

    frame = imutils.resize(frame, anchoOG * resizer_glob[numeroGlob], altoOG * resizer_glob[numeroGlob])

    # Cámara lenta para mayor análisis
    #cv2.waitKey(100)
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #blurred = cv2.dilate(frame, None, iterations=2)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # Filtra los tonos verdes de la imagen
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    #cv2.imshow("mask2", mask)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   #morphology close operation for remove small noise point
    #cv2.imshow("mask3", mask)
    
    # Toma todos los contornos de la imagen
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    center_glob[numeroGlob] = None
    
    #if numeroGlob == 0:
        #for h in contornosIgnorar_norm:
            #cv2.circle(frame, (h[0], h[1]), 20, (255, 255, 255), -1)
    
    #else:
        #for h in contornosIgnorar_pers:
            #cv2.circle(frame, (h[0], h[1]), 20, (255, 255, 255), -1)
    
    if (countSegundosTotales % 5 == 0):
        if numeroGlob == 0:
            eliminarContornosInservibles(todosContornos_norm)
        else:
            eliminarContornosInservibles(todosContornos_pers)
    
    #print("Length Contornos", len(cnts))
    
    if len(cnts) > 0:
        # Busca el contorno más grande y encuentra su posición (x, y)
        if numeroGlob == 0:
            contornosQuietos(cnts, todosContornos_norm, contornosIgnorar_norm)
            #if len(ultimosCentros_norm) == 5 and count_glob[numeroGlob] >= 0.3 and not seEstaMoviendo(ultimosCentros_norm):
            if len(ultimosCentros_norm) == 5 and count_glob[numeroGlob] >= 0.3 and not seEstaMoviendo(ultimosCentros_norm):
                cnts = ignorarContornosQuietos(cnts, contornosIgnorar_norm)
        
        else:
            contornosQuietos(cnts, todosContornos_pers, contornosIgnorar_pers)
            if len(ultimosCentros_pers) == 5 and count_glob[numeroGlob] >= 0.3 and not seEstaMoviendo(ultimosCentros_pers):
                #print("Count", count_glob[numeroGlob])
                #print("Ultimos Centros", ultimosCentros_pers)
                cnts = ignorarContornosQuietos(cnts, contornosIgnorar_pers)
                
        if len(cnts) > 0:
            if primeraVez_glob[numeroGlob]:
                #print("Primera Vez")
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center_glob[numeroGlob] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), int(radius)
                # if esResult == False:
                #     primeraVez_glob[0] = False
                # else:
                #     primeraVez_glob[1] = False
                primeraVez_glob[numeroGlob] = False
                preCentro_glob[numeroGlob] = center_glob[numeroGlob]
                count_glob[numeroGlob] = 0
                count2_glob[numeroGlob] = 0
                if numeroGlob == 0:
                    pique3_norm.appendleft(center_glob[numeroGlob][0][1])
                    ultimosCentros_norm.appendleft(center_glob[numeroGlob])
                else:
                    pique3_pers.appendleft(center_glob[numeroGlob][0][1])
                    ultimosCentros_pers.appendleft(center_glob[numeroGlob])
            
            else:
                c = tp_fix(cnts, preCentro_glob[numeroGlob], count_glob[numeroGlob])
                
                if c is not None:
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center_glob[numeroGlob] = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])], int(radius)
                    preCentro_glob[numeroGlob] = center_glob[numeroGlob]
                    # count2_glob[numeroGlob] += count_glob[numeroGlob]
                    count2_glob[numeroGlob] += count_glob[numeroGlob]
                    count_glob[numeroGlob] = 0
                    if numeroGlob == 0:
                        pique3_norm.appendleft(center_glob[numeroGlob][0][1])
                        ultimosCentros_norm.appendleft(center_glob[numeroGlob])
                    else:
                        pique3_pers.appendleft(center_glob[numeroGlob][0][1])
                        ultimosCentros_pers.appendleft(center_glob[numeroGlob])
                    #if len(pique3) == 3 and count2 <= 0.1:
                        #pica(pique3[2], pique3[1], pique3[0])
                        #count2 = 0
                
                else:
                    if count_glob[numeroGlob] >= 0.3 and numeroGlob == 0 or count_glob[numeroGlob] >= 0.4 and numeroGlob == 1:
                        primeraVez_glob[numeroGlob] = True
                        preCentro_glob[numeroGlob] = None
                    count_glob[numeroGlob] += 1/fps
                    count2_glob[numeroGlob] = 0
                
            # Sigue si el contorno tiene cierto tamaño
            if radius > 0 and primeraVez_glob[numeroGlob] and c is not None or c is not None:
                # Dibuja el círculo en la pelota
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, (center_glob[numeroGlob][0][0], center_glob[numeroGlob][0][1]), 5, (0, 0, 255), -1)
    
    else:
        if count_glob[numeroGlob] >= 0.3 and numeroGlob == 0 or count_glob[numeroGlob] >= 0.4 and numeroGlob == 1:
            primeraVez_glob[numeroGlob] = True
            preCentro_glob[numeroGlob] = None
        count_glob[numeroGlob] += 1/fps
        count2_glob[numeroGlob] = 0
    

    # La variable count es asignada
    # if esResult == False: 
    #     if count != 0:
    #         count_glob2[0] += count
    #     else:
    #         count_glob2[0] = count
    # else:
    #     if count != 0:
    #         count_glob2[1] += count
    #     else:
    #         count_glob2[1] = count
    
    # Actualiza los puntos para trazar la trayectoria
    if numeroGlob == 0:
        pts_norm.appendleft(center_glob[numeroGlob])
    else:
        pts_pers.appendleft(center_glob[numeroGlob])
    
    if numeroGlob == 0:
        for i in range(1, len(pts_norm)):
            # Ignora los puntos de trayectoria inexistentes
            if pts_norm[i - 1] is None or pts_norm[i] is None:
                continue
            
            # Traza la trayectoria
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts_norm[i - 1][0], pts_norm[i][0], (0, 0, 255), thickness)
    
    else:
        for i in range(1, len(pts_pers)):
            # Ignora los puntos de trayectoria inexistentes
            if pts_pers[i - 1] is None or pts_pers[i] is None:
                continue
            
            # Traza la trayectoria
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts_pers[i - 1][0], pts_pers[i][0], (0, 0, 255), thickness)
    
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
            print("Pique", pique_norm)
            print("Pique 2", pique2_norm)
            print("Centro", center_glob)
            print("PreCentro", preCentro_glob)
        
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
                    print("Posibles Piques pers", posiblesPiques_pers)
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


            #elif posiblePique and center_glob[numeroGlob] is None and center_glob[0] is not None:
                #Gerard = False

            #elif posiblePique and center_glob[numeroGlob] is None:
                #Gerard = False
                #puntoMaximoArribaCancha = min(topLeftY, topRightY)
                #puntoMaximoAbajoCancha = max(bottomLeftY, bottomRightY)
                #mitadDeCancha = (puntoMaximoAbajoCancha - puntoMaximoArribaCancha) / 2
                #if center_glob[0][0][1] <= mitadDeCancha: abajo = False
                #else: abajo = True
    
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
    #     if len(pique3_norm) == 3 and count2_glob[numeroGlob] <= 0.1:
    #         pica(pique3_norm[2], pique3_norm[1], pique3_norm[0])
    #         count2_glob[numeroGlob] = 0
    # else:
    #     if center_glob[numeroGlob] is not None:
    #         pique3_pers.appendleft(center_glob[numeroGlob][1])
    #     if len(pique3_pers) == 3 and count2_glob[numeroGlob] <= 0.1:
    #         pica(pique3_pers[2], pique3_pers[1], pique3_pers[0])
    #         count2_glob[numeroGlob] = 0

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
    #             print("Count2: ", count2_glob[numeroGlob], "Center", center_glob[numeroGlob])
    #             #if len(pique3_pers) == 3 and count2_glob[numeroGlob] <= 0.2 and count2_glob[numeroGlob] > 0 and center_glob[numeroGlob] is not None:
    #             if len(pique3_pers) == 3 and count2_glob[numeroGlob] <= 0.3 and center_glob[numeroGlob] is not None:
    #                 esGerard = pica(pique3_pers[2][1], pique3_pers[1][1], pique3_pers[0][1])
    #                 #pica(pique3_pers[2][1], pique3_pers[1][1], pique3_pers[0][1])
    #                 count2_glob[numeroGlob] = 0
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

# Toma la cámara si no recibe video
if not args.get("video", False):
    vs = cv2.VideoCapture(0)

    # Toma video en caso de haber
else:
    vs = cv2.VideoCapture(args["video"])

# Puntos de esquinas Alcaraz vs Fucsovics: 366, 196, 608, 198, 78, 378, 724, 398
# Puntos de esquinas TennisBrothers: 311, 106, 456, 105, 89, 331, 628, 326
# Puntos de esquinas TennisBrothers 1080p: 749, 253, 1095, 252, 206, 797, 1518, 785
# Puntos de esquinas TheUltimateClutch Completo: 656, 429, 1044, 426, 0, 866, 1716, 802
# Puntos de esquinas TheUltimateClutch: 137, 355, 602, 348, 1, 889, 606, 866
# Puntos de esquinas TheUltimateClutch Hasta La Red: 1, 458, 606, 448, 1, 889, 606, 866
# Puntos de esquinas TennisBrothers 1080p Hasta La Red: 640, 365, 1180, 360, 206, 797, 1518, 785

# Rango de deteccion de verdes
greenLower = np.array([29, 86, 110])
greenUpper = np.array([64, 255, 255])
greenLower = np.array([29, 50, 110])

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

#topLeftX = 640
#topLeftY = 365
#topRightX = 1180
#topRightY = 360

pts_norm = deque(maxlen=args["buffer"])
pts_pers = deque(maxlen=args["buffer"])

preCentro_glob = deque(maxlen=2)
preCentro_glob.append(None)
preCentro_glob.append(None)

primeraVez_glob = deque(maxlen=2)
primeraVez_glob.append(True)
primeraVez_glob.append(True)

center_glob = deque(maxlen=2)
center_glob.append(None)
center_glob.append(None)

#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))  #ellipse kernel

# Fps del video
fps = int(vs.get(cv2.CAP_PROP_FPS))
print(fps)

time.sleep(2.0)

# Indica el tiempo que pasó desde que se detectó la última pelota
count_glob = deque(maxlen=2)
count_glob.append(0)
count_glob.append(0)

# Indica cuanto tiempo pasa entre tres centros consecutivos. 
# Esto para saber si detectó la pelota correctamente a la hora de determinar el pique
count2_glob = deque(maxlen=2)
count2_glob.append(0)
count2_glob.append(0)

# countSegundosTotales cuenta cuanto tiempo pasó en segundos desde que empezó el video 
countSegundosTotales = 0

ultimosCentros_norm = deque(maxlen=5)
ultimosCentros_pers = deque(maxlen=5)

todosContornos_norm = []
todosContornos_pers = []

contornosIgnorar_norm = []
contornosIgnorar_pers = []

pique_norm = deque(maxlen=4)
pique_pers = deque(maxlen=4)

pique2_norm = deque(maxlen=4)
pique2_pers = deque(maxlen=4)

pique3_norm = deque(maxlen=3)
pique3_pers = deque(maxlen=3)

# Se establece el resizer, sirve para agrandar la imagen y realizar un análisis más profundo, a cambio de más tiempo de procesamiento
# El primer valor corresponde al video original y el segundo a la perspectiva
resizer_glob = [3, 15]

altoOG = 0
anchoOG = 0

numeroGlob = 0
Gerard = None
esGerard = None
posiblePique = False
posiblesPiques_norm = deque()
posiblesPiques_pers = deque()

# CountDifVelocidad cuenta cuento tiempo en segundos pasa desde que se encontraron los dos puntos para usar en la velocidad
countDifVelocidad = 0

# CountDifPiques cuenta cuanto tiempo pasa desde que se encontró un pique hasta que se encuentra el siguiente
countDifPiques = 0

numeroFrame = 0

punto1Velocidad = None
velocidad = False
diferente = False
velocidadFinal = None
afterVelocidad = False

# abajo = False
# listaPrueba = []
# listaPrueba.append(((1, 5), 8))
# listaPrueba.append(abajo)
# print("Lista Prueba", listaPrueba)
# if type(listaPrueba[0]) is not bool and type(listaPrueba[0]) is not bool and type(listaPrueba[1]) is not bool and type(listaPrueba[1]) is not bool:
#     print("A")
# else: print("B", listaPrueba)


while True:
    numeroFrame += 1
    print("Numero de Frame: ", numeroFrame)

    countSegundosTotales += 1/fps

    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    if frame is None:
        break

    pts1 = np.float32([[topLeftX, topLeftY],       [topRightX, topRightY],
                         [bottomLeftX, bottomLeftY], [bottomRightX, bottomRightY]])
    pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (164, 474))

    numeroGlob = 0
    main(frame, numeroGlob)
    numeroGlob = 1
    main(result, numeroGlob)

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

cv2.destroyAllWindows()