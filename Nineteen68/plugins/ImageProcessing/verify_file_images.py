#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      parampreet.singh
#
# Created:     02-06-2017
# Copyright:   (c) parampreet.singh 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import os
import logger

import logging

# Required for Image Comparison Task
#960 Imageverificaton: added histogram and ssim algorithm (Himanshu)
#import matplotlib.pyplot as plt

#All libraries required for ImageProcessing plugin will be at this location
path1 = os.environ["NINETEEN68_HOME"]
##sys.path.insert(0, path1+'\Lib\site-packages\ImageProcessingBundle')
sys.path.append(path1+"\\Nineteen68\\plugins\\ImageProcessing\\ImageProcessing")

import numpy as np
import cv2
from PIL import Image
import urllib
import os
#from skimage.measure import compare_ssim as ssim


log = logging.getLogger('util_operations.py')

def get_thumbnail(image, size=(128,128), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size); # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image

def image_similarity_histogram_via_pil(image1,image2):
    from PIL import Image
    import math
    import operator

    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)

    h1 = image1.histogram()
    h2 = image2.histogram()

    rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return rms


class VerifyFileImages:


#ssim algo instead of MSE for better performence(Himanshu)
      # Function to do Image Comparison. It prints percentage similarity between the images
    def imagecomparison(self,image_filepath1,image_filepath2):
        # Open source & target image as np array
        import ssim

        im1 = Image.open(image_filepath1)
        im2 = Image.open(image_filepath2)
        im1 = im1.convert('RGB')
        im2 = im2.convert('RGB')


        similarity2 = image_similarity_histogram_via_pil(im1,im2)


        similarity5 = ssim.compute_ssim(im1,im2)
        #Classification logic
        if(similarity2<10):
            return 1
        elif(similarity2<100 and similarity5>.50):
            return 1
        elif(similarity5>.70):
            return 1
        else:
            return 0