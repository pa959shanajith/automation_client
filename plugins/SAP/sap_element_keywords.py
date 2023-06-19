#-------------------------------------------------------------------------------
# Name:        SAP_Element_Keywords
# Purpose:      contains click and get element text
#
# Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     7-04-2017
# Copyright:   (c) anas.ahmed1 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pywinauto
import sap_constants
from sap_launch_keywords import Launch_Keywords
from constants import *
import logger
from saputil_operations import SapUtilKeywords
from sendfunction_keys import SendFunctionKeys
from sap_scontainer_keywords import SContainer_Keywords
import logging
log = logging.getLogger('sap_element_keywords.py')

class ElementKeywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()
        self.sc = SContainer_Keywords()

    def get_element_text(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                value = ses.FindById(id).text
                status = sap_constants.TEST_RESULT_PASS
                result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
                log.info(err_msg)
            #------------------------logging error messages
            if( err_msg ):
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Get Element Text" )
        return status, result, value, err_msg

    def verify_element_text(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( len(input_val) != 0 ):
                    if ( len(input_val) > 1 ):
                        input = input_val[3]
                    else:
                        input = input_val[0]

                    if ( ses.FindById(id).text == input ):
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                elif ( len(input_val) == 0 ):
                    err_msg = 'Entered text is empty'
                else:
                    err_msg = sap_constants.INVALID_INPUT
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Verify Element Text' )
        return status, result, value, err_msg

    def getTooltipText(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                #------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl' ):
                    arg = args[0]
                    if ( len(arg) == 1 and arg[0] == '' ):
                        pass
                    elif ( len( arg ) == 2 ):
                        row = int(arg[0]) - 1
                        col = int(arg[1]) - 1
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                #------------------------------Condition to check if its a table element
                #------------------------------Condition to check if its a simple-container element
                elif ( elem.type == 'GuiSimpleContainer' ):
                    arg = args[0]
                    if ( len(arg) == 1 and arg[0] == '' ):
                        pass
                    elif ( len( arg ) == 2 ):
                        row = int(arg[0])-1
                        col = int(arg[1])-1
                        elem = self.sc.getElementFromCell(self.sc.createCustomTable(elem),row,col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                #------------------------------Condition to check if its a simple-container element
                if ( not flag ):
                        value = elem.tooltip
                        if ( value == '' ):
                            value = elem.DefaultTooltip
                            if ( value == '' ):
                                value = "Null"
                        if ( value != None or value == "Null" ):
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            value = OUTPUT_CONSTANT
                            err_msg = 'ToolTipText not avaliable for the element'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Get Tooltip Text" )
        return status, result, value, err_msg

    def verifyTooltipText(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                input_val = args[0][0]
                #------------------------------Condition to check if its a table element
                if( elem.type == 'GuiTableControl' ):
                    if (len(args[0]) == 1 and args[0][0] == ''):
                        pass
                    elif len(args[0]) == 3:
                        row = int(args[0][0]) - 1
                        col = int(args[0][1]) - 1
                        input_val = args[0][2]
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                #------------------------------Condition to check if its a simple-container element
                elif ( elem.type == 'GuiSimpleContainer' ):
                    if (len(args[0]) == 1 and args[0][0] == ''):
                        pass
                    elif len(args[0]) == 3:
                        row = int(args[0][0]) - 1
                        col = int(args[0][1]) - 1
                        input_val = args[0][2]
                        elem = self.sc.getElementFromCell(self.sc.createCustomTable(elem),row,col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                #------------------------------Condition to check if its a simple-container element
                if ( not flag ):
                    #--------------------changing Null to ''
                    if ( input_val.strip() == "Null" ):
                        input_val = ''
                    # ------------------------------
                    if ( elem and id ):
                        if input_val.strip() == elem.tooltip.strip() or input_val.strip() == elem.DefaultTooltip.strip():
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'ToolTipText does not match input text'
                    else:
                        err_msg = sap_constants.ELELMENT_NOT_FOUND
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Tooltip Text" )
        return status, result, value, err_msg

    def getIconName(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                #------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl'):
                    if ( len(args[0]) == 1 and args[0][0] == '' ):
                        pass
                    elif ( len(args[0]) == 2 ) :
                        row = int(args[0][0]) - 1
                        col = int(args[0][1]) - 1
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                #------------------------------Condition to check if its a table element
                if ( not flag ):
                    if( elem != None and id != None ):
                        if ( elem.IconName != '' or elem.IconName != None ):
                                value = elem.IconName
                                if ( value in sap_constants.ICON_BITMAP ):
                                    value = sap_constants.ICON_BITMAP[value]
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'Icon name does not exist for the element.'
                    else:
                        err_msg = sap_constants.ELELMENT_NOT_FOUND
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Get Icon Name' )
        return status, result, value, err_msg

    def verifyIconName(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                text = args[0][0]
                # ------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl' ):
                    if ( len(args[0]) == 1 and args[0][0] == '' ):
                        pass
                    elif len( args[0] ) == 3:
                        row = int(args[0][0]) - 1
                        col = int(args[0][1]) - 1
                        text = args[0][2]
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                # ------------------------------Condition to check if its a table element
                if ( not flag ):
                    if ( id != None and elem != None ):
                        if ( elem.IconName != '' or elem.IconName != None ):
                            val = elem.IconName
                            if ( val.lower() == text.lower() ):
                                status = TEST_RESULT_PASS
                                result = TEST_RESULT_TRUE
                            if ( val in sap_constants.ICON_BITMAP ):
                                val = sap_constants.ICON_BITMAP[val]
                            #-----------------------------------------------check if input val and element val is the same
                                if (val.lower() == text.lower()):
                                    status = TEST_RESULT_PASS
                                    result = TEST_RESULT_TRUE
                            if (status == TEST_RESULT_FAIL):
                                err_msg = "Value did not match"
                        else:
                            err_msg = 'Icon name does not exist for the element.'
                    else:
                        err_msg = sap_constants.ELELMENT_NOT_FOUND
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occoured in Verify Icon Name' )
        return status, result, value, err_msg

    def getInputHelp(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                #------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl' ):
                    if ( len(args[0]) > 0 and len(args[0]) == 2 ) :
                        row = int(args[0][0]) - 1
                        col = int(args[0][1]) - 1
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                #------------------------------------------------------------------------
                if ( not flag ):
                    if ( elem.type == "GuiTextField" or elem.type == "GuiCTextField" or elem.type == "GuiRadioButton" or elem.type == "GuiCheckBox" ):
                        elem.SetFocus()
                        sendfnt = SendFunctionKeys()
                        sendfnt.sendfunction_keys("F4")
                        d1,d2,error,d3 = self.lk.getStatusBarMessage()
                        if ( error == "No input help is available" or error == "No error message" or error == "" ):
                            err_msg = 'No input help is available'
                        else:
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = 'No input help is available'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Get Input Help" )
        return status, result, value, err_msg

    def mouseHover(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
            #------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl' ):
                    if ( len(args[0]) == 1 and args[0][0] == '' ):
                        pass
                    elif ( len(args[0]) == 2 ):
                        row = int(args[0][0])-1
                        col = int(args[0][1])-1
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
            #--------------------------------mouse will move over to the middle of the element and click
                if ( not flag ):
                    left =  elem.__getattr__("ScreenLeft")
                    width = elem.__getattr__("Width")
                    x = left + width/2
                    top =  elem.__getattr__("ScreenTop")
                    height = elem.__getattr__("Height")
                    y = top + height/2
                    pywinauto.mouse.move(coords = (int(x), int(y)))
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Mouse Hover" )
        return status, result, value, err_msg

    def doubleClick(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
            #------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl' ):
                    if ( len(args[0]) == 1 and args[0][0] == '' ):
                        pass
                    elif ( len(args[0]) == 2 ):
                        row = int(args[0][0]) - 1
                        col = int(args[0][1]) - 1
                        elem = elem.GetCell(row, col)
                    elif ( len(args[0]) > 2 and len(args[0])==5 ):
                        row = int(args[0][3]) - 1
                        col = int(args[0][4]) - 1
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
            #--------------------------------mouse will move over to the middle of the element and click
                if ( not flag ):
                    left =  elem.ScreenLeft
                    width = elem.Width
                    x = left + width/2
                    top =  elem.ScreenTop
                    height = elem.Height
                    y= top + height/2
                    if ( elem.type == 'GuiTab' ):
                        x = left + width*0.75
                        y = top + height*0.25
                    pywinauto.mouse.double_click(button = "left", coords = (int(x), int(y)))
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Double Click" )
        return status, result, value, err_msg

    def click(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                #------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl' ):
                    if ( len(args[0]) == 1 and args[0][0] == '' ):
                        pass
                    elif ( len(args[0]) == 2 ):
                        row = int(args[0][0])-1
                        col = int(args[0][1])-1
                        elem = elem.GetCell(row, col)
                    elif ( len(args[0]) > 2 and len(args[0])==5 ):
                        row = int(args[0][3]) - 1
                        col = int(args[0][4]) - 1
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                #--------------------------------mouse will move over to the middle of the element and click
                if( not flag ):
                    left =  elem.__getattr__("ScreenLeft")
                    width = elem.__getattr__("Width")
                    x = left + width/2
                    top =  elem.__getattr__("ScreenTop")
                    height = elem.__getattr__("Height")
                    y = top + height/2
                    if ( elem.type == 'GuiTab' ):
                        x = left + width*0.75
                        y = top + height*0.25
                    pywinauto.mouse.click(button = 'left', coords = (int(x), int(y)))
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console("Error occured in Click")
        return status, result, value, err_msg

    def rightClick(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                #------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl' ):
                    if ( len(args[0]) == 1 and args[0][0] == '' ):
                        pass
                    elif ( len(args[0]) == 2 ):
                        row = int(args[0][0]) - 1
                        col = int(args[0][1]) - 1
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                if ( not flag ):
                    #--------------------------------Check if element is a tab and select that element
                    if ( elem.Type == "GuiTab" ):
                        elem.Select()
                    #--------------------------------mouse will move over to the middle of the element and click
                    left =  elem.__getattr__("ScreenLeft")
                    width = elem.__getattr__("Width")
                    x = left + width/2
                    top =  elem.__getattr__("ScreenTop")
                    height = elem.__getattr__("Height")
                    y = top + height/2
                    pywinauto.mouse.right_click(coords = (int(x), int(y)))
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Right Click" )
        return status, result, value, err_msg

    def setFocus(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
            #------------------------------Condition to check if its a table element
                if ( elem.type == 'GuiTableControl' ):
                    if ( len(args[0]) == 1 and args[0][0] == '' ):
                        pass
                    elif ( len(args[0]) == 2 ):
                        row = int(args[0][0]) - 1
                        col = int(args[0][1]) - 1
                        elem = elem.GetCell(row, col)
                    else:
                        elem = None
                        flag = True
                        err_msg = sap_constants.INVALID_INPUT
                if ( not flag ):
                    try:
                        #--------------------------------mouse will move over to the middle of the element and click
                        left = elem.__getattr__("ScreenLeft")
                        width = elem.__getattr__("Width")
                        x = left + width / 2
                        top = elem.__getattr__("ScreenTop")
                        height = elem.__getattr__("Height")
                        y = top + height / 2
                        pywinauto.mouse.move(coords=(int(x), int(y)))
                    except Exception as e:
                        err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
                    elem.SetFocus()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Set Focus" )
        return status, result, value, err_msg
#-----------------------------------------------------------------Scroll_Bar_related_keywords
    def scrollUp(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                element = ses.FindById(id)
                maximum = element.VerticalScrollbar.Maximum
                minimum = element.VerticalScrollbar.Minimum # will always be 0
                currentPosition = element.VerticalScrollbar.position
                pos = int(input_val[0])
                try:
                    if ( maximum == 0 ):
                        maximum, element, currentPosition = self.getVerticalScrollbarMax(element)

                    if ( maximum != 0 ):
                        if( pos>=0 ):
                            if (currentPosition >= pos):
                                element.VerticalScrollbar.position = currentPosition - pos
                            else:
                                element.VerticalScrollbar.position = minimum
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = sap_constants.INVALID_INPUT
                    else:
                        err_msg = 'Scrollbar cannot be moved'
                except Exception as e:
                    err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
                logger.print_on_console( "Error occured in Scroll UP" )
        except:
            err_msg = sap_constants.INVALID_INPUT
            log.error( err_msg )
            logger.print_on_console( err_msg )
        return status, result, value, err_msg

    def scrollDown(self, sap_id, input_val,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id,ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                element = ses.FindById(id)
                maximum = element.VerticalScrollbar.Maximum
                currentPosition = element.VerticalScrollbar.position
                pos = int(input_val[0])
                try:
                    if ( maximum == 0 ):
                        maximum, element, currentPosition = self.getVerticalScrollbarMax(element)

                    if ( maximum != 0 ):
                        if ( pos >= 0 ):
                            if(maximum - currentPosition >= pos):
                                element.VerticalScrollbar.position = currentPosition + pos
                            else:
                                element.VerticalScrollbar.position = maximum
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = sap_constants.INVALID_INPUT
                    else:
                        err_msg = 'Scrollbar cannot be moved'
                except Exception as e:
                    err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
                logger.print_on_console( "Error occured in Scroll Down" )
        except:
            err_msg = sap_constants.INVALID_INPUT
            log.error( err_msg )
            logger.print_on_console( err_msg )
        return status, result, value, err_msg

    def scrollLeft(self, sap_id, input_val,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                element = ses.FindById(id)
                maximum = element.HorizontalScrollbar.Maximum
                minimum = element.HorizontalScrollbar.Minimum
                currentPosition = element.HorizontalScrollbar.position
                pos=int(input_val[0])
                try:
                    if ( maximum == 0 ):
                       maximum, element, currentPosition = self.getHorizontalScrollbarMax(element)

                    if ( maximum != 0 ):
                        if ( pos >= 0 ):
                            if ( currentPosition >= pos ):
                                element.HorizontalScrollbar.position = currentPosition - pos
                            else:
                                element.HorizontalScrollbar.position = minimum
                            status=sap_constants.TEST_RESULT_PASS
                            result=sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = sap_constants.INVALID_INPUT
                    else:
                        err_msg = 'Scrollbar cannot be moved'
                except Exception as e:
                    err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
                logger.print_on_console( 'Error occured in Scroll Left' )
        except:
            err_msg = sap_constants.INVALID_INPUT
            log.error( err_msg )
            logger.print_on_console( err_msg )
        return status, result, value, err_msg

    def scrollRight(self, sap_id, input_val,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                element = ses.FindById(id)
                maximum = element.HorizontalScrollbar.Maximum
                currentPosition = element.HorizontalScrollbar.position
                pos=int(input_val[0])
                try:
                    if ( maximum == 0 ):
                        maximum, element, currentPosition = self.getHorizontalScrollbarMax(element)

                    if ( maximum != 0 ):
                        if ( pos >= 0 ):
                            if (maximum - currentPosition >= pos):
                                    element.HorizontalScrollbar.position = currentPosition + pos
                            else:
                                element.HorizontalScrollbar.position = maximum
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = sap_constants.INVALID_INPUT
                    else:
                        err_msg = 'Scrollbar cannot be moved'
                except Exception as e:
                    err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
                logger.print_on_console( 'Error occured in Scroll Right' )
        except:
            err_msg = sap_constants.INVALID_INPUT
            log.error( err_msg )
            logger.print_on_console( err_msg )
        return status, result, value, err_msg
#----------------------------------------------------------Scroll bar operations to recursively call elements
#----------------------------------------------------------to find out if the max scroll bar length exists
    def getVerticalScrollbarMax(self, elem):
            i = 0
            while True:
                try:
                    child = elem.Children(i)
                    try:
                        if ( child.VerticalScrollbar.Maximum != 0 ):
                            maximum = child.VerticalScrollbar.Maximum
                            element = child
                            currentPosition = element.VerticalScrollbar.position
                            break
                    except:
                        pass
                    i = i + 1
                    maximum, element, currentPosition = self.getVerticalScrollbarMax(child)
                except Exception as e:
                    break
            try:
                return maximum, element, currentPosition
            except Exception as e:
                return 0, None, 0


    def getHorizontalScrollbarMax(self, elem):
            i = 0
            while True:
                try:
                    child = elem.Children(i)
                    try:
                        if ( child.HorizontalScrollbar.Maximum != 0 ):
                            maximum = child.HorizontalScrollbar.Maximum
                            element = child
                            currentPosition = element.HorizontalScrollbar.position
                            break
                    except:
                        pass
                    i = i + 1
                    maximum, element, currentPosition = self.getHorizontalScrollbarMax(child)
                except Exception as e:
                    break
            try:
                return maximum, element, currentPosition
            except Exception as e:
                return 0, None, 0
#----------------------------------------------------------Scroll bar operations

#-----------------------------------------------------------------Tabs_Related_related_keywords
    def moveTabs(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.ScrollToLeft()
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Move Tabs" )
        return status, result, value, err_msg

    def selectTab(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiTab' ):
                    elem.Select()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Select Tab" )
        return status, result, value, err_msg