
'''
realiza un procesado del stack de imagenes totales en un directorio;
    para cada posicion x_y_ realiza un promedio con suma_stack(nombre,posicion),
    elimina las imagenes oscuras con eliminar_oscuras(nombre,posicion,stack_sumado)
    usando como umbral el valor medio del promedio del stack.
    luego aplica filtros FFT y realiza un ajuste de iluminacion. 
'''

from astropy.io import fits
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

def suma_stack(nombre,posicion):
    directorio=nombre

    mylist=os.listdir(directorio) #modify to change directory dynamically
    c=len(mylist)
    print("number of files:",len(mylist))
    #suma_fits=fits.open(directorio+"/c2"+posicion+"t1.fits")

    #suma=np.zeros(np.shape(suma_fits[0].data))
    suma=np.zeros((1024, 1280))
    #print(suma)
    cuenta=0
    for i in mylist:

        if posicion in i:
            try:
                #print(i)
                imagen_fits=fits.open(directorio+"/"+str(i))
                imag=imagen_fits[0].data
                #print(np.mean(imag))
                suma=suma+imag
                cuenta+=1
            except:
                pass
    print('numero de imagenes sumadas',cuenta)
    return suma/cuenta  #/cuenta para hacer el promedio

def eliminar_oscuras(nombre,posicion,stack_sumado):
    directorio=nombre
    umbral1=np.mean(stack_sumado)
    print('umbral1',umbral1)
    umbral2=100
    mylist=os.listdir(directorio) #modify to change directory dynamically
    c=len(mylist)
    print("number of files:",len(mylist))
    #suma_fits=fits.open(directorio+"/c2"+posicion+"t1.fits")
    #suma=np.zeros(np.shape(suma_fits[0].data))
    suma=np.zeros((1024, 1280))
    #print('-------------------------------shape shape shape',np.shape(suma_fits[0].data))
    count=0
    for i in mylist:

        if posicion in i:
            try:
                imagen_fits=fits.open(directorio+"/"+str(i))
                imag=imagen_fits[0].data

                if np.count_nonzero(imag > umbral1)>umbral2:
                        #print(i)
                        suma=suma+imag
                        count+=1
            except:
                pass           
    print('numero de imagenes con señal',count)
    return suma

def create_circular_mask(h, w, center=None, radius=None):

    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
    mask=np.zeros((h,w,2),np.float32)
    mask[:,:,0] = dist_from_center <= radius
    mask[:,:,1] = dist_from_center <= radius
    return mask


def low_pass_filter(image,radius):
    data = image
    fft=cv2.dft(np.float32(data),flags=cv2.DFT_COMPLEX_OUTPUT)
    dshift=np.fft.fftshift(fft)
    rows,cols=data.shape[:2]
    mid_row,mid_col=int(rows/2), int(cols/2)
    #mask=np.zeros((rows,cols,2),np.float32)
    #mask[mid_row-radius:mid_row+radius,mid_col-radius:mid_col+radius]=1
    mask=create_circular_mask(rows,cols, center=None, radius=radius)

    fft_filtering=dshift*mask
    mascara=np.array(mask)
    #print(np.shape(mascara))
    #plt.imshow(mask[:,:,1])
    #plt.show()
    ishift=np.fft.ifftshift(fft_filtering)
    image_filtering=cv2.idft(ishift)
    image_filtering=cv2.magnitude(image_filtering[:,:,0],image_filtering[:,:,1])
    cv2.normalize(image_filtering,image_filtering, 0, 256, cv2.NORM_MINMAX)
    return image_filtering


def high_pass_filter(image,radius):
    data = image
    fft=cv2.dft(np.float32(data),flags=cv2.DFT_COMPLEX_OUTPUT)
    dshift=np.fft.fftshift(fft)
    rows,cols=data.shape[:2]
    mid_row,mid_col=int(rows/2), int(cols/2)
    mask=np.ones((rows,cols,2),np.float32)
    mask[mid_row-radius:mid_row+radius,mid_col-radius:mid_col+radius]=0
    fft_filtering=dshift*mask
    mascara=np.array(mask)

    ishift=np.fft.ifftshift(fft_filtering)
    image_filtering=cv2.idft(ishift)
    image_filtering=cv2.magnitude(image_filtering[:,:,0],image_filtering[:,:,1])
    cv2.normalize(image_filtering,image_filtering, 0, 256, cv2.NORM_MINMAX)
    return image_filtering
# Automatic brightness and contrast optimization with optional histogram clipping


def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=image
    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)

def disigmoidScaling(values, steepnessFactor=1, ref=None):
    ''' Sigmoid scaling in which values around a reference point are flattened
    arround a reference point

    Scaled value y is calculated as 
        y = sign(v - d)(1 - exp(-((x - d)/s)**2)))
    where v is the original value,  d is the referenc point and s is the 
    steepness factor
    '''
    if ref is None:
        mn = np.min(values)
        mx = np.max(values)
        ref = mn + (mx - mn) / 2.0

    sgn = np.sign(values - ref)
    term1 = ((values - ref)/steepnessFactor) ** 2
    term2 = np.exp(- term1) 
    term3 = 1.0 - term2 
    return sgn * term3


f=open('ij.txt','r')
valor=f.readlines(0)
xstep=int(valor[0])
ystep=int(valor[1])
directory=valor[3].replace("\n","")



#directory='../2021-09-28_arandelaxplastico_run_116'
if os.path.isdir(directory+'FFT')==False:
    os.mkdir(directory+'FFT')


import matplotlib


#xstep=1
#ystep=1

for iy in range (1,ystep+1):
    for ix in range(1,xstep+1):    
        print(ix,iy)
        posit='x'+str(ix)+'y'+str(iy)
        sumatoria=suma_stack(directory,posit)
        suma_sin_oscuras=eliminar_oscuras(directory,posit,sumatoria)
        imagen=low_pass_filter(suma_sin_oscuras,77)
        #imagen=high_pass_filter(suma_sin_oscuras,100)

        auto_result, alpha, beta = automatic_brightness_and_contrast(imagen)


        scale_percent = 70 # percent of original size
        width = int(auto_result.shape[1] * scale_percent / 100)
        height = int(auto_result.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(auto_result, dim, interpolation = cv2.INTER_NEAREST)
        #damped=disigmoidScaling(resized, 1.5)
        plt.imsave(directory+'FFT/'+posit+'.jpg',resized,format='jpg',cmap="Greys_r")   #my_cmap


'''
ig=cv2.imread('run91_2.jpg')
cmap = plt.get_cmap('jet')

rgba_img = cmap(ig)
#plt.imshow(rgba_img[:,:,1,1], cmap=my_cmap)
#plt.show()
plt.imsave('run91.jpg',rgba_img[:,:,1,1],format='jpg',cmap=my_cmap)
'''