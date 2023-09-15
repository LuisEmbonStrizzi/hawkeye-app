import numpy as np
import matplotlib.pyplot as plt
import cv2
import imutils
from shapely.geometry import LineString

vs = cv2.VideoCapture("../InkedInkedTennisBrothersVideo1080p.mp4")

fps = 30

output_path = 'video_zoom2.mp4'
frame_width = int(vs.get(3))
frame_height = int(vs.get(4))
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
zooming = False
zoom_coords = (487, 599)

#Centro de la imagen: 960 x 540

start_frame = 272  # Cambia este valor al fotograma en el que deseas iniciar el zoom
zoom_duration = 50  # Cambia este valor a la duración de la animación de zoom en fotogramas

#lineal = funcion_lineal(frame_width / 2, frame_height / 2, zoom_coords[0], zoom_coords[1])

mascara = np.zeros((1080, 1920, 3), dtype=np.uint8)

if zoom_coords[0] < frame_width * 1/4 or zoom_coords[0] > frame_width * 3/4 or zoom_coords[1] < frame_height * 1/4 or zoom_coords[1] > frame_height * 3/4:
    lineaPrincipal = ((frame_width / 2, frame_height / 2), (zoom_coords))
    lineas = [
    ((frame_width * 1/4, frame_height * 1/4), (frame_width * 3/4, frame_height * 1/4)), 
    ((frame_width * 1/4, frame_height * 1/4), (frame_width * 1/4, frame_height * 3/4)),
    ((frame_width * 3/4, frame_height * 1/4), (frame_width * 3/4, frame_height * 3/4)),
    ((frame_width * 1/4, frame_height * 3/4), (frame_width * 3/4, frame_height * 3/4))]

    cv2.line(mascara, (int(lineaPrincipal[0][0]), int(lineaPrincipal[0][1])), (int(lineaPrincipal[1][0]), int(lineaPrincipal[1][1])), (255, 255, 255), 4)

    for i in lineas:
        cv2.line(mascara, (int(i[0][0]), int(i[0][1])), (int(i[1][0]), int(i[1][1])), (255, 255, 255), 4)
        (x1, y1), (x2, y2) = lineaPrincipal
        (x3, y3), (x4, y4) = i
        i = np.array(i, dtype=np.float32)
        lineaPrincipal = np.array(lineaPrincipal, dtype=np.float32)

        #denominador = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        #if denominador != 0:
        #    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominador
        #    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominador
        #    print(f'El punto de intersección es: ({px}, {py})')
        #else:
        #    print('Las líneas son paralelas y no tienen intersección.')

        #resultado = cv2.intersectLines(lineaPrincipal[0], lineaPrincipal[1], i[0], i[1])

        #if resultado[0] == 0:
        #    print("Los segmentos de línea son paralelos y no se cruzan.")
        #else:
            # Calcular el punto de intersección
        #    punto_interseccion = (int(resultado[2]), int(resultado[3]))

        # Crear objetos LineString a partir de los segmentos
        linea1 = LineString(i)
        linea2 = LineString(lineaPrincipal)

        # Verificar si las líneas se intersectan
        if linea1.intersects(linea2):
            # Si se intersectan, encontrar el punto de intersección
            punto_interseccion = linea1.intersection(linea2)
            if punto_interseccion.geom_type == 'Point':
                x, y = punto_interseccion.coords[0]
                print(f"Los segmentos de línea se cruzan en el punto ({x}, {y})")
            else:
                print("Las líneas se superponen pero no se cruzan en un punto único.")
        else:
            print("Los segmentos de línea no se cruzan.")

    
    dif_x = x - frame_width / 2
    dif_y = y - frame_height / 2

    un_zoom_x = dif_x / zoom_duration
    un_zoom_y = dif_y / zoom_duration

else:
    dif_x = zoom_coords[0] - frame_width / 2
    dif_y = zoom_coords[1] - frame_height / 2

    un_zoom_x = dif_x / zoom_duration
    un_zoom_y = dif_y / zoom_duration

todos_puntos = []
todos_puntos_con_proporcion = []

for i in range(zoom_duration):
    #todos_puntos.append((un_zoom_x + frame_width[0], funcion_lineal2(lineal[0], lineal[1], un_zoom_x + frame_width[0])))
    todos_puntos.append((un_zoom_x + frame_width / 2, un_zoom_y + frame_height / 2))
    todos_puntos_con_proporcion.append(((un_zoom_x + frame_width / 2) * (i / zoom_duration + 1), (un_zoom_y + frame_height / 2) * (i / zoom_duration + 1)))
    un_zoom_x += dif_x / zoom_duration
    un_zoom_y += dif_y / zoom_duration

num_frame = 0
contador = 0
while True:
    num_frame += 1

    frame = vs.read()[1]

    if frame is None:
        break

    if num_frame < start_frame:
        out.write(frame)
    elif num_frame == start_frame:
        # Congela el último fotograma antes del inicio del zoom
        frozen_frame = frame.copy()
    elif num_frame < start_frame + zoom_duration:
        zoom_factor = 1.0 + (num_frame - start_frame) / zoom_duration
        
        frame_zoomed = cv2.resize(frozen_frame, (int(frame_width * zoom_factor), int(frame_height * zoom_factor)))
        
        y1 = int(todos_puntos_con_proporcion[contador][1] - 540)
        y2 = int(todos_puntos_con_proporcion[contador][1] + 540)
        x1 = int(todos_puntos_con_proporcion[contador][0] - 960)
        x2 = int(todos_puntos_con_proporcion[contador][0] + 960)

        frame_zoomed_2 = frame_zoomed[y1:y2,x1:x2]

        contador += 1
        out.write(frame_zoomed_2)  # Escribe los fotogramas durante la animación de zoom
    else:
        break  # Sale del bucle después de la animación de zoom

print("Todos Puntos", todos_puntos)
print("Todos Puntos Con Proporción", todos_puntos_con_proporcion)

while True:
    # Mostrar la máscara
    mascara = imutils.resize(mascara, height= 600)
    cv2.imshow("Mascara", mascara)

    # Esperar a que se presione una tecla
    key = cv2.waitKey(1) & 0xFF

    # Si se presiona la tecla 'q', salir del bucle
    if key == ord("q"):
        break

vs.release()
out.release()
cv2.destroyAllWindows()