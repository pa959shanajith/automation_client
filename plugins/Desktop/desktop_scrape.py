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
import desktop_launch_keywords
desktop_scraping_obj = desktop_scraping.Scrape()
import os
from constants import *
import logger
import logging
log = logging.getLogger('desktop_scrape.py')
import core_utils
#--------------------
import time
import win32gui
import base64
#-------------------
cropandaddobj = None
backend_process = None
obj = None
visiblity_status = False

class ScrapeWindow(wx.Frame):
    def __init__(self, parent,id, title, filePath, socketIO):
        try:
            wx.Frame.__init__(self, parent, title = title,
                       pos = (300, 150), size = (360, 310), style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.CLOSE_BOX) )
            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            global obj
            obj = desktop_launch_keywords.Launch_Keywords()
            self.socketIO = socketIO
            self.core_utilsobject = core_utils.CoreUtils()
            self.parent = parent
            windowname = filePath[0]
            pid = filePath[1]
            self.backend_process = filePath[2]
            global backend_process
            backend_process = self.backend_process
            input_val = []
            self.choice='Manual'
            verify_pname = None
            if ( windowname != None or windowname.strip() != '' ) and ( pid == None or pid == '' ):
                input_val.append(windowname)
                input_val.append(5)
                status = obj.find_window_and_attach(input_val)
                verify_pname = status[0].lower()
            elif ( windowname == None or windowname.strip() == '' ) and ( pid != None or pid != '' ):
                input_val.append(int(pid))
                input_val.append(5)
                status = obj.find_window_and_attach_pid(input_val)
            elif ( windowname != None or windowname.strip() != '' ) and ( pid != None or pid != '' ):
                input_val.append(windowname)
                input_val.append(5)
                status = obj.find_window_and_attach(input_val)
                if ( status[0].lower() == 'fail' ):
                    input_val = []
                    input_val.append(int(pid))
                    input_val.append(5)
                    status = obj.find_window_and_attach_pid(input_val)
            self.scrapeoptions = ['Full', 'Button', 'Textbox', 'Dropdown', 'Tree', 'Radiobutton', 'Checkbox', 'Table', 'List', 'Tab', 'DateTimePicker', 'Other Tags']
            self.tag_map = {'Full':'full','Button':'button', 'Textbox':'input', 'Dropdown':'select', 'Tree':'tree', 'Radiobutton':'radiobutton', 'Checkbox':'checkbox', 'Table':'table', 'List':'list', 'Tab':'tab', 'DateTimePicker':'datepicker', 'Other Tags':'label'}
            self.delay_time=["0s","5s","10s","15s","20s","25s"]
            self.delay_time_map={"0s":0,"5s":5,"10s":10,"15s":15,"20s":20,"25s":25}
            if ( desktop_launch_keywords.app_uia != None and desktop_launch_keywords.app_win32 != None and status[0].lower() != 'fail' ):
                if ( status != TERMINATE ):
                    self.panel = wx.Panel(self)
                    self.vsizer = wx.BoxSizer(wx.VERTICAL)
                    self.startbutton = wx.ToggleButton(self.panel, label = "Start ClickAndAdd", pos = (20, 20), size = (300, 30))
                    self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)
                    self.startbutton.SetToolTip(wx.ToolTip( "Elements will be scraped via Click and Add method." ))

                    self.fullscrapedropdown = wx.ComboBox(self.panel, value = "Full", pos = (20, 60), size = (145, 30), choices = self.scrapeoptions, style = wx.CB_DROPDOWN)
                    self.fullscrapedropdown.SetEditable(False)
                    self.fullscrapedropdown.SetToolTip(wx.ToolTip( "Full objects will be scraped" ))

                    self.fullscrapebutton = wx.Button(self.panel, label = "Scrape", pos = (175, 60), size = (145, 30))
                    self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)

                    self.visibilityCheck = wx.CheckBox(self.panel, label = "Visibility", pos = (20,100), size = (80, 30))
                    self.visibilityCheck.Bind(wx.EVT_CHECKBOX, self.visibility)

                    self.delaytext=wx.StaticText(self.panel, label="Delay", pos=(175,100), size=(40,30), style=0, name="")
                    self.scrapeDelaydropdown = wx.ComboBox(self.panel, value = "0s", pos = (225,100), size = (55, 25), choices = self.delay_time, style = wx.CB_DROPDOWN)
                    self.scrapeDelaydropdown.SetEditable(False)
                    self.scrapeDelaydropdown.SetToolTip(wx.ToolTip( "Set delay time before start of scraping." ))
                    #radio buttons
                    
                    lblList = ['Manual', 'Auto']
                    self.rbox = wx.RadioBox(self.panel,label = 'Capture options',  choices = lblList , pos = (20, 140), size = (300,60), style = wx.RA_SPECIFY_COLS)
                    self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)

                    import cropandadd
                    import cropandadd_auto


                    global cropandaddobj_manual
                    global cropandaddobj_auto

                    cropandaddobj_manual = cropandadd.Cropandadd()
                    cropandaddobj_auto = cropandadd_auto.Cropandadd()
                    self.cropbutton = wx.ToggleButton(self.panel, label = "Start IRIS", pos=(20, 210), size = (300, 30))
                    self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)
                    self.Centre()
                    style = self.GetWindowStyle()
                    self.SetWindowStyle( style|wx.STAY_ON_TOP )
                    wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
                    self.Show()
                else:
                    self.socketIO.emit('scrape','Terminate')
                    self.parent.schedule.Enable()
                    time.sleep(1)
                    self.Close()
            elif ( verify_pname == 'fail' ):
                self.socketIO.emit('scrape', 'wrongWindowName')
                logger.print_on_console( 'Wrong Window Name, Please check the Window Name and provide valid one' )
                self.Hide()
                time.sleep(1)
                self.parent.schedule.Enable()
                self.Close()
            else:
                self.socketIO.emit('scrape', 'Fail')
                logger.print_on_console( 'Wrong Process Id, Please check the Process Id and provide valid one' )
                self.parent.schedule.Enable()
                time.sleep(1)
                self.Close()
            windowname = ''
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
    #----------------------------------------------------------------------

    #--------------------------------------------------------Click and Add Logic
    def clickandadd(self, event):
        try:
            state = event.GetEventObject().GetValue()
            if ( desktop_launch_keywords.app_uia != None and desktop_launch_keywords.app_win32 != None ):
                if ( state == True ):
                    time.sleep(self.delay_time_map[self.scrapeDelaydropdown.GetValue()])
                    self.fullscrapebutton.Disable()
                    self.fullscrapedropdown.Disable()
                    self.scrapeDelaydropdown.Disable()
                    self.visibilityCheck.Disable()
                    self.cropbutton.Disable()
                    desktop_scraping_obj.clickandadd('STARTCLICKANDADD', self)
                    event.GetEventObject().SetLabel("Stop ClickAndAdd")
                    logger.print_on_console( 'click and add initiated, select the elements from AUT' )

                else:
                    data = {}
                    data['view'] = desktop_scraping_obj.clickandadd('STOPCLICKANDADD', self)
                    event.GetEventObject().SetLabel("Start ClickAndAdd")
                    logger.print_on_console('Stopped click and add')
                    #--------------
                    self.Hide()
                    time.sleep(1)
                    #--------------
                    try:
                        img = obj.captureScreenshot()
                        img.save('out.png')
                        with open("out.png", "rb") as image_file:
                                  encoded_string = base64.b64encode(image_file.read())
                    except Exception as e:
                        try:
                            img = obj.capture_window( win32gui.GetDesktopWindow())
                            img.save('out.png')
                            with open("out.png", "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                        except Exception as e:
                            logger.print_on_console( 'Error occured while capturing Screenshot' )
                            log.error(e)
                    data['mirror'] = encoded_string.decode('UTF-8').strip()
                    #10 is the limit of MB set as per Avo Assure standards
                    if self.core_utilsobject.getdatasize(str(data), 'mb') < 10:
                        self.socketIO.emit('scrape', data)
                    else:
                        logger.print_on_console( 'Scraped data exceeds max. Limit.')
                        self.socketIO.emit('scrape', 'Response Body exceeds max. Limit.')
                    os.remove("out.png")
                    self.parent.schedule.Enable()
                    self.Close()
                    logger.print_on_console( 'Click and add scrape  completed successfully...' )
            else:
                logger.print_on_console( 'Click and add Scrape Failed' )
                self.parent.schedule.Enable()
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

    #----------------------------------------------------------Full Scrape Logic
    def fullscrape(self, event):
        try:
            logger.print_on_console( 'Performing full scrape...' )
            self.startbutton.Disable()
            self.fullscrapedropdown.Disable()
            self.scrapeDelaydropdown.Disable()
            self.visibilityCheck.Disable()
            self.cropbutton.Disable()
            if ( desktop_launch_keywords.app_uia != None and desktop_launch_keywords.app_win32 != None ):
                time.sleep(self.delay_time_map[self.scrapeDelaydropdown.GetValue()])
                data = {}
                scraped_data = self.OnFullscrapeChoice(desktop_scraping_obj.full_scrape(self), self.fullscrapedropdown.GetValue())
                #-------------
                self.Hide()
                time.sleep(1)
                #--------------
                try:
                    img = obj.captureScreenshot()
                    img.save('out.png')
                    with open("out.png", "rb") as image_file:
                              encoded_string = base64.b64encode(image_file.read())
                except Exception as e:
                    try:
                        img = obj.capture_window( win32gui.GetDesktopWindow())
                        img.save('out.png')
                        with open("out.png", "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                    except Exception as e:
                        logger.print_on_console( 'Error occured while capturing Screenshot' )
                        log.error(e)
                data['view'] = scraped_data
                data['mirror'] = encoded_string.decode('UTF-8').strip()
                if ( self.core_utilsobject.getdatasize(str(data), 'mb') < 10 ):
                    self.socketIO.emit('scrape', data)
                else:
                    logger.print_on_console( 'Scraped data exceeds max. Limit.')
                    self.socketIO.emit('scrape', 'Response Body exceeds max. Limit.')
                os.remove("out.png")
                self.Close()
                logger.print_on_console('Full scrape  completed successfully...')
            else:
                log.error( 'Full scrape Failed...' )
                logger.print_on_console( 'Full scrape Failed...' )
            self.parent.schedule.Enable()
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

    def cropandadd(self, event):
        try:
            state = event.GetEventObject().GetValue()
            global cropandaddobj_manual
            global cropandaddobj_auto
            obj = desktop_launch_keywords.Launch_Keywords()
            if ( state == True ):
                event.GetEventObject().SetLabel("Stop IRIS")
                self.startbutton.Disable()
                self.fullscrapebutton.Disable()
                self.fullscrapedropdown.Disable()
                self.visibilityCheck.Disable()
                self.scrapeDelaydropdown.Disable()
                if (self.delay_time_map[self.scrapeDelaydropdown.GetValue()]>0):
                    time.sleep(self.delay_time_map[self.scrapeDelaydropdown.GetValue()])
                else:
                    obj.set_to_foreground()
                    time.sleep(1)
                    if self.choice=='Auto':
                        status = cropandaddobj_auto.startcropandadd(self)
                        #logger.print_on_console(self.choice)
                    else:
                        status = cropandaddobj_manual.startcropandadd(self)
                        #logger.print_on_console(self.choice)
            else:
                self.Hide()
                import cv2
                cv2.destroyAllWindows()
                time.sleep(1)
                
                if self.choice=='Auto':
                    d = cropandaddobj_auto.stopcropandadd()

                else:
                    d = cropandaddobj_manual.stopcropandadd()

                logger.print_on_console( 'Scraped data saved successfully in domelements.json file' )
                self.socketIO.emit('scrape', d)
                self.parent.schedule.Enable()
                self.Close()
                logger.print_on_console( 'Crop and add scrape completed' )
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

    def OnFullscrapeChoice(self, scrape_data, tag_choice):
        new_data = []
        global visiblity_status
        try:
            tag_choice = self.tag_map[tag_choice]
            if ( tag_choice == 'full' ):
                if ( not visiblity_status ):
                    new_data = scrape_data
                else:
                    for data in scrape_data:
                        if ( data['hiddentag'] == False ):
                            new_data.append(data)
            elif ( tag_choice == 'label' ):
                for data in scrape_data:
                    if ( not visiblity_status ):
                        if ( data['tag'] != 'button' and data['tag'] != 'input' and data['tag'] != 'select' and data['tag'] != 'GuiLabel' and data['tag'] != 'radiobutton' and data['tag'] != 'checkbox' and data['tag'] != 'table' and data['tag'] != 'GuiScrollContainer' and data['tag'] != 'GuiTab' and data['tag'] != 'shell' ):
                            new_data.append(data)
                    elif ( visiblity_status and data['hiddentag'] == False ):
                        if ( data['tag'] != 'button' and data['tag'] != 'input' and data['tag'] != 'select' and data['tag'] != 'GuiLabel' and data['tag'] != 'radiobutton' and data['tag'] != 'checkbox' and data['tag'] != 'table' and data['tag'] != 'GuiScrollContainer' and data['tag'] != 'GuiTab' and data['tag'] != 'shell' ):
                            new_data.append(data)
            else:
                for data in scrape_data:
                    if ( data['tag'] == tag_choice ):
                        if ( not visiblity_status ):
                            new_data.append(data)
                        elif ( visiblity_status and data['hiddentag'] == False ):
                            new_data.append(data)
        except Exception as e:
            log.error(e)
        if ( not new_data ):
            logger.print_on_console( 'Unable to find objects of type : ' + list(self.tag_map.keys())[list(self.tag_map.values()).index(tag_choice)] )
            log.error( 'Unable to find object_type : ' + list(self.tag_map.keys())[list(self.tag_map.values()).index(tag_choice)] + ' while scraping' )
        else:
            logger.print_on_console( 'Detected and scraped "' + str(len(new_data)) + '" objects of type : ' + list(self.tag_map.keys())[list(self.tag_map.values()).index(tag_choice)] )
        return new_data

    def visibility(self, event):
        global visiblity_status
        visiblity_state = event.GetEventObject()
        log.info( str(visiblity_state.GetLabel()) + ' is clicked and value obtained is : ' + str(visiblity_state.GetValue()) )
        visiblity_status = visiblity_state.GetValue()


    def onRadioBox(self,e):
        self.choice=self.rbox.GetStringSelection()
        #logger.print_on_console(self.choice)