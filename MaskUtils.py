import cv2
import numpy as np
from PIL import Image
import FileMan as fm



def blank_paper(width, height,ndpi, blank='blank.jpg')  :
  img1 = Image.new(mode='L', size=(width, height), color=255)
  img1.save(blank, dpi=(ndpi,ndpi))




def count_nonblack_np(img):
  """Return the number of pixels in img that are not black.
  img must be a Numpy array with colour values along the last axis.

  """
  try:
    return img.any(axis=-1).sum()
  except :
    return -1




def HorizontalMask(img,ks1=(20,50),ks2=(2000,2),
      invName="inverted.jpg",dilName="horizontal2.jpg") :

    img_not = img.copy()


    kernel = np.ones(ks1,np.uint8)
    img_not = cv2.erode(img_not,kernel,iterations = 1)


    img_not = cv2.bitwise_not(img_not)


    fm.secureDel(invName,fm.FILE_TYPE)
    cv2.imwrite(invName, img_not)




    r, c =img_not.shape

    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, ks2)
    horizontal = cv2.dilate(img_not, horizontalStructure, (-1, -1))

    #show_wait_destroy("HorizImage", horizontal)
    fm.secureDel(dilName,fm.FILE_TYPE)
    cv2.imwrite(dilName, horizontal)








def VerticalMask(img, ks1=(50,5),ks2=(200,5),
      invName=".\\inverted.jpg",dilName=".\\dilatedpart.jpg") :

    img_not=img.copy()
    kernel = np.ones(ks1,np.uint8)
    img_not = cv2.erode(img,kernel,iterations = 1)

    #show_wait_destroy("erodeImage", img_not)
    img_not=cv2.bitwise_not(img_not)
    
    #show_wait_destroy("INV_image", img_not)
    fm.secureDel(invName,fm.FILE_TYPE,False)
    cv2.imwrite(invName, img_not)


    #dilating
    kernel = np.ones(ks2,np.uint8)
    dilation = cv2.dilate(img_not,kernel,iterations = 1)
    #show_wait_destroy("dilatPart", dilation,mouse=True)
    fm.secureDel(dilName,fm.FILE_TYPE,False)
    cv2.imwrite(dilName, dilation)















def edgeLines(img,imfile='edges.jpg',
          minLineLength = 100,    maxLineGap = 10) :

    #defining the edges
    edges = cv2.Canny(img,50,150,apertureSize = 3)
    fm.secureDel(imfile,fm.FILE_TYPE,False)
    cv2.imwrite(imfile,edges)

    #finding the end points of the hough lines

    m=[]
    lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
    try :
      for x in range(0, len(lines)):
          for x1,y1,x2,y2 in lines[x]:
                m.append(((x1,y1),(x2,y2)))
    except TypeError :
      fm.printLog("No lines !!")
    #fm.printLog("length of list m is:",len(m))
    return m



