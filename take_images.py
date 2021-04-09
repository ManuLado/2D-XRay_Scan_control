#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Graba video leido desde la arducam
# Se le debe indicar el archivo de video a grabar y
# la duración de la captura en segundos.

# SINTAXIS: python capturar_video.py VIDEO TIEMPO
#   1- Ruta del video
#   2- Tiempo de grabacion en segundos

from ctypes import *

import ctypes

import sys
import os

import time
from PIL import Image
import numpy as np
import thread as thread
import math

from select import select
from evdev import InputDevice
from evdev import ecodes
from astropy.io import fits
import ArducamSDK

# Analisis de argumentos
if (len(sys.argv)==3):
    NOMBREIMG = sys.argv[1];
    NUMIMG = int(sys.argv[2]);
else:
    print ("Se requieren 2 argumentos: NOMBRE_IMAGENES NUMERO_IMAGENES")
    exit()

#### CONFIGURACION ARDUCAMSDK ################
COLOR_BYTE2RGB = 47 # No se modifico del original
CAMERA_MT9M001 = 0x4D091031 # No se modifico del original
SensorShipAddr = 186
I2C_MODE_8_16  = 1
usbVid = 0x52CB # No se modifico del original
Width = 1280 #1280
Height = 1024 #1024
cfg ={"u32CameraType":CAMERA_MT9M001,
      "u32Width":Width,"u32Height":Height,
      "u32UsbVersion":1,
      "u8PixelBytes":1,
      "u16Vid":0x52cb,
      "u8PixelBits":8,
      "u32SensorShipAddr":SensorShipAddr,
      "emI2cMode":I2C_MODE_8_16 }

# FLAGS
global saveFlag,downFlag,flag,H_value,V_value,lx,ly,mx,my,dx,dy,W_zoom,H_zooM,handle,openFlag,initTime,storeFlag,bufferData,globalGain
global testPatternFlag
global integrationTime
global shutterWidth

openFlag = False
handle = {}
downFlag = False
flag = True
saveFlag = False
storeFlag = False
saveNum=0
H_value = 0
V_value = 0
W_zoom = 0
H_zoom = 0
lx = 0
ly = 0
mx = 0
my = 0
dx = 0
dy = 0
testPatternFlag = False;

regArr=[[0x01, 0x000C], # Row Start
    [0x02, 0x0014], # Column Start
    [0x03, Height - 1], # Window Height 0x03FF
    [0x04, Width - 1], # Window Width 0x04FF
    [0x05, 0x0009], # Horizontal Blanking
    [0x06, 0x0019], # Vertical Blanking
    [0x07, 0x0002], # Output Control
    [0x09, 0x0419], # Shutter Width 0x0419 (max: 0x3FFF)
    [0x0B, 0x0000], # Frame Restart
    [0x0C, 0x0000],#0x0100], 
    [0x0D, 0x0000], 
    [0x1E, 0x8000], # Read Mode 1 0x8000
    [0x20, 0x1104], 
    [0x2B, 0x0008], 
    [0x2C, 0x0008], 
    [0x2D, 0x0008], 
    [0x2E, 0x0008],
    [0x32, 0x0FFC], # Test Data Register
    [0x35, 0x0067], # Global Gain 0x0008 (max: 0x0067)
    [0x5F, 0x0904], 
    #[0x60, 0x0000], # BLC offset: Even row, even column
    #[0x61, 0x0000], # BLC offset: Odd row, odd column
    #[0x62, 0x049F], # Black Level Calibration Control 0x0498 (No-BLC: 0x049F; Manual-BLC: 0x0499 & reg0x60/61/63/64)
    #[0x63, 0x0000], # BLC offset: Even row, odd column
    #[0x64, 0x0000], # BLC offset: Odd row, Even column
    [0x60, 0x002F], # BLC offset: Even row, even column
    [0x61, 0x002F], # BLC offset: Odd row, odd column
    [0x62, 0x0499], # Black Level Calibration Control 0x0498 (No-BLC: 0x049F; Manual-BLC: 0x0499 & reg0x60/61/63/64)
    [0x63, 0x000F], # BLC offset: Even row, odd column
    [0x64, 0x000F], # BLC offset: Odd row, Even column
    [0xF1, 0x0001], 
    [0xFFFF, 0xFFFF]
]

globalGain = regArr[18][1];

# Cálculo del tiempo de integración inicial (pag 16 del datasheet)
rowTime = regArr[3][1] + 1 + 244 + regArr[4][1] - 19; #[pixel clock periods] default: 1514
resetDelay = 4*regArr[9][1] #[pixel clock periods] default: 0
overheadTime = 180; #[pixel clock periods]
shutterWidth = regArr[7][1]
integrationPeriods = shutterWidth*rowTime - overheadTime - resetDelay;
clockPeriod = 1000.0/24e6; #[ms]
integrationTime = integrationPeriods * clockPeriod; #[ms]
with open('integrationtime.txt','w') as it:
    it.write(str(integrationTime)+"\n")

print ("Initial integration time: %.3fms"%(integrationTime));
print ("Initial gain: 0x%02x"%(globalGain));

a_lock = thread.allocate_lock();

def readThread(threadName,read_Flag):
    global flag,handle,storeFlag,bufferData,openFlag
    global a_lock
    count = 0
    time0 = time.time()
    time1 = time.time()
    data = {}
    # Wait for the arducam object to be ready
    while openFlag == False:
        time1 = time.time();
        if time1 - time0 > 20:
            #timeout
            exit;

    while flag:
        res = ArducamSDK.Py_ArduCam_available(handle)
        #~ print "Available frames %d"%(res)
        if res > 0:
            
            res,data = ArducamSDK.Py_ArduCam_read(handle,Width * Height)
            if res == 0:
                count += 1
                time1 = time.time()
                ArducamSDK.Py_ArduCam_del(handle)
            else:
                print ("read data fail!")
            
        else:
            #print "No data availiable"
            time.sleep(.01);
        
        if len(data) >= Width * Height:
            if time1 - time0 >= 5:
                print ("%s %f %s\n"%("fps:",count*1.0/(time1-time0),"/s"))
                count = 0
                time0 = time1
            
            a_lock.acquire();
            bufferData = data;
            data = [];
            storeFlag = True;
            a_lock.release();
            #show(data)
		#else:
		#	print "data length is not enough!"
        if flag == False:
            break
    
thread.start_new_thread( readThread,("Thread-2", flag,))

pass

def showAndSave(threadName,algoquenoseusa):
    global flag,W_zoom,H_zoom,V_value,H_value,lx,ly,downFlag,saveFlag,saveNum,bufferData,storeFlag
    global a_lock
    global hist_ax
    global NOMBREIMG
    img = np.zeros((Height, Width), dtype=np.uint8);
    while flag:
        a_lock.acquire();
        if storeFlag == True:
            storeFlag = False;
            img = np.frombuffer(bufferData, np.uint8)
            img = np.reshape(img, (Height, Width));

            saveNum += 1
            #name = NOMBREIMG + str(saveNum) + ".fits"
	    #name = NOMBREIMG + "_" + str(saveNum) + ".jpeg"
            name = NOMBREIMG + ".fits"
            hdu=fits.PrimaryHDU()
            hdu.data=img
            hdu.writeto(name,overwrite=True)
            print ("Frame saved to %s"%(name))
                
        a_lock.release();
                
        if saveNum == NUMIMG:
            flag=False;
            print ("Total number of adq images = %d"%(saveNum))
        
        if flag == False:
            break
thread.start_new_thread( showAndSave,("Thread-3",flag))
pass

def init_and_read_arducam():
	global flag,regArr,handle,openFlag
	regNum = 0
	res,handle = ArducamSDK.Py_ArduCam_autoopen(cfg)
	if res == 0:
		openFlag = True
		print ("device open success!")
		while (regArr[regNum][0] != 0xFFFF):
			ArducamSDK.Py_ArduCam_writeSensorReg(handle,regArr[regNum][0],regArr[regNum][1])
			regNum = regNum + 1
		res = ArducamSDK.Py_ArduCam_beginCapture(handle)
		
		if res == 0:
			print ("transfer task create success!")
			while flag :		
				res = ArducamSDK.Py_ArduCam_capture(handle)
				if res != 0:
					print ("capture failed!")
					flag = False;
					break;					
				time.sleep(0.1)
				if flag == False:		
					break
		else:
			print ("transfer task create fail!")
		
		time.sleep(2);
		res = ArducamSDK.Py_ArduCam_close(handle)
		if res == 0:
			openFlag = False
			print ("device close success!")
		else:
			print ("device close fail!")
	else:
		print ("device open fail!")

if __name__ == "__main__":
	initTime = time.time();
	init_and_read_arducam();

