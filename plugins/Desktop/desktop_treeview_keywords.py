#-------------------------------------------------------------------------------
# Name:        desktop_treeview_keywords
# Purpose:     To automate tree view object/element in a give window
#
# Author:      anas.ahmed
#
# Created:     25-09-2017
# Copyright:   (c) anas.ahmed 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_launch_keywords
import pywinauto
from desktop_editable_text import Text_Box
import logger
import desktop_constants
import desktop_editable_text
import time
import string
from constants import *
import logging
log = logging.getLogger( 'desktop_treeview_keywords.py' )

class Tree_View_Keywords():
##    def get_item_count(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        try:
##            if desktop_launch_keywords.window_name!=None:
##                verify_obj = Text_Box()
##                log.info('Recieved element from the desktop dispatcher')
##                check = verify_obj.verify_parent(element,parent)
##                log.debug('Parent of element while scraping')
##                log.debug(parent)
##                log.debug('Parent check status')
##                log.debug(check)
##                if (check):
##                    log.info('Parent matched')
##                    if(element.is_enabled()):
##                        verb=element.ItemCount()
##                        status = desktop_constants.TEST_RESULT_PASS
##                        result = desktop_constants.TEST_RESULT_TRUE
##                    else:
##                      log.info('Element state does not allow to perform the operation')
##                      logger.print_on_console('Element state does not allow to perform the operation')
##                      err_msg= 'Element state does not allow to perform the operation'
##                else:
##                   log.info('Element not present on the page where operation is trying to be performed')
##                   err_msg='Element not present on the page where operation is trying to be performed'
##                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
##        except Exception as exception:
##            log.error(exception)
##            logger.print_on_console(exception)
##            err_msg="Unable to perform action on this element."
##        return status,result,verb,err_msg
##
##    def verify_item_count(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        try:
##            if desktop_launch_keywords.window_name!=None:
##                verify_obj = Text_Box()
##                log.info('Recieved element from the desktop dispatcher')
##                check = verify_obj.verify_parent(element,parent)
##                log.debug('Parent of element while scraping')
##                log.debug(parent)
##                log.debug('Parent check status')
##                log.debug(check)
##                if (check):
##                    log.info('Parent matched')
##                    if(element.is_enabled()):
##                        count=element.ItemCount()
##                        if count==int(input_val[0]):
##                            status = desktop_constants.TEST_RESULT_PASS
##                            result = desktop_constants.TEST_RESULT_TRUE
##                    else:
##                      log.info('Element state does not allow to perform the operation')
##                      logger.print_on_console('Element state does not allow to perform the operation')
##                      err_msg= 'Element state does not allow to perform the operation'
##                else:
##                   log.info('Element not present on the page where operation is trying to be performed')
##                   err_msg='Element not present on the page where operation is trying to be performed'
##                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
##        except Exception as exception:
##            log.error(exception)
##            logger.print_on_console(exception)
##            err_msg="Unable to perform action on this element."
##        return status,result,verb,err_msg
##
##    def get_root_elements(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        roots=[]
##        All_roots=[]
##        try:
##            if desktop_launch_keywords.window_name!=None:
##                verify_obj = Text_Box()
##                log.info('Recieved element from the desktop dispatcher')
##                check = verify_obj.verify_parent(element,parent)
##                log.debug('Parent of element while scraping')
##                log.debug(parent)
##                log.debug('Parent check status')
##                log.debug(check)
##                if (check):
##                    log.info('Parent matched')
##                    if(element.is_enabled()):
##                        All_roots=element.Roots()
##                        for root in All_roots:
##                            root_text=root.Text()
##                            if not isinstance(root_text,basestring):
##                                root_text=str(root_text)
##                            else:
##                                root_text=root_text.encode('ascii', 'replace')
##                            roots.append(root_text)
##                        verb=roots
##                        status = desktop_constants.TEST_RESULT_PASS
##                        result = desktop_constants.TEST_RESULT_TRUE
##                    else:
##                      log.info('Element state does not allow to perform the operation')
##                      logger.print_on_console('Element state does not allow to perform the operation')
##                      err_msg= 'Element state does not allow to perform the operation'
##                else:
##                   log.info('Element not present on the page where operation is trying to be performed')
##                   err_msg='Element not present on the page where operation is trying to be performed'
##                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
##        except Exception as exception:
##            log.error(exception)
##            logger.print_on_console(exception)
##            err_msg="Unable to perform action on this element."
##        return status,result,verb,err_msg
##
##    def expand_all(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        roots=[]
##        try:
##            if desktop_launch_keywords.window_name!=None:
##                verify_obj = Text_Box()
##                log.info('Recieved element from the desktop dispatcher')
##                check = verify_obj.verify_parent(element,parent)
##                log.debug('Parent of element while scraping')
##                log.debug(parent)
##                log.debug('Parent check status')
##                log.debug(check)
##                if (check):
##                    log.info('Parent matched')
##                    if(element.is_enabled()):
##                        roots=element.Roots()
##                        for root in roots:
##                            root.Expand()
##                            sub_roots=root.SubElements()
##                            for sub_elem in sub_roots:
##                                sub_elem.Expand()
##                        status = desktop_constants.TEST_RESULT_PASS
##                        result = desktop_constants.TEST_RESULT_TRUE
##                    else:
##                      log.info('Element state does not allow to perform the operation')
##                      logger.print_on_console('Element state does not allow to perform the operation')
##                      err_msg= 'Element state does not allow to perform the operation'
##                else:
##                   log.info('Element not present on the page where operation is trying to be performed')
##                   err_msg='Element not present on the page where operation is trying to be performed'
##                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
##        except Exception as exception:
##            log.error(exception)
##            logger.print_on_console(exception)
##            err_msg="Unable to perform action on this element."
##        return status,result,verb,err_msg
##
##    def collapse_all(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        roots=[]
##        try:
##            if desktop_launch_keywords.window_name!=None:
##                verify_obj = Text_Box()
##                log.info('Recieved element from the desktop dispatcher')
##                check = verify_obj.verify_parent(element,parent)
##                log.debug('Parent of element while scraping')
##                log.debug(parent)
##                log.debug('Parent check status')
##                log.debug(check)
##                if (check):
##                    log.info('Parent matched')
##                    if(element.is_enabled()):
##                        roots=element.Roots()
##                        for root in roots:
##                            sub_roots=root.SubElements()
##                            for sub_elem in sub_roots:
##                                sub_elem.Collapse()
##                            root.Collapse()
##                        status = desktop_constants.TEST_RESULT_PASS
##                        result = desktop_constants.TEST_RESULT_TRUE
##                    else:
##                      log.info('Element state does not allow to perform the operation')
##                      logger.print_on_console('Element state does not allow to perform the operation')
##                      err_msg= 'Element state does not allow to perform the operation'
##                else:
##                   log.info('Element not present on the page where operation is trying to be performed')
##                   err_msg='Element not present on the page where operation is trying to be performed'
##                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
##        except Exception as exception:
##            log.error(exception)
##            logger.print_on_console(exception)
##            err_msg="Unable to perform action on this element."
##        return status,result,verb,err_msg
##
##    def select_element(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        input_val=input_val[0]
##        #------------------------------------------------ replacing ";" with "\"
##        if "\\" in input_val:
##            input_val=string.replace(input_val,'\\','\ ')
##        input_val="\ "+input_val
##        #-------------------------------------------------
##        try:
##            if desktop_launch_keywords.window_name!=None:
##                verify_obj = Text_Box()
##                log.info('Recieved element from the desktop dispatcher')
##                check = verify_obj.verify_parent(element,parent)
##                log.debug('Parent of element while scraping')
##                log.debug(parent)
##                log.debug('Parent check status')
##                log.debug(check)
##                if (check):
##                    log.info('Parent matched')
##                    if(element.is_enabled()):
##                        try:
##                            element.Select(input_val)
##                            status = desktop_constants.TEST_RESULT_PASS
##                            result = desktop_constants.TEST_RESULT_TRUE
##                        except Exception as e:
##                            err_msg =e
##                            logger.print_on_console(e)
##                            log.info(e)
##                    else:
##                      log.info('Element state does not allow to perform the operation')
##                      logger.print_on_console('Element state does not allow to perform the operation')
##                      err_msg= 'Element state does not allow to perform the operation'
##                else:
##                   log.info('Element not present on the page where operation is trying to be performed')
##                   err_msg='Element not present on the page where operation is trying to be performed'
##                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
##        except Exception as exception:
##            log.error(exception)
##            logger.print_on_console(exception)
##            err_msg="Unable to perform action on this element."
##        return status,result,verb,err_msg
##
##    def get_children(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        children=[]
##        child=''
##        children_text=[]
##        input_val=input_val[0]
##        #------------------------------------------------ replacing ";" with "\"
##        if "\\" in input_val:
##            input_val=string.replace(input_val ,'\\','\ ')
##        input_val="\ "+input_val
##        #-------------------------------------------------
##        try:
##            if desktop_launch_keywords.window_name!=None:
##                verify_obj = Text_Box()
##                log.info('Recieved element from the desktop dispatcher')
##                check = verify_obj.verify_parent(element,parent)
##                log.debug('Parent of element while scraping')
##                log.debug(parent)
##                log.debug('Parent check status')
##                log.debug(check)
##                if (check):
##                    log.info('Parent matched')
##                    if(element.is_enabled()):
##                        try:
##                            root_elem=element.Item(input_val,exact=False)
##                            children=root_elem.Children()
##                            if len(children)>0:
##                                for child in children:
##                                    child=child.Text()
##                                    if not isinstance(child,basestring):
##                                        child=str(child)
##                                    else:
##                                        child=child.encode('ascii', 'replace')
##                                    children_text.append(child)
##                                verb=children_text
##                                status = desktop_constants.TEST_RESULT_PASS
##                                result = desktop_constants.TEST_RESULT_TRUE
##                            else:
##                                err_msg="Element has no children"
##                                log.info('Element has no children')
##                                logger.print_on_console('Element has no children')
##                        except Exception as e:
##                            err_msg =e
##                            logger.print_on_console(e)
##                            log.info(e)
##                    else:
##                      log.info('Element state does not allow to perform the operation')
##                      logger.print_on_console('Element state does not allow to perform the operation')
##                      err_msg= 'Element state does not allow to perform the operation'
##                else:
##                   log.info('Element not present on the page where operation is trying to be performed')
##                   err_msg='Element not present on the page where operation is trying to be performed'
##                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
##        except Exception as exception:
##            log.error(exception)
##            logger.print_on_console(exception)
##            err_msg="Unable to perform action on this element."
##        return status,result,verb,err_msg
##
##    def verify_children(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        ele=''
##        children=[]
##        child=''
##        children_text=[]
##        input_path=''
##        input_text=[]
##        temp_list=[]
##        #-------------------------------------------------
##        input_path=str(input_val[0])
##        if "\\" in input_path:
##            input_path=string.replace(input_path ,'\\','\ ')
##        input_path="\ "+input_path
##        #-------------------------------------------------
##        input_text=input_val[1:]
##        try:
##            if desktop_launch_keywords.window_name!=None:
##                verify_obj = Text_Box()
##                log.info('Recieved element from the desktop dispatcher')
##                check = verify_obj.verify_parent(element,parent)
##                log.debug('Parent of element while scraping')
##                log.debug(parent)
##                log.debug('Parent check status')
##                log.debug(check)
##                if (check):
##                    log.info('Parent matched')
##                    if(element.is_enabled()):
##                        ele=element.Item(input_path,exact=False)
##                        children=ele.children()
##                        if len(children)>0:
##                                for child in children:
##                                    child=child.Text()
##                                    if not isinstance(child,basestring):
##                                        child=str(child)
##                                    else:
##                                        child=child.encode('ascii', 'replace')
##                                    children_text.append(child)
##                        if len(children_text)!=0 and len(input_text)!=0:
##                            fail_flag=False
##                            for i in input_text:
##                                if i not in children_text:
##                                    fail_flag=True
##                            if fail_flag==False:
##                                status = desktop_constants.TEST_RESULT_PASS
##                                result = desktop_constants.TEST_RESULT_TRUE
##                            else:
##                                log.info('Element/Elements provided do not exist')
##                                logger.print_on_console('Element/Elements provided do not exist')
##                                err_msg= 'Element/Elements provided do not exist'
##                    else:
##                      log.info('Element state does not allow to perform the operation')
##                      logger.print_on_console('Element state does not allow to perform the operation')
##                      err_msg= 'Element state does not allow to perform the operation'
##                else:
##                   log.info('Element not present on the page where operation is trying to be performed')
##                   err_msg='Element not present on the page where operation is trying to be performed'
##                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
##        except Exception as exception:
##            log.error(exception)
##            logger.print_on_console(exception)
##            err_msg="Unable to perform action on this element."
##        return status,result,verb,err_msg

    def click_tree_element(self, element , parent , input_val , *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        tree_elm = ''
        #-----------------------custom element check
        """Following operations need to be performed for custom:
        1.Check is input is > 3
        2.Check if input_val[0] is a tree object type
        3.Check if input type of inputval[2] is an integer
        4.If above conditions are matched then object is a custom object of tree type at position input_val[1] from parent object
        5.Since inputs start from the 4th input_val assign these values to a variable and proceed"""
        if ( len(input_val) > 3 and (input_val[0]).lower()=='tree' and int(input_val[2])==True):
            input_val = input_val[3:]
            log.info('Custom object of type "tree" with input : ' + str(input_val))
        #-------------------------------------------

        if ( len(input_val) == 1 ):
            if ( input_val[0] == '' ):
                flag = True
        else:
            input_val = '\\' + '\\'.join(input_val) #replacing ";" with "\\"
        if ( flag != True ):
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    verify_obj = Text_Box()
                    log.info( 'Recieved element from the desktop dispatcher' )
                    check = verify_obj.verify_parent(element, parent)
                    log.debug( 'Parent of element while scraping' )
                    log.debug( parent )
                    log.debug( 'Parent check status' )
                    log.debug( check )
                    if ( check ):
                        log.info('Parent matched')
                        if( element.is_enabled() ):
                                if ( element.backend.name == 'win32' ):
                                    tree_elm = element.item(input_val, exact = True)
                                    tree_elm.click_input(button = 'left', double = False, wheel_dist = 0, where = 'text', pressed = '')
                                elif ( element.backend.name == 'uia' ):
                                    tree_elm = element.get_item(input_val, exact = True)
                                    tree_elm.click_input(button = 'left', double = False, wheel_dist = 0, pressed = '')
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'Element state does not allow to perform the operation'
                    else:
                       err_msg = 'Element not present on the page where operation is trying to be performed'
                if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
        elif ( flag == True ):
            Rect = ''
            try:
                #----------get the element coordinates
                Rect = str(element.rectangle())
                Rect = Rect[1 : len(Rect) - 1]
                Rect = Rect.split(",")
                Left = Rect[0].strip()#left
                if ( "L" in Left ):
                    Left = int(Left[1:])
                else:
                    Left = int(Left)
                Top = Rect[1].strip()#top
                if ( "T" in Top ):
                    Top = int(Top[1:])
                else:
                    Top = int(Top)
                Right = Rect[2].strip()#right
                if ( "R" in Right ):
                    Right = int(Right[1:])
                else:
                    Right = int(Right)
                Bottom = Rect[3].strip()#bottom
                if ( "B" in Bottom ):
                    Bottom = int(Bottom[1:])
                else:
                    Bottom = int(Bottom)
                #---------------------Finding height and width
                height = Bottom - Top
                width = Right - Left
                #--------------------Finding X and Y co-ordinates
                x = Left + width / 2
                y = Top + height / 2
                pywinauto.mouse.click(button = 'left', coords = (int(x), int(y)))
                status = desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
        return status, result, verb, err_msg

##    def double_click_tree_element(self, element , parent , input_val , *args):
##        status=desktop_constants.TEST_RESULT_FAIL
##        result=desktop_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        err_msg=None
##        flag=False
##        tree_elm=''
##        if len(input_val)==0:
##            flag=True
##        else:
##            input_val=input_val[0]
##            #------------------------------------------------ replacing ";" with "\"
##            if "\\" in input_val:
##                input_val=string.replace(input_val ,'\\','\ ')
##            input_val="\ "+input_val
##            #-------------------------------------------------
##        if flag!=True:
##            try:
##                if desktop_launch_keywords.window_name!=None:
##                    verify_obj = Text_Box()
##                    log.info('Recieved element from the desktop dispatcher')
##                    check = verify_obj.verify_parent(element,parent)
##                    log.debug('Parent of element while scraping')
##                    log.debug(parent)
##                    log.debug('Parent check status')
##                    log.debug(check)
##                    if (check):
##                        log.info('Parent matched')
##                        if(element.is_enabled()):
##                            tree_elm=element.Item(input_val, exact=False)
##                            tree_elm.ClickInput(button='left', double=True, wheel_dist=0, where='text', pressed='')
##                            status = desktop_constants.TEST_RESULT_PASS
##                            result = desktop_constants.TEST_RESULT_TRUE
##                        else:
##                          log.info('Element state does not allow to perform the operation')
##                          logger.print_on_console('Element state does not allow to perform the operation')
##                          err_msg= 'Element state does not allow to perform the operation'
##                    else:
##                       log.info('Element not present on the page where operation is trying to be performed')
##                       err_msg='Element not present on the page where operation is trying to be performed'
##                       logger.print_on_console('Element not present on the page where operation is trying to be performed')
##            except Exception as exception:
##                log.error(exception)
##                logger.print_on_console(exception)
##                err_msg="Unable to perform action on this element."
##        elif flag==True:
##            Rect=''
##            try:
##                #----------get the element coordinates
##                Rect=str(element.Rectangle())
##                Rect=Rect[1:len(Rect)-1]
##                Rect=Rect.split(",")
##                Left=Rect[0].strip()#left
##                if "L" in Left:
##                    Left=int(Left[1:])
##                else:
##                    Left=int(Left)
##                Top=Rect[1].strip()#top
##                if "T" in Top:
##                    Top=int(Top[1:])
##                else:
##                    Top=int(Top)
##                Right=Rect[2].strip()#right
##                if "R" in Right:
##                    Right=int(Right[1:])
##                else:
##                    Right=int(Right)
##                Bottom=Rect[3].strip()#bottom
##                if "B" in Bottom:
##                    Bottom=int(Bottom[1:])
##                else:
##                    Bottom=int(Bottom)
##                #---------------------Finding height and width
##                height=Bottom-Top
##                width=Right-Left
##                #--------------------Finding X and Y co-ordinates
##                x = Left + width/2
##                y= Top + height/2
##                pywinauto.mouse.double_click(button='left',coords=(int(x), int(y)))
##                status = desktop_constants.TEST_RESULT_PASS
##                result = desktop_constants.TEST_RESULT_TRUE
##            except Exception as exception:
##                import traceback
##                traceback.print_exc()
##                log.error(exception)
##                logger.print_on_console(exception)
##                err_msg="Unable to perform Mouse Hover"
##        return status,result,verb,err_msg

    def getElementTextByIndex(self, element , parent , input_val , *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            #-----------------------custom element check
            """Following operations need to be performed for custom:
            1.Check is input is > 3
            2.Check if input_val[0] is a tree object type
            3.Check if input type of inputval[2] is an integer
            4.If above conditions are matched then object is a custom object of tree type at position input_val[1] from parent object
            5.Since inputs start from the 4th input_val assign these values to a variable and proceed"""
            if ( len(input_val) > 3 and (input_val[0]).lower()=='tree' and int(input_val[2])==True):
                input_val = input_val[3:]
                log.info('Custom object of type "tree" with input : ' + str(input_val))
            #-------------------------------------------
            if ( desktop_launch_keywords.window_name != None ):
                verify_obj = Text_Box()
                log.info( 'Recieved element from the desktop dispatcher' )
                check = verify_obj.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if( element.is_enabled() ):
                        try:
                            roots = element.roots()
                            root_elem = roots[int(input_val[0]) - 1]
                            if ( len(input_val) > 1 ):
                                input_val = input_val[1:]
                                #------------------------win32
                                if ( element.backend.name == 'win32' ):
                                    new_elem = root_elem
                                    def recur(elem, index):
                                        children = elem.children()
                                        return children[index]
                                    for i in input_val:
                                        index = int(i) - 1
                                        new_elem = recur(new_elem, index)
                                    verb = new_elem.text()
                                    flag = True
                                #------------------------uia
                                elif ( element.backend.name == 'uia' ):
                                    new_elem = root_elem
                                    def recur(elem, index):
                                        if ( elem.is_expanded() == False):
                                            elem.expand()
                                        children = elem.children()
                                        return children[index]
                                    for i in input_val:
                                        index = int(i) - 1
                                        new_elem = recur(new_elem, index)
                                    verb = new_elem.texts()[0]
                                    flag = True
                                if ( flag == True ):
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                            else:
                                if ( element.backend.name == 'win32' ):
                                    verb = root_elem.text()
                                elif ( element.backend.name == 'uia' ):
                                    verb = root_elem.texts()[0]
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                        except Exception as e:
                            log.info(e)
                            log.error(e)
                    else:
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                   err_msg = 'Element not present on the page where operation is trying to be performed'
            if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def right_click_tree_element(self, element , parent , input_val , *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        tree_elm = ''
        path = ''
        counter = 0
        #-----------------------custom element check
        """Following operations need to be performed for custom:
        1.Check is input is > 3
        2.Check if input_val[0] is a tree object type
        3.Check if input type of inputval[2] is an integer
        4.If above conditions are matched then object is a custom object of tree type at position input_val[1] from parent object
        5.Since inputs start from the 4th input_val assign these values to a variable and proceed"""
        if ( len(input_val) > 3 and (input_val[0]).lower()=='tree' and int(input_val[2])==True):
            input_val = input_val[3:]
            log.info('Custom object of type "tree" with input : ' + str(input_val))
        #-------------------------------------------

        if ( len(input_val) == 1 ):
            if ( input_val[0] == '' ):
                flag = True
        
        if ( flag != True ):
            try:
                def iterate_through_tree(element, input_path, path, counter):
                    if element.backend.name == 'win32':
                        tree_element = element.item(path, exact = True)
                        child_elements = tree_element.children()
                        for child in child_elements:
                            if input_path[counter] in child.text():
                                path = path + "\\" + str(child.text())
                                counter = counter + 1
                                break
                        else:
                            return False
                    elif element.backend.name == 'uia':
                        tree_element = element.get_item(path, exact = True)
                        child_elements = tree_element.children()
                        for child in child_elements:
                            if input_path[counter] in child.element_info.name or input_path[counter] in child.element_info.rich_text:
                                path = path + "\\" + str(child.element_info.name or child.element_info.rich_text)
                                counter = counter + 1
                                break
                        else:
                            return False
                        
                    if len(input_path) == counter:
                        return path
                    else:
                        return iterate_through_tree(element, input_path, path, counter)
                    
                if ( desktop_launch_keywords.window_name != None ):
                    verify_obj = Text_Box()
                    log.info( 'Recieved element from the desktop dispatcher' )
                    check = verify_obj.verify_parent(element, parent)
                    log.debug( 'Parent of element while scraping' )
                    log.debug( parent )
                    log.debug( 'Parent check status' )
                    log.debug( check )
                    if ( check ):
                        log.info('Parent matched')
                        if( element.is_enabled() ):
                                if ( element.backend.name == 'win32' ):
                                    root_element = element.roots()
                                    for list_item in root_element:
                                        if input_val[counter] in list_item.text():
                                            path = "\\" + str(list_item.text())
                                            counter = counter + 1
                                            break

                                    if len(path) == 0:
                                        err_msg = 'Element not present on the page where operation is trying to be performed'
                                    else:
                                        tree_path = iterate_through_tree(element, input_val, path, counter)
                                        if tree_path == False:
                                            err_msg = 'Element not present on the page where operation is trying to be performed'
                                        else:
                                            tree_elm = element.item(tree_path, exact = True)
                                            tree_elm.click_input(button = 'right', double = False, wheel_dist = 0, where = 'text', pressed = '')
                                elif ( element.backend.name == 'uia' ):
                                    root_element = element.roots()
                                    for list_item in root_element:
                                        if input_val[counter] in list_item.element_info.name or input_val[counter] in list_item.element_info.rich_text:
                                            path = "\\" + str(list_item.element_info.name or list_item.element_info.rich_text)
                                            counter = counter + 1
                                            break

                                    if len(path) == 0:
                                        err_msg = 'Element not present on the page where operation is trying to be performed'
                                    else:
                                        tree_path = iterate_through_tree(element, input_val, path, counter)
                                        if tree_path == False:
                                            err_msg = 'Element not present on the page where operation is trying to be performed'
                                        else:
                                            tree_elm = element.get_item(tree_path, exact = True)
                                            tree_elm.click_input(button = 'right', double = False, wheel_dist = 0, pressed = '')    
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'Element state does not allow to perform the operation'
                    else:
                       err_msg = 'Element not present on the page where operation is trying to be performed'
                if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
        elif ( flag == True ):
            Rect = ''
            try:
                #----------get the element coordinates
                Rect = str(element.rectangle())
                Rect = Rect[1 : len(Rect) - 1]
                Rect = Rect.split(",")
                Left = Rect[0].strip()#left
                if ( "L" in Left ):
                    Left = int(Left[1:])
                else:
                    Left = int(Left)
                Top = Rect[1].strip()#top
                if ( "T" in Top ):
                    Top = int(Top[1:])
                else:
                    Top = int(Top)
                Right = Rect[2].strip()#right
                if ( "R" in Right ):
                    Right = int(Right[1:])
                else:
                    Right = int(Right)
                Bottom = Rect[3].strip()#bottom
                if ( "B" in Bottom ):
                    Bottom = int(Bottom[1:])
                else:
                    Bottom = int(Bottom)
                #---------------------Finding height and width
                height = Bottom - Top
                width = Right - Left
                #--------------------Finding X and Y co-ordinates
                x = Left + width / 2
                y = Top + height / 2
                pywinauto.mouse.click(button = 'right', coords = (int(x), int(y)))
                status = desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
        return status, result, verb, err_msg