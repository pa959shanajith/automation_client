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
from webscrape_utils import WebScrape_Utils

cropandaddobj = None
browserobj = browserops.BrowserOperations()
clickandaddoj = clickandadd.Clickandadd()
fullscrapeobj = fullscrape.Fullscrape()

class ScrapeWindow(wx.Frame):
    #----------------------------------------------------------------------
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
        status = obj.openBrowser(browser)
        self.irisFlag = irisFlag
        if status == False:
            self.socketIO.emit('scrape',status)
            driver = browserops.driver
            driver.close()
            self.Close()
        else:
            try:
                self.panel = wx.Panel(self)
                self.core_utilsobject = core_utils.CoreUtils()
                self.webscrape_utils_obj = WebScrape_Utils()
                if (self.action == 'scrape'):
                    self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,18 ), size=(175, 25))
                    self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)

                    self.fullscrapedropdown = wx.ComboBox(self.panel, value="Full", pos=(12,48 ),size=(87.5, 25), choices=self.scrapeoptions, style = wx.CB_DROPDOWN)
                    self.fullscrapedropdown.SetEditable(False)
                    self.fullscrapedropdown.SetToolTip(wx.ToolTip("full objects will be scraped"))
                    self.fullscrapedropdown.Bind(wx.EVT_COMBOBOX,self.OnFullscrapeChoice)

                    self.fullscrapebutton = wx.Button(self.panel, label="Scrape",pos=(101,48 ), size=(86, 25))
                    self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)

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
                print e



    #----------------------------------------------------------------------
    def OnExit(self, event):
        self.Close()
        driver = browserops.driver
        driver.close()

    #----------------------------------------------------------------------
    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton.Disable()
            if(self.irisFlag):
                self.cropbutton.Disable()
            status = clickandaddoj.startclickandadd()
            event.GetEventObject().SetLabel("Stop ClickAndAdd")
##            wx.MessageBox('CLICKANDADD: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
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

##            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.Close()
            event.GetEventObject().SetLabel("Start ClickAndAdd")
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


    #----------------------------------------------------------------------
    def fullscrape(self,event):
        print 'Performing fullscrape using option: ',self.scrape_selected_option[0]

        self.startbutton.Disable()
        if(self.irisFlag):
            self.cropbutton.Disable()
        #if any of the last two options are selected then scrape_selected_option will be having one more entry as the value of tagname/xpath
        if self.scrape_selected_option[0]  == self.scrapeoptions[-1]:
            self.scrape_selected_option.append(self.fullscrapedropdown.GetValue())
        elif self.scrape_selected_option[0] == self.scrapeoptions[-2]:
            self.scrape_selected_option.append(self.fullscrapedropdown.GetValue().lower())

        if len(self.scrape_selected_option) > 1:
            print "value is: ",self.scrape_selected_option[1]
        d = fullscrapeobj.fullscrape(self.scrape_selected_option)

        # Check the limit of data size as per Nineteen68 standards
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
            self.socketIO.emit('scrape',d)
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





