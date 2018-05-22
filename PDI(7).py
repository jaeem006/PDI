#Javier Enriquez Mendoza
#Proceso Digital de Imagenes
#filtros

import numpy as np 
import png
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import random

image = Image.open('img1.jpg')
pixels = np.array(image)

def dithering(image):
	rgb = image.copy()
	pixels = image.copy()
	ancho = len(image[0])
	alto = len(image)
	for i in range(alto):
		errorDif = 0
		k = 1
		for j in range(ancho):
			r,g,b = rgb[i,j]
			newByte = errorDif + r
			if (newByte >= 255):
				newByte = 255
				pixels[i,j] = (255,255,255)
				errorDif = 0
			elif(newByte <= 0):
				newByte = 0
				pixels[i,j] = (0,0,0)
				errorDif = 0
			elif((255-newByte) > 127):
				pixels[i,j] = (0,0,0)
				k = 1
				errorDif = newByte * k
			else:
				pixels[i,j] = (255,255,255)
				k = -1
				errorDif = 255 - newByte
				errorDif = errorDif * k
	return pixels

def generaImagenesGris(imagen,aplica):
    gris = filtroGris1(imagen,aplica)
    brillo = -128
    contador = 1
    while(brillo < 129):
        im = filtroBrillo(gris,imagen,brillo)
        im.save("imagen"+str(contador)+".png","PNG")
        brillo = brillo + 9
        contador = contador + 1

def aplicaRecursivaColor(imagen,aplica,mosX,mosY):
    size = mosX,mosY
    posX = 0
    posY = 0
    recorreX = 0
    recorreY = 0
    rprom = 0
    gprom = 0
    bprom = 0
    promedio = 0
    ancho = imagen.size[0]
    alto = imagen.size[1]
    rgb = imagen.convert('RGB')
    pixels = aplica.load()
    for i in range(0,ancho,mosX):
        recorreX = i + mosX
        for j in range(0,alto,mosY):
            recorreY = j + mosY
            for k in range(i,recorreX):
                if (k >= ancho):
                    break
                for l in range(j,recorreY):
                    if (l >= alto):
                        break
                    r,g,b = rgb.getpixel((k,l))
                    rprom += r
                    gprom += g
                    bprom += b
                    promedio += 1
            promRojo = (rprom/promedio)
            promVerde = (gprom/promedio)
            promAzul = (bprom/promedio)
            rprom = 0
            gprom = 0
            bprom = 0
            promedio = 0
            pinta = PIL.Image.new('RGB',(500,500))
            img = filtroWarhol(imagen,pinta,promRojo,promVerde,promAzul)
            img = img.resize(size)
            aplica.paste(img,(posX,posY))
            posY += mosY
        posX += mosX
        posY = 0
    return aplica