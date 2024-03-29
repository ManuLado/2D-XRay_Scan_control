import serial
import time
from datetime import date
import datetime
import os
import sys
import RPi.GPIO as gpio
from multiprocessing import Process
import numpy as np
import subprocess


peso=1.3 #Mb
noitt = 16              #numero de imagenes en cada exposicion
capturasxposicion = 5   #numero de exposiciones en cada posicion
steps_per_mm = 19.685   #steps/mm
sensor_size_x = 6.66/2  #mm
sensor_size_y = 5.32/1.5  #mm

#valores para el sensor
frec = 50 #Hz    
integrationTime = 1/frec*10**3 #ms
rowTime = (1280+244+9-19)
clockPeriod = 1000.0/24e6; #[ms]
overheadTime = 180
resetDelay = 0

def buzzer(pin,duracion):
    gpio.setup(pin,gpio.OUT)
    gpio.setwarnings(False)
    gpio.output(pin,False)
    for i in range(1,duracion):
        gpio.output(pin,True)
        time.sleep(0.25)
        gpio.output(pin,False)
        time.sleep(0.25)

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


def tomaimagen(): #esta funcion y tubo() van sin argumentos para el multiprocess
    print("tomando imagen")
    global i
    global j
    global h
    
    os.system("sudo python take_images.py "+dirname+ "/c"+str(h)+"x" +str(j) +"y" +str(i)+'t'+" "+str(noitt))
    #image_name="dirname"+ "/c"+str(h)+"x" +str(j) +"y" +str(i)+'t'
    #proc = subprocess.Popen(['sudo', 'python', 'take_images.py',image_name,str(noitt)], stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    #tomaimagen.camera_output_string=proc.communicate()
    
def check_camera(i,j,h,dirname):
    
    if os.path.exists(dirname+ "/c"+str(h)+"x" +str(j) +"y" +str(i)+'t'+"10.fits"):
        return True
    else:
        return False
    
    
from astropy.io import fits
def check_tubo(i,j,h,dirname):
    imagen_fits=fits.open(dirname+ "/c"+str(h)+"x" +str(j) +"y" +str(i)+'t'+"10.fits")
    imag=imagen_fits[0].data
    if np.count_nonzero(imag > np.mean(100))>100:
        #print('el tubo se encendio correctamente') 
        return True
    else:
        return False



def tubo():
    time.sleep(3)
    print("prende tubo")
    print('\x1b[6;30;43m'+"!!!WARNING: X-RAYs ON!!!"+'\x1b[0m')
    gpio.output(10,False)
    time.sleep(3)
    print("apaga tubo")
    gpio.output(10,True)    #es un rele NORMAL ABIERTO
    print('\x1b[7;37;42m'+"X-RAYs OFF"+'\x1b[0m')
    
def usb_reset():
    os.system('sudo sh -c "echo 0 > /sys/bus/usb/devices/usb1/authorized"')
    os.system('sudo sh -c "echo 1 > /sys/bus/usb/devices/usb1/authorized"')
    

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



xrange=float(input("<<<<ingrese ancho x de muestreo [mm]>>>>"))

yrange=float(input("<<<<ingrese largo y de muestreo[mm]>>>>"))

pasox=round(steps_per_mm*sensor_size_x)
pasoy=round(steps_per_mm*sensor_size_y)

print('....................................................................................')
xstep=round(steps_per_mm*xrange/pasox)
ystep=round(steps_per_mm*yrange/pasoy)
#xstep=1
#ystep=1


duracion_estimada=round(xstep*ystep*capturasxposicion*46/60,2) #minutos
espacio_estimado=round(peso*xstep*ystep*capturasxposicion*noitt,2) #Mb
print('xstep:',xstep)
print('ystep:',ystep)
print('duracion estimada:',duracion_estimada,'minutos ( ',duracion_estimada/60,' horas)')
print('se necesitan:',espacio_estimado,'Mb ( ',espacio_estimado/1024,' Gb) de espacio en disco')
import shutil
total, used, free = shutil.disk_usage("/")
print("Total: %d GiB" % (total // (2**30)))
print("Used: %d GiB" % (used // (2**30)))
print("Free: %d GiB" % (free // (2**30)))
free_space=(free // (2**30))
if espacio_estimado/1024> free_space:
    print('el espacio libre en disco es de ',free_space,'Gb')
    print('no hay suficiente espacio en el disco!')
    exit()

matrix=np.zeros((ystep,xstep))
print('x-->')
print('y')
print('|')
print('v')
print(matrix)

print('....................................................................................')
input("press enter")
dirname=str(date.today())+"_"+str(samplename)+"_run_"+str(st)
print("creating folder "+ dirname +" ...")
os.system("mkdir "+dirname)
star_time=time.time()

print('\33[33m'+"iniciando...  "+'\x1b[0m')




integrationPeriods =integrationTime/ clockPeriod #[ms]

shutterWidth=int((integrationPeriods + overheadTime + resetDelay)/rowTime)

valorReg9_hex = '0x' + hex(shutterWidth)[2:].zfill(4).upper()
print("---------------------------------shutterWidth:",valorReg9_hex)
replace_line('take_images.py', 86, '    [0x09, '+str(valorReg9_hex)+'], # Shutter Width 0x0419 (max: 0x3FFF) \n')

#///////////////////////////////// el pin del rele que activa el tubo es el GPIO 10 !!!
gpio.setmode(gpio.BOARD)
gpio.setup(10,gpio.OUT)
gpio.setwarnings(False)
gpio.output(10,True)            #es un rele NORMAL ABIERTO

print('\33[101m'+"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒INICIANDO TUBO DE RAYOS X... ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ "+'\x1b[0m')
print('\33[101m'+"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒Mantenga la distancia!!      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"+'\x1b[0m')
time.sleep(7)
#os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -H")
#os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 500")
time.sleep(5)
camera_fail=0
tubo_fail=0
for i in range(1,ystep+1):
    for j in range(1,xstep+1):

        for h in range(1,capturasxposicion+1):
            while True:
                                                        
                try:
                    p1 = Process(target=tomaimagen)
                    p1.start()
                    p2 = Process(target=tubo)
                    p2.start()
                    
                    
                    
                    time.sleep(40)

                    if check_camera(i,j,h,dirname)==False:
                        print('camera failure: intentando de nuevo...')
                        camera_fail+=1
                        usb_reset()
                        time.sleep(5)
                    
                    else:
                        print('camera success!')
                        
                        if check_tubo(i,j,h,dirname)==False:
                            tubo_fail+=1
                            print('fallo el tubo: intentando de nuevo...')
                            time.sleep(3)
                            
                        if check_tubo(i,j,h,dirname)==True:
                            print('La camara y el tubo funcionaron correctamente')                         
                            time.sleep(3)
                            break
                        
                
                except KeyboardInterrupt:
                    print ('\nPausing...  (Hit ENTER to continue, type quit to exit.)')
                    try:
                        response = input()
                        if response == 'quit':
                            break
                        print ('Resuming...')
                    except KeyboardInterrupt:
                        print ('Resuming...')
                        continue
                    

                
            matrix[i-1,j-1]=h
            print(matrix)


            sys.stdout.write("va por la captura "+str(h)+" de "+str(capturasxposicion))
            sys.stdout.flush()

        os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m "+str(pasox)+":0")
        print("stoped")
    return_val=-pasox*(xstep)
    os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 0:"+str(pasoy))
    os.system("python3 engraver.py -d /dev/ttyUSB0 --no-fan -m "+str(return_val))
        
        
print('\x1b[7;37;42m'+"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒X-RAYs OFF          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"+'\x1b[0m')
print('\x1b[7;37;42m'+"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒Escaneo finalizado  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"+'\x1b[0m')
time.sleep(10)

c=len(os.listdir(dirname))
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

with open('ij.txt','w') as h:
    h.write(str(xstep)+"\n")
    h.write(str(ystep)+"\n")
    h.write(str(noitt)+"\n")
    h.write(dirname+"\n")

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
    f.write('cantidad de imagenes promediadas por posicion: '+str(noitt)+"\n")
    f.write('runtime----'+str(time.time()-star_time)+' seconds ----'+"\n")
    f.write('frecuencia de muestreo [Hz]: '+str(frec)+"\n")
    f.write('numero de imagenes por captura: '+str(noitt)+"\n")
    f.write('numero capturas por posicion: '+str(capturasxposicion)+"\n")
    f.write('veces que fallo la camara: '+str(camera_fail)+"\n")
    f.write('veces que fallo el tubo: '+str(tubo_fail)+"\n")
    f.write('-----------valores de los registros en take_images.py----------- '+"\n")
    for p in range(79,112):
        f.write(str(content[p])+"\n")
        
print("log file saved as log.txt")
print('runtime----'+str(time.time()-star_time)+' seconds ----')

buzzer(11,10)
print('...finished')