import cv2
import time
import imutils
import numpy as np
import ctypes

resizer = 3
greenLower = np.array([29, 50, 110])
greenUpper = np.array([64, 255, 255])

def soFile():
    #### CTYPES ####
    cpplibrary = ctypes.CDLL("./cpplibrary.so", winmode=0)

    #resultado = cpplibrary.suma(1, 2)
    #print(f"corrí en C++: {resultado}")

    resizer = 3
    greenLower = np.array([29, 50, 110])
    greenUpper = np.array([64, 255, 255])

    vs = cv2.VideoCapture("./InkedInkedTennisBrothersVideo1080p.mp4")
    frame_count = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_actual = 1
    for _ in range(frame_count):
        frame = vs.read()[1]

        start_time = time.time()
            
        # Convierte la imagen a un array de NumPy
        imagen_array = np.asarray(frame)

        # Obtiene un puntero al array NumPy
        imagen_ptr = imagen_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

        # Establece los tipos de argumento y retorno de la función
        cpplibrary.procesar_frame.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.c_int, ctypes.c_int]
        cpplibrary.procesar_frame.restype = ctypes.POINTER(ctypes.c_ubyte)

        # Llama a la función en C++ y guarda el puntero de la máscara
        mask_ptr = cpplibrary.procesar_frame(imagen_ptr, frame.shape[0], frame.shape[1], frame.shape[2])

        # Crea una matriz NumPy a partir del puntero de la máscara
        imagen_np = np.ctypeslib.as_array(mask_ptr, shape=(frame.shape[0] * resizer, frame.shape[1] * resizer, 1)) # Nota: tiene un solo canal ya que es en escala de grises

        # Busca los contornos en la imagen
        contornos = cv2.findContours(imagen_np, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Accede al resultado a través del puntero
        print("Tiempo:", time.time() - start_time, "frame: ", frame_actual)
        #print("Contornos:", contornos)

        # Libera la memoria
        ctypes.CDLL('libc.so.6').free(mask_ptr)

        frame_actual += 1

    #return contornos

#if __name__ == '__main__':
#    soFile()


"""
if __name__ == '__main__':
    video = cv2.VideoCapture("E:\Guido\Documentos\Programacion\Hawkeye-2022\Videos Tenis para Analizar\InkedInkedTennisBrothersVideo1080p.mp4")

    
    frame_actual = 0
    while True:
        frame_actual += 1

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
"""