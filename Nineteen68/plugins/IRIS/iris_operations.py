import logger
import time
import logging
import PIL.ImageGrab
import numpy as np
import cv2
import screeninfo
from PIL import Image
import pyautogui
from constants import *
log = logging.getLogger('iris_operations.py')
import os
from pytesseract import pytesseract

#Input Image Name
vertical = []
horizontal = []

def remove_duplicates(lines):
    # remove duplicate lines (lines within 10 pixels of eachother)
    for x1, y1, x2, y2 in lines:
        for index, (x3, y3, x4, y4) in enumerate(lines):
            if y1 == y2 and y3 == y4:
                diff = abs(y1-y3)
            elif x1 == x2 and x3 == x4:
                diff = abs(x1-x3)
            else:
                diff = 0
            if diff < 15 and diff is not 0:
                del lines[index]
    return lines

def sort_line_list(lines,pos):
    # sort lines into horizontal and vertical
    vertical = []
    for line in lines:
        if line[0] == line[2]:
            vertical.append(line)
    vertical.sort()
    return vertical

def get_ocr(image):
    image = cv2.resize(image,(0,0),fx=5,fy=5)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # write the grayscale image to disk as a temporary file.
    filename = str(int(time.time()))+".png"
    cv2.imwrite(filename, gray)
    # load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file

    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text

def hough_transform_p(img,pos):
    global horizontal,vertical
    # open and process images
    img_copy = img.copy()
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

    img = cv2.filter2D(img, -1, kernel)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    #aver = img[:, :].mean()
    #ret,edges = cv2.threshold(gray,aver,255,cv2.THRESH_BINARY_INV)
    # probabilistic hough transform
    lines = cv2.HoughLinesP(edges,rho=1, theta=np.pi, threshold=int(0.8*edges.shape[0]), minLineLength=int(0.6*edges.shape[0]), maxLineGap=int(0.02*edges.shape[0]))
    lines_t = []
    for line in lines:
        lines_t.append(line[0].tolist())
    # remove duplicates
    lines = remove_duplicates(lines_t)

    # draw image
    for i in range(len(lines)):
        if(lines[i]!=[0,0,0,0]):
            cv2.line(img_copy,(lines[i][0], lines[i][1]),(lines[i][2],lines[i][3]), (0, 0, 255), 1)

    # sort lines into vertical & horizontal lists
    if(pos==1):
        vertical = sort_line_list(lines,1)
    else:
        horizontal = sort_line_list(lines,2)

def data_in_cells(image,row,column):
    text = ''
    if(row<len(horizontal) and column<len(vertical)):
        img = image[horizontal[row-1][0]+2:horizontal[row][0]-2,vertical[column-1][0]+2:vertical[column][0]-2]
        text = get_ocr(img)
    else:
        logger.print_on_console("Invalid Input for row and column number")
    return text

def gotoobject(elem):
        img_rgb = elem.decode('base64')
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
    def clickiris(self,element,*args):
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            res = gotoobject(element['cord'])
            if(res):
                pyautogui.click()
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                logger.print_on_console("Object not found")
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in clickiris")
        return status,result,value,err_msg

    def settextiris(self,element,*args):
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            res = gotoobject(element['cord'])
            if(res):
                pyautogui.click()
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                pyautogui.typewrite(args[0][0], interval=0.1)
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                logger.print_on_console("Object not found")
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in settextiris")
        return status,result,value,err_msg

    def gettextiris(self,element,*args):
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            if(os.path.isdir(os.environ["NINETEEN68_HOME"] + '/Scripts/Tesseract-OCR')):
                pytesseract.tesseract_cmd = os.environ["NINETEEN68_HOME"] + '/Scripts/Tesseract-OCR/tesseract'
                os.environ["TESSDATA_PREFIX"] = os.environ["NINETEEN68_HOME"] + '/Scripts/Tesseract-OCR/tessdata'
                with open("cropped.png", "wb") as f:
                    f.write(element['cord'].decode('base64'))
                image = cv2.imread("cropped.png")
                text = get_ocr(image)
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
                value = text
                os.remove('cropped.png')
            else:
                log.error("Tesseract module not found.")
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in gettextiris")
        return status,result,value,err_msg

    def getrowcountiris(self,element,*args):
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            with open("cropped.png", "wb") as f:
                f.write(element['cord'].decode('base64'))
            img = cv2.imread("cropped.png")
            hough_transform_p(img,1)
            # rotated = imutils.rotate_bound(img, 270)
            rotated = np.rot90(img,1)
            cv2.imwrite("rotated.png", rotated)
            time.sleep(1)
            img = cv2.imread("rotated.png")
            hough_transform_p(img,2)
            status  = TEST_RESULT_PASS
            result = TEST_RESULT_TRUE
            value = len(horizontal)-1
            os.remove('cropped.png')
            os.remove('rotated.png')
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in gettextiris")
        return status,result,value,err_msg

    def getcolcountiris(self,element,*args):
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            with open("cropped.png", "wb") as f:
                f.write(element['cord'].decode('base64'))
            img = cv2.imread("cropped.png")
            hough_transform_p(img,1)
            # rotated = imutils.rotate_bound(img, 270)
            rotated = np.rot90(img,1)
            cv2.imwrite("rotated.png", rotated)
            time.sleep(1)
            img = cv2.imread("rotated.png")
            hough_transform_p(img,2)
            status  = TEST_RESULT_PASS
            result = TEST_RESULT_TRUE
            value = len(vertical)-1
            os.remove('cropped.png')
            os.remove('rotated.png')
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in gettextiris")
        return status,result,value,err_msg

    def getcellvalueiris(self,element,*args):
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        row = int(args[0][0])
        col = int(args[0][1])
        try:
            self.getrowcountiris(element)
            if(os.path.isdir(os.environ["NINETEEN68_HOME"] + '/Scripts/Tesseract-OCR')):
                pytesseract.tesseract_cmd = os.environ["NINETEEN68_HOME"] + '/Scripts/Tesseract-OCR/tesseract'
                os.environ["TESSDATA_PREFIX"] = os.environ["NINETEEN68_HOME"] + '/Scripts/Tesseract-OCR/tessdata'
                with open("cropped.png", "wb") as f:
                    f.write(element['cord'].decode('base64'))
                img = cv2.imread("cropped.png")
                text = data_in_cells(img,row,col)
                status  = TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
                value = text
                os.remove('cropped.png')
            else:
                log.error("Tesseract module not found.")
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in gettextiris")
        return status,result,value,err_msg