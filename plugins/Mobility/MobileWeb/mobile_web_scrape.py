import wx
import sys
import os
from selenium import webdriver
import browserops_MW
import clickandadd_MW
import fullscrape_MW
from constants import SYSTEM_OS
from socketIO_client import SocketIO,BaseNamespace
import time
import objectspy_MW
import core_utils
import platform
import logger

#browserobj = browserops_MW.BrowserOperations()
clickandadd_MWoj = clickandadd_MW.clickandadd_MW()
fullscrape_MWobj = fullscrape_MW.fullscrape_MW()

class ScrapeWindow(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self, parent,id, title,browser,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        obj = browserops_MW.BrowserOperations()
        self.socketIO = socketIO
        status = obj.openBrowser(browser)
        self.panel = wx.Panel(self)
        self.core_utilsobject = core_utils.CoreUtils()
        self.parent = parent
        #if SYSTEM_OS== "Darwin":
        self.startbutton = wx.ToggleButton(self.panel, label="Start clickandadd",pos=(12,8 ), size=(175, 28))
        self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd_MW)   # need to implement OnExtract()
        self.fullscrape_MWbutton = wx.Button(self.panel, label="Full Scrape",pos=(12,48 ), size=(175, 28))
        self.fullscrape_MWbutton.Bind(wx.EVT_BUTTON, self.fullscrape_MW)   # need to implement OnExtract()

##            self.fullscrape_MWbutton.SetToolTip(wx.ToolTip("To perform fullscrape_MW Scraping"))
        #if SYSTEM_OS != "Darwin":
        # self.comparebutton = wx.ToggleButton(self.panel, label="Compare",pos=(12,68 ), size=(175, 28))
        # self.comparebutton.Bind(wx.EVT_TOGGLEBUTTON, self.compare)   # need to implement OnExtract()
        self.Centre()
        style = self.GetWindowStyle()
        self.SetWindowStyle( style|wx.STAY_ON_TOP )
        wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Show()



    #----------------------------------------------------------------------
    def OnExit(self, event):
        self.Close()
        driver = browserops_MW.driver
        driver.close()

    #----------------------------------------------------------------------
    def clickandadd_MW(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrape_MWbutton.Disable()
            #self.comparebutton.Disable()
            clickandadd_MWoj.startclickandadd_MW()
            event.GetEventObject().SetLabel("Stop clickandadd")
##            wx.MessageBox('clickandadd_MW: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
            logger.print_on_console('click and add initiated, select the elements from AUT')

        else:
            d = clickandadd_MWoj.stopclickandadd_MW()
            logger.print_on_console('Scrapped data saved successfully in domelements.json file')

            #10 is the limit of MB set as per Avo Assure standards
            if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                self.socketIO.emit('scrape',d)
            else:
                logger.print_on_console('Scraped data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

##            wx.MessageBox('clickandadd_MW: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.parent.schedule.Enable()
            self.Close()
            event.GetEventObject().SetLabel("Start clickandadd_MW")
            logger.print_on_console('Click and add scrape  completed')

    def compare(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrape_MWbutton.Disable()
            self.startbutton.Disable()
            obj = objectspy_MW.Object_Mapper()
            obj.compare()
            event.GetEventObject().SetLabel("Update")
        else:
            obj = objectspy_MW.Object_Mapper()
            d = obj.update()
            self.socketIO.send(d)
            self.Close()


    #----------------------------------------------------------------------
    def fullscrape_MW(self,event):
        logger.print_on_console('Performing full scrape')
        d = fullscrape_MWobj.fullscrape_MW()


        #10 is the limit of MB set as per Avo Assure standards
        if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
            self.socketIO.emit('scrape',d)
        else:
            logger.print_on_console('Scraped data exceeds max. Limit.')
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.parent.schedule.Enable()
        self.Close()
        if d != 'FAIL':
            logger.print_on_console('Full scrape  completed')
        else:
            logger.print_on_console('Full scrape not Done')


