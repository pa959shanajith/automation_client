import wx
import sys
import os
from selenium import webdriver
import browserops
import clickandadd
import fullscrape
import clientwindow
from socketIO_client import SocketIO,BaseNamespace
import time
import objectspy

browserobj = browserops.BrowserOperations()
clickandaddoj = clickandadd.Clickandadd()
fullscrapeobj = fullscrape.Fullscrape()

class ScrapeWindow(wx.Frame):
    print 'pavvvvvvvvvvv'
    #----------------------------------------------------------------------
    def __init__(self, parent,id, title,browser,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.RESIZE_BOX |wx.MAXIMIZE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
##        style = wx.CAPTION|wx.CLIP_CHILDREN
        curdir = os.getcwd()
        self.iconpath = curdir + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        obj = browserops.BrowserOperations()
        self.socketIO = socketIO
        status = obj.openBrowser(browser)
##        if status == 'SUCCESS':
##            self.iconpath = curdir + "\\slk.ico"
        self.panel = wx.Panel(self)
##            self.sizer = wx.GridBagSizer(6, 5)
##            self.icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap(self.iconpath))
##            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
##            self.SetIcon(self.wicon)
##            self.sizer.Add(self.icon, pos=(0, 3), flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT,border=5)

##            self.tbtn = wx.ToggleButton(panel , -1, "click to on")
##            vbox.Add(self.tbtn,0,wx.EXPAND|wx.ALIGN_CENTER)
##            self.tbtn.Bind(wx.EVT_TOGGLEBUTTON,self.OnToggle)

        self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,8 ), size=(175, 28))
        self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)   # need to implement OnExtract()
##            self.startbutton.SetToolTip(wx.ToolTip("To START Click and Add Scraping"))
##            self.startbutton.Show()
##            self.stopbutton = wx.Button(self.panel, label="Stop ClickAndAdd", pos=(12,8 ), size=(175, 28))
##            self.stopbutton.Bind(wx.EVT_BUTTON, self.stopcliclandadd)   # need to implement OnExtract()
##            self.stopbutton.SetToolTip(wx.ToolTip("To STOP Click and Add Scraping"))
##            self.stopbutton.Hide()
        self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,38 ), size=(175, 28))
        self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()

##            self.fullscrapebutton.SetToolTip(wx.ToolTip("To perform FULLSCRAPE Scraping"))
        self.comparebutton = wx.ToggleButton(self.panel, label="Compare",pos=(12,68 ), size=(175, 28))
        self.comparebutton.Bind(wx.EVT_TOGGLEBUTTON, self.compare)   # need to implement OnExtract()
##            self.savescrapebutton.SetToolTip(wx.ToolTip("To save SCRAPE data"))
##            self.savescrapebutton.Disable()
##            self.label1 = wx.StaticText(self.panel,label = "@ 2017 SLK Software Services Pvt. Ltd.",pos=(12,128 ), size=(220, 28))
##            self.label1 = wx.StaticText(self.panel,label =" All Rights Reserved. Patent Pending",pos=(12,158 ), size=(220, 28))

##            self.sizer.AddGrowableCol(2)
##            self.panel.SetSizer(self.sizer)
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

    #----------------------------------------------------------------------
##    def stopcliclandadd(self,event):
####        self.stopbutton.Hide()
##        d = clickandaddoj.stopclickandadd()
####        self.startbutton.Enable()
####        self.fullscrapebutton.Enable()
####        self.savescrapebutton.Enable()
##
##        self.socketIO.send(d)
##        self.Close()
##        print 'Stopped click and add'
##
##    #----------------------------------------------------------------------
##    def startcliclandadd(self,event):
##        self.startbutton.Hide()
##        self.stopbutton.Show()
##        time.sleep(2)
##        clickandaddoj.startclickandadd()
##
##
####        self.stopbutton.Enable()
####        self.fullscrapebutton.Disable()
####        self.savescrapebutton.Disable()
##        print 'click and add initiated, select the elements from AUT'



    #----------------------------------------------------------------------
##    def savescrape(self,event):
##        print 'Saving scraped data
##        data = clickandadd.vie
##        if len(data) > 0:
##          d=   clickandaddoj.save_json_data()
##        else:
##            d = fullscrapeobj.save_json_data()
##        self.savescrapebutton.Disable()
##        self.socketIO.send(d)
##
##        self.Close()
##        driver = browserops.driver
##        driver.close()
##        print 'Scrapped data saved successfully in domelements.json file'


#----------------------------------------------------------------------
##if __name__ == '__main__':
##    app = wx.App()
##    ScrapeWindow(None, title="SLK Nineteen68 - Web Scrapper")
##    app.MainLoop()
