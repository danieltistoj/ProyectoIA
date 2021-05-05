import neurolab as nl
import numpy as np
import scipy as sp

#Se genera una matriz a partir de los datos del modulo anterior
#Se especifica los valores de entrada y salida
datos = np.matrix(sp.genfromtxt("Entrenamiento.csv", delimiter=" "))
entrada = datos[:,:-3]
objetivo = datos[:,-3:]

#Se especifican los valores maximos y minimos de cada dato
#Tambien se determina la cantidad de neuronas en cada capa de la red neuronal
maxmin = np.matrix([[ -5, 5] for i in range(len(entrada[1,:].T))])
capa_entrada = entrada.shape[0]
capa_oculta1 = int(capa_entrada*0.5)
capa_salida = 3

#Se genera la red neuronal con el numero determinado anteriormente y se entrena la red
rna = nl.net.newff(maxmin, [capa_entrada, capa_entrada, capa_oculta1, capa_salida])
rna.trainf = nl.train.train_gd

error = rna.train(entrada, objetivo, epochs=1000000, show=100, goal=0.0001, lr=0.01)

#Se guarda la informacion de la red neuronal para posteriores comprobaciones con datos distintos
#a los datos de entrenamiento.
rna.save("RNAFresa.tmt")
salida = rna.sim(entrada)
print (salida)