# -*- coding: latin-1 -*-
import cv2
import numpy as np
import argparse
from FileMan import secureDel, FILE_TYPE, printLog
import pickle as pk
import os
from DotAlign import DotsLines

def writeMSG(msg,sign='') :
  with open('cod.txt','a') as wf :
      wf.write(sign+" m = "+msg+"\n")


def chk(cod) :
#  writeMSG(cod,sign='cod')
  for c in cod :
    if c not in '0123456789' :
      writeMSG(cod,sign='cod')
      return False
  return True




def codeChar(h_lines, col1=[],col2=[]) :

  strCod=""
  try :
    L1=h_lines[0]
    L2=h_lines[1]
    L3=h_lines[2]



    y1= L1[0][1]
    y2=L2[0][1]
    y3=L3[0][1]
    if len(col1)>0 :
      for p in col1 :
        if p[1]==y1 :
          strCod+='1'
        elif p[1]==y2 :
          strCod+='2'
        elif p[1]==y3 :
          strCod+='3'
    if len(col2)>0 :
      for p in col2 :
        if p[1]==y1 :
          strCod+='4'
        elif p[1]==y2 :
          strCod+='5'
        elif p[1]==y3 :
          strCod+='6'
  except :
    pass
  return strCod



def main(lang='ar') :


  # load the list of DotsLines objects
  listDotsLines=[]
  with open('dLdata','rb') as dLfile :
    dLUnpickler=pk.Unpickler(dLfile)
    listDotsLines=dLUnpickler.load()

  printLog("nb DotsLines obj : ", len(listDotsLines))



  # load the dictionary for selected language
  dicBTX={}
  dicNum={}


  if lang=="ar" :
  #  dicBTX=arabic_btx
  #  dicNum=arabic_num
    with open('arData','rb') as arFile :
      arUnpickler=pk.Unpickler(arFile)
      dicBTX=arUnpickler.load()
      dicNum=arUnpickler.load()
    printLog("nb arabic dict items : ", len(dicBTX),"++",len(dicNum))

  elif lang=="fr" :
  #  dicBTX=french_btx
  #  dicNum=french_num
    with open('frData','rb') as frFile :
      frUnpickler=pk.Unpickler(frFile)
      dicBTX=frUnpickler.load()
      dicNum=frUnpickler.load()
    printLog("nb french dict items : ", len(dicBTX),"++",len(dicNum))







##########################################

  elif lang=="en" :

    with open('enData','rb') as enFile :
      enUnpickler=pk.Unpickler(enFile)
      dicBTX=enUnpickler.load()
      dicNum=enUnpickler.load()
    printLog("nb english dict items : ", len(dicBTX),"++",len(dicNum))





  #lang="ar"






  secureDel('cod.txt',FILE_TYPE,False)
  secureDel('text.txt',FILE_TYPE,False)


  for dL in listDotsLines :

    checked=False #toggle var
    curDic=dicBTX
    col1=[]
    col2=[]
    h_lines=dL.h_lines
    v_lines=dL.v_lines
    nbL=len(v_lines)

    for i in range(nbL-1) :
      cL1=v_lines[i]
      cL2=v_lines[i+1]
      xL1=cL1[0][0]
      xL2=cL2[0][0]

      if (xL2-xL1)<36 and not checked :
        col1=dL.selectDots(cL1,0)
        col2=dL.selectDots(cL2,0)
        cod=codeChar(h_lines, col1,col2)
#        printLog("cod= ", cod)
        mcod=0
        if cod!="" and chk(cod) :
          mcod=int(cod.strip())
        else :
          continue



        if mcod in curDic.keys():
          asc=curDic[mcod]
          for c in asc :
            dL.textLine+=c
          checked=True
        else : #if mcod not in curDic.keys():
          writeMSG(str(mcod)+"line="+str(dL.id)+"  numcol = "+str(i))
          checked=False
          if lang!="ar" :
            dL.textLine+='?'
      elif (xL2-xL1)<50 and checked :
        checked=False
      elif (xL2-xL1)<75 and not checked :
        col1=dL.selectDots(cL1,0)
        col2=[]
        cod=codeChar(h_lines, col1,col2)
        mcod=0
        if cod!="" and chk(cod) :
          mcod=int(cod.strip())
        else :
          continue

        if mcod in curDic.keys():
          asc=curDic[mcod]
          for c in asc :
            dL.textLine+=c
          checked=False
        else : #if mcod not in curDic.keys():
          writeMSG(str(mcod)+"line="+str(dL.id)+"  numcol = "+str(i))
          checked=False
          if lang!="ar" :
            dL.textLine+='?'
      elif (xL2-xL1)>78 :
        checked=False
        dL.textLine+=' '
      #printLog(dL.textLine.strip())












    with open('text.txt','a',encoding='latin-1') as wf :
        wf.write(dL.textLine.strip()+'\n')



if __name__ == "__main__":
  main()






