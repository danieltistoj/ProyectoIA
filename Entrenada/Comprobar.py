from __future__ import division
import cv2
import numpy as np
from PIL import Image
from os import listdir
import os
import neurolab as nl
import scipy as sp

#Se realiza todo el proceso para el tratamiento de imagenes como con los datos de entrenamiento
#A excepcion de que en este caso solo se comprobaran los valores extraidos de la imagen deseada

def mostrar(imagen):
    imagen = cv2.resize(imagen, (300, 300))
    cv2.imshow('fresa', imagen)
    cv2.waitKey(0)

def contorno(imagen):
    imagen = imagen.copy()
    contornos = cv2.findContours(imagen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contour_sizes = [(cv2.contourArea(contorno), contorno) for contorno in contornos]
    mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

    mascara = np.zeros(imagen.shape, np.uint8)
    cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
    return mayor_contorno, mascara

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

#Finaliza el tratamiento de imagen e inicia la extraccion de datos
def RGBEntrada(Imagen):
    foto = Image.open(Imagen)
    foto = foto.resize((40, 10), Image.ANTIALIAS)
    pixels = foto.load()
    filas, columnas = foto.size
    decimales = 4
    cadena = ""
    for columna in range (columnas):
        for fila in range(filas):
            R = str(normalizar(pixels[fila,columna][0]))
            G = str(normalizar(pixels[fila,columna][1]))
            B = str(normalizar(pixels[fila,columna][2]))
            cadena += R[:R.find(".")+decimales] + " " + G[:G.find(".")+decimales] + " " + B[:B.find(".")+decimales] + " "

    return cadena

def normalizar(valor):
    salida = (valor*1.)/255.
    return salida

#Finaliza extraccion de datos e inicia comprobacion de datos
def fotoComp(ruta):
    imagen = cv2.imread(ruta)
    imagen = BuscarFresa(imagen)
    cv2.imwrite("RecorteFresaPrueba.jpg",imagen)

    cadena =  RGBEntrada("RecorteFresaPrueba.jpg")  

    if(os.path.exists("PruebaFresa.csv")== True):
        os.remove("PruebaFresa.csv")

    archivoPrueba = open("PruebaFresa.csv", "a")
    archivoPrueba.write(cadena)
    archivoPrueba.close()

    datos = np.matrix(sp.genfromtxt("PruebaFresa.csv", delimiter=" "))

    rna = nl.load("RNAFresa.tmt")

    salida = rna.sim(datos)

    M = salida[0][0] * 100
    I = salida[0][1] * 100
    P = salida[0][2] * 100
    resultado = ""

    if (P > 80.):
        if (M > 40.):
            resultado = "La fresa esta por pasarse"
        else:
            resultado = "La fresa esta podrida"
    elif (M > 80.):
        if (P > 40.):
            resultado = "La fresa esta muy madura"
        elif (I > 40.):
            resultado = "La fresa esta a punto madurar"
        else:
            resultado = "La fresa esta en su mejor punto"
    elif (I > 80.):
        if (M > 40.):
            resultado = "La fresa aun no esta madura"
        else:
            resultado = "La fresa esta madurando"
    
    return resultado