import cv2
import numpy as np
import ctypes

def analizarFrame (frame):
    cpplibrary = ctypes.CDLL("./cpplibrary.so", winmode=0)
    
    resizer = 3

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

    # Libera la memoria
    ctypes.CDLL('libc.so.6').free(mask_ptr)

    return contornos