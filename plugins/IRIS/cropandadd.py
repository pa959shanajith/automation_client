import json
import logger
import logging
from PIL import Image
import base64
import PIL.ImageGrab
import numpy as np
import cv2
import screeninfo
import os
import time
import controller
import readconfig
from constants import *
if SYSTEM_OS != 'Darwin':
    import screeninfo
    from pywinauto.findwindows import find_window
    from pywinauto.win32functions import SetForegroundWindow
else:
    from AppKit import NSScreen

drawing1 = False
constant_image = False
ix,iy = -1,-1
log = logging.getLogger('cropandadd.py')

class Cropandadd():
    def startcropandadd(self,wx_window):
        try:
            controller.terminate_flag = False
            wx_window.Hide()
            time.sleep(1)
            im = PIL.ImageGrab.grab()
            im.save('test.png')
            image_orig = cv2.imread("test.png")
            if SYSTEM_OS != 'Darwin':
                screen = screeninfo.get_monitors()[0]
            else:
                width = int(NSScreen.mainScreen().frame().size.width)
                height = int(NSScreen.mainScreen().frame().size.height)
            screen = screeninfo.get_monitors()[0]
            overlay = image_orig.copy()
            output = image_orig.copy()
            cv2.rectangle(overlay, (0, 0), im.size,(220,220,220), -1)
            alpha=0.4
            cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
            cv2.imwrite('test.png',output)
            im1 = Image.open('test.png')
            wx_window.Show()
            image = np.array(im1)
            self.RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.RGB_img_c = np.copy(self.RGB_img)
            self.data = {}
            self.data['view'] = []            #cords of selected parts
            self.stopflag = False
            def draw_rect(event,x,y,flags,param):
                global ix,iy,drawing1,constant_image
                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing1 = True
                    ix,iy = x,y
                    if (flags == 9):
                        constant_image = True

                elif event == cv2.EVENT_MOUSEMOVE:
                    if drawing1 == True:
                        self.RGB_img = np.copy(self.RGB_img_c)
                        if(constant_image):
                            cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,0,255),1)
                        else:
                            cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),1)

                elif event == cv2.EVENT_LBUTTONUP:
                    drawing1 = False
                    self.data['scrapetype'] = 'caa'
                    RGB_img_crop = image_orig[iy:y,ix:x]
                    cv2.imwrite("cropped.png", RGB_img_crop)
                    with open("cropped.png", "rb") as imageFile:
                        RGB_img_crop_im = str(base64.b64encode(imageFile.read()))
                    if(ix!=x and iy!=y):
                        if(constant_image):
                            custname = 'const_img_object_'+str(ix)+'_'+str(iy)+'_'+str(x)+'_'+str(y)
                            tag = 'constant'
                        else:
                            custname = 'img_object_'+str(ix)+'_'+str(iy)+'_'+str(x)+'_'+str(y)
                            tag = 'relative'
                        self.data['view'].append({'custname': custname,'cord':RGB_img_crop_im,'tag':tag,'width':abs(x-ix),'height':abs(y-iy),'top':iy,'left':ix,'xpath':'iris','objectType':''})
                    if(constant_image):
                        cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,0,255),1)
                    else:
                        cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),1)
                    self.RGB_img_c = np.copy(self.RGB_img)
                    self.RGB_img[(iy+1):(y-1),(ix+1):(x-1)]=image_orig[(iy+1):(y-1),(ix+1):(x-1)]
                    self.RGB_img_c = np.copy(self.RGB_img)
                    constant_image = False

            cv2.namedWindow('image',cv2.WND_PROP_FULLSCREEN)
            cv2.setMouseCallback('image',draw_rect)
            if SYSTEM_OS != 'Darwin':
                cv2.moveWindow('image', screen.x - 1, screen.y - 1)
            else:
                cv2.moveWindow('image', width-1,height-1)
            cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            flag = False
            while(1):
                cv2.imshow('image',self.RGB_img)
                if(not flag):
                    flag = True
                    if SYSTEM_OS != 'Darwin':
                        SetForegroundWindow(find_window(title='image'))
                k = cv2.waitKey(1) & 0xFF
                if(controller.terminate_flag):
                    self.stopflag = True
                    cv2.destroyAllWindows()
                if self.stopflag:
                    if(os.path.isfile("test.png")):
                        os.remove("test.png")
                    if(os.path.isfile("cropped.png")):
                        os.remove("cropped.png")
                    break
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in capturing iris object")

    def stopcropandadd(self):
        try:
            im = PIL.ImageGrab.grab()
            im.save('out.png')
            with open("out.png", "rb") as imageFile:
                self.data['mirror'] = str(base64.b64encode(imageFile.read()))
            os.remove('out.png')
            with open(os.environ["NINETEEN68_HOME"] + '/output/domelements.json', 'w') as outfile:
                log.info('Opening domelements.json file to write scraped objects')
                json.dump(self.data, outfile, indent=4, sort_keys=False)
                log.info('crop and add is dumped into domelements.json file')
            outfile.close()
            self.stopflag = True
            configvalues = readconfig.readConfig().readJson()
            if(configvalues['prediction_for_iris_objects'].lower()=='yes'):
                logger.print_on_console("Starting prediction...")
                import label_image
                label = label_image.LabelImage()
                res = label.start(self.data['view'])
                for i in range(0,len(self.data['view'])):
                    self.data['view'][i]['objectType'] = res[self.data['view'][i]['custname']]
            return self.data
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in stop IRIS")
