from __future__ import division
import cv2
import numpy as np
from os import listdir

# Recorta las imagenes por partes para poder evaluar el nivel de madurez de la fruta
#Libreria para las direcciones
#Libreria para utilizar float como python 3.5
#libreria para aplicar filtros y determinar colores en python
#LIBRRIA para matrices y vectores

#Funcion recorre los directorios(carpeta) en ella busca cada imagen y llama a la funcion contorno
def Directorio(CarpetaImagenes, CarpetaRecortes, Imagenes_):
    for NombreImagen in Imagenes_:
        print(NombreImagen)
        imagen = cv2.imread(CarpetaImagenes + "/" +NombreImagen)
        buscaFresa = BuscarFresa(imagen)
        cv2.imwrite((CarpetaRecortes + "/" + NombreImagen), buscaFresa)


#Busca encontrar el contorno de la imagen
def contorno(imagen):
    imagen = imagen.copy()
    contornos = cv2.findContours(imagen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contour_sizes = [(cv2.contourArea(contorno), contorno) for contorno in contornos]
    mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

    mascara = np.zeros(imagen.shape, np.uint8)
    cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
    return mayor_contorno, mascara


#Con el tratamiento de la imagen y su contorno se le calculan las dimensiones nuevas a tener 
#Estas dimensiones son recortadas a un rectangulo y la ubicacion del mismo
def rectangulo(imagen, contorno):
    imagenElipse = imagen.copy()
    elipse = cv2.fitEllipse(contorno)
    factor_redn = 0.5
    sx = int((elipse[1][0]*factor_redn)/2)
    sy = int((elipse[1][1]*factor_redn)/2)
    x = int(elipse[0][0]) - sy
    y = int(elipse[0][1]) - sx
    if x < 0 and y < 0:
        x = x * -1
        y = y * -1
    imagenElipse = imagenElipse[y:(y + sx*2), x:(x + sy*2)]
    return imagenElipse

#Trata la imagen para encontrara un cuadrado y redimensionarla
def BuscarFresa(imagen):
    imagen2 = imagen.copy()
    imagen3 = imagen.copy()
    imagen2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2HSV)
    max_dimension = max(imagen2.shape)
    scale = 700/max_dimension
    imagen2 = cv2.resize(imagen2, None, fx=scale, fy=scale)
    imagen3 = cv2.resize(imagen3, None, fx=scale, fy=scale)
    imagen_azul = cv2.GaussianBlur(imagen2, (7, 7), 0)
    min_rojo = np.array([0, 100, 80])
    max_rojo = np.array([10, 256, 256])

    mascara1 = cv2.inRange(imagen_azul, min_rojo, max_rojo)
    min_rojo2 = np.array([10, 100, 80])
    max_rojo2 = np.array([180, 256, 256])

    mascara2 = cv2.inRange(imagen_azul, min_rojo2, max_rojo2)
    mascara = mascara1 + mascara2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    MascaraCerrada = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    MascaraLimpia = cv2.morphologyEx(MascaraCerrada, cv2.MORPH_OPEN, kernel)

    contorno_Fresa_gramde, mascara_Fresa = contorno(MascaraLimpia)

    rectangulo_Fresa = rectangulo(imagen3, contorno_Fresa_gramde)
    return rectangulo_Fresa


Directorio("FresasInmaduras", "FresasRecortadasI", listdir("./FresasInmaduras"))
Directorio("FresasMaduras", "FresasRecortadasM", listdir("./FresasMaduras"))
Directorio("FresasPasadas", "FresasRecortadasP", listdir("./FresasPasadas"))