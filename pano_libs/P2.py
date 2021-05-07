import cv2
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()

dire=args.echo


lista=os.listdir(dire)

stitcher=cv2.createStitcher(cv2.Stitcher_SCANS)
stitcher.setPanoConfidenceThresh(0.0) # might be too aggressive for real examples
cv2.ocl.setUseOpenCL(False)

images=[]

for i in lista:
    print(i)
    im=cv2.imread(dire+"/"+str(i))
    #im=cv2.resize(im,(0,0),None,0.1,0.1)
    images.append(im)


(status,result)=stitcher.stitch((images))



if (status==cv2.STITCHER_OK):
    print("pano created")
    cv2.imwrite('P2_'+dire+".png", result)
else:
    ("no pano")