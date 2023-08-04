import wx
import sys
import os
from selenium import webdriver
import browserops
import clickandadd
import fullscrape
import time
import objectspy
import core_utils
import readconfig
import controller
import logger
import logging
import json
from webscrape_utils import WebScrape_Utils
from selenium.common.exceptions import NoSuchWindowException
from os.path import normpath
from constants import SYSTEM_OS
cropandaddobj = None
browserobj = browserops.BrowserOperations()
clickandaddoj = clickandadd.Clickandadd()
fullscrapeobj = fullscrape.Fullscrape()
log = logging.getLogger(__name__)
visiblity_status=False
checkWebPackage = None
# Name: A sreenivaulu Date:02/08/2022
# scraping is allowed for list of allowed_urls only if istrail=1  
allowed_urls = readconfig.configvalues["sample_application_urls"]
isTrial = readconfig.configvalues["isTrial"]

class ScrapeWindow(wx.Frame):

    def __init__(self, parent,id, title,browser,socketIO,action,data):  #called in core #1646
        global checkWebPackage
        checkWebPackage = self.get_client_manifest()
        if SYSTEM_OS == 'Linux':
            scrapper_window_config={
                "frame":[(300, 150),(510, 270)],
                "url_label_field": [(75, 34)],
                "navigateURL_field": [(120, 30),(265, 30)],
                "navigateurl_bttn_field":[(400,30 ), (80, 30)],
                "scrape_type_label_field":[(25,83)],
                "fullscrapedropdown_field":[(120, 80 ),(265, 30)],
                "fullscrapebutton": [(400, 80),(80, 30)],
                "visibilityCheck":[(120,120), (86, 20)],
                "cropbutton_field":[(290,160 ), (165, 30)],
                "startbutton_field":[(110, 160), (165, 30)]
            }
        else:
            scrapper_window_config = {
                "frame": [(300, 150), (510, 270)],
                "url_label_field": [(75, 34)],
                "navigateURL_field": [(110, 30), (260, 30)],
                "navigateurl_bttn_field": [(380, 30), (75, 30)],
                "startbutton_field": [(110, 160), (165, 30)],
                "scrape_type_label_field": [(25, 83)],
                "fullscrapedropdown_field": [(110, 80), (260, 30)],
                "fullscrapebutton": [(380, 80), (75, 30)],
                "visibilityCheck": [(110, 120), (160, 20)],
                "cropbutton_field": [(290, 160), (165, 30)]
            }
        wx.Frame.__init__(self, parent, title=title,pos=scrapper_window_config["frame"][0],  size=scrapper_window_config["frame"][1] ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        obj = browserops.BrowserOperations()

        self.socketIO = socketIO
        self.action = action
        self.data = data
        self.scrapeoptions = ["Full",'Button','Checkbox','Radiobutton','Dropdown','Grid','ListBox','Image','Link','TextBox','Table','Element','Other tag','Select A Section using XPath']
        self.scrape_selected_option = ["full"]
        self.window_handle_number = 0
        self.window_selected = False
        status = obj.openBrowser(browser)
        self.driver = browserops.driver
        self.scrape_type = None
        self.invalid_urls = ["about:blank","data:,",""]
        self.invalid_url_msg = "There is no URL in the browser selected or the URL is empty/blank. Please load the webpage and then start performing the desired action."
        self.allowed_url_msg = "Only AvoBank URL: "+ allowed_urls[0] + " is supported for this trial."
        self.parent = parent
        if status == False:
            self.socketIO.emit('scrape',status)
            if self.driver is not None: self.driver.close()
            self.parent.schedule.Enable()
            self.Close()
        else:
            try:
                self.panel = wx.Panel(self)
                self.core_utilsobject = core_utils.CoreUtils()
                self.webscrape_utils_obj = WebScrape_Utils()
                if (self.action in ['scrape','replace']):
                    self.vsizer = wx.BoxSizer(wx.VERTICAL)

                    #----------------- --------------------------------------------------------------
                    # Name:        web_scrape window
                    # Purpose:     1)textctrl is added for url to navigate a given url(input) in driver
                    #              2) NAVIGATE button is added with binding func ==> def navigateurl_scrape(self,event)  
                    #              3) all the textctrl , buttons and checkebox are alligned properly
                    #
                    # Author:      sreenivasulu A
                    # Created:     08 - 07 - 2022
                    #-------------------------------------------------------------------------------
                    self.url_label = wx.StaticText((self.panel), label='URL', pos=scrapper_window_config["url_label_field"][0], style=0, name='')
                    self.navigateURL = wx.TextCtrl((self.panel), pos=scrapper_window_config["navigateURL_field"][0], size=scrapper_window_config["navigateURL_field"][1])
                    self.navigateurl = wx.Button(self.panel, label="Navigate", pos=scrapper_window_config["navigateurl_bttn_field"][0], size=scrapper_window_config["navigateurl_bttn_field"][1])
                    self.navigateurl.Bind(wx.EVT_BUTTON, self.navigateurl_scrape)
                    self.navigateurl.SetDefault()
                    self.navigateurl.SetFocus()

                    self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd", pos=scrapper_window_config["startbutton_field"][0], size=scrapper_window_config["startbutton_field"][1])
                    self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)

                    self.scrape_type = wx.StaticText((self.panel), label='ScrapeType', pos=scrapper_window_config["scrape_type_label_field"][0], style=0, name='')
                    self.fullscrapedropdown = wx.ComboBox(self.panel, value="Full", pos=scrapper_window_config["fullscrapedropdown_field"][0], size=scrapper_window_config["fullscrapedropdown_field"][1], choices=self.scrapeoptions, style=wx.CB_DROPDOWN)
                    self.fullscrapedropdown.SetEditable(False)
                    self.fullscrapedropdown.SetToolTip(wx.ToolTip("full objects will be scraped"))
                    self.fullscrapedropdown.Bind(wx.EVT_COMBOBOX,self.OnFullscrapeChoice)

                    self.fullscrapebutton = wx.Button(self.panel, label="Scrape", pos=scrapper_window_config["fullscrapebutton"][0], size=scrapper_window_config["fullscrapebutton"][1])
                    self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)

                    self.visibilityCheck = wx.CheckBox(self.panel, label="VisibleElementsOnly", pos=scrapper_window_config["visibilityCheck"][0], size=scrapper_window_config["visibilityCheck"][1])
                    self.visibilityCheck.Bind(wx.EVT_CHECKBOX, self.visibility)

                    self.prevbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(os.environ["IMAGES_PATH"] +"stepBack.png", wx.BITMAP_TYPE_ANY), (160, 90), (35, 28))
                    self.prevbutton.Bind(wx.EVT_LEFT_DOWN, self.on_prev)
                    self.prevbutton.SetToolTip(wx.ToolTip("Select previous window/tab"))
                    self.prevbutton.Hide()

                    self.resume_scraping_button = wx.StaticBitmap(self.panel, -1, wx.Bitmap(os.environ["IMAGES_PATH"] +"play.png", wx.BITMAP_TYPE_ANY), (200, 90), (35, 28))
                    self.resume_scraping_button.Bind(wx.EVT_LEFT_DOWN, self.resume_scraping)
                    self.resume_scraping_button.SetToolTip(wx.ToolTip("Resume scraping"))
                    self.resume_scraping_button.Hide()

                    self.nextbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(os.environ["IMAGES_PATH"] +"step.png", wx.BITMAP_TYPE_ANY), (240, 90), (35, 28))
                    self.nextbutton.Bind(wx.EVT_LEFT_DOWN, self.on_next)
                    self.nextbutton.SetToolTip(wx.ToolTip("Select next window/tab"))
                    self.nextbutton.Hide()

                    if checkWebPackage['isWebPackage'] == "False":
                        import cropandadd
                        global cropandaddobj
                        cropandaddobj = cropandadd.Cropandadd()
                        self.cropbutton = wx.ToggleButton(self.panel, label="Start IRIS",pos=(290,160 ), size=(165, 30))
                        self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)
                        if(self.action == 'replace'): self.cropbutton.Disable()

                    # Name : A sreenivasulu Date: 02/08/2022
                    # setting the URL from allowed_urls when istrail is true
                    if isTrial:
                        self.navigateURL.SetValue(allowed_urls[0])

                elif(self.action == 'compare'):
                    if (data.get('scenarioLevel')==True):
                        screen = data['view']
                        try:
                            browserops.driver.get(screen['scrapedurl'])
                        except:
                            log.error("scrapedurl is Empty")
                        self.compare(None)
                        logger.print_on_console('Compared objects for '+screen['name']+'.')
                    else:
                        try:
                            browserops.driver.get(data['scrapedurl'])
                        except:
                            log.error("scrapedurl is Empty")
                        self.comparebutton = wx.ToggleButton(self.panel, label="Start Compare",pos=(110,80 ), size=(260, 30))
                        self.comparebutton.Bind(wx.EVT_TOGGLEBUTTON, self.compare)
                if (data.get('scenarioLevel')==None or data.get('scenarioLevel')==False):
                    self.Centre()
                    style = self.GetWindowStyle()
                    self.SetWindowStyle( style|wx.STAY_ON_TOP )
                    wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
                    self.Show()
            except Exception as e:
                log.error(e)
                self.parent.schedule.Enable()
    #Name: A sreenivasulu Date:14/07/2022
    # this function will help you navigate a url in browser by scrape window
    def navigateurl_scrape(self,event):
        url = self.navigateURL.GetValue()
        try:
            if not (url is None and url.strip() is ''):
                if url[0:7].lower()!='http://' and url[0:8].lower()!='https://' and url[0:5].lower()!='file:':
                    url='https://'+url
                self.driver.get(url)
                logger.print_on_console('Navigated to URL')
                log.info('Navigated to URL')
            else:
                logger.print_on_console("INVALID_INPUT")
                log.info("INVALID_INPUT")
        except Exception as e:
            log.error(e)
  
    def OnExit(self, event):
        self.Close()
        self.driver.close()

    def clickandadd(self,event):
        global checkWebPackage
        driver = browserops.driver
        current_url = driver.current_url
        # Name: SN adiga Date:02/08/2022
        # conditional statements for check the browser current url in allowed urls list
        if isTrial:
            allowed = False
            for url in allowed_urls:
                if url in driver.current_url:
                    allowed = True

            if allowed == True:
        # end
                try:
                    if not(self.driver.current_window_handle):
                        self.driver.switch_to_window(self.driver.window_handles[-1])
                except NoSuchWindowException as e:
                    log.debug("Window Handle not found, switching to window",self.driver.window_handles[-1])
                    self.driver.switch_to_window(self.driver.window_handles[-1])
                if self.driver.current_url in self.invalid_urls:
                    wx.MessageBox(self.invalid_url_msg, "Avo Assure - Web Scraper", wx.OK | wx.ICON_ERROR)
                    self.startbutton.SetValue(not self.startbutton.GetValue())
                else:
                    self.scrape_type = "clickandadd"
                    self.fullscrapebutton.Disable()
                    self.fullscrapedropdown.Disable()
                    self.visibilityCheck.Disable()
                    if checkWebPackage['isWebPackage'] == "False":
                        self.cropbutton.Disable()
                    if len(self.driver.window_handles) > 1 and not self.window_selected:
                        self.fullscrapebutton.Hide()
                        self.visibilityCheck.Hide()
                        self.startbutton.Hide()
                        if checkWebPackage['isWebPackage'] == "False":
                            self.cropbutton.Hide()
                        self.fullscrapedropdown.Hide()
                        self.nextbutton.Show()
                        self.resume_scraping_button.SetToolTip(wx.ToolTip("Resume " + self.scrape_type))
                        self.resume_scraping_button.Show()
                        self.prevbutton.Show()
                        self.vsizer.Layout()
                    else:
                        self.perform_clickandadd()
            else:
                wx.MessageBox(self.allowed_url_msg, "Avo Assure - Web Scraper", wx.OK | wx.ICON_ERROR)
        else:
            try:
                if not(self.driver.current_window_handle):
                    self.driver.switch_to_window(self.driver.window_handles[-1])
            except NoSuchWindowException as e:
                log.debug("Window Handle not found, switching to window",self.driver.window_handles[-1])
                self.driver.switch_to_window(self.driver.window_handles[-1])
            if self.driver.current_url in self.invalid_urls:
                wx.MessageBox(self.invalid_url_msg, "Avo Assure - Web Scraper", wx.OK | wx.ICON_ERROR)
                self.startbutton.SetValue(not self.startbutton.GetValue())
            else:
                self.scrape_type = "clickandadd"
                self.fullscrapebutton.Disable()
                self.fullscrapedropdown.Disable()
                self.visibilityCheck.Disable()
                if checkWebPackage['isWebPackage'] == "False":
                    self.cropbutton.Disable()
                if len(self.driver.window_handles) > 1 and not self.window_selected:
                    self.fullscrapebutton.Hide()
                    self.visibilityCheck.Hide()
                    self.startbutton.Hide()
                    if checkWebPackage['isWebPackage'] == "False":
                        self.cropbutton.Hide()
                    self.fullscrapedropdown.Hide()
                    self.nextbutton.Show()
                    self.resume_scraping_button.SetToolTip(wx.ToolTip("Resume " + self.scrape_type))
                    self.resume_scraping_button.Show()
                    self.prevbutton.Show()
                    self.vsizer.Layout()
                else:
                    self.perform_clickandadd()

    def perform_clickandadd(self):
        state = self.startbutton.GetValue()
        if state == True:
            status = clickandaddoj.startclickandadd(self.window_handle_number)
            self.startbutton.SetLabel("Stop ClickAndAdd")
            if status.lower() == 'fail':
                self.socketIO.emit('scrape',status)
                self.Close()
            else:
                logger.print_on_console('click and add initiated, select the elements from AUT')

        else:
            d = clickandaddoj.stopclickandadd()
            d['action'] = self.action
            logger.print_on_console('Scrapped data saved successfully in domelements.json file')

            # Check the limit of data size as per Avo Assure standards
            if self.core_utilsobject.getdatasize(str(d),'mb') < self.webscrape_utils_obj.SCRAPE_DATA_LIMIT:
                if  isinstance(d,str):
                    if d.lower() == 'fail':
                        self.socketIO.emit('scrape',d)
                else:
                    self.socketIO.emit('scrape',d)
            else:
                logger.print_on_console('Scraped data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
            self.parent.schedule.Enable()
            self.Close()
            logger.print_on_console('Click and add scrape  completed')

    def compare(self,event):
        if event!=None:
            state = event.GetEventObject().GetValue()
        if event==None or state == True:
            obj = objectspy.Object_Mapper()
            if event!=None:
                event.GetEventObject().SetLabel("Comparing...")
            if event!=None:
                self.comparebutton.Disable()
            if (self.data['scenarioLevel']):
                currentScrapedData = self.data['view']

            else:
                currentScrapedData = self.data
            
            d = obj.perform_compare(currentScrapedData)  #self.data is the current scraped objects

            if (self.data['scenarioLevel']):
                d['orderlist']=currentScrapedData['orderlist']
                
            tagfilter = {}
            for elem in d['view'][2]['notfoundobject']:
                tagfilter[elem['tag']]=True
            
            core_obj=core_utils.CoreUtils()
            xpathfilter = {}
            for elem in currentScrapedData['view']:
                if len(elem['xpath'].split(';'))==3:    #xpath is encrypted
                    decry_abs_xpath = core_obj.scrape_unwrap(elem['xpath'].split(';')[0]).split(';')[0] 
                    xpathfilter[decry_abs_xpath] = True
                else:
                    xpathfilter[elem['xpath'].split(';')[0]] = True
                
            #Full scraping for scenario level impact analysis and analyze screen. Decided by scenario flag
            fullScrapeData = fullscrapeobj.fullscrape(self.scrape_selected_option,self.window_handle_number,visiblity_status,tagfilter,xpathfilter,self.data['scenarioLevel'])
            
            d['view'].append({'newElements':fullScrapeData['view']})
            logger.print_on_console('Full scrape completed for compare object.')

            if self.core_utilsobject.getdatasize(str(d),'mb') < self.webscrape_utils_obj.SCRAPE_DATA_LIMIT:
                if  isinstance(d,str):
                    if d.lower() == 'fail':
                        self.socketIO.emit('scrape',d)
                else:
                    self.socketIO.emit('scrape',d)
                    logger.print_on_console('Compare completed')
            else:
                logger.print_on_console('data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
            self.parent.schedule.Enable()
            self.Close()

    def fullscrape(self,event):
        global checkWebPackage
        driver = browserops.driver
        current_url = driver.current_url
        # Name: SN adiga Date:02/08/2022
        # conditional statements for check the browser current url in allowed urls list
        if isTrial:
            allowed = False
            for url in allowed_urls:
                if url in driver.current_url:
                    allowed = True

            if allowed == True:
        # end
                try:
                    if not(self.driver.current_window_handle):
                        self.driver.switch_to_window(self.driver.window_handles[-1])
                except NoSuchWindowException as e:
                    log.debug("Window Handle not found, switching to window",self.driver.window_handles[-1])
                    self.driver.switch_to_window(self.driver.window_handles[-1])
                if self.driver.current_url in self.invalid_urls:
                    wx.MessageBox(self.invalid_url_msg, "Avo Assure - Web Scraper", wx.OK | wx.ICON_ERROR)
                else:
                    self.scrape_type = "fullscrape"
                    self.startbutton.Disable()
                    if checkWebPackage['isWebPackage'] == "False":
                        self.cropbutton.Disable()  

                    logger.print_on_console('Performing fullscrape using option: ',self.scrape_selected_option[0])
                    if not isinstance(self.driver,webdriver.Ie) and len(self.driver.window_handles) > 1 and not self.window_selected:
                        self.fullscrapebutton.Hide()
                        self.startbutton.Hide()
                        self.visibilityCheck.Hide()
                        if checkWebPackage['isWebPackage'] == "False":
                            self.cropbutton.Hide()
                        self.fullscrapedropdown.Hide()
                        self.nextbutton.Show()
                        self.resume_scraping_button.SetToolTip(wx.ToolTip("Resume " + self.scrape_type))
                        self.resume_scraping_button.Show()
                        self.prevbutton.Show()
                        self.vsizer.Layout()
                    else:
                        self.perform_fullscrape()
            else:
                wx.MessageBox(self.allowed_url_msg, "Avo Assure - Web Scraper", wx.OK | wx.ICON_ERROR)
        else:
            try:
                if not(self.driver.current_window_handle):
                    self.driver.switch_to_window(self.driver.window_handles[-1])
            except NoSuchWindowException as e:
                log.debug("Window Handle not found, switching to window",self.driver.window_handles[-1])
                self.driver.switch_to_window(self.driver.window_handles[-1])
            if self.driver.current_url in self.invalid_urls:
                wx.MessageBox(self.invalid_url_msg, "Avo Assure - Web Scraper", wx.OK | wx.ICON_ERROR)
            else:
                self.scrape_type = "fullscrape"
                self.startbutton.Disable()
                if checkWebPackage['isWebPackage'] == "False":
                    self.cropbutton.Disable()

                logger.print_on_console('Performing fullscrape using option: ',self.scrape_selected_option[0])
                if not isinstance(self.driver,webdriver.Ie) and len(self.driver.window_handles) > 1 and not self.window_selected:
                    self.fullscrapebutton.Hide()
                    self.startbutton.Hide()
                    self.visibilityCheck.Hide()
                    if checkWebPackage['isWebPackage'] == "False":
                        self.cropbutton.Hide()
                    self.fullscrapedropdown.Hide()
                    self.nextbutton.Show()
                    self.resume_scraping_button.SetToolTip(wx.ToolTip("Resume " + self.scrape_type))
                    self.resume_scraping_button.Show()
                    self.prevbutton.Show()
                    self.vsizer.Layout()
                else:
                    self.perform_fullscrape()

    def visibility(self,event):
        global visiblity_status
        visiblity_state = event.GetEventObject()
        log.info(visiblity_state.GetLabel(),' is clicked',str(visiblity_state.GetValue()))
        visiblity_status= visiblity_state.GetValue()

    def perform_fullscrape(self):

        '''if any of the last two options are selected then
        scrape_selected_option must be having one more entry as the value of tagname/xpath'''
        global visiblity_status
        if self.scrape_selected_option[0]  == self.scrapeoptions[-1]:
            self.scrape_selected_option.append(self.fullscrapedropdown.GetValue())
        elif self.scrape_selected_option[0] == self.scrapeoptions[-2]:
            self.scrape_selected_option.append(self.fullscrapedropdown.GetValue().lower())
        if len(self.scrape_selected_option) > 1:
            logger.print_on_console("value is: ",self.scrape_selected_option[1])
        
        #Full scraping for normal. Passing filters as empty and scenario flag as
        d = fullscrapeobj.fullscrape(self.scrape_selected_option,self.window_handle_number,visiblity_status,{},{}, False)

        '''Check the limit of data size as per Avo Assure standards'''
        if self.core_utilsobject.getdatasize(str(d),'mb') < self.webscrape_utils_obj.SCRAPE_DATA_LIMIT:
            if  isinstance(d,str):
                if d.lower() == 'fail':
                    self.socketIO.emit('scrape',d)
            else:
                d['action'] = self.action
                self.socketIO.emit('scrape',d)
                logger.print_on_console('Full scrape  completed')
        else:
            logger.print_on_console('Scraped data exceeds max. Limit.')
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.parent.schedule.Enable()
        self.Close()
        visiblity_status =False

    def cropandadd(self,event):
        state = event.GetEventObject().GetValue()
        global cropandaddobj
        if state == True:
            self.fullscrapebutton.Disable()
            self.fullscrapedropdown.Disable()
            self.visibilityCheck.Disable()
            self.startbutton.Disable()
            event.GetEventObject().SetLabel("Stop IRIS")
            status = cropandaddobj.startcropandadd(self)
        else:
            self.Hide()
            import cv2
            cv2.destroyAllWindows()
            time.sleep(1)
            d = cropandaddobj.stopcropandadd()
            logger.print_on_console('Scrapped data saved successfully in domelements.json file')
            self.socketIO.emit('scrape', d)
            self.parent.schedule.Enable()
            self.Close()
            logger.print_on_console('Crop and add scrape completed')

    def OnFullscrapeChoice(self,event):
        selected_choice = self.fullscrapedropdown.GetValue()

        if selected_choice == self.scrapeoptions[-1]:
            self.fullscrapedropdown.SetEditable(True)
            self.fullscrapedropdown.SetToolTip(wx.ToolTip("Type the xpath to start the section"))
            self.scrape_selected_option[0] = selected_choice
        elif selected_choice == self.scrapeoptions[-2]:
            self.fullscrapedropdown.SetEditable(True)
            self.fullscrapedropdown.SetToolTip(wx.ToolTip("Type a tagname"))
            self.scrape_selected_option[0] = selected_choice
        else:
            self.fullscrapedropdown.SetEditable(False)
            self.fullscrapedropdown.SetToolTip(wx.ToolTip(self.fullscrapedropdown.GetValue() + " objects will be scraped"))
            self.scrape_selected_option[0] = selected_choice.lower()

    def resume_scraping(self,event):
        selector_window_buttons = [self.nextbutton,self.resume_scraping_button,self.prevbutton]
        scrape_window_basic_buttons = [self.fullscrapebutton, self.startbutton, self.fullscrapedropdown,self.visibilityCheck]
        list(map(lambda button: button.Disable(),selector_window_buttons))
        if self.scrape_type == "fullscrape":
            self.perform_fullscrape()
        elif self.scrape_type == "clickandadd":
            self.perform_clickandadd()
            list(map(lambda button: button.Hide(), selector_window_buttons))
            list(map(lambda button: button.Show(), scrape_window_basic_buttons))
            if checkWebPackage['isWebPackage'] == "False":
                self.cropbutton.Show()
            self.vsizer.Layout()
            self.window_selected = True
            self.startbutton.SetValue(True)

    def on_next(self,event):
        if self.window_handle_number < len(self.driver.window_handles) - 1:
            self.window_handle_number += 1
            self.driver.switch_to.window(self.driver.window_handles[self.window_handle_number])
            if isinstance(self.driver,webdriver.Ie):
                import win32gui
                win_name=self.driver.title
                if win_name == '':
                    win_name='Blank Page'
                hwnd=win32gui.FindWindow(None, win_name+" - Internet Explorer")
                if hwnd==0:
                    hwnd=win32gui.FindWindow(None, win_name+" - Windows Internet Explorer")
                win32gui.SetForegroundWindow(hwnd)
            logger.print_on_console("Currently selected window/tab's URL: ", self.driver.current_url)

    def on_prev(self,event):
        if self.window_handle_number > 0:
            self.window_handle_number -= 1
            self.driver.switch_to.window(self.driver.window_handles[self.window_handle_number])
            if isinstance(self.driver,webdriver.Ie):
                import win32gui
                win_name=self.driver.title
                if win_name == '':
                    win_name='Blank Page'
                hwnd=win32gui.FindWindow(None, win_name+" - Internet Explorer")
                if hwnd==0:
                    hwnd=win32gui.FindWindow(None, win_name+" - Windows Internet Explorer")
                win32gui.SetForegroundWindow(hwnd)
            logger.print_on_console("Currently selected window/tab's URL: ", self.driver.current_url)
    def get_client_manifest(self):
        data=None
        MANIFEST_LOC= normpath(os.environ["AVO_ASSURE_HOME"] + "/assets/about_manifest.json")
        try:
            with open(MANIFEST_LOC) as f:
                data = json.load(f)
        except Exception as e:
            msg = 'Unable to fetch package manifest.'
            logger.print_on_console(msg)
            log.error(msg)
            logger.print_on_console(e)
            log.error(e)
        return data

