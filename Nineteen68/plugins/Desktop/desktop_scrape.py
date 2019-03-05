#-------------------------------------------------------------------------------
# Name:        desktop_scrape.py
# Purpose:     acts as a control for scraped objects
#
# Author:      wasimakram.sutar,anas.ahmed
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

cropandaddobj = None
backend_process = None
obj=None

class ScrapeWindow(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO,irisFlag):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        global obj
        obj = desktop_launch_keywords.Launch_Keywords()
        self.socketIO = socketIO
        self.core_utilsobject = core_utils.CoreUtils()
        self.parent = parent
        windowname=filePath[0]
        pid=filePath[1]
        self.backend_process=filePath[2]
        global backend_process
        backend_process=self.backend_process
        input_val=[]
        verify_pname = None
        if (windowname!=None or windowname.strip()!='') and (pid==None or pid ==''):
            input_val.append(windowname)
            input_val.append(5)
            status = obj.find_window_and_attach(input_val)
            verify_pname = status[0].lower()
        elif (windowname==None or windowname.strip()=='') and (pid!=None or pid !=''):
            input_val.append(int(pid))
            input_val.append(5)
            status = obj.find_window_and_attach_pid(input_val)
        elif (windowname!=None or windowname.strip()!='') and (pid!=None or pid !=''):
            input_val.append(windowname)
            input_val.append(5)
            status = obj.find_window_and_attach(input_val)
            if status[0].lower() == 'fail':
                input_val=[]
                input_val.append(int(pid))
                input_val.append(5)
                status = obj.find_window_and_attach_pid(input_val)
        self.irisFlag = irisFlag
        if desktop_launch_keywords.app_uia != None and desktop_launch_keywords.app_win32 != None and status[0].lower() != 'fail':
            if status!=TERMINATE:
                self.panel = wx.Panel(self)
                self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,8 ), size=(175, 28))
                self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)   # need to implement OnExtract()
                self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,38 ), size=(175, 28))
                self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()
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
                self.parent.schedule.Enable()
        elif verify_pname == 'fail':
            self.socketIO.emit('scrape','Fail')
            logger.print_on_console('Wrong Window Name, Please check the Window Name and provide valid one')
            self.parent.schedule.Enable()
        else:
            self.socketIO.emit('scrape','Fail')
            logger.print_on_console('Wrong Process Id, Please check the Process Id and provide valid one')
            self.parent.schedule.Enable()
        windowname = ''
     #----------------------------------------------------------------------

    #----------------------------------------------------------------------
    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        if desktop_launch_keywords.app_uia != None and desktop_launch_keywords.app_win32 != None:
            if state == True:
                self.fullscrapebutton.Disable()
                if(self.irisFlag):
                    self.cropbutton.Disable()
                desktop_scraping_obj.clickandadd('STARTCLICKANDADD',self)
                event.GetEventObject().SetLabel("Stop ClickAndAdd")
                logger.print_on_console( 'click and add initiated, select the elements from AUT')

            else:
                data={}
                data['view'] = desktop_scraping_obj.clickandadd('STOPCLICKANDADD',self)
                event.GetEventObject().SetLabel("Start ClickAndAdd")
                logger.print_on_console('Stopped click and add')
                #--------------
                self.Hide()
                time.sleep(1)
                #--------------
                try:
                    img=obj.captureScreenshot()
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
                        msg='Error occured while capturing Screenshot '
                        log.error(msg)
                        log.error(e)
                        logger.print_on_console(msg)
                data['mirror'] =encoded_string.decode('UTF-8').strip()
                #10 is the limit of MB set as per Nineteen68 standards
                if self.core_utilsobject.getdatasize(str(data),'mb') < 10:
                    self.socketIO.emit('scrape',data)
                else:
                    logger.print_on_console( 'Scraped data exceeds max. Limit.')
                    self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
                os.remove("out.png")
                self.parent.schedule.Enable()
                self.Close()
                logger.print_on_console('Click and add scrape  completed successfully...')
        else:
            logger.print_on_console('Click and add Scrape Failed')
            self.parent.schedule.Enable()


    #----------------------------------------------------------------------
    def fullscrape(self,event):
        logger.print_on_console('Performing full scrape...')
        self.startbutton.Disable()
        if(self.irisFlag):
            self.cropbutton.Disable()
        if desktop_launch_keywords.app_uia != None and desktop_launch_keywords.app_win32 != None:
            data={}
            data['view'] = desktop_scraping_obj.full_scrape(self)
            #-------------
            self.Hide()
            time.sleep(1)
            #--------------
            try:
                img=obj.captureScreenshot()
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
                    msg='Error occured while capturing Screenshot '
                    log.error(msg)
                    log.error(e)
                    logger.print_on_console(msg)
            data['mirror'] =encoded_string.decode('UTF-8').strip()
            if self.core_utilsobject.getdatasize(str(data),'mb') < 10:
                self.socketIO.emit('scrape',data)
            else:
                logger.print_on_console( 'Scraped data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
            os.remove("out.png")
            self.Close()
            logger.print_on_console('Full scrape  completed successfully...')
        else:
            logger.print_on_console('Full scrape Failed..')
        self.parent.schedule.Enable()

    def cropandadd(self,event):
        state = event.GetEventObject().GetValue()
        global cropandaddobj
        obj=desktop_launch_keywords.Launch_Keywords()
        if state == True:
            obj.set_to_foreground()
            self.fullscrapebutton.Disable()
            self.startbutton.Disable()
            event.GetEventObject().SetLabel("Stop IRIS")
            time.sleep(1)
            status = cropandaddobj.startcropandadd(self)
        else:
            self.Hide()
            import cv2
            cv2.destroyAllWindows()
            time.sleep(1)
            d = cropandaddobj.stopcropandadd()
            logger.print_on_console('Scraped data saved successfully in domelements.json file')
            self.socketIO.emit('scrape',d)
            self.parent.schedule.Enable()
            self.Close()
            logger.print_on_console('Crop and add scrape completed')