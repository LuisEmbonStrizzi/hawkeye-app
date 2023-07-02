# import numpy as np

# # Datos de posición de la pelota en coordenadas x e y a lo largo del tiempo
# tiempo = [0, 1, 2, 3, 4]  # Tiempos
# posicion_x = [2802, 2809, 2817, 2825, 2831]  # Posiciones en coordenada x correspondientes a los tiempos
# posicion_y = [1428, 1319, 1214, 1117, 1028]  # Posiciones en coordenada y correspondientes a los tiempos

# posicion_x = [2657, 2657, 2634, 2618, 2618]  # Posiciones en coordenada x correspondientes a los tiempos
# posicion_y = [899, 899, 899, 900, 917]  # Posiciones en coordenada y correspondientes a los tiempos

# # Ajustar una curva cuadrática a los datos de posición en coordenada x utilizando numpy.polyfit
# coeficientes_x = np.polyfit(tiempo, posicion_x, 2)

# # Ajustar una curva cuadrática a los datos de posición en coordenada y utilizando numpy.polyfit
# coeficientes_y = np.polyfit(tiempo, posicion_y, 2)

# # Coeficientes de la curva cuadrática para la coordenada x
# a_x = coeficientes_x[0]
# b_x = coeficientes_x[1]
# c_x = coeficientes_x[2]

# # Coeficientes de la curva cuadrática para la coordenada y
# a_y = coeficientes_y[0]
# b_y = coeficientes_y[1]
# c_y = coeficientes_y[2]

# # Calcular la posición estimada en nuevas coordenadas x e y para un nuevo tiempo
# nuevo_tiempo = 5
# posicion_estimada_x = a_x * nuevo_tiempo**2 + b_x * nuevo_tiempo + c_x
# posicion_estimada_y = a_y * nuevo_tiempo**2 + b_y * nuevo_tiempo + c_y

# # Debería tirar 2840,952
# # Tira 2838, 944.6
# print("Posición estimada (x, y):", (posicion_estimada_x, posicion_estimada_y))

# import numpy as np
# from scipy.optimize import curve_fit

# data_points = np.array([[1, 2730, 928], [2, 2690, 906], [3, 2656, 899], [4, 2656, 899], [5, 2633, 899], [6, 2616, 898], [7, 2605, 905]])
# x_data = data_points[:, 0]
# y_data = data_points[:, 1:]

# def quadratic_func(x, a, b, c):
#     return a * x**2 + b * x + c

# params_x, _ = curve_fit(quadratic_func, x_data, y_data[:, 0])  # Coordenada X
# params_y, _ = curve_fit(quadratic_func, x_data, y_data[:, 1])  # Coordenada Y

# # Coeficientes de la regresión cuadrática para X y Y
# a_x, b_x, c_x = params_x
# a_y, b_y, c_y = params_y

# # Predecir las siguientes posiciones de la pelota en los frames 8 y 9
# frame_8 = 8
# frame_9 = 9

# pos_x_frame_8 = quadratic_func(frame_8, a_x, b_x, c_x)
# pos_y_frame_8 = quadratic_func(frame_8, a_y, b_y, c_y)

# pos_x_frame_9 = quadratic_func(frame_9, a_x, b_x, c_x)
# pos_y_frame_9 = quadratic_func(frame_9, a_y, b_y, c_y)

# print("Posición de la pelota en el frame 8:")
# print("X:", pos_x_frame_8)
# print("Y:", pos_y_frame_8)

# print("Posición de la pelota en el frame 9:")
# print("X:", pos_x_frame_9)
# print("Y:", pos_y_frame_9)

# import numpy as np
# import matplotlib.pyplot as plt

# # Datos de los centros de la pelota en cada frame
# x = [2901, 2800, 2730, 2690, 2656, 2656, 2633, 2616, 2605, 2605]
# y = [1007, 956, 928, 906, 899, 899, 899, 898, 905, 887]

# # Ajuste de la regresión cuadrática
# coefficients = np.polyfit(x, y, 2)
# a, b, c = coefficients

# # Generar puntos de la curva ajustada
# x_fit = np.linspace(min(x), max(x), 100)
# y_fit = a * x_fit**2 + b * x_fit + c

# # Obtener el punto resultante de la regresión cuadrática
# x_result = x_fit[-1]
# y_result = y_fit[-1]
# result_point = (x_result, y_result)

# # Imprimir el punto resultante
# print("El punto resultante de la regresión cuadrática es:", result_point)

# # Graficar los puntos y la curva ajustada
# plt.scatter(x, y, label='Datos')
# plt.plot(x_fit, y_fit, color='red', label='Regresión Cuadrática')
# plt.xlabel('Coordenada X')
# plt.ylabel('Coordenada Y')
# plt.legend()
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt

# # Puntos conocidos
# x_data = np.array([2901, 2800, 2730, 2690, 2656, 2656, 2633, 2616, 2605, 2605])
# y_data = np.array([1007, 956, 928, 906, 899, 899, 899, 898, 905, 887])

# # Función de regresión cuadrática
# def quadratic_func(x, a, b, c):
#     return a * x**2 + b * x + c

# # Ajuste de la curva mediante regresión cuadrática
# params = np.polyfit(x_data, y_data, 2)
# a, b, c = params

# # Punto estimado
# x_estimated = 52
# y_estimated = quadratic_func(x_estimated, a, b, c)

# # Crear un rango de valores x para graficar
# x_range = np.linspace(min(x_data), max(x_data), 100)

# # Calcular los valores correspondientes de y para el rango de x
# y_range = quadratic_func(x_range, a, b, c)

# # Graficar los puntos conocidos y el punto estimado
# plt.plot(x_data, y_data, 'ro', label='Puntos conocidos')
# plt.plot(x_estimated, y_estimated, 'bo', label='Punto estimado')
# plt.plot(x_range, y_range, 'g-', label='Regresión cuadrática')
# plt.xlabel('Número de Frame')
# plt.ylabel('Centro')
# plt.title('Regresión cuadrática de la posición de la pelota')
# plt.legend()
# plt.show()

# # Imprimir los puntos conocidos y el punto estimado
# print("Puntos conocidos:")
# for i in range(len(x_data)):
#     print(f"Frame {x_data[i]}: Centro {y_data[i]}")

# print(f"\nPunto estimado:")
# print(f"Frame {x_estimated}: Centro {y_estimated}")

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy.polynomial import Polynomial

# Función cuadrática
def quadratic_func(x, a, b, c):
    return a * x ** 2 + b * x + c

# Puntos de datos
x_data = np.array([2901, 2800, 2730, 2690, 2656, 2656, 2633, 2616, 2605, 2605])
y_data = np.array([1007, 956, 928, 906, 899, 899, 899, 898, 905, 887])


# Ajustar una función cuadrática a los datos
coefs = Polynomial.fit(range(len(x_data)), x_data, deg=2).convert().coef

# Obtener el siguiente valor extrapolando la función cuadrática
next_x = coefs[0] * len(x_data)**2 + coefs[1] * len(x_data) + coefs[2]

print("Siguiente valor en el eje X:", next_x)

# Ajuste de la curva cuadrática
params, _ = curve_fit(quadratic_func, x_data, y_data)

# Parámetros de la regresión cuadrática
a, b, c = params

# Calcular el valor estimado de y para los puntos existentes
y_estimated = quadratic_func(x_data, a, b, c)

# Imprimir los puntos y sus estimaciones
print("Puntos reales:")
for x, y in zip(x_data, y_data):
    print(f"({x}, {y})")

print("\nEstimaciones:")
for x, y_est in zip(x_data, y_estimated):
    print(f"({x}, {y_est})")

# Predecir el siguiente valor
next_x = x_data[-1] + 1
next_y = quadratic_func(next_x, a, b, c)
print(f"\nSiguiente valor estimado: ({next_x}, {next_y})")

# Graficar los datos y la regresión cuadrática
plt.scatter(x_data, y_data, label='Puntos reales')
plt.plot(x_data, y_estimated, 'r-', label='Regresión cuadrática')
plt.plot(next_x, next_y, 'bo', label='Siguiente valor estimado')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()