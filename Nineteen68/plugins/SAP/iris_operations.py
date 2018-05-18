import logger
import time
import logging
import PIL.ImageGrab
import numpy as np
import cv2
import pyautogui
log = logging.getLogger('iris_operations.py')
import sap_constants
from constants import *
import saputil_operations
utilobj = saputil_operations.SapUtilKeywords()
from sap_scraping import Scrape
import sap_launch_keywords
launchobj = sap_launch_keywords.Launch_Keywords()

class IRISKeywords():
    def clickiris(self,sapelement,input,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            sapgui = utilobj.getSapObject()
            if(sapgui != None):
                scrapingObj=Scrape()
                wnd = scrapingObj.getWindow(sapgui)
                wnd = wnd.Text + '/'
                launchobj.setWindowToForeground(wnd)
                res = self.gotoobject(sapelement['cord'])
                if(res):
                    pyautogui.click()
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in clickIris")
            err_msg = e
        return status,result,value,err_msg

    def settextiris(self,sapelement,input,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            sapgui = utilobj.getSapObject()
            if(sapgui != None):
                scrapingObj=Scrape()
                wnd = scrapingObj.getWindow(sapgui)
                wnd = wnd.Text + '/'
                launchobj.setWindowToForeground(wnd)
                res = self.gotoobject(sapelement['cord'])
                if(res):
                    pyautogui.click()
                    pyautogui.typewrite(input[0], interval=0.5)
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in setTextIris")
            err_msg = e
        return status,result,value,err_msg

    def gotoobject(self,sapelem):
        img_rgb = sapelem.decode('base64')
        fh = open("sample.png", "wb")
        fh.write(img_rgb)
        fh.close()

        im = PIL.ImageGrab.grab()
        im.save('test.png')
        img_rgb = cv2.imread('test.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)


        template = cv2.imread('sample.png',0)
        w, h = template.shape[::-1]
        iter = 0
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        pt = []
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        cv2.imwrite('res.png',img_rgb)
        if(len(pt) > 0):
            pyautogui.moveTo(pt[0]+ int(w/2),pt[1] + int(h/2))
        else:
            return False
        time.sleep(1)
        return True