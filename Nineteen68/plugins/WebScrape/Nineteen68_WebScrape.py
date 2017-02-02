import wx
import sys
import os
from selenium import webdriver
import browserops
import clickandadd
import fullscrape
import clientwindow
from socketIO_client import SocketIO,BaseNamespace


browserobj = browserops.BrowserOperations()
clickandaddoj = clickandadd.Clickandadd()
fullscrapeobj = fullscrape.Fullscrape()

class ScrapeWindow(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self, parent,id, title,browser,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(280, 220) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour(   (245,222,179))
        curdir = os.getcwd()
        obj = browserops.BrowserOperations()
        self.socketIO = socketIO
        obj.openBrowser(browser)
        self.iconpath = curdir + "\\slk.ico"
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 5)
        self.icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap(self.iconpath))
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.sizer.Add(self.icon, pos=(0, 3), flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT,
                       border=5)


        self.startbutton = wx.Button(self.panel, label="Start ClickAndAdd",pos=(12,8 ), size=(175, 28))
        self.startbutton.Bind(wx.EVT_BUTTON, self.startcliclandadd)   # need to implement OnExtract()
        self.startbutton.SetToolTip(wx.ToolTip("To START Click and Add Scraping"))
        self.stopbutton = wx.Button(self.panel, label="Stop ClickAndAdd", pos=(12,38 ), size=(175, 28))
        self.stopbutton.Bind(wx.EVT_BUTTON, self.stopcliclandadd)   # need to implement OnExtract()
        self.stopbutton.SetToolTip(wx.ToolTip("To STOP Click and Add Scraping"))
        self.stopbutton.Disable()
        self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,68 ), size=(175, 28))
        self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()
        self.fullscrapebutton.SetToolTip(wx.ToolTip("To perform FULLSCRAPE Scraping"))
        self.savescrapebutton = wx.Button(self.panel, label="Save Scrape",pos=(12,98 ), size=(175, 28))
        self.savescrapebutton.Bind(wx.EVT_BUTTON, self.savescrape)   # need to implement OnExtract()
        self.savescrapebutton.SetToolTip(wx.ToolTip("To save SCRAPE data"))
        self.savescrapebutton.Disable()
        self.label1 = wx.StaticText(self.panel,label = "@ 2017 SLK Software Services Pvt. Ltd.",pos=(12,128 ), size=(220, 28))
        self.label1 = wx.StaticText(self.panel,label =" All Rights Reserved. Patent Pending",pos=(12,158 ), size=(220, 28))

        self.sizer.AddGrowableCol(2)
        self.panel.SetSizer(self.sizer)
        self.Centre()
        style = self.GetWindowStyle()
        self.SetWindowStyle( style|wx.STAY_ON_TOP )
        wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
##        self.Show()



    #----------------------------------------------------------------------
    def OnExit(self, event):
        self.Close()
        driver = browserops.driver
        driver.close()

    #----------------------------------------------------------------------
    def stopcliclandadd(self,event):
        self.stopbutton.Disable()
        clickandaddoj.stopclickandadd()
        self.startbutton.Enable()
        self.fullscrapebutton.Enable()
        self.savescrapebutton.Enable()
        print 'Stopped click and add'

    #----------------------------------------------------------------------
    def startcliclandadd(self,event):
        self.startbutton.Disable()
        clickandaddoj.startclickandadd()
        self.stopbutton.Enable()
        self.fullscrapebutton.Disable()
        self.savescrapebutton.Disable()
        print 'click and add initiated, select the elements from AUT'

    #----------------------------------------------------------------------
    def fullscrape(self,event):
        print 'Performing full scrape'
        self.startbutton.Disable()
        fullscrapeobj.fullscrape()
        self.startbutton.Enable()
        self.savescrapebutton.Enable()
        print 'Full scrape  completed'

    #----------------------------------------------------------------------
    def savescrape(self,event):
        print 'Saving scraped data'
        data = clickandadd.vie
        if len(data) > 0:
          d=   clickandaddoj.save_json_data()
        else:
            d = fullscrapeobj.save_json_data()
        self.savescrapebutton.Disable()
        self.socketIO.send(d)

##        self.Close()
##        driver = browserops.driver
##        driver.close()
        print 'Scrapped data saved successfully in domelements.json file'


#----------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App()
    ScrapeWindow(None, title="SLK Nineteen68 - Web Scrapper")
    app.MainLoop()
