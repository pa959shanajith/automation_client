import browserops
import platform
from core_utils import CoreUtils
if platform.system()!='Darwin':
    import win32gui
    import win32con
import time
import json
import domconstants
import logger
import Exceptions
import logging.config
import logging
import os
import time
from selenium import webdriver
from PIL import Image
import base64

import PIL.ImageGrab
#show in full screen
import numpy as np
import cv2
import screeninfo
# from PIL import Image


drawing1 = False
ix,iy = -1,-1
log = logging.getLogger('clickandadd.py')
currenthandle = ''
status = domconstants.STATUS_FAIL
browserops_obj=browserops.BrowserOperations()

class Cropandadd():
    def startcropandadd(self):
        print "starting crop and add"
        pathlist = list()
        try:
            log.info('Performing the click and add operation on default/outer page')
            log.info('Performing the click and add operation on default/outer page done')
            im = PIL.ImageGrab.grab()
            im.save('test.jpg')
        except Exception as e:
            print e
        screen_id = 0

        # get the size of the screen
        print screeninfo.get_monitors()
        screen = screeninfo.get_monitors()[screen_id]
        width, height = screen.width, screen.height
        im1 = Image.open('test.jpg')
        image = np.array(im1)
        self.RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.RGB_img_c = np.copy(self.RGB_img)
        self.data = {}
        self.data['view'] = []            #cords of selected parts
        self.stopflag = False
        with open("test.jpg", "rb") as imageFile:
            self.data['mirror'] = base64.b64encode(imageFile.read())     #screenshot
        # self.data['mirror'] = ''
        print "copied: ",self.RGB_img_c
        #drawing = False # true if mouse is pressed
        mode = True # if True, draw rectangle. Press 'm' to toggle to curve
        # mouse callback function
        def draw_rect(event,x,y,flags,param):
            global ix,iy,drawing1
            if event == cv2.EVENT_LBUTTONDOWN:
                print "down event","ix,iy,x,y: ",ix,iy,x,y
                drawing1 = True
                print "mousedown wala : ",drawing1
                ix,iy = x,y

            elif event == cv2.EVENT_MOUSEMOVE:
                # print "move invoked : ",drawing1
                if drawing1 == True:
                    self.RGB_img = np.copy(self.RGB_img_c)
                    # print "move event","ix,iy,x,y: ",ix,iy,x,y
                    cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),1)
                    #time.sleep(1)
                    # print "drawn rect"
                else:
                    print "pause event","ix,iy,x,y: ",ix,iy,x,y

            elif event == cv2.EVENT_LBUTTONUP:
                print "up event"
                drawing1 = False
                print "ix,iy,x,y: ",ix,iy,x,y
                self.data['scrapetype'] = 'caa'
                RGB_img_crop = self.RGB_img_c[iy:y,ix:x]
                cv2.imwrite("cropped.png", RGB_img_crop)
                with open("cropped.png", "rb") as imageFile:
                    RGB_img_crop_im = base64.b64encode(imageFile.read())
                self.data['view'].append({'custname': 'img_object_'+str(ix)+'_'+str(x)+'_'+str(iy)+'_'+str(y),'cord':RGB_img_crop_im})                
                cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),1)
                self.RGB_img_c = np.copy(self.RGB_img)


        #img = np.zeros((512,512,3), np.uint8)
        cv2.namedWindow('image',cv2.WND_PROP_FULLSCREEN)
        cv2.setMouseCallback('image',draw_rect)
        cv2.moveWindow('image', screen.x - 1, screen.y - 1)
        cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN) 
        cv2.rectangle(self.RGB_img,(1,1),(10,10),(0,255,0),1)
        while(1):
            #print "showing image"
            cv2.imshow('image',self.RGB_img)
            k = cv2.waitKey(1) & 0xFF
            if self.stopflag:
                break

        cv2.destroyAllWindows()
   

    def stopcropandadd(self):
        print "crop and add stopping ... "
        with open('domelements.json', 'w') as outfile:
            log.info('Opening domelements.json file to write vie object')
            json.dump(self.data, outfile, indent=4, sort_keys=False)
            log.info('crop and add is dumped into  domelements.json file ')
        outfile.close()     
        print "crop and add stopped"
        self.stopflag = True
        return self.data

