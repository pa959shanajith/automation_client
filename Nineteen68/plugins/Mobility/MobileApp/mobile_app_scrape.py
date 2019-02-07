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
import android_scrapping
import wx
from socketIO_client import SocketIO,BaseNamespace
##import launch_keywords
##desktop_scraping_obj = desktop_scraping.Scrape()
import os
import logger
obj=android_scrapping.InstallAndLaunch()
import core_utils

class ScrapeWindow(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.core_utilsobject = core_utils.CoreUtils()
        self.parent = parent
        global obj
        #obj = android_scrapping.InstallAndLaunch()

        self.socketIO = socketIO
        apk_path=filePath.split(';')[0]
        serial=filePath.split(';')[1]
        if str(apk_path).endswith("apk"):
            status = obj.installApplication(apk_path, None, serial, None)
        elif filePath.split(';')[4]== "ios":
            deviceName = filePath.split(';')[0]
            platform_version = filePath.split(';')[1]
            bundle_id = filePath.split(';')[2]
            Ip_Address = filePath.split(';')[3]
            status = obj.installApplication(deviceName, platform_version,bundle_id,Ip_Address,"ios")
        if status!=None:
            self.panel = wx.Panel(self)
            self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,38 ), size=(175, 28))
            self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()
            self.Centre()
            style = self.GetWindowStyle()
            self.SetWindowStyle( style|wx.STAY_ON_TOP )
            wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            self.Show()
        else:
            self.socketIO.emit('scrape','Fail')
            self.Close()
            self.parent.schedule.Enable()

     #----------------------------------------------------------------------
##    def OnExit(self, event):
##        self.Close()
##        driver = browserops.driver
##        driver.close()

    #----------------------------------------------------------------------
##    def clickandadd(self,event):
##        state = event.GetEventObject().GetValue()
##        if state == True:
##            self.fullscrapebutton.Disable()
####        self.comparebutton.Disable()
##            desktop_scraping_obj.clickandadd('STARTCLICKANDADD')
##            event.GetEventObject().SetLabel("Stop ClickAndAdd")
####            wx.MessageBox('CLICKANDADD: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
##            print 'click and add initiated, select the elements from AUT'
##
##        else:
##            d = desktop_scraping_obj.clickandadd('STOPCLICKANDADD')
##            event.GetEventObject().SetLabel("Start ClickAndAdd")
##            print 'print json'
##            print d
####            print desktop_scraping.finalJson
##            print 'after click on stop'
##            print 'Scrapped data saved successfully in domelements.json file'
##            self.socketIO.emit('scrape',d)
####            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
##            self.Close()
####            event.GetEventObject().SetLabel("Start ClickAndAdd")
##            print 'Click and add scrape  completed'
##        print 'done'

##    def compare(self,event):
##        state = event.GetEventObject().GetValue()
##        if state == True:
##            self.fullscrapebutton.Disable()
##            self.startbutton.Disable()
##            obj = objectspy.Object_Mapper()
##            obj.compare()
##            event.GetEventObject().SetLabel("Update")
##        else:
##            obj = objectspy.Object_Mapper()
##            d = obj.update()
##            self.socketIO.send(d)
##            self.Close()


    #----------------------------------------------------------------------
    def fullscrape(self,event):
        logger.print_on_console('Performing full scrape')
        d = obj.scrape()
        # 10 is the limit of MB set as per Nineteen68 standards
        if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
            self.socketIO.emit('scrape',d)
        else:
            logger.print_on_console('Scraped data exceeds max. Limit.')
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.parent.schedule.Enable()
        self.Close()
        logger.print_on_console('Full scrape  completed')
