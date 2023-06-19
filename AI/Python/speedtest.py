import cv2
import time
#import imutils
import numpy as np
import ctypes


def soFile():
    #### CTYPES ####
    cpplibrary = ctypes.CDLL("./cpplibrary.so", winmode=0)

    #resultado = cpplibrary.suma(1, 2)
    #print(f"corrí en C++: {resultado}")

    resizer = 3
    greenLower = np.array([29, 50, 110])
    greenUpper = np.array([64, 255, 255])

    imagen = np.zeros((1000, 1000, 3), np.uint8)
    imagen = cv2.putText(imagen, "Luis panza", (50, 50),
                         cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 255, 0))
    cv2.imwrite('imagen.jpg', imagen)

    # Convierte la imagen a un array de NumPy
    imagen_array = np.asarray(imagen)

    # Obtiene un puntero al array NumPy
    imagen_ptr = ctypes.c_void_p(imagen_array.ctypes.data)

    # Crea una variable en Python para almacenar el retorno de la función en C++
    result = ctypes.c_int()

    # Llama a la función en C++
    cpplibrary.abrir_img(
        imagen_ptr, imagen.shape[0], imagen.shape[1], imagen.shape[2], ctypes.byref(result))

    # Accede al resultado a través del puntero
    result_value = result.value
    print("Resultado:", result_value)
    return result_value
