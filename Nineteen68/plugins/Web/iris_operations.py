import logger
import time
import webconstants
import logging
from constants import *
import core_utils
import base64



#Take the screenshot
import PIL.ImageGrab
#show in full screen
import numpy as np
import cv2
import screeninfo
from PIL import Image
import pyautogui
log = logging.getLogger('popup_keywords.py')

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
        print "Loc: ",zip(*loc[::-1])
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        cv2.imwrite('res.png',img_rgb)
        print pt
        pyautogui.moveTo(pt[0]+ int(w/2),pt[1] + int(h/2))
        time.sleep(1)
        return True

class IRISKeywords():
    def clickiris(self,webelement,*args):
        #img_rgb = cv2.imread('test.jpg')
        gotoobject(webelement['cord'])
        pyautogui.click()
        print "clicked"
        return True

    def settextiris(self,webelement,*args):
        #img_rgb = cv2.imread('test.jpg')
        gotoobject(webelement['cord'])
        pyautogui.click()
        print "text",args[0]
        pyautogui.typewrite(args[0][0], interval=0.5)
        print "clicked"
        return True