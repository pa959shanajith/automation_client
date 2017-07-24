#-------------------------------------------------------------------------------
# Name:        scrape_dispatcher.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     15-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import utils
import oebs_fullscrape
import oebsclickandadd
import logger
import logging
import oebs_constants
import wx
import os
import base64
import json
import time
from constants import *
from socketIO_client import SocketIO,BaseNamespace
import core_utils

log = logging.getLogger('scrape_dispatcher.py')
windownametoscrape = ''
class ScrapeDispatcher(wx.Frame):
    print("Enetering inside scrape window")
    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        global obj
        obj = utils.Utils()
        self.utils_obj=utils.Utils()
        self.scrape_obj=oebs_fullscrape.FullScrape()
        self.core_utilsobject = core_utils.CoreUtils()
        global windownametoscrape
        windownametoscrape = filePath
        self.socketIO = socketIO
##        fileLoc=filePath.split(';')[0]
        windowname=filePath
        input_val=[]
##        input_val.append(fileLoc)
        input_val.append(windowname)
        input_val.append(10)
        status = obj.set_to_foreground(windowname)
        if status!=TERMINATE and status:
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

            self.socketIO.emit('scrape','wrongWindowName')


    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        clickandadd_obj=oebsclickandadd.ClickAndAdd()

        if state == True:
            self.fullscrapebutton.Disable()
    ##        self.comparebutton.Disable()

            event.GetEventObject().SetLabel("Stop ClickAndAdd")
            clickandadd_obj.clickandadd(windownametoscrape,'STARTCLICKANDADD')
    ##            wx.MessageBox('CLICKANDADD: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
            logger.print_on_console( 'click and add initiated, select the elements from AUT')

        else:
            d = clickandadd_obj.clickandadd(windownametoscrape,'STOPCLICKANDADD')
            event.GetEventObject().SetLabel("Start ClickAndAdd")


    ##            print desktop_scraping.finalJson
            logger.print_on_console('Stopped click and add')
            logger.print_on_console( 'Scrapped data saved successfully in domelements.json file')
            try:
                self.Iconize(True)
                #providing 1 sec delay to minimize wx scrape window to hide in screenshot
                time.sleep(1)
                img = self.utils_obj.captureScreenshot(windownametoscrape)
                img.save('oebs_form.png')
                with open("oebs_form.png", "rb") as image_file:
                          encoded_string = base64.b64encode(image_file.read())

                d = json.loads(d);
                d['mirror'] =encoded_string.encode('UTF-8').strip()
            except Exception as e:
                logger.print_on_console('Error occured while capturing Screenshot',e)

            #10 is the limit of MB set as per Nineteen68 standards
            if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                self.socketIO.emit('scrape',d)
            else:
                print 'Scraped data exceeds max. Limit.'
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

    ##            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.Close()
    ##            event.GetEventObject().SetLabel("Start ClickAndAdd")
            logger.print_on_console('Click and add scrape  completed')


    def fullscrape(self,event):
        logger.print_on_console('Performing full scrape')
        self.startbutton.Disable()
##        print 'desktop_scraping_obj:',desktop_scraping_obj
####        self.comparebutton.Disable()
        scrape_obj=oebs_fullscrape.FullScrape()
        print("windowname to scrape : ",windownametoscrape)
        d = scrape_obj.getentireobjectlist(windownametoscrape)
        try:
            self.Iconize(True)
            #providing 1 sec delay to minimize wx scrape window to hide in screenshot
            time.sleep(1)
            img = self.utils_obj.captureScreenshot(windownametoscrape)
            img.save('oebs_form.png')
            with open("oebs_form.png", "rb") as image_file:
                      encoded_string = base64.b64encode(image_file.read())
            d = json.loads(d);

            d['mirror'] =encoded_string.encode('UTF-8').strip()
        except Exception as e:
            logger.print_on_console('Error occured while capturing Screenshot ',e)

        #10 is the limit of MB set as per Nineteen68 standards
        if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
            self.socketIO.emit('scrape',d)
        else:
            print 'Scraped data exceeds max. Limit.'
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

        self.Close()
        logger.print_on_console('Full scrape  completed')


    def scrape_dispatcher(self,keyword,*message):
             logger.print_on_console('Keyword is '+keyword)


             if keyword in oebs_constants.OEBS_SCRAPE_KEYWORDS:
                self.utils_obj.find_oebswindow_and_attach(message[0])
                if len(message)>1 and not(message[1].lower()=='stopclickandadd'):
                    self.utils_obj.set_to_foreground(message[0])

             try:
                dict={
                      'highlight':self.utils_obj.higlight,
                      'fullscrape': self.scrape_obj.getentireobjectlist,
                      'clickandadd':self.clickandadd_obj.clickandadd,
                    }
                keyword=keyword.lower()
                if keyword in dict.keys():
                    return dict[keyword](*message)
                else:
                    logger.print_on_console(oebs_constants.INVALID_INPUT)
             except Exception as e:
                log.error(e)
                logger.print_on_console(e)