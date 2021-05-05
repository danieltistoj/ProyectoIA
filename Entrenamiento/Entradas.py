from PIL import Image
from os import listdir
import os

#Genera los datos de entrada a la red neuronal para el entrenamiento a partir de los recortes realizados
#y almacenados en las carpetas especificadas anteriormente
#Obtiene el formato RGB de cada pixel del recorte a analizar
def RGBEntrada(Imagen, salida_red):
    foto = Image.open(Imagen)
    foto = foto.resize((40, 10), Image.ANTIALIAS)
    pixels = foto.load()
    archivo_entrenamiento = open("Entrenamiento.csv", "a")
    filas, columnas = foto.size
    decimales = 4
    for columna in range (columnas):
        for fila in range(filas):
            R = str(normalizar(pixels[fila,columna][0]))
            G = str(normalizar(pixels[fila,columna][1]))
            B = str(normalizar(pixels[fila,columna][2]))
            cadena = R[:R.find(".")+decimales] + " " + G[:G.find(".")+decimales] + " " + B[:B.find(".")+decimales] + " "
            archivo_entrenamiento.write(cadena)

    archivo_entrenamiento.write(salida_red)
    archivo_entrenamiento.write("\n")
    archivo_entrenamiento.close()

#Recorre la carpeta especificada con cada archivo que encuentre en ella
def carpetaFotos(carpeta, lista, salida):
    for nombre in lista:
        print(nombre)
        RGBEntrada(carpeta + "/" +nombre, salida)

#Normaliza el valor del colo para no tener un rango muy grande de valores (el rango sera entre 0 y 1)
def normalizar(valor):
    salida = (valor*1.)/255.
    return salida
    

if(os.path.exists("Entrenamiento.csv")== True):
    os.remove("Entrenamiento.csv")
carpetaFotos("FresasRecortadasI", listdir("./FresasRecortadasI"), "0 1 0")
carpetaFotos("FresasRecortadasM",  listdir("./FresasRecortadasM"), "1 0 0")
carpetaFotos("FresasRecortadasP", listdir("./FresasRecortadasP"), "0 0 1" )
