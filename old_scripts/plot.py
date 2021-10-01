import pylab as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

# ----------------------------------------
ivA=pd.read_csv('noFFT.csv',skiprows=[1])

ivA.info()

im1 = (mpimg.imread('noFFT.jpg'))
im2 = mpimg.imread('FFT.jpg')
fig = plt.figure()

# show original image
#-----------------------------------
fig.add_subplot(221)
plt.title('')
plt.ylabel('Sin filtro')
plt.set_cmap('gray')
plt.imshow(im1)
#-----------------------------------
ax1=fig.add_subplot(222)
plt.title('Histogramas')
ax1.yaxis.tick_left()
ax1.yaxis.set_label_position("left")
#plt.hist(im1.ravel(), bins=256, range=(0, 255), fc='k', ec='k')
plt.fill_between(ivA['Distance_(pixels)'],ivA['noFFTcounts'],color='black')
#plt.text(120,188050, r'$\mu=41.5,\ \sigma=2.9$')
#plt.text(120,158050, r'min=28, max=60')
plt.ylabel('numero de pixeles')
plt.xlabel('Valor de pixel [ADU]')
#-----------------------------------
fig.add_subplot(223)

plt.ylabel('Filtro FFT pasa-alto')
plt.set_cmap('gray')
plt.imshow(im2)
#-----------------------------------
ax2=fig.add_subplot(224)
ax2.yaxis.tick_left()
ax2.yaxis.set_label_position("left")
#plt.hist(im1.ravel(), bins=256, range=(0, 255), fc='k', ec='k')
plt.fill_between(ivA['Distance_(pixels)'],ivA['FFTcounts'],color='black')
#plt.text(120,188050, r'$\mu=41.5,\ \sigma=2.9$')
#plt.text(120,158050, r'min=28, max=60')
plt.ylabel('numero de pixeles')
plt.xlabel('Valor de pixel [ADU]')



'''
#FFT,FFTcorrido
plt.plot(ivA['Distance_(pixels)'],ivA['noFFT'],marker='.', label='Sin filtro')
plt.plot(ivA['Distance_(pixels)'],ivA['FFT'],marker='.', label='Filtro FFT pasa-altos')
'''



#plt.xlabel('Distancia [pixeles]')
#plt.set_cmap('gray')
#plt.imshow(im1)

plt.show() 
