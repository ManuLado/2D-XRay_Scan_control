import cv2
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()

dire=args.echo

lista=os.listdir(dire)

os.system("mkdir "+dire+'_P5')

dimensionx=3 #(numero de pasos en x) + 1
dimensiony=3 #(numero de pasos en y) + 1


stitcher=cv2.createStitcher(cv2.Stitcher_SCANS)
stitcher.setPanoConfidenceThresh(0.0) # might be too aggressive for real examples

matrix=[]

for j in range(1,dimensionx):
    images=[]
    for i in range(1,dimensiony):
        print(j,i)

        im=cv2.imread(dire+"/"+str(j)+str(i)+'.jpg') #chekear protocolo de nombre de imagenes
        images.append(im)
        
    (status,mat)=stitcher.stitch((images))
    cv2.imwrite(dire+'_P5/'+str(j)+".jpg", mat)
    matt=cv2.imread(dire+'_P5/'+str(j)+".jpg")
    matrix.append(matt)
    print(status)

(status,result)=stitcher.stitch((matrix))
cv2.imwrite(dire+'_P5/'+"P5.jpg", result)

