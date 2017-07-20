#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     29/05/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_scraping
from pywinauto.application import Application
import pywinauto
import wx
##import clientwindow
from socketIO_client import SocketIO,BaseNamespace
import desktop_launch_keywords
desktop_scraping_obj = desktop_scraping.Scrape()
import os
from constants import *
import logger
import core_utils
#--------------------
import time
import win32gui
import base64
#-------------------
obj=None
class ScrapeWindow(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        global obj
        obj = desktop_launch_keywords.Launch_Keywords()
        self.socketIO = socketIO
        self.core_utilsobject = core_utils.CoreUtils()
        windowname=filePath.split(';')[0]
        input_val=[]
        input_val.append(windowname)
        input_val.append(5)
        status = obj.find_window_and_attach(input_val)
        if desktop_launch_keywords.app_uia != None and status[0].lower() != 'fail':
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
        else:
            self.socketIO.emit('scrape','Fail')
            logger.print_on_console('Wrong window name, Please check the window name and provide valid one')

        windowname = ''
     #----------------------------------------------------------------------

    #----------------------------------------------------------------------
    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        app_uia = desktop_launch_keywords.app_uia
        window_name = desktop_launch_keywords.window_name
        if app_uia != None:
            if state == True:
                self.fullscrapebutton.Disable()
    ##        self.comparebutton.Disable()
                desktop_scraping_obj.clickandadd('STARTCLICKANDADD',self)
                event.GetEventObject().SetLabel("Stop ClickAndAdd")
                logger.print_on_console( 'click and add initiated, select the elements from AUT')

            else:
                data={}
                d = desktop_scraping_obj.clickandadd('STOPCLICKANDADD',self)
                event.GetEventObject().SetLabel("Start ClickAndAdd")
                logger.print_on_console('Stopped click and add')
                objc=desktop_launch_keywords.Launch_Keywords()
                #--------------
                self.Hide()
                time.sleep(1)
                #--------------
                try:
                    img=objc.captureScreenshot()
                    img.save('out.png')
                    with open("out.png", "rb") as image_file:
                              encoded_string = base64.b64encode(image_file.read())
                except Exception as e:
                    try:
                        img=obj.capture_window( win32gui.GetDesktopWindow())
                        img.save('out.png')
                        with open("out.png", "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        logger.print_on_console('Error occured while capturing Screenshot ')
                data['mirror'] =encoded_string.encode('UTF-8').strip()
                data['view'] = d
                # 5 is the limit of MB set as per Nineteen68 standards
                if self.core_utilsobject.getdatasize(str(data),'mb') < 5:
                    self.socketIO.emit('scrape',data)
                else:
                    logger.print_on_console( 'Scraped data exceeds max. Limit.')
                    self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
                os.remove("out.png")
                self.Close()
                logger.print_on_console('Click and add scrape  completed successfully...')
        else:
            logger.print_on_console('Click and add Scrape Failed')


    #----------------------------------------------------------------------
    def fullscrape(self,event):
        logger.print_on_console('Performing full scrape...')
        self.startbutton.Disable()
##        print 'desktop_scraping_obj:',desktop_scraping_obj
####        self.comparebutton.Disable()
        app_uia = desktop_launch_keywords.app_uia
        if app_uia != None:
            data={}
            d = desktop_scraping_obj.full_scrape(app_uia,self)
            objc=desktop_launch_keywords.Launch_Keywords()
            #-------------
            self.Hide()
            time.sleep(1)
            #--------------
            try:
                img=objc.captureScreenshot()
                img.save('out.png')
                with open("out.png", "rb") as image_file:
                          encoded_string = base64.b64encode(image_file.read())
            except Exception as e:
                try:
                    img=obj.capture_window( win32gui.GetDesktopWindow())
                    img.save('out.png')
                    with open("out.png", "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.print_on_console('Error occured while capturing Screenshot ')
            data['mirror'] =encoded_string.encode('UTF-8').strip()
            data['view'] = d
            if self.core_utilsobject.getdatasize(str(data),'mb') < 5:
                self.socketIO.emit('scrape',data)
            else:
                logger.print_on_console( 'Scraped data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
            os.remove("out.png")
            self.Close()
            logger.print_on_console('Full scrape  completed successfully...')
        else:
            logger.print_on_console('Full scrape Failed..')




