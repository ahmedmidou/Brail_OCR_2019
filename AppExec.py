import os
import argparse
import ImgProcess
import DotCenters
import LineCropper
import DotAlign
import TextDecoder
import ErrorRemoval
from FileMan import new_popen

#python AppExec.py -t 0
#python AppExec.py -t 1
#python AppExec.py -t 2












def imProcess(path,lang,mod,spell) :

  txtLog=""
  ImgProcess.main(path)
  DotCenters.main()
  LineCropper.main(mod)
  DotAlign.main()
  TextDecoder.main(lang)
  if spell and lang!='ar' :
    ErrorRemoval.main(lang)
    new_popen("notepad.exe correction.txt")
  else :
    new_popen("notepad.exe text.txt")


#  with open('Log.txt','w') as logFile :
#    logFile.write(txtLog)







if __name__ == "__main__":


  ap = argparse.ArgumentParser()
  ap.add_argument("-t", "--token", required=True,type=int,
    help="dummy int as token")

  ap.add_argument("-i", "--image",type=str,default='./images/ImageScan.tif',
    help="path to input image to be OCR'd")


  ap.add_argument("-m", "--mod",type=str,default='Tablet_A4',
    help="supported mode (Tablet_A4, Embosser)")
  ap.add_argument("-l", "--lang",type=str,default='ar',
    help="language used to decode brail dots")




  args = vars(ap.parse_args())


  t=args['token']
  if t==0 :
    file_name=args["image"]  
    ImgProcess.main(file_name)
  elif t==1 :
    DotCenters.main()
  elif t==2 :
    filter_mode=args["mod"] 
    LineCropper.main(filter_mode)



  exclude="""
  elif t==3 :
    DotAlign.main()
  elif t==4 :
    lang=args["lang"]
    TextDecoder.main(lang)
  elif t==5 :
    lang=args["lang"]
    ErrorRemoval.main(lang) """


