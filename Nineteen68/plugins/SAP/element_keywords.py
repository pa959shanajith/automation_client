#-------------------------------------------------------------------------------
# Name:        Element_Keywords
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
import launch_keywords
from launch_keywords import Launch_Keywords
from constants import *
import logger
from saputil_operations import SapUtilKeywords
from sendfunction_keys import SendFunctionKeys
import logging
import logging.config
log = logging.getLogger('element_keywords.py')

class ElementKeywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()


    def get_element_text(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):

                        value = ses.FindById(id).text
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg='element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Exception has occured :",e)
        #log.info(RETURN_RESULT)
        return status,result,value,err_msg

    def verify_element_text(self, sap_id,url,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                    if(len(input_val)!=0):
                        if(len(input_val)>1):
                            input = input_val[2]
                        else:
                            input=input_val[0]

                        if(ses.FindById(id).text== input):
                            status=sap_constants.TEST_RESULT_PASS
                            result=sap_constants.TEST_RESULT_TRUE
                    elif(len(input_val)==0):
                        log.info('entered text is empty')
                        err_msg='entered text is empty'
                        logger.print_on_console('entered text is empty')
                    else:
                        log.info('Incorrect syntax')
                        err_msg='Incorrect syntax'
                        logger.print_on_console('Incorrect syntax')
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg='element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Exception has occured :",e)
        #log.info(RETURN_RESULT)
        return status,result,value,err_msg

    def getTooltipText(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        id,ses=self.uk.getSapElement(sap_id)
        elem = ses.FindById(id)

        try:
            #------------------------------Condition to check if its a table element
            if(elem.type=='GuiTableControl'):
                arg=args[1]
                if len(arg) > 0 and len(arg)==2 :
                    row=int(arg[0])-2
                    col=int(arg[1])-2
                    elem = elem.GetCell(row, col)
                else:
                    elem=None
                    logger.print_on_console('Invalid Arguments Passed')
            #------------------------------Condition to check if its a table element
            if(id != None):
                    value = elem.tooltip
                    if value== '':
                        value = elem.DefaultTooltip
                        if value =='':
                            value ="Null"
                    if(value != None or value =="Null"):
                        status=sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        value=OUTPUT_CONSTANT
                        logger.print_on_console('ToolTipText not avaliable for the element ')
            else:
                err_msg = sap_constants.ERROR_MSG
                logger.print_on_console('Element does not exist')

        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console('Error cooured in getTooltipText and is :',e)
        return status,result,value,err_msg

    def verifyTooltipText(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        id,ses=self.uk.getSapElement(sap_id)
        elem = ses.FindById(id)
        input_val=args[1]
        try:
            #------------------------------Condition to check if its a table element
            if(elem.type=='GuiTableControl'):
                arg=args[1]
                if len(arg) > 0 and len(arg)==2 :
                    row=int(arg[0])-2
                    col=int(arg[1])-2
                    input_val=arg[2]
                    elem = elem.GetCell(row, col)
                else:
                    elem=None
                    logger.print_on_console('Invalid Arguments Passed')
            #------------------------------Condition to check if its a table element
            if(id != None):
                    value = elem.tooltip
                    if value== '':
                        value = elem.DefaultTooltip
                        if value =='':
                            value ="Null"
                    if(value ==input_val):
                        status=sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        value=OUTPUT_CONSTANT
                        logger.print_on_console('ToolTipText does not match verify text ')
            else:
                err_msg = sap_constants.ERROR_MSG
                logger.print_on_console('Element does not exist')

        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console('Error cooured in getTooltipText and is :',e)
        return status,result,value,err_msg

    def getInputHelp(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
        sendfnt=SendFunctionKeys()
        id,ses=self.uk.getSapElement(sap_id)
        elem = ses.FindById(id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                        #------------------------------Condition to check if its a table element
                        if(elem.type=='GuiTableControl'):
                            arg=args[1]
                            if len(arg) > 0 and len(arg)==2 :
                                row=int(arg[0])-2
                                col=int(arg[1])-2
                                elem = elem.GetCell(row, col)
                            else:
                                elem=None
                                logger.print_on_console('Invalid Arguments Passed')

                        if(elem.type == "GuiTextField" or elem.type == "GuiCTextField" or elem.type == "GuiRadioButton" or elem.type == "GuiCheckBox"):
                            elem.SetFocus()
                            sendfnt.sendfunction_keys("F4")
                            d1,d2,error,d3=self.lk.getErrorMessage()
                            if(error=="No input help is available" or error=="No error message" or error ==""):
                                logger.print_on_console('No input help is available')
                                err_msg='No input help is available'
                            else:
                                status=sap_constants.TEST_RESULT_PASS
                                result=sap_constants.TEST_RESULT_TRUE
                        else:
                            logger.print_on_console('No input help is available')
                            err_msg='No input help is available'

            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg='element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Exception has occured :",e)
        #log.info(RETURN_RESULT)
        return status,result,value,err_msg

    def mouseHover(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        id,ses=self.uk.getSapElement(sap_id)
        elem = ses.FindById(id)
        try:
        #------------------------------Condition to check if its a table element
            if(elem.type=='GuiTableControl'):
                arg=args[1]
                if len(arg) > 0 and len(arg)==2 :
                    row=int(arg[0])-2
                    col=int(arg[1])-2
                    elem = elem.GetCell(row, col)
                else:
                    elem=None
                    logger.print_on_console('Invalid Arguments Passed')
        #--------------------------------mouse will move over to the middle of the element and click

            left =  elem.__getattr__("ScreenLeft")
            width = elem.__getattr__("Width")
            x = left + width/2
            top =  elem.__getattr__("ScreenTop")
            height = elem.__getattr__("Height")
            y= top + height/2
            pywinauto.mouse.move(coords=(int(x), int(y)))
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            import traceback
            traceback.print_exc()
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg

    def doubleClick(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        id,ses=self.uk.getSapElement(sap_id)
        elem=ses.FindById(id)
        try:
        #------------------------------Condition to check if its a table element
            if(elem.type=='GuiTableControl'):
                arg=args[1]
                if len(arg) > 0 and len(arg)==2:
                    row=int(arg[0])-2
                    col=int(arg[1])-2
                    elem = elem.GetCell(row, col)
                else:
                    elem=None
                    logger.print_on_console('Invalid Arguments Passed')
        #--------------------------------mouse will move over to the middle of the element and click

            left =  elem.ScreenLeft
            width = elem.Width
            x = left + width/2
            top =  elem.ScreenTop
            height = elem.Height
            y= top + height/2
            pywinauto.mouse.double_click(button="left", coords = (int(x), int(y)))
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            import traceback
            traceback.print_exc()
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg

    def click(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        id,ses=self.uk.getSapElement(sap_id)
        elem=ses.FindById(id)
        try:
##            if(elem.type=="GuiRadioButton"):
##                if(elem.Changeable == True):
##                    elem.Press()
##                    status =sap_constants.TEST_RESULT_PASS
##                    result = sap_constants.TEST_RESULT_TRUE

            #------------------------------Condition to check if its a table element
                if(elem.type=='GuiTableControl'):
                    arg=args[1]
                    if len(arg) > 0 and len(arg)==2:
                        row=int(arg[0])-2
                        col=int(arg[1])-2
                        elem = elem.GetCell(row, col)
                    else:
                        elem=None
                        logger.print_on_console('Invalid Arguments Passed')
            #--------------------------------mouse will move over to the middle of the element and click

                left =  elem.__getattr__("ScreenLeft")
                width = elem.__getattr__("Width")
                x = left + width/2
                top =  elem.__getattr__("ScreenTop")
                height = elem.__getattr__("Height")
                y= top + height/2
                pywinauto.mouse.click(button='left', coords=(int(x), int(y)))
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            import traceback
            traceback.print_exc()
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg

    def rightClick(self, sap_id,*args):
            self.lk.setWindowToForeground(sap_id)
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            value = OUTPUT_CONSTANT
            err_msg=None
            id,ses=self.uk.getSapElement(sap_id)
            elem=ses.FindById(id)
            try:

                #------------------------------Condition to check if its a table element
                    if(elem.type=='GuiTableControl'):
                        arg=args[1]
                        if len(arg) > 0 and len(arg)==2:
                            row=int(arg[0])-2
                            col=int(arg[1])-2
                            elem = elem.GetCell(row, col)
                        else:
                            elem=None
                            logger.print_on_console('Invalid Arguments Passed')
                #--------------------------------Check if element is a tab and select that element

                    if(elem.Type == "GuiTab"):
                            elem.Select()
                #--------------------------------mouse will move over to the middle of the element and click
                    left =  elem.__getattr__("ScreenLeft")
                    width = elem.__getattr__("Width")
                    x = left + width/2
                    top =  elem.__getattr__("ScreenTop")
                    height = elem.__getattr__("Height")
                    y= top + height/2
                    pywinauto.mouse.right_click(coords=(int(x), int(y)))
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
            except Exception as e:
                log.error('Error occured',e)
                import traceback
                traceback.print_exc()
                err_msg = sap_constants.ERROR_MSG
            return status,result,value,err_msg

    def setFocus(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        id,ses=self.uk.getSapElement(sap_id)
        elem=ses.FindById(id)
        try:
        #------------------------------Condition to check if its a table element
            if(elem.type=='GuiTableControl'):
                arg=args[1]
                if len(arg) > 0 and len(arg)==2 :
                    row=int(arg[0])-2
                    col=int(arg[1])-2
                    elem = elem.GetCell(row, col)
                else:
                    elem=None
                    logger.print_on_console('Invalid Arguments Passed')
        #--------------------------------mouse will move over to the middle of the element and click
            left =  elem.__getattr__("ScreenLeft")
            width = elem.__getattr__("Width")
            x = left + width/2
            top =  elem.__getattr__("ScreenTop")
            height = elem.__getattr__("Height")
            y= top + height/2
            pywinauto.mouse.move(coords=(int(x), int(y)))
            elem.SetFocus()
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg
#-----------------------------------------------------------------Scroll_Bar_related_keywords
    def scrollUp(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            pos=int(input_val[0])
            try:
                elem = ses.FindById(id)
                maximum = elem.VerticalScrollbar.Maximum
                element = elem
                if(elem.VerticalScrollbar.Maximum==0):
                    maximum, element = self.getVerticalScrollbarMax(elem)
                if maximum!=0:
                    if(pos>=0):
                        element.VerticalScrollbar.position = element.VerticalScrollbar.Position - pos
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                else:
                    logger.print_on_console('Scrollbar cannot be moved')
            except Exception as e:
                #import traceback
                #traceback.print_exc()
                logger.print_on_console('Scrollbar not found    ',e)
                log.error('Error occured',e)
                err_msg = sap_constants.ERROR_MSG
        except:
            logger.print_on_console(sap_constants.INVALID_INPUT)
            err_msg=sap_constants.INVALID_INPUT
        return status,result,value,err_msg

    def scrollDown(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            pos=int(input_val[0])
            try:
                elem = ses.FindById(id)
                maximum = elem.VerticalScrollbar.Maximum
                element = elem
                if(elem.VerticalScrollbar.Maximum==0):
                    maximum, element = self.getVerticalScrollbarMax(elem)
                if maximum!=0:
                    if(pos>=0):
                        element.VerticalScrollbar.position = element.VerticalScrollbar.Position + pos
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                else:
                    logger.print_on_console('Scrollbar cannot be moved')
            except Exception as e:
                logger.print_on_console('Scrollbar not found')
                log.error('Error occured',e)
                err_msg = sap_constants.ERROR_MSG
        except:
            logger.print_on_console(sap_constants.INVALID_INPUT)
            err_msg=sap_constants.INVALID_INPUT
        return status,result,value,err_msg

    def scrollLeft(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            pos=int(input_val[0])
            try:
                elem = ses.FindById(id)
                maximum = elem.HorizontalScrollbar.Maximum
                element = elem
                if(elem.HorizontalScrollbar.Maximum==0):
                   maximum, element = self.getHorizontalScrollbarMax(elem)
                if maximum!=0:
                    if(pos>=0):
                        element.HorizontalScrollbar.position = element.HorizontalScrollbar.Position - pos
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                else:
                    logger.print_on_console('Scrollbar cannot be moved')
            except Exception as e:
                logger.print_on_console('Scrollbar not found')
                log.error('Error occured',e)
                err_msg = sap_constants.ERROR_MSG
        except:
            logger.print_on_console(sap_constants.INVALID_INPUT)
            err_msg=sap_constants.INVALID_INPUT
        return status,result,value,err_msg

    def scrollRight(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            pos=int(input_val[0])
            try:
                elem = ses.FindById(id)
                maximum = elem.HorizontalScrollbar.Maximum
                element = elem
                if(elem.HorizontalScrollbar.Maximum==0):
                    maximum, element = self.getHorizontalScrollbarMax(elem)
                if maximum!=0:
                    if(pos>=0):
                        element.HorizontalScrollbar.position = element.HorizontalScrollbar.Position + pos
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                else:
                    logger.print_on_console('Scrollbar cannot be moved')
            except Exception as e:
                logger.print_on_console('Scrollbar not found')
                log.error('Error occured',e)
                err_msg = sap_constants.ERROR_MSG
        except:
            logger.print_on_console(sap_constants.INVALID_INPUT)
            err_msg=sap_constants.INVALID_INPUT
        return status,result,value,err_msg
#----------------------------------------------------------Scroll bar operations to recursively call elements
#----------------------------------------------------------to find out if the max scroll bar length exists
    def getVerticalScrollbarMax(self,elem):
            i = 0
            while True:
                try:
                    child = elem.Children(i)
                    try:
                        if(child.VerticalScrollbar.Maximum != 0):
                            maximum = child.VerticalScrollbar.Maximum
                            element = child
                            break
                    except:
                        pass
                    i = i + 1
                    maximum, element = self.getVerticalScrollbarMax(child)
                except Exception as e:
                    break
            try:
                return maximum, element
            except Exception as e:
                return 0, None


    def getHorizontalScrollbarMax(self,elem):
            i = 0
            while True:
                try:
                    child = elem.Children(i)
                    try:
                        if(child.HorizontalScrollbar.Maximum != 0):
                            maximum = child.HorizontalScrollbar.Maximum
                            element = child
                            break
                    except:
                        pass
                    i = i + 1
                    maximum, element = self.getHorizontalScrollbarMax(child)
                except Exception as e:
                    break
            try:
                return maximum, element
            except Exception as e:
                return 0, None

#----------------------------------------------------------Scroll bar operations

#-----------------------------------------------------------------Tabs_Related_related_keywords
    def moveTabs(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem = ses.FindById(id)
            elem.ScrollToLeft()
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg


