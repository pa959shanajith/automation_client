#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     17-02-2017
# Copyright:   (c) rakesh.v 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from mobile_app_constants import *
from constants import *
import android_scrapping
import wx
from socketIO_client import SocketIO,BaseNamespace
import os
import logger
import logging
log = logging.getLogger('mobile_app_scrape.py')
obj=android_scrapping.InstallAndLaunch()
import core_utils

class ScrapeWindow(wx.Frame):

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title, size=(190, 170), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.CLOSE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.core_utilsobject = core_utils.CoreUtils()
        self.parent = parent
        if (SYSTEM_OS != 'Darwin'):
            self.scrapeoptions = ["Full",'Textbox','Timepicker','Datepicker','Radio','Button','Switch','Checkbox','Spinner','Numberpicker','Seekbar','Text','Image','Layout','View','Element']
            self.classes = {
                'textbox': ['_txtbox'],
                'timepicker': ['_timepicker'],
                'datepicker': ['_datepicker'],
                'radio': ['_radiobtn'],
                'button': ['_btn','_imagebtn'],
                'switch': ['_switch'],
                'checkbox': ['_chkbox','_chkdtxtview'],
                'spinner': ['_spinner'],
                'numberpicker': ['_numberpicker'],
                'seekbar': ['_seekbar'],
                'listview': ['_listview'],
                'text': ['_txtview'],
                'image': ['_img'],
                'layout': ['_linearlayout','_relativelayout','_framelayout'],
                'view':['_view'],
                'element': ['_elmnt']
            }
        else:
            self.scrapeoptions = ["Full",'Textbox','Radio','Button','Switch','Checkbox','Picker','Slider','Link','Text','Image','Table','Cell','Key','Element']
            self.classes = {
                'textbox': ['_textfield','_searchfield','_securetextfield'],
                'radio': ['_radio'],
                'button': ['_button'],
                'switch': ['_switch','_toggle'],
                'checkbox': ['_checkbox'],
                'picker': ['_picker'],
                'slider': ['_slider'],
                'link': ['_link'],
                'text': ['_statictxt','_txtview'],
                'image': ['_image','_icon'],
                'table': ['_table'],
                'cell' : ['_cell'],
                'key' : ['_key'],
                'element': ['_elmnt']
            }
        self.scrape_selected_option = ["full"]
        self.selected_choice = "Full"
        
        global obj
        self.min_y = 0
        self.max_y = 0
        self.x_Value = 0
        self.socketIO = socketIO
        apk_path=filePath.split(';')[0]
        serial=filePath.split(';')[1]
        if str(apk_path).endswith("apk"):
            status = obj.installApplication(apk_path, None, serial, None)
        else:
            deviceName = filePath.split(';')[0]
            platform_version = filePath.split(';')[1]
            bundle_id = filePath.split(';')[2]
            Ip_Address = filePath.split(';')[3]
            status = obj.installApplication(deviceName, platform_version,bundle_id,Ip_Address)

        if status!=None:
            if android_scrapping.driver is not None:
                size = android_scrapping.driver.get_window_size()
                self.min_y = size['height']/4
                self.max_y = size['height']*0.75
                self.x_Value = size['width']*0.50
            self.panel = wx.Panel(self)
            self.scrapedropdown = wx.ComboBox(self.panel, value="Full",pos=(12, 28), size=(87.5, 28),choices=self.scrapeoptions, style = wx.CB_DROPDOWN)
            self.scrapedropdown.SetEditable(False)
            self.scrapedropdown.SetToolTip(wx.ToolTip("selected objects will be scraped"))
            self.scrapedropdown.Bind(wx.EVT_COMBOBOX,self.OnFullscrapeChoice)
            
            self.scrapebutton = wx.Button(self.panel, label="Scrape",pos=(100,28), size=(63, 28))
            self.scrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)

            self.swipedownbutton = wx.Button(self.panel, label="Swipe Down",pos=(12, 60), size=(150, 28))
            self.swipedownbutton.Bind(wx.EVT_BUTTON, self.swipedown)
            self.swipeupbutton = wx.Button(self.panel, label="Swipe Up",pos=(12,92), size=(150, 28))
            self.swipeupbutton.Bind(wx.EVT_BUTTON, self.swipeup)
            self.Centre()
            style = self.GetWindowStyle()
            self.SetWindowStyle( style|wx.STAY_ON_TOP )
            wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            self.Show()
        else:
            self.socketIO.emit('scrape','fail')
            self.Close()
            self.parent.schedule.Enable()

     #----------------------------------------------------------------------
##    def OnExit(self, event):
##        self.Close()
##        driver = browserops.driver
##        driver.close()

    #----------------------------------------------------------------------
##    def clickandadd(self,event):
##        state = event.GetEventObject().GetValue()
##        if state == True:
##            self.fullscrapebutton.Disable()
####        self.comparebutton.Disable()
##            desktop_scraping_obj.clickandadd('STARTCLICKANDADD')
##            event.GetEventObject().SetLabel("Stop ClickAndAdd")
####            wx.MessageBox('CLICKANDADD: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
##            print 'click and add initiated, select the elements from AUT'
##
##        else:
##            d = desktop_scraping_obj.clickandadd('STOPCLICKANDADD')
##            event.GetEventObject().SetLabel("Start ClickAndAdd")
##            print 'print json'
##            print d
####            print desktop_scraping.finalJson
##            print 'after click on stop'
##            print 'Scrapped data saved successfully in domelements.json file'
##            self.socketIO.emit('scrape',d)
####            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
##            self.Close()
####            event.GetEventObject().SetLabel("Start ClickAndAdd")
##            print 'Click and add scrape  completed'
##        print 'done'

##    def compare(self,event):
##        state = event.GetEventObject().GetValue()
##        if state == True:
##            self.fullscrapebutton.Disable()
##            self.startbutton.Disable()
##            obj = objectspy.Object_Mapper()
##            obj.compare()
##            event.GetEventObject().SetLabel("Update")
##        else:
##            obj = objectspy.Object_Mapper()
##            d = obj.update()
##            self.socketIO.send(d)
##            self.Close()


    #----------------------------------------------------------------------


    def fullscrape(self,event):
        # logger.print_on_console('Performing full scrape')
        
        try:
            if(self.selected_choice.lower()=="full"):
                d = obj.scrape()
                # 10 is the limit of MB set as per Nineteen68 standards
                if d is not None:
                    if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                        self.socketIO.emit('scrape',d)
                    else:
                        self.print_error('Scraped data exceeds max. Limit.')
                        self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
                else:
                    self.print_error('Error in scraping')
                    self.socketIO.emit('scrape','fail')
                self.parent.schedule.Enable()
                self.Close()
                log.info('Fullscrape completed')
            else:
                d = obj.scrape()
                if d is not None:
                    new = {'view':[]}
                    for i in d:
                        if i not in new:
                            new[i] = d[i]
                    for i in range(len(d['view'])):
                        for j in self.classes[self.selected_choice.lower()]:
                            if(d['view'][i]['custname'].endswith(j)):
                                new['view'].append(d['view'][i])
                                break
                    if new["view"]==[]:
                        self.print_error('Selected type of objects not found while scraping')
                        self.socketIO.emit('scrape','fail')
                    else:
                        if self.core_utilsobject.getdatasize(str(new),'mb') < 10:
                            self.socketIO.emit('scrape',new)
                        else:
                            self.print_error('Scraped data exceeds max. Limit.')
                            self.socketIO.emit('scrape','Response Body exceeds max. Limit.')
                else:
                    self.print_error('Error in scraping')
                    self.socketIO.emit('scrape','fail')
                self.parent.schedule.Enable()
                self.Close()
                log.info('Selective scrape completed')
        except Exception as e:
            self.print_error("Error occurred in FullScrape")
            self.socketIO.emit('scrape','fail')
            self.parent.schedule.Enable()
            self.Close()
            log.error(e, exc_info=True)
        

    def OnFullscrapeChoice(self,event):
        self.selected_choice = self.scrapedropdown.GetValue()
        self.scrapedropdown.SetEditable(False)
        self.scrapedropdown.SetToolTip(wx.ToolTip(self.scrapedropdown.GetValue() + " objects will be scraped"))
        self.scrape_selected_option[0] = self.selected_choice.lower()


    def swipedown(self,event):
        try:
            if android_scrapping.driver is not None:
                android_scrapping.driver.swipe(self.x_Value, self.min_y, self.x_Value, self.max_y, 3000)
            else:
                self.print_error(DRIVER_ERROR)
                self.Close()
        except Exception as e:
            self.print_error("Error occurred in SwipeDown")
            log.error(e, exc_info=True)


    def swipeup(self,event):
        try:
            if android_scrapping.driver is not None:
                android_scrapping.driver.swipe(self.x_Value, self.max_y, self.x_Value, self.min_y, 3000)
            else:
                self.print_error(DRIVER_ERROR)
                self.Close()
        except Exception as e:
            self.print_error("Error occurred in SwipeUp")
            log.error(e, exc_info=True)