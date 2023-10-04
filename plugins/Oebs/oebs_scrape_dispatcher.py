#-------------------------------------------------------------------------------
# Name:        oebs_scrape_dispatcher.py
# Purpose:
#
# Author:      sushma.p, divyansh.singh
#
# Created:     15-07-2021
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import oebs_utils
import oebs_fullscrape
import logger
import logging
import oebs_constants
import wx
import os
import base64
import json
import time
from constants import *
import core_utils
import threading
import cropandadd
import re

visiblity_status = False
scrape_pop_window = False

log = logging.getLogger('scrape_dispatcher.py')
windownametoscrape = ''
class ScrapeDispatcher(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(350, 255) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour('#ffffff')
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.start_clickandadd_img = wx.Image(os.environ["IMAGES_PATH"] +"start.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.stop_clickandadd_img = wx.Image(os.environ["IMAGES_PATH"] +"stop.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.capture_button_img = wx.Image(os.environ["IMAGES_PATH"] +"desktop_capture.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.startiris_button_img = wx.Image(os.environ["IMAGES_PATH"] +"start.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.stopiris_button_img = wx.Image(os.environ["IMAGES_PATH"] +"stop.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        global obj
        obj = oebs_utils.Utils()
        self.utils_obj=oebs_utils.Utils()
        self.scrape_obj=oebs_fullscrape.FullScrape()
        self.core_utilsobject = core_utils.CoreUtils()
        self.scrapeoptions = ['Full', 'Button', 'Textbox', 'Dropdown', 'Radiobutton', 'Checkbox', 'Table', 'List', 'InternalFrame', 'Frame', 'ScrollBar', 'Link', 'Page Tab', 'Other Tags']
        self.tag_map = {'Full':'full','Button':['push button','toggle button'], 'Textbox':['edit','Edit Box','text','password text'], 'Dropdown':'combo box', 'Radiobutton':'radio button', 'Checkbox':'check box', 'Table':'table', 'List':['list item','list'],'InternalFrame':'internal frame','Frame':'frame','ScrollBar':'scroll bar', 'Link':['hyperlink','Static'], 'Page Tab': 'page tab', 'Other Tags':'element'}
        self.delay_time=["0s","5s","10s","15s","20s","25s"]
        self.delay_time_map={"0s":0,"5s":5,"10s":10,"15s":15,"20s":20,"25s":25}
        self.parent = parent
        self.img_path = AVO_ASSURE_HOME + OS_SEP + 'output' + OS_SEP +'oebs_form.png'
        global windownametoscrape
        windownametoscrape = filePath
        scrape_pop_window = False
        self.socketIO = socketIO
        windowname=filePath
        input_val=[]
        input_val.append(windowname)
        input_val.append(10)
        #status = obj.set_to_foreground(windowname)
        result = obj.find_oebswindow_and_attach(windowname)
        status = result[0]
        if ( status!=TERMINATE and status ):
            self.panel = wx.Panel(self)
            self.vsizer = wx.BoxSizer(wx.VERTICAL)
            self.startbutton_label = wx.StaticText((self.panel), label='Click and Add', pos = (20, 22), name='Click and Add')
            self.startbutton = wx.BitmapToggleButton(self.panel, label = self.start_clickandadd_img, pos = (175, 20), size = (145, 30))
            self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)
            self.startbutton.SetToolTip(wx.ToolTip( "Elements will be scraped via Click and Add method." ))

            self.fullscrapedropdown = wx.ComboBox(self.panel, value = "Full", pos = (20, 70), size = (145, 30), choices = self.scrapeoptions, style = wx.CB_DROPDOWN)
            self.fullscrapedropdown.SetEditable(False)
            self.fullscrapedropdown.SetToolTip(wx.ToolTip( "Elements will be scraped via Full Scrape method." ))

            self.fullscrapebutton = wx.BitmapButton(self.panel, bitmap = self.capture_button_img, pos = (175, 69), size = (145, 30))
            self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)

            self.visibilityCheck = wx.CheckBox(self.panel, label = "Visible Elements", pos = (20,120))
            self.visibilityCheck.Bind(wx.EVT_CHECKBOX, self.visibility)

            self.delaytext=wx.StaticText(self.panel, label="Delay", pos=(175,120), size=(40,30), style=0, name="")
            self.scrapeDelaydropdown = wx.ComboBox(self.panel, value = "0s", pos = (225,120), size = (55, 25), choices = self.delay_time, style = wx.CB_DROPDOWN)
            self.scrapeDelaydropdown.SetEditable(False)
            self.scrapeDelaydropdown.SetToolTip(wx.ToolTip( "Set delay time before start of IRIS scraping." ))

            global cropandaddobj
            cropandaddobj = cropandadd.Cropandadd()
            self.startbutton_label = wx.StaticText((self.panel), label='IRIS Capture', pos = (20, 168), name='IRIS Capture')
            self.cropbutton = wx.BitmapToggleButton(self.panel, label = self.startiris_button_img, pos=(175, 165), size = (145, 30))
            self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)
            self.Centre()
            style = self.GetWindowStyle()
            self.SetWindowStyle( style|wx.STAY_ON_TOP )
            wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            screen_width, screen_height = wx.GetDisplaySize()
            self.SetPosition((screen_width - self.GetSize()[0], screen_height - self.GetSize()[1]))
            scrape_pop_window=self.Show()
        else:
            self.socketIO.emit('scrape','wrongWindowName')
            self.parent.schedule.Enable()
            self.Close()

        if scrape_pop_window:
            logger.print_on_console("Entering inside scrape window")


    
    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        import oebs_click_and_add

        if state == True:
            self.fullscrapebutton.Disable()
            self.cropbutton.Disable()

            event.GetEventObject().SetBitmapLabel(self.stop_clickandadd_img)
            self.utils_obj.set_to_foreground(windownametoscrape)
            oebs_click_and_add.init_core(windownametoscrape)
            logger.print_on_console('Select the elements from AUT')

        else:
            d, err = oebs_click_and_add.terminate_core()
            event.GetEventObject().SetLabel("Start ClickAndAdd")
            logger.print_on_console('Stopped click and add')
            logger.print_on_console( 'Scrapped data saved successfully in domelements.json file')
            if d and d != '' and d != '{"view": []}':
                try:
                    self.Iconize(True)
                    #providing 1 sec delay to minimize wx scrape window to hide in screenshot
                    time.sleep(1)
                    img = self.utils_obj.captureScreenshot(windownametoscrape)
                    img.save(self.img_path)
                    with open(self.img_path, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())

                    d = json.loads(d)
                    d['mirror'] =encoded_string.decode('UTF-8').strip()
                except Exception as e:
                    logger.print_on_console('Error occured while capturing Screenshot ',e)
                    log.error('Error occured while capturing Screenshot %s',e)
            else:
                logger.print_on_console(err)
                log.debug(err)
            #10 is the limit of MB set as per Avo Assure standards
            if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                self.socketIO.emit('scrape',d)
            else:
                logger.print_on_console('Scraped data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

            self.Close()
            self.parent.schedule.Enable()
            try:
                self.Close()
            except:
                logger.print_on_console('Click and add scrape  completed')


    def fullscrape(self,event):
        logger.print_on_console('Performing full scrape')
        global visiblity_status
        self.startbutton.Disable()
        self.cropbutton.Disable()
        scrape_obj=oebs_fullscrape.FullScrape()
        log.info(("windowname to scrape : %s",windownametoscrape))
        try:
            d = {}
            d['view'] = self.OnFullscrapeChoice(eval(scrape_obj.getentireobjectlist(windownametoscrape))['view'], self.fullscrapedropdown.GetValue())
            self.Iconize(True)
            #providing 1 sec delay to minimize wx scrape window to hide in screenshot
            time.sleep(1)
            img = self.utils_obj.captureScreenshot(windownametoscrape)
            img.save(self.img_path)
            with open(self.img_path, "rb") as image_file:
                      encoded_string = base64.b64encode(image_file.read())
            d['mirror'] =encoded_string.decode('UTF-8').strip()
        except Exception as e:
            log.error('Error occured while capturing Screenshot %s',e)
            logger.print_on_console('Error occured while capturing Screenshot ',e)
        #10 is the limit of MB set as per Avo Assure standards
        if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
            self.socketIO.emit('scrape',d)
        else:
            logger.print_on_console('Scraped data exceeds max. Limit.')
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.parent.schedule.Enable()
        self.Close()
        visiblity_status = False
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
                if keyword in list(dict.keys()):
                    return dict[keyword](*message)
                else:
                    logger.print_on_console(oebs_constants.INVALID_INPUT)
             except Exception as e:
                log.error(e)
                logger.print_on_console(e)

    def cropandadd(self,event):
        try:
            state = event.GetEventObject().GetValue()
            global cropandaddobj
            if ( state == True ):
                event.GetEventObject().SetBitmapLabel(self.stopiris_button_img)
                self.startbutton.Disable()
                self.fullscrapebutton.Disable()
                self.fullscrapedropdown.Disable()
                self.visibilityCheck.Disable()
                self.scrapeDelaydropdown.Disable()
                if (self.delay_time_map[self.scrapeDelaydropdown.GetValue()]>0):
                    time.sleep(self.delay_time_map[self.scrapeDelaydropdown.GetValue()])
                else:
                    time.sleep(1)
                status = cropandaddobj.startcropandadd(self)
            else:
                self.Hide()
                import cv2
                cv2.destroyAllWindows()
                time.sleep(1)
                d = cropandaddobj.stopcropandadd()
                logger.print_on_console( 'Scraped data saved successfully in domelements.json file' )
                self.socketIO.emit('scrape', d)
                self.parent.schedule.Enable()
                self.Close()
                logger.print_on_console( 'Crop and add scrape completed' )
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

    def OnFullscrapeChoice(self, scrape_data, tag_choice):
        """ Input : Full Scraped Data, Tag choice from dropdown
            Output : Filtered tag type data
            Description : When filters are selected from the drop-down , this method filters out the full scrape data based on tag-values"""
        new_data = []
        global visiblity_status
        try:
            tag_choice = self.tag_map[tag_choice]
            #for full scrape
            if tag_choice == 'full':
                if not visiblity_status:
                    new_data = scrape_data
                else:
                    for data in scrape_data:
                        if data['hiddentag'] == str(False):
                            new_data.append(data)
            #for element tag
            elif tag_choice == 'element':
                for data in scrape_data:
                    #logger.print_on_console(data['hiddentag'])
                    tag_values = self.tag_map.values()
                    items_tag = []
                    for each_tag in tag_values:
                        if isinstance(each_tag, list):
                            for tag_in in each_tag:
                                items_tag.append(tag_in)
                        else:
                            items_tag.append(each_tag)
                    if data['tag'] != tag_choice and data['tag'] not in items_tag:
                        if not visiblity_status:
                                new_data.append(data)
                        elif data['hiddentag'] == str(False):
                            new_data.append(data)

            #for tags which are defined in tag_map
            else:
                for data in scrape_data:
                    match=False
                    if isinstance(tag_choice, list):
                        for each_tag in tag_choice:
                            if data['tag'] == each_tag:
                                match=True
                    elif isinstance(tag_choice,str):
                        if data['tag'] == tag_choice:
                            match=True
                    if match:
                        if not visiblity_status:
                            new_data.append(data)
                        elif data['hiddentag'] == str(False):
                            new_data.append(data)
        except Exception as e:
            log.error(e)
        if not new_data:
            logger.print_on_console( 'Unable to find objects of type : ' + list(self.tag_map.keys())[list(self.tag_map.values()).index(tag_choice)] )
            log.error( 'Unable to find object_type : ' + list(self.tag_map.keys())[list(self.tag_map.values()).index(tag_choice)] + ' while scraping' )
        else:
            log.info( 'Detected and scraped "' + str(len(new_data)) + '" objects of type : ' + list(self.tag_map.keys())[list(self.tag_map.values()).index(tag_choice)] )
        return new_data

    def visibility(self, event):
        """Input: click event on visibility checkbox
           Output: N/A
           Description: set the  visiblity_status True/False"""
        global visiblity_status
        visiblity_state = event.GetEventObject()
        log.info( str(visiblity_state.GetLabel()) + ' is clicked and value obtained is : ' + str(visiblity_state.GetValue()) )
        visiblity_status = visiblity_state.GetValue()