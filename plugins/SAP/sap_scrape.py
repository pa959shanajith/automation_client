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
log = logging.getLogger('sap_scrape.py')
from saputil_operations import SapUtilKeywords
import time
import base64
import win32gui
import core_utils
cropandaddobj = None
obj=None

class ScrapeWindow(wx.Frame):
    def __init__(self, parent, id, title, filePath, socketIO, irisFlag):
        self.uk=SapUtilKeywords()
        wx.Frame.__init__(self, parent, title=title,
                   pos = (300, 150), size = (210, 150), style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.core_utilsobject = core_utils.CoreUtils()
        self.parent = parent
        global obj
        obj = sap_launch_keywords.Launch_Keywords()
        self.socketIO = socketIO
        fileLoc = filePath.split(';')[0]
        windowname = filePath.split(';')[1]
        input_val = []
        input_val.append(fileLoc)
        input_val.append(windowname)
        status = obj.launch_application(input_val)
        self.irisFlag = irisFlag
        self.scrapeoptions = ['Full', 'Button', 'Textbox', 'Dropdown', 'Label', 'Radiobutton', 'Checkbox', 'Table', 'Scroll Bar', 'Tab', 'Shell', 'SContainer', 'Other Tags']
        self.tag_map = {'Full':'full','Button':'button', 'Textbox':'input', 'Dropdown':'select', 'Label':'label', 'Radiobutton':'radiobutton', 'Checkbox':'checkbox', 'Table':'table', 'Scroll Bar':'GuiScrollContainer', 'Tab':'GuiTab', 'Shell':'shell', 'SContainer':'scontainer', 'Other Tags':'others'}
        if ( status != TERMINATE ):
            try:
                self.panel = wx.Panel(self)
                self.vsizer = wx.BoxSizer(wx.VERTICAL)
                self.startbutton = wx.ToggleButton(self.panel, label = "Start ClickAndAdd", pos=(12, 18), size=(175, 25))
                self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)

                self.fullscrapedropdown = wx.ComboBox(self.panel, value = "Full", pos = (12, 48), size = (87.5, 25), choices = self.scrapeoptions, style = wx.CB_DROPDOWN)
                self.fullscrapedropdown.SetEditable(False)
                self.fullscrapedropdown.SetToolTip(wx.ToolTip( "Full objects will be scraped" ))

                self.fullscrapebutton = wx.Button(self.panel, label="Scrape", pos = (101, 48), size = (86, 25))
                self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)
            except Exception as e:
                log.error(e)
                logger.print_on_console(e)
            if ( irisFlag ):
                import cropandadd
                global cropandaddobj
                cropandaddobj = cropandadd.Cropandadd()
                self.cropbutton = wx.ToggleButton(self.panel, label = "Start IRIS", pos = (12, 78), size = (175, 25))
                self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)
            self.Centre()
            style = self.GetWindowStyle()
            self.SetWindowStyle( style | wx.STAY_ON_TOP )
            wx.Frame(self.panel, style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            self.Show()
        else:
            self.socketIO.emit('scrape','Fail')
            self.parent.schedule.Enable()

    def clickandadd(self, event):
        state = event.GetEventObject().GetValue()
        if ( state == True ):
            self.fullscrapebutton.Disable()
            self.fullscrapedropdown.Disable()
            if ( self.irisFlag ):
                self.cropbutton.Disable()
            sap_scraping_obj.clickandadd('STARTCLICKANDADD')
            event.GetEventObject().SetLabel("Stop ClickAndAdd")
        else:
            data = {}
            d = sap_scraping_obj.clickandadd('STOPCLICKANDADD')
            event.GetEventObject().SetLabel("Start ClickAndAdd")
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
            # 10 is the limit of MB set as per Nineteen68 standards
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
        if ( self.irisFlag ):
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
        # 10 is the limit of MB set as per Nineteen68 standards
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
        global cropandaddobj
        if ( state == True ):
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