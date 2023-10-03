# import math

# def cosine_similarity(tuple1, tuple2):
#     # Calcular el producto escalar entre las dos tuplas
#     dot_product = sum(x * y for x, y in zip(tuple1, tuple2))

#     # Calcular la magnitud de cada tupla
#     magnitude1 = math.sqrt(sum(x ** 2 for x in tuple1))
#     magnitude2 = math.sqrt(sum(x ** 2 for x in tuple2))

#     # Calcular la similitud del coseno
#     similarity = dot_product / (magnitude1 * magnitude2)

#     return similarity

# # Ejemplo de uso
# tuple_a = (159, 252, 255)
# tuple_b = (26, 41, 43)
# tuple_b = (170, 248, 255)

# similarity = cosine_similarity(tuple_a, tuple_b)
# print("Similitud del coseno entre las tuplas:", similarity)


# import numpy as np

# def distancia_bgr(color1, color2):
#     """
#     Calcula la distancia euclidiana entre dos colores BGR.
#     """
#     return np.sqrt(np.sum((color1 - color2) ** 2))

# # Valor de referencia BGR
# valor_referencia = np.array([159, 252, 255])
# print("Valor de referencia: ", valor_referencia)

# # Lista de valores BGR
# valores_lista = [(170, 248, 255), (92, 172, 255)]  # Agrega tus valores aquí

# print("Type valores lista", type(valores_lista))
# print("Type valores lista[0]", type(valores_lista[0]))

# # Calcula la distancia entre el valor de referencia y cada valor en la lista
# distancias = [distancia_bgr(valor_referencia, np.array(color)) for color in valores_lista]

# # Encuentra el índice del valor más cercano
# indice_mas_cercano = np.argmin(distancias)

# # El valor más cercano en la lista
# color_mas_cercano = valores_lista[indice_mas_cercano]

# print("color mas cercano: ", color_mas_cercano)
# print("distancia: ", distancias[1])
# #print(f"El color más cercano a ({a}, {b}, {c}) en la lista es ({color_mas_cercano[0]}, {color_mas_cercano[1]}, {color_mas_cercano[2]})")


import cv2
import numpy as np

lista = ((170, 190), (171, 190), (172, 190), (170, 191))

circle = cv2.minEnclosingCircle(np.array(lista))

print("circle: ", circle)
print((170, 190) in lista)

imagen_recortada_copia = cv2.imread("imagen_recortada312SinCirculos.png")
cv2.imwrite("prueba_imagen1.png", imagen_recortada_copia)

pixel = (201, 193)
color_mas_cercano = [166, 244, 255]
print("Color1", color_mas_cercano)

centro_lista = [(pixel)]
contador = 1

color_mas_cercano = imagen_recortada_copia[pixel[1], pixel[0]]
print("Color2", color_mas_cercano)

while contador > 0:
    contador = 0
    for pxl in centro_lista: 
        for i in range(-1, 2):
            for h in range(-1, 2):
                print("pxl: ", pxl[0] + i, pxl[1] + h)
                if (pxl[0] + i, pxl[1] + h) not in centro_lista:
                    color = imagen_recortada_copia[pxl[1] + h, pxl[0] + i]
                    print("Color", color)
                    distancia = abs(int(color[0]) - int(color_mas_cercano[0])) + abs(int(color[1]) - int(color_mas_cercano[1])) + abs(int(color[2]) - int(color_mas_cercano[2]))
                    if distancia <= 15: 
                        centro_lista.append((pxl[0] + i, pxl[1] + h))
                        contador += 1

print("centro_lista: ", centro_lista)
#cv2.circle(imagen_recortada_copia, (pixel[0], pixel[1]), 1, (0, 0, 255), 2)
circle = cv2.minEnclosingCircle(np.array(centro_lista))
print("circle: ", circle)
cv2.circle(imagen_recortada_copia, (int(circle[0][0]), int(circle[0][1])), int(circle[1]), (0, 0, 255), 2)

cv2.imshow("imagen_recortada_copia", imagen_recortada_copia)
cv2.imwrite("prueba_imagen2.png", imagen_recortada_copia)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()