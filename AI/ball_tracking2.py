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

    # Agrandamos el frame para ver más la pelota
    frame = imutils.resize(frame, anchoOG * resizer, altoOG * resizer)

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

    # Encontrar los contornos en la máscara
    contornos, _ = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar los contornos en la imagen original
    cv2.drawContours(frame, contornos, -1, (0, 255, 0), 2)
    
    centro = None
    
    # Cada 5 segundos elimina los contornos que no son tan frecuentes, es decir, los contornos parecidos que no aparecen tanto a lo largo del video
    if (TiempoSegundosEmpezoVideo % 5 == 0):
        eliminarContornosInservibles(todosContornos)
    
    if len(contornos) > 0:
        # Vemos cuales son los contornos casi inmóviles y si lo que considera que es la pelota no se está moviendo (o sea no es la pelota) se ignoran estos contornos.
        contornosQuietos(contornos, todosContornos, contornosIgnorar)
        if len(ultimosCentros) == 5 and seEstaMoviendo(ultimosCentros) == False:
            contornos = ignorarContornosQuietos(contornos, contornosIgnorar)

        if len(contornos) > 0:
            # Cuando empezó el video o pasaron 0.3 segundos desde que no se encuentra la pelota
            if primeraVez:
                # Busca el contorno más grande y encuentra su posición (x, y). Determina el centro de la pelota
                casiCentro = max(contornos, key=cv2.contourArea)
                ((x, y), radio) = cv2.minEnclosingCircle(casiCentro)
                M = cv2.moments(casiCentro)
                if M["m00"] > 0: centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), int(radio)
                primeraVez = False
                preCentro = centro
                TiempoDeteccionUltimaPelota = 0
                TiempoTresCentrosConsecutivos = 0

                if centro is not None: ultimosCentros.appendleft(centro)
            
            # Si se detectó un centro hace menos de 0.3 segundos
            else:
                # Corre la función tp_fix para determinar cual es el contorno detectado que está mas cerca de la pelota del frame anterior, es decir, encuentra la peltoa a través de su posición en el frame anterior
                if preCentro is not None: casiCentro = tp_fix(contornos, preCentro, TiempoDeteccionUltimaPelota)
                
                # Encuentra la posición x, y del contorno más cercano a la pelota del frame anterior. Determina el centro de la pelota
                if casiCentro is not None:
                    ((x, y), radio) = cv2.minEnclosingCircle(casiCentro)
                    M = cv2.moments(casiCentro)
                    if M["m00"] > 0: centro = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])], int(radio)
                    preCentro = centro
                    TiempoTresCentrosConsecutivos += TiempoDeteccionUltimaPelota
                    TiempoDeteccionUltimaPelota = 0
                    if centro is not None: ultimosCentros.appendleft(centro)
                
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
                cv2.circle(frame, (centro[0][0], centro[0][1]), 5, (0, 0, 255), -1)
    
    # Si no se encuentra la pelota, se cambian algunas variables para poder determinar mejor su posición en los siguientes frame
    else:
        if TiempoDeteccionUltimaPelota >= 0.3:
            primeraVez = True
            preCentro = None
        TiempoDeteccionUltimaPelota += 1/fps
        TiempoTresCentrosConsecutivos = 0
    
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
    
    # Resizea el frame al tamaño original y lo muestra
    frame = imutils.resize(frame, anchoOG, altoOG)
    frame = imutils.resize(frame, height= 768)
    mascara = imutils.resize(mascara, anchoOG, altoOG)
    mascara = imutils.resize(mascara, height= 768)
    
    # También muestra la máscara
    cv2.imshow("Mascara Normal", mascara)
    cv2.imshow("Normal", frame)

# Función que recibe el centro de la pelota y pasa sus coordenadas a un plano 2D de la cancha de tenis
def coordenadaPorMatriz(centro):
    # Adapto la variable centro para que sea siempre de esta forma ((x, y), r)
    if type(centro) is list:
        centro = (centro, 0)
    pts1 = np.float32([[topLeftX, topLeftY],[topRightX, topRightY],[bottomLeftX, bottomLeftY],[bottomRightX, bottomRightY]])
    pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

    # Pasamos las esquinas a perspectiva
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    perspectiva = cv2.warpPerspective(frame, matrix, (164, 474))

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
def seEstaMoviendo(ultCentros):
    movimiento = False
    # Si la suma de las restas de los últimos centros es mayor a 15, significa que la pelota se está moviendo, de lo contrario no lo está.
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
    
    # Devuelve True o False dependiendo de si la pelota se mueve o no
    if movimiento: 
        return True
    return False

# Función que arregla el problema de "la zapatilla verde"
def tp_fix(contornos, pre_centro, count):
    cnts_pts = []
    medidorX = 100
    medidorY = 103
    
    for contorno in contornos:
        ((x, y), _) = cv2.minEnclosingCircle(contorno)
        # cnts_pts tiene aquellos contornos del frame actual que están cerca del pre_centro en las coordenadas x,y. 
        if x - pre_centro[0][0] > medidorX * resizer or pre_centro[0][0] - x > medidorX * resizer or y - pre_centro[0][1] > medidorY * resizer or pre_centro[0][1] - y > medidorY * resizer and count <= 0.5:
            continue
        cnts_pts.append(contorno)
    if cnts_pts != []:
        # Devuelve la función cualEstaMasCerca con los parametros obtenidos en la función
        return cualEstaMasCerca(pre_centro, cnts_pts)

# Define qué candidato a pelota es el punto más cercano al anterior. Toma los puntos de tp_fix y analiza cual está mas cerca al pre_centro (centro anterior).
def cualEstaMasCerca(punto, lista):
    suma = []
    suma2 = []
    for i in lista:
        # Obtenemos las diferencias entre el preCentro y el círculo a comparar que proviene del contorno.
        (xCenter, yCenter), radius = cv2.minEnclosingCircle(i)
        difEnX = abs(int(xCenter) - int(punto[0][0]))
        difEnY = abs(int(yCenter) - int(punto[0][1]))
        difRadio = abs(int(radius) - int(punto[1]))
        
        # Guardamos los valores en listas
        suma.append(difEnX + difEnY + difRadio * 3)
        suma2.append(i)
    # Devolvemos el valor más chico que represeta el círculo a menor distancia del preCentro
    return suma2[suma.index(min(suma))]

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

# Toma la cámara si no recibe video
if not args.get("video", False):
    vs = cv2.VideoCapture(0)

    # Toma video en caso de haber
else:
    vs = cv2.VideoCapture(args["video"])

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

# El número del Frame del video
numeroFrame = 0

punto1Velocidad = None
velocidad = False
diferente = False
velocidadFinal = None
afterVelocidad = False

pelotaEstaEnPerspectiva = None

casiCentro = None

start_time = time.time()
previous_time = start_time

# Se corre el for la cantidad de frames que contiene el video
for _ in range(frame_count):
    numeroFrame += 1
    print("Numero de Frame: ", numeroFrame)

    TiempoSegundosEmpezoVideo += 1/fps

    # Toma el frame del video
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    if numeroFrame == 1:
        # Ancho y alto de la imagen
        anchoOG = frame.shape[1]
        altoOG = frame.shape[0]
        
        ############ VER DE BORRAR ESTO
        estaCercaX = anchoOG * 10/100
        estaCercaY = altoOG * 10/100
        #################

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
        cv2.imwrite('zoomed_image.jpg', zoomed_area)
        #break

    main(frame)

    print("pts_piques", pts_piques_finales)
    print("pts_golpes", pts_golpes_finales)

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