#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     21-11-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import ldtp
import launch_keywords
import logger
import Exceptions
import desktop_constants
import editable_text
import time
from ldtp.client_exception import LdtpExecutionError

editable_text=editable_text.Text_Box()
class Dropdown_Keywords():

        def selectValueByIndex(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            item_index=int(input_val[0])
            print item_index
            try:

                if object_xpath[0:3]=='cbo':
                        if item_index>0:
                            try:
                                time.sleep(0.5)
                                if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                    states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                    if desktop_constants.ENABLED_CHECK in states:
                                        select=ldtp.selectindex(launch_keywords.window_name,object_xpath, itemIndex-1)
                                        if select==1:
                                            status=desktop_constants.TEST_RESULT_PASS
                                            result=desktop_constants.TEST_RESULT_TRUE
                                            return status,result
                                        else:
                                            logger.log('unable to slect the dropdown item')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                if isinstance(e,LdtpExecutionError):
                                    self.clickOnCombo(object_xpath)
                                else:
                                    Exceptions.error(e)
                elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                    try:
                        if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                            child=ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CHILD)
                            if child!=None:
                                list_count=-1
                                children_list=child.split(',')
                                for element in children_list:
                                    if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)!=desktop_constants.LIST_ITEM:
                                       list_count= list_count+1
                                if item_index>0 and len(children_list)-list_count>item_index:
                                    item_index=item_index+list_count
                                    select=ldtp.selectindex(launch_keywords.window_name,object_xpath, item_index)
                                    if select==1:
                                        status=desktop_constants.TEST_RESULT_PASS
                                        result=desktop_constants.TEST_RESULT_TRUE
                                        return status,result
                                    else:
                                        logger.log('unable to select list item')
                        else:
                            logger.log('element not found')
                    except Exception as e:
                        Exceptions.error(e)
                else:
                    print 'not a list'

            except Exception as e:
                Exceptions.error(e)
            return status,result

        def selectValueByText(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            item_text=input_val[0].strip()
            try:
                if launch_keywords.window_name!=None:
                    if object_xpath[0:3]=='cbo':
                        if item_text!=None:
                            try:
                                time.sleep(0.5)
                                if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                    states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                    if desktop_constants.ENABLED_CHECK in states:
                                        select=ldtp.selectitem(launch_keywords.window_name,object_xpath, item_text)
                                        if select==1:
                                            status=desktop_constants.TEST_RESULT_PASS
                                            result=desktop_constants.TEST_RESULT_TRUE
                                            return status,result
                                        else:
                                            logger.log('unable to slect the dropdown item')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                if isinstance(e,LdtpExecutionError):
                                    self.clickOnCombo(object_xpath)
                                else:
                                    Exceptions.error(e)
                elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                    try:
                        if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if desktop_constants.ENABLED_CHECK in states:
                                select=ldtp.selectitem(launch_keywords.window_name,object_xpath, item_text)
                                if select==1:
                                    status=desktop_constants.TEST_RESULT_PASS
                                    result=desktop_constants.TEST_RESULT_TRUE
                                    return status,result
                                else:
                                    logger.log('unable to select list item')
                        else:
                            logger.log('element not found')
                    except Exception as e:
                        Exceptions.error(e)
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def getSelected(self,element,parent,input_val, *args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                object_xpath=element.split(';')[0]
                object_index=element.split(';')[1]
                try:
                    if launch_keywords.window_name!=None:
                        if object_xpath[0:3]=='cbo':
                                try:
                                    time.sleep(0.5)
                                    if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                        states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                        if desktop_constants.ENABLED_CHECK in states:
                                            select=ldtp.getcombovalue(launch_keywords.window_name,object_xpath)
                                            if select!=None:
                                                status=desktop_constants.TEST_RESULT_PASS
                                                result=select
                                                return status,result
                                            else:
                                                logger.log('unable to get  the selected item')
                                    else:
                                        logger.log('element not found')
                                except Exception as e:
                                    if isinstance(e,LdtpExecutionError):
                                        self.clickOnCombo(object_xpath)
                                    else:
                                        Exceptions.error(e)
                        elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                            try:
                                if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                    states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                    if desktop_constants.ENABLED_CHECK in states:
                                        child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                        selected_text=[]
                                        if child!=None:
                                            children_list=child.split(',')
                                            for element in children_list:
                                                states_child=ldtp.getallstates(launch_keywords.window_name,element)
                                                if desktop_constants.SELECTED_CHECK in states_child:
                                                    sub_list=ldtp.getobjectproperty(launch_keywords.window_name,element, desktop_constants.CHILD)
                                                    sub_list_children=sub_list.split(',')
                                                    if sub_list_children!=None:
                                                        sub_index=0
                                                        mutli_text=''
                                                        for sub_list_child in sub_list_children:
                                                            label_text=ldtp.getobjectproperty(launch_keywords.window_name,sub_list_child, desktop_constants.LABEL)
                                                            if sub_index==0:
                                                                mutli_text=label_text
                                                            else:
                                                                mutli_text=mutli_text+'~@~'+label_text
                                                            sub_index=sub_index+1
                                                        selected_text.append(mutli_text)
                                                    else:
                                                        selected_text=selected_text.append(ldtp.getobjectproperty(launch_keywords.window_name,element, desktop_constants.LABEL))

                                            if selected_text!=None:
                                                status=desktop_constants.TEST_RESULT_PASS
                                                result=selected_text
                                                return status,result
                                            else:
                                                logger.log('unable to get the selected list item')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                Exceptions.error(e)
                except Exception as e:
                    Exceptions.error(e)
                return status,result

        def verifySelected(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            item_text=input_val[0].strip()
            try:
                if launch_keywords.window_name!=None:
                    if object_xpath[0:3]=='cbo':
                        if item_text!=None:
                            try:
                                time.sleep(0.5)
                                if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                    states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                    if desktop_constants.ENABLED_CHECK in states:
                                        select=ldtp.verifyselect(launch_keywords.window_name,object_xpath,item_text)
                                        if select==1:
                                            status=desktop_constants.TEST_RESULT_PASS
                                            result=desktop_constants.TEST_RESULT_TRUE
                                            return status,result
                                        else:
                                            logger.log('unable to verify  the selected item')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                if isinstance(e,LdtpExecutionError):
                                    self.clickOnCombo(object_xpath)
                                else:
                                    Exceptions.error(e)
                    elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        try:
                            if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                if desktop_constants.ENABLED_CHECK in states:
                                    child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                    selected_text=[]
                                    if child!=None:
                                        children_list=child.split(',')
                                        for element in children_list:
                                            states_child=ldtp.getallstates(launch_keywords.window_name,element)
                                            if desktop_constants.SELECTED_CHECK in states_child:
                                                sub_list=ldtp.getobjectproperty(launch_keywords.window_name,element, desktop_constants.CHILD)
                                                sub_list_children=sub_list.split(',')
                                                if sub_list_children!=None:
                                                    sub_index=0
                                                    mutli_text=''
                                                    for sub_list_child in sub_list_children:
                                                        label_text=ldtp.getobjectproperty(launch_keywords.window_name,sub_list_child, desktop_constants.LABEL)
                                                        if sub_index==0:
                                                            mutli_text=label_text
                                                        else:
                                                            mutli_text=mutli_text+'~@~'+label_text
                                                        sub_index=sub_index+1
                                                    selected_text.append(mutli_text)
                                                else:
                                                    selected_text=selected_text.append(ldtp.getobjectproperty(launch_keywords.window_name,element, desktop_constants.LABEL))

                                        if selected_text!=None:
                                            item_list=input_val
                                            for item in item_list:
                                                if item in selected_text:
                                                    status=desktop_constants.TEST_RESULT_PASS
                                                    result=desktop_constants.TEST_RESULT_TRUE
                                                else:
                                                    status=desktop_constants.TEST_RESULT_FAIL
                                                    result=desktop_constants.TEST_RESULT_FALSE
                                                    break
                                        else:
                                            logger.log('unable to verify the selected list item')
                            else:
                                logger.log('element not found')
                        except Exception as e:
                            Exceptions.error(e)
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def getCount(self,element,parent, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            try:
                if launch_keywords.window_name!=None:
                    if object_xpath[0:3]=='cbo':
                            try:
                                time.sleep(0.5)
                                if object_xpath!=None  and editable_text.verify_parent(object_xpath,parent):
                                    states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                    if desktop_constants.ENABLED_CHECK in states:
                                        select=ldtp.getallitem(launch_keywords.window_name,object_xpath)
                                        if select!=None :
                                            status=desktop_constants.TEST_RESULT_PASS
                                            result=len(select)
                                            return status,result
                                        else:
                                            logger.log('unable to verify  the selected item')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                if isinstance(e,LdtpExecutionError):
                                    self.clickOnCombo(object_xpath)
                                else:
                                    Exceptions.error(e)
                    elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        try:
                            if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                child=ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CHILD)
                                if child!=None:
                                    list_count=0
                                    children_list=child.split(',')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)!=desktop_constants.LIST_ITEM:
                                           list_count= list_count+1
                                    actual_count=len(children_list)-list_count
                                    if actual_count>0:
                                        status=desktop_constants.TEST_RESULT_PASS
                                        result=actual_count
                                        return status,result
                                    else:
                                        logger.log('unable to select list item')
                            else:
                                logger.log('element not found')
                        except Exception as e:
                            Exceptions.error(e)
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def verifyCount(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            count_given=input_val[0]
            try:
                if launch_keywords.window_name!=None:
                    if object_xpath[0:3]=='cbo':
                            try:
                                time.sleep(0.5)
                                if object_xpath!=None and editable_text.verify_parent(object_xpath,parent) :
                                    states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                    if desktop_constants.ENABLED_CHECK in states:
                                        select=ldtp.getallitem(launch_keywords.window_name,object_xpath)
                                        if select!=None :
                                            if int(count_given)==len(select):
                                                status=desktop_constants.TEST_RESULT_PASS
                                                result=desktop_constants.TEST_RESULT_TRUE
                                                return status,result
                                        else:
                                            logger.log('unable to verify  the selected item')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                if isinstance(e,LdtpExecutionError):
                                    self.clickOnCombo(object_xpath)
                                else:
                                    Exceptions.error(e)
                    elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        try:
                            if object_xpath!=None and editable_text.verify_parent(object_xpath,parent) :
                                child=ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CHILD)
                                if child!=None:
                                    list_count=0
                                    children_list=child.split(',')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)!=desktop_constants.LIST_ITEM:
                                           list_count= list_count+1
                                    actual_count=len(children_list)-list_count
                                    if actual_count>0 and  int(count_given)==actual_count:
                                        status=desktop_constants.TEST_RESULT_PASS
                                        result=desktop_constants.TEST_RESULT_TRUE
                                        return status,result
                            else:
                                logger.log('element not found')
                        except Exception as e:
                            Exceptions.error(e)
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def verifyValuesExists(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            item_text=input_val

            try:
                if launch_keywords.window_name!=None:
                    if object_xpath[0:3]=='cbo':
                        if item_text!=None :
                            try:
                                time.sleep(0.5)
                                if object_xpath!=None and editable_text.verify_parent(object_xpath,parent) :
                                    states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                    if desktop_constants.ENABLED_CHECK in states:
                                        elements=ldtp.getallitem(launch_keywords.window_name,object_xpath)
                                        if elements!=None:
                                            for item in item_text:
                                                if item in elements:
                                                    status=desktop_constants.TEST_RESULT_PASS
                                                    result=desktop_constants.TEST_RESULT_TRUE
                                                else:
                                                    status=desktop_constants.TEST_RESULT_FAIL
                                                    result=desktop_constants.TEST_RESULT_FALSE
                                                    break
                                        else:
                                            logger.log('unable to verify  the  combo items')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                if isinstance(e,LdtpExecutionError):
                                    self.clickOnCombo(object_xpath)
                                else:
                                    Exceptions.error(e)
                    elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        try:
                            if object_xpath!=None and editable_text.verify_parent(object_xpath,parent) :
                                states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                if desktop_constants.ENABLED_CHECK in states:
                                    child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                    selected_text=[]
                                    if child!=None:
                                        children_list=child.split(',')
                                        for element in children_list:
                                            sub_list=ldtp.getobjectproperty(launch_keywords.window_name,element, desktop_constants.CHILD)
                                            sub_list_children=sub_list.split(',')
                                            if sub_list_children!=None:
                                                sub_index=0
                                                mutli_text=''
                                                for sub_list_child in sub_list_children:
                                                    label_text=ldtp.getobjectproperty(launch_keywords.window_name,sub_list_child, desktop_constants.LABEL)
                                                    if sub_index==0:
                                                        mutli_text=label_text
                                                    else:
                                                        mutli_text=mutli_text+'~@~'+label_text
                                                    sub_index=sub_index+1
                                                selected_text.append(mutli_text)
                                            else:
                                                selected_text.append(ldtp.getobjectproperty(launch_keywords.window_name,element, desktop_constants.LABEL))
                                        if selected_text!=None:

                                            for item in input_val:
                                                if item in selected_text:
                                                    status=desktop_constants.TEST_RESULT_PASS
                                                    result=desktop_constants.TEST_RESULT_TRUE
                                                else:
                                                    status=desktop_constants.TEST_RESULT_FAIL
                                                    result=desktop_constants.TEST_RESULT_FALSE
                                                    break
                                        else:
                                            logger.log('unable to verify the list item')
                            else:
                                logger.log('element not found')
                        except Exception as e:
                            Exceptions.error(e)
            except Exception as e:
                Exceptions.error(e)
            return status,result


        def verifyAllValues(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            item_text=input_val
            try:
                if launch_keywords.window_name!=None:
                    if object_xpath[0:3]=='cbo':
                        if item_text!=None and editable_text.verify_parent(object_xpath,parent) :
                            try:
                                time.sleep(0.5)
                                if object_xpath!=None :
                                    elements=ldtp.getallitem(launch_keywords.window_name,object_xpath)
                                    if elements!=None:
                                        if len(elements)==len(item_text):
                                            for item in item_text:
                                                if item in elements:
                                                    status=desktop_constants.TEST_RESULT_PASS
                                                    result=desktop_constants.TEST_RESULT_TRUE
                                                else:
                                                    status=desktop_constants.TEST_RESULT_FAIL
                                                    result=desktop_constants.TEST_RESULT_FALSE
                                                    break
                                    else:
                                        logger.log('unable to verify  the  combo items')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                if isinstance(e,LdtpExecutionError):
                                    self.clickOnCombo(object_xpath)
                                else:
                                    Exceptions.error(e)
                    elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        try:
                            if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                if desktop_constants.ENABLED_CHECK in states:
                                    child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                    selected_text=[]
                                    if child!=None:
                                        children_list=child.split(',')
                                        for element in children_list:
                                            sub_list=ldtp.getobjectproperty(launch_keywords.window_name,element, desktop_constants.CHILD)
                                            sub_list_children=sub_list.split(',')
                                            if sub_list_children!=None:
                                                sub_index=0
                                                mutli_text=''
                                                for sub_list_child in sub_list_children:
                                                    label_text=ldtp.getobjectproperty(launch_keywords.window_name,sub_list_child, desktop_constants.LABEL)
                                                    if sub_index==0:
                                                        mutli_text=label_text
                                                    else:
                                                        mutli_text=mutli_text+'~@~'+label_text
                                                    sub_index=sub_index+1
                                                selected_text.append(mutli_text)
                                            else:
                                                selected_text.append(ldtp.getobjectproperty(launch_keywords.window_name,element, desktop_constants.LABEL))
                                        if selected_text!=None:
                                            if len(selected_text)==len(item_text):
                                                for item in input_val:
                                                    if item in selected_text:
                                                        status=desktop_constants.TEST_RESULT_PASS
                                                        result=desktop_constants.TEST_RESULT_TRUE
                                                    else:
                                                        status=desktop_constants.TEST_RESULT_FAIL
                                                        result=desktop_constants.TEST_RESULT_FALSE
                                                        break
                                        else:
                                            logger.log('unable to verify the list item')
                            else:
                                logger.log('element not found')
                        except Exception as e:
                            Exceptions.error(e)
            except Exception as e:
                Exceptions.error(e)
            return status,result


        def getValueByIndex(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            index=input_val[0]
            try:
                if launch_keywords.window_name!=None:
                    if object_xpath[0:3]=='cbo':
                        if index!=None and editable_text.verify_parent(object_xpath,parent) :
                            index=int(index)
                            try:
                                time.sleep(0.5)
                                if object_xpath!=None :
                                    elements=ldtp.getallitem(launch_keywords.window_name,object_xpath)
                                    if elements!=None:
                                        if len(elements)>int(index) and int(index)>0:
                                            status=desktop_constants.TEST_RESULT_PASS
                                            result=elements[index-1]
                                        else:
                                            logger.log('invalid input')
                                    else:
                                        logger.log('unable to verify  the  combo items')
                                else:
                                    logger.log('element not found')
                            except Exception as e:
                                raise e
                                if isinstance(e,LdtpExecutionError):
                                    self.clickOnCombo(object_xpath)
                                else:
                                    Exceptions.error(e)
                    elif ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        try:
                            if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                                item_index=int(index)
                                states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                                if desktop_constants.ENABLED_CHECK in states:
                                    child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                    selected_text=[]
                                    list_count=-1
                                    if child!=None:
                                        children_list=child.split(',')
                                        for element in children_list:
                                            if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)!=desktop_constants.LIST_ITEM:
                                                list_count= list_count+1
                                        if item_index>0 and len(children_list)-list_count>item_index:
                                                item_index=item_index+list_count
                                                sub_list=ldtp.getobjectproperty(launch_keywords.window_name,children_list[item_index], desktop_constants.CHILD)
                                                sub_list_children=sub_list.split(',')
                                                if sub_list_children!=None:
                                                    sub_index=0
                                                    mutli_text=''
                                                    for sub_list_child in sub_list_children:
                                                        label_text=ldtp.getobjectproperty(launch_keywords.window_name,sub_list_child, desktop_constants.LABEL)
                                                        if sub_index==0:
                                                            mutli_text=label_text
                                                        else:
                                                            mutli_text=mutli_text+'~@~'+label_text
                                                        sub_index=sub_index+1
                                                    selected_text.append(mutli_text)
                                                else:
                                                    selected_text.append(ldtp.getobjectproperty(launch_keywords.window_name,children_list[item_index], desktop_constants.LABEL))

                                    if len(selected_text)>0:
                                        status=desktop_constants.TEST_RESULT_PASS
                                        result=selected_text
                            else:
                                logger.log('element not found')
                        except Exception as e:
                            Exceptions.error(e)
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def getMultpleValuesByIndexs(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            try:
                    if ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        if object_xpath!=None  and editable_text.verify_parent(object_xpath,parent):
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if desktop_constants.ENABLED_CHECK in states:
                                child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                selected_text=[]
                                list_count=-1
                                if child!=None:
                                    children_list=child.split(',')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)!=desktop_constants.LIST_ITEM:
                                            list_count= list_count+1
                                    for item_index in input_val:
                                        item_index=int(item_index)
                                        if item_index>0 and len(children_list)-list_count>item_index:
                                                item_index=item_index+list_count
                                                sub_list=ldtp.getobjectproperty(launch_keywords.window_name,children_list[item_index], desktop_constants.CHILD)
                                                sub_list_children=sub_list.split(',')
                                                if sub_list_children!=None:
                                                    sub_index=0
                                                    mutli_text=''
                                                    for sub_list_child in sub_list_children:
                                                        label_text=ldtp.getobjectproperty(launch_keywords.window_name,sub_list_child, desktop_constants.LABEL)
                                                        if sub_index==0:
                                                            mutli_text=label_text
                                                        else:
                                                            mutli_text=mutli_text+'~@~'+label_text
                                                        sub_index=sub_index+1
                                                    selected_text.append(mutli_text)
                                                else:
                                                    selected_text.append(ldtp.getobjectproperty(launch_keywords.window_name,children_list[item_index], desktop_constants.LABEL))
                                        else:
                                            selected_text=[]
                                            break
                                if len(selected_text)>0:
                                    status=desktop_constants.TEST_RESULT_PASS
                                    result=selected_text
                        else:
                            logger.log('element not found')
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def selectAllValues(self,element,parent,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            try:

                    if ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        if object_xpath!=None and editable_text.verify_parent(object_xpath,parent) :
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if desktop_constants.ENABLED_CHECK in states:
                                child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                selected_text=[]
                                list_count=-1
                                if child!=None:
                                    children_list=child.split(',')
                                    ldtp.keypress('<ctrl>')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)==desktop_constants.LIST_ITEM:
                                            if not desktop_constants.SELECTED_CHECK in   ldtp.getallstates(launch_keywords.window_name, element):
                                                ldtp.click(launch_keywords.window_name,element)
                                            else:
                                                continue
                                    ldtp.keyrelease('<ctrl>')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)==desktop_constants.LIST_ITEM:
                                            if  desktop_constants.SELECTED_CHECK in   ldtp.getallstates(launch_keywords.window_name, element):
                                                status=desktop_constants.TEST_RESULT_PASS
                                                result=desktop_constants.TEST_RESULT_TRUE
                                                continue
                                            else:
                                                status=desktop_constants.TEST_RESULT_FAIL
                                                result=desktop_constants.TEST_RESULT_FALSE
                                                break

                        else:
                            logger.log('element not found')
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def deSelectAll(self,element,parent,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]

            try:
                    if ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        if object_xpath!=None  and editable_text.verify_parent(object_xpath,parent) :
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if desktop_constants.ENABLED_CHECK in states:
                                child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                selected_text=[]
                                list_count=-1
                                if child!=None:
                                    children_list=child.split(',')
                                    ldtp.keypress('<ctrl>')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)==desktop_constants.LIST_ITEM:
                                            if  desktop_constants.SELECTED_CHECK in   ldtp.getallstates(launch_keywords.window_name, element):
                                                ldtp.click(launch_keywords.window_name,element)
                                            else:
                                                continue
                                    ldtp.keyrelease('<ctrl>')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)==desktop_constants.LIST_ITEM:
                                            if not  desktop_constants.SELECTED_CHECK in   ldtp.getallstates(launch_keywords.window_name, element):
                                                status=desktop_constants.TEST_RESULT_PASS
                                                result=desktop_constants.TEST_RESULT_TRUE
                                                continue
                                            else:
                                                status=desktop_constants.TEST_RESULT_FAIL
                                                result=desktop_constants.TEST_RESULT_FALSE
                                                break

                        else:
                            logger.log('element not found')
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def selectMultpleValuesByIndexs(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            try:
                    if ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        if object_xpath!=None and editable_text.verify_parent(object_xpath,parent) :
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if desktop_constants.ENABLED_CHECK in states:
                                child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                selected_text=[]
                                list_count=-1
                                if child!=None:
                                    children_list=child.split(',')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.CLASS)!=desktop_constants.LIST_ITEM:
                                            list_count= list_count+1
                                    for item_index in input_val:
                                        item_index=int(item_index)
                                        if item_index>0 and len(children_list)-list_count>item_index:
                                            item_index=item_index+list_count
                                            if not  desktop_constants.SELECTED_CHECK in   ldtp.getallstates(launch_keywords.window_name, children_list[item_index]):
                                                ldtp.keypress('<ctrl>')
                                                ldtp.click(launch_keywords.window_name,children_list[item_index])
                                                ldtp.keyrelease('<ctrl>')
                                                if   desktop_constants.SELECTED_CHECK in   ldtp.getallstates(launch_keywords.window_name, children_list[item_index]):
                                                    status=desktop_constants.TEST_RESULT_PASS
                                                    result=desktop_constants.TEST_RESULT_TRUE
                                                    continue
                                                else:
                                                    status=desktop_constants.TEST_RESULT_FAIL
                                                    result=desktop_constants.TEST_RESULT_FALSE
                                                    break

                        else:
                            logger.log('element not found')
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def selectMultpleValuesByText(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')[0]
            object_index=element.split(';')[1]
            try:
                    if ldtp.getobjectproperty(launch_keywords.window_name, object_xpath,desktop_constants.CLASS)==desktop_constants.LIST_BOX:
                        if object_xpath!=None  and editable_text.verify_parent(object_xpath,parent):
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if desktop_constants.ENABLED_CHECK in states:
                                child=ldtp.getobjectproperty(launch_keywords.window_name,object_xpath, desktop_constants.CHILD)
                                indexes=[]
                                index=0
                                if child!=None:
                                    children_list=child.split(',')
                                    for element in children_list:
                                        if  ldtp.getobjectproperty(launch_keywords.window_name, element,desktop_constants.LABEL) in input_val:
                                            if not  desktop_constants.SELECTED_CHECK in  ldtp.getallstates(launch_keywords.window_name, element):
                                                indexes.append(index)
                                        index=index+1
                                for item_text in indexes:
                                    ldtp.keypress('<ctrl>')
                                    select=ldtp.selectindex(launch_keywords.window_name,object_xpath, item_text)
                                    ldtp.keyrelease('<ctrl>')
                                    if select==1:
                                        status=desktop_constants.TEST_RESULT_PASS
                                        result=desktop_constants.TEST_RESULT_TRUE
                                    else:
                                        status=desktop_constants.TEST_RESULT_FAIL
                                        result=desktop_constants.TEST_RESULT_FALSE
                                        break
                        else:
                            logger.log('element not found')
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def clickOnCombo(self,objectName):
            try:
                a = ldtp.getobjectsize(launch_keywords.window_name,objectName);
                ldtp.generatemouseevent(a[0] + (a[2]) / 2, a[1]+ (a[3] / 2), "b1c")
            except Exception as e:
                logger.log('')


