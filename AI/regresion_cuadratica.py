import numpy as np

# Datos de posición de la pelota en coordenadas x e y a lo largo del tiempo
tiempo = [0, 1, 2, 3, 4]  # Tiempos
posicion_x = [2802, 2809, 2817, 2825, 2831]  # Posiciones en coordenada x correspondientes a los tiempos
posicion_y = [1428, 1319, 1214, 1117, 1028]  # Posiciones en coordenada y correspondientes a los tiempos

posicion_x = [2657, 2657, 2634, 2618, 2618]  # Posiciones en coordenada x correspondientes a los tiempos
posicion_y = [899, 899, 899, 900, 917]  # Posiciones en coordenada y correspondientes a los tiempos

# Ajustar una curva cuadrática a los datos de posición en coordenada x utilizando numpy.polyfit
coeficientes_x = np.polyfit(tiempo, posicion_x, 2)

# Ajustar una curva cuadrática a los datos de posición en coordenada y utilizando numpy.polyfit
coeficientes_y = np.polyfit(tiempo, posicion_y, 2)

# Coeficientes de la curva cuadrática para la coordenada x
a_x = coeficientes_x[0]
b_x = coeficientes_x[1]
c_x = coeficientes_x[2]

# Coeficientes de la curva cuadrática para la coordenada y
a_y = coeficientes_y[0]
b_y = coeficientes_y[1]
c_y = coeficientes_y[2]

# Calcular la posición estimada en nuevas coordenadas x e y para un nuevo tiempo
nuevo_tiempo = 5
posicion_estimada_x = a_x * nuevo_tiempo**2 + b_x * nuevo_tiempo + c_x
posicion_estimada_y = a_y * nuevo_tiempo**2 + b_y * nuevo_tiempo + c_y

# Debería tirar 2840,952
# Tira 2838, 944.6
print("Posición estimada (x, y):", (posicion_estimada_x, posicion_estimada_y))
