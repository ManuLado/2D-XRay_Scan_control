import cv2
import os

'''
#script que une imagenes. modificar para que una consecutivamente las que tomo en cada fila y luego para que una las filas entre si
#stitcher = cv2.createStitcher(cv2.Stitcher_SCANS)
stitch = cv2.createStitcher()
stitch.setPanoConfidenceThresh(0.0) # might be too aggressive for real examples
cv2.ocl.setUseOpenCL(False)

i1=cv2.imread("x1y2.jpeg")

i2=cv2.imread("x1y1.jpeg")
i3=cv2.imread("x2y2.jpeg")


resultado=stitch.stitch(i3,i1)



cv2.imwrite("resultado.jpg",resultado[1])

'''
lista=os.listdir("1")
#"Images/1/"+
images=[]
j=0
for i in lista:
    print(i)
    im=cv2.imread("1/"+str(i))
    im=cv2.resize(im,(0,0),None,0.1,0.1)
    images.append(im)
    
print('total number of files:',len(images))



stitcher=cv2.createStitcher(cv2.Stitcher_SCANS)
stitcher = cv2.createStitcher()
stitcher.setPanoConfidenceThresh(0.0) # might be too aggressive for real examples
cv2.ocl.setUseOpenCL(False)
(status,result)=stitcher.stitch(images)
if (status==cv2.STITCHER_OK):
    print("pano created")
    cv2.imwrite("result.png", result)
else:
    ("no pano")
    
'''
for j in [0,len(images)]:
    if result[0]==True:
        result=stitcher.stitch((images[j],images[j+1])) #modificar esto para unir segun nombre
        cv2.imwrite("result"+str(j)+".png", result[1])
        
    else:
        print("no paso nada")
'''
