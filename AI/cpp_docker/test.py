import ctypes

ruta_archivo_so = "/app/main.so"
lib = ctypes.CDLL(ruta_archivo_so)

resultado = lib.suma(1, 2)
print(resultado)
