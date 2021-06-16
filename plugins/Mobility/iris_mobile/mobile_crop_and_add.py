import json
import logger
import logging
import subprocess
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
import ctypes
from constants import *
if SYSTEM_OS != 'Darwin':
    import screeninfo
    import sys
    sys.coinit_flags = 2
    from pywinauto.findwindows import find_window
    from win32gui import SetForegroundWindow
else:
    from AppKit import NSScreen

drawing1 = False
constant_image = False
ix,iy = -1,-1
log = logging.getLogger('mobile_crop_and_add.py')

class Cropandadd():
    def startcropandadd(self, wx_window, img_size):
        '''
            this method displays the mobile screenshot onto the monitor and performs the crop operations
        '''
        try:
            self.terminate_flag = False     # self.terminate_flag because the stop method will change the value to True
            wx_window.Hide()                # hides the scrapping window , one with start/stop iris
            time.sleep(1)
            image_orig = cv2.imread("resized_test_screenshot.png")      # reads the resized screenshot image file created by get_screenshot method in android_scrapping 
            imgtostore = cv2.imread("test_screenshot.png")
            self.user32 = ctypes.windll.user32
            self.device_width = img_size[0]
            self.device_height = img_size[1]

            img_ratio = self.device_width / self.device_height
            new_height = int(87.890625*self.user32.GetSystemMetrics(79)/100)
            new_width = int(img_ratio * new_height)

            imgtostore_height = 1000
            imgtostore_width = int(img_ratio * imgtostore_height)

            imgtostore = cv2.resize(imgtostore, (imgtostore_width, imgtostore_height), interpolation=cv2.INTER_AREA)
            
            # if SYSTEM_OS != 'Darwin':
            #     screen = screeninfo.get_monitors()[0]
            # else:
            #     width = int(NSScreen.mainScreen().frame().size.width)
            #     height = int(NSScreen.mainScreen().frame().size.height)
            # screen = screeninfo.get_monitors()[0]
            
            overlay = image_orig.copy()
            output = image_orig.copy()
            cv2.rectangle(overlay, (0, 0), (image_orig.shape[1],image_orig.shape[0]),(220,220,220), -1)
            alpha=0.4
            cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
            out_path = TEMP_PATH + OS_SEP + 'test.png'
            cv2.imwrite(out_path,output)
            im1 = Image.open(out_path)
            wx_window.Show()                # again displays the start/stop iris window
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
                    
                    # coordinates wrt original device dimensions
                    ixx = int((ix*self.device_width)/new_width)
                    iyy = int((iy*self.device_height)/new_height)
                    xx = int((x*self.device_width)/new_width)
                    yy = int((y*self.device_height)/new_height)


                    # coordinates wrt 1000px height
                    imgtostore_ix = int((ix*imgtostore_width)/new_width) 
                    imgtostore_iy =  int((iy*imgtostore_height)/new_height)
                    imgtostore_x = int((x*imgtostore_width)/new_width)
                    imgtostore_y = int((y*imgtostore_height)/new_height)

                    drawing1 = False
                    self.data['scrapetype'] = 'caa'
                    RGB_img_crop = imgtostore[imgtostore_iy:imgtostore_y,imgtostore_ix:imgtostore_x]
                    cv2.imwrite("cropped.png", RGB_img_crop)
                    with open("cropped.png", "rb") as imageFile:
                        RGB_img_crop_im = str(base64.b64encode(imageFile.read()))
                    if(ix!=x and iy!=y):

                        if(constant_image):
                            custname = 'const_img_object_'+str(ixx)+'_'+str(iyy)+'_'+str(xx)+'_'+str(yy)
                            tag = 'constant'
                        else:
                            custname = 'img_object_'+str(ixx)+'_'+str(iyy)+'_'+str(xx)+'_'+str(yy)
                            tag = 'relative'
                        self.data['view'].append({'custname': custname,'cord':RGB_img_crop_im,'tag':tag,'width':abs(xx-ixx),'height':abs(yy-iyy),'top':iyy,'left':ixx, 'original_device_width': self.device_width, 'original_device_height':self.device_height,'xpath':'iris','objectType':''})
                    if(constant_image):
                        cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,0,255),1)
                    else:
                        cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),1)
                    self.RGB_img_c = np.copy(self.RGB_img)
                    self.RGB_img[(iy+1):(y-1),(ix+1):(x-1)]=image_orig[(iy+1):(y-1),(ix+1):(x-1)]
                    self.RGB_img_c = np.copy(self.RGB_img)
                    constant_image = False

            cv2.namedWindow('image',cv2.WND_PROP_AUTOSIZE)
            cv2.setMouseCallback('image',draw_rect)
            if SYSTEM_OS != 'Darwin':
                cv2.moveWindow('image', 50, 30)
            else:
                cv2.moveWindow('image', 50, 30)
            cv2.setWindowProperty('image', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
            flag = False
            while(1):
                cv2.imshow('image',self.RGB_img)

                if(not flag):
                    flag = True
                    if SYSTEM_OS != 'Darwin':
                        SetForegroundWindow(find_window(title='image'))
                k = cv2.waitKey(1) & 0xFF
                if(self.terminate_flag):
                    self.stopflag = True
                    cv2.destroyAllWindows()
                if self.stopflag:
                    if(os.path.isfile(out_path)):
                        os.remove(out_path)
                    if(os.path.isfile("cropped.png")):
                        os.remove("cropped.png")
                    break
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in capturing iris object")

    def stopcropandadd(self):
            try:
                self.terminate_flag = True      # self.terminate_flag value changed to end the startcropandadd method
                cv2.destroyWindow('image')      # destroys the screenshot viewing display
                with open("test_screenshot.png", "rb") as imageFile:
                    self.data['mirror'] =  base64.b64encode(imageFile.read()).decode('UTF-8').strip()
                os.remove('test_screenshot.png')
                os.remove('resized_test_screenshot.png')
                with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements_android.json', 'w') as outfile:
                    log.info('Opening domelements_Android.json file to write scraped objects')
                    logger.print_on_console("Writing scrape data to domelements_Android.json file")
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
