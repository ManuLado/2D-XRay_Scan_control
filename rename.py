#change directory list files format form .tif to .jpg  
import os
import cv2
from PIL import Image
path='.' 
lista=os.listdir(path) 
for i in lista: 
	print(i) 
	#img=cv2.imread(i,cv2.IMREAD_GRAYSCALE) 
	im=Image.open(i)
	newname=i.replace('tif','jpg') 
	print(newname,'.....................') 
	#cv2.imwrite(newname,img,[int(cv2.IMWRITE_JPEG_QUALITY), 200])
	out = im.convert("RGB")
	out.save(newname, "JPEG", quality=90)