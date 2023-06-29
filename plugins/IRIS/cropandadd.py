import json
import logger
import logging
from PIL import Image
import base64
import PIL.ImageGrab
import numpy as np
import cv2
# import screeninfo
import os
import time
import controller
import readconfig
from constants import *
#import label_image
if SYSTEM_OS == 'Windows':
    import screeninfo
    from pywinauto.findwindows import find_window
    from pywinauto.win32functions import SetForegroundWindow
elif SYSTEM_OS=='Darwin':
    from AppKit import NSScreen

drawing1 = False
constant_image = False
ix,iy = -1,-1
log = logging.getLogger('cropandadd.py')

class Cropandadd():

    def getobjectlabel(self,obj):
        #get tensorflow image lable
        res = None
        try:
            label = label_image.LabelImage()
            res = label.start(obj)
        except Exception as e:
            log.error("Error occured in getobjectlabel : " + str(e))
            logger.print_on_console("Error occured in getobjectlabel")
        return res

    def startcropandadd(self,wx_window):
        try:
            controller.terminate_flag = False
            if SYSTEM_OS == 'Darwin':
                import wx
                wx_window.HideWithEffect(wx.SHOW_EFFECT_ROLL_TO_BOTTOM)
            else:
                wx_window.Hide()
            time.sleep(1)
            im = PIL.ImageGrab.grab()
            test_img_path = TEMP_PATH + OS_SEP + "test.png"
            crop_img_path = TEMP_PATH + OS_SEP + "cropped.png"
            im.save(test_img_path)
            image_orig = cv2.imread(test_img_path)
            if SYSTEM_OS == 'Windows':
                screen = screeninfo.get_monitors()[0]
            elif SYSTEM_OS == 'Darwin':
                width = int(NSScreen.mainScreen().frame().size.width)
                height = int(NSScreen.mainScreen().frame().size.height)
            else:
                import wx
                app=wx.App(False)
                width,height=wx.GetDisplaySize()
            #screen = screeninfo.get_monitors()[0]
            overlay = image_orig.copy()
            output = image_orig.copy()
            cv2.rectangle(overlay, (0, 0), im.size,(220,220,220), -1)
            alpha=0.4
            cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
            cv2.imwrite(test_img_path,output)
            im1 = Image.open(test_img_path)
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
                    log.debug('Inside draw : Event1 - left button down')
                    drawing1 = True
                    ix,iy = x,y
                    if (flags == 9):
                        log.debug('Inside draw : Event1 - setting const obj true')
                        constant_image = True

                elif event == cv2.EVENT_MOUSEMOVE:
                    if drawing1 == True:
                        self.RGB_img = np.copy(self.RGB_img_c)
                        if(constant_image):
                            cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,0,255),2)
                        else:
                            cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),2)

                elif event == cv2.EVENT_LBUTTONUP:
                    log.debug('Inside draw : Event3 - left button up')
                    drawing1 = False
                    self.data['scrapetype'] = 'caa'
                    if (iy > y and ix > x) : RGB_img_crop = image_orig[y:iy,x:ix]
                    else : RGB_img_crop = image_orig[iy:y,ix:x]
                    cv2.imwrite(crop_img_path, RGB_img_crop)
                    with open(crop_img_path, "rb") as imageFile:
                        RGB_img_crop_im = str(base64.b64encode(imageFile.read()))
                    if(ix!=x and iy!=y):
                        log.debug('Inside draw : Event3 - if ix/x and iy/y are not equal')
                        if(constant_image):
                            log.debug('Inside draw : Event3 - if constant obj set custname and tag')
                            custname = 'const_img_object_'+str(ix)+'_'+str(iy)+'_'+str(x)+'_'+str(y)
                            tag = 'constant'
                        else:
                            log.debug('Inside draw : Event3 - if relative obj set custname and tag')
                            custname = 'img_object_'+str(ix)+'_'+str(iy)+'_'+str(x)+'_'+str(y)
                            tag = 'relative'
                        if (iy > y and ix > x) : self.data['view'].append({'custname': custname,'cord':RGB_img_crop_im,'tag':tag,'width':abs(ix-x),'height':abs(iy-y),'top':y,'left':x,'xpath':'iris','objectType':''})
                        else : self.data['view'].append({'custname': custname,'cord':RGB_img_crop_im,'tag':tag,'width':abs(x-ix),'height':abs(y-iy),'top':iy,'left':ix,'xpath':'iris','objectType':''})
                    if(constant_image):
                        log.debug('Inside draw : Event3 - constant obj - box colour red ')
                        cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,0,255),2)
                    else:
                        log.debug('Inside draw : Event3 - constant obj - box colour green ')
                        cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),2)
                    self.RGB_img_c = np.copy(self.RGB_img)
                    self.RGB_img[(iy+1):(y-1),(ix+1):(x-1)]=image_orig[(iy+1):(y-1),(ix+1):(x-1)]
                    self.RGB_img_c = np.copy(self.RGB_img)
                    constant_image = False

            cv2.namedWindow('image',cv2.WND_PROP_FULLSCREEN)
            cv2.setMouseCallback('image',draw_rect)
            if SYSTEM_OS == 'Windows':
                cv2.moveWindow('image', screen.x - 1, screen.y - 1)
            else:
                cv2.moveWindow('image', width-1,height-1)
            cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

            if SYSTEM_OS == 'Windows':
                SetForegroundWindow(find_window(title='image'))
            while(1):
                cv2.imshow('image',self.RGB_img)
                """cv2.waitKey : The waitkey() is a keyword binding function and it only accepts time in milliseconds as an argument.
                   When you add any time as an argument , then it waits for the specified time and then the program continues.
                   If o is passed , it waits indefinitely until a key is pressed.
                   Note: wait key is set to 100 in AvoAssure, this was done as we noted in some machines(slow VDI's/RDP's) setting to
                   1 milisecond caused the system to stress and scraping periods became unmanageably long.
                """
                cv2.waitKey(100)
                if(controller.terminate_flag):
                    log.debug('Terminating.....')
                    self.stopflag = True
                    cv2.destroyAllWindows()
                    log.debug('Terminated')
                if self.stopflag:
                    log.debug('Clicked on stop.....')
                    if(os.path.isfile(test_img_path)):
                        os.remove(test_img_path)
                    if(os.path.isfile(crop_img_path)):
                        os.remove(crop_img_path)
                    log.debug('Clicked on stop completed')
                    break
        except Exception as e:
            log.error("Error occured in capturing iris object, ERR_MSG : " + str(e))
            logger.print_on_console("Error occured in capturing iris object")

    def stopcropandadd(self):
        try:
            log.debug('Inside stopcropandadd')
            im = PIL.ImageGrab.grab()
            out_path = TEMP_PATH + OS_SEP + "out.png"
            im.save(out_path)
            log.debug('out.png saved in '+TEMP_PATH+' folder')
            with open(out_path, "rb") as imageFile:
                self.data['mirror'] = base64.b64encode(imageFile.read()).decode('UTF-8').strip()
            os.remove(out_path)
            with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json', 'w') as outfile:
                log.info('Opening domelements.json file to write scraped objects')
                json.dump(self.data, outfile, indent=4, sort_keys=False)
                log.info('crop and add is dumped into domelements.json file')
            outfile.close()
            self.stopflag = True
            configvalues = readconfig.readConfig().readJson()
            if(configvalues['prediction_for_iris_objects'].lower()=='yes'):
                logger.print_on_console("Starting prediction...")
                for i in range(0,len(self.data['view'])):
                    objectType = self.getobjectlabel({'custname': self.data['view'][i]['custname'],'cord':self.data['view'][i]['cord']})
                    if(objectType): self.data['view'][i]['objectType'] = str(objectType[self.data['view'][i]['custname']]).lower()
                    else:self.data['view'][i]['objectType'] = "unrecognizableobject"
            elif(configvalues['prediction_for_iris_objects'].lower()=='no'):
                for i in range(0,len(self.data['view'])):
                    self.data['view'][i]['objectType'] = "unrecognizableobject"
            return self.data
        except Exception as e:
            log.error("Error occured in stop IRIS, ERR_MSG : ", str(e))
            logger.print_on_console("Error occured in stop IRIS")