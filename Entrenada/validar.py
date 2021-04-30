from fann2 import libfann as fann
import Fotografia as fotogr 
import cv2

def imagenAEpisodio(imagen):
	lista=[]
	for fil in imagen:
		for col in fil:
			for x in col:
				lista.append(x)
	return lista
##### Cargamos la red neuronal previamente entrenada #####
def cargarRed(ruta="RedNeuronal.net"):
	ann = fann.neural_net()
	ann.create_from_file(ruta)
	return ann
##### Validamos la fotografía a escanear #####
def validar(ruta,ann): 
	im=cv2.resize(fotogr.ProcesarFoto(ruta)[0],(50,50))
	#cv2.imshow(ruta,im)
	#cv2.waitKey(0)
	entrada = imagenAEpisodio(im)
#print len(entrada)
	return ann.run(entrada)