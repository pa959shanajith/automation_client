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
##from skimage.measure import compare_ssim as ssim
##import matplotlib.pyplot as plt
import numpy as np
##import cv2
from PIL import Image
import urllib
import os


log = logging.getLogger('util_operations.py')

class VerifyFileImages:

    # Function to do Image Comparison. It prints percentage similarity between the images
    def imagecomparison(self,source,target):
        # Open source & target image as np array

        sarray = np.asarray(source)
        tarray = np.asarray(target)

        """# Print the value of MSE and SSIM
        print 'Mean Square Error (MSE): ', mse(s, t)
        print 'Structural Similarity Index (SSIM): ', ssim(s, t)"""

        percentage_mse = 100 - (self.mse(sarray,tarray) / 600)


        if percentage_mse >= 60:
            return 1
        else:
            return 0



##    # Function to do Image Comparison. It prints percentage similarity between the images
##    def imagecomparison(self,source,target):
##        # Open source & target image as np array
##        source = Image.open(source)
##        sarray = np.asarray(source)
##
##        target = Image.open(target)
##        tarray = np.asarray(target)
##
##        # Resize the images to 1024 * 768
##        s = cv2.resize(sarray, (1024,768))
##        t = cv2.resize(tarray, (1024,768))
##
##        # Convert images to Gray color
##        s = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
##        t = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
##
##        """# Print the value of MSE and SSIM
##        print 'Mean Square Error (MSE): ', mse(s, t)
##        print 'Structural Similarity Index (SSIM): ', ssim(s, t)"""
##
##        percentage_mse = 100 - (self.mse(s,t) / 600)
##        percentage_ssim = 100 * ssim(s,t)
##
##        percentage_similarity = (percentage_mse + percentage_ssim) / 2
##
##        if percentage_similarity >= 60:
##            return 1
##        else:
##            return 0

    # Defining Fuction for Mean Square Error MSE
    def mse(self,imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err


