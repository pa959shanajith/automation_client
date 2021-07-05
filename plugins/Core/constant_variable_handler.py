#-------------------------------------------------------------------------------
# Name:        constant_variable_handler
# Purpose:
#
# Author:      sathwik.p
#
# Created:     05-07-2021
# Copyright:   (c) sathwik.p 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
from collections import OrderedDict
from constants import *
import re
import core_utils
import logging
import ast
import math
import threading
import json
import controller
local_constant = threading.local()

class ConstantVariables:
    def __init__(self):
        local_constant.constant_variable_map=OrderedDict()
        local_constant.log = logging.getLogger('constant_variable_handler.py')

    #To Check if the given pattern of the variable matches '_a_'
    def check_for_constantvariables(self,outputval,keyword=None,store_val=False):
        #checks whether the given variable is constant or not
        status = TEST_RESULT_FALSE
        if outputval != None and outputval != '':
            if '_' in outputval and '_' in outputval:
                var_list=re.findall(r"\_(.*?)\_",outputval)
                if len(var_list)>0:
                    status = TEST_RESULT_TRUE
        return status

    #To get the value of given constant variable
    def get_constant_value(self,variable):
        #returns the value of the constant variable if it exists otherwise returns None

        value=None
        if variable in local_constant.constant_variable_map:
            value=local_constant.constant_variable_map.get(variable)
        return value