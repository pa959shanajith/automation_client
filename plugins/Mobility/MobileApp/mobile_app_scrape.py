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
import subprocess
from constants import *
import android_scrapping
import wx
import os, time, sys
import logger
import logging
log = logging.getLogger('mobile_app_scrape.py')
obj=android_scrapping.InstallAndLaunch()
import core_utils
from threading import Thread
import json
# cropandaddobj = None
img=None
from queue import Queue
import concurrent.futures

class ScrapeWindow(wx.Frame):

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title, size=(430, 180), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))#|wx.CLOSE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
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
            self.startbutton = wx.Button(self.panel, label="Start Capture", pos=(120,28), size=(180, 28))
            self.startbutton.Bind(wx.EVT_BUTTON, self.startClickAndAdd)
            self.scrapedropdown = wx.ComboBox(self.panel, value="Full",pos=(22, 60), size=(180, 28),choices=self.scrapeoptions, style = wx.CB_DROPDOWN)
            self.scrapedropdown.SetEditable(False)
            self.scrapedropdown.SetToolTip(wx.ToolTip("selected objects will be scraped"))
            self.scrapedropdown.Bind(wx.EVT_COMBOBOX,self.OnFullscrapeChoice)
            
            self.scrapebutton = wx.Button(self.panel, label="Capture",pos=(210,60), size=(180, 28))
            self.scrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)

            self.swipedownbutton = wx.Button(self.panel, label="Swipe Down",pos=(22, 92), size=(180, 28))
            self.swipedownbutton.Bind(wx.EVT_BUTTON, self.swipedown)
            self.swipeupbutton = wx.Button(self.panel, label="Swipe Up",pos=(210,92), size=(180, 28))
            self.swipeupbutton.Bind(wx.EVT_BUTTON, self.swipeup)
            import mobile_crop_and_add
            self.cropandaddobj = mobile_crop_and_add.Cropandadd()
            self.queue = Queue()
            # self.irisbutton = wx.ToggleButton(self.panel, label="Start IRIS", pos=(12, 124), size=(150, 28))
            # self.irisbutton.Bind(wx.EVT_TOGGLEBUTTON, self.iris)
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
                # 10 is the limit of MB set as per Avo Assure standards
                if d is not None:
                    if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
                        
                        # Separate the items starting with "NONAME" from the rest of the items
                        noname_items = [item for item in d['view'] if item['text'].startswith('NONAME')]
                        other_items = [item for item in d['view'] if not item['text'].startswith('NONAME')]

                        # Combine the sorted items and the items starting with "NONAME"
                        sorted_view_list = other_items + noname_items

                        # Update the 'view' list in the JSON data
                        d['view'] = sorted_view_list
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
    
    def startClickAndAdd(self,event):
        state = event.GetEventObject().LabelText
        if state == 'Start Capture':
            # logger.print_on_console('Performing full scrape')
            self.scrapebutton.Disable()       
            self.scrapedropdown.Disable()
            self.startbutton.SetLabel("Stop Capture")        
            try:
                if(self.selected_choice.lower()=="full"):
                    folder_path = os.environ["AVO_ASSURE_HOME"] + '/avoAssureClient_Mobile'
                    command = "npm start"
                    self.process = subprocess.Popen(command, shell=True, cwd=folder_path)
                else:
                    logger.print_on_console("Fail to start Capture Element Screen")  
            except Exception as e:
                self.print_error("Error occurred in Capture Element")
                self.parent.schedule.Enable()
                self.Close()
                log.error(e, exc_info=True)
        else:      
            try:
                if(self.selected_choice.lower()=="full"):
                    if self.process.poll() is None:
                            subprocess.call(["taskkill", "/F", "/T", "/PID", str(self.process.pid)])
                    folder_path = os.environ["AVO_ASSURE_HOME"] + '/avoAssureClient_Mobile'
                    file_name = 'scraped_data.json'
                    file_path = folder_path + '/' + file_name

                    with open(file_path) as file:
                        # Step 2: Parse the JSON data
                        capturedData = json.load(file)
                    # 10 is the limit of MB set as per Avo Assure standards
                    if capturedData is not None:
                        if self.core_utilsobject.getdatasize(str(capturedData),'mb') < 10:
                            self.socketIO.emit('scrape',capturedData)
                            # Step 1: Open the JSON file in write mode
                            with open(file_path, 'w') as file:
                                # Step 2: Write an empty dictionary to the file
                                json.dump({}, file)

                        else:
                            self.print_error('Error Ocurred in Capture Screen')
                            self.socketIO.emit('scrape','Error Ocurred in Capture Screen')
                    else:
                        self.print_error('Error in Capturing')
                        self.socketIO.emit('scrape','fail')
                    self.parent.schedule.Enable()
                    self.Close()
                    log.info('Capturing Elements completed')
                else:
                    capturedData = obj.scrape()
                    if capturedData is not None:
                        new = {'view':[]}
                        for i in capturedData:
                            if i not in new:
                                new[i] = capturedData[i]
                        for i in range(len(capturedData['view'])):
                            for j in self.classes[self.selected_choice.lower()]:
                                if(capturedData['view'][i]['custname'].endswith(j)):
                                    new['view'].append(capturedData['view'][i])
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
                self.print_error("Error occurred in Capture Screen")
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
       

    '''
        --- def onIRISstart() ---
        > Disable other buttons
        > Gets the screenshot dimensions
        > launches screenshot viewer
        > starts another thread to perform cropandadd
    '''
    def onIRISstart(self, event):
        logger.print_on_console("Performing IRIS")
        self.scrapebutton.Disable()
        self.scrapedropdown.Disable()             #disabling the rest of buttons
        self.swipedownbutton.Disable()
        self.swipeupbutton.Disable()
        event.GetEventObject().SetLabel("Stop IRIS")                # changing the label "start iris" to "stop iris"
        size = obj.get_screenshot(resizeImg=True)         # saves the screenshot and gets the size of that screenshot
        time.sleep(1)
        status = self.cropandaddobj.startcropandadd(self,size)

    '''
        --- def onIRISstop() ---
        > Closes the cropandadd and screenshot viewer
        > Stores the scraped elements
        > Returns scraped elements to webserver
    '''

    def onIRISstop(self, event):
        logger.print_on_console("Stopped IRIS")
        self.Hide()                     # hides the scrapping window
        self.scraped_data = None            # initializing scraped_data to None
        data = self.cropandaddobj.stopcropandadd()
        self.scraped_data = data
        time.sleep(2)                
        self.parent.schedule.Enable()
        self.socketIO.emit('scrape',self.scraped_data)
        self.Close()

    '''
        --- def iris() ---
        > Gets called when start or stop iris button pressed
        > Calls onIRISstart and onIRISstop depending upon status' value True or False
    '''

    def iris(self, event):
        status = event.GetEventObject().GetValue()          # stores True/False to status keyword
        if status:
            self.onIRISstart(event)                 # perform start crop operation
        else:
            self.onIRISstop(event)                  # perform stop crop operation


class MobileWindow():

    def run_adb_devices(self, socket):
        """
            Method to get the serail number of connected mobile device
            related to android native scraping
            returns the serial numbers of connected mobile device
        """
        try:
            adb_path = os.environ["AVO_ASSURE_HOME"] + "/platform-tools/adb.exe"
            result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout.strip()
                devices = output.split('\n')[1:]
                devices = [device.split('\t')[0] for device in devices if '\t' in device]  # Remove '\tdevice' part
                socket.emit('get_serial_number', devices)
            else:
                error = result.stderr.strip()
                socket.emit('get_serial_number', 'Error occurred in getting the serial number of connected device')
        except Exception as e:
            socket.emit('get_serial_number', 'Error occurred in getting the serial number of connected device')
            logger.print_on_console("ADB command not found. Make sure ADB is installed and added to your system's PATH.")