#-------------------------------------------------------------------------------
# Name:        dropdown_keywords.py
# Purpose:
#
# Author:      kavyasree.l
#
# Created:     25-05-2017
# Copyright:   (c) kavyasree.l 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import launch_keywords
import logger
from editable_text import Text_Box
import desktop_constants
import editable_text
import time
from constants import *
editable_text=editable_text.Text_Box()
import logging
log = logging.getLogger('dropdown_keywords.py')
class Dropdown_Keywords():

        def selectValueByIndex(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            try:
                if launch_keywords.window_name!=None:
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
                        if(element.is_enabled):
                            item_index=int(input_val[0])
                            if element.friendly_class_name() == 'ListView':
                                item_count = element.item_count()
                                if item_index <= item_count:
                                    item = element.get_item(item_index-1)
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

                            elif element.friendly_class_name() == 'ComboBox':
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
                                        log.info('Combobox state does not allow to perform the operation')
                                        logger.print_on_console('Combobox state does not allow to perform the operation')
                                        err_msg = 'Combobox state does not allow to perform the operation'
                                else:
                                    log.info('There is no item in Combobox with the given index')
                                    logger.print_on_console('There is no item in Combobox with the given index')
                                    err_msg = 'There is no item in Combobox with the given index'
                        else:
                            log.info('element not present on the page where operation is trying to be performed')
                            err_msg='element not present on the page where operation is trying to be performed'
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
               log.debug('Parent of element while scraping')
               log.debug(parent)
               log.debug('Parent check status')
               log.debug(check)
               if (check):
                        log.info('Parent matched')
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
                                print 'inside list check'
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
                                    logger.print_on_console(item)
                                    item_new = (int(item)-1)*2
                                    logger.print_on_console(item_new)
                                    item_list.append(item_new)
                                val,res=0
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
                                verb=newlist
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            elif element.friendly_class_name() == 'ComboBox':
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
                        else:
                          log.info('Element state does not allow to perform the operation')
               else:
                   log.info('element not present on the page where operation is trying to be performed')
                   err_msg='element not present on the page where operation is trying to be performed'
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
                if launch_keywords.window_name!=None:
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
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
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
                          log.info('Element state does not allow to perform the operation')
                    else:
                      log.info('element not present on the page where operation is trying to be performed')
                      err_msg='element not present on the page where operation is trying to be performed'
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
                if launch_keywords.window_name!=None:
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
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
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
                          log.info('Element state does not allow to perform the operation')
                    else:
                      log.info('element not present on the page where operation is trying to be performed')
                      err_msg='element not present on the page where operation is trying to be performed'
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
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
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

                            elif element.friendly_class_name() == 'ComboBox':
                                selected=element.selected_text()
                                verb=selected
                                logger.print_on_console('selected values are:',verb)
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                          log.info('Element state does not allow to perform the operation')
               else:
                   log.info('element not present on the page where operation is trying to be performed')
                   err_msg='element not present on the page where operation is trying to be performed'
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
                   dektop_element = element
                   verify_obj = Text_Box()
                   check = verify_obj.verify_parent(element,parent)
                   log.debug('Parent of element while scraping')
                   log.debug(parent)
                   log.debug('Parent check status')
                   log.debug(check)
                   if (check):
                            log.info('Parent matched')
                            if(element.is_enabled):
                                if element.friendly_class_name() == 'ListView':
                                    if element.is_active() == False:
                                      element.click()
                                    items=element.items()
                                    elelist=element.texts()
                                    poplist=elelist.pop(0)
                                    oldlist=len(elelist)
                                    cols=element.column_count()
                                    res=oldlist/cols
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

                                elif element.friendly_class_name() == 'ComboBox':
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
                            else:
                              log.info('Element state does not allow to perform the operation')
                   else:
                       log.info('element not present on the page where operation is trying to be performed')
                       err_msg='element not present on the page where operation is trying to be performed'
                except Exception as exception:
                    import traceback
                    traceback.print_exc()
                    log.error(exception)
                    logger.print_on_console(exception)

                return status,result,verb,err_msg

        def selectValueByText(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            text_flag = False
            try:
                if launch_keywords.window_name!=None:
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
                        if(element.is_enabled):
                            item_text=str(input_val[0])
                            if element.friendly_class_name() == 'ListView':
                                if item_text != '' or item_text != None:
                                    try:
                                        item = element.get_item(item_text)
                                    except Exception as e:
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

                            elif element.friendly_class_name() == 'ComboBox':
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
                                        log.info('Combobox state does not allow to perform the operation')
                                        logger.print_on_console('Combobox state does not allow to perform the operation')
                                        err_msg = 'Combobox state does not allow to perform the operation'
                                else:
                                    log.info('There is no item in Combobox with the given text')
                                    logger.print_on_console('There is no item in Combobox with the given text')
                                    err_msg = 'There is no item in Combobox with the given text'
                        else:
                            log.info('element not present on the page where operation is trying to be performed')
                            err_msg='element not present on the page where operation is trying to be performed'
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)
            return status,result,verb,err_msg


        def verifyAllValues(self,element,parent,input_val, *args):
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
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
                                 items=element.items()
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

                            elif element.friendly_class_name() == 'ComboBox':
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
                        else:
                          log.info('Element state does not allow to perform the operation')
               else:
                   log.info('element not present on the page where operation is trying to be performed')
                   err_msg='element not present on the page where operation is trying to be performed'
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
               log.debug('Parent of element while scraping')
               log.debug(parent)
               log.debug('Parent check status')
               log.debug(check)
               if (check):
                        log.info('Parent matched')
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
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

                            elif element.friendly_class_name() == 'ComboBox':
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
                        else:
                          log.info('Element state does not allow to perform the operation')
               else:
                   log.info('element not present on the page where operation is trying to be performed')
                   err_msg='element not present on the page where operation is trying to be performed'
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
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
                                 if element.is_active() == False:
                                   element.click()
                                 items=element.items()
                                 for i in range(0,len(items)):
                                  items[i].select()
                                  status = desktop_constants.TEST_RESULT_PASS
                                  result = desktop_constants.TEST_RESULT_TRUE

                        else:
                          log.info('Element state does not allow to perform the operation')
               else:
                   log.info('element not present on the page where operation is trying to be performed')
                   err_msg='element not present on the page where operation is trying to be performed'
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
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
                                 if element.is_active() == False:
                                   element.click()
                                 items=element.items()
                                 for i in range(0,len(items)):
                                  items[i].deselect()
                                  status = desktop_constants.TEST_RESULT_PASS
                                  result = desktop_constants.TEST_RESULT_TRUE

                        else:
                          log.info('Element state does not allow to perform the operation')
               else:
                   log.info('element not present on the page where operation is trying to be performed')
                   err_msg='element not present on the page where operation is trying to be performed'
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
                        if(element.is_enabled):
                            if element.friendly_class_name() == 'ListView':
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
                                    logger.print_on_console(item)
                                    item_new = (int(item)-1)*2
                                    logger.print_on_console(item_new)
                                    item_list.append(item_new)
                                val,res=0
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
                            verb=newlist
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)

                        elif element.friendly_class_name() == 'ComboBox':
                                selected=element.selected_text()
                                verb=selected
                                logger.print_on_console('Values obtained are:',verb)
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                          log.info('Element state does not allow to perform the operation')
               else:
                   log.info('element not present on the page where operation is trying to be performed')
                   err_msg='element not present on the page where operation is trying to be performed'
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
                if launch_keywords.window_name!=None:
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
                        if(element.is_enabled):
                            item_index=input_val

                            if element.friendly_class_name() == 'ListView':
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


                        else:
                            log.info('Combobox state does not allow to perform the operation')
                            logger.print_on_console('Combobox state does not allow to perform the operation')
                            err_msg = 'Combobox state does not allow to perform the operation'

                    else:
                        log.info('element not present on the page where operation is trying to be performed')
                        err_msg='element not present on the page where operation is trying to be performed'
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
                if launch_keywords.window_name!=None:
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
                        if(element.is_enabled):
                            item_text=input_val
                            items=element.items()
                            elelist=element.texts()
                            new_elelist=[]
                            for i in range(0,len(elelist)):
                                new_elelist.append(elelist[i].encode("utf-8"))
                            if element.friendly_class_name() == 'ListView':
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

                        else:
                            log.info('Combobox state does not allow to perform the operation')
                            logger.print_on_console('Combobox state does not allow to perform the operation')
                            err_msg = 'Combobox state does not allow to perform the operation'
                    else:
                        log.info('element not present on the page where operation is trying to be performed')
                        err_msg='element not present on the page where operation is trying to be performed'
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)


            return status,result,verb,err_msg


