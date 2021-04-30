import cv2
from fann2 import libfann as fann
import Fotografia as fotogr 
from os import listdir
from os.path import isfile

salidas=[]
def entrenamiento(inp,out,capas):
	indice_conexion = 1 #Caracteristica de las conexiones entre capas 1 -> completamente conectada
	rango_aprendizaje = 0.1 #Constante de aprendizaje
	error_deseado = 0.0001 #Error deseado a obtener 0.01%
	data = fann.training_data()    
	data.set_train_data(inp,out)
	max_iteraciones = 100 #Número de epocas
	ann = fann.neural_net()
	ann.create_sparse_array(indice_conexion, capas) #Funcion que crear la red, PARAM indice y vector de neuronas por capa
	ann.set_learning_rate(rango_aprendizaje) #Funcion para insertar el rango de aprendizaje
	ann.set_activation_function_output(fann.SIGMOID) #Setear la funcion de activacion
		
	###### Entrenar la red en un archivo de salida, maximo de iteraciones ##### 
	ann.train_on_data(data,max_iteraciones,100,error_deseado)
	ann.save("RedNeuronal.net")

def imagenAEpisodio(imagen):
	lista=[]
	for fil in imagen:
		for col in fil:
			for x in col:
				lista.append(x)
	return lista

##### Se enlista las fotografías para el entrenamiento de la red #####
def listar_red1(ruta='.'):
	lista=[]
	for archivo in listdir(ruta): 
		if isfile(archivo):
			nombre = archivo.split(".")
			if(nombre[1]=='jpg' or nombre[1]=='jpeg' or nombre[1]=='png'):
				#print("primer caracter:", nombre[0][0], " segundo caracter:", nombre[0][1])
				##### Fresa Podrida FP #####
				if (nombre[0][0] == 'F' and nombre[0][1] == 'P'):
					salidas.append([0, 0, 1])
				##### Fresa Madura FM #####
				elif (nombre[0][0] == 'F' and nombre[0][1] == 'M'):
					salidas.append([0, 1, 0])
				##### Fresa Inmadura  FI#####
				elif (nombre[0][0] == 'F' and nombre[0][1] == 'I'):
					salidas.append([1, 0, 0])
				##### Otro Objeto  #####
				else:
					salidas.append([1, 1, 1])
				lista.append(archivo)
				#print("lista:", lista)
	return lista
##### Generamos las entradas, metiendo en una lista las fotografías ya compuestas #####
def generarEntrada():
	entradas=[]
	for r in listar_red1():
		im=cv2.resize(fotogr.ProcesarFoto(r)[0],(50,50))
		entradas.append(imagenAEpisodio(im))
	return entradas
entradas=generarEntrada()
##### Enviamos las entradas, salidas, 7500, 5000 y 3 neuronas #####
entrenamiento(entradas,salidas,[7500,5000,3])