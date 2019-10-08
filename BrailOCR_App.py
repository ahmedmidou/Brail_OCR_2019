"""  An open source app for BrailOCR  """

import wx
#from Auth import *
from ScanGUI import *
from ContPanel import *
from FileMan import secureDel, FILE_TYPE, printLog
import ADMIN as adm
import os, sys
from WorkLoad import wThread
#import win32gui, win32con, ctypes



class MainAppFrame(wx.Frame):
  """  MainAppFrame  """

  def __init__(self, *args, **kw):
    # ensure the parent's __init__ is called
    super(MainAppFrame, self).__init__(*args, **kw)





    # create a panel in the frame
    self.pnl = MainPanel(self, -1)
    # create a menu bar
    self.makeMenuBar()

    # and a status bar
    self.CreateStatusBar()
    self.SetStatusText("Welcome to Brail OCR!")


  def makeMenuBar(self):
    """ A menu bar is composed of menus, which are composed of menu items.
    This method builds a set of menus and binds handlers to be called
    when the menu item is selected."""
    
    # Make a file menu with Open, Scan and Exit items
    fileMenu = wx.Menu()
    # The "\t..." syntax defines an accelerator key that also triggers
    # the same event
    openItem = fileMenu.Append(-1, "&Open...\tCtrl-O", 
        "PLEASE Open an image ")
    scanItem = fileMenu.Append(-1, "&Scan...\tCtrl-S", 
        "Select scan settings ")


    fileMenu.AppendSeparator()
    # When using a stock ID we don't need to specify the menu item's
    # label
    exitItem = fileMenu.Append(wx.ID_EXIT)

    # Now a help menu for the about item
    helpMenu = wx.Menu()
    aboutItem = helpMenu.Append(wx.ID_ABOUT)

    # Make the menu bar and add the two menus to it. The '&' defines
    # that the next letter is the "mnemonic" for the menu item. On the
    # platforms that support it those letters are underlined and can be
    # triggered from the keyboard.
    menuBar = wx.MenuBar()
    menuBar.Append(fileMenu, "&File")
    menuBar.Append(helpMenu, "&Help")

    # Give the menu bar to the frame
    self.SetMenuBar(menuBar)

    # Finally, associate a handler function with the EVT_MENU event for
    # each of the menu items. That means that when that menu item is
    # activated then the associated handler function will be called.
    self.Bind(wx.EVT_MENU, self.pnl.onOpen, openItem)
    self.Bind(wx.EVT_MENU, self.OnScan, scanItem)
    self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
    self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
    self.Center()





  def OnExit(self, event):
    """Close the frame, terminating the application."""
    self.Close(True)


  def OnOpen(self, event):
    """ open image."""
    wx.MessageBox("please open image")
  def OnScan(self, event):

    wx.MessageBox("warning : The CLscan tool of TerminalWorks is demo\n"+
      "it's for 15 days evaluation only and not part of the app  !!")
    if ScannerObj.nbScanners==0 :
      wx.MessageBox("No scanners !!")
    else :
        dlg = ScanDialog(ScannerObj.listScanners)
        dlg.ShowModal()
        scanned = dlg.scanned

        dlg.Destroy()

        if scanned :
          self.pnl.pathText.SetValue(".\\images\\ImageScan.tif")






  def OnAbout(self, event):
    """Display an About Dialog"""
    wx.MessageBox(" An App By Siala Midou", 
      "About the Auther",
      wx.OK|wx.ICON_INFORMATION)




def showProgress() :
  progressMax = 100

  dialog = wx.ProgressDialog("Please wait : ", "Time Load remaining", progressMax,
          style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE) # wx.PD_CAN_ABORT | 
#  dialog.SetFocus()

  keepGoing = True
  count = 0
  ss=1
  while keepGoing and count < progressMax:
      pr=ScannerObj.currentProgress
      if pr<50 :
        count = pr+ss
      else :
        count = pr
#      print("count", ScannerObj.currentProgress)
      if(count>=100) :
        count=100
      wx.Sleep(1)
      keepGoing = dialog.Update(count)
      ss+=1
  print("Loaded ...", keepGoing)
  dialog.Close()

  dialog.Destroy()
  print("destroyed !!")



if __name__ == '__main__':
  # When this module is run (not imported) then create the app, the
  # frame, show it, and start the event loop.

#  The_program_to_hide = win32gui.GetForegroundWindow()
#  win32gui.ShowWindow(The_program_to_hide , win32con.SW_HIDE)




  if not adm.isUserAdmin():
    printLog("You're not an admin.", os.getpid())
    adm.runAsAdmin()
    sys.exit(0)
  else:
    printLog("You are an admin!", os.getpid())


  secureDel("./log.txt",FILE_TYPE)


  app = wx.App(False)
#  ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


  
  # Ask user to login
#  dlg = LoginDialog()
#  dlg.ShowModal()
#  authenticated = dlg.logged_in
#  dlg.Destroy()
  authenticated = True
  if authenticated :
    #ScannerObj.loadScanners()
    thw=wThread("th_load_scanners")
    thw.start()
    showProgress()
    frm = MainAppFrame(None, title='Brail OCR App', size = (350, 250))
    frm.Show()


  app.MainLoop()


