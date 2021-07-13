'''
offset correction for arducam sensor demosaicing
edits 'take_images.py' by taking dark images and finding the offset value
that overlaps the histogram maxima of rows and columns

'''


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def histogram(image):
	data = image
	hist=plt.hist(data.ravel(), bins=256,range=(0.0, 1.0), fc='k', ec='k') #definir el rango x segun cantidad de pixeles
	
	plt.show(hist)
	y=hist[0]
	x=hist[1]
	x_max=x[np.where(y == hist[0].max())]
	#x_max=maxima
	return x_max

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

offset=10
value='0x000F'
newvalue=15
overlap_max_error=0.01
offset_increment=10

while offset>overlap_max_error:
	#os.system('take_images.py dark_img 1')
	#imagen=plt.imread(dark_img)

	imagen=plt.imread('20kV.png')

	#imagen[::2] # odd row
	#imagen[:,1::2] #even column
	im1=imagen[::2,1::2] #odd row+even column
	im2=imagen[::2,::2] #odd column+even row

	offset=abs(histogram(im1)-histogram(im2))

	print('offset_err=',offset)
	newvalue+=offset_increment
	newvalue_hex = '0x' + hex(newvalue)[2:].zfill(4).upper()
	replace_line('take_images.py', 107, '    [0x63, '+str(newvalue_hex)+'], # BLC offset: Even row,odd column \n')
	print(newvalue_hex)