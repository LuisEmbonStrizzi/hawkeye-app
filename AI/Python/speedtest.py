import cv2
import time
import imutils
import numpy as np
import ctypes

#### CTYPES ####
cpplibrary = ctypes.CDLL("cpplibrary.so", winmode=0)

resultado = cpplibrary.suma(1, 2)
print(f"corrí en C++: {resultado}")

resizer = 3
greenLower = np.array([29, 50, 110])
greenUpper = np.array([64, 255, 255])

if __name__ == '__main__':
    video = cv2.VideoCapture("E:\Guido\Documentos\Programacion\Hawkeye-2022\Videos Tenis para Analizar\InkedInkedTennisBrothersVideo1080p.mp4")

    

    frame_actual = 0
    while True:
        frame_actual += 1

        gpu_frame = cv2.cuda_GpuMat()
        gpu_frame.upload(frame)

        ### BLOQUE 1 ###
        start_time = time.time()
        frame = video.read()[1]
        print("BLOQUE 1:", time.time() - start_time, "frame: ", frame_actual)
        ### BLOQUE 1 ###

        if frame is None: 
            break

        ### BLOQUE 2 ###
        start_time = time.time()
        anchoOG = frame.shape[1]
        altoOG = frame.shape[0]

        frame = imutils.resize(frame, anchoOG * resizer, altoOG * resizer)

        print("BLOQUE 2:", time.time() - start_time, "frame: ", frame_actual)
        ### BLOQUE 2 ###

        ### BLOQUE 3 ###
        start_time = time.time()
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        print("BLOQUE 3:", time.time() - start_time, "frame: ", frame_actual)
        ### BLOQUE 3 ###

        ### BLOQUE 4 ###
        start_time = time.time()
        # Filtra los tonos verdes de la imagen
        mascara = cv2.inRange(hsv, greenLower, greenUpper)
        mascara = cv2.erode(mascara, None, iterations=2)
        mascara = cv2.dilate(mascara, None, iterations=2)
        print("BLOQUE 4:", time.time() - start_time, "frame: ", frame_actual)
        ### BLOQUE 4 ###
        
        ### BLOQUE 5 ###
        # Toma todos los contornos de la imagen
        start_time = time.time()
        contornos = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos = imutils.grab_contours(contornos)
        print("BLOQUE 5:", time.time() - start_time, "frame: ", frame_actual, "\n--------------------")
        ### BLOQUE 5 ###