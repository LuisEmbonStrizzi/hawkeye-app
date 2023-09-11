import numpy as np
import cv2

vs = cv2.VideoCapture("../InkedInkedTennisBrothersVideo1080p.mp4")

fps = 30

output_path = 'video_zoom.mp4'
frame_width = int(vs.get(3))
frame_height = int(vs.get(4))
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
zooming = False

start_frame = 1380  # Cambia este valor al fotograma en el que deseas iniciar el zoom
zoom_duration = 100  # Cambia este valor a la duración de la animación de zoom en fotogramas

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
        frozen_frame = cv2.circle(frozen_frame, (1321, 587), 3, (0, 0, 255), -1)
    elif num_frame < start_frame + zoom_duration:
        zoom_factor = 1.0 + (num_frame - start_frame) / zoom_duration
        frame = cv2.resize(frozen_frame, (int(frame_width * zoom_factor), int(frame_height * zoom_factor)))
        dx = int((frame.shape[1] - frame_width) / 2)
        print("dx", dx)
        dy = int((frame.shape[0] - frame_height) / 2)
        print("dy", dy)
        print("frame", (frame.shape[1], frame.shape[0]))
        frame = frame[dy:dy+frame_height, dx:dx+frame_width]
        print("total", dy + frame_height - dy, "\n")
        out.write(frame)  # Escribe los fotogramas durante la animación de zoom
    else:
        break  # Sale del bucle después de la animación de zoom

vs.release()
out.release()
cv2.destroyAllWindows()