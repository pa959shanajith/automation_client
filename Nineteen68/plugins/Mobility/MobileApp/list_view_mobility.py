#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak
#
# Created:     31-05-2017
# Copyright:   (c) pavan.nayak 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from constants import *
from mobile_app_constants import *
from appium.webdriver.common.touch_action import TouchAction
import android_scrapping
import logging
import logger
import time


log = logging.getLogger('list_view_mobility.py')

class List_Keywords():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e

    def verify_selected_views(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        selected=[]
        count=0
        text=[]
        obj=[]
        flag=False

        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                                    checked=i.get_attribute("checked")
                                    if str(checked) == 'true' :
                                        selected.append(str(i.text))
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]

                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                                    checked=i.get_attribute("checked")
                                    if str(checked) == 'true' :
                                        selected.append(str(i.text))
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if len(input) == len(selected):
                                    for k in input :
                                        if k in selected:
                                            count=count+1
                                        else :
                                            err_msg=self.print_error(INVALID_INPUT)
                                            break
                                    if count==len(input):
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                                    break

                            if (length1==length2):
                                break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg



    def select_multiple_views_by_indexes(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text=[]
        count=0
        temp=[]
        obj=[]
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            for k in input:
                                for j in obj:
                                    k=int(k)
                                    if k<len(obj) :
                                        if obj[k].text not in temp:
                                            temp.append(obj[k].text)
                                            obj[k].click()
                                            count=count+1

                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            for k in input:
                                for j in obj:
                                    k=int(k)
                                    if k<len(obj) :
                                        if obj[k].text not in temp:
                                            temp.append(obj[k].text)
                                            obj[k].click()
                                            count=count+1
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if len(input) == count:
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                                    break
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                                    break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg



    def select_multiple_views_by_text(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text=[]
        obj=[]
        temp=[]
        count=0
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            for k in input:
                                for j in obj:
                                    if k==j.text :
                                        if k not in temp:
                                            temp.append(j.text)
                                            j.click()
                                            count=count+1
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            for k in input:
                                for j in obj:
                                 if k==j.text :
                                    if k not in temp:
                                        temp.append(j.text)
                                        j.click()
                                        count=count+1
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if len(input) == count:

                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                                    break
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                                    break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def get_selected_views(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        text=[]
        selected=[]
        obj=[]
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                                    checked=i.get_attribute("checked")
                                    if str(checked) == 'true' :
                                        selected.append(str(i.text))
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]

                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                                    checked=i.get_attribute("checked")
                                    if str(checked) == 'true' :
                                        selected.append(str(i.text))
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                output=selected
                                logger.print_on_console("Output: "+output)
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                                break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg

    def get_list_count(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        text=[]
        obj=[]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]

                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                output=length1
                                logger.print_on_console("Count: "+output)
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                                break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def verify_list_count(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        count=None
        input=int(input[0])
        err_msg=None
        text=[]
        obj=[]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                count=length1
                                break

                        if (input==count):
                            log.debug('count matched')
                            logger.print_on_console("Count: "+count)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def select_view_by_text(self,element,input,*args):
        global flag
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        input=input[0]
        text=[]
        obj=[]
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            for j in obj:
                                if input is not None:
                                    if input == j.text :
                                        j.click()
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                        flag=True
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            if flag == False:
                                if input is not None:
                                    if input == j.text :
                                        j.click()
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                        flag=True
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if flag == False:
                                    err_msg=self.print_error(INVALID_INPUT)
                                break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg




    def select_view_by_index(self,element,input,*args):
        global flag
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text=[]
        input=int(input[0])
        obj=[]
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            for j in obj:
                                if flag == False:
                                    if input is not None:
                                        if input<len(obj) :
                                            obj[input].click()
                                            status=TEST_RESULT_PASS
                                            result=TEST_RESULT_TRUE
                                            flag=True
                                    else :
                                        err_msg=self.print_error(INVALID_INPUT)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            if flag == False:
                                if input is not None:
                                   if input<len(obj) :
                                        obj[input].click()
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                        flag=True
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if flag == False:
                                    err_msg=self.print_error(INVALID_INPUT)
                                break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def get_list_view_by_index(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        temp=[]
        err_msg=None
        text=[]
        obj=[]
        count=0
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)

                                k=int(input[0])
                                if k<len(obj) :
                                    if text[k] not in temp:
                                        temp.append(text[k])
                                        count=count+1

                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)

                                k=int(input[0])
                                if k<len(obj) :
                                    if text[k] not in temp:
                                        temp.append(text[k])
                                        count=count+1
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if len(input) == count:
                                    output=temp[0]
                                    logger.print_on_console("Output: "+output)
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                                    break
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                                    break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def get_multiple_views_by_indexs(self,element,input,*args):

        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        temp=[]
        err_msg=None
        text=[]
        obj=[]
        count=0
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            for k in input:
                                k=int(k)
                                if int(k)<len(obj) :
                                    if text[k] not in temp:
                                        temp.append(text[k])
                                        count=count+1

                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            for k in input:
                                k=int(k)
                                if k<len(obj) :
                                    if text[k] not in temp:
                                        temp.append(text[k])
                                        count=count+1
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if len(input) == count:
                                    output=temp
                                    logger.print_on_console("Output: "+output)
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                                    break
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                                    break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg



    def get_all_views(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        text=[]
        obj=[]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                output=text
                                logger.print_on_console("Output: "+output)
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                                break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def verify_all_views(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        count=0
        text=[]
        obj=[]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        while(True):
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            elementlist=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in elementlist:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if len(input) == len(text):
                                    for k in input :
                                        if k in text:
                                            count=count+1
                                        else :
                                            err_msg=self.print_error(INVALID_INPUT)
                                            break
                                    if count==len(input):
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                else :
                                    err_msg=self.print_error(INVALID_INPUT)
                                    break

                            if (length1==length2):
                                break
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error(e)
            log.error(e,exc_info=True)
        return status,result,output,err_msg
