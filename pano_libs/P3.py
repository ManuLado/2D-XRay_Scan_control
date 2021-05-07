import cv2
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()

dire=args.echo

lista=os.listdir(dire)

os.system("mkdir "+dire+'_P3')

dimensionx=4 #(numero de pasos en x) + 1
dimensiony=5 #(numero de pasos en y) + 1


stitcher=cv2.createStitcher(cv2.Stitcher_SCANS)
stitcher.setPanoConfidenceThresh(0.0) # might be too aggressive for real examples



for j in range(1,dimensionx):
    images=[]
    for i in range(1,dimensiony):
        print(i)

        im=cv2.imread(dire+"/"+str(j)+str(i)+'.jpg') #chekear protocolo de nombre de imagenes
        images.append(im)


    result=images[1]

    for k in range(2,dimensiony-1):
        print(k)
        (status,result)=stitcher.stitch((images[k],result))
        cv2.imwrite(dire+'_P3/'+str(j)+".jpg", result)
