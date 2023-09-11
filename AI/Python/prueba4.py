import numpy as np
import matplotlib.pyplot as plt
import cv2

vs = cv2.VideoCapture("../InkedInkedTennisBrothersVideo1080p.mp4")

fps = 30

output_path = 'video_zoom.mp4'
frame_width = int(vs.get(3))
frame_height = int(vs.get(4))
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
zooming = False
zoom_coords = (487, 599)

#Centro de la imagen: 960 x 540

start_frame = 272  # Cambia este valor al fotograma en el que deseas iniciar el zoom
zoom_duration = 50  # Cambia este valor a la duración de la animación de zoom en fotogramas

#lineal = funcion_lineal(frame_width / 2, frame_height / 2, zoom_coords[0], zoom_coords[1])

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

vs.release()
out.release()
cv2.destroyAllWindows()