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
import core_utils

import cropandadd

browserobj = browserops.BrowserOperations()
clickandaddoj = clickandadd.Clickandadd()
fullscrapeobj = fullscrape.Fullscrape()
cropandaddobj = cropandadd.Cropandadd()

class ScrapeWindow(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self, parent,id, title,browser,socketIO,action,data):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
##        style = wx.CAPTION|wx.CLIP_CHILDREN
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        obj = browserops.BrowserOperations()
        self.socketIO = socketIO
        self.action = action
        self.data = data
        status = obj.openBrowser(browser)
        if status == False:
            self.socketIO.emit('scrape',status)
            driver = browserops.driver
            driver.close()
            self.Close()
        else:
            self.panel = wx.Panel(self)
            self.core_utilsobject = core_utils.CoreUtils()
            if (self.action == 'scrape'):
                self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,18 ), size=(175, 28))
                self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)   # need to implement OnExtract()
                self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,48 ), size=(175, 28))
                self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()
                self.cropbutton = wx.ToggleButton(self.panel, label="Start IRIS",pos=(12,78 ), size=(175, 28))
                self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)

            elif(self.action == 'compare'):
                browserops.driver.get(data['scrapedurl'])
                self.comparebutton = wx.ToggleButton(self.panel, label="Start Compare",pos=(12,38 ), size=(175, 28))
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
            self.cropbutton.Disable()
            status = clickandaddoj.startclickandadd()
            event.GetEventObject().SetLabel("Stop ClickAndAdd")
##            wx.MessageBox('CLICKANDADD: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
            if status.lower() == 'fail':
                self.socketIO.emit('scrape',status)
                self.Close()
            else:
                print 'click and add initiated, select the elements from AUT'

        else:
            d = clickandaddoj.stopclickandadd()
            print 'Scrapped data saved successfully in domelements.json file'

            # 10 is the limit of MB set as per Nineteen68 standards
            if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                if  isinstance(d,str):
                    if d.lower() == 'fail':
                        self.socketIO.emit('scrape',d)
                else:
                    self.socketIO.emit('scrape',d)
            else:
                print 'Scraped data exceeds max. Limit.'
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

##            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.Close()
            event.GetEventObject().SetLabel("Start ClickAndAdd")
            print 'Click and add scrape  completed'

    def compare(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            obj = objectspy.Object_Mapper()
            event.GetEventObject().SetLabel("Comparing...")
            self.comparebutton.Disable()
            d = obj.perform_compare(self.data)
            if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                if  isinstance(d,str):
                    if d.lower() == 'fail':
                        self.socketIO.emit('scrape',d)
                else:
                    self.socketIO.emit('scrape',d)
                    print 'Compare completed'
            else:
                print 'data exceeds max. Limit.'
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
            self.Close()


    #----------------------------------------------------------------------
    def fullscrape(self,event):
        print 'Performing full scrape'
        self.startbutton.Disable()
        self.cropbutton.Disable()
        d = fullscrapeobj.fullscrape()

        # 10 is the limit of MB set as per Nineteen68 standards
        if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
            if  isinstance(d,str):
                if d.lower() == 'fail':
                    self.socketIO.emit('scrape',d)
            else:
                self.socketIO.emit('scrape',d)
                print 'Full scrape  completed'
        else:
            print 'Scraped data exceeds max. Limit.'
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.Close()

    def cropandadd(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton.Disable()
            self.startbutton.Disable()
            event.GetEventObject().SetLabel("Stop IRIS")
            status = cropandaddobj.startcropandadd()
        else:
            self.Hide()
            import cv2
            cv2.destroyAllWindows()
            time.sleep(1)
            d = cropandaddobj.stopcropandadd()
            print 'Scrapped data saved successfully in domelements.json file'
            self.socketIO.emit('scrape',d)
            self.Close()
            event.GetEventObject().SetLabel("Start IRIS")
            print 'Crop and add scrape completed'




