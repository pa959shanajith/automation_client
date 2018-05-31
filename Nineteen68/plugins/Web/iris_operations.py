import logger
import time
import logging
import PIL.ImageGrab
import numpy as np
import cv2
from PIL import Image
import pyautogui
from constants import *
log = logging.getLogger('iris_operations.py')

def gotoobject(webelem):
        img_rgb = webelem.decode('base64')
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

        if(len(pt) > 0):
            pyautogui.moveTo(pt[0]+ int(w/2),pt[1] + int(h/2))
        else:
            return False
        time.sleep(1)
        return True

class IRISKeywords():
    def clickiris(self,webelement,*args):
        status = webconstants.TEST_RESULT_FAIL
        result = webconstants.TEST_RESULT_FALSE
        err_msg=None
        try:
            res = gotoobject(webelement['cord'])
            if(res):
                pyautogui.click()
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in clickiris")
        return status,result,None,err_msg

    def settextiris(self,webelement,*args):
        status = webconstants.TEST_RESULT_FAIL
        result = webconstants.TEST_RESULT_FALSE
        err_msg=None
        try:
            res = gotoobject(webelement['cord'])
            if(res):
                pyautogui.click()
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                pyautogui.typewrite(args[0][0], interval=0.1)
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in settextiris")
        return status,result,None,err_msg
