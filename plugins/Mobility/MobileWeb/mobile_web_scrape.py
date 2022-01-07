import wx
import sys
import os
from selenium import webdriver
import browser_Keywords_MW
import clickandadd_MW
import fullscrape_MW
from constants import SYSTEM_OS
from selenium.common.exceptions import NoSuchWindowException
import time
from webscrape_utils_MW import WebScrape_Utils  
import objectspy_MW
import core_utils
import platform
import logger
import logging
log = logging.getLogger('mobile_web_scrape.py')

clickandadd_MWoj = clickandadd_MW.Clickandadd()
fullscrape_MWobj = fullscrape_MW.Fullscrape()
visiblity_status=False

class ScrapeWindow(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self, parent,id, title,browser,socketIO,action,data):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        obj = browser_Keywords_MW.BrowserKeywords()
        self.socketIO = socketIO
        self.scrapeoptions = ["Full",'Button','Checkbox','Radiobutton','Dropdown','ListBox','Image','Link','TextBox','Table','Element','Other tag','Select A Section using XPath']
        self.scrape_selected_option = ["full"] 
        self.window_handle_number = 0
        status = obj.openBrowser(None,browser.split(';'))
        # self.panel = wx.Panel(self)
        self.scrape_type = None
        self.action = action
        self.data = data
        # self.irisFlag = irisFlag
        self.invalid_urls = ["about:blank","data:,",""]
        self.invalid_url_msg = "There is no URL in the browser selected or the URL is empty/blank. Please load the webpage and then start performing the desired action."
        self.parent = parent
        self.driver = browser_Keywords_MW.driver_obj
        if status[1] == 'False':
            self.socketIO.emit('scrape',status)
            if self.driver is not None: self.driver.close()
            self.parent.schedule.Enable()
            self.Close()
        else:
            try:
                self.panel = wx.Panel(self)
                self.core_utilsobject = core_utils.CoreUtils()
                self.webscrape_utils_obj = WebScrape_Utils()
                if (self.action == 'scrape'): 
                    #if SYSTEM_OS== "Darwin":
                    self.vsizer = wx.BoxSizer(wx.VERTICAL)
                    self.startbutton = wx.ToggleButton(self.panel, label="Start clickandadd",pos=(12,18 ), size=(165, 25))
                    self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd_MW)   # need to implement OnExtract()
                    # self.fullscrape_MWbutton = wx.Button(self.panel, label="Full Scrape",pos=(12,48 ), size=(175, 28)) #previously present
                    # self.fullscrape_MWbutton.Bind(wx.EVT_BUTTON, self.fullscrape_MW)   # need to implement OnExtract() #previously present

                    self.fullscrapedropdown_MW = wx.ComboBox(self.panel, value="Full", pos=(12,48 ),size=(87.5, 25), choices=self.scrapeoptions, style = wx.CB_DROPDOWN)
                    self.fullscrapedropdown_MW.SetEditable(False)
                    self.fullscrapedropdown_MW.SetToolTip(wx.ToolTip("full objects will be scraped"))
                    self.fullscrapedropdown_MW.Bind(wx.EVT_COMBOBOX,self.OnFullscrapeChoice)

                    self.fullscrapebutton_MW = wx.Button(self.panel, label="Scrape",pos=(101,47 ), size=(75, 25))
                    self.fullscrapebutton_MW.Bind(wx.EVT_BUTTON, self.fullscrape)

                    self.visibilityCheck = wx.CheckBox(self.panel, label="Visibility",pos=(12,78), size=(175, 25))
                    self.visibilityCheck.Bind(wx.EVT_CHECKBOX, self.visibility)

            ##            self.fullscrape_MWbutton.SetToolTip(wx.ToolTip("To perform fullscrape_MW Scraping"))
                    #if SYSTEM_OS != "Darwin":
                elif(self.action == 'compare'):
                    try:
                        browser_Keywords_MW.driver_obj.get(data['scrapedurl'])
                    except:
                        log.error("scrapedurl is Empty")
                    self.comparebutton = wx.ToggleButton(self.panel, label="Start Compare",pos=(12,38 ), size=(175, 28))
                    self.comparebutton.Bind(wx.EVT_TOGGLEBUTTON, self.compare)   # need to implement OnExtract()
                self.Centre()
                style = self.GetWindowStyle()
                self.SetWindowStyle( style|wx.STAY_ON_TOP )
                wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
                self.Show()
            except Exception as e:
                log.error(e)
                self.parent.schedule.Enable()



    #----------------------------------------------------------------------
    def OnExit(self, event):
        self.Close()
        driver = browser_Keywords_MW.driver_obj
        driver.close()

    #----------------------------------------------------------------------
    def clickandadd_MW(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton_MW.Disable()
            #self.comparebutton.Disable()
            clickandadd_MWoj.startclickandadd(self.window_handle_number)
            event.GetEventObject().SetLabel("Stop clickandadd")
##            wx.MessageBox('clickandadd_MW: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
            logger.print_on_console('click and add initiated, select the elements from AUT')

        else:
            d = clickandadd_MWoj.stopclickandadd()
            logger.print_on_console('Scrapped data saved successfully in domelements.json file')

            #10 is the limit of MB set as per Avo Assure standards
            if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                self.socketIO.emit('scrape',d)
            else:
                logger.print_on_console('Scraped data exceeds max. Limit.')
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')

##            wx.MessageBox('clickandadd_MW: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.parent.schedule.Enable()
            self.Close()
            event.GetEventObject().SetLabel("Start clickandadd_MW")
            logger.print_on_console('Click and add scrape  completed')


    def compare(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            obj = objectspy_MW.Object_Mapper()
            event.GetEventObject().SetLabel("Comparing...")
            self.comparebutton.Disable()
            d = obj.perform_compare(self.data)
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
        try:
            if not(self.driver.current_window_handle):
                self.driver.switch_to_window(self.driver.window_handles[-1])
        except NoSuchWindowException as e:
            log.debug("Window Handle not found, switching to window " + str(self.driver.window_handles[-1]))
            self.driver.switch_to_window(self.driver.window_handles[-1])
        if self.driver.current_url in self.invalid_urls:
            wx.MessageBox(self.invalid_url_msg, "Avo Assure - Web Scraper", wx.OK | wx.ICON_ERROR)
        else:
            self.scrape_type = "fullscrape"
            self.startbutton.Disable()
            # if(self.irisFlag):
            #     self.cropbutton.Disable()

            logger.print_on_console('Performing fullscrape using option: ',self.scrape_selected_option[0])
            if not isinstance(self.driver,webdriver.Ie) and len(self.driver.window_handles) > 1 and not self.window_selected:
                self.fullscrapebutton_MW.Hide()
                self.startbutton.Hide()
                # self.visibilityCheck.Hide()
                # if(self.irisFlag):
                #     self.cropbutton.Hide()
                self.fullscrapedropdown_MW.Hide()
                # self.nextbutton.Show()
                # self.resume_scraping_button.SetToolTip(wx.ToolTip("Resume " + self.scrape_type))
                # self.resume_scraping_button.Show()
                # self.prevbutton.Show()
                self.vsizer.Layout()
            else:
                self.perform_fullscrape()

    def OnFullscrapeChoice(self,event):
        selected_choice = self.fullscrapedropdown_MW.GetValue()

        if selected_choice == self.scrapeoptions[-1]:
            self.fullscrapedropdown_MW.SetEditable(True)
            self.fullscrapedropdown_MW.SetToolTip(wx.ToolTip("Type the xpath to start the section"))
            self.scrape_selected_option[0] = selected_choice
        elif selected_choice == self.scrapeoptions[-2]:
            self.fullscrapedropdown_MW.SetEditable(True)
            self.fullscrapedropdown_MW.SetToolTip(wx.ToolTip("Type a tagname"))
            self.scrape_selected_option[0] = selected_choice
        else:
            self.fullscrapedropdown_MW.SetEditable(False)
            self.fullscrapedropdown_MW.SetToolTip(wx.ToolTip(self.fullscrapedropdown_MW.GetValue() + " objects will be scraped"))
            self.scrape_selected_option[0] = selected_choice.lower()

    def visibility(self,event):
        global visiblity_status
        visiblity_state = event.GetEventObject()
        log.info(visiblity_state.GetLabel(),' is clicked',visiblity_state.GetValue())
        visiblity_status= visiblity_state.GetValue()

    def perform_fullscrape(self):

        '''if any of the last two options are selected then
        scrape_selected_option must be having one more entry as the value of tagname/xpath'''
        global visiblity_status
        if self.scrape_selected_option[0]  == self.scrapeoptions[-1]:
            self.scrape_selected_option.append(self.fullscrapedropdown_MW.GetValue())
        elif self.scrape_selected_option[0] == self.scrapeoptions[-2]:
            self.scrape_selected_option.append(self.fullscrapedropdown_MW.GetValue().lower())
        if len(self.scrape_selected_option) > 1:
            logger.print_on_console("value is: ",self.scrape_selected_option[1])
        d = fullscrape_MWobj.fullscrape(self.scrape_selected_option,self.window_handle_number,visiblity_status)

        '''Check the limit of data size as per Avo Assure standards'''
        if self.core_utilsobject.getdatasize(str(d),'mb') < self.webscrape_utils_obj.SCRAPE_DATA_LIMIT:
        # if self.core_utilsobject.getdatasize(str(d),'mb') < 30:
            if  isinstance(d,str):
                if d.lower() == 'fail':
                    self.socketIO.emit('scrape',d)
            else:
                self.socketIO.emit('scrape',d)
                logger.print_on_console('Full scrape  completed')
        else:
            logger.print_on_console('Scraped data exceeds max. Limit.')
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.parent.schedule.Enable()
        self.Close()
        visiblity_status =False


