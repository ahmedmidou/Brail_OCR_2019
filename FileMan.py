import os
import sys

import subprocess as sub



FILE_TYPE = 1
FOLDER_TYPE = 0

class StdoutRedirection:
    """Standard output redirection context manager"""

    def __init__(self, path):
        self._path = path

    def __enter__(self):
        sys.stdout = open(self._path, mode="a")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = sys.__stdout__



def printLog(*args) :
  with StdoutRedirection("log.txt"):
    print(args,'\n')



def new_popen(cmd) :
  p=sub.Popen(cmd,stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, universal_newlines=True, shell=True, encoding="latin-1") 
  stdout, stderr =p.communicate()
  p.wait()
  lines=stdout.split('\n')
  return lines





def secureDel(path, ftype, echo=True) :
  """ check if a folder or file exists
  then delete it.
  given paremeters : 
  path to the file or folder.
  ftype : (1==file) , (0 == Folder)
  return true if action performed """


  if os.path.exists(path):
    if ftype == FILE_TYPE :
      os.remove(path)
      if echo :
        printLog("file : ",path , " removed")
      return True
    elif ftype == FOLDER_TYPE :
      os.rmdir(path)
      if echo :
        printLog("folder : ",path , " removed")
      return True
  else :
    if echo :
      printLog("the item does not exist : \n", path)
  return False



