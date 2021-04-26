import cv2
from fann2 import libfann as fann
import Fotografia as fotogr 
from os import listdir
from os.path import isfile

salidas=[]
def entrenamiento(inp,out,capas):
	indice_conexion = 1 #Caracteristica de las conexiones entre capas 1 -> completamente conectada
	rango_aprendizaje = 0.1 #Constante de aprendizaje
	error_deseado = 0.0001
	data = fann.training_data()    
	data.set_train_data(inp,out)
	max_iteraciones = 100000
	ann = fann.neural_net()
	ann.create_sparse_array(indice_conexion, capas)# funcion que crear la red, PARAM indice y vector de neuronas por capa
	ann.set_learning_rate(rango_aprendizaje) #funcion para insertar el rango de aprendizaje,
	ann.set_activation_function_output(fann.SIGMOID) #setear la funcion de activacion 
	#ann.train_on_file("and.data", max_iteraciones, 1000, error_deseado)
	#^Entrenar la red en un archivo PARAM archivo salida, maximo de iteraciones, 
	ann.train_on_data(data,max_iteraciones,100,error_deseado)
	ann.save("red20.net")

def imagenAEpisodio(imagen):
	lista=[]
	for fil in imagen:
		for col in fil:
			for x in col:
				lista.append(x)
	return lista

def listar_red1(ruta='.'):
	lista=[]
	for archivo in listdir(ruta): 
		if isfile(archivo):
			nombre = archivo.split(".")
			if(nombre[1]=='jpg' or nombre[1]=='jpeg' or nombre[1]=='png'):
    			##### Fresa Podrida #####	
				if(nombre[0][0]=='FP'):
					salidas.append([0,0,1])
				##### Fresa Madura #####
				elif(nombre[0][0]=='FM'):
					salidas.append([0,1,0])
				##### Fresa Inmadura #####
				elif(nombre[0][0]=='FI'):
					salidas.append([1,0,0])
				##### Otro Objeto #####
				elif(nombre[0][0]=='O'):
					salidas.append([1,1,1])
				lista.append(archivo)
	return lista
def generarEntrada():
	entradas=[]
	for r in listar_red1():
		im=cv2.resize(fotogr.ProcesarFoto(r)[0],(50,50))
		entradas.append(imagenAEpisodio(im))
	return entradas
entradas=generarEntrada()
entrenamiento(entradas,salidas,[7500,5000,3])
