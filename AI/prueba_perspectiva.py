import cv2
import numpy as np

foto = cv2.imread("E:\Guido\Documentos\Programacion\Hawkeye\IA\imagenPrueba.png")

pts1 = np.float32([[121, 144], [271, 144], [64, 281], [341, 283]])
pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
deformado = cv2.warpPerspective(foto, matrix, (164, 474))

print(matrix)

#Hola Arotu!

cv2.imshow('prueba', foto)
cv2.imshow('deformado', deformado)
cv2.waitKey(0)