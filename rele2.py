
import serial
import time
from datetime import date
import datetime
import os
import sys
import RPi.GPIO as gpio
from multiprocessing import Process
import fits2jpeg
import numpy as np
#/////////////////////////////////
if not os.path.exists('logdir.txt'):
    with open('logdir.txt','w') as f:
        f.write('0')
with open('logdir.txt','r') as f:
    st = int(f.read())
    st+=1 
with open('logdir.txt','w') as f:
    f.write(str(st))
#////////////////////////////////
samplename=input("Nombre de muestra:>>>")
objetivo=input("Objetivo:>>>")

dirname="../"+str(date.today())+"_"+str(samplename)+"_run_"+str(st)
print("creating folder "+ dirname +" ...")
os.system("mkdir "+dirname)


#................................................................................................
xrange=float(input("<<<<ingrese ancho x de muestreo [mm]>>>>"))
yrange=float(input("<<<<ingrese largo y de muestreo[mm]>>>>"))
#pasos=float(input("<<<<ingrese pasos de muestreo>>>>:"))

steps_per_mm=19.685 #steps/mm
sensor_size_x=6.66/2  #mm
sensor_size_y=5.32/2  #mm
#pasox=70   #estos tienen que ser h/y
#pasoy=70  #                      v/2


pasox=round(steps_per_mm*sensor_size_x)
pasoy=round(steps_per_mm*sensor_size_y)


print('....................................................................................')
xstep=round(steps_per_mm*xrange/pasox)
ystep=round(steps_per_mm*yrange/pasoy)
#xstep=1
#ystep=1

matrix=np.zeros((ystep,xstep))
print('                       x-->')
print('                       y')
print('                       |')
print('                       v')
print(matrix)

print('....................................................................................')
input("press enter")

star_time=time.time()
 #numberofimagestotake
print('\33[33m'+"iniciando...  "+'\x1b[0m')

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


def tomaimagen():
    print("tomando imagen")
    #global k
    global i
    global j
    global h
    #os.system("sudo python take_images.py prueba2/rana_Shuterwidth_offset11F_"+str(k)+"_ 20")
    os.system("sudo python take_images.py "+dirname+ "/c"+str(h)+"x" +str(j) +"y" +str(i)+'t'+" "+str(noitt))
    
    
def tubo():
    time.sleep(3)
    print("prende tubo")
    print('\x1b[6;30;43m'+"!!!WARNING: X-RAYs ON!!!"+'\x1b[0m')
    gpio.output(10,False)
    time.sleep(3)
    print("apaga tubo")
    gpio.output(10,True)
    print('\x1b[7;37;42m'+"X-RAYs OFF"+'\x1b[0m')
#valores para el sensor
frec=50 #Hz    
integrationTime=1/frec*10**3 #ms
rowTime=(1280+244+9-19)
clockPeriod = 1000.0/24e6; #[ms]
overheadTime = 180
resetDelay=0

integrationPeriods =integrationTime/ clockPeriod #[ms]

shutterWidth=int((integrationPeriods + overheadTime + resetDelay)/rowTime)

valorReg9_hex = '0x' + hex(shutterWidth)[2:].zfill(4).upper()
print("---------------------------------shutterWidth:",valorReg9_hex)
replace_line('take_images.py', 86, '    [0x09, '+str(valorReg9_hex)+'], # Shutter Width 0x0419 (max: 0x3FFF) \n')

#///////////////////////////////// puerto 10!!!
gpio.setmode(gpio.BOARD)
gpio.setup(10,gpio.OUT)
gpio.setwarnings(False)
gpio.output(10,True)

#os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -v -H")
print('\33[31m'+"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒INICIANDO TUBO DE RAYOS X... ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ "+'\x1b[0m')
print('\33[31m'+"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒Mantenga la distancia!!      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"+'\x1b[0m')
time.sleep(7)
k=0
i=0
loop=4
j=0
noitt=16
capturasxposicion=5




#ystep=1
#xstep=1

#os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -H")
#os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 500")
time.sleep(5)



for i in range(1,ystep+1):
    for j in range(1,xstep+1):
        #i+=1
        k+=1
        os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m "+str(pasox)+":0")
        #os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 50:0")
        print("stoped")
        for h in range(1,capturasxposicion+1):
            
            try:
              p1 = Process(target=tomaimagen)
              p1.start()
              p2 = Process(target=tubo)
              p2.start()
            except:
              print ('error')
              
            matrix[i-1,j-1]=h
            print(matrix)
            
            time.sleep(43)
            sys.stdout.write("va por la captura "+str(h)+" de "+str(capturasxposicion))
            sys.stdout.flush()
            

            
    return_val=-pasox*(xstep+1)
    os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 0:"+str(pasoy))
    os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m "+str(return_val))
    #os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 0:50")



#os.system("python3 engraver.py -d /dev/ttyUSB3 --no-fan -v -H")
print("termino")
print('\x1b[7;37;42m'+"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒X-RAYs OFF          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"+'\x1b[0m')
print('\x1b[7;37;42m'+"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒Escaneo finalizado  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"+'\x1b[0m')
time.sleep(10)


c=len(os.listdir(dirname))

'''
print("===============================================================")
print("converting .fits to .png ...........")
print("===============================================================")
import fits2jpeg

fits2jpeg.directory_name(dirname)
'''

# ----------------------------------------------------write logfile

tkimgs=open('take_images.py')


content = tkimgs.readlines()

ct86=content[86]
ct86=ct86.replace(", # Shutter Width 0x0419 (max: 0x3FFF)"," pp")
ct86=ct86.replace("0x09"," **")
ct86=ct86.lstrip("[ **, ")
ct86=ct86.replace("] pp","")

ct97=content[97]
ct97=ct97.replace(", # Global Gain 0x0008 (max: 0x0067)"," pp")
ct97=ct97.replace("0x35"," **")
ct97=ct97.lstrip("[ **, ")
ct97=ct97.replace("] pp","")

itt=open('integrationtime.txt')
content2 = itt.readlines()



#//////////////////////////////////AVERAGING IMG1*alfa+IMAG2*beta+gamma cv2.addWeighted(IMG1,alfa,IMAG2,beta,gamma)
#os.system("mkdir "+dirname+"/averaged")
print('performing Stack Averaging of ',noitt,'images per position')
with open('ij.txt','w') as h:
    h.write(str(xstep)+"\n")
    h.write(str(ystep)+"\n")
    h.write(str(noitt)+"\n")
    h.write(dirname+"\n")

#import average

#os.system("sudo python3 average.py")
'''
import cv2


peso=1
i=0


while i<xstep:
    j=0
    i+=1
    while j<ystep:
        j+=1
        k=3
        path1=dirname+'/x1y1t1.png'
        imagen=cv2.imread(path1)
        im=np.zeros(imagen.shape)
        #im=0
        while k<noitt-1:
            k+=1
            path=dirname+'/x'+str(j)+'y'+str(i)+'t'+str(k)+'.png'
            if os.path.exists(path):
                im2=cv2.imread(path)            
                im2=np.array(im2)
                im=np.add(im2,im) #si uso esta linea inicializar con im=np.zeros(imagen.shape)
                print(path,"--listo")
        cv2.imwrite(dirname+'/averaged/x'+str(j)+'y'+str(i)+'.png',im)


'''
print('images saved in folder '+dirname+'/averaged')
#////////////////////////////////////////////////////////////////////////////////////////


with open(str(dirname)+'/log.txt','w') as f:
    f.write('Directorio: '+str(dirname)+"\n")
    f.write('Fecha: '+str(date.today())+"\n")
    f.write('Nombre de muestra: '+str(samplename)+"\n")
    f.write('Objetivo: '+str(objetivo)+"\n")
    f.write('Numero de imagenes tomadas: '+str(c)+"\n")
    f.write('----------Parametros del sensor------------- '+"\n")
    f.write('Distancia focal: 2 cm'+"\n")
    
    f.write('Ancho del sensor: '+str(content[43])+"\n")
    f.write('Alto del sensor: '+str(content[44])+"\n")
    f.write('Ancho del obturador: '+str(int(ct86, 16))+"\n")
    f.write('Ganancia global: '+str(int(ct97, 16))+"\n")
    f.write('Tiempo de integracion [ms]: '+str(content2[0])+"\n")
    
    f.write('----------Parametros de muestreo------------- '+"\n")
    f.write('ancho x de muestreo [mm]: '+str(xrange)+"\n")
    f.write('alto y de muestreo [mm]: '+str(yrange)+"\n")
    
    f.write('pasos x de muestreo : '+str(xstep)+"\n")
    f.write('pasos y de muestreo : '+str(ystep)+"\n")
    
    
    #f.write('pasos: '+str(pasos)+"\n")
    f.write('cantidad de imagenes promediadas por posicion: '+str(noitt)+"\n")
    f.write('runtime----'+str(time.time()-star_time)+' seconds ----'+"\n")
    f.write('frecuencia de muestreo [Hz]: '+str(frec)+"\n")
    f.write('numero de imagenes por captura: '+str(noitt)+"\n")
    f.write('numero capturas por posicion: '+str(capturasxposicion)+"\n")
    
    f.write('-----------valores de los registros en take_images.py----------- '+"\n")
    for p in range(79,112):
        f.write(str(content[p])+"\n")
        
print("log file saved as log.txt")
print('runtime----'+str(time.time()-star_time)+' seconds ----')


gpio.setup(3,gpio.OUT)
gpio.setwarnings(False)
gpio.output(3,False)
for i in range(1,10):
    gpio.output(3,True)
    time.sleep(0.25)
    gpio.output(3,False)
    time.sleep(0.25)
    
#//////////////////////////////////Stitching P0;P1;P2;P3;P4

#print('performing STITCHING of images in'+dirname+'/averaged')

                    
#os.system("sudo python3 RUNPANO.py "+dirname+'/averaged')

#print('images saved in folders '+dirname+'/averaged_P0;P1;P2;P3;P4')
#////////////////////////////////////////////////////////////////////////////////////////
#os.system("sudo python3 procesado.py")