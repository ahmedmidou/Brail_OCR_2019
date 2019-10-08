import wx
import os
import FileMan as fm
import AppExec as apx

imgExts=['.bmp','.jpg','.png','.tif']
class MainPanel(wx.Panel):
  """  class MainPanel creates a panel with 2 comboboxes and more, inherits wx.Panel
    (putting your components/widgets on a panel gives additional versatility) """


  def __init__(self, parent, id):
  # no pos and size given, so panel defaults to fill the parent frame
    wx.Panel.__init__(self, parent, id)


    # Language combobox
    listLang=["English","French","Arabic"]

 
    lang_lbl = wx.StaticText(self,-1 , "Language:    ", (50, 25))
    self.cbLang = wx.ComboBox(self, -1, value=listLang[0], pos=wx.Point(250, 25),
      choices=listLang, style=wx.CB_DROPDOWN|wx.CB_READONLY)
    self.cbLang.SetToolTip(wx.ToolTip("select language from dropdown-list"))

 


    # mode combobox
#    listMod=["Tablet_A4","Embosser"]
 
#    mod_lbl = wx.StaticText(self, label="Mode    :", pos=wx.Point(50, 50))
#    self.cbMod = wx.ComboBox(self, -1, value=listMod[0], pos=wx.Point(250, 50),
#      choices=listMod, style=wx.CB_DROPDOWN|wx.CB_READONLY)
    self.pathText = wx.TextCtrl(self, pos=wx.Point(50, 100),
       style =wx.TE_CENTER)

    btn = wx.Button(self, label="Select", pos=wx.Point(150, 100))
    btn.Bind(wx.EVT_BUTTON, self.onOpen)

    self.ckxSpell = wx.CheckBox(self, label = 'Spell Check !', pos = (50,150))

    btn2 = wx.Button(self, label="Process", pos=wx.Point(150, 150))
    btn2.Bind(wx.EVT_BUTTON, self.onProcess)




  def onProcess(self, event) :
    lang=self.cbLang.GetValue()[:2].lower()
    fm.printLog("lang = ",lang)
    mod=""
#    mod=self.cbMod.GetValue()
    path=self.pathText.GetValue()
    spell=self.ckxSpell.GetValue()
    fm.printLog("spell = ",spell)
    f_ext=path[-4:].lower()
    if not os.path.isfile(path) :
      wx.MessageBox("Please enter a valid path !!")
    elif f_ext not in imgExts :
      #fm.printLog("fext : ",path[-4:])
      wx.MessageBox("Supported image Types \n"+
        "'.bmp','.jpg','.png','.tif'")
    else :
      #pass
      apx.imProcess(path,lang,mod,spell)




  def onOpen(self, event):
    with wx.FileDialog(self, "Open image file", wildcard="ALL image files (*.*)|*.*",
      style=wx.FD_OPEN ) as fileDialog:

      if fileDialog.ShowModal() == wx.ID_CANCEL:
        return     # the user changed their mind

      # Proceed loading the file chosen by the user
      self.pathname = fileDialog.GetPath()
      imgName=fileDialog.GetFilename()
      fm.printLog("file : ", imgName)
      self.pathText.SetValue(self.pathname)




if __name__ == '__main__':

  app = wx.App()
  # create a window/frame, no parent, -1 is default ID, title, size
  frame = wx.Frame(None, -1, "Process Settings...", size = (350, 250)) 
  # call the derived class, -1 is default ID, can also use wx.ID_ANY
  MainPanel(frame,-1)
  # show the frame
  frame.Show(True)
  # start the event loop
  app.MainLoop()



