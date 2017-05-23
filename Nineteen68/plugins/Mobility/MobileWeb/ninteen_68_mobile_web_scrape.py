import wx
import sys
import os
from selenium import webdriver
import browserops
import clickandadd
import fullscrape

from socketIO_client import SocketIO,BaseNamespace
import time
import objectspy

browserobj = browserops.BrowserOperations()
clickandaddoj = clickandadd.Clickandadd()
fullscrapeobj = fullscrape.Fullscrape()

class ScrapeWindow(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self, parent,id, title,browser,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        obj = browserops.BrowserOperations()
        self.socketIO = socketIO
        status = obj.openBrowser(browser)
        self.panel = wx.Panel(self)

        self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,8 ), size=(175, 28))
        self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)   # need to implement OnExtract()
        self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,38 ), size=(175, 28))
        self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()

##            self.fullscrapebutton.SetToolTip(wx.ToolTip("To perform FULLSCRAPE Scraping"))
        self.comparebutton = wx.ToggleButton(self.panel, label="Compare",pos=(12,68 ), size=(175, 28))
        self.comparebutton.Bind(wx.EVT_TOGGLEBUTTON, self.compare)   # need to implement OnExtract()
        self.Centre()
        style = self.GetWindowStyle()
        self.SetWindowStyle( style|wx.STAY_ON_TOP )
        wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Show()



    #----------------------------------------------------------------------
    def OnExit(self, event):
        self.Close()
        driver = browserops.driver
        driver.close()

    #----------------------------------------------------------------------
    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton.Disable()
            self.comparebutton.Disable()
            clickandaddoj.startclickandadd()
            event.GetEventObject().SetLabel("Stop ClickAndAdd")
##            wx.MessageBox('CLICKANDADD: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
            print 'click and add initiated, select the elements from AUT'

        else:
            d = clickandaddoj.stopclickandadd()
            print 'Scrapped data saved successfully in domelements.json file'
            self.socketIO.emit('scrape',d)
##            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.Close()
            event.GetEventObject().SetLabel("Start ClickAndAdd")
            print 'Click and add scrape  completed'

    def compare(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton.Disable()
            self.startbutton.Disable()
            obj = objectspy.Object_Mapper()
            obj.compare()
            event.GetEventObject().SetLabel("Update")
        else:
            obj = objectspy.Object_Mapper()
            d = obj.update()
            self.socketIO.send(d)
            self.Close()


    #----------------------------------------------------------------------
    def fullscrape(self,event):
        print 'Performing full scrape'
        self.startbutton.Disable()
        self.comparebutton.Disable()
        d = fullscrapeobj.fullscrape()
##        self.startbutton.Enable()
##        self.savescrapebutton.Enable()
##        wx.MessageBox('FULLSCRAPE: Scrape completed', 'Info', wx.OK | wx.ICON_INFORMATION)
##        print 'self.socketIO : ',self.socketIO
##        print 'Acknoledgement id : ',self.socketIO._ack_id
        self.socketIO.emit('scrape',d)
        self.Close()
        print 'Full scrape  completed'


