import wx
import sys
import os
from selenium import webdriver
import browserops
import clickandadd
import fullscrape
from socketIO_client import SocketIO,BaseNamespace
import time
import objectspy
import core_utils
import logging
from webscrape_utils import WebScrape_Utils
cropandaddobj = None
browserobj = browserops.BrowserOperations()
clickandaddoj = clickandadd.Clickandadd()
fullscrapeobj = fullscrape.Fullscrape()
log = logging.getLogger(__name__)

class ScrapeWindow(wx.Frame):

    def __init__(self, parent,id, title,browser,socketIO,action,data,irisFlag):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        obj = browserops.BrowserOperations()

        self.socketIO = socketIO
        self.action = action
        self.data = data
        self.scrapeoptions = ["Full",'Button','Checkbox','Radiobutton','Dropdown','ListBox','Image','Link','TextBox','Table','Element','Other tag','Select A Section using XPath']
        self.scrape_selected_option = ["full"]
        self.window_handle_number = 0
        self.window_selected = False
        status = obj.openBrowser(browser)
        self.driver = browserops.driver
        self.irisFlag = irisFlag
        self.scrape_type = None
        self.invalid_urls = ["about:blank","data:,",""]
        self.invalid_url_msg = "There is no URL in the browser selected or the URL is empty/blank. Please load the webpage and then start performing the desired action."
        if status == False:
            self.socketIO.emit('scrape',status)
            self.driver.close()
            self.Close()
        else:
            try:
                self.panel = wx.Panel(self)
                self.core_utilsobject = core_utils.CoreUtils()
                self.webscrape_utils_obj = WebScrape_Utils()
                if (self.action == 'scrape'):
                    self.vsizer = wx.BoxSizer(wx.VERTICAL)
                    self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,18 ), size=(175, 25))
                    self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)

                    self.fullscrapedropdown = wx.ComboBox(self.panel, value="Full", pos=(12,48 ),size=(87.5, 25), choices=self.scrapeoptions, style = wx.CB_DROPDOWN)
                    self.fullscrapedropdown.SetEditable(False)
                    self.fullscrapedropdown.SetToolTip(wx.ToolTip("full objects will be scraped"))
                    self.fullscrapedropdown.Bind(wx.EVT_COMBOBOX,self.OnFullscrapeChoice)

                    self.fullscrapebutton = wx.Button(self.panel, label="Scrape",pos=(101,48 ), size=(86, 25))
                    self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)

                    self.prevbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(os.environ["IMAGES_PATH"] +"stepBack.png", wx.BITMAP_TYPE_ANY), (35, 48), (35, 28))
                    self.prevbutton.Bind(wx.EVT_LEFT_DOWN, self.on_prev)
                    self.prevbutton.SetToolTip(wx.ToolTip("Select previous window/tab"))
                    self.prevbutton.Hide()

                    self.resume_scraping_button = wx.StaticBitmap(self.panel, -1, wx.Bitmap(os.environ["IMAGES_PATH"] +"play.png", wx.BITMAP_TYPE_ANY), (75, 48), (35, 28))
                    self.resume_scraping_button.Bind(wx.EVT_LEFT_DOWN, self.resume_scraping)
                    self.resume_scraping_button.SetToolTip(wx.ToolTip("Resume scraping"))
                    self.resume_scraping_button.Hide()

                    self.nextbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(os.environ["IMAGES_PATH"] +"step.png", wx.BITMAP_TYPE_ANY), (115, 48), (35, 28))
                    self.nextbutton.Bind(wx.EVT_LEFT_DOWN, self.on_next)
                    self.nextbutton.SetToolTip(wx.ToolTip("Select next window/tab"))
                    self.nextbutton.Hide()

                    if(irisFlag):
                        import cropandadd
                        global cropandaddobj
                        cropandaddobj = cropandadd.Cropandadd()
                        self.cropbutton = wx.ToggleButton(self.panel, label="Start IRIS",pos=(12,78 ), size=(175, 25))
                        self.cropbutton.Bind(wx.EVT_TOGGLEBUTTON, self.cropandadd)

                elif(self.action == 'compare'):
                    browserops.driver.get(data['scrapedurl'])
                    self.comparebutton = wx.ToggleButton(self.panel, label="Start Compare",pos=(12,38 ), size=(175, 28))
                    self.comparebutton.Bind(wx.EVT_TOGGLEBUTTON, self.compare)
                self.Centre()
                style = self.GetWindowStyle()
                self.SetWindowStyle( style|wx.STAY_ON_TOP )
                wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
                self.Show()
            except Exception as e:
                log.error(e)

    def OnExit(self, event):
        self.Close()
        self.driver.close()

    def clickandadd(self,event):
        if self.driver.current_url in self.invalid_urls:
            wx.MessageBox(self.invalid_url_msg, "SLK Nineteen68 - Web Scraper", wx.OK | wx.ICON_ERROR)
            self.startbutton.SetValue(not self.startbutton.GetValue())
        else:
            self.scrape_type = "clickandadd"
            self.fullscrapebutton.Disable()
            self.fullscrapedropdown.Disable()
            if(self.irisFlag):
                    self.cropbutton.Disable()
            if not isinstance(self.driver,webdriver.Ie) and len(self.driver.window_handles) > 1 and not self.window_selected:
                self.fullscrapebutton.Hide()
                self.startbutton.Hide()
                if(self.irisFlag):
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
                print 'click and add initiated, select the elements from AUT'

        else:
            d = clickandaddoj.stopclickandadd()
            print 'Scrapped data saved successfully in domelements.json file'

            # Check the limit of data size as per Nineteen68 standards
            if self.core_utilsobject.getdatasize(str(d),'mb') < self.webscrape_utils_obj.SCRAPE_DATA_LIMIT:
                if  isinstance(d,str):
                    if d.lower() == 'fail':
                        self.socketIO.emit('scrape',d)
                else:
                    self.socketIO.emit('scrape',d)
            else:
                print 'Scraped data exceeds max. Limit.'
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
            self.Close()
            print 'Click and add scrape  completed'

    def compare(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            obj = objectspy.Object_Mapper()
            event.GetEventObject().SetLabel("Comparing...")
            self.comparebutton.Disable()
            d = obj.perform_compare(self.data)
            if self.core_utilsobject.getdatasize(str(d),'mb') < self.webscrape_utils_obj.SCRAPE_DATA_LIMIT:
                if  isinstance(d,str):
                    if d.lower() == 'fail':
                        self.socketIO.emit('scrape',d)
                else:
                    self.socketIO.emit('scrape',d)
                    print 'Compare completed'
            else:
                print 'data exceeds max. Limit.'
                self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
            self.Close()

    def fullscrape(self,event):

        if self.driver.current_url in self.invalid_urls:
            wx.MessageBox(self.invalid_url_msg, "SLK Nineteen68 - Web Scraper", wx.OK | wx.ICON_ERROR)
        else:
            self.scrape_type = "fullscrape"
            self.startbutton.Disable()
            if(self.irisFlag):
                self.cropbutton.Disable()

            print 'Performing fullscrape using option: ',self.scrape_selected_option[0]
            if not isinstance(self.driver,webdriver.Ie) and len(self.driver.window_handles) > 1 and not self.window_selected:
                self.fullscrapebutton.Hide()
                self.startbutton.Hide()
                if(self.irisFlag):
                    self.cropbutton.Hide()
                self.fullscrapedropdown.Hide()
                self.nextbutton.Show()
                self.resume_scraping_button.SetToolTip(wx.ToolTip("Resume " + self.scrape_type))
                self.resume_scraping_button.Show()
                self.prevbutton.Show()
                self.vsizer.Layout()
            else:
                self.perform_fullscrape()

    def perform_fullscrape(self):

        '''if any of the last two options are selected then
        scrape_selected_option must be having one more entry as the value of tagname/xpath'''
        if self.scrape_selected_option[0]  == self.scrapeoptions[-1]:
            self.scrape_selected_option.append(self.fullscrapedropdown.GetValue())
        elif self.scrape_selected_option[0] == self.scrapeoptions[-2]:
            self.scrape_selected_option.append(self.fullscrapedropdown.GetValue().lower())
        if len(self.scrape_selected_option) > 1:
            print "value is: ",self.scrape_selected_option[1]
        d = fullscrapeobj.fullscrape(self.scrape_selected_option,self.window_handle_number)

        '''Check the limit of data size as per Nineteen68 standards'''
        if self.core_utilsobject.getdatasize(str(d),'mb') < self.webscrape_utils_obj.SCRAPE_DATA_LIMIT:
            if  isinstance(d,str):
                if d.lower() == 'fail':
                    self.socketIO.emit('scrape',d)
            else:
                self.socketIO.emit('scrape',d)
                print 'Full scrape  completed'
        else:
            print 'Scraped data exceeds max. Limit.'
            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
        self.Close()

    def cropandadd(self,event):
        state = event.GetEventObject().GetValue()
        global cropandaddobj
        if state == True:
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
            print 'Scrapped data saved successfully in domelements.json file'
            self.socketIO.emit('scrape', d)
            self.Close()
            event.GetEventObject().SetLabel("Start IRIS")
            print 'Crop and add scrape completed'

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
        scrape_window_basic_buttons = [self.fullscrapebutton, self.startbutton, self.fullscrapedropdown]
        map(lambda button: button.Disable(),selector_window_buttons)
        if self.scrape_type == "fullscrape":
            self.perform_fullscrape()
        elif self.scrape_type == "clickandadd":
            self.perform_clickandadd()
            map(lambda button: button.Hide(), selector_window_buttons)
            map(lambda button: button.Show(), scrape_window_basic_buttons)
            if(self.irisFlag):
                self.cropbutton.Show()
            self.vsizer.Layout()
            self.window_selected = True
            self.startbutton.SetValue(True)

    def on_next(self,event):
        if self.window_handle_number < len(self.driver.window_handles) - 1:
            self.window_handle_number += 1
            self.driver.switch_to.window(self.driver.window_handles[self.window_handle_number])
            print "Currently selected window/tab's URL: ", self.driver.current_url

    def on_prev(self,event):
        if self.window_handle_number > 0:
            self.window_handle_number -= 1
            self.driver.switch_to.window(self.driver.window_handles[self.window_handle_number])
            print "Currently selected window/tab's URL: ", self.driver.current_url


