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

#ESCALA DE GRISES 
def grayScale(image):
	img = image.copy()
	rangeI = range(len(img))
	rangeJ =range (len(img[0]))
	for i in rangeI:
		for j in rangeJ:
			val = np.sum(img[i,j]) / 3
			img[i,j] = [val, val, val]
	return img

#ROJO
def red(image):
	img = image.copy()
	for i in range(len(img)):
		for j in range (len(img[i])):
			img[i,j] = [img[i,j][0], 0, 0]
	return img

#VERDE
def green(image):
	img = image.copy()
	for i in range(len(img)):
		for j in range (len(img[i])):
			img[i,j] = [0, img[i,j][1], 0]
	return img
#AZUL

def blue(image):
	img = image.copy()
	for i in range(len(img)):
		for j in range (len(img[i])):
			img[i,j] = [0, 0, img[i,j][2]]
	return img

#INVERSO
def inverse(image):
	img = image.copy()
	for i in range(len(img)):
		for j in range (len(img[i])):
			rgb = img[i,j]
			img[i,j] = [255-rgb[0], 255-rgb[1], 255-rgb[2]]
	return img

#RGB
def componenteRGB(image, r, g, b):
	img = image.copy()
	for i in range(len(img)):
		for j in range (len(img[i])):
			img[i,j] = componentRGBPixel(img[i,j], r, g, b)
	return img

#Componente RGB
def componentRGBPixel(rgb, r, g, b):
	if r != 0:
		new_r = (rgb[0]/ 255) * r
	else:
		new_r = 0
	if g != 0:
		new_g = (rgb[1]/ 255) * g
	else:
		new_g = 0
	if b != 0:
		new_b = (rgb[2]/ 255) * b
	else:
		new_b = 0
	return [new_r, new_g, new_b]

#Alto Contraste
def highContrast(image):
	img = image.copy()
	img = grayScale(img)
	for i in range(len(img)):
		for j in range(len(img[i])):
			rgb = img[i,j]
			img[i,j] = [255, 255, 255] if rgb[0] > 125 else [0,0,0]
	return img 

#Mosaico
def mosaic(image, pixelSize):
	img = image.copy()
	img = img.resize((int(img.size[0]/pixelSize), int(img.size[1]/pixelSize)), Image.NEAREST)
	img = img.resize((img.size[0]*pixelSize, img.size[1]*pixelSize), Image.NEAREST)
	return img

#AT&T
def att(image,tam):
	img = image.copy()
	imgGris = grayScale(img)
	imgBN = highContrast(imgGris)
	ancho = len(img[0])
	alto = len(img)
	nuevoAlto = alto - tam
	rgb = imgBN.copy()
	pixels = image.copy()
	for i in range(ancho):
		for j in range(0,nuevoAlto,tam):
			negros = 0
			salto = j + tam
			for k in range(j,salto):
				r,g,b = rgb[k,i]
				if(r == 0):
					negros += 1
			lista = puntosAcumulados(tam,negros)
			for k in range(j,salto):
				if(lista[k-j] == True):
					pixels[k,i] = (0,0,0)
				else:
					pixels[k,i] = (255,255,255)
	return highContrast(pixels)

def puntosAcumulados(tam,pix):
	lista = [None] * tam
	n = pix/2
	if(pix % 2 == 0):
		m = n-1
	else:
		m = n
	inicia = int((tam/2)-n)
	termina = int((tam/2)+m)
	for i in range(inicia,termina):
		lista[i] = True
	return lista

#dithering
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

def cadenaBinario(cadena):
	cadenaBin = ""
	for i in cadena:
		cadenaBin = cadenaBin + bin(ord(i))[2:].zfill(8)
	return cadenaBin

#cifrado
def cifrar(imagen,mensaje):
	rgb = imagen.copy()
	ancho = len(imagen[0])
	alto = len(imagen)
	nueva = Image.new("RGB",(ancho,alto),"white")
	pixels = nueva.load()
	mensajeBin = cadenaBinario(mensaje)
	contador = 0
	for i in range(ancho):
		for j in range(alto):
			r,g,b = rgb[j,i]
			rbyte = "{0:b}".format(r)
			rbyte = list(rbyte)
			gbyte = "{0:b}".format(g)
			gbyte = list(gbyte)
			bbyte = "{0:b}".format(b)
			bbyte = list(bbyte)
			if(contador < len(mensajeBin)):
				if(contador < len(mensajeBin)):
					rbyte[len(rbyte)-1] = mensajeBin[contador]
					contador += 1
				if(contador < len(mensajeBin)):
					gbyte[len(gbyte)-1] = mensajeBin[contador]
					contador += 1
				if(contador < len(mensajeBin)):
					bbyte[len(bbyte)-1] = mensajeBin[contador]
					contador += 1
			else:
				rbyte[len(rbyte)-1] = "1"
				gbyte[len(gbyte)-1] = "1"
				bbyte[len(bbyte)-1] = "1"
			r = "".join(rbyte)
			r = int(r,2)
			g = "".join(gbyte)
			g = int(g,2)
			b = "".join(bbyte)
			b = int(b,2)
			pixels[i,j] = (r,g,b)
	nueva.save(nombre + ".png","PNG")
	return imagen

#estereograma
def estereograma(archivo):
	f = open(archivo,"r")
	g = open("estenograma.txt","w")
	lines = f.readlines()
	abc = string.letters
	sub = abc[26:]
	for i in lines:
		for j in i:
			rand = random.choice(sub)
			g.write(rand)
		g.write("\n")
	g.close()

#brillo
def brillo(imagen, tope):
	rgb = imagen.copy()
	pixels = imagen.copy()
	brillo = tope
	if brillo >= -128 and brillo <= 128:
		for i in range(len(imagen[0])):
			for j in range(len(imagen)):
				r,g,b = rgb[j,i]
				r = r+brillo
				g = g+brillo
				b = b+brillo
				r = min(max(r,0),255)
				g = min(max(g,0),255)
				b = min(max(b,0),255)
				pixels[j,i] = (r,g,b)
		return pixels
	else:
		return pixels

#Sepia
def sepia(imagen,depth):
	gris = grayScale(imagen)
	rgb = gris.copy()
	pixels = imagen.copy()
	ancho = len(imagen[0])
	alto = len(imagen)
	if depth >= 0 and depth <= 255:
		for i in range(ancho):
			for j in range(alto):
				r,g,b = rgb[j,i]
				rr = r+(depth*2)
				gg = g+depth
				if (rr <= ((depth*2)-1)):
					rr = 255
				if (gg <= (depth-1)):
					gg = 255
				pixels[j,i] = (rr,gg,b)
		return pixels
	else:
		return imagen

#Warhol
def warhol(imagen,rojo,verde,azul):
	if ((rojo > 255 or rojo < 0) or (verde > 255 or verde < 0) or (azul > 255 or azul < 0)):
		return imagen
	else:
		rgb = imagen.copy()
		pixels = imagen.copy()
		for i in range(len(imagen[0])):
			for j in range(len(imagen)):
				r,g,b = rgb[j,i]
				andRojo = (rojo & r)
				andVerde = (verde & g)
				andAzul = (azul & b)
				pixels[j,i] = (andRojo,andVerde,andAzul)
		return pixels

def blur1(imagen):
	matriz = np.matrix([[0.0,0.2,0.0],[0.2,0.2,0.2],[0.0,0.2,0.0]])
	factor = 1.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def blur2(imagen):
	matriz = np.matrix([[0,0,1,0,0], [0,1,1,1,0], [1,1,1,1,1], [0,1,1,1,0], [0,0,1,0,0]])
	factor = 1.0/13.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def motionBlur(imagen):
	matriz = np.matrix([[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0], [0,0,1,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0], [0,0,0,0,1,0,0,0,0], [0,0,0,0,0,1,0,0,0], [0,0,0,0,0,0,1,0,0], [0,0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,0,1]])
	factor = 1.0/9.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def encuentraBordes1(imagen):
	matriz = np.matrix([[0,0,-1,0,0], [0,0,-1,0,0], [0,0, 2,0,0], [0,0, 0,0,0], [0,0, 0,0,0]])
	factor = 1.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def encuentraBordes2(imagen):
	matriz = np.matrix([[0,0,-1,0,0], [0,0,-1,0,0], [0,0, 4,0,0], [0,0,-1,0,0], [0,0,-1,0,0]])
	factor = 1.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def encuentraBordes3(imagen):
	matriz = np.matrix([[-1, 0,0, 0, 0], [ 0,-2,0, 0, 0], [ 0, 0,6, 0, 0], [ 0, 0,0,-2, 0], [ 0, 0,0, 0,-1]])
	factor = 1.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def encuentraBordes4(imagen):
	matriz = np.matrix([[-1,-1,-1], [-1, 8,-1], [-1,-1,-1]])
	factor = 1.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def sharpen1(imagen):
	matriz = np.matrix([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])
	factor = 1.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def sharpen2(imagen):
	matriz = np.matrix([[-1,-1,-1,-1,-1], [-1, 2, 2, 2,-1], [-1, 2, 8, 2,-1], [-1, 2, 2, 2,-1], [-1,-1,-1,-1,-1]])
	factor = 1.0/8.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def sharpen3(imagen):
	matriz = np.matrix([[1, 1,1], [1,-7,1], [1, 1,1]])
	factor = 1.0
	bias = 0.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def emboss1(imagen):
	matriz = np.matrix([[-1,-1, 0], [-1, 0, 1], [ 0, 1, 1]])
	factor = 1.0
	bias = 128.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def emboss2(imagen):
	matriz = np.matrix([[-1,-1,-1,-1, 0], [-1,-1,-1, 0, 1], [-1,-1, 0, 1, 1], [-1, 0, 1, 1, 1], [ 0, 1, 1, 1, 1]])
	factor = 1.0
	bias = 128.0
	img = convolucion(imagen,matriz,factor,bias)
	return img

def convolucion(imagen,matriz,factor,bias):
	ancho = len(imagen[0])
	alto = len(imagen)
	rgb = imagen.copy()
	pixels = imagen.copy()
	x,y = matriz.shape

	for i in range(ancho):
		for j in range(alto):
			rojo = 0.0
			verde = 0.0
			azul = 0.0
			for k in range(x):
				for l in range (y):
					imageX = int(i - x / 2 + k + ancho) % ancho
					imageY = int(j - y / 2 + l + alto) % alto
					r,g,b = rgb[imageY, imageX]
					valor = matriz.item((k,l))
					rojo += r * valor
					verde += g * valor
					azul += b * valor
			red = min(max((factor * rojo + bias),0),255)
			green = min(max((factor * verde + bias),0),255)
			blue = min(max((factor * azul + bias),0),255)
			pixels[j,i] = (int(red),int(green),int(blue))

	return pixels

def letraColor(imagen,img,size):
	mosaico = mosaic(img, size)
	ancho = mosaico.size[0]
	alto = mosaico.size[1]
	rgb = mosaico.convert('RGB')
	f = open('letraColor.html','w')
	for i in range(alto):
		for j in range(ancho):
			r,g,b = rgb.getpixel((j,i))
			f.write('<font size="1" style="color:rgb('+str(r)+','+str(g)+','+str(b)+');">M</font>')
		f.write('<br>')
	f.close()

def letraGris(imagen,img,size):
	mosaico = mosaic(img, size)
	mos = np.array(mosaico)
	gris = grayScale(mos)
	ancho = len(mos[0])
	alto = len(mos)
	rgb = gris.copy()
	f = open('letraGris.html','w')
	for i in range(alto):
		for j in range(ancho):
			r,g,b = rgb[i,j]
			f.write('<font size="1" style="color:rgb('+str(r)+','+str(g)+','+str(b)+');">M</font>')
		f.write('<br>')
	f.close()

def simbolos(imagen,img,size):
	mosaico = mosaic(img, size)
	mos = np.array(mosaico)
	gris = grayScale(mos)
	ancho = len(mos[0])
	alto = len(mos)
	rgb = gris.copy()
	f = open('simbolos.html','w')
	f.write("<PRE>")
	for i in range(alto):
		for j in range(ancho):
			r,g,b = rgb[i,j]
			if(r >= 0 and r < 16):
				f.write('<font size="1">M</font>')
			elif(r >= 16 and r < 32):
				f.write('<font size="1">N</font>')
			elif(r >= 32 and r < 48):
				f.write('<font size="1">H</font>')
			elif(r >= 48 and r < 64):
				f.write('<font size="1">#</font>')
			elif(r >= 64 and r < 80):
				f.write('<font size="1">Q</font>')
			elif(r >= 80 and r < 96):
				f.write('<font size="1">U</font>')
			elif(r >= 96 and r < 112):
				f.write('<font size="1">A</font>')
			elif(r >= 112 and r < 128):
				f.write('<font size="1">D</font>')
			elif(r >= 128 and r < 144):
				f.write('<font size="1">O</font>')
			elif(r >= 144 and r < 160):
				f.write('<font size="1">Y</font>')
			elif(r >= 160 and r < 176):
				f.write('<font size="1">2</font>')
			elif(r >= 176 and r < 192):
				f.write('<font size="1">$</font>')
			elif(r >= 192 and r < 208):
				f.write('<font size="1">%</font>')
			elif(r >= 208 and r < 224):
				f.write('<font size="1">+</font>')
			elif(r >= 224 and r < 240):
				f.write('<font size="1">-</font>')
			elif(r >= 240 and r < 256):
				f.write('<font size="1">M</font>')
		f.write('<br>')
	f.close()

def naipes(imagen,img,size):
	mosaico = mosaic(img, size)
	mos = np.array(mosaico)
	gris = grayScale(mos)
	ancho = len(mos[0])
	alto = len(mos)
	rgb = gris.copy()
	f = open('naipes.html','w')
	f.write("<PRE><style>@font-face{font-family: 'Playcrds';src: url('dominos-cartas_FILES/Playcrds.TTF') format('truetype');}font{font-family: 'Playcrds'}</style>")
	for i in range(alto):
		for j in range(ancho):
			r,g,b = rgb[i,j]
			if(r >= 0 and r < 19):
				f.write('<font size="1">A</font>')
			elif(r >= 19 and r < 38):
				f.write('<font size="1">B</font>')
			elif(r >= 38 and r < 57):
				f.write('<font size="1">C</font>')
			elif(r >= 57 and r < 76):
				f.write('<font size="1">D</font>')
			elif(r >= 76 and r < 95):
				f.write('<font size="1">E</font>')
			elif(r >= 95 and r < 114):
				f.write('<font size="1">F</font>')
			elif(r >= 114 and r < 133):
				f.write('<font size="1">G</font>')
			elif(r >= 133 and r < 152):
				f.write('<font size="1">H</font>')
			elif(r >= 152 and r < 171):
				f.write('<font size="1">I</font>')
			elif(r >= 171 and r < 190):
				f.write('<font size="1">J</font>')
			elif(r >= 190 and r < 209):
				f.write('<font size="1">K</font>')
			elif(r >= 209 and r < 228):
				f.write('<font size="1">L</font>')
			elif(r >= 228 and r < 256):
				f.write('<font size="1">M</font>')
		f.write('<br>')
	f.close()

def domino(imagen,img,size):
	mosaico = mosaic(img, size)
	mos = np.array(mosaico)
	gris = grayScale(mos)
	ancho = len(mos[0])
	alto = len(mos)
	rgb = gris.copy()
	f = open('domino.html','w')
	f.write("<PRE><style>@font-face{font-family: 'lasvwd__';src: url('dominos-cartas_FILES/lasvwd__.TTF') format('truetype');}font{font-family: 'lasvwd__'}</style>")
	for i in range(alto):
		for j in range(ancho):
			r,g,b = rgb[i,j]
			if(r >= 0 and r < 25):
				f.write('<font size="1">0</font>')
			elif(r >= 25 and r < 50):
				f.write('<font size="1">1</font>')
			elif(r >= 50 and r < 75):
				f.write('<font size="1">2</font>')
			elif(r >= 75 and r < 100):
				f.write('<font size="1">3</font>')
			elif(r >= 100 and r < 125):
				f.write('<font size="1">4</font>')
			elif(r >= 125 and r < 150):
				f.write('<font size="1">5</font>')
			elif(r >= 150 and r < 175):
				f.write('<font size="1">6</font>')
			elif(r >= 175 and r < 200):
				f.write('<font size="1">7</font>')
			elif(r >= 200 and r < 225):
				f.write('<font size="1">8</font>')
			elif(r >= 225 and r < 256):
				f.write('<font size="1">9</font>')
		f.write('<br>')
	f.close()



naipes(pixels,image,35)
domino(pixels,image,35)

# plt.imshow(motionBlur(pixels))
# plt.show()

# plt.imshow(warhol(pixels,100,100,100))
# plt.show()

# plt.imshow(sepia(pixels, 10))
# plt.show()

# estereograma("img1.jpg")
# cifrar(pixels, "Hola soy Javier", "cipher")

