import cv2
import numpy as np

foto = cv2.imread("E:\Guido\Documentos\Programacion\Hawkeye\IA\imagenPrueba.png")

pts1 = np.float32([[121, 144], [271, 144], [64, 281], [341, 283]])
pts2 = np.float32([[0, 0], [164, 0], [0, 474], [164, 474]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
deformado = cv2.warpPerspective(foto, matrix, (164, 474))

cords_pelota = np.array([[237], [165], [1]])
cords_pelota_pers = np.dot(matrix, cords_pelota)
cords_pelota_pers = (int(cords_pelota_pers[0]/cords_pelota_pers[2]), int(cords_pelota_pers[1]/cords_pelota_pers[2]))

deformado = cv2.circle(deformado, cords_pelota_pers, 2, (0, 0, 255), -1)

print(cords_pelota_pers)

cv2.imshow('prueba', foto)
#cv2.imshow('deformado', deformado)
cv2.waitKey(0)