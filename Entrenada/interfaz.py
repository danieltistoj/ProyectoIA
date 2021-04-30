import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageOps
import validar
import numpy as np

class GUI(Frame):
	ruta='/'
	im = None
	ann = None
	def __init__(self,master=None):
		Frame.__init__(self)
		self.ann = validar.cargarRed() ##### Cargamos el archivo generado en la carpeta de entramiento #####
		##### Buscamos la fotografía que queremos #####
		def btnaceptarClick():
			root.filename = filedialog.askopenfilename(initialdir = "\Desktop", title = "Buscar imagen",filetypes = (("jpeg files","*.jpg | *.jpeg | *.png"),("all files","*.*")))
			self.ruta=root.filename
			if(self.im != None):
				messagebox.showinfo('¡ERROR!',"Imagen no aceptada...")
				self.im.close()
			messagebox.showinfo('¡CORRECTO!',"Imagen aceptada correctamente")
		
		def hola():
			if(self.ruta!=None):
				origin = validar.validar(self.ruta,self.ann)
				ron= [ round(num,0) for num in origin]
				print (ron)
				if np.sum(ron)>1 or np.sum(ron)==0 :
					messagebox.showinfo('¡ERROR!',"No se reconoce la imagen...")
				else:
					if ron[0]==1:
						messagebox.showinfo('Fresa',"Fresa Madura")
					elif ron[1]==1:
						messagebox.showinfo('Fresa',"Fresa Pasada")
					else:
						messagebox.showinfo('Fresa',"Fresa Podrida")
		def imagenAEpisodio(imagen):
			image = Image.open(imagen)
			pixeles = list(image.getdata())
			lista=[]
			for x in pixeles:
				lista.append(x[0])
				lista.append(x[1])
				lista.append(x[2])
			return lista
		self.btnaceptar = Button(root, command=btnaceptarClick, text="Buscar Imagen")
		self.btnaceptar.pack(fill=X,pady=10,padx=100)
		self.boton = Button(root,command=hola,text="Validar Imagen")
		self.boton.pack(fill=X,pady=10,padx=100)
root = Tk()
root.title("Red #2")
root.resizable(width=FALSE, height=FALSE)
guiframe=GUI(root)
guiframe.pack()
root.mainloop()
