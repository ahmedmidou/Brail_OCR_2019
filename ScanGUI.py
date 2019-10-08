import wx
import os
import sys
import subprocess as sub
#import TimeStop as tm
from FileMan import secureDel, FILE_TYPE, printLog, new_popen
import ADMIN as adm



#tm.fixDate="01-01-2019"




def selectScanners() :
  scList=[]



  for line in new_popen(".\\clscan\\clscan.exe /GetScanners") :
    ln=line.strip()
    if (ln=="") or (ln.startswith('Supported scanners:')) or ('wia' in ln.lower()):
      continue
    else :
      scList.append(ln)

  return scList


def getResolution(ln) :
# Supported resolutions:
# Min value=50, max value=1184, step=1
      res=0
      maxStr=ln.split(',')[1]
      maxR=int(maxStr.split('=')[1])
      if maxR>=300 :
        res= 300
      else :
        res= maxR
      return res





def selectSettings(scanner) :
  pgList=[]
  clList=[]
  tbr=[]
  res=0
  switch=0

#or (ln.startswith('Supported page sizes:'))

#Problem while opening the scanner HP DeskJet 2130 series TWAIN
  for line in new_popen('.\\clscan\\clscan.exe /GetPageSizes /GetColorTypes /GetResolutions /SetScanner "'+scanner+'"'):
    ln=line.strip()
    printLog(ln+'\n')
    if (ln=="") or (ln.startswith('Selected scanner')) :
      continue
    elif 'Problem while opening the scanner' in ln :
      ScannerObj.listScanners.remove(scanner)
      ScannerObj.nbScanners-=1
      break
    elif (ln.startswith('Supported page sizes:')) :
      switch=1
    elif (ln.startswith('Supported color types:')) :
      switch=2
    elif (ln.startswith('Supported resolutions:')) :
      switch=3
    elif ('not supported' in ln) :
      switch=0
    elif switch==1 :
      pgList.append(ln)
    elif switch==2 :
      clList.append(ln)
    elif switch==3 :
      #print("line : ",ln)
      if 'step' in ln :
        res = getResolution(ln)
      else :
        tbr.append(int(ln.strip()))



  if len(tbr)>0 :
    tbr.sort(reverse=True)
    if tbr[0]>300 :
      res=300
    else :
      res=tbr[0]

  return pgList, clList, res

def get_A4_idx(list) :
  for i,m in enumerate(list):
    if m=='A4' :
      return i

  return 0

def get_GRAY_idx(list) :
  for i,m in enumerate(list):
    if m=='GRAY' :
      return i

  return 0


class ScannerObj :
  listScanners=[]
  scObjList=[]
  nbScanners=0
  currentProgress=0
  progressStep=0





  def storeScanners(cls, listScanners) :
    cls.progressStep=int(90//cls.nbScanners)
    for sc in listScanners:
      cls.scObjList.append(ScannerObj(sc))
      cls.currentProgress+=cls.progressStep
      print("loaded : "+sc)
    cls.currentProgress=100
  storeScanners=classmethod(storeScanners)
  def getScanner(cls, scannerName) :
    for sc in cls.scObjList:
      if sc.scannerName==scannerName :
        return sc
    return None

  getScanner=classmethod(getScanner)



  def loadScanners(cls) :
    ScannerObj.listScanners=selectScanners()
    cls.currentProgress=10

    ScannerObj.nbScanners=len(ScannerObj.listScanners)
    printLog("nb scanners = ",ScannerObj.nbScanners)
    if ScannerObj.nbScanners==0 :
      printLog("No scanners !!")
      cls.currentProgress=100
    else :
      ScannerObj.storeScanners(ScannerObj.listScanners)

  loadScanners=classmethod(loadScanners)



  def __init__(self,scannerName) :
    listPgs,listColors,res=selectSettings(scannerName)
    self.listPgs=listPgs
    self.listColors=listColors
    self.res=res
    self.scannerName=scannerName


    



class ScanDialog(wx.Dialog):
  """  Class to define Scan dialog  """
 

  def fillSettings(self, scannerName) :
    idx=-1
    idx2=-1
#    listPgs,listColors,res=selectSettings(scanner)
    sc=ScannerObj.getScanner(scannerName)
    listPgs=sc.listPgs
    listColors=sc.listColors
    res=sc.res

    if len(listPgs)>0 :
      idx=get_A4_idx(listPgs)
    if len(listColors)>0 :
      idx2=get_GRAY_idx(listColors)
    self.cbPgs.SetItems(listPgs)
    self.cbCls.SetItems(listColors)
    self.resolution=res

    if idx>0 :
      self.cbPgs.SetValue(listPgs[idx])
    if idx2>0 :
      self.cbCls.SetValue(listColors[idx2])




  def onScan(self, event):
    scn=self.cbScanners.GetValue()
    pg=self.cbPgs.GetValue()
    cr=self.cbCls.GetValue()
    res=self.resolution
    secureDel("./scanLog.txt",FILE_TYPE)
    secureDel("./images/ImageScan.tif",FILE_TYPE)



    cmd='.\\clscan\\clscan.exe '
    cmd+='/SetFileName ".\\images\\ImageScan.tif" '
    cmd+='/LogToFile ".\\scanLog.txt" '
    cmd+='/SetDeskew '
    cmd+='/SetSource Auto '
    cmd+='/SetCrop '
    cmd+='/SetThreshold "150" '
    cmd+='/SetContrast "50" '
    cmd+='/SetBrightness "50" '
#    cmd+='/ShowUI '
#    cmd+='/UseScan2 '
    cmd+='/SetDuplex:Y '
    cmd+='/SetJpegQuality "100" '
#    cmd+='/SetDeskew '





    cmd+='/SetResolution "'+str(res)+'" '
    if pg!='' :
      cmd+='/SetPageSize "'+pg+'" '
      printLog("added :"+pg)
    else :
      printLog("not added :"+pg)




    if cr!='' :
      cmd+='/SetColorType "'+cr+'" '

    cmd+='/SetScanner "'+scn+'" '



    log=new_popen(cmd)

    log+=new_popen("python AppExec.py -t 0")
    log+=new_popen("python AppExec.py -t 1")


    #printLog("\n".join(log))

    self.scanned=True
    self.Close()







  def OnCombo(self, event): 


    self.fillSettings(self.cbScanners.GetValue())

    printLog("You selected"+self.cbScanners.GetValue()+" from Combobox")








  def __init__(self,listScanners):
    """  Constructor  """
    wx.Dialog.__init__(self, None, title="Scan settings :",size = (300,300))
    self.scanned = False
    self.listScanners=listScanners

#    self.scObjList=scObjList



    scanners_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
    scanners_lbl = wx.StaticText(self, label="scanners:")
    scanners_sizer.Add(scanners_lbl, 0, wx.ALL|wx.CENTER, 5)
    self.cbScanners = wx.ComboBox(self, -1, value=listScanners[0], 
      choices=listScanners, style=wx.CB_DROPDOWN|wx.CB_READONLY)
    self.cbScanners.Bind(wx.EVT_COMBOBOX, self.OnCombo)
    scanners_sizer.Add(self.cbScanners, 0, wx.ALL, 5)
 

#    listPgs,listColors,res=selectSettings(listScanners[0])

    pgs_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
    pgs_lbl = wx.StaticText(self, label="format:")
    pgs_sizer.Add(pgs_lbl, 0, wx.ALL|wx.CENTER, 5)
    self.cbPgs = wx.ComboBox(self, -1, 
       style=wx.CB_DROPDOWN|wx.CB_READONLY)



    pgs_sizer.Add(self.cbPgs, 0, wx.ALL, 5)
 



    cls_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
    cls_lbl = wx.StaticText(self, label="color:")
    cls_sizer.Add(cls_lbl, 0, wx.ALL|wx.CENTER, 5)

    self.cbCls = wx.ComboBox(self, -1, 
       style=wx.CB_DROPDOWN|wx.CB_READONLY)


    cls_sizer.Add(self.cbCls, 0, wx.ALL, 5)




    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(scanners_sizer, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
    main_sizer.Add(pgs_sizer, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
    main_sizer.Add(cls_sizer, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

    btn = wx.Button(self, label="Scan")
    btn.Bind(wx.EVT_BUTTON, self.onScan)
    main_sizer.Add(btn, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)


    self.SetSizer(main_sizer)
    self.fillSettings(listScanners[0])
    self.Center()




if __name__ == '__main__':
  # When this module is run (not imported) then create the app, the
  # dialog, show it, and start the event loop.

  if not adm.isUserAdmin():
    printLog("You're not an admin.", os.getpid())
    adm.runAsAdmin()
    sys.exit(0)
  else:
    printLog("You are an admin!", os.getpid())




  ScannerObj.loadScanners()

  app = wx.App()
  if ScannerObj.nbScanners==0 :
    wx.MessageBox("No scanners !!")
  else :
      dlg = ScanDialog(ScannerObj.listScanners)
      dlg.ShowModal()
      scanned = dlg.scanned

      dlg.Destroy()

  app.MainLoop()


