import cv2
from PIL import Image as Img
from PIL import ImageTk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import imutils
import Comprobar as c

def elegir_imagen():
    path_image = filedialog.askopenfilename(initialdir = "\Desktop", title = "Buscar imagen",filetypes = (("jpeg files","*.jpg | *.jpeg | *.png"),("all files","*.*")))
    if len(path_image) > 0:
        global image
        # Leer la imagen de entrada y la redimensionamos
        image = cv2.imread(path_image)
        image = imutils.resize(image, height=380)
        # Para visualizar la imagen de entrada en la GUI
        imageToShow= imutils.resize(image, width=180)
        imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        im = Img.fromarray(imageToShow )
        img = ImageTk.PhotoImage(image=im)
        lblInputImage.configure(image=img)
        lblInputImage.image = img
        # Label IMAGEN DE ENTRADA
        #print(c.fotoComp(path_image))
        lblInfo1 = Label(root, text="Imagen Seleccionada:")
        lblInfo1.grid(column=0, row=1, padx=5, pady=5)
        messagebox.showinfo("¡Fresa encontrada!", c.fotoComp(path_image))
        #print(path_image)

# Creamos la ventana principal
root = Tk()
root.title("RF")
# Label donde se presentará la imagen de entrada
lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2)
# Creamos el botón para elegir la imagen de entrada
btn = Button(root, text="Cargar fotografía", width=25, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5)
root.mainloop()