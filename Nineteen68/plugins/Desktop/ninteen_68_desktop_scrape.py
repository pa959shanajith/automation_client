#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     17-02-2017
# Copyright:   (c) rakesh.v 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_scraping
import wx
##import clientwindow
from socketIO_client import SocketIO,BaseNamespace
import launch_keywords
desktop_scraping_obj = desktop_scraping.Scrape()
import os
from constants import *
import logger
import core_utils

obj=None
class ScrapeWindow(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        global obj
        obj = launch_keywords.Launch_Keywords()
        self.core_utilsobject = core_utils.CoreUtils()

        self.socketIO = socketIO
        fileLoc=filePath.split(';')[0]
        windowname=filePath.split(';')[1]
        input_val=[]
        input_val.append(fileLoc)
        input_val.append(windowname)
        input_val.append(5)
        status = obj.launch_application(input_val)
        if status!=TERMINATE:
            self.panel = wx.Panel(self)
            self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,8 ), size=(175, 28))
            self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)   # need to implement OnExtract()
            self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,38 ), size=(175, 28))
            self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()
            self.Centre()

            self.Centre()
            style = self.GetWindowStyle()
            self.SetWindowStyle( style|wx.STAY_ON_TOP )
            wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            self.Show()
        else:

            self.socketIO.emit('scrape','Fail')


     #----------------------------------------------------------------------
##    def OnExit(self, event):
##        self.Close()
##        driver = browserops.driver
##        driver.close()

    #----------------------------------------------------------------------
    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton.Disable()
##        self.comparebutton.Disable()
            desktop_scraping_obj.clickandadd('STARTCLICKANDADD')
            event.GetEventObject().SetLabel("Stop ClickAndAdd")
##            wx.MessageBox('CLICKANDADD: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
            logger.print_on_console( 'click and add initiated, select the elements from AUT')

        else:
            d = desktop_scraping_obj.clickandadd('STOPCLICKANDADD')
            event.GetEventObject().SetLabel("Start ClickAndAdd")


##            print desktop_scraping.finalJson
            logger.print_on_console('Stopped click and add')
            logger.print_on_console( 'Scrapped data saved successfully in domelements.json file')

            # 5 is the limit of MB set as per Nineteen68 standards
            if self.core_utilsobject.getdatasize(str(d),'mb') < 5:
                self.socketIO.emit('scrape',d)
            else:
                print 'Scraped data exceeds max. Limit.'
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

##            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.Close()
##            event.GetEventObject().SetLabel("Start ClickAndAdd")
            logger.print_on_console('Click and add scrape  completed')





    #----------------------------------------------------------------------
    def fullscrape(self,event):
        logger.print_on_console('Performing full scrape')
        self.startbutton.Disable()
##        print 'desktop_scraping_obj:',desktop_scraping_obj
####        self.comparebutton.Disable()
        d = desktop_scraping_obj.full_scrape()
        # 5 is the limit of MB set as per Nineteen68 standards
        if self.core_utilsobject.getdatasize(str(d),'mb') < 5:
            self.socketIO.emit('scrape',d)
        else:
            print 'Scraped data exceeds max. Limit.'
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.Close()
        logger.print_on_console('Full scrape  completed')



