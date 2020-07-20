#-------------------------------------------------------------------------------
# Name:        pdf_scrape_dispatcher
# Purpose:	   PDF dispatcher for PDF utility scraping
#
# Author:      shree.p
#
# Created:
# Copyright:   (c) shree.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import logging
import wx
import os
import base64
import json
import time
from constants import *
import core_utils
pdfV = None
log = logging.getLogger('pdf_scrape_dispatcher.py')
windownametoscrape = ''

class ScrapeDispatcher(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO,irisFlag):
        try:
            wx.Frame.__init__(self, parent, title=title,pos=(300, 150),  size=(210, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            global obj
##        obj = utils.Utils()
##            self.utils_obj=utils.Utils()
            self.core_utilsobject = core_utils.CoreUtils()
            self.irisFlag = irisFlag
            self.parent = parent
            global windownametoscrape
            windownametoscrape = filePath
            self.socketIO = socketIO
            windowname=filePath
            input_val=[]
            self.panel = wx.Panel(self)
            self.startbutton = wx.ToggleButton(self.panel, label="Start PDF",pos=(12,38 ), size=(175, 28))
            self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)   # need to implement OnExtract()
##            self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,38 ), size=(175, 28))
##            self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.clickandadd)   # need to implement OnExtract()
##            if(irisFlag):
##                import cropandadd
##                global cropandaddobj
##                cropandaddobj = cropandadd.Cropandadd()
##                self.cropbutton = wx.ToggleButton(self.panel, label="Start IRIS",pos=(12,68 ), size=(175, 28))
##                self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)
##            self.Centre()
            self.Centre()
            style = self.GetWindowStyle()
            self.SetWindowStyle( style|wx.STAY_ON_TOP )
            wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            self.Show()
        except e as Exception:
            logger.print_on_console('Error at pdf clickandadd')
            log.error(e)

    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        import pdf_main
        from pdf_main import PDFViewer

        if state == True:
            try:
                global pdfV
                pdfV = PDFViewer(None, title="PDF Window", size=(615,850))
                pdfV.Show()
                pdfV.Centre()
            except Exception as e:
                logger.print_on_console('Error at pdf clickandadd')
                log.error(e)

            event.GetEventObject().SetLabel("Stop PDF")
        else:
            event.GetEventObject().SetLabel("Start PDF")
            logger.print_on_console('Stopped click and add')

            logger.print_on_console( 'Scrapped data saved successfully in domelements.json file')
            res = pdfV.OnStop(event)
            ie = {'view': res}
            scrapeJson =  json.dumps(ie)
            d = json.loads(scrapeJson);

            try:
                self.Iconize(True)
                #providing 1 sec delay to minimize wx scrape window to hide in screenshot
                time.sleep(1)
                img = pdfV.capture_window()
                img.save('pdf.png')
                with open("pdf.png", "rb") as image_file:
                          encoded_string = base64.b64encode(image_file.read())

##                d = json.loads(d);
                d['mirror'] =encoded_string.decode('UTF-8').strip()
            except Exception as e:
                logger.print_on_console('Error occured while capturing Screenshot',e)

            if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                self.socketIO.emit('scrape',d)
            else:
                logger.print_on_console('Scraped data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

    ##            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.Close()
            self.parent.schedule.Enable()
    ##            event.GetEventObject().SetLabel("Start ClickAndAdd")
            logger.print_on_console('Click and add scrape  completed')
            pdfV.Destroy()

    def cropandadd(self,event):
        state = event.GetEventObject().GetValue()
        global cropandaddobj
        if state == True:
##            self.fullscrapebutton.Disable()
            self.startbutton.Disable()
            pdfV = PDFViewer(None, size=(615,850))
            pdfV.Show()
            event.GetEventObject().SetLabel("Stop IRIS")
            time.sleep(1)
            status = cropandaddobj.startcropandadd(self)
        else:
            self.Hide()
            import cv2
            cv2.destroyAllWindows()
            time.sleep(1)
            d = cropandaddobj.stopcropandadd()
            logger.print_on_console('Scrapped data saved successfully in domelements.json file')
            self.socketIO.emit('scrape',d)
            self.parent.schedule.Enable()
            self.Close()
            logger.print_on_console('Crop and add scrape completed')