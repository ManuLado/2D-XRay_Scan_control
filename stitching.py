import cv2
import os
#script que une imagenes. modificar para que una consecutivamente las que tomo en cada fila y luego para que una las filas entre si

stitcher = cv2.createStitcher(cv2.Stitcher_SCANS)
stitcher.setPanoConfidenceThresh(0.0) # might be too aggressive for real examples
list=os.listdir('Images\\1')
images=[]
j=0
for i in list:
    #print(i)
    im=cv2.imread('Images\\1\\'+str(i))
    images.append(im)

for i in list:
    result=stitcher.stitch((images[j],images[j+1])) #modificar esto para unir segun nombre
    cv2.imwrite("result"+str(j)+".jpg", result[1])
    j+=1
