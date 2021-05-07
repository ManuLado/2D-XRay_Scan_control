import cv2
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()

dire=args.echo

lista=os.listdir(dire)


dimensiony=5

stitcher=cv2.createStitcher(cv2.Stitcher_SCANS)
stitcher.setPanoConfidenceThresh(0.0) # might be too aggressive for real examples

os.system("mkdir "+dire+'_P4')


images=[]
for i in range(1,dimensiony):
    print(i)

    im=cv2.imread(dire+"_P3/"+str(i)+'.jpg')
    images.append(im)
    #if !=
    #(status,result)=stitcher.stitch((images[i-1],images[i]))
    #cv2.imwrite('14'+"/"+"result.jpg", result)


result=images[0]
for k in range(2,dimensiony):
    print(k)
    (status,result)=stitcher.stitch((images[k],result))
    cv2.imwrite(dire+'_P4/'+"result.jpg", result)
