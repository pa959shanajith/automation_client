'''
    This Class contains all the IRIS operations methods in it
'''
import logger
import logging
import android_scrapping
from appium.webdriver.common.touch_action import TouchAction
from constants import *
import install_and_launch
import cv2
import time, sys
import math
import numpy as np
import subprocess
import base64
from pytesseract import pytesseract
import os
log = logging.getLogger('iris_mobile.py')
TESSERACT_PATH = os.environ["AVO_ASSURE_HOME"] + '/Lib/Tesseract-OCR'
TESSERACT_PATH_EXISTS = os.path.isdir(TESSERACT_PATH)


class iris_mobile_class():

    android_scrapping_obj = android_scrapping.InstallAndLaunch()
    install_and_launch_obj = install_and_launch.LaunchAndInstall()
    
    # Key dictionary for keyevent inputs
    # shift_key_dict = {"A":29, "B":30, "C":31, "D":32, "E":33, "F":34, "G":35, "H":36, "I":37, "J":38, "K":39, "L":40, "M":41, "N":42, "O":43, "P":44, "Q":45, "R":46, "S":47, "T":48, "U":49, "V":50, "W":51, "X":52, "Y":53, "Z":54, "!":8, "$":11, "%":12, "^":13, "&":14, "(":16, ")":7, "~":68, "_":69, "{":71, "}":72, "|":73, ":":74, "\"":75, "<":55, ">":56, "?":76}
    # key_dict = {"a":29, "b":30, "c":31, "d":32, "e":33, "f":34, "g":35, "h":36, "i":37, "j":38, "k":39, "l":40, "m":41, "n":42, "o":43, "p":44, "q":45, "r":46, "s":47, "t":48, "u":49, "v":50, "w":51, "x":52, "y":53, "z":54, "0":7, "1":8, "2":9, "3":10, "4":11, "5":12, "6":13, "7":14, "8":15, "9":16, "\t":61, " ":62, "#":18, "*":17, "@":77, "`": 68, "-":69, "[":71, "]":72, "\\":73, ";":74, "'":75, ",":55, ".":56,"/":76}
    verified_fields = {}


    '''
        definition: Presses/Taps the element passed in the argument
        input: NA
        output: Pass/Fail
        outputtype: Boolean
    '''
    def Press(self, objectname, input, cord, original_device_width, original_device_height):
        self.driver = self.android_scrapping_obj.get_driver()   # getting the driver obj from android_scrapping
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            tap_cords = self.gotoobject(objectname, cord, original_device_width, original_device_height)
            if tap_cords:
                TouchAction(self.driver).tap(None, tap_cords[0], tap_cords[1], 1).perform()   #performing the press/tap operation at calculated coordinates
                log.debug("Element Pressed")
                status=TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
            else:
                err_msg = "Element not found!"
                log.error("Element not found!") 
                logger.print_on_console("Element not found!")        
        except Exception as e:
            log.error("Error while pressing "+str(e))
            err_msg="Error occured while pressing"
            logger.print_on_console("Error occured  while pressing")
        return status, methodoutput, output, err_msg

    '''
        definition: Press and holds the element passed in the argument for 1000ms
        input: NA
        output: Pass/Fail
        outputtype: Boolean
    '''
    def LongPress(self, objectname, input, cord, original_device_width, original_device_height):
        self.driver = self.android_scrapping_obj.get_driver()       #getting driver obj from android_scrapping
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            tap_cords = self.gotoobject(objectname, cord, original_device_width, original_device_height)
            if tap_cords:
                TouchAction(self.driver).long_press(None, tap_cords[0], tap_cords[1], 1000).release().perform()
                # action performed
                log.debug("Element Long Pressed")
                status=TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Element not found!")
                err_msg="Element not found!"
                logger.print_on_console("Element not found!")
        except Exception as e:
            err_msg="Error occured while performing long press"
            log.error("Error occured while performing long press "+str(e))
            logger.print_on_console(e)
        return status, methodoutput, output, err_msg    
    

    '''
        definition: Set Texts to the element passed in the arguments
        input: String
        output: Pass/Fail
        outputtype: Boolean
    '''
    def SetText(self, objectname, input, cord, original_device_width, original_device_height):
        self.driver = self.android_scrapping_obj.get_driver()   # gets the driver object from android_scrapping
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            tap_cords = self.gotoobject(objectname, cord, original_device_width, original_device_height)
            elem = None

            if objectname in self.verified_fields:
                elem = self.verified_fields[objectname]         # if the element is already verified then it will fetch the element object from dictionary

            if tap_cords or elem:
                if tap_cords and not elem:
                    # only tap_cords are available. the object hasnt been verified yet so checking if the passed element is editText or not
                    elements = self.driver.find_elements_by_class_name("android.widget.EditText")
                    min_dist = sys.maxsize
                    # checking if elements is not empty
                    if elements:
                        for element in elements:
                            x = element.location['x']
                            y = element.location['y']
                            # getting the closest editText to the tap_cords
                            dist = math.sqrt((x - int(tap_cords[0]))**2 + (y - int(tap_cords[1]))**2 )
                            if(dist<min_dist):
                                min_dist = dist
                                elem = element
                        x = elem.location['x']
                        y = elem.location['y']
                        xx = x+elem.size['width']
                        yy = y+elem.size['height']
                        # checking if the tap_cords are belong to editText or not , if not elem=None
                        if not ((x<tap_cords[0] and y<tap_cords[1]) and (xx>tap_cords[0] and yy>tap_cords[1])):
                            elem = None
                    else:
                        elem = None
                try:
                    if elem:
                        log.debug("Element found, performing operations")
                        # element is found and clearing the up the field before entering new text
                        elem.clear()
                        # if field is still not empty, we are deleting letter by letter
                        if elem.text != '':
                            for i in elem.text:
                                textBefore = elem.text          # storing the text before clearing
                                self.driver.keyevent(67)        # keyevent=67 is the key code for del
                                textAfter = elem.text           # storing the text after clearing
                                # checking if both texts are same if same the text is probably a placeholder which cannot be deleted further 
                                # hence breaking the loop, if not then more text is yet to clear
                                if textBefore == textAfter:     
                                    break
                        #getting the placeholder text
                        textPlaceholder = elem.text
                        # if placeholder text is empty then we are assigning it our placeholder
                        if textPlaceholder == '':
                            textPlaceholder = "!PLACEHOLDER!"

                        elem.set_text(input) #setting the text
                        log.debug("Set Text has been performed")

                        # checking if the element has set text the and removing the appended placeholder
                        # if text is set, element is stored to verified_field dictionary and result is passed 
                        if input == elem.text.replace(", "+str(textPlaceholder), "") and input != textPlaceholder:
                            self.verified_fields[objectname] = elem
                            status=TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        '''
                        else:
                            checkFlag = True
                            hideSoftKeyFlag = False
                            for letter in input:
                                if letter in self.shift_key_dict.keys():
                                    self.driver.keyevent(self.shift_key_dict[letter], 193)          # 193 is keycode for shift
                                elif letter in self.key_dict.keys():
                                    self.driver.keyevent(self.key_dict[letter])
                                
                                if(checkFlag):
                                    time.sleep(1)
                                    if elem.text.replace(", "+str(textPlaceholder), "") != letter and elem.text.replace(", "+str(textPlaceholder), "") != "•":
                                        hideSoftKeyFlag = True
                                        break
                                    else:
                                        checkFlag = False
                                
                            if hideSoftKeyFlag:
                                checkFlag = True
                                for letter in input:
                                    if self.driver.is_keyboard_shown():
                                        self.driver.hide_keyboard()
                                    if letter in self.shift_key_dict.keys():
                                        self.driver.keyevent(self.shift_key_dict[letter], 193)          # 193 is keycode for shift
                                    elif letter in self.key_dict.keys():
                                        self.driver.keyevent(self.key_dict[letter])
                                    
                                    if(checkFlag):
                                        time.sleep(1)
                                        if elem.text.replace(", "+str(textPlaceholder), "") == letter or elem.text.replace(", "+str(textPlaceholder), "") == "•":
                                            checkFlag = False

                            if (input == elem.text.replace(", "+str(textPlaceholder), "") and input != textPlaceholder) or elem.text.replace(", "+str(textPlaceholder), "") == "•"*len(elem.text.replace(", "+str(textPlaceholder), "")):
                                self.verified_fields[objectname] = elem
                                status=TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE'''
                    else:
                        logger.print_on_console("Invalid Element Found!")
                        err_msg="Invalid Element Found!"
                        log.error("Invalid Element Found!")
                except Exception as e:
                    log.error("Error occured while setting text "+str(e))
                    err_msg="Element not found on current view."
                    logger.print_on_console("Element not found on current view.")
            else:
                log.error("Element not found!")
                err_msg="Element not found!"
                logger.print_on_console("Element not Found!")

            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
           
        except Exception as e:
            log.error("Error occured while performing setText " + str(e))
            err_msg="Error occured while performing setText"
            logger.print_on_console("Error occured while performing setText")
        return status, methodoutput, output, err_msg


    '''
        definition: Verifies if the element passed in the argument exists
        input: NA
        output: True/False
        outputtype: Boolean
    '''
    def VerifyExists(self, objectname, input, cord, original_device_width, original_device_height):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:          
            tap_cords = self.gotoobject(objectname, cord, original_device_width, original_device_height)
            # if tap_cords has coordinate values then element exists and if None then it doesn't
            if tap_cords is None:
                log.debug("Empty tap_cords found, VerifyExists False")
                return status, methodoutput, output, err_msg        
            status=TEST_RESULT_PASS
            methodoutput = TEST_RESULT_TRUE
            log.debug("tap_cords found, VerifyExists True")
        except Exception as e:
            log.error("Error occured while performing VerifyExistsIris "+str(e))
            logger.print_on_console("Error Occured while performing VerifyExistsIris")
            err_msg="Error occured while performing VerifyExistsIris"
        return status, methodoutput, output, err_msg

    '''
        definition: gets the text value from the element passed in the arguments
        input: NA
        output: Text Output
        outputtype: String
    '''
    def GetText(self, objectname, input, cord, original_device_width, original_device_height):
        self.driver = self.android_scrapping_obj.get_driver()
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:        
            time.sleep(2)
            screenshot_size = self.android_scrapping_obj.get_screenshot()
            screen_shot = cv2.imread("test_screenshot.png")
            device_height, device_width = screenshot_size[1], screenshot_size[0]
            
            # screen_shot = cv2.resize(screen_shot, (new_width, new_height), interpolation=cv2.INTER_AREA)
            original_device_coords = objectname.split(';')[2:6]
            coord_x = int(original_device_coords[0]) * (device_width/original_device_width)
            coord_y = int(original_device_coords[1]) * (device_height/original_device_height)

            coord_xx = int(original_device_coords[2]) * (device_width/original_device_width)
            coord_yy = int(original_device_coords[3]) * (device_height/original_device_height)

            ss_region = screen_shot[int(coord_y):int(coord_yy), int(coord_x):int(coord_xx)]
            ss_region=cv2.addWeighted(ss_region,1.5,np.zeros(ss_region.shape,ss_region.dtype),0,0) # increase the contrast of image
            
            if(TESSERACT_PATH_EXISTS):
                if SYSTEM_OS != 'Darwin':
                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                    os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                else:
                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/bin/tesseract'
                    os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/share/tessdata'

            string_output = pytesseract.image_to_string(ss_region) # currently reading the direct image, can be changed to get_ocr by uncommenting below line
            # string_output = self.get_ocr(screenshot_region)

            os.remove("test_screenshot.png")

            status=TEST_RESULT_PASS
            methodoutput = string_output
            output = string_output

        except Exception as e:
            log.error("Error occured while getting text "+str(e))
            logger.print_on_console("Error occured while getting text")
            err_msg="Error occured while getting text"

        del(screen_shot)
        del(device_width)
        del(device_height)
        del(ss_region)
        del(original_device_coords)
        del(original_device_height)
        del(original_device_width)
        del(coord_x)
        del(coord_y)
        del(coord_xx)
        del(coord_yy)
        
        return status, methodoutput, output, err_msg
    


    '''
        definition: Clears the text of the element passed in the arguments
        input: NA
        output: Pass/Fail
        outputtype: Boolean
    '''
    def ClearText(self, objectname, input, cord, original_device_width, original_device_height):
        self.driver = self.android_scrapping_obj.get_driver()
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            tap_cords = self.gotoobject(objectname, cord, original_device_width, original_device_height)
            elem = None

            if objectname in self.verified_fields:
                elem = self.verified_fields[objectname]

            if tap_cords or elem:
                if tap_cords and not elem:
                    elements = self.driver.find_elements_by_class_name("android.widget.EditText")
                    min_dist = sys.maxsize
                    if elements:
                        for element in elements:
                            x = element.location['x']
                            y = element.location['y']
                            dist = math.sqrt((x - int(tap_cords[0]))**2 + (y - int(tap_cords[1]))**2 )
                            if(dist<min_dist):
                                min_dist = dist
                                elem = element
                        x = elem.location['x']
                        y = elem.location['y']
                        xx = x+elem.size['width']
                        yy = y+elem.size['height']

                        if not ((x<tap_cords[0] and y<tap_cords[1]) and (xx>tap_cords[0] and yy>tap_cords[1])):
                            elem = None
                    else:
                        elem = None
                try:
                    if elem:
                        elem.clear()
                        if elem.text != '':
                            for i in elem.text:
                                textBefore = elem.text
                                self.driver.keyevent(67)
                                textAfter = elem.text
                                if textBefore == textAfter:
                                    break
                        log.debug("ClearText performed")
                        status=TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                    else:
                        logger.print_on_console("Invalid Element Found!")
                        log.error("Invalid Element Found!")
                        err_msg="Invalid Element Found!"
                except Exception as e:
                    log.error("Error occured while performing clearText "+str(e))
                    err_msg="Error occured while performing clearText"
                    logger.print_on_console("Element not found on current view.")
            else:
                logger.print_on_console("Element not Found!")
                log.error("Element Not Found!")
                err_msg="Element Not Found!"


            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
           
        except Exception as e:
            log.error("Error occured while performing clearText "+str(e))
            err_msg="Error occured while performing clearText"
            logger.print_on_console("Error occured while performing clearText")

        return status, methodoutput, output, err_msg

    '''
        definition: Verifies the text of the element passed in the arguments
        input: String
        output: True/False
        outputtype: Boolean
    '''
    def VerifyText(self, objectname, input, cord, original_device_width, original_device_height):
        self.driver = self.android_scrapping_obj.get_driver()
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:        
            screenshot_size = self.android_scrapping_obj.get_screenshot()
            screen_shot = cv2.imread("test_screenshot.png")
            device_height, device_width = screenshot_size[1], screenshot_size[0]
            # aspect_ratio = original_width / original_height
            original_device_coords = objectname.split(';')[2:6]
            coord_x = int(original_device_coords[0]) * (device_width/original_device_width)
            coord_y = int(original_device_coords[1]) * (device_height/original_device_height)

            coord_xx = int(original_device_coords[2]) * (device_width/original_device_width)
            coord_yy = int(original_device_coords[3]) * (device_height/original_device_height)

            ss_region = screen_shot[int(coord_y):int(coord_yy), int(coord_x):int(coord_xx)]
            ss_region=cv2.addWeighted(ss_region,1.5,np.zeros(ss_region.shape,ss_region.dtype),0,0)
            
            if(TESSERACT_PATH_EXISTS):
                if SYSTEM_OS != 'Darwin':
                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                    os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                else:
                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/bin/tesseract'
                    os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/share/tessdata'

            string_output = pytesseract.image_to_string(ss_region)  # currently reading direct image, can be changed by calling get_ocr
            
            # checking if input string matches the string result
            log.debug("Checking Text Values")
            if input==string_output:
                status=TEST_RESULT_PASS
                methodoutput = string_output
                output = TEST_RESULT_TRUE
            else:
                logger.print_on_console("Expected value is: ", input)
                logger.print_on_console("Actual value is: ", string_output)

            os.remove("test_screenshot.png")
        except Exception as e:
            log.error("Error occured while verifying text "+str(e))
            logger.print_on_console("Error occured while verifying text")
            err_msg="Error occured while verifying text"

        del(screen_shot)
        del(device_width)
        del(device_height)
        del(ss_region)
        del(original_device_coords)
        del(original_device_height)
        del(original_device_width)
        del(coord_x)
        del(coord_y)
        del(coord_xx)
        del(coord_yy)

        return status, methodoutput, output, err_msg

    '''
        definition : core of all the method, checks if the element is present on screen and returns the coordinates to operate on
        input: objectname, cord, original_device_width, original_device_height
        output: coordinates
        outputtype: tuple
    '''
    def gotoobject(self, objectname, cord, original_device_width, original_device_height):
        t=None
        try:
            encoded_image = cord.replace('b', '', 1)                # getting the base64 dataobject_image for finding object on device
            decoded_image = base64.b64decode(encoded_image)         # decoding the dataobject_image
            with open("template_image.png", "wb") as image_file:    
                image_file.write(decoded_image)                     # saving the dataobject_image as template_image temporarily

            screenshot_size = self.android_scrapping_obj.get_screenshot()       # getting the device screenshot and storing its dimensions
            screen_shot = cv2.imread("test_screenshot.png")            # reading the image file that above method created
            templateImage = cv2.imread("template_image.png", 0)         # reading template_image as grayscale
            device_height, device_width = screenshot_size[1], screenshot_size[0]    # storing device dimensions as height and width
            
            aspect_ratio = device_width / device_height             # calculating its aspect ratio for resizing purpose
            new_height = 1000                                       # for comparison, the screenshot will be resized to height of 1000
            new_width = int(aspect_ratio * new_height)              # calculating new width for resizing screenshot of height 1000px
            
            screen_shot = cv2.resize(screen_shot, (new_width, new_height), interpolation=cv2.INTER_AREA)        #resizing the screenshot image
            template_width, template_height = templateImage.shape[::-1]                 # storing dataobject height and width

            if len(screen_shot.shape) > 2 and screen_shot.shape[2] == 4:
                #convert the image from RGBA2RGB else causes error in matching template
                screen_shot = cv2.cvtColor(screen_shot, cv2.COLOR_BGRA2BGR)
            
            screen_shot_gray = cv2.cvtColor(screen_shot, cv2.COLOR_BGR2GRAY)                # converting resized screenshot image to grayscale for comparison
            matched_region = cv2.matchTemplate(screen_shot_gray, templateImage, cv2.TM_CCOEFF_NORMED)           # searching for dataobject image in screenshot
            threshold = 0.8                  # threshold to determine how much accurate the match has to be , low threshold = low precision , high threshold = high precision
            loc = np.where(matched_region>=threshold)           # storing regions of matches
            ind = np.unravel_index(np.argmax(matched_region, axis=None), matched_region.shape)
            total_points = []                # initializing total points
            pt=[]                              # initializing point to store element coord
            for pt in zip(*loc[::-1]):
                total_points.append(pt)

            device_coords = objectname.split(";")[2:6]          # retrieving coordinates of scraped dataobject

            os.remove("template_image.png")         # erasing temporary files
            os.remove("test_screenshot.png")

            if(len(pt) > 0):
                if(len(total_points)>1):
                    #If multiple matches are found, choose the one which is closest to the captured coordinates.
                    point = ()
                    min_dist = sys.maxsize
                    for p in total_points:
                        dist = math.sqrt( (int(device_coords[0]) * (new_width/original_device_width) - p[0])**2 + (int(device_coords[1]) * (new_height/original_device_height) - p[1])**2 )
                        if(dist<min_dist):
                            min_dist = dist
                            point = p
                else:
                    point = (ind[1],ind[0])

                resized_template_width = ( template_width * (device_width/new_width) )          # re-scaling found coordinates wrt testing device
                resized_template_height = ( template_height * (device_height/new_height) )
                
                resized_x = point[0] * (device_width/new_width)
                resized_y = point[1] * (device_height/new_height)

                tap_x = resized_x + resized_template_width / 2              # coordinates to perform operation
                tap_y = resized_y + resized_template_height / 2

                # returning coordinates
                t=(tap_x, tap_y)
                #  del() del all variables other than t
            else:
                log.error("Coordinates not found")
                logger.print_on_console("Coords not found")

            # if total_points !=[]:
            #     cv2.rectangle(screen_shot, total_points[0], (total_points[0][0] + template_width, total_points[0][1] + template_height), (0, 0, 255), 1)
            #     self.verifyexist = True
            

        except Exception as e:
            logger.print_on_console("Error occured while finding element")
            log.error("Error occured while finding element "+str(e))
        # del() del all variables
        del(encoded_image)
        del(decoded_image)
        del(aspect_ratio)
        del(screen_shot)
        del(screen_shot_gray)
        del(templateImage)
        del(loc)
        del(ind)
        del(total_points)
        del(resized_x)
        del(resized_y)
        del(resized_template_width)
        del(resized_template_height)
        del(template_height)
        del(template_width)
        del(new_height)
        del(new_width)
        del(device_coords)
        del(device_height)
        del(device_width)
        del(point)
        del(min_dist)



        return t
    
    def get_ocr(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # write the grayscale image to disk as a temporary file.
        filename = str(int(time.time()))+".png"
        cv2.imwrite(filename, gray)
        # load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
        text = pytesseract.image_to_string(cv2.imread(filename))
        os.remove(filename)
        return text

        