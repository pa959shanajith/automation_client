#-------------------------------------------------------------------------------
# Name:        oebs_scrollbarops.py
# Purpose:     keywords in this script enables to perform action on text Objects.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



from oebs_msg import *
import oebs_key_objects
import oebs_serverUtilities
import logging
import oebs_mouseops
import time


class ScrollbarOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()

    def right(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_SCROLLBAR,DEF_RIGHT)
            objstates = charinfo.states
            x1_cor = charinfo.x
            y1_cor = charinfo.y
            width = charinfo.width
            height = charinfo.height
            x2_cor = x1_cor+width
            y2_cor = y1_cor+height
            numofoperation = int(oebs_key_objects.keyword_input[0])
            if 'enabled' in objstates:
                    if(numofoperation > 0):
                        for i in range(numofoperation):
                            if(width>height):
                                x_cor = ((x2_cor-height)+x2_cor)/2
                                y_cor = (y1_cor+y2_cor)/2
                                oebs_mouseops.MouseOperation('click',x_cor,y_cor)
                                verifyresponse = MSG_TRUE
                                keywordresult=MSG_PASS

                    else:
                        logging.debug('FILE: %s , DEF: %s MSG: Invalid Input',OEBS_SCROLLBAR,DEF_DOWN,MSG_INVALID_INPUT)
                        oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")

            else:
                logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_SCROLLBAR,DEF_DOWN,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_SCROLLBAR,DEF_RIGHT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_SCROLLBAR,DEF_RIGHT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_SCROLLBAR,DEF_RIGHT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    def left(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_SCROLLBAR,DEF_LEFT)
            objstates = charinfo.states
            x1_cor = charinfo.x
            y1_cor = charinfo.y
            width = charinfo.width
            height = charinfo.height
            x2_cor = x1_cor+width
            y2_cor = y1_cor+height
            numofoperation = int(oebs_key_objects.keyword_input[0])
            if 'enabled' in objstates:
                    if(numofoperation > 0):
                        for i in range(numofoperation):
                            if(width>height):
                                x_cor = ((x1_cor+height)+x1_cor)/2
                                y_cor = (y1_cor+y2_cor)/2
                                oebs_mouseops.MouseOperation('click',x_cor,y_cor)
                                verifyresponse = MSG_TRUE
                                keywordresult=MSG_PASS

                    else:
                        logging.debug('FILE: %s , DEF: %s MSG: Invalid Input',OEBS_SCROLLBAR,DEF_DOWN,MSG_INVALID_INPUT)
                        oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")

            else:
                logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_SCROLLBAR,DEF_DOWN,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_SCROLLBAR,DEF_LEFT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_SCROLLBAR,DEF_LEFT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_SCROLLBAR,DEF_LEFT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    def up(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_SCROLLBAR,DEF_UP)
            objstates = charinfo.states
            x1_cor = charinfo.x
            y1_cor = charinfo.y
            width = charinfo.width
            height = charinfo.height
            x2_cor = x1_cor+width
            y2_cor = y1_cor+height
            numofoperation = int(oebs_key_objects.keyword_input[0])
            if 'enabled' in objstates:
                    if(numofoperation > 0):
                        for i in range(numofoperation):
                            if(height>width):
                                x_cor = (x1_cor+x2_cor)/2
                                y_cor = (y1_cor+(y1_cor+width))/2
                                oebs_mouseops.MouseOperation('click',x_cor,y_cor)
                                verifyresponse = MSG_TRUE
                                keywordresult=MSG_PASS

                    else:
                        logging.debug('FILE: %s , DEF: %s MSG: Invalid Input',OEBS_SCROLLBAR,DEF_DOWN,MSG_INVALID_INPUT)
                        oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")

            else:
                logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_SCROLLBAR,DEF_DOWN,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_SCROLLBAR,DEF_UP,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_SCROLLBAR,DEF_UP,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_SCROLLBAR,DEF_UP,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    def down(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_SCROLLBAR,DEF_DOWN)
            objstates = charinfo.states
            x1_cor = charinfo.x
            y1_cor = charinfo.y
            width = charinfo.width
            height = charinfo.height
            x2_cor = x1_cor+width
            y2_cor = y1_cor+height
            numofoperation = int(oebs_key_objects.keyword_input[0])
            if 'enabled' in objstates:
                if(numofoperation > 0):
                    for i in range(numofoperation):
                        if(height>width):
                            x_cor = (x1_cor+x2_cor)/2
                            y_cor = (y2_cor+(y2_cor-width))/2
                            oebs_mouseops.MouseOperation('click',x_cor,y_cor)
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS

                else:
                    logging.debug('FILE: %s , DEF: %s MSG: Invalid Input',OEBS_SCROLLBAR,DEF_DOWN,MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")

            else:
                logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_SCROLLBAR,DEF_DOWN,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_SCROLLBAR,DEF_DOWN,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_SCROLLBAR,DEF_DOWN,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_SCROLLBAR,DEF_DOWN,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

