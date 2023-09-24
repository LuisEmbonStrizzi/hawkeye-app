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


import numpy as np

def distancia_bgr(color1, color2):
    """
    Calcula la distancia euclidiana entre dos colores BGR.
    """
    return np.sqrt(np.sum((color1 - color2) ** 2))

# Valor de referencia BGR
valor_referencia = np.array([159, 252, 255])
print("Valor de referencia: ", valor_referencia)

# Lista de valores BGR
valores_lista = [(170, 248, 255), (92, 172, 255)]  # Agrega tus valores aquí

print("Type valores lista", type(valores_lista))
print("Type valores lista[0]", type(valores_lista[0]))

# Calcula la distancia entre el valor de referencia y cada valor en la lista
distancias = [distancia_bgr(valor_referencia, np.array(color)) for color in valores_lista]

# Encuentra el índice del valor más cercano
indice_mas_cercano = np.argmin(distancias)

# El valor más cercano en la lista
color_mas_cercano = valores_lista[indice_mas_cercano]

print("color mas cercano: ", color_mas_cercano)
print("distancia: ", distancias[1])
#print(f"El color más cercano a ({a}, {b}, {c}) en la lista es ({color_mas_cercano[0]}, {color_mas_cercano[1]}, {color_mas_cercano[2]})")
