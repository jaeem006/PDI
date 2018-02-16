#Javier Enriquez Mendoza
#Proceso Digital de Imagenes
#Tarea 1

import numpy as np 
from scipy import misc
import matplotlib.pyplot as plt

f = misc.imread('img2.jpg')

print(len(f))
print(len(f[0]))

#ESCALA DE GRISES 
def grayScale(img):
	rangeI = range(len(img))
	rangeJ =range (len(img[0]))
	for i in rangeI:
		for j in rangeJ:
			val = np.sum(img[i,j]) / 3
			img[i,j] = [val, val, val]
	return img

#ROJO
def red(img):
	for i in range(len(img)):
		for j in range (len(img[i])):
			img[i,j] = [img[i,j][0], 0, 0]
	return img

#VERDE
def green(img):
	for i in range(len(img)):
		for j in range (len(img[i])):
			img[i,j] = [0, img[i,j][1], 0]
	return img
#AZUL

def blue(img):
	for i in range(len(img)):
		for j in range (len(img[i])):
			img[i,j] = [0, 0, img[i,j][2]]
	return img

#INVERSO
def inverse(img):
	for i in range(len(img)):
		for j in range (len(img[i])):
			rgb = img[i,j]
			img[i,j] = [255-rgb[0], 255-rgb[1], 255-rgb[2]]
	return img

#RGB
def componenteRGB(img, r, g, b):
	for i in range(len(img)):
		for j in range (len(img[i])):
			img[i,j] = componentRGBPixel(img[i,j], r, g, b)
	return img


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

def highContrast(img):
	img = grayScale(img)
	for i in range(len(img)):
		for j in range(len(img[i])):
			rgb = img[i,j]
			img[i,j] = [255, 255, 255] if rgb[0] > 125 else [0,0,0]
	return img 

#def mosaic(img):
#	for i in range(len(img)):
#		for j in range(len(img[i]))

plt.imshow(grayScale(f))
plt.show()

