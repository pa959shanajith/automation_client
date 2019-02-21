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
import base64,json
from pyrobot import Robot
import imutils
import sys,math
from uuid import uuid4
vertical = []
horizontal = []
verifyexists = []
TESSERACT_PATH = os.environ["NINETEEN68_HOME"] + '/Scripts/Tesseract-OCR'
TESSERACT_PATH_EXISTS = os.path.isdir(TESSERACT_PATH)

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
    text = None
    if(row<len(horizontal) and column<len(vertical)):
        img = image[horizontal[row-1][0]+2:horizontal[row][0]-2,vertical[column-1][0]+2:vertical[column][0]-2]
        text = get_ocr(img)
    else:
        logger.print_on_console("Invalid Input for row and column number")
    return text

def gotoobject(elem):
    byte_mirror = base64.b64encode(elem['cord'].encode('utf-8'))
    b64 = base64.b64decode(byte_mirror)
    mirror = b64[2:len(b64)-1]
    img_rgb = base64.b64decode(mirror)
    fh = open("sample.png", "wb")
    fh.write(img_rgb)
    fh.close()

    im = PIL.ImageGrab.grab()
    im.save('test.png')
    img_rgb = cv2.imread('test.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread('sample.png',0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)
    ind = np.unravel_index(np.argmax(res, axis=None), res.shape)
    pt = []
    total_points = []
    for pt in zip(*loc[::-1]):
        total_points.append(pt)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    #cv2.imwrite('res1.png',img_rgb)
    if(len(pt) > 0):
        if(len(total_points)>1):
            """If multiple matches are found, choose the one which is closest to the captured coordinates."""
            point = ()
            min_dist = sys.maxsize
            for p in total_points:
                dist = math.sqrt( (int(elem['coordinates'][0]) - p[0])**2 + (int(elem['coordinates'][1]) - p[1])**2 )
                if(dist<min_dist):
                    min_dist = dist
                    point = p
        else:
            point = (ind[1],ind[0])
        pyautogui.moveTo(point[0]+ int(w/2),point[1] + int(h/2))
    else:
        """If no matches are found, try scaling down the image. If still no match, try scaling up."""
        point,w,h = scaleUpOrDown(0.2,elem,template,img_rgb)
        if(len(point)>0):
            pyautogui.moveTo(point[0]+ int(w/2),point[1] + int(h/2))
        else:
            point,w,h = scaleUpOrDown(2.0,elem,template,img_rgb)
            if(len(point)>0):
                pyautogui.moveTo(point[0]+ int(w/2),point[1] + int(h/2))
    if(os.path.isfile('sample.png')):
        os.remove('sample.png')
    if(os.path.isfile('test.png')):
        os.remove('test.png')
    return point

def find_relative_image(elements,const_new_coordinates):
    try:
        coordinates = []
        rel_image = ''
        if(len(elements)>2):
            im = PIL.ImageGrab.grab()
            im.save('find_relative.png')
            image = cv2.imread('find_relative.png')

            #Start and end points of constant and relative image
            a1 = elements[1]
            a2 = elements[2]
            a3 = elements[3]
            a4 = elements[0]
            #Distance between two image
            dist = int(a2[0])-int(a4[0])

            #Dimensions of captured relative image
            width = int(a3[0])-int(a2[0])
            height = abs(int(a2[1])-int(a3[1]))

            #--Relative Coordinates--#
            starty = int(const_new_coordinates[1]) + (int(a2[1]) - int(a4[1]))
            endy = int(const_new_coordinates[1]) + (int(a2[1]) - int(a4[1])) + height
            startx = int(const_new_coordinates[0]) + dist
            endx = int(const_new_coordinates[0]) + dist + width

            coordinates = [startx,starty,endx,endy]
            img = image[starty:endy,startx:endx]
            cv2.imwrite('output.png',img)
            with open('output.png', "rb") as imageFile:
                rel_image = base64.b64encode(imageFile.read())
            os.remove('find_relative.png')
            os.remove('output.png')
    except Exception as e:
        log.error(e)
        logger.print_on_console("Error occured in finding relative image.")
    return rel_image,coordinates

def check_duplicates(scrapedata, socketIO):
    try:
        duplicates = []
        mirror = scrapedata['mirror']
        byte_mirror = base64.b64encode(mirror.encode('utf-8'))
        b64 = base64.b64decode(byte_mirror)
        mirror = b64[2:len(b64)-1]
        with open('screen.png','wb') as f:
            f.write(base64.b64decode(mirror))
        img_rgb = cv2.imread('screen.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        for elem in scrapedata['view']:
            byte_mirror = base64.b64encode(elem['cord'].encode('utf-8'))
            b64 = base64.b64decode(byte_mirror)
            mirror = b64[2:len(b64)-1]
            img = base64.b64decode(mirror)
            fh = open("sample.png", "wb")
            fh.write(img)
            fh.close()
            template = cv2.imread('sample.png',0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where( res >= threshold)
            ind = np.unravel_index(np.argmax(res, axis=None), res.shape)
            p = [0,0]
            points = []
            for pt in zip(*loc[::-1]):
                if(not ((pt[0] in range(p[0]-2,p[0]+3)) and (pt[1] in range(p[1]-2,p[1]+3)))):
                    points.append(pt)
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                p = list(pt)
            #cv2.imwrite('res.png',img_rgb)
            if(len(points)>1):
                duplicates.append(elem['custname'])
        socketIO.emit('iris_operations_result',str(json.dumps(duplicates)))
        if(os.path.isfile('sample.png')):
            os.remove('sample.png')
        if(os.path.isfile('screen.png')):
            os.remove('screen.png')
    except Exception as e:
        log.error(e)
        logger.print_on_console("Error while checking for duplicate objects.")

def scaleUpOrDown(arg,elem,template,img_rgb):
    try:
        point = ()
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        for scale in np.linspace(arg, 1.0, 20)[::-1]:
            resized = imutils.resize(template, width = int(template.shape[1] * scale))
            resized_width = resized.shape[1]
            resized_height = resized.shape[0]
            res = cv2.matchTemplate(img_gray,resized,cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where( res >= threshold)
            ind = np.unravel_index(np.argmax(res, axis=None), res.shape)
            pt = []
            total_points = []
            for pt in zip(*loc[::-1]):
                total_points.append(pt)
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            if(len(pt) > 0):
                if(len(total_points)>1):
                    point = ()
                    min_dist = sys.maxsize
                    for p in total_points:
                        dist = math.sqrt( (int(elem['coordinates'][0]) - p[0])**2 + (int(elem['coordinates'][1]) - p[1])**2 )
                        if(dist<min_dist):
                            min_dist = dist
                            point = p
                else:
                    point = (ind[1],ind[0])
                break
    except Exception as e:
        log.error(e)
        logger.print_on_console("Error while scaling image.")
    return point,resized_width,resized_height

def update_dataset(image_data):
    try:
        mirror = image_data['cord']
        byte_mirror = base64.b64encode(mirror.encode('utf-8'))
        b64 = base64.b64decode(byte_mirror)
        mirror = b64[2:len(b64)-1]
        filename = os.environ['NINETEEN68_HOME'] + '/Lib/site-packages/prediction/Dataset/' + str(image_data['type']) + '/' + str(uuid4()).replace("-","")+".png"
        with open(filename,'wb') as f:
            f.write(base64.b64decode(mirror))
        return True
    except Exception as e:
        log.error(e)
        return False

class IRISKeywords():
    def clickiris(self,element,*args):
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            img = None
            if(len(args) == 3 and args[2]!='' and len(verifyexists)>0):
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img,res = find_relative_image(elements, verifyexists)
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                res = gotoobject(element)
            if(len(res)>0):
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
            img = None
            if(len(args) == 3 and args[2]!='' and len(verifyexists)>0):
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img,res = find_relative_image(elements, verifyexists)
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                res = gotoobject(element)
            if(len(res)>0):
                pyautogui.click()
                robot = Robot()
                robot.ctrl_press('a')
                time.sleep(0.5)
                robot.key_press('backspace')
                time.sleep(0.5)
                pyautogui.typewrite(args[0][0], interval=0.2)
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
            if(TESSERACT_PATH_EXISTS):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if(len(args) == 3 and args[2]!='' and len(verifyexists)>0):
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img,res = find_relative_image(elements, verifyexists)
                else:
                    byte_mirror = base64.b64encode(element['cord'].encode('utf-8'))
                    b64 = base64.b64decode(byte_mirror)
                    img = b64[2:len(b64)-1]
                with open("cropped.png", "wb") as f:
                    f.write(base64.b64decode(img))
                image = cv2.imread("cropped.png")
                text = ''
                if(len(args[0])==1 and args[0][0].lower().strip() == 'select'):
                    robot = Robot()
                    height = int(element['coordinates'][3]) - int(element['coordinates'][1])
                    pyautogui.moveTo(int(element['coordinates'][2]),int(element['coordinates'][3])-int(height/2))
                    pyautogui.dragTo(int(element['coordinates'][0]),int(element['coordinates'][1])+int(height/2),button='left')
                    robot.ctrl_press('c')
                    time.sleep(1)
                    text = robot.get_clipboard_data()
                elif(len(args[0])==1 and args[0][0].lower().strip() == 'date'):
                    img = Image.open('cropped.png')
                    imgr = img.resize((img.size[0] * 10, img.size[1] * 10), Image.ANTIALIAS)
                    imgr.save('scaled_cropped.png')
                    '''
                    image = cv2.imread('scaled_cropped.png')
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    avg = np.mean(gray)
                    gray = cv2.threshold(gray, 0.7*avg, 255, cv2.THRESH_BINARY_INV)[1]
                    '''
                    filename = 'scaled_cropped.png'
                    img = cv2.imread(filename,0)
                    Z = img.reshape((-1,))

                    # convert to np.float32
                    Z = np.float32(Z)

                    # define criteria, number of clusters(K) and apply kmeans()
                    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                    K = 2
                    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
                    lbllist = np.unique(label)

                    # Now convert back into uint8, and make original image
                    center = np.uint8(center)
                    res = center[label.flatten()]
                    res2 = res.reshape((img.shape))
                    a=int(center[0][0]/2+center[1][0]/2)
                    if((center[0]>center[1] and center[0][0]>center[1][0]) or (center[0]<center[1] and center[0][0]<center[1][0])):
                        a=255 - a
                        res2 = cv2.bitwise_not(res2)
                    img,gray = cv2.threshold(res2,a,255,cv2.THRESH_BINARY)
                    cv2.imwrite('demo_cropped.png', gray)
                    text = pytesseract.image_to_string(Image.open('demo_cropped.png'))
                    if(os.path.isfile('scaled_cropped.png')):
                        os.remove('scaled_cropped.png')
                    if(os.path.isfile('demo_cropped.png')):
                        os.remove('demo_cropped.png')
                else:
                    text = get_ocr(image)
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
                if(isinstance(text,str)):
                    value = text.encode('utf-8')
                else:
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
            img = None
            if(len(args) == 3 and args[2]!='' and len(verifyexists)>0):
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img,res = find_relative_image(elements, verifyexists)
            else:
                byte_mirror = base64.b64encode(element['cord'].encode('utf-8'))
                b64 = base64.b64decode(byte_mirror)
                img = b64[2:len(b64)-1]
            with open("cropped.png", "wb") as f:
                f.write(base64.b64decode(img))
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
            logger.print_on_console("Error occured in getrowcountiris")
        return status,result,value,err_msg

    def getcolcountiris(self,element,*args):
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            img = None
            if(len(args) == 3 and args[2]!='' and len(verifyexists)>0):
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img,res = find_relative_image(elements, verifyexists)
            else:
                byte_mirror = base64.b64encode(element['cord'].encode('utf-8'))
                b64 = base64.b64decode(byte_mirror)
                img = b64[2:len(b64)-1]
            with open("cropped.png", "wb") as f:
                f.write(base64.b64decode(img))
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
            logger.print_on_console("Error occured in getcolcountiris")
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
            if(TESSERACT_PATH_EXISTS):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if(len(args) == 3 and args[2]!='' and len(verifyexists)>0):
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img,res = find_relative_image(elements, verifyexists)
                else:
                    byte_mirror = base64.b64encode(element['cord'].encode('utf-8'))
                    b64 = base64.b64decode(byte_mirror)
                    img = b64[2:len(b64)-1]
                with open("cropped.png", "wb") as f:
                    f.write(base64.b64decode(img))
                img = cv2.imread("cropped.png")
                text = data_in_cells(img,row,col)
                if(text != None):
                    status  = TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                    value = text
                os.remove('cropped.png')
            else:
                log.error("Tesseract module not found.")
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in getcellvalueiris")
        return status,result,value,err_msg

    def verifyexistsiris(self,element,*args):
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            global verifyexists
            if(len(args) == 3 and args[2]!='' and len(verifyexists)>0):
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img,res = find_relative_image(elements, verifyexists)
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                res = gotoobject(element)
            if(len(res)>0):
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
                verifyexists = res
                logger.print_on_console('Element exists.')
            else:
                logger.print_on_console("Object not found.")
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in verifyexistsiris")
        return status,result,value,err_msg

    def verifytextiris(self,element,*args):
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = [args[0][0],'null']
        try:
            verifytext = args[0][0]
            text = ''
            if(TESSERACT_PATH_EXISTS):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if(len(args) == 3 and args[2]!='' and len(verifyexists)>0):
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img,res = find_relative_image(elements, verifyexists)
                else:
                    byte_mirror = base64.b64encode(element['cord'].encode('utf-8'))
                    b64 = base64.b64decode(byte_mirror)
                    img = b64[2:len(b64)-1]
                with open("cropped.png", "wb") as f:
                    f.write(base64.b64decode(img))
                image = cv2.imread("cropped.png")
                text = get_ocr(image)
                if(isinstance(text,str)):
                    text = text.encode('utf-8')
                if(verifytext == text):
                    status= TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                else:
                    logger.print_on_console("Expected value is:", verifytext)
                    logger.print_on_console("Actual value is:", text)
                value = [verifytext,text]
                os.remove('cropped.png')
            else:
                log.error("Tesseract module not found.")
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in verifytextiris")
        return status,result,value,err_msg