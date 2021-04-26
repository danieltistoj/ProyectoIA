import cv2
def ProcesarFoto(img):
	lista=[]

	##### FILTROS: Foto normal -> Filtro blanco y negro -> Filtro Gaussiano #####
	foto = cv2.imread(img)
	#fotoTemp = cv2.imread(img)
	#cv2.imshow('Color', foto)
	fotoBN = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
	#cv2.imshow('BN', fotoBN)
	fotoG = cv2.GaussianBlur(fotoBN, (51,51), 3)
	#cv2.imshow('Gauss', fotoG)

	##### OBTENCION DE BINARIOS  #####
	binario = cv2.adaptiveThreshold(fotoG, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,901,29)
	#t, binario = cv2.threshold(fotoG, 190, 300, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
	#cv2.imshow('Binario', binario)
	canny = cv2.Canny(binario, 10, 100)
	#cv2.imshow('Bordes', canny)

	##### CONTORNOS DE LA FOTOGRAFÍA #####
	contornos = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
	#cv2.drawContours(fotoTemp, contornos, -1, (128,0,0), 2)
	#cv2.imshow("Contornos",fotoTemp)

	##### RECORTE DE FOTOGRAFIA #####
	for c in contornos:
	    area = cv2.contourArea(c)
	    if area > 90:  
	        x, y, w, h = cv2.boundingRect(c)
	        cv2.rectangle(canny, (x, y), (x + w, y + h), (200, 200, 0), 1) 
	        crop_img = foto[y:y+h, x:x+w]
	        lista.append(crop_img)
	        #cv2.imshow("a",crop_img)
	return lista
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()