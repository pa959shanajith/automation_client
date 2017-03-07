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

import browserops
import clickandadd
import highlight
import io
import logging
import win32gui
import win32con
import logger
import logging

log = logging.getLogger('objectspy.py')
currenthandle=''

class Object_Mapper():

    def compare(self):
##        a=browserops.BrowserOperations()
##        a.openBrowser(browserType)
##        time.sleep(10)
        find_ele=highlight.Highlight()

        with open('domelements_scraped.json') as data_file:
            self.data = json.load(data_file)
            driver = browserops.driver
            time.sleep(10)
            hwndg = browserops.hwndg
            log.info( 'Obtained browser handle and driver from browserops.py class .....')
##            toolwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            log.info( 'Minimizing the foreground window i.e tool and assuming AUT on top .....')
##            time.sleep(2)
##            actwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
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
            for element  in self.data['view']:
                    updated_ele=find_ele.highlight('OBJECTMAPPER'+','+element['xpath']+','+element['url'],element,currenthandle)


    def update(self):
        driver = browserops.driver
##        global data
        data = {}
        lst =[]
        cobject = {'changedobject' : highlight.changedobject}
        ncobject = {'notchangedobject': highlight.notchangedobject}
        nfobject = {'notfoundobject' : highlight.notfoundobject}
        lst.append(cobject)
        lst.append(ncobject)
        lst.append(nfobject)
##        vie = {'view': lst}
        comparedin  =''
        if browserops.browser == 2:
            comparedin =  'FX'
        elif browserops.browser == 3:
            comparedin = 'IE'
        elif browserops.browser == 1:
            comparedin =  'CH'
##        data.append(vie)
        screen = driver.get_screenshot_as_base64()
##        data['scrapetype'] = 'cna'
        data['comparedin'] = comparedin
        data['view'] = lst
        data['mirror'] = screen
##        screenshot = {'mirror':screen}
##        scrapetype = {'scrapetype' : 'fs'}
##        data.append(comparedin)
##        data.append(screenshot)
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

