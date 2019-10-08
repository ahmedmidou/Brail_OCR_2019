import cv2
import numpy as np
from PIL import Image
import os
import argparse
from FileMan import secureDel, FILE_TYPE, printLog


#python ImgProcess.py -i ./images/img017.tif

#python help("ImgProcess.get_dpi")





def get_dpi(imgPath) :
    """get_dpi(imgPath)
     return a tuple (x_dpi,y_dpi)
    describing the resolution of a given image path
    if the info does not exist returns (0,0)"""


    img= Image.open(imgPath)
    #printLog("info = ",img.info)
    #Or we can loop through it as in 2.0 as such:

    for tag,value in img.info.items() :
      if tag.lower()=="dpi" :
        return value
    return (0,0)


def set_resolution(filename,new_filename, new_dpi=300) :
    """ set_resolution(filename,new_filename, new_dpi=300)
    resize the image :
    filename is the path to the image.
    new_dpi is the new resolution default is300
    new_filename is the path to the result image to save """

    # define the x,y scale (default resolution is 300dpi)
    x_scale=1.0
    y_scale=1.0

    dpi=get_dpi(filename)
    printLog(dpi," ",type(dpi))

    if dpi[0]>0 :
      x_scale=dpi[0]/new_dpi
    if dpi[1]>0 :
      y_scale=dpi[1]/new_dpi

    im = Image.open(filename)
    size=(int(im.width//x_scale),int(im.height//y_scale))
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save(new_filename, dpi=(new_dpi,new_dpi))




def BlurErodeThresh(imFilename,ksize=(8,5),erod=True) :

    img= cv2.imread(imFilename,0)

    #img = cv2.blur(img,(5,5))


#     median blurring should be done to remove noise
    img = cv2.medianBlur(img, 7)

    if erod :
      kernel = np.ones(ksize,np.uint8)
      img = cv2.erode(img,kernel,iterations = 1)

    img = cv2.threshold(img, 0, 255,
      cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #show_wait_destroy("ThreshImage", img)
    h,w=img.shape
    thName='./images/thresh.jpg'
    secureDel(thName,FILE_TYPE)
    cv2.imwrite(thName,img[20:(h-40), 60:(w-100)])


def preProcess(file_name,new_file_name,ksize=(5,5)) :
  set_resolution(file_name,new_file_name)
  printLog(get_dpi(new_file_name))
  BlurErodeThresh(file_name,ksize)










def main(file_name) :

    new_file_name="./images/resized.tif"
    secureDel(new_file_name,FILE_TYPE)
    preProcess(file_name,new_file_name,ksize=(5,5))

if __name__ == "__main__":


    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
      help="path to input image to be OCR'd")
    args = vars(ap.parse_args())




    file_name=args["image"]  
    main(file_name)
