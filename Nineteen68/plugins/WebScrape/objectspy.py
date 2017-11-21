#-------------------------------------------------------------------------------
# Name:        objectspy
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     28-09-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import json
import time
import domconstants
import browserops
import clickandadd
import highlight
import io
import logging
import platform
if platform.system()!='Darwin':
    import win32gui
    import win32con
import logger
import logging
import os
from PIL import Image
from selenium import webdriver
from core_utils import CoreUtils
log = logging.getLogger('objectspy.py')
currenthandle=''

class Object_Mapper():
    temp_changedobject = None
    temp_notchangedobject = None
    temp_notfoundobject = None
    obj=CoreUtils()
    def compare(self,data):
        find_ele=highlight.Highlight()
        maindir = os.environ["NINETEEN68_HOME"]
        screen_shot_path = maindir + '/Nineteen68/plugins/WebScrape' + domconstants.SCREENSHOT_IMG
        driver = browserops.driver
        time.sleep(10)
        hwndg = browserops.hwndg
        log.info( 'Obtained browser handle and driver from browserops.py class .....')
        log.info( 'Minimizing the foreground window i.e tool and assuming AUT on top .....')
        javascript_hasfocus = """return(document.hasFocus());"""
        for eachdriverhand in driver.window_handles:
            log.info( 'Iterating through the number of windows open by the driver')
            driver.switch_to.window(eachdriverhand)
            log.info( 'Switching to each handle and checking weather it has focus ')
            time.sleep(3)
            if (driver.execute_script(javascript_hasfocus)):
                    log.info( 'Got the window which has the focus')
                    global currenthandle
                    currenthandle = eachdriverhand
        for element  in data:
            orig_element=element
            xpath_string=element['xpath'].split(';')
            #Xpath Decryption logic implemented
            left_part=self.obj.scrape_unwrap(xpath_string[0])
            right_part=self.obj.scrape_unwrap(xpath_string[2])
            element['xpath'] = left_part+';'+xpath_string[1]+';'+right_part
            element['url']=self.obj.scrape_unwrap(element['url'])
            updated_ele=find_ele.highlight('OBJECTMAPPER'+','+element['xpath']+','+element['url'],element,currenthandle,orig_element)
        Object_Mapper.temp_changedobject = find_ele.changedobject
        Object_Mapper.temp_notchangedobject = find_ele.notchangedobject
        Object_Mapper.temp_notfoundobject = find_ele.notfoundobject

    def fullpage_screenshot(self,driver, screen_shot_path):
        try:
            total_width = driver.execute_script("return document.body.offsetWidth")
            total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
            viewport_width = driver.execute_script("return document.body.clientWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            rectangles = []
            screen = None
            if(total_width == 0):
                total_width = driver.execute_script("return document.documentElement.offsetWidth")
            if(total_width > 0 and total_height > 0 and viewport_width > 0 and viewport_height > 0):
                i = 0
                while i < total_height:
                    ii = 0
                    top_height = i + viewport_height
                    if top_height > total_height:
                        top_height = total_height
                    while ii < total_width:
                        top_width = ii + viewport_width
                        if top_width > total_width:
                            top_width = total_width
                        rectangles.append((ii, i, top_width,top_height))
                        ii = ii + viewport_width
                    i = i + viewport_height
                stitched_image = Image.new('RGB', (total_width, total_height))
                previous = None
                part = 0
                for rectangle in rectangles:
                    if not previous is None:
                        driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                        time.sleep(0.2)
                    file_name = "part_{0}.png".format(part)
                    driver.get_screenshot_as_file(file_name)
                    screenshot = Image.open(file_name)
                    if rectangle[1] + viewport_height > total_height:
                        offset = (rectangle[0], total_height - viewport_height)
                    else:
                        offset = (rectangle[0], rectangle[1])
                    stitched_image.paste(screenshot, offset)
                    del screenshot
                    os.remove(file_name)
                    part = part + 1
                    previous = rectangle
                stitched_image.save(screen_shot_path)
                with open(screen_shot_path, "rb") as f:
                    data = f.read()
                    screen =  data.encode("base64")
            else:
                screen = driver.get_screenshot_as_base64()
        except Exception as e:
            screen = driver.get_screenshot_as_base64()
        return screen


    def remove_highlight(self):
        try:
            driver = browserops.driver
            remove_highlight_script = """document.getElementsByTagName('HTML')[0].click(); function getElementsByClassName(classname) {     var a = [];     var re = new RegExp('(^| )' + classname + '( |$)');     var els = document.getElementsByTagName("*");     for (var i = 0, j = els.length; i < j; i++)         if (re.test(els[i].className)) a.push(els[i]);     return a; }  var a = getElementsByClassName('SLKNineteen68_Highlight');     for (var i = 0; i < a.length; i++) {         a[i].removeAttribute('style');     } """
            driver.execute_script(remove_highlight_script)
            def switchtoframe_stopclicknadd1(mypath):
                log.info('Inside switchtoframe_stopclicknadd1 method')
                cond_flag_scna = False
                log.info('Splitting Iframe/frame url by /')
                indiframes = mypath.split("/")
                driver.switch_to.window(currenthandle)
                log.info('Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = domconstants.IFRAME
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'f':
                            frame_iframe = domconstants.FRAME
                            log.info('It is  frame')
                        else:
                            log.info('It is iframe')
                        try:
                            if (driver.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                                driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                                log.info('Switched to frame/iframe')
                                cond_flag_scna = True
                            else:
                                cond_flag_scna = False
                                break
                        except Exception as e:
                            cond_flag_scna = False
                return cond_flag_scna

            def callback_stopclicknadd1(myipath):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' + '/'
                    if(switchtoframe_stopclicknadd1(path)):
                        log.info('before stopclicknadd operation on iframe page is done and data is obtained')
                        driver.execute_script(remove_highlight_script)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            inpath = path + str(frames) + 'f' + '/'
                            if switchtoframe_stopclicknadd1(inpath):
                                driver.execute_script(remove_highlight_script)
                            callback_stopclicknadd1(inpath)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            inpath = path + str(frames) + 'i' + '/'
                            if switchtoframe_stopclicknadd1(inpath):
                                driver.execute_script(remove_highlight_script)
                            callback_stopclicknadd2(inpath)
                        callback_stopclicknadd1(path)

            def callback_stopclicknadd2(myipath):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'f' + '/'
                    if(switchtoframe_stopclicknadd1(path)):
                        driver.execute_script(remove_highlight_script)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            inpath = path + str(frames) + 'i' + '/'
                            if switchtoframe_stopclicknadd1(inpath):
                                driver.execute_script(remove_highlight_script)
                            callback_stopclicknadd2(inpath)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            inpath = path + str(frames) + 'f' + '/'
                            if switchtoframe_stopclicknadd1(inpath):
                                driver.execute_script(remove_highlight_script)
                            callback_stopclicknadd1(inpath)
                        callback_stopclicknadd2(path)

            callback_stopclicknadd1('')
            log.info('stopclickandadd operation on iframe/frame pages is completed')
            driver.switch_to.default_content()
            callback_stopclicknadd2('')
            log.info('stopclickandadd operation on frame/iframe pages is completed')
            driver.switch_to.default_content()
        except Exception as e:
            print e


    def update(self):
        driver = browserops.driver
        data = {}
        lst =[]
        cobject = {}
        ncobject= {}
        nfobject = {}
        cobject = {'changedobject' : Object_Mapper.temp_changedobject }
        ncobject = {'notchangedobject':  Object_Mapper.temp_notchangedobject}
        nfobject = {'notfoundobject' :  Object_Mapper.temp_notfoundobject}
        lst.append(cobject)
        lst.append(ncobject)
        lst.append(nfobject)
        Object_Mapper.temp_changedobject=[]
        Object_Mapper.temp_notchangedobject=[]
        Object_Mapper.temp_notfoundobject=[]
        comparedin  =''
        if browserops.browser == '2':
            comparedin =  'FX'
        elif browserops.browser == '3':
            comparedin = 'IE'
        elif browserops.browser == '1':
            comparedin =  'CH'
        screen = ''
        self.remove_highlight()
        time.sleep(2)
        maindir = os.environ["NINETEEN68_HOME"]
        screen_shot_path = maindir + '/Nineteen68/plugins/WebScrape' + domconstants.SCREENSHOT_IMG
        if (isinstance(driver,webdriver.Firefox) or isinstance(driver,webdriver.Chrome)):
            screen = self.fullpage_screenshot(driver, screen_shot_path )
        else:
            screen = driver.get_screenshot_as_base64()
        data['action'] = 'compare'
        data['comparedin'] = comparedin
        data['view'] = lst
        data['mirror'] = screen
        with open('domelements.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=False)
        return data



    def clickandadd(self):
        b=clickandadd.Clickandadd()
        b.startclickandadd()
        abc=raw_input("enter ok to stop click and add ")
        if abc=='ok':
            b.stopclickandadd()
        with open('domelements.json') as data_file:
            data = json.load(data_file)
            lst=self.data['view']
            for element  in data['view']:
                lst.append(element)
            vie = {'view': lst}
            with io.open('domelements.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(vie, ensure_ascii=False))




if __name__ == '__main__':
        print 'Inside main'
        logging.basicConfig(filename='python-scrappy.log', level=logging.DEBUG, format='%(asctime)s--Line No:%(lineno)d--%(message)s')
        logging.debug('==================OBJECT MAPPING UTILITY STARTED============================')
        logging.debug('---------------------------------------------------------------------------------------')
        a=Object_Mapper()
        a.compare('CH')
        a.clickandadd()
        print 'End of main'

