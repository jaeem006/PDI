#Javier Enriquez Mendoza
#Proceso Digital de Imagenes
#Tarea 1

import numpy as np 
# from scipy import misc
import matplotlib.pyplot as plt
from PIL import Image

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

def highContrast(image):
	img = image.copy()
	img = grayScale(img)
	for i in range(len(img)):
		for j in range(len(img[i])):
			rgb = img[i,j]
			img[i,j] = [255, 255, 255] if rgb[0] > 125 else [0,0,0]
	return img 

def mosaic(image, pixelSize):
	img = image.copy()
	img = img.resize((int(img.size[0]/pixelSize), int(img.size[1]/pixelSize)), Image.NEAREST)
	img = img.resize((img.size[0]*pixelSize, img.size[1]*pixelSize), Image.NEAREST)
	return img

#def mosaic(img):
#	for i in range(len(img)):
#		for j in range(len(img[i]))

plt.imshow(grayScale(pixels))
plt.show()

plt.imshow(red(pixels))
plt.show()

plt.imshow(green(pixels))
plt.show()

plt.imshow(blue(pixels))
plt.show()

plt.imshow(inverse(pixels))
plt.show()

plt.imshow(componenteRGB(pixels, 200,100,0))
plt.show()

plt.imshow(highContrast(pixels))
plt.show()

plt.imshow(mosaic(image, 35))
plt.show()

