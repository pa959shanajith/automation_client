#-------------------------------------------------------------------------------
# Name:        sap_scrape
# Purpose:     Module that acts as a control for ClickAndAdd and  FullScrape
#
# Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_scraping
import wx
from socketIO_client import SocketIO,BaseNamespace
import sap_launch_keywords
sap_scraping_obj = sap_scraping.Scrape()
import os
from constants import *
import logger
import logging
import logging.config
log = logging.getLogger('clientwindow.py')
from saputil_operations import SapUtilKeywords
import json
import time
import base64
import core_utils
cropandaddobj = None
obj=None

class ScrapeWindow(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO,irisFlag):
        self.uk=SapUtilKeywords()
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.core_utilsobject = core_utils.CoreUtils()

        global obj
        obj = sap_launch_keywords.Launch_Keywords()
        self.socketIO = socketIO
        fileLoc=filePath.split(';')[0]
        windowname=filePath.split(';')[1]
        input_val=[]
        input_val.append(fileLoc)
        input_val.append(windowname)
        status = obj.launch_application(input_val)
        self.irisFlag = irisFlag
        if status!=TERMINATE:
            self.panel = wx.Panel(self)
            self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,8 ), size=(175, 28))
            self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)
            self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,38 ), size=(175, 28))
            self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)
            if(irisFlag):
                import cropandadd
                global cropandaddobj
                cropandaddobj = cropandadd.Cropandadd()
                self.cropbutton = wx.ToggleButton(self.panel, label="Start IRIS",pos=(12,68 ), size=(175, 28))
                self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)
            self.Centre()
            style = self.GetWindowStyle()
            self.SetWindowStyle( style|wx.STAY_ON_TOP )
            wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            self.Show()
        else:
            self.socketIO.emit('scrape','Fail')



    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton.Disable()
            if(self.irisFlag):
                self.cropbutton.Disable()
            sap_scraping_obj.clickandadd('STARTCLICKANDADD')
            event.GetEventObject().SetLabel("Stop ClickAndAdd")
        else:
            data={}
            d = sap_scraping_obj.clickandadd('STOPCLICKANDADD')
            event.GetEventObject().SetLabel("Start ClickAndAdd")
            SapGui=self.uk.getSapObject()
            obj=sap_launch_keywords.Launch_Keywords()
            wndname=sap_scraping_obj.getWindow(SapGui)
            wnd_title = wndname.__getattr__("Text")
            wnd_id = wndname.__getattr__("Id")
            try:
                self.Hide()
                time.sleep(1)
                img=obj.captureScreenshot(wnd_title, wnd_id)
                img.save('out.png')
                with open("out.png", "rb") as image_file:
                          encoded_string = base64.b64encode(image_file.read())
            except Exception as e:
                logger.print_on_console('Error occured while capturing Screenshot ')
                log.error(e)
            data['mirror'] =encoded_string.encode('UTF-8').strip()
            data['view'] = d
            # 10 is the limit of MB set as per Nineteen68 standards
            if self.core_utilsobject.getdatasize(str(data),'mb') < 10:
                self.socketIO.emit('scrape',data)
            else:
                logger.print_on_console('Scraped data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

            os.remove("out.png")
            self.Close()

    def fullscrape(self,event):
        self.startbutton.Disable()
        if(self.irisFlag):
            self.cropbutton.Disable()
        SapGui=self.uk.getSapObject()
        wndname=sap_scraping_obj.getWindow(SapGui)
        wnd_title = wndname.__getattr__("Text")
        wnd_id = wndname.__getattr__("Id")
        data={}
        scraped_data = sap_scraping_obj.full_scrape(wndname,wnd_title)
        obj=sap_launch_keywords.Launch_Keywords()
        self.Hide()
        time.sleep(1)
        try:
            img=obj.captureScreenshot(wnd_title,wnd_id)
            img.save('out.png')
            with open("out.png", "rb") as image_file:
                      encoded_string = base64.b64encode(image_file.read())
        except Exception as e:
            logger.print_on_console('Error occured while capturing Screenshot ')
            log.error(e)


        data['mirror'] =encoded_string.encode('UTF-8').strip()
        data['view'] = scraped_data
##        with open('domelements.json', 'w') as outfile:
##                json.dump(data, outfile, indent=4, sort_keys=False)
##                outfile.close()

        # 10 is the limit of MB set as per Nineteen68 standards
        if self.core_utilsobject.getdatasize(str(data),'mb') < 10:
            self.socketIO.emit('scrape',data)
        else:
            print 'Scraped data exceeds max. Limit.'
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

        os.remove("out.png")
        self.Close()

    def cropandadd(self,event):
        SapGui=self.uk.getSapObject()
        wndname=sap_scraping_obj.getWindow(SapGui)
        state = event.GetEventObject().GetValue()
        global cropandaddobj
        if state == True:
            self.fullscrapebutton.Disable()
            self.startbutton.Disable()
            event.GetEventObject().SetLabel("Stop IRIS")
            status = cropandaddobj.startcropandadd(self)
        else:
            self.Hide()
            import cv2
            cv2.destroyAllWindows()
            time.sleep(1)
            d = cropandaddobj.stopcropandadd()
            self.socketIO.emit('scrape',d)
            self.Close()
            event.GetEventObject().SetLabel("Start IRIS")






