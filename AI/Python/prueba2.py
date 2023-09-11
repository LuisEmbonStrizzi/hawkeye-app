import numpy as np
import cv2

vs = cv2.VideoCapture("../InkedInkedTennisBrothersVideo1080p.mp4")

fps = 30

output_path = 'video_zoom.mp4'
frame_width = int(vs.get(3))
frame_height = int(vs.get(4))
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
zooming = False
zoom_coords = (1900, 1080) # Si y es mayor a 812 tira error (?????) 1732

start_frame = 100  # Cambia este valor al fotograma en el que deseas iniciar el zoom
zoom_duration = 50  # Cambia este valor a la duración de la animación de zoom en fotogramas

unidad_x = (zoom_coords[0] - frame_width / 2) / zoom_duration
unidad_y = (zoom_coords[1] - frame_height / 2) / zoom_duration

num_frame = 0
while True:
    num_frame += 1

    frame = vs.read()[1]

    try:
        if frame is None:
            break

    
        if num_frame < start_frame:
            out.write(frame)
        elif num_frame == start_frame:
            # Congela el último fotograma antes del inicio del zoom
            frozen_frame = frame.copy()
        elif num_frame < start_frame + zoom_duration:
            print("HOLA")
            zoom_factor = 1.0 + (num_frame - start_frame) / zoom_duration
            print("zoom factor", zoom_factor)
            
            frame_zoomed = cv2.resize(frozen_frame, (int(frame_width * zoom_factor), int(frame_height * zoom_factor)))
            zoom_coords_zoomed = (zoom_coords[0] * zoom_factor, zoom_coords[1] * zoom_factor)
            
            # Calcula el desplazamiento para centrar el zoom en el punto específico
            dx = int(unidad_x * (num_frame - start_frame) * zoom_factor + (frame_zoomed.shape[1] - frame_width) / 2)
            dy = int(unidad_y * (num_frame - start_frame) * zoom_factor + (frame_zoomed.shape[0] - frame_height) / 2)

            dx = max(0, min(dx, frame_zoomed.shape[1] - frame_width))
            dy = max(0, min(dy, frame_zoomed.shape[0] - frame_height))
            
            ###print("dx", dx)
            #dy = int((zoom_coords_zoomed[1] - zoom_coords[1]) / 2)
            ###print("dy", dy)
            print("frame", (frame_zoomed.shape[1], frame_zoomed.shape[0]))

            if dx < 0:
                print("ENTRE EN EL PRIMERO")
                dx = 0

            elif dx + frame_width > frame_zoomed.shape[1]:
                print("ENTRE EN EL SEGUNDO")
                dx -= dx + frame_width - frame_zoomed.shape[1]
            
            if dy < 0:
                print("ENTRE EN EL TERCERO")
                dy = 0

            elif dy + frame_height > frame_zoomed.shape[0]:
                print("ENTRE EN EL CUARTO")
                dy -= dy + frame_height - frame_zoomed.shape[0]

            print("dx", dx)
            print("dy", dy)

            # Aplica el recorte para centrar el zoom en el punto específico
            frame_zoomed = frame_zoomed[dy:dy+frame_height, dx:dx+frame_width]
            print("DY + altura", dy+frame_height)
            print("total", (frame_zoomed.shape[1], frame_zoomed.shape[0]), "\n")
            out.write(frame_zoomed)  # Escribe los fotogramas durante la animación de zoom
            print("GUARDE")
        else:
            break  # Sale del bucle después de la animación de zoom

    except cv2.error as e:
        print("Error de OpenCV:", e)
        break

vs.release()
out.release()
cv2.destroyAllWindows()