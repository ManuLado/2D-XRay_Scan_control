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

images=[]
results=[]
j=0
for i in lista:
    print(i)
    im=cv2.imread(dire+"/"+str(i))
    #im=cv2.resize(im,(0,0),None,0.1,0.1)
    images.append(im)
    result=images[0]
    if j!=0:
        (status,result)=stitcher.stitch((images[j-1],images[j]))
        results.append(result)
    j+=1        


#cv2.imwrite('result'+dire+".png", result)
#result=images[0]



#cv2.ocl.setUseOpenCL(False)

(status,result)=stitcher.stitch(results)
if (status==cv2.STITCHER_OK):
    print("pano created")
    cv2.imwrite('P1_'+dire+"panoramic.png", result)
else:
    ("no pano")
    
