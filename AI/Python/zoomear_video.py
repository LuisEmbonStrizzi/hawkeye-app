import cv2


def zoomear_video(url_video: str, pique: list[(int, int), int]):
    vs = cv2.VideoCapture(url_video)

    fps = int(vs.get(cv2.CAP_PROP_FPS))

    output_path = 'video_zoom.mp4'
    frame_width = int(vs.get(3))
    frame_height = int(vs.get(4))
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(
        *'avc1'), fps, (frame_width, frame_height))  # Con el códec XVID y ciertos valores tira error

    zoom_coords = pique[0]
    if zoom_coords is None:
        return
    start_frame = pique[1]  # Frame del pique
    zoom_duration = 50  # Duración en frames del zoom
    video_duration = 7  # Cuantos segundos de video antes del pique se guardan

    unidad_x = (zoom_coords[0] - frame_width / 2) / zoom_duration
    unidad_y = (zoom_coords[1] - frame_height / 2) / zoom_duration

    num_frame = 0
    while True:
        num_frame += 1

        if num_frame < start_frame:
            frame = vs.read()[1]
            if num_frame > start_frame - video_duration * fps:
                out.write(frame)

        elif num_frame == start_frame:
            # Congela el último fotograma antes del inicio del zoom
            frame = vs.read()[1]
            frozen_frame = frame.copy()

        elif num_frame <= start_frame + zoom_duration:
            zoom_factor = 1.0 + (num_frame - start_frame) / zoom_duration

            frame_zoomed = cv2.resize(frozen_frame, (int(
                frame_width * zoom_factor), int(frame_height * zoom_factor)))

            # Calcula el desplazamiento para centrar el zoom en el punto específico
            dx = int(unidad_x * (num_frame - start_frame) *
                     zoom_factor + (frame_zoomed.shape[1] - frame_width) / 2)
            dy = int(unidad_y * (num_frame - start_frame) *
                     zoom_factor + (frame_zoomed.shape[0] - frame_height) / 2)

            dx = max(0, min(dx, frame_zoomed.shape[1] - frame_width))
            dy = max(0, min(dy, frame_zoomed.shape[0] - frame_height))

            # if dx < 0:
            #     dx = 0

            # elif dx + frame_width > frame_zoomed.shape[1]:
            #     dx -= dx + frame_width - frame_zoomed.shape[1]

            # if dy < 0:
            #     dy = 0

            # elif dy + frame_height > frame_zoomed.shape[0]:
            #     dy -= dy + frame_height - frame_zoomed.shape[0]

            # Aplica el recorte para centrar el zoom en el punto específico
            frame_zoomed = frame_zoomed[dy:dy +
                                        frame_height, dx:dx + frame_width]

            out.write(frame_zoomed)
        else:
            break

        if frame is None:
            break

    vs.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    zoomear_video(
        r"C:\Users\47205114\Documents\hawkeye-app\gopro_api\official_sdk\GH010130.mp4", [(1321, 587), 150])
