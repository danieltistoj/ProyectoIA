from PIL import Image, ImageOps
import validar
import numpy as np
n='n'
im=None
ann = validar.cargarRed()
while(n!='s'):
	ruta = raw_input('Ingrese la ruta del archivo: ')
	#im = Image.open(ruta)
	#im.show()
	origin = validar.validar(ruta,ann)
	ron= [ round(num,0) for num in origin]
	print (origin)
	if np.sum(ron)>1 or np.sum(ron)==0 :
		print ('ERROR',"No se reconoce")
	else:
		if ron[0]==1:
			print ("Fresa Madura")
		elif ron[1]==1:
			print ("Fresa Pasada")
		else:
			print ("Fresa Podrida")
	n = raw_input("Salir? (s)")
	print
	print

