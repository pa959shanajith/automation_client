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



    def verify_selected_views(self,webelement,input,*args):
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
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                            err_msg='invalid input'
                                            log.error('invalid input')
                                            logger.print_on_console(err_msg)
                                            break
                                    if count==len(input):
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE



                                else :
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                                        break

                            if (length1==length2):
                                break




                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg




    def select_multiple_views_by_indexes(self,webelement,input,*args):
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
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                                        break






                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg



    def select_multiple_views_by_text(self,webelement,input,*args):
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
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                                        break


                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg


    def get_selected_views(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        text=[]
        selected=[]
        obj=[]
##        input=int(input[0])
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg

    def get_list_count(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        text=[]
        obj=[]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]

                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg


    def verify_list_count(self,webelement,input,*args):
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
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                        else :
                                err_msg='count not matching'
                                log.error('count not matching')
                                logger.print_on_console(err_msg)



                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg


    def select_view_by_text(self,webelement,input,*args):
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
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if flag == False:
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)

                                break


                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg




    def select_view_by_index(self,webelement,input,*args):
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
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                            length2=len(text)
                            time.sleep(3)
                            driver.scroll(scrollele1,scrollele2)

                            if (length1==length2):
                                if flag == False:
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)

                                break
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg


    def get_list_view_by_index(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        temp=[]
        err_msg=None
        text=[]
        obj=[]
##        input=int(input)
        count=0
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                                        break





                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:


                log.error(e)

        return status,result,output,err_msg



    def get_multiple_views_by_indexs(self,webelement,input,*args):

        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        temp=[]
        err_msg=None
        text=[]
        obj=[]
##        input=int(input)
        count=0
        flag=False
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                                        break





                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:


                log.error(e)

        return status,result,output,err_msg



    def get_all_views(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        text=[]
        obj=[]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg



    def verify_all_views(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        count=0
        text=[]
        obj=[]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver

                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            length1=len(text)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(3)
                                driver.scroll(scrollele1,scrollele2)
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            for i in element:
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
                                            err_msg='invalid input'
                                            log.error('invalid input')
                                            logger.print_on_console(err_msg)
                                            break
                                    if count==len(input):
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE



                                else :
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                                        break

                            if (length1==length2):
                                break



                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)

        return status,result,output,err_msg



