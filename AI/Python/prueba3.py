import numpy as np
import matplotlib.pyplot as plt
import cv2

def funcion_lineal(x1, y1, x2, y2):
    # Calcula la pendiente m
    m = (y2 - y1) / (x2 - x1)
    
    # Calcula la ordenada al origen b
    b = y1 - m * x1

    # Genera un rango de valores x para la gráfica
    x = np.linspace(min(x1, x2) - 1, max(x1, x2) + 1, 100)
    
    # Calcula los valores correspondientes de y utilizando la función lineal
    y = m * x + b
    
    # Dibuja la gráfica de la función lineal
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'y = {m}x + {b}', color='blue')
    plt.scatter([x1, x2], [y1, y2], color='red', label='Puntos (x1, y1) y (x2, y2)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Función Lineal')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return m, b

def funcion_lineal2(m, b, x):
    return m * x + b

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
zoom_duration = 100  # Cambia este valor a la duración de la animación de zoom en fotogramas

#lineal = funcion_lineal(frame_width / 2, frame_height / 2, zoom_coords[0], zoom_coords[1])

dif_x = frame_width / 2 - zoom_coords[0]
dif_y = frame_height / 2 - zoom_coords[1]

un_zoom_x = dif_x / zoom_duration
un_zoom_y = dif_y / zoom_duration

todos_puntos = []
todos_puntos_con_proporcion = []

for i in range(zoom_duration):
    #todos_puntos.append((un_zoom_x + frame_width[0], funcion_lineal2(lineal[0], lineal[1], un_zoom_x + frame_width[0])))
    todos_puntos.append((un_zoom_x + zoom_coords[0], un_zoom_y + zoom_coords[1]))
    todos_puntos_con_proporcion.append(((un_zoom_x + zoom_coords[0]) * (i / 100 + 1), (un_zoom_y + zoom_coords[1]) * (i / 100 + 1)))
    un_zoom_x += dif_x / zoom_duration
    un_zoom_y += dif_y / zoom_duration

unidad_x = (zoom_coords[0] - frame_width / 2) / zoom_duration
unidad_y = (zoom_coords[1] - frame_height / 2) / zoom_duration

num_frame = 0
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
        print("zoom factor", zoom_factor)
        
        frame_zoomed = cv2.resize(frozen_frame, (int(frame_width * zoom_factor), int(frame_height * zoom_factor)))
        zoom_coords_zoomed = (zoom_coords[0] * zoom_factor, zoom_coords[1] * zoom_factor)
        
        # Calcula el desplazamiento para centrar el zoom en el punto específico
        dx = int(unidad_x * (num_frame - start_frame) * zoom_factor + (frame_zoomed.shape[1] - frame_width) / 2)
        dy = int(unidad_y * (num_frame - start_frame) * zoom_factor + (frame_zoomed.shape[0] - frame_height) / 2)
        
        print("dx", dx)
        #dy = int((zoom_coords_zoomed[1] - zoom_coords[1]) / 2)
        print("dy", dy)
        print("frame", (frame_zoomed.shape[1], frame_zoomed.shape[0]))

        if dx < 0:
            dx = 0

        elif dx + frame_width > frame_zoomed.shape[1]:
            dx -= dx + frame_width - frame_zoomed.shape[1]
        
        if dy < 0:
            dy = 0

        elif dy + frame_height > frame_zoomed.shape[0]:
            dy -= dy + frame_height - frame_zoomed.shape[0]

        # Aplica el recorte para centrar el zoom en el punto específico
        frame_zoomed = frame_zoomed[dy:dy+frame_height, dx:dx+frame_width]
        print("total", dy+frame_height - dy, "\n")
        out.write(frame_zoomed)  # Escribe los fotogramas durante la animación de zoom
    else:
        break  # Sale del bucle después de la animación de zoom

print("Todos Puntos", todos_puntos)
print("Todos Puntos Con Proporción", todos_puntos_con_proporcion)

vs.release()
out.release()
cv2.destroyAllWindows()