import cv2
import numpy as np
#from MaskUtils import *
import argparse
from FileMan import secureDel, FILE_TYPE, printLog


def wrDist(h) :
  with open('dist.txt','a') as f :
    f.write(str(h)+'\n')



def calculEdges(image,echo=True) :

  img=image.copy()
  cntList=[]
  txtLines=[]
  conflict=[]
  rows,cols=img.shape

  # convert the grayscale image to binary image
  ret,thresh = cv2.threshold(img,127,255,0)


  # find contour in the binary image
  contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  if echo :
    printLog("nb contours : ", len(contours))

  for c in contours :
    x,y,w,h = cv2.boundingRect(c)
    line1=((0,y),(cols,y))
    line2=((0,y+h),(cols,y+h))
    txtLines.append((line1,line2))
    wrDist(h)
#    img=cv2.rectangle(img,(0,y),(cols,y+h),(0,255,0),2)
  if echo :
    printLog("number of lines : ", len(txtLines))
  txtLines.sort(key=lambda x : x[0][0][1])
  return txtLines





def erodInvert(img,ks1=(20,200),ks2=(5,100),
      invName="inverted.jpg") :
    img_not = img.copy()


    kernel = np.ones(ks1,np.uint8)
    img_not = cv2.erode(img_not,kernel,iterations = 1)


    img_not = cv2.bitwise_not(img_not)

#    kernel = np.ones(ks2,np.uint8)
#    dilation = cv2.dilate(img_not,kernel,iterations = 1)

#    img_not = cv2.bitwise_not(img_not)


    secureDel(invName,FILE_TYPE, False)
    cv2.imwrite(invName, img_not)





def main(filter_mode) :
  img=cv2.imread('./images/centers2.png',0)
  img_copy=img.copy()
  rows, cols =img.shape
  secureDel('dist.txt',FILE_TYPE,False)

  imgName=".\\images\\inverted.jpg"
  erodInvert(img, ks1=(3,300),ks2=(5,200),
    invName=imgName)
  image=cv2.imread(imgName,0)
  txtLines=calculEdges(image)
  img_copy=cv2.imread('./images/centers.png',0)

  for (L1,L2) in txtLines :
    cv2.line(img_copy,L1[0],L1[1],(0,0,0),2)
    cv2.line(img_copy,L2[0],L2[1],(0,0,0),2)

  cv2.imwrite('./images/hough_lines.png',img_copy)

  with open('nbLines.txt','w') as file :
    file.write("nbLines:"+str(len(txtLines))+":\n")

  img_copy=cv2.imread('./images/centers.png',0)


  for i,tLine in enumerate(txtLines) :
      yL1=tLine[0][0][1]
      yL2=tLine[1][0][1]
      frame=img_copy[yL1:yL2, 0:cols].copy()
      frmName='./Lines/Line' +str(i+1)+'.jpg'
      secureDel(frmName,FILE_TYPE,False)
      cv2.imwrite(frmName,frame)


