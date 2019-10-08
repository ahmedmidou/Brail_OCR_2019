import cv2
import numpy as np
from PIL import Image
from MaskUtils import blank_paper
import argparse
import os
from FileMan import secureDel, FILE_TYPE, printLog

#python DotCenters.py -t 1 -A4 1 -lb 85








#Dot height is approximately 0.02 inches (0.5 mm); [6px/300dpi]
#the horizontal and vertical spacing between dot centers within a Braille cell is approximately 0.1 inches (2.5 mm); [30px/300dpi]
#the blank space between dots on adjacent cells is approximately 0.15 inches (3.75 mm) horizontally; [45px/300dpi] 
#and 0.2 inches (5.0 mm) vertically; [60px/300dpi]

# a scanner (epson perfection v19)







def calcul_centers(image,echo=True) :
  """calculate the center of dots 
  wich are concidered as multiple blobs.
  the only given parameter is the image 
  return a list of tuple coordinate (x,y) of centers 
  and corresponding list 
  of bounding rect tuple = ((x,y),(w,h))"""
 
  img=image.copy()
  cntList=[]
  points=[]
  if len(img.shape)!=2 : 
    # convert the image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


  img=cv2.bitwise_not(img)
  # convert the grayscale image to binary image
  ret,thresh = cv2.threshold(img,127,255,0)

  # find contour in the binary image
  contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #im2,
  if echo :
    printLog("number of dots : ", len(contours))
  for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    cntList.append(((x,y),(w,h)))
    # calculate moments for each contour
    try :
      M = cv2.moments(c)
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])
    except ZeroDivisionError :
      continue
    points.append((cX,cY))
  return points,cntList









def main() :
  img = cv2.imread('./images/thresh.jpg',0)

  height,width=img.shape
  points,cntList=calcul_centers(img)

  points=calcul_centers(img)[0]

  blankName='.\\images\\blank.jpg'
  secureDel(blankName,FILE_TYPE,False)
  blank_paper(width, height,300,blank=blankName)

  img1 = cv2.imread(blankName,0)

  for p in points :
    # draw x,y coordinate of center
    cv2.circle(img1, (p[0], p[1]), 5, (0, 0, 0), 5)
    cv2.circle(img1, (p[0], p[1]), 4, (0, 0, 0), -1)

  resultName="./images/centers.png"
  secureDel(resultName,FILE_TYPE)
  cv2.imwrite(resultName,img1)




  img2 = cv2.imread(blankName,0)

  for p in points :
    # draw x,y coordinate of center
    cv2.circle(img2, (p[0], p[1]), 12, (0, 0, 0), 12)
    cv2.circle(img2, (p[0], p[1]), 10, (0, 0, 0), -1)

  resultName="./images/centers2.png"
  secureDel(resultName,FILE_TYPE)
  cv2.imwrite(resultName,img2)










if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("-t", "--token", required=True,type=int,
    help="dummy int as token")
  args = vars(ap.parse_args())


  main()



