import json
import logger
import logging
from PIL import Image
import base64
import PIL.ImageGrab
import numpy as np
import cv2
import screeninfo
drawing1 = False
ix,iy = -1,-1
log = logging.getLogger('cropandadd.py')


class Cropandadd():
    def startcropandadd(self):
        try:
            im = PIL.ImageGrab.grab()
            im.save('test.jpg')
            screen_id = 0

            # get the size of the screen
            screen = screeninfo.get_monitors()[screen_id]
            width, height = screen.width, screen.height
            im1 = Image.open('test.jpg')
            image = np.array(im1)
            self.RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.RGB_img_c = np.copy(self.RGB_img)
            self.data = {}
            self.data['view'] = []            #cords of selected parts
            self.stopflag = False
           # with open("test.jpg", "rb") as imageFile:
            #    self.data['mirror'] = base64.b64encode(imageFile.read())     #screenshot
            # self.data['mirror'] = ''
            #drawing = False # true if mouse is pressed
            mode = True # if True, draw rectangle. Press 'm' to toggle to curve
            # mouse callback function
            def draw_rect(event,x,y,flags,param):
                global ix,iy,drawing1
                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing1 = True
                    ix,iy = x,y

                elif event == cv2.EVENT_MOUSEMOVE:
                    if drawing1 == True:
                        self.RGB_img = np.copy(self.RGB_img_c)
                        cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),1)

                elif event == cv2.EVENT_LBUTTONUP:
                    drawing1 = False
                    self.data['scrapetype'] = 'caa'
                    RGB_img_crop = self.RGB_img_c[iy:y,ix:x]
                    cv2.imwrite("cropped.png", RGB_img_crop)
                    with open("cropped.png", "rb") as imageFile:
                        RGB_img_crop_im = base64.b64encode(imageFile.read())
                    if(ix!=x and iy!=y):
                        self.data['view'].append({'custname': 'img_object_'+str(ix)+'_'+str(x)+'_'+str(iy)+'_'+str(y),'cord':RGB_img_crop_im,'tag':'iris','width':abs(x-ix),'height':abs(y-iy),'top':iy,'left':ix})
                    cv2.rectangle(self.RGB_img,(ix,iy),(x,y),(0,255,0),1)
                    self.RGB_img_c = np.copy(self.RGB_img)


            #img = np.zeros((512,512,3), np.uint8)
            cv2.namedWindow('image',cv2.WND_PROP_FULLSCREEN)
            cv2.setMouseCallback('image',draw_rect)
            cv2.moveWindow('image', screen.x - 1, screen.y - 1)
            cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            while(1):
                cv2.imshow('image',self.RGB_img)
                k = cv2.waitKey(1) & 0xFF
                if self.stopflag:
                    break

            #cv2.destroyAllWindows()
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in capturing iris object")

    def stopcropandadd(self):
        im = PIL.ImageGrab.grab()
        im.save('out.jpg')
        with open("out.jpg", "rb") as imageFile:
            self.data['mirror'] = base64.b64encode(imageFile.read())
        import os
        os.remove('out.jpg')
        with open('domelements.json', 'w') as outfile:
            log.info('Opening domelements.json file to write scraped objects')
            json.dump(self.data, outfile, indent=4, sort_keys=False)
            log.info('crop and add is dumped into domelements.json file')
        outfile.close()
        self.stopflag = True
        return self.data

