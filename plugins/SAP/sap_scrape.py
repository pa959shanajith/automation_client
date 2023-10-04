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
import sap_launch_keywords
sap_scraping_obj = sap_scraping.Scrape()
import os
from constants import *
import logger
import logging
log = logging.getLogger('sap_scrape.py')
from saputil_operations import SapUtilKeywords
import time
import base64
import win32gui
import core_utils
cropandaddobj = None
obj=None

class ScrapeWindow(wx.Frame):
    def __init__(self, parent, id, title, filePath, socketIO):
        scrape_flag = False
        input_val = []
        try:
            self.uk=SapUtilKeywords()
            wx.Frame.__init__(self, parent, title=title,
                    pos = (300, 150), size = (360, 290), style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.CLOSE_BOX) )
            self.SetBackgroundColour('#ffffff')# white background
            self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            self.start_clickandadd_img = wx.Image(os.environ["IMAGES_PATH"] +"start.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.stop_clickandadd_img = wx.Image(os.environ["IMAGES_PATH"] +"stop.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.capture_button_img = wx.Image(os.environ["IMAGES_PATH"] +"desktop_capture.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.startiris_button_img = wx.Image(os.environ["IMAGES_PATH"] +"start.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.stopiris_button_img = wx.Image(os.environ["IMAGES_PATH"] +"stop.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.core_utilsobject = core_utils.CoreUtils()
            self.parent = parent
            global obj
            obj = sap_launch_keywords.Launch_Keywords()
            self.socketIO = socketIO
            fileLoc = filePath.split(';')[0]
            windowname = filePath.split(';')[1]
            input_val.append(fileLoc)
            input_val.append(windowname)
            self.choice='Manual'
            status = obj.launch_application(input_val)
            self.scrapeoptions = ['Full', 'Button', 'Textbox', 'Dropdown', 'Label', 'Radiobutton', 'Checkbox', 'Table', 'Scroll Bar', 'Tab', 'Shell', 'SContainer', 'Other Tags']
            self.tag_map = {'Full':'full','Button':'button', 'Textbox':'input', 'Dropdown':'select', 'Label':'label', 'Radiobutton':'radiobutton', 'Checkbox':'checkbox', 'Table':'table', 'Scroll Bar':'GuiScrollContainer', 'Tab':'GuiTab', 'Shell':'shell', 'SContainer':'scontainer', 'Other Tags':'others'}
            if ( status != TERMINATE ):
                self.panel = wx.Panel(self)
                self.vsizer = wx.BoxSizer(wx.VERTICAL)
                self.startbutton_label = wx.StaticText((self.panel), label='Click and Add', pos = (20, 22), name='Click and Add')
                self.startbutton = wx.BitmapToggleButton(self.panel, label = self.start_clickandadd_img, pos = (175, 20), size = (145, 30))
                self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)

                self.fullscrapedropdown = wx.ComboBox(self.panel, value = "Full", pos = (20, 65), size = (145, 30), choices = self.scrapeoptions, style = wx.CB_DROPDOWN)
                self.fullscrapedropdown.SetEditable(False)
                self.fullscrapedropdown.SetToolTip(wx.ToolTip( "Full objects will be scraped" ))

                self.fullscrapebutton = wx.BitmapButton(self.panel, bitmap = self.capture_button_img, pos = (175, 64), size = (145, 30))
                self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)

                lblList = ['Manual', 'Auto']
                self.rbox = wx.RadioBox(self.panel,label = 'Capture options',  choices = lblList , pos = (20,110), size = (300,70), style = wx.RA_SPECIFY_COLS)
                self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)

                import cropandadd
                import cropandadd_auto


                global cropandaddobj_manual
                global cropandaddobj_auto


                # import cropandadd
                # global cropandaddobj
                # cropandaddobj = cropandadd.Cropandadd()
                cropandaddobj_manual = cropandadd.Cropandadd()
                cropandaddobj_auto = cropandadd_auto.Cropandadd()
                self.startbutton_label = wx.StaticText((self.panel), label='IRIS Capture', pos = (20, 202), name='IRIS Capture')
                self.cropbutton = wx.BitmapToggleButton(self.panel, label = self.startiris_button_img, pos=(175, 200), size = (145, 30))
                self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)
                self.Centre()
                style = self.GetWindowStyle()
                self.SetWindowStyle( style | wx.STAY_ON_TOP )
                wx.Frame(self.panel, style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
                screen_width, screen_height = wx.GetDisplaySize()
                self.SetPosition((screen_width - self.GetSize()[0], screen_height - self.GetSize()[1]))
                self.Show()
            else:
                scrape_flag=True
        except IndexError as ex:
            scrape_flag=True
            log.error(ex)
            logger.print_on_console("Failed to launch application. Please provide valid inputs")
        except Exception as e:
            scrape_flag=True
            log.error(e)
        if (scrape_flag):
            self.socketIO.emit('scrape','Fail')
            self.parent.schedule.Enable()
            self.Close()

    def clickandadd(self, event):
        state = event.GetEventObject().GetValue()
        if ( state == True ):
            self.fullscrapebutton.Disable()
            self.fullscrapedropdown.Disable()
            self.cropbutton.Disable()
            sap_scraping_obj.clickandadd('STARTCLICKANDADD')
            event.GetEventObject().SetBitmapLabel(self.stop_clickandadd_img)
        else:
            data = {}
            d = sap_scraping_obj.clickandadd('STOPCLICKANDADD')
            event.GetEventObject().SetBitmapLabel(self.start_clickandadd_img)
            SapGui = self.uk.getSapObject()
            obj = sap_launch_keywords.Launch_Keywords()
            wndname = sap_scraping_obj.getWindow(SapGui)
            wnd_title = wndname.__getattr__("Text")
            wnd_id = wndname.__getattr__("Id")
            self.Hide()
            time.sleep(1)
            encoded_string = self.screenShot(wnd_title,wnd_id)
            data['mirror'] = encoded_string.decode('UTF-8').strip()
            data['view'] = d
            # 10 is the limit of MB set as per Avo Assure standards
            if ( self.core_utilsobject.getdatasize(str(data),'mb') < 10 ):
                self.socketIO.emit('scrape',data)
            else:
                logger.print_on_console( 'Scraped data exceeds max. Limit.' )
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
            self.parent.schedule.Enable()
            os.remove("out.png")
            self.Close()

    def fullscrape(self, event):
        self.startbutton.Disable()
        self.fullscrapedropdown.Disable()
        self.cropbutton.Disable()
        SapGui = self.uk.getSapObject()
        wndname = sap_scraping_obj.getWindow(SapGui)
        wnd_title = wndname.__getattr__("Text")
        wnd_id = wndname.__getattr__("Id")
        data = {}
        scraped_data = self.OnFullscrapeChoice(sap_scraping_obj.full_scrape(wndname, wnd_title), self.fullscrapedropdown.GetValue())
        obj = sap_launch_keywords.Launch_Keywords()
        self.Hide()
        time.sleep(1)
        encoded_string = self.screenShot(wnd_title,wnd_id)
        data['mirror'] = encoded_string.decode('UTF-8').strip()
        data['view'] = scraped_data
        # 10 is the limit of MB set as per Avo Assure standards
        if ( self.core_utilsobject.getdatasize(str(data),'mb') < 10 ):
            self.socketIO.emit('scrape',data)
        else:
            logger.print_on_console('Scraped data exceeds max. Limit.')
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.parent.schedule.Enable()
        os.remove("out.png")
        self.Close()

    def screenShot(self,wnd_title,wnd_id):
        encoded_string = None
        img = None
        try:
            img = obj.captureScreenshot(wnd_title,wnd_id)
            img.save('out.png')
            with open("out.png", "rb") as image_file:
                      encoded_string = base64.b64encode(image_file.read())
        except Exception as e:
            log.error('Error occurred while capturing screenshot of window handle, proceeding to screenshot entire screen')
            try:
                img = obj.capture_window( win32gui.GetDesktopWindow())
                img.save('out.png')
                with open("out.png", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
            except Exception as e:
                logger.print_on_console( 'Error occured while capturing Screenshot' )
                log.error(e)
        del img
        return encoded_string

    def cropandadd(self,event):
        SapGui = self.uk.getSapObject()
        wndname = sap_scraping_obj.getWindow(SapGui)
        state = event.GetEventObject().GetValue()
        global cropandaddobj_manual
        global cropandaddobj_auto
        #global cropandaddobj
        if ( state == True ):
            self.fullscrapebutton.Disable()
            self.startbutton.Disable()
            event.GetEventObject().SetBitmapLabel(self.stopiris_button_img)
            if self.choice=='Auto':
                status = cropandaddobj_auto.startcropandadd(self)
                        #logger.print_on_console(self.choice)
            else:
                status = cropandaddobj_manual.startcropandadd(self)
            #status = cropandaddobj.startcropandadd(self)
        else:
            self.Hide()
            import cv2
            cv2.destroyAllWindows()
            time.sleep(1)

            if self.choice=='Auto':
                d = cropandaddobj_auto.stopcropandadd()

            else:
                d = cropandaddobj_manual.stopcropandadd()
            #d = cropandaddobj.stopcropandadd()
            self.socketIO.emit('scrape',d)
            self.parent.schedule.Enable()
            self.Close()

    def OnFullscrapeChoice(self, scrape_data, tag_choice):
        new_data = []
        try:
            tag_choice = self.tag_map[tag_choice]
            if ( tag_choice == 'full' ):
                new_data = scrape_data
            elif ( tag_choice == 'others' ):
                for data in scrape_data:
                    if ( data['tag'] != 'button' and data['tag'] != 'input' and data['tag'] != 'select' and data['tag'] != 'label' and data['tag'] != 'radiobutton' and data['tag'] != 'checkbox' and data['tag'] != 'table' and data['tag'] != 'GuiScrollContainer' and data['tag'] != 'GuiTab' and data['tag'] != 'shell' and data['tag'] != 'scontainer' ):
                        new_data.append(data)
            else:
                for data in scrape_data:
                    if ( data['tag'] == tag_choice ):
                        new_data.append(data)
        except Exception as e:
            log.error(e)
        if ( len( new_data ) == 0 ):
            log.error('Unable to find object_type : ' + tag_choice + ' when scraping ')
        return new_data
    
    def onRadioBox(self,e):
        self.choice=self.rbox.GetStringSelection()
        #logger.print_on_console(self.choice)