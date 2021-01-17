#!/usr/bin/env python
# coding: utf-8


import serial
import time
from datetime import date
import datetime
import os
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
#dirname="run_"+str(datetime.datetime.now())
dirname="date_"+str(date.today())+"_run_"+str(st)
print("creating folder "+ dirname +" ...")
os.system("mkdir "+dirname)    
#................................................................................................
arduino = serial.Serial("/dev/ttyACM0",250000)   #NOMBRE DEL PUERTO Y BOUDRATE
time.sleep(2)
#arduino.write(b"M1005\n")               #set units in mm
#arduino.flush()
arduino.write(b"G21\n")                 #set units in mm
arduino.flush()
arduino.write(b"G91\n")                 #G90 absolute posit; G91 relative position
arduino.flush()
arduino.write(b"M121\n")                #M121 disable endstops; M120 to enable
arduino.flush()
arduino.write(b"M92 X70.63 Y50\n")      #steps per mm
arduino.flush()
arduino.write(b"M203 X50 Y300 \n")      #set max feedrate
arduino.flush()
arduino.write(b"G92 X0 Y0\n")          #set current position as 00 (calibrar en el origen del plano)
arduino.flush()
#................................................................................................
#definicion de variables e input
xrange=float(input("ingrese ancho x de muestreo [mm]"))#200
yrange=float(input("ingrese largo y de muestreo[mm]"))#50
pasos=float(input("ingrese pasos de muestreo (numero de imagenes):"))#10

xstep=int(xrange/pasos)
ystep=int(yrange/pasos)
movx='G0 X'+str(xstep) + " \\" +'n'
movy='G0 Y'+str(ystep) + " \\" +'n'
print(movx)



#................................................................................................
#bucles while, zigzag
i=0
arduino.write(b"G0 X-200 Y-50\n")
time.sleep(10)
arduino.flush()
while i<pasos:
    j=0
    i+=1
    while j<pasos:
        j+=1
        #arduino.write(bytes(movx,'utf-8'))
        arduino.write(b"G0 X30 \n") 
        arduino.flush()
        arduino.write(b" M114 \n")
        arduino.flush()
        arduino.write(b" M400 \n")
        arduino.flush()
#arduino.write(b" M280 \n")    #Set or get the position of a servo.
#arduino.flush()
##


#ser_bytes = str(arduino.readline())
        string1="b'echo:busy: processing" + "\\" + "n'"

        string2="b'ok" + "\\" + "n'"

        print(string1)
        arduino.flushInput()

        s =string1

        while True:
            print(s)
            ser_bytes =arduino.readline()
            s=str(ser_bytes)
            arduino.flushInput()
            arduino.flushOutput()
            if s==string2:
                print("saving image...")
                os.system("sudo python take_images.py "+dirname+ "/x" +str(j) +"y" +str(i)+ " 1")
            break
    arduino.flush()    
    #arduino.write(b"G28 X \n") #regresa a x=0
    arduino.write(b"G0 X-200 \n")
    arduino.flush()
    time.sleep(10)
    #arduino.write(bytes(movy,'utf-8'))
    arduino.write(b"G0 Y5 \n")
##
#output=arduino.read(5)
#print(str(output,'utf8'))


time.sleep(10)
#arduino.write(b"G28 X Y \n")             #auto home
#time.sleep(10)
home='G0 X-'+str(xstep) + " Y-" +str(ystep) + " \\" +'n'
arduino.write(bytes(home,'utf-8'))             #
#arduino.write(b"G0 X200 Y20 \n")

time.sleep(15)
arduino.close()
arduino.open()
arduino.close()


# In[17]:


arduino.close()


# In[1]:


string="b'ok" + "\\" + "n'"
#print(ser_bytes)
print(string)


# In[ ]:




