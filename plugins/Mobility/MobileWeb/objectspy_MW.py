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
import os
import browserops_MW
import clickandadd_MW
import highlight_MW
import io
import logging
from constants import SYSTEM_OS
if SYSTEM_OS!="Darwin":
    import win32gui
    import win32con
import logger
import logging

log = logging.getLogger('objectspy.py')
currenthandle=''

class Object_Mapper():

    def compare(self):
        find_ele=highlight_MW.Highlight()
        global currenthandle
        with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements_scraped.json') as data_file:
            self.data = json.load(data_file)
            driver = browserops_MW.driver
            time.sleep(10)
            hwndg = browserops_MW.hwndg
            log.info( 'Obtained browser handle and driver from browserops_MW.py class .....')

            log.info( 'Minimizing the foreground window i.e tool and assuming AUT on top .....')
            javascript_hasfocus = """return(document.hasFocus());"""

            for eachdriverhand in driver.window_handles:
                log.info( 'Iterating through the number of windows open by the driver')
                driver.switch_to.window(eachdriverhand)
                log.info( 'Switching to each handle and checking weather it has focus ')
                time.sleep(3)
                if (driver.execute_script(javascript_hasfocus)):
                        log.info( 'Got the window which has the focus')
                        currenthandle = eachdriverhand
            for element  in self.data['view']:
                    updated_ele=find_ele.highlight('OBJECTMAPPER'+','+element['xpath']+','+element['url'],element,currenthandle)


    def update(self):
        driver = browserops_MW.driver
        data = {}
        lst =[]
        cobject = {'changedobject' : highlight_MW.changedobject}
        ncobject = {'notchangedobject': highlight_MW.notchangedobject}
        nfobject = {'notfoundobject' : highlight_MW.notfoundobject}
        lst.append(cobject)
        lst.append(ncobject)
        lst.append(nfobject)
        comparedin  =''
        if browserops_MW.browser == 2:
            comparedin =  'FX'
        elif browserops_MW.browser == 3:
            comparedin = 'IE'
        elif browserops_MW.browser == 1:
            comparedin =  'CH'
        screen = driver.get_screenshot_as_base64()
        data['comparedin'] = comparedin
        data['view'] = lst
        data['mirror'] = screen

        with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=False)
        return data



    def clickandadd_MW(self):
        b=clickandadd_MW.clickandadd_MW()
        b.startclickandadd_MW()
        abc=input("enter ok to stop click and add ")
        if abc=='ok':
            b.stopclickandadd_MW()
        with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json') as data_file:
            data = json.load(data_file)
            lst=self.data['view']
            for element  in data['view']:
                lst.append(element)
            vie = {'view': lst}
            with io.open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(vie, ensure_ascii=False))
