#-------------------------------------------------------------------------------
# Name:        desktop_dropdown_keywords.py
# Purpose:     to handle dropdown,listbox and listview
#
# Author:      kavyasree.l,anas.ahmed
#
# Created:     25-05-2017
# Copyright:   (c) kavyasree.l 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_launch_keywords
import logger
from desktop_editable_text import Text_Box
import desktop_constants
import time
from constants import *
import logging
log = logging.getLogger( 'dropdown_keywords.py' )
class Dropdown_Keywords():
        def selectValueByIndex(self, element, parent, input_val, *args):
            if( len(input_val) > 1 ):
                item_index = int(input_val[3])
            else:
                item_index = int(input_val[0])
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    log.info( 'Recieved element from the desktop dispatcher' )
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element, parent)
                    checkName = element.friendly_class_name()
                    if ( check ):
                        log.info( 'Parent matched' )
                        if( element.is_enabled() ):
                            #------------------------------------------------------------dropdown
                            if ( checkName == 'ComboBox' ):
                                item_count = element.item_count()
                                if ( item_index <= item_count ):
                                    if ( element.is_enabled() ):
                                        if ( element.backend.name == 'win32' ):
                                            selected_index = element.selected_index()
                                        elif ( element.backend.name == 'uia' ):
                                            try:
                                                selected_index = element.selected_index()
                                            except Exception as e:
                                                err_msg = 'SelectValueByIndex returns inconsistent outputs for method B elements, Err Msg : ' +  str(e)
                                                log.error( err_msg )
                                        if ( selected_index == item_index -1 ):
                                            err_msg = 'Combobox with given index is already selected'
                                        else:
                                            if ( item_index <= 0 ):
                                                err_msg = 'Combobox index starts with 1'
                                            else:
                                                element.select(item_index-1)
                                                log.info( 'Combobox item selected' )
                                                logger.print_on_console( 'Combobox item selected' )
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info( STATUS_METHODOUTPUT_UPDATE )
                                    else:
                                        err_msg = 'Element state does not allow to perform the operation'
                                else:
                                    err_msg = 'There is no item in Combobox with the given index'
                            #---------------------------------------------------------------------------List element
                            elif ( checkName == 'ListView' or 'ListBox' ):
                                item_count = element.item_count()
                                if ( item_index <= item_count ):
                                     #----------------------------------------------------ListBox
                                    if ( checkName == 'ListBox' ):
                                        if ( item_index <= 0 ):
                                            err_msg = 'List item index starts with 1'
                                        else:
                                            element.Select(item_index - 1)
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    #----------------------------------------------------ListBox
                                    #----------------------------------------------------ListView
                                    elif ( checkName == 'ListView' ):
                                        item = element.get_item(item_index - 1)
                                        if ( not item.is_selected() ):
                                            if ( element.is_active() == False ):
                                                element.click()
                                            if ( item_index <= 0 ):
                                                err_msg = 'List item index starts with 1'
                                            else:
                                                item.select()
                                                log.info( 'List item selected' )
                                                logger.print_on_console( 'ListView item selected' )
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info( STATUS_METHODOUTPUT_UPDATE )
                                        else:
                                            err_msg = 'List item is already selected'
                                    #----------------------------------------------------ListView
                                else:
                                    err_msg = 'There is no List item in List view with the given index'
                        else:
                            err_msg = 'Element not present on the page where operation is trying to be performed'
                if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg=  desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg

        def getValueByIndex(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            items = []
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element, parent)
               checkName = element.friendly_class_name()
               if ( check ):
                        log.info( 'Parent matched' )
                        #-------------------------------------------------------------------------dropdown
                        if ( checkName == 'ComboBox' ):
                            elelist = element.texts()
                            elelist.pop(0)
                            if ( int(input_val[0]) < 0 ):
                                err_msg = 'Combobox index starts with 1'
                            else:
                                if ( element.backend.name == 'uia' ):
                                    verb = elelist[int(input_val[0]) - 1]
                                    logger.print_on_console('GetValueByIndex returns inconsistent outputs for method B elements')
                                    log.info('GetValueByIndex returns inconsistent outputs for method B elements')
                                elif ( element.backend.name == 'win32' ):
                                    verb = elelist[int(input_val[0]) - 1]
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info( STATUS_METHODOUTPUT_UPDATE )
                        #====================================================================ListView and ListBox
                        elif ( checkName == 'ListView' or 'ListBox' ):
                            index = int(input_val[0]) - 1
                            if ( index >= 0 ):
                                if ( checkName == 'ListBox' ):
                                    items = element.item_texts()
                                    verb = items[index]
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                elif ( checkName == 'ListView' ):
                                    #---------------------------------------------checker(32 or 64)
                                    import platform
                                    info_32 = platform.architecture()
                                    if ( info_32[0] == '32bit' ):
                                        logger.print_on_console( 'Warning : You are using 32bit version of Avo Assure Client Engine.This keyword is unstable for this version.If unsatisfactory results, use 64bit Avo Assure Client Engine.')
                                    #---------------------------------------------
##                                    if element.is_active() == False:
##                                      element.click()
                                    items = list(element.items())
                                    cols = element.column_count()
                                    elelist = element.texts()
                                    elelist.pop(0)
                                    oldlist = len(items)
                                    itemcount = element.item_count()
                                    newlist = []
                                    list_input = input_val
                                    item_list = []
                                    for item in list_input:
                                        #logger.print_on_console(item)
                                        item_new = (int(item) - 1) * 2
                                        #logger.print_on_console(item_new)
                                        item_list.append(item_new)
                                    val = ''
                                    res = ''
                                    for i in range(0, len(item_list)):
                                        if ( cols == 1 ):
                                         val = item_list[i]
                                         res = elelist[int(val)]
                                        else:
                                         val = item_list[i]
                                         res1 = elelist[int(val)]
                                         res2 = elelist[int(val) + 1]
                                         newlist.append(res1)
                                         newlist.append(res2)
                                    if ( cols == 1 ):
                                        verb = newlist
                                    else:
                                        verb = self.multiListGetter(cols, elelist, input_val)
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info( STATUS_METHODOUTPUT_UPDATE )

                            else:
                                logger.print_on_console( 'Index value index starts with 1' )
                        #========================================================================
               else:
                    err_msg = 'Element not present on the page where operation is trying to be performed'
               if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg

        def getCount(self, element, parent, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            output = None
            err_msg = None
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    log.info( 'Recieved element from the desktop dispatcher' )
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element, parent)
                    log.debug( 'Parent of element while scraping' )
                    log.debug( parent )
                    log.debug( 'Parent check status' )
                    log.debug( check )
                    if ( check ):
                        log.info( 'Parent matched' )
                        if ( element.friendly_class_name() == 'ListView' or 'ListBox' ):
                            if ( element.is_active() == False ):
                                if ( element.backend.name == 'win32' ):
                                    element.click()
                                elif ( element.backend.name == 'uia' ):
                                    pass
                            if ( element.backend.name == 'uia' and element.friendly_class_name() == 'ListBox' ):
                                verb = len(element.get_items())
                            else:
                                verb = int(element.item_count())
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info( STATUS_METHODOUTPUT_UPDATE )
                        elif ( element.friendly_class_name() == 'ComboBox' ):
                            verb = int(element.item_count())
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info( STATUS_METHODOUTPUT_UPDATE )
                    else:
                        err_msg = 'Element not present on the page where operation is trying to be performed'
                        log.info( err_msg )
                        logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg

        def verifyCount(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    log.info( 'Recieved element from the desktop dispatcher' )
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element, parent)
                    log.debug( 'Parent of element while scraping' )
                    log.debug( parent )
                    log.debug( 'Parent check status' )
                    log.debug( check )
                    if ( check ):
                        log.info( 'Parent matched' )
                        if ( element.friendly_class_name() == 'ListView' or 'ListBox' ):
                            if ( element.is_active() == False ):
                               if ( element.backend.name == 'win32' ):
                                    element.click()
                               elif ( element.backend.name == 'uia' ):
                                    pass
                            if ( element.backend.name == 'uia' and element.friendly_class_name() == 'ListBox' ):
                                count = len(element.get_items())
                            else:
                                count = element.item_count()
                            if ( count == int(input_val[0]) ):
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info( STATUS_METHODOUTPUT_UPDATE )
                            else:
                                err_msg = 'Count mismatched'
                                logger.print_on_console( err_msg )
                                log.info( err_msg )
                        elif ( element.friendly_class_name() == 'ComboBox' ):
                            count = element.item_count()
                            if ( count == int(input_val[0]) ):
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info( STATUS_METHODOUTPUT_UPDATE )
                            else:
                                err_msg = 'Count mismatched'
                                logger.print_on_console( err_msg )
                                log.info( err_msg )
                    else:
                        err_msg = 'Element not present on the page where operation is trying to be performed'
                        log.info( err_msg )
                        logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg

        def getSelected(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            flag = False
            err_msg = None
            items = []
            checkName = ""
            try:
               checkName = element.friendly_class_name()
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               if ( check ):
                        log.info( 'Parent matched' )
                        if ( checkName.strip() == 'ComboBox' ):
                            try:
                                if ( element.backend.name == 'uia' ):
                                    try:
                                        verb = element.selected_text()
                                        flag = True
                                    except Exception as e:
                                        err_msg = 'GetSelected returns inconsistent outputs for method B elements. Err Msg : ' + str(e)
                                        log.error( err_msg )
                                elif ( element.backend.name == 'win32' ):
                                    verb = element.selected_text()
                                    flag = True
                                if ( flag == True ):
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                            except Exception as e :
                                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                                log.error( err_msg )
                        elif ( checkName == 'ListView' or 'ListBox' ):
                            if ( checkName == 'ListBox' ):
                                if ( element.is_active() == False ):
                                    if ( element.backend.name == 'win32' ):
                                        element.click()
                                if ( element.backend.name == 'uia' ):
                                        item = element.get_items()
                                        items = []
                                        for i in item:
                                            if ( type(i.texts()) == list ):
                                                items.append(i.texts()[0])
                                            else:
                                                items.append(i.texts())
                                elif ( element.backend.name == 'win32' ):
                                    items = element.item_texts()
                                newlist=[]
                                if ( element.backend.name == 'win32' ):
                                    if ( element.is_single_selection() == True ):
                                        logger.print_on_console( 'List is a single selection type.' )
                                    n=element.selected_indices()
                                    for i in range(0, len(n)):
                                        idindex = None
                                        idindex = int(n[i])
                                        newlist = items[idindex]
                                    flag = True
                                elif ( element.backend.name == 'uia' ):
                                    try:
                                        for i in range(0, len(item)):
                                            if ( item[i].is_checked() == True ):
                                                newlist.append(items[i])
                                        flag = True
                                    except Exception as e:
                                        err_msg = 'GetSelected returns inconsistent outputs for method B elements. Err Msg : ' + str(e)
                                        log.error( err_msg )
                                if ( flag == True ):
                                    verb = newlist
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info( STATUS_METHODOUTPUT_UPDATE )
                            elif ( checkName == 'ListView' ):
                                if ( element.is_active() == False ):
                                    if ( element.backend.name == 'win32' ):
                                        element.click()
                                items = list(element.items())
                                elelist = element.texts()
                                elelist.pop(0)
                                itemcount = element.item_count()
                                newlist = []
                                for i in range(0, len(items)):
                                     if ( items[i].is_selected() ):
                                       newlist.append(elelist[i])
                                verb = newlist
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info( STATUS_METHODOUTPUT_UPDATE )
                        #=========================================================
               else:
                   err_msg = 'Element not present on the page where operation is trying to be performed'
               if ( err_msg ):
                   log.info( err_msg )
                   logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg

        def verifySelected(self, element, parent, input_val, *args):
                status = desktop_constants.TEST_RESULT_FAIL
                result = desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                flag = True
                err_msg = None
                try:
                   checkName = element.friendly_class_name()
                   dektop_element = element
                   verify_obj = Text_Box()
                   check = verify_obj.verify_parent(element, parent)
                   log.debug( 'Parent of element while scraping' )
                   log.debug( parent )
                   log.debug( 'Parent check status' )
                   log.debug( check )
                   if ( check ):
                            log.info('Parent matched')
                            if ( checkName == 'ComboBox' ):
                                if ( element.backend.name == 'uia' ):
                                    try:
                                        verb = element.selected_text()
                                    except Exception as e:
                                        err_msg = 'VerifySelectedValue returns inconsistent outputs for method B elements. Err Msg : ' + str(e)
                                        log.error( err_msg )
                                elif ( element.backend.name == 'win32' ):
                                    verb = element.selected_text()
                                if ( input_val[0] == verb ):
                                   status = desktop_constants.TEST_RESULT_PASS
                                   result = desktop_constants.TEST_RESULT_TRUE
                                   verb = OUTPUT_CONSTANT
                                else:
                                  verb = OUTPUT_CONSTANT
                                  err_msg = 'Failed to verify selected value'
                            #================================================================
                            elif ( checkName == 'ListView' or 'ListBox' ):
                                if ( element.is_active() == False ):
                                    element.click()
                                if ( checkName == 'ListBox' ):
                                    if element.is_active() == False:
                                      element.click()
                                    items = element.item_texts()
                                    elelist = element.texts()
                                    elelist.pop(0)
                                    oldlist = len(items)
                                    itemcount = element.item_count()
                                    newlist = []
                                    if ( element.is_single_selection() == True ):
                                        logger.print_on_console( 'List is a single selection type.' )
                                    n = element.selected_indices()
                                    for i in range(0, len(n)):
                                        idindex = None
                                        idindex = int(n[i])
                                        newlist = items[idindex]
                                    #newitems=[item.encode("utf-8") for item in items]
                                    verb = newlist
                                    item_list=input_val
                                    for item in item_list:
                                        if ( item not in verb ):
                                            flag = False
                                            err_msg = 'Failed to verify selected value'
                                            verb=OUTPUT_CONSTANT
                                            break
                                    if (flag == True):
                                        status = desktop_constants.TEST_RESULT_PASS
                                        result = desktop_constants.TEST_RESULT_TRUE
                                        verb=OUTPUT_CONSTANT
                                if ( checkName == 'ListView' ):
                                    items = list(element.items())
                                    elelist = element.texts()
                                    elelist.pop(0)
                                    oldlist = len(elelist)
                                    #cols=element.column_count()
                                    #res=oldlist/cols
                                    itemcount = element.item_count()
                                    newlist = []
                                    for i in range(0, len(items)):
                                         if ( items[i].is_selected() ):
                                           selected = element.item(i, subitem_index = 0)
                                           newlist.append(elelist[i])
                                    item_list = input_val
                                    for item in item_list:
                                        if ( item not in newlist ):
                                            flag = False
                                            err_msg = 'Failed to verify selected value'
                                            verb=OUTPUT_CONSTANT
                                            break
                                    if (flag == True):
                                        status = desktop_constants.TEST_RESULT_PASS
                                        result = desktop_constants.TEST_RESULT_TRUE
                                        verb=OUTPUT_CONSTANT
                            #================================================================
                   else:
                       err_msg = 'Element not present on the page where operation is trying to be performed'
                   if ( err_msg ):
                       log.info( err_msg )
                       logger.print_on_console( err_msg )
                except Exception as exception:
                    err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                    log.error( err_msg )
                    logger.print_on_console( err_msg )
                return status, result, verb, err_msg

        def selectValueByText(self, element, parent, input_val, *args):
            if ( len(input_val) > 1 ):
                text = input_val[3]
            else:
                text = input_val[0]
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            text_flag = False
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    log.info( 'Recieved element from the desktop dispatcher' )
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element, parent)
                    checkName = element.friendly_class_name()
                    if ( check ):
                        log.info( 'Parent matched' )
                        if ( element.is_enabled() ):
                            item_text = str(text)
                            #----------------------------------------------------------------------------------------dropdown
                            if ( checkName == 'ComboBox' ):
                                if ( item_text != '' or item_text != None ):
                                    if ( element.is_enabled() ):
                                        if ( element.backend.name == 'win32' ):
                                            selected_text = element.selected_text()
                                        elif ( element.backend.name == 'uia' ):
                                            try:
                                                selected_text = element.selected_text()
                                            except Exception as e:
                                                err_msg = 'SelectValueByText returns inconsistent outputs for method B elements.Err Msg : ' + str(e)
                                                log.error( err_msg )
                                        if ( selected_text == item_text ):
                                            err_msg = 'Combobox with given text is already selected'
                                        else:
                                            try:
                                                element.select(item_text)
                                                log.info( 'Combobox item selected' )
                                                #logger.print_on_console('Combobox item selected')
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info( STATUS_METHODOUTPUT_UPDATE )
                                            except Exception as e:
                                                err_msg = 'There is no item in Combobox with the given text'
                                    else:
                                        err_msg = 'Element state does not allow to perform the operation'
                                else:
                                    err_msg = 'There is no item in Combobox with the given text'
                            #==============================================================================
                            elif ( checkName == 'ListView' or 'ListBox' ):
                                if ( checkName == 'ListBox' ):
                                    if ( item_text != '' or item_text != None ):
                                        items = element.item_texts()
                                        for i in range(0, len(items)):
                                            if ( item_text == str(items[i]) ):
                                                try:
                                                    element.Select(item_text)
                                                    status = desktop_constants.TEST_RESULT_PASS
                                                    result = desktop_constants.TEST_RESULT_TRUE
                                                    log.info( STATUS_METHODOUTPUT_UPDATE )
                                                except Exception as e:
                                                    err_msg = 'There is no item in List with the given text. Err Msg : ' + str(e)
                                                    log.error( err_msg )

                                elif ( checkName == 'ListView' ):
                                    if ( item_text != '' or item_text != None ):
                                        try:
                                            item = element.get_item(item_text)
                                        except:
                                            text_flag = True
                                        if ( text_flag == False ):
                                            if ( not item.is_selected() ):
                                                if ( element.is_active() == False ):
                                                    element.click()
                                                item.select()
                                                log.info( 'List item selected' )
                                                logger.print_on_console( 'List item selected' )
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info( STATUS_METHODOUTPUT_UPDATE )
                                            else:
                                                err_msg = 'List item is already selected'
                                        else:
                                            err_msg = 'There is no List item in List view with the given text'
                                else:
                                    err_msg = 'There is no List item in List view with the given text'
                            #==============================================================================
                        else:
                            err_msg = 'Element not present on the page where operation is trying to be performed'
                if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg

        def getAllValues(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            err_msg = None
            dektop_element = []
            checkName = None
            try:
                if ( input_val[0] == 'dropdown' and int(input_val[1]) == True ):
                    input_val = input_val[3:]
            except :
                pass
            try:
                if (element is not None ):
                    checkName = element.friendly_class_name()
                    dektop_element = element.texts()
                    opt_len = len(dektop_element)
                    output = []
                    if (checkName == 'ComboBox' or checkName == 'ListView' or checkName == 'ListBox'):
                        for x in range(1,opt_len):
                            internal_val = dektop_element[x]
                            output.append(internal_val)
                    if(len(output) != 0 ):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                else:
                    err_msg='No Desktop element found'
                    log.error(err_msg)
                    logger.print_on_console(err_msg)
            except Exception as e:
                log.error(e)
                logger.print_on_console(e)
            return status, result, output, err_msg

        def verifyAllValues(self, element, parent, input_val, *args):
            try:
                if ( input_val[0] == 'dropdown' and int(input_val[2]) == True ):         #to check is object is custom dropdown
                    input_val = input_val[3:]                                #if custom then populate list from 4th element
            except :
                pass
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            items = []
            checkName = None
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               checkName = element.friendly_class_name()
               if ( check ):
                        log.info( 'Parent matched' )
                        if ( checkName == 'ComboBox' ):
                            items = element.texts()
                            items.pop(0)
                            if ( input_val == items ):
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = 'Failed to verify values'
                                log.info( err_msg )
                                logger.print_on_console( err_msg )
                        #==================================================================
                        elif ( checkName == 'ListView' or 'ListBox' ):
                             if ( checkName == 'ListBox' ):
                                items = element.item_texts()
                                if ( items == input_val ):
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                             elif ( checkName == 'ListView' ):
                                items = element.texts()
                                items.pop(0)
                                #----------------------------remove characters from input
                                input_val = [i.replace('\\\\','\\') for i in input_val]
                                #----------------------------remove characters from input
                                if ( input_val == items ):
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                else:
                                    err_msg = 'Failed to verify values'
                                    log.info( err_msg )
                                    logger.print_on_console( err_msg )
                        #==================================================================
               else:
                   err_msg = 'Element not present on the page where operation is trying to be performed'
                   log.info( err_msg )
                   logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg


        def verifyValuesExists(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            items = []
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element, parent)
               checkName = element.friendly_class_name()
               if (check):
                    log.info( 'Parent matched' )
                    if ( checkName == 'ComboBox' ):
                        items = element.texts()
                        items.pop(0)
                        flag = True
                        for i in range(0, len(input_val)):
                            if ( input_val[i] not in items ):
                                flag = False
                                break

                        if ( flag == True ):
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'Given Value does not exist in the list'
                            log.info( err_msg )
                            logger.print_on_console( err_msg )
                    #==============================================================
                    elif ( checkName == 'ListView' or 'ListBox' ):
                        if ( checkName == 'ListBox' ):
                            fail_flag = False #will set to true if item is not apart of original list,if set to true result is set to fail
                            items = element.item_texts()
                            newlist = []
                            newlist = [item for item in items] #removing unicode
                            #items_list=input_val
                            for i in range(0, len(input_val)):
                                if ( input_val[i] not in newlist ):
                                    fail_flag = True
                                    break
                            if ( fail_flag == False ):
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = 'Given Value does not exist in the list'
                                log.info( err_msg )
                                logger.print_on_console( err_msg )

                        if ( checkName == 'ListView' ):
                             flag = False
                             itemtextlist = []
                             items = list(element.items())
                             for i in items: itemtextlist.append(i.text())
                             for ele in input_val:
                                if (ele not in itemtextlist):
                                    flag = True
                                    break
                             if(flag == False):
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                             else:
                                err_msg = 'Given Value does not exist in the list'
                                log.info( err_msg )
                                logger.print_on_console( err_msg )
                    #=================================================================
               else:
                   err_msg = 'Element not present on the page where operation is trying to be performed'
                   log.info( err_msg )
                   logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg

        def selectAllValues(self, element, parent, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element, parent)
               log.debug( 'Parent of element while scraping' )
               log.debug( parent )
               log.debug( 'Parent check status' )
               log.debug( check )
               if ( check ):
                        log.info( 'Parent matched' )
                        if ( element.is_enabled() ):
                            #============================================================================
                            if ( element.friendly_class_name() == 'ListView' or 'ListBox' ):
                                if ( element.friendly_class_name() == 'ListBox' ):
                                    fail_flag = False
                                    if ( element.is_single_selection() != True ):
                                        if ( element.is_active() == False ):
                                            element.click()
                                        items = element.item_texts()
                                        for item in range(0, len(items)):
                                            try:
                                                element.select(item)
                                            except:
                                                fail_flag = True
                                        if ( fail_flag == False ):
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        err_msg = 'List is a single selection type.Could not select all values'
                                elif ( element.friendly_class_name() == 'ListView' ):
                                     if ( element.is_active() == False ):
                                        element.click()
                                     items = list(element.items())
                                     for i in range(0, len(items)):
                                          items[i].select()
                                          status = desktop_constants.TEST_RESULT_PASS
                                          result = desktop_constants.TEST_RESULT_TRUE
                            #============================================================================
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
            return status, result, verb, err_msg

        def deSelectAll(self, element, parent, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element, parent)
               log.debug( 'Parent of element while scraping' )
               log.debug( parent )
               log.debug( 'Parent check status' )
               log.debug( check )
               if ( check ):
                        log.info( 'Parent matched' )
                        if( element.is_enabled() ):
                            #===============================================================
                            if ( element.friendly_class_name() == 'ListView' or 'ListBox' ):
                                if ( element.friendly_class_name() == 'ListBox' ):
                                    items = element.item_texts()
                                    fail_flag = False
                                    if ( element.is_single_selection() != True):#to check if the ListBox is a singleSelection type
                                        for item in range(0, len(items)):
                                            try:
                                                element.select(item, select = False)
                                            except:
                                                fail_flag = True
                                        if ( fail_flag == False ):
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        err_msg = 'Element state does not allow to perform the operation'
                                elif ( element.friendly_class_name() == 'ListView' ):
                                     if ( element.is_active() == False ):
                                        element.click()
                                     items = list(element.items())
                                     for i in range(0,len(items)):
                                         items[i].deselect()
                                         status = desktop_constants.TEST_RESULT_PASS
                                         result = desktop_constants.TEST_RESULT_TRUE
                            #===============================================================
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
            return status, result, verb, err_msg


        def getMultpleValuesByIndexs(self,element,parent,input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            items = []
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element, parent)
               log.debug( 'Parent of element while scraping' )
               log.debug( parent )
               log.debug( 'Parent check status' )
               log.debug( check )
               if ( check ):
                        log.info( 'Parent matched' )
                        #=================================================================================
                        if ( element.friendly_class_name() == 'ListView' or 'ListBox' ):
                            if ( element.friendly_class_name() == 'ListBox' ):
                                false_flag = False
                                if ( element.is_active() == False ):
                                  element.click()
                                input_list = input_val
                                ilist = []
                                newlist = []
                                verbList = []
                                for x in range(0, len(input_list)):
                                    ilist.append(int(input_list[x]) - 1)
                                items = element.item_texts()
                                newlist = [item for item in items]#removing unicode
                                for i in range(len(ilist)):
                                    index = None
                                    index = int(ilist[i])
                                    if ( index < 0 or index >= len(items) ):
                                        verbList.append("No Value")
                                        false_flag = True
                                    else:
                                        verbList.append(items[index])
                                verb = [nitem for nitem in verbList]
                                if ( false_flag == False ):
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info( STATUS_METHODOUTPUT_UPDATE )
                            if ( element.friendly_class_name() == 'ListView' ):
                                #---------------------------------------------checker(32 or 64)
                                import platform
                                info_32=platform.architecture()
                                if ( info_32[0] == '32bit' ):
                                    logger.print_on_console( 'Warning : You are using 32bit version of Avo Assure Client Engine.This keyword is unstable for this version.If unsatisfactory results, use 64bit Avo Assure Client Engine.' )
                                #---------------------------------------------
                                if ( element.is_active() == False ):
                                  element.click()
                                items = list(element.items())
                                cols = element.column_count()
                                elelist = element.texts()
                                elelist.pop(0)
                                oldlist = len(items)
                                itemcount = element.item_count()
                                newlist = []
                                list_input = input_val
                                item_list = []
                                for item in list_input:
                                    item_new = (int(item) - 1) * 2
                                    item_list.append(item_new)
                                val=''
                                res=''
                                for i in range(0, len(item_list)):
                                    if ( cols == 1 ):
                                        val = item_list[i]
                                        res = elelist[int(val)]
                                    else:
                                        val = item_list[i]
                                        res1 = elelist[int(val)]
                                        res2 = elelist[int(val) + 1]
                                        newlist.append(res1)
                                        newlist.append(res2)
                                if ( cols == 1 ):
                                    verb = newlist
                                else:
                                    verb=self.multiListGetter(cols, elelist, input_val)
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info( STATUS_METHODOUTPUT_UPDATE )
                        #=================================================================================

                        elif ( element.friendly_class_name() == 'ComboBox' ):
                            selected = element.selected_text()
                            verb = selected
                            logger.print_on_console('Values obtained are : ', verb)
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info( STATUS_METHODOUTPUT_UPDATE )
               else:
                    err_msg = 'Element not present on the page where operation is trying to be performed'
               if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg


        def selectMultpleValuesByIndexs(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    log.info( 'Recieved element from the desktop dispatcher' )
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element, parent)
                    log.debug( 'Parent of element while scraping' )
                    log.debug( parent )
                    log.debug( 'Parent check status' )
                    log.debug(check)
                    if ( check ):
                        log.info( 'Parent matched' )
                        if ( element.is_enabled() ):
                            item_index = input_val
                            #====================================================================================
                            if ( element.friendly_class_name() == 'ListView' or 'ListBox' ):
                                if ( element.friendly_class_name() == 'ListBox' ):
                                    fail_flag = False
                                    if ( element.is_single_selection() != True ):
                                        if ( element.is_active() == False ):
                                           element.click()
                                        ilist = []
                                        items = element.item_texts()
                                        for x in range(0, len(item_index)):
                                            ilist.append(int(item_index[x]) - 1)
                                        for i in range(len(ilist)):
                                            index = None
                                            index = int(ilist[i])
                                            if ( index < 0 or index >= len(items) ):
                                                fail_flag = True
                                            else:
                                                element.Select(index)
                                        if ( fail_flag == False ):
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        err_msg = 'List is a single selection type. Could not select all values'
                                elif ( element.friendly_class_name() == 'ListView' ):
                                    item_count = element.item_count()
                                    items = list(element.items())
                                    for i in range(0, len(items)):
                                        items[i].deselect()
                                    for i in range(0, len(item_index)):
                                      if ( int(item_index[i]) <= item_count ):
                                         item = element.get_item(int(item_index[i]) - 1)
                                         if ( not item.is_selected() ):
                                            if ( element.is_active() == False ):
                                                element.click()
                                            if ( int(item_index[i]) <= 0 ):
                                                err_msg = 'List item index starts with 1'
                                            else:
                                                item.select()
                                                log.info( 'List item selected' )
                                                logger.print_on_console( 'List item selected' )
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info( STATUS_METHODOUTPUT_UPDATE )
                                         else:
                                            err_msg = 'List item is already selected'
                                      else:
                                        err_msg = 'There is no List item in List view with the given index'
                            #====================================================================================
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
            return status, result, verb, err_msg


        def selectMultpleValuesByText(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            pass_flag = True
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    log.info( 'Recieved element from the desktop dispatcher' )
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element,parent)
                    checkName = element.friendly_class_name()
                    if ( check ):
                        log.info( 'Parent matched' )
                        if ( element.is_enabled() ):
                            item_text = input_val
                            if ( checkName == 'ListView' ):
                                items = list(element.items())
                                elelist = element.texts()
                                new_elelist = []
                                for i in range(0, len(elelist)):
                                    new_elelist.append(elelist[i].encode("utf-8")) #to remove special characters
                                new_elelist = [bytearray(x).decode('ascii') for x in new_elelist]
                        #=======================================================================================================
                            if ( checkName == 'ListView' or 'ListBox' ):
                                if ( checkName == 'ListBox' ):
                                    fail_flag = False
                                    if ( element.is_single_selection() != True ):
                                        newlist = []
                                        items = element.item_texts()
                                        newlist = [item for item in items]#removing unicode
                                        for i in range(len(item_text)):
                                            if ( item_text[i] not in newlist ):
                                                fail_flag=True
                                        if ( fail_flag == False ):
                                            for i in range(len(item_text)):
                                                element.Select(item_text[i])
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        err_msg = 'List is a single selection type.Could not select all values'
                                elif ( checkName == 'ListView' ):
                                    item_count = element.item_count()
                                    items = list(element.items())
                                    for i in range(0,len(items)):
                                                      items[i].deselect()
                                    for i in range(0, len(item_text)):
                                        if ( item_text[i] in new_elelist ):
                                             itemtext = element.get_item(item_text[i])
                                             if ( not itemtext.is_selected() ):
                                                if ( element.is_active() == False ):
                                                    element.click()
                                                itemtext.select()
                                                log.info(STATUS_METHODOUTPUT_UPDATE)
                                             else:
                                                err_msg = 'List item is already selected'
                                        else:
                                            pass_flag = False
                                    if ( pass_flag == True ):
                                        status = desktop_constants.TEST_RESULT_PASS
                                        result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        for i in range(0, len(items)):
                                            items[i].deselect()
                                        err_msg = 'Element/Elements not present on the page where operation is trying to be performed'
                            #=======================================================================================================

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
            return status, result, verb, err_msg

        def multiListGetter(self, cols, elelist, input_val):
            rows=int(len(elelist) / cols)
            #-------------------------------------------------creating a 2D list
            Matrix = [[0 for x in range(cols)] for y in range(rows)]
            #-------------------------------------------------creating a 2D list
            #-------------------------------------------------populating the 2D list
            index_i = 0
            for j in range(0, rows):
                for k in range (0, cols):
                    try:
                        Matrix[j][k] = elelist[index_i]
                        index_i = index_i + 1
                    except Exception as e:
                        logger.print_on_console( "Error occoured in populating the 2D matrix" )
                        log.error( "Error occoured in populating the 2D matrix" )
                        log.error( e )
            #-------------------------------------------------populating the 2D list
            #-------------------------------------------------creating new Matrix based on indexes given
            NewMatrix = [[0 for x in range(cols)] for y in range(len(input_val))]
            #-------------------------------------------------creating new Matrix based on indexes given
            #-------------------------------------------------poulating the new martix
            new_input_val = []
            for z in range(0, len(input_val)):
                new_input_val.append(str(int(input_val[z]) - 1))
            try:
                r = 0
                for nr in new_input_val:
                    rowindex = int(nr)
                    for c in range(0, cols):
                        NewMatrix[r][c] = Matrix[rowindex][c]
                    r = r + 1
            except Exception as e:
                log.error( e )
            #-------------------------------------------------poulating the new martix
            return NewMatrix