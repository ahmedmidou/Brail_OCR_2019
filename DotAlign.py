import cv2
import numpy as np
#from MaskUtils import *
import argparse
from FileMan import secureDel, FILE_TYPE, printLog
from LineCropper import erodInvert
from DotCenters import calcul_centers
from math import fabs
from MaskUtils import blank_paper
import pickle






X_AXIS=0
Y_AXIS=1


def writeDist(listLines,sign="") :

  with open('dist2.txt','a') as wf :
    wf.write(sign+":\n")
    for i in range(len(listLines)-1) :
      x1=listLines[i][0][0]
      x2=listLines[i+1][0][0]
      d=x2-x1
#      wf.write("x1= "+str(x1)+",x2= "+str(x2)+"\n")

      wf.write(str(d)+"\n")



class DotsLines :

  def __init__(self, id, points=[], h_lines=[], v_lines=[]) :
    self.id=id
    self.dots=points
    self.h_lines=h_lines
    self.v_lines=v_lines
    self.textLine=""

    self.h_lines.sort(key=lambda x : x[0][1])
    self.v_lines.sort()





  def selectDots(self,line,axis) :
    """ selectDots(self,line,axis)
    select and return a sorted list of dots,
    from the current list of dots,
    if horizontal line the Y_AXIS is given
    if vertical line the X_AXIS is given"""

    pList=self.dots
    lineDots=[]
    posL=line[0][axis]
    for p in pList :
      if p[axis]==posL :
        lineDots.append(p)

    if axis == X_AXIS:
      xy=Y_AXIS
    elif axis == Y_AXIS :
      xy=X_AXIS

    lineDots= sorted(lineDots,key=lambda d : d[xy])
    return lineDots


























def drawDotsLines(frmName, points, Lines=None, id=0) :


  imgc=cv2.imread(frmName, 0)

  r, c=imgc.shape


  blankName='./images/blank.jpg'
  secureDel(blankName,FILE_TYPE,False)
  blank_paper(c, r, 300,blank=blankName)
  img1 = cv2.imread(blankName,0)

  for p in points :
    # draw x,y coordinate of center
    cv2.circle(img1, (p[0], p[1]), 6, (0, 0, 0), 6)
    cv2.circle(img1, (p[0], p[1]), 5, (0, 0, 0), -1)

  if (Lines is not None) and (len(Lines)>0) :
    for L in Lines :
      cv2.line(img1,L[0],L[1],(0,0,0),2)
  frmName='./Lines/frames/Line' +str(id)+'.jpg'

  secureDel(frmName,FILE_TYPE,False)
  cv2.imwrite(frmName,img1)
  return frmName














def selectLine(Lines,dot,axis) :
    """ selectLine(Lines,dot,axis)
    return the x or y coordinate of the nearest line to a given dot,
    the line is selected from a list of vertical listLines according to the X_AXIS,
     or horizontal listLines according to the Y_AXIS"""

  
    posDot=dot[axis]
    distTab =[]
    for i in range(len(Lines)) :
      posL=Lines[i][0][axis]
      dist=fabs(posDot - posL)
      distTab.append((posL,dist))


    distTab = sorted(distTab,key = lambda x : x[1])
    return distTab[0][0]












def main() :

  nbL=0
  secureDel('dist2.txt',FILE_TYPE,False)
  with open ('nbLines.txt','r') as f :
    ln=f.read()
    tab=ln.strip().split(':')
    nbL=int(tab[1])
    printLog("nbL = ", nbL)
  listDotsLines=[]
  for i in range(nbL) :
    HL=[]
    frmName='./Lines/Line' +str(i+1)+'.jpg'
    img=cv2.imread(frmName, 0)
    points=calcul_centers(img,echo=False)[0]
    rows,cols=img.shape



    imgName="./Lines/frames/inverted_"+str(i+1)+".jpg"
    erodInvert(img, ks1=(1,400), ks2=(0,0),
      invName=imgName)

    img2=cv2.imread(imgName, 0)


    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(img2, 127, 255, 0)


    # find contour in the binary image
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #printLog("nb contours : ",len(contours))
    for c in contours :
      x,y,w,h = cv2.boundingRect(c)
      y0=int(y+(h//2))
      line0=((0,y0),(cols,y0))
      HL.append(line0)

    points2=[]
    for p in points :
      yp=selectLine(HL,p,Y_AXIS)
      points2.append((p[0],yp))

  #  drawDotsLines(frmName, points2, HL,(i+1))
    frmName=drawDotsLines(frmName, points2, None,(i+1))

    img1=cv2.imread(frmName,0)

  #  imvName='./Lines/frames/inverted_' +str(i+1)+'.jpg'
    imgName='./Lines/frames/vertical_' +str(i+1)+'.jpg'
  #  VerticalMask(img1, ks1=(50,1),ks2=(5,1),
  #    invName=imvName,dilName=imgName)
    erodInvert(img1, ks1=(100,3), ks2=(0,0),
      invName=imgName)



    k=cv2.imread(imgName,0)

    ret,thresh = cv2.threshold(k,127,255,0)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #printLog("nb contours : ",len(contours))



    v_lines=[]
    for c in contours :
      x,y,w,h = cv2.boundingRect(c)
      xL=int(x+(w//2))
      v_lines.append(((xL, 0),(xL, rows)))

    v_lines.sort()

    points3=[]
    for p in points2 :
      xp=selectLine(v_lines,p,X_AXIS)
      points3.append((xp,p[1]))


    frmName=drawDotsLines(frmName, points3, v_lines,(i+1))

    dL=DotsLines(i+1, points3, HL, v_lines)
    listDotsLines.append(dL)
    writeDist(v_lines,sign="line "+str(i+1)+" : \n")




  with open('dLdata','wb') as dLfile :
    dLPickler=pickle.Pickler(dLfile)
    dLPickler.dump(listDotsLines)








if __name__ == "__main__":
  main()







