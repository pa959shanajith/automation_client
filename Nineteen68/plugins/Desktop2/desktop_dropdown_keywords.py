#-------------------------------------------------------------------------------
# Name:        desktop_dropdown_keywords.py
# Purpose:
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
import desktop_editable_text
import time
from constants import *
#editable_text=desktop_editable_text.Text_Box()
import logging
log = logging.getLogger('dropdown_keywords.py')
class Dropdown_Keywords():

        def selectValueByIndex(self,element,parent,input_val, *args):
            if(len(input_val)>1):
                text = input_val[2]
            else:
                text=input_val[0]
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            try:
                if desktop_launch_keywords.window_name!=None:
                    log.info('Recieved element from the desktop dispatcher')
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element,parent)
                    checkName =element.friendly_class_name()
                    if (check):
                        log.info('Parent matched')
                        if(element.is_enabled()):
                            item_index=int(text)
                            #------------------------------------------------------------dropdown
                            if checkName == 'ComboBox':
                                item_count = element.item_count()
                                if item_index <= item_count:
                                    if element.is_enabled():
                                        selected_index = element.selected_index()
                                        if selected_index == item_index -1:
                                            log.info('Combobox with given index is already selected')
                                            logger.print_on_console('Combobox with given index is already selected')
                                            err_msg = 'Combobox with given index is already selected'
                                        else:
                                            if item_index <=0:
                                                log.info('Combobox index starts with 1')
                                                logger.print_on_console('Combobox index starts with 1')
                                                err_msg = 'Combobox index starts with 1'
                                            else:
                                                element.select(item_index-1)
                                                log.info('Combobox item selected')
                                                logger.print_on_console('Combobox item selected')
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info(STATUS_METHODOUTPUT_UPDATE)
                                    else:
                                        log.info('Element state does not allow to perform the operation')
                                        logger.print_on_console('Element state does not allow to perform the operation')
                                        err_msg = 'Element state does not allow to perform the operation'
                                else:
                                    log.info('There is no item in Combobox with the given index')
                                    logger.print_on_console('There is no item in Combobox with the given index')
                                    err_msg = 'There is no item in Combobox with the given index'
                            #---------------------------------------------------------------------------List element
                            elif checkName == 'ListView' or 'ListBox':
                                item_count = element.item_count()
                                if item_index <= item_count:
                                     #----------------------------------------------------ListBox
                                    if checkName == 'ListBox':
                                        if item_index <=0:
                                                log.info('List item index starts with 1')
                                                logger.print_on_console('List item index starts with 1')
                                        else:
                                            element.Select(item_index-1)
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    #----------------------------------------------------ListBox
                                    #----------------------------------------------------ListView
                                    elif checkName == 'ListView':
                                        item = element.GetItem(item_index-1)
                                        if not item.is_selected():
                                            if element.is_active() == False:
                                                element.click()
                                            if item_index <=0:
                                                log.info('List item index starts with 1')
                                                logger.print_on_console('List item index starts with 1')
                                            else:
                                                item.select()
                                                log.info('List item selected')
                                                logger.print_on_console('ListView item selected')
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info(STATUS_METHODOUTPUT_UPDATE)

                                        else:
                                            log.info('List item is already selected')
                                            logger.print_on_console('List item is already selected')
                                            err_msg = 'List item is already selected'
                                    #----------------------------------------------------ListView

                                else:
                                    log.info('There is no List item in List view with the given index')
                                    logger.print_on_console('There is no List item in List view with the given index')
                                    err_msg = 'There is no List item in List view with the given index'


                        else:
                            log.info('Element not present on the page where operation is trying to be performed')
                            err_msg='Element not present on the page where operation is trying to be performed'
                            logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)
            return status,result,verb,err_msg

        def getValueByIndex(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            items=[]
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               checkName =element.friendly_class_name()
               if (check):
                        log.info('Parent matched')
                        #-------------------------------------------------------------------------dropdown
                        if checkName == 'ComboBox':
                            elelist=element.texts()
                            elelist.pop(0)
                            newlist=[]
                            index=input_val
                            res1=[]
                            if int(index[0])<0:
                                log.info('Combobox index starts with 1')
                                logger.print_on_console('Combobox index starts with 1')
                                err_msg = 'Combobox index starts with 1'
                            else:
                                res1=elelist[int(index[0])-1]
                                verb=res1
                                logger.print_on_console('Value obtained is',verb)
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                        #====================================================================ListView and ListBox
                        elif checkName == 'ListView' or 'ListBox':
                            index=int(input_val[0])-1
                            if index>=0:
                                if checkName=='ListBox':
                                    items=element.ItemTexts()
                                    verb =items[index]
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE

                                elif checkName=='ListView':
                                    #---------------------------------------------checker(32 or 64)
                                    import platform
                                    info_32=platform.architecture()
                                    if info_32[0]=='32bit':
                                        logger.print_on_console('Warning:You are using 32bit version of ICE Engine.This keyword is unstable for this version.If unsatisfactory results, use 64bit ICE Engine.')
                                    #---------------------------------------------
##                                    if element.is_active() == False:
##                                      element.click()
                                    items=element.items()
                                    cols=element.column_count()
                                    elelist=element.texts()
                                    elelist.pop(0)
                                    oldlist=len(items)
                                    itemcount=element.item_count()
                                    newlist=[]
                                    list = input_val
                                    item_list=[]
                                    for item in list:
                                        #logger.print_on_console(item)
                                        item_new = (int(item)-1)*2
                                        #logger.print_on_console(item_new)
                                        item_list.append(item_new)
                                    val=''
                                    res=''
                                    for i in range(0,len(item_list)):
                                        if(cols==1):
                                         val=item_list[i]
                                         res=elelist[int(val)]
                                        else:

                                         val=item_list[i]
                                         res1=elelist[int(val)]
                                         res2=elelist[int(val) + 1]
                                         newlist.append(res1.encode("utf-8"))
                                         newlist.append(res2.encode("utf-8"))
                                    if cols==1:
                                        verb=newlist
                                    else:
                                        verb=self.multiListGetter(cols,elelist,input_val)
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)

                            else:
                                logger.print_on_console('Index value index starts with 1')
                        #========================================================================


               else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
            except Exception as exception:
                import traceback
                traceback.print_exc()
                log.error(exception)
                logger.print_on_console(exception)


            return status,result,verb,err_msg

        def getCount(self,element,parent, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            output=None
            err_msg=None
            try:
                if desktop_launch_keywords.window_name!=None:
                    log.info('Recieved element from the desktop dispatcher')
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element,parent)
                    log.debug('Parent of element while scraping')
                    log.debug(parent)
                    log.debug('Parent check status')
                    log.debug(check)
                    if (check):
                        log.info('Parent matched')
                        if element.friendly_class_name() == 'ListView' or 'ListBox':
                            if element.is_active() == False:
                               element.click()
                            val=element.texts()
                            verb1 = element.item_count()
                            verb=int(verb1)
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                        elif element.friendly_class_name() == 'ComboBox':
                            verb1 = element.item_count()
                            verb=int(verb1)
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)

                    else:
                      log.info('Element not present on the page where operation is trying to be performed')
                      err_msg='Element not present on the page where operation is trying to be performed'
                      print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)
            return status,result,verb,err_msg

        def verifyCount(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            output=None
            err_msg=None
            try:
                if desktop_launch_keywords.window_name!=None:
                    log.info('Recieved element from the desktop dispatcher')
                    dektop_element = element
                    input_val[0]=int(input_val[0])
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element,parent)
                    log.debug('Parent of element while scraping')
                    log.debug(parent)
                    log.debug('Parent check status')
                    log.debug(check)
                    if (check):
                        log.info('Parent matched')
                        if element.friendly_class_name() == 'ListView' or 'ListBox':
                            if element.is_active() == False:
                               element.click()
                            val=element.texts()
                            count = element.item_count()
                            if(count == input_val[0]):
                             status = desktop_constants.TEST_RESULT_PASS
                             result = desktop_constants.TEST_RESULT_TRUE
                             log.info(STATUS_METHODOUTPUT_UPDATE)
                        elif element.friendly_class_name() == 'ComboBox':
                            count = element.item_count()
                            if(count == input_val[0]):
                             status = desktop_constants.TEST_RESULT_PASS
                             result = desktop_constants.TEST_RESULT_TRUE
                             log.info(STATUS_METHODOUTPUT_UPDATE)

                    else:
                      log.info('Element not present on the page where operation is trying to be performed')
                      err_msg='Element not present on the page where operation is trying to be performed'
                      print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)

            return status,result,verb,err_msg


        def getSelected(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            items=[]
            checkName=""
            try:
               checkName =element.friendly_class_name()
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               if (check):
                        log.info('Parent matched')
                        if checkName.strip() == 'ComboBox':
                            try:
                                selected=element.selected_text()
                                verb=selected
                                logger.print_on_console('selected values are:',verb)
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            except Exception as e :
                                logger.print_on_console(e)
                        elif checkName == 'ListView' or 'ListBox':
                            if checkName =='ListBox':
                                if element.is_active() == False:
                                  element.click()
                                items=element.ItemTexts()
                                elelist=element.texts()
                                elelist.pop(0)
                                oldlist=len(items)
                                itemcount=element.item_count()
                                newlist=[]
                                if(element.IsSingleSelection()==True):
                                    logger.print_on_console('List is a single selection type.')
                                n=element.selected_indices()
                                for i in range(0,len(n)):
                                    idindex=None
                                    idindex=int(n[i])
                                    newlist=items[idindex]
                                #newitems=[item.encode("utf-8") for item in items]
                                verb=newlist
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            elif checkName =='ListView':
                                if element.is_active() == False:
                                  element.click()
                                items=element.items()
                                elelist=element.texts()
                                elelist.pop(0)
                                oldlist=len(items)
                                itemcount=element.item_count()
                                newlist=[]
                                for i in range(0,len(items)):
                                     if (items[i].is_selected()):
                                       newlist.append(elelist[i].encode("utf-8"))
                                verb=newlist
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                        #=========================================================

               else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                import traceback
                traceback.print_exc()
                log.error(exception)
                logger.print_on_console(exception)


            return status,result,verb,err_msg

        def verifySelected(self,element,parent,input_val, *args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                err_msg=None
                try:
                   checkName =element.friendly_class_name()
                   dektop_element = element
                   verify_obj = Text_Box()
                   check = verify_obj.verify_parent(element,parent)
                   log.debug('Parent of element while scraping')
                   log.debug(parent)
                   log.debug('Parent check status')
                   log.debug(check)
                   if (check):
                            log.info('Parent matched')
                            if checkName == 'ComboBox':
                                selected=element.selected_text()
                                verb=selected
                                item_list=input_val
                                for item in item_list:
                                 if item == verb:
                                   status=desktop_constants.TEST_RESULT_PASS
                                   result=desktop_constants.TEST_RESULT_TRUE
                                 else:
                                  status = desktop_constants.TEST_RESULT_FAIL
                                  result = desktop_constants.TEST_RESULT_FALSE
                            #================================================================
                            elif checkName == 'ListView' or 'ListBox':
                                if element.is_active() == False:
                                  element.click()
                                if checkName == 'ListBox':
                                    if element.is_active() == False:
                                      element.click()
                                    items=element.ItemTexts()
                                    elelist=element.texts()
                                    elelist.pop(0)
                                    oldlist=len(items)
                                    itemcount=element.item_count()
                                    newlist=[]
                                    if(element.IsSingleSelection()==True):
                                        logger.print_on_console('List is a single selection type.')
                                    n=element.selected_indices()
                                    for i in range(0,len(n)):
                                        idindex=None
                                        idindex=int(n[i])
                                        newlist=items[idindex]
                                    #newitems=[item.encode("utf-8") for item in items]
                                    verb=newlist
                                    item_list=input_val
                                    for item in item_list:
                                     if item in verb:
                                       status=desktop_constants.TEST_RESULT_PASS
                                       result=desktop_constants.TEST_RESULT_TRUE
                                if checkName == 'ListView':
                                    items=element.items()
                                    elelist=element.texts()
                                    elelist.pop(0)
                                    oldlist=len(elelist)
                                    #cols=element.column_count()
                                    #res=oldlist/cols
                                    itemcount=element.item_count()
                                    newlist=[]
                                    for i in range(0,len(items)):
                                         if (items[i].is_selected()):
                                           selected=element.item(i, subitem_index=0)
                                           newlist.append(elelist[i].encode("utf-8"))
                                    verb=newlist
                                    item_list=input_val
                                    for item in item_list:
                                     if item in verb:
                                       status=desktop_constants.TEST_RESULT_PASS
                                       result=desktop_constants.TEST_RESULT_TRUE
                                     else:
                                      status = desktop_constants.TEST_RESULT_FAIL
                                    result = desktop_constants.TEST_RESULT_FALSE
                            #================================================================


                   else:
                       log.info('Element not present on the page where operation is trying to be performed')
                       err_msg='Element not present on the page where operation is trying to be performed'
                       logger.print_on_console('Element not present on the page where operation is trying to be performed')
                except Exception as exception:
                    import traceback
                    traceback.print_exc()
                    log.error(exception)
                    logger.print_on_console(exception)

                return status,result,verb,err_msg

        def selectValueByText(self,element,parent,input_val, *args):
            if(len(input_val)>1):
                text = input_val[2]
            else:
                text=input_val[0]
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            text_flag = False
            try:
                if desktop_launch_keywords.window_name!=None:
                    log.info('Recieved element from the desktop dispatcher')
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element,parent)
                    checkName =element.friendly_class_name()
                    if (check):
                        log.info('Parent matched')
                        if(element.is_enabled()):
                            item_text=str(text)
                            #----------------------------------------------------------------------------------------dropdown
                            if checkName == 'ComboBox':
                                if item_text != '' or item_text != None:
                                    if element.is_enabled():
                                        selected_text = element.selected_text()
                                        if selected_text == item_text:
                                            log.info('Combobox with given text is already selected')
                                            logger.print_on_console('Combobox with given text is already selected')
                                            err_msg = 'Combobox with given text is already selected'
                                        else:
                                            try:
                                                element.select(item_text)
                                                log.info('Combobox item selected')
                                                logger.print_on_console('Combobox item selected')
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info(STATUS_METHODOUTPUT_UPDATE)
                                            except Exception as e:
                                                log.info('There is no item in Combobox with the given text')
                                                logger.print_on_console('There is no item in Combobox with the given text')
                                                err_msg = 'There is no item in Combobox with the given text'


                                    else:
                                        log.info('Element state does not allow to perform the operation')
                                        logger.print_on_console('Element state does not allow to perform the operation')
                                        err_msg = 'Element state does not allow to perform the operation'
                                else:
                                    log.info('There is no item in Combobox with the given text')
                                    logger.print_on_console('There is no item in Combobox with the given text')
                                    err_msg = 'There is no item in Combobox with the given text'
                            #==============================================================================
                            elif checkName == 'ListView' or 'ListBox':
                                if checkName == 'ListBox':
                                    if item_text != '' or item_text != None:
                                        items=element.ItemTexts()
                                        for i in range(0,len(items)):
                                            if(item_text==str(items[i])):
                                                try:
                                                    element.Select(item_text)
                                                    status = desktop_constants.TEST_RESULT_PASS
                                                    result = desktop_constants.TEST_RESULT_TRUE
                                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                                                except Exception as e:
                                                    import traceback
                                                    traceback.print_exc()
                                                    logger.print_on_console('There is no item in List with the given text',e)

                                elif checkName == 'ListView':
                                    if item_text != '' or item_text != None:
                                        try:
                                            item = element.get_item(item_text)
                                        except:
                                            text_flag = True
                                        if text_flag == False:
                                            if not item.is_selected():
                                                if element.is_active() == False:
                                                    element.click()
                                                item.select()
                                                log.info('List item selected')
                                                logger.print_on_console('List item selected')
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info(STATUS_METHODOUTPUT_UPDATE)
                                            else:
                                                log.info('List item is already selected')
                                                logger.print_on_console('List item is already selected')
                                                err_msg = 'List item is already selected'
                                        else:
                                            log.info('There is no List item in List view with the given text')
                                            logger.print_on_console('There is no List item in List view with the given text')
                                            err_msg = 'There is no List item in List view with the given text'
                                else:
                                    log.info('There is no List item in List view with the given text')
                                    logger.print_on_console('There is no List item in List view with the given text')
                                    err_msg = 'There is no List item in List view with the given text'
                            #==============================================================================

                        else:
                            log.info('Element not present on the page where operation is trying to be performed')
                            err_msg='Element not present on the page where operation is trying to be performed'
                            logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)
            return status,result,verb,err_msg


        def verifyAllValues(self,element,parent,input_val, *args):
            try:
                if input_val[0]=='dropdown' and int(input_val[1])==True:         #to check is object is custom dropdown
                    input_val = input_val[2:]                                #if custom then populate list from 3rd element
                    
                if len(input_val)==1 and ';' in input_val[0]:                   # check if the list of inputs comes as a single string
                     input_val=input_val[0].split(';')                          # check is input val has ";", if so then split
            except :
                pass
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            items=[]
            checkName=""
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               checkName =element.friendly_class_name()
               if (check):
                        log.info('Parent matched')
                        if checkName == 'ComboBox':
                            items=element.texts()
                            items.pop(0)
                            newlist=[]
                            items_list=input_val
                            for i in range(0,len(items)):
                                    newlist.append(items[i].encode("utf-8"))
                                    if items_list==newlist:
                                        status = desktop_constants.TEST_RESULT_PASS
                                        result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        status = desktop_constants.TEST_RESULT_FAIL
                                        result = desktop_constants.TEST_RESULT_FALSE
                        #==================================================================
                        elif checkName == 'ListView' or 'ListBox':
                             if checkName == 'ListBox':
                                items=element.ItemTexts()
                                newlist=[]
                                newlist=[item.encode("utf-8") for item in items]#removing unicode
                                items_list=input_val
                                if newlist==items_list:
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE

                             elif checkName == 'ListView':
                                 items=element.items()
                                 items.pop(0)
                                 newlist=[]
                                 items_list=input_val
                                 for i in range(0,len(items)):
                                        #newitems=[item.encode("utf-8") for item in items]
                                        newlist.append(items[i].encode("utf-8"))
                                        if items_list==newlist:
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                        else:
                                            status = desktop_constants.TEST_RESULT_FAIL
                                            result = desktop_constants.TEST_RESULT_FALSE
                        #==================================================================
               else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                import traceback
                traceback.print_exc()
                log.error(exception)
                logger.print_on_console(exception)
            return status,result,verb,err_msg




        def verifyValuesExists(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            items=[]
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               checkName =element.friendly_class_name()
               if (check):
                        log.info('Parent matched')
                        if checkName == 'ComboBox':
                            items=element.texts()
                            items.pop(0)
                            newlist=[]
                            items_list=input_val
                            for i in range(0,len(items)):
                                    newlist.append(items[i])
                                    for i in range(0,len(items_list)):
                                        if items_list[i] in newlist:
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                        else:
                                            status = desktop_constants.TEST_RESULT_FAIL
                                            result = desktop_constants.TEST_RESULT_FALSE
                        #==============================================================
                        elif checkName == 'ListView' or 'ListBox':
                            if checkName == 'ListBox':
                                fail_flag=False #will set to true if item is not apart of original list,if set to true result is set to fail
                                items=element.ItemTexts()
                                newlist=[]
                                newlist=[item.encode("utf-8") for item in items] #removing unicode
                                items_list=input_val
                                for i in range(0,len(items_list)):
                                    if items_list[i] not in newlist:
                                        fail_flag=True
                                if fail_flag==False:
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE

                            if checkName == 'ListView':
                                 items=element.items()
                                 elelist=element.texts()
                                 elelist.pop(0)
                                 newlist=[]
                                 items_list=input_val
                                 for i in range(0,len(items)):
                                        newlist.append(elelist[i].encode("utf-8"))
                                        for i in range(0,len(items_list)):
                                            if items_list[i] in newlist:
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                            else:
                                                status = desktop_constants.TEST_RESULT_FAIL
                                                result = desktop_constants.TEST_RESULT_FALSE
                        #=================================================================
               else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                import traceback
                traceback.print_exc()
                log.error(exception)
                logger.print_on_console(exception)
            return status,result,verb,err_msg

        def selectAllValues(self,element,parent,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               log.debug('Parent of element while scraping')
               log.debug(parent)
               log.debug('Parent check status')
               log.debug(check)
               if (check):
                        log.info('Parent matched')
                        if(element.is_enabled()):
                            #============================================================================
                            if element.friendly_class_name() == 'ListView' or 'ListBox':
                                if element.friendly_class_name() == 'ListBox':
                                    fail_flag=False
                                    if(element.IsSingleSelection()!=True):
                                        if element.is_active() == False:
                                           element.click()
                                        items=element.ItemTexts()
                                        for item in range(0,len(items)):
                                            try:
                                                element.select(item)
                                            except:
                                                fail_flag=True
                                        if fail_flag==False:
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        logger.print_on_console('List is a single selection type.Could not select all values')
                                        err_msg='List is a single selection type.Could not select all values'

                                elif element.friendly_class_name() == 'ListView':
                                     if element.is_active() == False:
                                       element.click()
                                     items=element.items()
                                     for i in range(0,len(items)):
                                          items[i].select()
                                          status = desktop_constants.TEST_RESULT_PASS
                                          result = desktop_constants.TEST_RESULT_TRUE
                            #============================================================================

                        else:
                          log.info('Element state does not allow to perform the operation')
                          logger.print_on_console('Element state does not allow to perform the operation')
                          err_msg= 'Element state does not allow to perform the operation'
               else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                import traceback
                traceback.print_exc()
                log.error(exception)
                logger.print_on_console(exception)

            return status,result,verb,err_msg

        def deSelectAll(self,element,parent,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               log.debug('Parent of element while scraping')
               log.debug(parent)
               log.debug('Parent check status')
               log.debug(check)
               if (check):
                        log.info('Parent matched')
                        if(element.is_enabled()):
                            #===============================================================
                            if element.friendly_class_name() == 'ListView' or 'ListBox':
                                if element.friendly_class_name() == 'ListBox':
                                    items=element.ItemTexts()
                                    fail_flag=False
                                    if(element.IsSingleSelection()!=True):#to check if the ListBox is a singleSelection type
                                        for item in range(0,len(items)):
                                            try:
                                                element.select(item,select=False)
                                            except:
                                                fail_flag=True
                                        if fail_flag==False:
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        logger.print_on_console('Element state does not allow to perform the operation')
                                elif element.friendly_class_name() == 'ListView':
                                     if element.is_active() == False:
                                       element.click()
                                     items=element.items()
                                     for i in range(0,len(items)):
                                      items[i].deselect()
                                      status = desktop_constants.TEST_RESULT_PASS
                                      result = desktop_constants.TEST_RESULT_TRUE
                            #===============================================================

                        else:
                          log.info('Element state does not allow to perform the operation')
                          logger.print_on_console('Element state does not allow to perform the operation')
                          err_msg= 'Element state does not allow to perform the operation'
               else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                import traceback
                traceback.print_exc()
                log.error(exception)
                logger.print_on_console(exception)


            return status,result,verb,err_msg


        def getMultpleValuesByIndexs(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            items=[]
            try:
               dektop_element = element
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element,parent)
               log.debug('Parent of element while scraping')
               log.debug(parent)
               log.debug('Parent check status')
               log.debug(check)
               if (check):
                        log.info('Parent matched')
                        #=================================================================================
                        if element.friendly_class_name() == 'ListView' or 'ListBox':
                            if element.friendly_class_name() == 'ListBox':
                                false_flag=False
                                if element.is_active() == False:
                                  element.click()
                                input_list=input_val
                                ilist=[]
                                newlist=[]
                                verbList=[]
                                for x in range(0,len(input_list)):
                                    ilist.append(int(input_list[x])-1)
                                items=element.ItemTexts()
                                newlist=[item.encode("utf-8") for item in items]#removing unicode
                                for i in range(len(ilist)):
                                    index=None
                                    index=int(ilist[i])
                                    if index < 0 or index >=len(items):
                                        verbList.append("No Value")
                                        false_flag=True
                                    else:
                                        verbList.append(items[index])
                                verb =[nitem.encode("utf-8") for nitem in verbList]
                                if false_flag==False:
                                    err_msg="Entered indexs are out of bound"
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                            if element.friendly_class_name() == 'ListView':
                                #---------------------------------------------checker(32 or 64)
                                import platform
                                info_32=platform.architecture()
                                if info_32[0]=='32bit':
                                    logger.print_on_console('Warning:You are using 32bit version of ICE Engine.This keyword is unstable for this version.If unsatisfactory results, use 64bit ICE Engine.')
                                #---------------------------------------------
                                if element.is_active() == False:
                                  element.click()
                                items=element.items()
                                cols=element.column_count()
                                elelist=element.texts()
                                elelist.pop(0)
                                oldlist=len(items)
                                itemcount=element.item_count()
                                newlist=[]
                                list = input_val
                                item_list=[]
                                for item in list:
                                    #logger.print_on_console(item)
                                    item_new = (int(item)-1)*2
                                    #logger.print_on_console(item_new)
                                    item_list.append(item_new)
                                val=''
                                res=''
                                for i in range(0,len(item_list)):
                                    if(cols==1):
                                     val=item_list[i]
                                     res=elelist[int(val)]
                                    else:
                                     val=item_list[i]
                                     res1=elelist[int(val)]
                                     res2=elelist[int(val) + 1]
                                     newlist.append(res1.encode("utf-8"))
                                     newlist.append(res2.encode("utf-8"))
                                if cols==1:
                                    verb=newlist
                                else:
                                    verb=self.multiListGetter(cols,elelist,input_val)
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                        #=================================================================================

                        elif element.friendly_class_name() == 'ComboBox':
                            selected=element.selected_text()
                            verb=selected
                            logger.print_on_console('Values obtained are:',verb)
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)

               else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                import traceback
                traceback.print_exc()
                log.error(exception)
                logger.print_on_console(exception)

            return status,result,verb,err_msg





        def selectMultpleValuesByIndexs(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            try:
                if desktop_launch_keywords.window_name!=None:
                    log.info('Recieved element from the desktop dispatcher')
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element,parent)
                    log.debug('Parent of element while scraping')
                    log.debug(parent)
                    log.debug('Parent check status')
                    log.debug(check)
                    if (check):
                        log.info('Parent matched')
                        if(element.is_enabled()):
                            item_index=input_val
                            #====================================================================================
                            if element.friendly_class_name() == 'ListView' or 'ListBox':
                                if element.friendly_class_name() == 'ListBox':
                                    fail_flag=False
                                    if(element.IsSingleSelection()!=True):
                                        if element.is_active() == False:
                                           element.click()
                                        ilist=[]
                                        items=element.ItemTexts()

                                        for x in range(0,len(item_index)):
                                            ilist.append(int(item_index[x])-1)
                                        for i in range(len(ilist)):
                                            index=None
                                            index=int(ilist[i])
                                            if index < 0 or index >=len(items):
                                                fail_flag=True
                                            else:
                                                element.Select(index)
                                        if fail_flag==False:
                                            err_msg="Entered indexs are out of bound"
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        logger.print_on_console('List is a single selection type.Could not select all values')
                                        err_msg='List is a single selection type.Could not select all values'

                                elif element.friendly_class_name() == 'ListView':
                                    item_count = element.item_count()
                                    items=element.items()
                                    for i in range(0,len(items)):
                                                      items[i].deselect()
                                    for i in range(0,len(item_index)):
                                      if int(item_index[i]) <= item_count:
                                         item = element.get_item(int(item_index[i])-1)
                                         if not item.is_selected():
                                            if element.is_active() == False:
                                                element.click()
                                            if item_index <=0:
                                                log.info('List item index starts with 1')
                                                logger.print_on_console('List item index starts with 1')
                                            else:
                                                item.select()
                                                log.info('List item selected')
                                                logger.print_on_console('List item selected')
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info(STATUS_METHODOUTPUT_UPDATE)
                                         else:
                                            log.info('List item is already selected')
                                            logger.print_on_console('List item is already selected')
                                            err_msg = 'List item is already selected'

                                      else:
                                            log.info('There is no List item in List view with the given index')
                                            logger.print_on_console('There is no List item in List view with the given index')
                                            err_msg = 'There is no List item in List view with the given index'
                            #====================================================================================
                        else:
                            log.info('Element state does not allow to perform the operation')
                            logger.print_on_console('Element state does not allow to perform the operation')
                            err_msg = 'Element state does not allow to perform the operation'

                    else:
                        log.info('Element not present on the page where operation is trying to be performed')
                        err_msg='Element not present on the page where operation is trying to be performed'
                        logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)

            return status,result,verb,err_msg


        def selectMultpleValuesByText(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            try:
                if desktop_launch_keywords.window_name!=None:
                    log.info('Recieved element from the desktop dispatcher')
                    dektop_element = element
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element,parent)
                    checkName=element.friendly_class_name()
                    if (check):
                        log.info('Parent matched')
                        if(element.is_enabled()):
                            item_text=input_val
                            if checkName == 'ListView':
                                items=element.items()
                                elelist=element.texts()
                                new_elelist=[]
                                for i in range(0,len(elelist)):
                                    new_elelist.append(elelist[i].encode("utf-8"))
                        #=======================================================================================================
                            if checkName == 'ListView' or 'ListBox':
                                if checkName == 'ListBox':
                                    fail_flag=False
                                    if(element.IsSingleSelection()!=True):
##                                        if element.is_active() == False:
##                                           element.click()
                                        newlist=[]
                                        items=element.ItemTexts()
                                        newlist=[item.encode("utf-8") for item in items]#removing unicode
                                        for i in range(len(item_text)):
                                            if(item_text[i] not in newlist):
                                                fail_flag=True
                                        if fail_flag==False:
                                            for i in range(len(item_text)):
                                                element.Select(item_text[i])
                                            #err_msg="Entered indexs are out of bound"
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        logger.print_on_console('List is a single selection type.Could not select all values')
                                        err_msg='List is a single selection type.Could not select all values'
                                elif checkName == 'ListView':
                                    item_count = element.item_count()
                                    items=element.items()
                                    for i in range(0,len(items)):
                                                      items[i].deselect()
                                    for i in range(0,len(item_text)):
                                        if item_text[i] in new_elelist:
                                             itemtext = element.get_item(item_text[i])
                                             if not itemtext.is_selected():
                                                if element.is_active() == False:
                                                    element.click()
                                                itemtext.select()
                                                logger.print_on_console('List item selected')
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info(STATUS_METHODOUTPUT_UPDATE)
                                             else:
                                                log.info('List item is already selected')
                                                logger.print_on_console('List item is already selected')
                                                err_msg = 'List item is already selected'
                            #=======================================================================================================

                        else:
                            log.info('Element state does not allow to perform the operation')
                            logger.print_on_console('Element state does not allow to perform the operation')
                            err_msg = 'Element state does not allow to perform the operation'
                    else:
                        log.info('Element not present on the page where operation is trying to be performed')
                        err_msg='Element not present on the page where operation is trying to be performed'
                        logger.print_on_console('Element not present on the page where operation is trying to be performed')
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)


            return status,result,verb,err_msg

        def multiListGetter(self,cols,elelist,input_val):
            rows=len(elelist)/cols
            #-------------------------------------------------creating a 2D list
            #print"creating a 2D list"
            Matrix = [[0 for x in range(cols)] for y in range(rows)]
            #-------------------------------------------------creating a 2D list
            #-------------------------------------------------populating the 2D list
            #print"populating the 2D list"
            index_i=0
            for j in range(0,rows):
                for k in range (0,cols):
                    try:
                        Matrix[j][k]=elelist[index_i].encode("utf-8")
                        index_i=index_i+1
                    except Exception as e:
                        print"Error Occured",e
            #-------------------------------------------------populating the 2D list
            #-------------------------------------------------printing the 2D list
##                                print"printing the 2D list"
##                                for j in range(0,rows):
##                                    for k in range (0,cols):
##                                        try:
##                                            print"Matrix"+"["+str(j+1)+"]["+str(k+1)+"]:"+str(Matrix[j][k])+"."
##                                        except Exception as e:
##                                            print"out of bound",e
            #-------------------------------------------------printing the 2D list
            #-------------------------------------------------creating new Matrix based on indexes given
            #print"creating new matrix based on input vals"
            NewMatrix = [[0 for x in range(cols)] for y in range(len(input_val))]
            #-------------------------------------------------creating new Matrix based on indexes given
            #-------------------------------------------------poulating the new martix
            #print"populating the new matrix"
            new_input_val=[]
            for z in range(0,len(input_val)):
                new_input_val.append(str(int(input_val[z])-1))
            try:
                r=0
                for nr in new_input_val:
                    rowindex=int(nr)
                    for c in range(0,cols):
                        NewMatrix[r][c]=Matrix[rowindex][c]
                    r=r+1
            except Exception as e:
                import traceback
                traceback.print_exc()
                print "Error happened :",e
            #-------------------------------------------------poulating the new martix
            #-------------------------------------------------printing the new 2D list
##            print"printing the new 2D list"
##            for j1 in range(0,len(input_val)):
##                for k1 in range (0,cols):
##                    try:
##                        print"NewMatrix"+"["+str(j1+1)+"]["+str(k1+1)+"]:"+str(NewMatrix[j1][k1])+"."
##                    except Exception as e:
##                        print"out of bound",e
            #-------------------------------------------------printing the new 2D list
            return NewMatrix