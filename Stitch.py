#!/usr/bin/env python
# coding: utf-8

import cv2  #opencv library
import numpy as np

dimensionx=4
dimensiony=5

matriz=[]

for i in range(1,dimensiony+1):
    fila=[]*dimension
    for j in range(1,dimensionx+1):  
    
        name=str(i)+"-"+str(j)+".png"
        img=cv2.imread(name)
        if j==1:
            fila= img
            
        else:
            fila=np.hstack((fila, img))
    if i==1:
        matriz=fila
    else:    
        matriz=np.vstack((matriz,fila))
        
# Using cv2.cvtColor() method 
# Using cv2.COLOR_BGR2GRAY color space 
# conversion code         
#matriz=cv2.cvtColor(matriz, cv2.COLOR_BGR2HSV )  
#matriz=cv2.cvtColor(matriz, cv2.COLOR_BGR2YCrCb  )  



cv2.imshow("1",matriz)
cv2.waitKey()
cv2.destroyAllWindows()

cv2.imwrite('result.png',matriz)


# In[ ]:




