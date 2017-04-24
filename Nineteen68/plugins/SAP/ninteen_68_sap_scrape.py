#-------------------------------------------------------------------------------
# Name:        Ninteen_68_sap_scrape
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
##import clientwindow
from socketIO_client import SocketIO,BaseNamespace
import launch_keywords
sap_scraping_obj = sap_scraping.Scrape()
import os
from constants import *
import logger
import win32com.client
import logging
import logging.config
log = logging.getLogger('clientwindow.py')

from text_keywords_sap import Text_Keywords

import json

import time
import win32gui
import win32ui
import win32process
import win32con
import win32api
from ctypes import windll
from PIL import Image
import base64

obj=None
class ScrapeWindow(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        global obj
        #logger.print_on_console("going to launch_keywords")
        obj = launch_keywords.Launch_Keywords()
        self.socketIO = socketIO
        fileLoc=filePath.split(';')[0]
        windowname=filePath.split(';')[1]
        input_val=[]
        input_val.append(fileLoc)
        input_val.append(windowname)
        input_val.append(5)
        status = obj.launch_application(input_val)
        print status
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



    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton.Disable()
            print 'calling start click and add'
            sap_scraping_obj.clickandadd('STARTCLICKANDADD')
            event.GetEventObject().SetLabel("Stop ClickAndAdd")
        else:
            print 'calling stop click and add'
            d = sap_scraping_obj.clickandadd('STOPCLICKANDADD')
            #print 'returning data---------------------------',d
            event.GetEventObject().SetLabel("Start ClickAndAdd")

            self.socketIO.emit('scrape',d)

            self.Close()

    def fullscrape(self,event):
        tk=Text_Keywords()
        #logger.print_on_console('Performing full scrape')
        self.startbutton.Disable()
        #logger.print_on_console('going to SapGui :')
        SapGui=tk.getSapObject()
        #logger.print_on_console('SapGui :',SapGui)
        wndname=sap_scraping_obj.getWindow(SapGui)
        wnd_title = wndname.__getattr__("Text")
        #logger.print_on_console('wndtitle :',wnd_title)
        data={}
        scraped_data = sap_scraping_obj.full_scrape(wndname,wnd_title)
        obj=launch_keywords.Launch_Keywords()

        try:
            img=obj.captureScreenshot(SapGui,scraped_data)
            img.save('out.png')
            with open("out.png", "rb") as image_file:
                      encoded_string = base64.b64encode(image_file.read())
        except Exception as e:
            logger.print_on_console('Error occured while capturing Screenshot ')
            log.error(e)


        data['mirror'] =encoded_string.encode('UTF-8').strip()
        #logger.print_on_console( 'scrape_data before loads',scraped_data)
        data['view'] = scraped_data
        #logger.print_on_console( 'scrape_data before dumping',scraped_data)
        with open('domelements.json', 'w') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=False)
                outfile.close()
        self.socketIO.emit('scrape',data)
        #logger.print_on_console('Full scrape  completed')
        self.Close()








