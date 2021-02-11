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
import imutils
import sys,math
from uuid import uuid4
import codecs
from encryption_utility import AESCipher
if SYSTEM_OS != 'Darwin':
    import win32clipboard
    from pyrobot import Robot
    import pythoncom
    import pywinauto
vertical = []
horizontal = []
relativeCoordinates = []
verifyFlag = False
dropIrisFlag = False
TESSERACT_PATH = os.environ["AVO_ASSURE_HOME"] + '/Lib/Tesseract-OCR'
TESSERACT_PATH_EXISTS = os.path.isdir(TESSERACT_PATH)

def remove_duplicates(lines):
    """
    Definition: Remove duplicate lines (lines within 10 pixels of eachother)
    Input : lines
    Output : sorted lines
    Method Referenced in : hough_transform_p
    """
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
        del index,diff #deleting variables
    del x1,x2,y1,y2 #deleting variables
    return lines

def sort_line_list(lines):
    """
    Definition: Sort lines into horizontal and vertical
    Input : lines
    Output : sorted lines
    Method Referenced in : hough_transform_p
    """
    vertical = []
    for line in lines:
        if line[0] == line[2]:
            vertical.append(line)
    vertical.sort()
    del line,lines #deleting variables
    return vertical

def get_ocr(image):
    """
    Definition: Converts image to text
    Input : image
    Output : text
    Method Referenced in : data_in_cells, gettextiris, verifytextiris
    """
    """Step 1. Resize input image"""
    rez_image = cv2.resize(image,(0,0),fx=5,fy=5)

    """Step 2: Convert the resized image to greyscle"""
    gray_img = cv2.cvtColor(rez_image, cv2.COLOR_BGR2GRAY)

    """Step 3: Apply blur to smoothen images
        Types of blurs:
            1.Averaging :It simply takes the average of all the pixels under the kernel area and replaces the central element.
                blur = cv.blur(img,(5,5))
            2.Gaussian blurring : it is highly effective in removing Gaussian noise from an image.
                blur = cv.GaussianBlur(img,(5,5),0)
            3.Median Blurring : takes the median of all the pixels under the kernel area and the central element is replaced with this median value.
                                highly effective against salt-and-pepper noise in an image.
                median = cv.medianBlur(img,5)
            4.Bilateral Filtering : highly effective in noise removal while keeping edges sharp
                blur = cv.bilateralFilter(img,9,75,75)
    """
    filter_img = cv2.medianBlur(gray_img, 5)

    """Step 4: Apply thresholding methods to remove edges
    Types of thresholding:
        1.Adaptive Thresholding: Used when image has different lighting conditions in different areas.
                                 Adaptive Method - It decides how thresholding value is calculated.
                                    cv2.ADAPTIVE_THRESH_MEAN_C : threshold value is the mean of neighbourhood area.
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C : threshold value is the weighted sum of neighbourhood values where weights are a gaussian window.
            th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C \ cv2.THRESH_BINARY,11,2)
            th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C \ cv2.THRESH_BINARY,11,2)
        2.Otsu's Binarization: it automatically calculates a threshold value from image histogram for a bimodal image.
            th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        3.Simple Thresholding :
    Function: cv2.threshold(p1,p2,p3,p4)
        Parameter 1:is the source image, which should be a grayscale image.
        Parameter 2:the threshold value which is used to classify the pixel values.
        Parameter 3:the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value.
        Parameter 4:OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function. Different types are:
            cv2.THRESH_BINARY
            cv2.THRESH_BINARY_INV
            cv2.THRESH_TRUNC
            cv2.THRESH_TOZERO
            cv2.THRESH_TOZERO_INV
            more info :https://www.learnopencv.com/opencv-threshold-python-cpp/
    """
    thresh_img = cv2.threshold(filter_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] # Otsu's thresholding -inv
    # thresh_img = cv2.threshold(filter_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] # Otsu's thresholding

    """Step 5: Write the image created from mentioned steps, to disk as a temporary file."""
    filename = str(int(time.time()))+".png"
    cv2.imwrite(filename, thresh_img)

    """Step 6: Load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file"""
    try:
        text = pytesseract.image_to_string(Image.open(filename))
    except Exception as e:
        log.info('WARNING!: error occured in get_ocr, ERR_MSG : ' + str(e))
        if(TESSERACT_PATH_EXISTS) :
            log.info('pytessaract is not pointing to TESSERACT_PATH, adding TESSERACT_PATH to path')
            pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
            text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)

    del image, rez_image, gray_img, filter_img, thresh_img, filename #deleting variables
    return text

def hough_transform_p(img, pos):
    """
    Def : Performs a hough transformation(hough transformation is a technique to find imperfect instances of objects within a certain class of shapes by a voting procedure). We use it to detect lines.
    Input : Image, Position
    Output : N/A, assigns sorted line pos to horizontal and vertical global variables
    Method Referenced in : getrowcountiris, getcolcountiris
    Reference : https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    """
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
    if(isinstance(lines,np.ndarray)):
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
            vertical = sort_line_list(lines)
        else:
            horizontal = sort_line_list(lines)
    del img_copy, kernel, img, pos, gray, edges, lines, lines_t #deleting variables


def data_in_cells(image,row,column):
    """
    Def : This function will return the data(text) from mentioned table image
    Input : image,row,column
    Output : text
    Method Referenced in : getcellvalueiris
    """
    text = None
    if(row<len(horizontal) and column<len(vertical)):
        img = image[horizontal[row-1][0]+2:horizontal[row][0]-2,vertical[column-1][0]+2:vertical[column][0]-2]
        text = get_ocr(img)
    else:
        logger.print_on_console("Invalid Input for row and column number")
    del image, row, column #deleting variables
    return text

def get_cell_position(image,row,column):
    """
    Def : This function will return the X and Y position of cell in the table
    Input : image,row,column
    Output : X,Y
    Method Referenced in : setcellvalueiris, clickcelliris, doubleclickcelliris, rightclickcelliris, mousehovercelliris
    """
    validFlag = False
    ele_w = None
    ele_h = None
    X = None
    Y = None
    try:
        if(row<len(horizontal) and column<len(vertical)):
            img = image[horizontal[row-1][0]+2:horizontal[row][0]-2,vertical[column-1][0]+2:vertical[column][0]-2]
            ele_h,ele_w,c=img.shape
            validFlag = True
        else:
            logger.print_on_console("Invalid Input for row and column number")

        if (validFlag):
            width = 0
            r = 1
            #To get width(left ->right) till the element then add the half width of target element to get total X
            for i in range(1,column):
                img = None
                img = image[horizontal[r-1][0]+2:horizontal[r][0]-2,vertical[i-1][0]+2:vertical[i][0]-2]
                h,wCell,c=img.shape
                width = width + wCell
            X = width + (ele_w/2)

            #To get height(top -> bottom) till the element then add the half height of target element to get total Y
            height = 0
            for i in range(1,row):
                img = None
                img = image[horizontal[row-1][0]+2:horizontal[row][0]-2,vertical[column-1][0]+2:vertical[column][0]-2]
                hCell,w,c=img.shape
                height = height + hCell
            Y = height + (ele_h/2)

            del width, height, img, h, hCell, w, wCell, c #deleting variables
    except Exception as e:
        log.error("Error occurred in get_cell_position, Err_Msg : ",e)
        logger.print_on_console("Error while fetching cell position.")
    del image, row, column, ele_h, ele_w #deleting variables
    return X, Y

def image_match(imageA,imageB):
    """
    Def : This function will return True/False if two images match
    Input : imageA,imageB
    Output : Boolean
    Method Referenced in : setcellvalueiris, clickcelliris, doubleclickcelliris, rightclickcelliris, mousehovercelliris
    """
    matchFlag = False
    if(imageA.shape == imageB.shape):
        log.debug('Images are of same size/shape')
        diff = cv2.subtract(imageA,imageB)
        b,g,r = cv2.split(diff)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            log.debug('Images are identical; return true')
            matchFlag = True
        else: log.debug('Images are non - identical; return false')
    else:
        log.debug('Images are not of the same size/shape, returning False')
    return matchFlag

def gotoobject(elem):
    """
    Def : Return a match of the scraped IRIS image. Compares the IRIS Image over the DOM and returns Image co-ordinates, if multiple matches are found then compares best possible match via the original IRIS image co-ordinates.
    Input : IRIS element object
    Output : point (matched image co-ordinates)
    Method Referenced in : clickiris, doubleclickiris, rightclickiris, settextiris, cleartextiris, setsecuretextiris, gettextiris, verifyexistsiris
    """
    mirror = get_byte_mirror(elem['cord'])
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
    """
    Template matching:
        Template matching is a technique in digital image processing for finding small parts of an image which match a template image.
        It can be used in manufacturing as a part of quality control, a way to navigate a mobile robot, or as a way to detect edges in images.
        The main challenges in the template matching task are: occlusion, detection of non-rigid transformations, illumination and background changes, background clutter and scale changes.

        T′(x′,y′)=T(x′,y′)−1/(w⋅h)⋅∑x′′,y′′T(x′′,y′′)

    Template matching methods:
       1. cv2.TM_CCOEFF( Template Matching Correlation Coefficient ) : The −1/(w⋅h)⋅∑x″,y″T(x″,y″) in the TM_CCOEFF method is simply used to a) make the template and image zero mean and b) make the dark parts of the image negative values and the bright parts of the image positive values.
       This means that when bright parts of the template and image overlap you'll get a positive value in the dot product, as well as when dark parts overlap with dark parts (-ve value x -ve value gives +ve value). That means you get a +ve score for both bright parts matching and dark parts matching.
       When you have dark on template (-ve) and bright on image (+ve) you get a -ve value. And when you have bright on template (+ve) and dark on image (-ve) you also get a -ve value. This means you get a negative score on mismatches.
       2. cv2.TM_CCOEFF_NORMED :
       3. cv2.TM_CCORR( Template Matching Correlation ) : When the −1/(w⋅h)⋅∑x″,y″T(x″,y″) term is absent, i.e. in TM_CCORR method, then you don't get any penalty when there are mismatches between the template and the image. Effectively this method is measuring where you get the brightest set of pixels
       in the image that are the same shape to the template.
       4. cv2.TM_CCORR_NORMED :
       5. cv2.TM_SQDIFF( Template Matching Square Difference ) :
       6. cv2.TM_SQDIFF_NORMED :
    """
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

    """
    KeyPoint Matching
    """
    threshold = 0.9
    loc = np.where( res >= threshold)
    ind = np.unravel_index(np.argmax(res, axis=None), res.shape)
    pt = []
    total_points = []
    dist = None
    min_dist = None
    for pt in zip(*loc[::-1]):
        total_points.append(pt)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2) #cv2.rectangle(img, top_left, bottom_right, 255, 2)
    #cv2.imwrite('res1.png',img_rgb)
    if(len(pt) > 0):
        if(len(total_points)>1):
            """If multiple matches are found, choose the one which is closest to the captured coordinates."""
            point = ()
            min_dist = sys.maxsize # sys.maxsize - fetches the largest value a variable of data type Py_ssize_t can store
            for p in total_points:
                dist = math.sqrt( (int(elem['coordinates'][0]) - p[0])**2 + (int(elem['coordinates'][1]) - p[1])**2 ) #finding the square root
                if(dist<min_dist):
                    min_dist = dist
                    point = p
        else:
            point = (ind[1],ind[0])
        if(not dropIrisFlag): pyautogui.moveTo(point[0]+ int(w/2),point[1] + int(h/2))
    else:
        """If no matches are found, try scaling down the image. If still no match, try scaling up."""
        point,w,h = scaleUpOrDown(0.2,elem,template,img_rgb)
        if(len(point)>0):
            if(not dropIrisFlag):pyautogui.moveTo(point[0]+ int(w/2),point[1] + int(h/2))
        else:
            point,w,h = scaleUpOrDown(2.0,elem,template,img_rgb)
            if(len(point)>0):
                if(not dropIrisFlag):pyautogui.moveTo(point[0]+ int(w/2),point[1] + int(h/2))
    if(os.path.isfile('sample.png')):
        os.remove('sample.png')
    if(os.path.isfile('test.png')):
        os.remove('test.png')
    del elem, mirror, img_rgb, img_gray, fh, im, template, res, threshold, loc, ind, pt, total_points, dist, min_dist #deleting variables
    return point, w, h

def find_relative_image(elements, const_new_coordinates):
    """
    Def : Finds the co-ordinates of the relative image
    Input : elements, const_new_coordinates
    Output : rel_image(the original image), co-ordinates(relative image co-ordinates)
    Method Referenced in : clickiris, doubleclickiris, rightclickiris, settextiris, cleartextiris, setsecuretextiris, gettextiris, verifyexistsiris, getrowcountiris, getcolcountiris, getcellvalueiris, verifytextiris
    """
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
        log.error("Error occurred in finding relative image, Err_Msg : ",e)
        logger.print_on_console("Error occurred in finding relative image.")
    del elements, const_new_coordinates, a1, a2, a3, a4, dist, width, height, starty, endy, startx, endx, img #deleting variables
    return rel_image, coordinates

def check_duplicates(scrapedata, socketIO):
    """
    Def : This method is used to check for duplicate IRIS objects in IRIS scrape data
    Input : scrapedata, socketIO
    Output : N/A, emits socket data (json format)
    Method Referenced in : webserver
    """
    try:
        duplicates = []
        mirror = get_byte_mirror(scrapedata['mirror'])
        with open('screen.png','wb') as f:
            f.write(base64.b64decode(mirror))
        img_rgb = cv2.imread('screen.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        for elem in scrapedata['view']:
            mirror = get_byte_mirror(elem['cord'])
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
        del duplicates, mirror, img_rgb, img_gray, scrapedata, img, fh, template, w, h, res, threshold, loc, ind, p, pt, socketIO #deleting variables
    except Exception as e:
        log.error("Error while checking for duplicate objects, Err_Msg : ",e)
        logger.print_on_console("Error while checking for duplicate objects.")

def scaleUpOrDown(arg,elem,template,img_rgb):
    """
    Def : This function resizes(scales up or down) the scraped image
    Input : element['coordinates'], template, RGB image
    Output : point, resized_width, resized_height
    Method Referenced in : gotoobject
    """
    dist = None
    min_dist = None
    img_gray = None
    point = ()
    w = None
    h = None
    try:
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
        log.error("Error while scaling image, Err_Msg : ", e)
        logger.print_on_console("Error while scaling image.")
    del arg, elem, template, img_rgb, img_gray, w, h, scale, resized, threshold, res, loc, ind, pt, total_points, min_dist, dist # deleting variables
    return point, resized_width, resized_height

def update_dataset(image_data):
    """
    Def : This method is to check and assign dataset values(button,textbox,etc) to the IRIS image
    Input : image data
    Output : boolean value
    Method Referenced in : webserver
    """
    flag = False
    try:
        if(image_data['type'] != 'others'):
            mirror = get_byte_mirror(image_data['cord'])
            filename = SCREENSHOT_PATH + '/Dataset/' + str(image_data['type']) + '/' + str(uuid4()).replace("-","") + ".png"
            if (os.path.exists(SCREENSHOT_PATH + '/Dataset')):
                with open(filename,'wb') as f:
                    f.write(base64.b64decode(mirror))
                flag = True
            else:
                log.error( "Dataset folder not found." )
                logger.print_on_console( "Dataset folder not found." )
            del mirror, filename # deleting variables
        else:
            """When the selected type is others"""
            flag = True
    except Exception as e:
        log.error("Error occurred in update_dataset, Err_Msg : ",e)
        logger.print_on_console("Error while updating dataset.")
    del image_data # deleting variables
    return flag

def get_byte_mirror(element_cord):
    """
    Def : Returns image from the coded mirror image
    Input : element['cord'](mirror of image)
    Output : decoded image
    Method Referenced in : gettextiris, getrowcountiris, getcolcountiris, getcellvalueiris, verifytextiris, gotoobject
    """
    img = None
    byte_mirror = None
    try:
        """ This check is done for IRIS 1.0 elements """
        if type(element_cord) == str and element_cord[0:2] != "b'":
            byte_mirror = base64.b64encode(codecs.encode(str(codecs.encode(element_cord))))
        else:
            byte_mirror = base64.b64encode(codecs.encode(element_cord))
        """Converting to a mirror image"""
        b64 = base64.b64decode(byte_mirror)
        img = b64[2:len(b64) - 1]
    except Exception as e:
        log.error("Error occurred in get_byte_mirror, Err_Msg : ", e)
        logger.print_on_console("Error occurred while fetching byte mirror")
    del byte_mirror, b64
    return img

class IRISKeywords():
    def __init__(self):
        self.dragIrisPos = {'x':'','y':''}
        self.dragIrisFlag = False
        global relativeCoordinates
        global verifyFlag
        global dropIrisFlag
        relativeCoordinates = []
        verifyFlag = False
        dropIrisFlag = False

    def clickiris(self,element,*args):
        """
        Discription: Performs a click operation on the IRIS object, if VerifyExistIRIS is provided then uses that(IRIS object) as a parent reference, then finds the element to perform action.
        Input: N/A
        OutPut: Boolean Value
        """
        log.info('Inside clickiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        width = None
        height = None
        try:
            img = None
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : ' + str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
                log.info( "Element co-ordinates after finding relative image are : " + str(res) )
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
            if( len(res) > 0 ):
                if SYSTEM_OS != 'Darwin': pythoncom.CoInitialize()
                log.info('Performing clickiris')
                pyautogui.click()
                log.info('clickiris performed')
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                err_msg = "Object not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in clickiris, Err_Msg : " + str(e)
            log.error(err_msg)
            logger.print_on_console("Error occurred in clickiris")
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status,result,value,err_msg

    def doubleclickiris(self,element,*args):
        """
        Discription: Performs a double-click operation on the IRIS object, if VerifyExistIRIS is provided then uses that(IRIS object) as a parent reference, then finds the element to perform action.
        Input: N/A
        OutPut: Boolean Value
        """
        log.info('Inside doubleclickiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements =[]
        width = None
        height = None
        try:
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : ' + str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
            if(len(res)>0):
                if SYSTEM_OS != 'Darwin': pythoncom.CoInitialize()
                log.info('Performing doubleClick')
                pyautogui.doubleClick()
                log.info('doubleClick performed')
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                logger.print_on_console("Object not found")
        except Exception as e:
            log.error("Error occurred in doubleclickiris, Err_Msg :",e)
            logger.print_on_console("Error occurred in doubleclickiris")
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status,result,value,err_msg

    def rightclickiris(self,element,*args):
        """
        Discription: Performs a right-click operation on the IRIS object, if VerifyExistIRIS is provided then uses that(IRIS object) as a parent reference, then finds the element to perform action.
        Input: N/A
        OutPut: Boolean Value
        """
        log.info('Inside rightclickiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements =[]
        width = None
        height = None
        try:
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : ' + str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
            if(len(res)>0):
                if SYSTEM_OS != 'Darwin': pythoncom.CoInitialize()
                log.info('Performing rightClick')
                pyautogui.rightClick()
                log.info('rightClick performed')
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                err_msg = "Object not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in rightclickiris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in rightclickiris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status, result, value, err_msg

    def settextiris(self,element,*args):
        """
        Discription: Performs a set text operation(keyboard type) on the IRIS object, if VerifyExistIRIS is provided then uses that(IRIS object) as a parent reference, then finds the element to perform action.
        Input: Input Text
        OutPut: Boolean Value
        """
        log.info('Inside settextiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements =[]
        width = None
        height = None
        try:
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : ' + str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
            if(len(res)>0):
                if SYSTEM_OS != 'Darwin':
                    pythoncom.CoInitialize()
                    pyautogui.click()
                    robot = Robot()
                    time.sleep(1)
                    robot.type_string(args[0][0], delay=0.2)
                else:
                    pyautogui.click()
                    time.sleep(1)
                    pyautogui.typewrite(args[0][0]) ## Pending
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                err_msg = "Object not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in SetTextIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in SetTextIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status, result, value, err_msg

    def cleartextiris(self,element,*args):
        """
        Discription: Performs a clear text operation(keyboard-backspace) on the IRIS object, if VerifyExistIRIS is provided then uses that(IRIS object) as a parent reference, then finds the element to perform action.
        Input: Options: a. N/A or 0 - Clearing text by default method: Click element + "Ctrl+A" + Backspace
                        b. 1 - 'Clearing text by method : Double click element + Backspace'
                        c. 2 - 'Clearing text by method : Click element + Home + "Shift+End" + Backspace'
                        d. 3 - 'Clearing text by method : Click element + End + "Shift+Home" + Backspace'
        OutPut: Boolean Value
        """
        log.info('Inside cleartextiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements =[]
        width = None
        height = None
        flag = False
        try:
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : ' + str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
            if(len(res) > 0):
                pythoncom.CoInitialize()
                if (args[0][0] == None or args[0][0] == '' or args[0][0] == str(0)):
                    log.debug( 'Clearing text by default method: Click element + "Ctrl+A" + Backspace' )
                    pyautogui.click()
                    pyautogui.hotkey('ctrl','a')
                    time.sleep(0.25)
                    pyautogui.press('backspace')
                    flag = True
                elif(args[0][0] == str(1) ):
                    log.debug( 'Clearing text by method : Double click element + Backspace' )
                    pyautogui.doubleClick()
                    time.sleep(0.25)
                    pyautogui.press('backspace')
                    flag = True
                elif(args[0][0] == str(2) ):
                    log.debug( 'Clearing text by method : Click element + Home + "Shift+End" + Backspace' )
                    pyautogui.click()
                    pyautogui.press('home')
                    time.sleep(0.25)
                    pyautogui.hotkey('shift','end')
                    time.sleep(0.25)
                    pyautogui.press('backspace')
                    flag = True
                elif(args[0][0] == str(3) ):
                    log.debug( 'Clearing text by method : Click element + End + "Shift+Home" + Backspace' )
                    pyautogui.click()
                    pyautogui.press('end')
                    time.sleep(0.25)
                    pyautogui.hotkey('shift','home')
                    time.sleep(0.25)
                    pyautogui.press('backspace')
                    flag = True
                else:
                    flag = False
                    err_msg = 'Invalid option'
                    log.error('Available Options : N/A or 0 - Clearing text by default method: Click element + "Ctrl+A" + Backspace, 1 - Clearing text by method : Double click element + Backspace, 2 - Clearing text by method : Click element + Home + "Shift+End" + Backspace, 3 - Clearing text by method : Click element + End + "Shift+Home" + Backspace')
                if (flag):
                    status= TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
            else:
                err_msg = "Object not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in ClearTextIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in ClearTextIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status, result, value, err_msg

    def setsecuretextiris(self,element,*args):
        """
        Discription: Performs a set secure text operation(inputs a AES encrypted text) on the IRIS object, if VerifyExistIRIS is provided then uses that(IRIS object) as a parent reference, then finds the element to perform action.
        Input: Encrypted Input Text (AES)
        OutPut: Boolean Value
        """
        log.info('Inside setsecuretextiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        width = None
        height = None
        try:
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : ' + str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
            if( len(res) > 0 ):
                encryption_obj = AESCipher()
                input_val_temp = encryption_obj.decrypt( args[0][0] )
                if SYSTEM_OS != 'Darwin':
                    pythoncom.CoInitialize()
                    pyautogui.click()
                    time.sleep(1)
                    robot = Robot()
                    robot.type_string(input_val_temp, delay=0.2)
                else:
                    pyautogui.click()
                    time.sleep(1)
                    pyautogui.typewrite(input_val_temp) ## Pending
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                err_msg = "Object not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in SetTextIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in SetSecureTextIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status,result,value,err_msg

    def gettextiris(self,element,*args):
        """
        Discription: Performs a get text operation(fetches text of the image) on the IRIS object, if VerifyExistIRIS is provided then uses that(IRIS object) as a parent reference, then finds the element to perform action.
        Input: N/A - no input then performs a direct image to text operation(uses Tessaract - OCR).
               'selective'|| 'selective;right' || 'selective;left' - giving this value as input will result in selection of text via mouse-drag. By default drags mouse from left to right, but second option(right/left) can be given to indicate mouse-drag starting direction.
               'date' - giving this value will help in removing
        OutPut: Text (of IRIS object)
        """
        log.info('Inside gettextiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        height = None
        width = None
        #-----------
        image = None
        text = ''
        opt = None
        try:
            if(TESSERACT_PATH_EXISTS):
                #---------------------------------------------------------------taking Tessaract path for respective OS
                if SYSTEM_OS != 'Darwin':
                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                    os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                else:
                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/bin/tesseract'
                    os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/share/tessdata'
                #---------------------------------------------------------------taking Tessaract path for respective OS
                if(len(args) == 3 and args[2]!='' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if (res and img):
                    with open("cropped.png", "wb") as f:
                        f.write(base64.b64decode(img))
                    image = cv2.imread("cropped.png")
                    text = ''
                    if(len(args[0]) >= 1 and args[0][0].lower().strip() == 'select'):
                        if ( SYSTEM_OS != 'Darwin' ):
                            win32clipboard.OpenClipboard()
                            win32clipboard.EmptyClipboard()
                            win32clipboard.CloseClipboard()
                            height = int(element['coordinates'][3]) - int(element['coordinates'][1])
                            opt = None
                            if (len(args[0])==2 and args[0][1].lower().strip()=='left'):opt='left'
                            elif ((len(args[0])==2 and args[0][1].lower().strip()=='right') or len(args[0])==1):opt='right'
                            if (opt):
                                def heightDiff(height,opt):
                                    h1 = h2 = None
                                    if (opt == 'right'):
                                        h1 = -int(height/2)
                                        h2 = int(height/2)
                                    else:
                                        h1 = int(height/2)
                                        h2 = -int(height/2)
                                    del opt, height # deleting variables
                                    return h1, h2
                                def getFromClipboard(flag):
                                    text = None
                                    robot = Robot()
                                    robot.ctrl_press('c')
                                    time.sleep(1)
                                    win32clipboard.OpenClipboard()
                                    try:
                                        text = win32clipboard.GetClipboardData()
                                        text = text.replace('\x00','') if text else None
                                    except : flag = False
                                    win32clipboard.CloseClipboard()
                                    del robot # deleting variables
                                    return text, flag
                                def dragFunctionA(c1, c2, c3, c4, h, opt):
                                    log.debug('Entering dragFunctionA ')
                                    text = None
                                    flag = True
                                    h1, h2 = heightDiff(h, opt)
                                    pyautogui.moveTo( c1, c2 + h1 )
                                    pyautogui.dragTo( c3, c4 + h2 , button = 'left')
                                    text, flag = getFromClipboard(flag)
                                    if not(text and flag):
                                        text,flag = dragFunctionB( c1, c2, c3, c4, h, opt )
                                    del c1, c2, c3, c4, opt, h, h1, h2 # deleting variables
                                    return text, flag
                                def dragFunctionB(c1, c2, c3, c4, h, opt):
                                    log.debug('Entering dragFunctionB ,dragFunctionA did not work')
                                    text = None
                                    flag = True
                                    h1, h2 = heightDiff(h, opt)
                                    pyautogui.moveTo( c1, c2 + h1 )
                                    pyautogui.drag( c3, c4 + h2 , button = 'left')
                                    text, flag = getFromClipboard(flag)
                                    if not(text and flag):
                                        text,flag = dragFunctionC( c1, c2, c3, c4, h, opt )
                                    del c1, c2, c3, c4, opt, h, h1, h2 # deleting variables
                                    return text, flag
                                def dragFunctionC(c1, c2, c3, c4, h, opt):
                                    log.debug('Entering dragFunctionC ,dragFunctionB did not work')
                                    text = None
                                    flag = True
                                    h1, h2 = heightDiff(h, opt)
                                    pywinauto.mouse.press(button = 'left', coords=(c1, c2 + h1))
                                    pywinauto.mouse.release(button = 'left', coords=(c3, c4 + h2))
                                    text, flag = getFromClipboard(flag)
                                    del c1, c2, c3, c4, opt, h, h1, h2 # deleting variables
                                    return text, flag
                                if ( opt =='left' ):#L-R
                                    text, flag = dragFunctionA(int(element['coordinates'][0]),int(element['coordinates'][1]),int(element['coordinates'][2]),int(element['coordinates'][3]) ,height ,opt)
                                elif (opt == 'right' ): #R-L
                                    text, flag = dragFunctionA(int(element['coordinates'][2]),int(element['coordinates'][3]),int(element['coordinates'][0]),int(element['coordinates'][1]) ,height ,opt)
                                if not(text and flag):
                                    err_msg = "Unable to select the text"
                            else:
                                err_msg = "Error : Invalid option"
                    elif( len(args[0])==1 and args[0][0].lower().strip() == 'date' ):
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
                    if not( err_msg ):
                        status= TEST_RESULT_PASS
                        result = TEST_RESULT_TRUE
                        value = text
                    os.remove('cropped.png')
                else:
                   err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found."
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in GetTextIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in GetTextIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width, image, text, opt # deleting variables
        return status, result, value, err_msg

#--------------------------------------------------------------------------------------------------------------------------------- iris table keywords
    def getrowcountiris(self,element,*args):
        """
        Discription: This function returns total row count of the IRIS image(uses hough transform to get cells of the table)
        Input: N/A
        OutPut: Row count
        """
        log.info('Inside getrowcountiris and No. of arguments passed are : '+str(len(args)))
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements =[]
        height = None
        width = None
        try:
            img = None
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : '+str(res) )
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
                if(res): img = get_byte_mirror(element['cord'])
            if( res and img ):
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
                if(len(horizontal)>0):
                    value = len(horizontal)-1
                else:
                    value = 0
                    logger.print_on_console('Unable to detect rows')
                os.remove('cropped.png')
                os.remove('rotated.png')
            else:
                err_msg = "Element not found on screen."
        except Exception as e:
            log.error("Error occurred in GetRowCountIris, Err_Msg : ",e)
            logger.print_on_console("Error occurred in GetRowCountIris")
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status,result,value,err_msg

    def getcolcountiris(self,element,*args):
        """
        Discription: This function returns total column count of the IRIS image(uses hough transform to get cells of the table)
        Input:N/A
        OutPut: Column count
        """
        log.info('Inside getcolcountiris and No. of arguments passed are : '+str(len(args)))
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        rotated = None
        height = None
        width = None
        try:
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : '+str(res) )
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
                if(res): img = get_byte_mirror(element['cord'])
            if( res and img ):
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
                if(len(vertical)>0):
                    value = len(vertical)-1
                else:
                    value = 0
                    logger.print_on_console('Unable to detect columns')
                os.remove('cropped.png')
                os.remove('rotated.png')
            else:
                err_msg = "Element not found on screen."
        except Exception as e:
            err_msg = "Error occurred in GetColCountIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in GetColCountIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, rotated, height, width # deleting variables
        return status, result, value, err_msg

    def getcellvalueiris(self,element,*args):
        """
        Discription: This function returns the cell text/value of the IRIS image(uses hough transform to get cells of the table)
        Input: Row, Column
        OutPut: Cell Text/Value
        """
        log.info( 'Inside getcellvalueiris and No. of arguments passed are : ' + str(len(args)) )
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        row = int(args[0][0])
        col = int(args[0][1])
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        height = None
        width = None
        try:
            self.getrowcountiris(element)
            if( TESSERACT_PATH_EXISTS ):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if( len(args) == 3 and args[2] != '' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if( res and img ):
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
                    err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in GetCellValueIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in GetCellValueIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, row, col, width, height # deleting variables
        return status,result,value,err_msg

    def setcellvalueiris(self,element,*args):
        """
        Discription: This function will set the cell text/value of the IRIS image(uses hough transform to get cells of the table)
        Input: Row, Column, Text
        OutPut: Boolean
        """
        log.info( 'Inside setcellvalueiris and No. of arguments passed are : ' + str(len(args)) )
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        row = int(args[0][0])
        col = int(args[0][1])
        text = args[0][2]
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        height = None
        width = None
        try:
            self.getrowcountiris(element)
            if( TESSERACT_PATH_EXISTS ):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if( len(args) == 3 and args[2] != '' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    width = res[2] - res[0]
                    height = res[3] - res[1]
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if( res and img ):
                    with open("cropped.png", "wb") as f:
                        f.write(base64.b64decode(img))
                    img = cv2.imread("cropped.png")
                    X,Y = get_cell_position(img,row,col)
                    #--------------------------------------------------------equal in distance
                    try:
                        if(args[0][3] == str(1)):
                            rows = len(horizontal)-1
                            height_ele = height/rows
                            Y = (height_ele*(row-1)) + (height_ele/2)
                    except:pass
                    #--------------------------------------------------------equal in distance
                    pyautogui.moveTo(res[0]+ int(X), res[1]+ int(Y))
                    if(text):
                        if SYSTEM_OS != 'Darwin':
                            pythoncom.CoInitialize()
                            pyautogui.click()
                            robot = Robot()
                            time.sleep(1)
                            robot.type_string(text, delay=0.2)
                        else:
                            pyautogui.click()
                            time.sleep(1)
                            pyautogui.typewrite(text) ## Pending
                        status  = TEST_RESULT_PASS
                        result = TEST_RESULT_TRUE
                    else:
                        err_msg = "Input text missing"
                    os.remove('cropped.png')
                else:
                    err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in SetCellValueIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in SetCellValueIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, row, col, width, height # deleting variables
        return status,result,value,err_msg

    def verifycellvalueiris(self,element,*args):
        """
        Discription: This function returns verifies cell text/value of the IRIS image(uses hough transform to get cells of the table)
        Input: Row, Column ,Text
        OutPut: Cell Text/Value
        """
        log.info( 'Inside verifycellvalueiris and No. of arguments passed are : ' + str(len(args)) )
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        row = int(args[0][0])
        col = int(args[0][1])
        inptext = args[0][2]
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        height = None
        width = None
        try:
            self.getrowcountiris(element)
            if( TESSERACT_PATH_EXISTS ):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if( len(args) == 3 and args[2] != '' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if( res and img ):
                    with open("cropped.png", "wb") as f:
                        f.write(base64.b64decode(img))
                    img = cv2.imread("cropped.png")
                    text = data_in_cells(img,row,col)
                    if (inptext):
                        if(text == inptext):
                            status  = TEST_RESULT_PASS
                            result = TEST_RESULT_TRUE
                    else:
                        err_msg = "Input text missing"
                    os.remove('cropped.png')
                else:
                    err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in VerifyCellValueIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in VerifyCellValueIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, row, col, width, height # deleting variables
        return status,result,value,err_msg

    def clickcelliris(self,element,*args):
        """
        Discription: This function will click the cell of the IRIS image(uses hough transform to get cells of the table)
        Input: Row, Column
        OutPut: Boolean
        """
        log.info( 'Inside clickcelliris and No. of arguments passed are : ' + str(len(args)) )
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        row = int(args[0][0])
        col = int(args[0][1])
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        height = None
        width = None
        try:
            self.getrowcountiris(element)
            if( TESSERACT_PATH_EXISTS ):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if( len(args) == 3 and args[2] != '' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    width = res[2] - res[0]
                    height = res[3] - res[1]
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if( res and img ):
                    with open("cropped.png", "wb") as f:
                        f.write(base64.b64decode(img))
                    img = cv2.imread("cropped.png")
                    X, Y = get_cell_position(img,row,col)
                    #--------------------------------------------------------equal in distance
                    try:
                        if(args[0][2] == str(1)):
                            rows = len(horizontal)-1
                            height_ele = height/rows
                            Y = (height_ele*(row-1)) + (height_ele/2)
                    except:pass
                    #--------------------------------------------------------equal in distance
                    pyautogui.moveTo(res[0]+ int(X), res[1]+ int(Y))
                    if SYSTEM_OS != 'Darwin': pythoncom.CoInitialize()
                    log.info('Performing clickcelliris')
                    pyautogui.click()
                    log.info('clickcelliris performed')
                    status  = TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                    os.remove('cropped.png')
                else:
                    err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in ClickCellIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in ClickCellIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, row, col, width, height # deleting variables
        return status,result,value,err_msg

    def doubleclickcelliris(self,element,*args):
        """
        Discription: This function will double click the cell of the IRIS image(uses hough transform to get cells of the table)
        Input: Row, Column
        OutPut: Boolean
        """
        log.info( 'Inside doubleclickcelliris and No. of arguments passed are : ' + str(len(args)) )
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        row = int(args[0][0])
        col = int(args[0][1])
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        height = None
        width = None
        try:
            self.getrowcountiris(element)
            if( TESSERACT_PATH_EXISTS ):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if( len(args) == 3 and args[2] != '' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    width = res[2] - res[0]
                    height = res[3] - res[1]
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if( res and img ):
                    with open("cropped.png", "wb") as f:
                        f.write(base64.b64decode(img))
                    img = cv2.imread("cropped.png")
                    X, Y = get_cell_position(img,row,col)
                    #--------------------------------------------------------equal in distance
                    try:
                        if(args[0][2] == str(1)):
                            rows = len(horizontal)-1
                            height_ele = height/rows
                            Y = (height_ele*(row-1)) + (height_ele/2)
                    except:pass
                    #--------------------------------------------------------equal in distance
                    pyautogui.moveTo(res[0]+ int(X), res[1]+ int(Y))
                    if SYSTEM_OS != 'Darwin': pythoncom.CoInitialize()
                    log.info('Performing doubleClickCell')
                    pyautogui.doubleClick()
                    log.info('doubleClickCell performed')
                    status  = TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                    os.remove('cropped.png')
                else:
                    err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in DoubleClickCellIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in DoubleClickCellIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, row, col, width, height # deleting variables
        return status,result,value,err_msg

    def rightclickcelliris(self,element,*args):
        """
        Discription: This function will right click the cell of the IRIS image(uses hough transform to get cells of the table)
        Input: Row, Column
        OutPut: Boolean
        """
        log.info( 'Inside rightclickcelliris and No. of arguments passed are : ' + str(len(args)) )
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        row = int(args[0][0])
        col = int(args[0][1])
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        height = None
        width = None
        try:
            self.getrowcountiris(element)
            if( TESSERACT_PATH_EXISTS ):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if( len(args) == 3 and args[2] != '' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    width = res[2] - res[0]
                    height = res[3] - res[1]
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if( res and img ):
                    with open("cropped.png", "wb") as f:
                        f.write(base64.b64decode(img))
                    img = cv2.imread("cropped.png")
                    X, Y = get_cell_position(img,row,col)
                    #--------------------------------------------------------equal in distance
                    try:
                        if(args[0][2] == str(1)):
                            rows = len(horizontal)-1
                            height_ele = height/rows
                            Y = (height_ele*(row-1)) + (height_ele/2)
                    except:pass
                    #--------------------------------------------------------equal in distance
                    pyautogui.moveTo(res[0]+ int(X), res[1]+ int(Y))
                    if SYSTEM_OS != 'Darwin': pythoncom.CoInitialize()
                    log.info('Performing rightClickCell')
                    pyautogui.rightClick()
                    log.info('rightClickCell performed')
                    status  = TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                    os.remove('cropped.png')
                else:
                    err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in RightClickCellIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in RightClickCellIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, row, col, width, height # deleting variables
        return status,result,value,err_msg

    def mousehovercelliris(self,element,*args):
        """
        Discription: This function will right click the cell of the IRIS image(uses hough transform to get cells of the table)
        Input: Row, Column
        OutPut: Boolean
        """
        log.info( 'Inside mousehovercelliris and No. of arguments passed are : ' + str(len(args)) )
        global horizontal,vertical
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        row = int(args[0][0])
        col = int(args[0][1])
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        height = None
        width = None
        try:
            self.getrowcountiris(element)
            if( TESSERACT_PATH_EXISTS ):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                img = None
                if( len(args) == 3 and args[2] != '' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    width = res[2] - res[0]
                    height = res[3] - res[1]
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if( res and img ):
                    with open("cropped.png", "wb") as f:
                        f.write(base64.b64decode(img))
                    img = cv2.imread("cropped.png")
                    X, Y = get_cell_position(img,row,col)
                    #--------------------------------------------------------equal in distance
                    try:
                        if(args[0][2] == str(1)):
                            rows = len(horizontal)-1
                            height_ele = height/rows
                            Y = (height_ele*(row-1)) + (height_ele/2)
                    except:pass
                    #--------------------------------------------------------equal in distance
                    if SYSTEM_OS != 'Darwin': pythoncom.CoInitialize()
                    log.info('Performing mouseHoverCell')
                    pyautogui.moveTo(res[0]+ int(X), res[1]+ int(Y))
                    log.info('mouseHoverCell performed')
                    status  = TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                    os.remove('cropped.png')
                else:
                    err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in MouseHoverCellIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in MouseHoverCellIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, row, col, width, height # deleting variables
        return status,result,value,err_msg
#--------------------------------------------------------------------------------------------------------------------------------- iris table keywords

    def verifyexistsiris(self,element,*args):
        """
        Discription: Verifies if image is present on DOM. This image will be set as a parent element , if scraped image is a 'const' type
        Input: N/A
        OutPut: Boolean Value
        """
        log.info('Inside verifyexistsiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        width = None
        height = None
        try:
            global relativeCoordinates
            global verifyFlag
            if( len(args) == 3 and args[2] != '' and args[2] !='constant' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : '+str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
            if( len(res) > 0 ):
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
                if( len(args) == 3 and args[2] == 'constant' ):
                    relativeCoordinates = res
                    verifyFlag = True
                    logger.print_on_console('Element exists and identified as constant')
                    log.info('verifyFlag set to True, Parent element recognised - all iris objects will be treated as relative IRIS elements.')
                else:
                    logger.print_on_console('Element exists.')
            else:
                err_msg = "Object not found."
                verifyFlag = False
                log.info('verifyFlag set to False, Parent element unrecognised - all iris objects will be treated as regular IRIS elements.')
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            verifyFlag = False
            log.info('verifyFlag set to Flase, Parent element unrecognised - all iris objects will be treated as regular IRIS elements.')
            err_msg = "Error occurred in VerifyExistsIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in VerifyExistsIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status, result, value, err_msg

    def verifytextiris(self,element,*args):
        """
        Discription: Verifyies the input text with the text of the image.
        Input: Input Text
        Output: list of [input text,text]
        """
        log.info('Inside verifytextiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = [args[0][0],'null']
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        image = None
        text = ''
        verifytext = args[0][0]
        height = None
        width = None
        try:
            if( TESSERACT_PATH_EXISTS ):
                pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                if(len(args) == 3 and args[2]!='' and verifyFlag ):
                    log.info('IRIS element recognised as a relative element')
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    log.info( 'Relative image co-ordinates : '+str(res) )
                else:
                    log.info('IRIS element recognised as a non-relative element')
                    res, width, height = gotoobject(element)
                    if(res): img = get_byte_mirror(element['cord'])
                if( res and img ):
                    with open("cropped.png", "wb") as f:
                        f.write(base64.b64decode(img))
                    image = cv2.imread("cropped.png")
                    text = get_ocr(image)
                    if(verifytext == text):
                        status= TEST_RESULT_PASS
                        result = TEST_RESULT_TRUE
                    else:
                        err_msg = "Values do not match"
                        logger.print_on_console("Expected value is:", verifytext)
                        logger.print_on_console("Actual value is:", text)
                    value = [verifytext,text]
                    os.remove('cropped.png')
                else:
                    err_msg = "Element not found on screen."
            else:
                err_msg = "Tesseract module not found."
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in VerifyTextIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in VerifyTextIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, text, verifytext, image, height, width # deleting variables
        return status, result, value, err_msg

    def dragiris(self,element,*args):
        """
        Discription: Set mouse position to the center of the scraped element and hold that element
        Input: N/A
        Output: Boolean Value
        """
        log.info('Inside dragIris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        width = None
        height = None
        img = None
        try:
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                width = res[2] - res[0]
                height = res[3] - res[1]
                log.info('Moving the mouse cursor to the element that needs to be dragged')
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
                self.dragIrisPos['x'] = res[0] + int(width/2)
                self.dragIrisPos['y'] = res[1] + int(height/2)
                log.info('Moved the mouse cursor to the element that needs to be dragged')
                log.info( 'Relative image co-ordinates : ' + str(res) )
            else:
                res, width, height = gotoobject(element)
                self.dragIrisPos['x'] = res[0] + int(width/2)
                self.dragIrisPos['y'] = res[0] + int(height/2)
                log.info( 'Image co-ordinates : ' + str(res) )
            if( len(res) > 0 ):
                self.dragIrisFlag = True
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                err_msg = "Object not found"
                self.dragIrisFlag = False
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            self.dragIrisFlag = False
            err_msg = "Error occurred in dragIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in dragIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status, result, value, err_msg

    def dropiris(self,element,*args):
        """
        Discription: Drop the dragiris-element to the target element described in dropiris
        Input: N/A
        Output: Boolean Value
        """
        log.info('Inside dropIris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        width = None
        height = None
        img = None
        try:
            global dropIrisFlag
            if ( self.dragIrisFlag ):
                #check if co-ordinates are on the drag-element if True ignor , if False then move mouse cursor to drag-element
                x, y = pyautogui.position()
                if( self.dragIrisPos['x'] != x and self.dragIrisPos['y'] != y ): pyautogui.moveTo(self.dragIrisPos['x'], self.dragIrisPos['y'])

                if(len(args) == 3 and args[2]!='' and verifyFlag ):
                    elem_coordinates = element['coordinates']
                    const_coordintes = args[2]['coordinates']
                    elements = [(const_coordintes[0],const_coordintes[1]),
                            (const_coordintes[2],const_coordintes[3]),
                            (elem_coordinates[0], elem_coordinates[1]),
                            (elem_coordinates[2], elem_coordinates[3])]
                    img, res = find_relative_image(elements, relativeCoordinates)
                    log.info( 'Relative image co-ordinates : ' + str(res) )
                    width = res[2] - res[0]
                    height = res[3] - res[1]
                else:
                    dropIrisFlag = True
                    res, width, height = gotoobject(element)
                    dropIrisFlag = False
                    log.info( 'Image co-ordinates : ' + str(res) )
                if( len(res) > 0 ):
                    log.info('Dragging the element to drop location')
                    pyautogui.dragTo(res[0]+ int(width/2),res[1] + int(height/2),1,button='left') #dragTo(X,Y,time in seconds to drag over,left/right click)
                    log.info('Dragged the element to drop location')
                    status= TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                else:
                    err_msg = "Object not found"
            else:
                err_msg = "Error: dragIris is not selected, cannot drag item"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in dropIris, Err_Msg : " + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in dropIris" )
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status, result, value, err_msg

    def mousehoveriris(self,element,*args):
        """
        Discription: Performs a mousehover operation on the element.
        Input: N/A
        OutPut: Boolean Value
        """
        log.info('Inside mousehoveriris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        width = None
        height = None
        try:
            img = None
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : ' + str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
                log.info( "Element co-ordinates after finding relative image are : " + str(res) )
            else:
                log.info('IRIS element recognised as a non-relative element')
                res, width, height = gotoobject(element)
            if( len(res) > 0 ):
                status= TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
            else:
                err_msg = "Object not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in mousehoveriris, Err_Msg : " + str(e)
            log.error(err_msg)
            logger.print_on_console("Error occurred in MouseHoverIris")
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width # deleting variables
        return status, result, value, err_msg

    def getstatusiris(self,element,*args):
        """
        Discription: Performs a get status operation on the checkbox element.
        Input: N/A
        OutPut: Boolean Value
        """
        log.info('Inside getstatusiris and No. of arguments passed are : '+str(len(args)))
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        img = None
        res = None
        elem_coordinates = None
        const_coordintes = None
        elements = []
        width = None
        height = None
        try:
            img = None
            if(len(args) == 3 and args[2]!='' and verifyFlag ):
                log.info('IRIS element recognised as a relative element')
                elem_coordinates = element['coordinates']
                const_coordintes = args[2]['coordinates']
                elements = [(const_coordintes[0],const_coordintes[1]),
                        (const_coordintes[2],const_coordintes[3]),
                        (elem_coordinates[0], elem_coordinates[1]),
                        (elem_coordinates[2], elem_coordinates[3])]
                img, res = find_relative_image(elements, relativeCoordinates)
                log.info( 'Relative image co-ordinates : ' + str(res) )
                width = res[2] - res[0]
                height = res[3] - res[1]
                pyautogui.moveTo(res[0]+ int(width/2),res[1] + int(height/2))
                log.info( "Element co-ordinates after finding relative image are : " + str(res) )
            else:
                log.info('IRIS element recognised as a non-relative element')
                logger.print_on_console("Warning!: Parent element not detected, will lead to inconsistant results")
                res, width, height = gotoobject(element)
                if(res): img = get_byte_mirror(element['cord'])
            if( len(res) > 0 ):
                #1.get original image
                originalImg = get_byte_mirror(element['cord'])
                with open("original.png", "wb") as f:
                    f.write(base64.b64decode(originalImg))
                originalImage = cv2.imread("original.png")

                #2. get target image
                with open("compare.png", "wb") as f:
                    f.write(base64.b64decode(img))
                relativeImage = cv2.imread("compare.png")

                #3. subtract target image with the original image
                flg = False
                matchFlag = image_match(originalImage,relativeImage)
                if (args[0][0] == str(0)):
                    #unchecked
                    if matchFlag: val = 'unchecked'
                    else: val = 'checked'
                    flg = True
                elif(args[0][0] == str(1)):
                    #checked
                    if matchFlag: val = 'checked'
                    else: val = 'unchecked'
                    flg = True
                else:
                    flg = False
                if (flg == True):
                    status= TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                    value = val
                else:
                    err_msg ="Invalid input"
                os.remove('original.png')
                os.remove('compare.png')
            else:
                err_msg = "Object not found"
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = "Error occurred in getstatusiris, Err_Msg : " + str(e)
            log.error(err_msg)
            logger.print_on_console("Error occurred in getStatusIris")
        del element, args, img, res, elem_coordinates, const_coordintes, elements, height, width, originalImage, relativeImage, matchFlag, flg # deleting variables
        return status, result, value, err_msg