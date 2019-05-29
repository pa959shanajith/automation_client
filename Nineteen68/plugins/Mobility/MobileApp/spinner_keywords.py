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
import install_and_launch
import android_scrapping
import logging
import logger
import time
driver_obj = None

log = logging.getLogger('spinner_keywords.py')

class Spinner_Keywords():

    def get_count(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        className=''
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        try:
                            while(True):
                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                    className='RadioButton'
                                    count= len(element)
                                    if count == 0 :
                                        element=driver.find_elements_by_class_name('android.widget.TextView')
                                        className='TextView'
                                        count= len(element)
                                else :
                                    className='CheckedTextView'
                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)

                                length1=len(text)
                                scrollele11=obj[0]
                                scrollele21=obj[(length1)-1]
                                time.sleep(2)
                                top_val=element[0].text
                                driver.scroll(scrollele11,scrollele21)
                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)
                                    if i.text ==top_val:
                                        break

                                length3=len(text)
                                driver.scroll(scrollele11,scrollele21)
                                if length1 >4 :
                                    scrollele1=obj[length3-1]
                                    scrollele2=obj[length3-2]
                                    time.sleep(2)
                                    driver.scroll(scrollele2,scrollele1)

                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                    className='RadioButton'
                                    count= len(element)
                                    if count == 0 :
                                        element=driver.find_elements_by_class_name('android.widget.TextView')
                                        className='TextView'
                                        count= len(element)
                                else :
                                    className='CheckedTextView'

                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)
                                length2=len(text)
                                time.sleep(2)
                                driver.scroll(scrollele2,scrollele1)

                                if (length1==length2):
                                    output=str(length1)
                                    logger.print_on_console("Count: "+output)
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                                    break
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console("Error occured in GetCount")
                        if className != 'RadioButton' :
                            driver.keyevent(4)
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
            logger.print_on_console("Error occured in GetCount")

        return status,result,output,err_msg


    def verify_count(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        count=None
        className=''
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        try:
                            while(True):
                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)

                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                    className='RadioButton'
                                    count= len(element)
                                    if count == 0 :
                                        element=driver.find_elements_by_class_name('android.widget.TextView')
                                        className='TextView'
                                        count= len(element)
                                else :
                                    className='CheckedTextView'
                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)

                                length1=len(text)
                                scrollele11=obj[0]
                                scrollele21=obj[(length1)-1]
                                time.sleep(2)
                                top_val=element[0].text
                                driver.scroll(scrollele11,scrollele21)
                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)
                                    if i.text ==top_val:
                                        break
                                length3=len(text)

                                if length1 >4 :
                                    scrollele1=obj[length3-1]
                                    scrollele2=obj[length3-2]
                                    time.sleep(2)
                                    driver.scroll(scrollele2,scrollele1)
                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                    className='RadioButton'
                                    count= len(element)
                                    if count == 0 :
                                        element=driver.find_elements_by_class_name('android.widget.TextView')
                                        className='TextView'
                                        count= len(element)
                                else :
                                    className='CheckedTextView'
                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)
                                length2=len(text)
                                time.sleep(2)
                                driver.scroll(scrollele2,scrollele1)

                                if (length1==length2):
                                    count=length1
                                    break
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console("Error occured in VerifyCount")

                        if className != 'RadioButton' :
                            driver.keyevent(4)
                        if (input==len(text)):
                                log.debug('count matched')
                                logger.print_on_console("Count: "+str(input))
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
            logger.print_on_console("Error occured in VerifyCount")
        return status,result,output,err_msg



    def select_value_by_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        className=''
        input=input[0]
        text=[]
        obj=[]
        global flag
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count= len(element)
                            if count == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                count= len(element)
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'

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
                                        break
                                else :
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                            if status == TEST_RESULT_PASS :
                                break
                            length1=len(text)
                            scrollele11=obj[0]
                            scrollele21=obj[(length1)-1]
                            time.sleep(2)
                            top_val=element[0].text
                            driver.scroll(scrollele11,scrollele21)
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                                if i.text ==top_val:
                                    break
                            for j in obj:
                                if input is not None:
                                    if input == j.text :
                                        j.click()
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                        flag=True
                                        break
                                else :
                                    err_msg='invalid input'
                                    log.error('invalid input')
                            if status == TEST_RESULT_PASS :
                                break
                            length3=len(text)
                            driver.scroll(scrollele11,scrollele21)
                            if flag == False:
                                if length1 >4 :
                                    scrollele1=obj[0]
                                    scrollele2=obj[(length1)-1]
                                    time.sleep(2)
                                    driver.scroll(scrollele2,scrollele1)
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
                                                break
                                        else :
                                            err_msg='invalid input'
                                            log.error('invalid input')
                                            logger.print_on_console(err_msg)
                            length2=len(text)
                            time.sleep(2)
                            driver.scroll(scrollele2,scrollele1)

                            if (length1==length2):
                                if flag == False:
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                                break


                            if className == 'CheckedTextView' :
                                driver.keyevent(4)
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

    def verify_selected_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        var=''
        input=input[0]
        className=''
        text=[]
        obj=[]
        global flag
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
                        element = driver.find_element_by_xpath(args[0]+'/android.widget.TextView[1]')
                        if (element):
                            if (input==element.text):
                                logger.print_on_console("Output: "+input)
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                        else:
                            action = TouchAction(driver)
                            action.tap(webelement).perform()
                            while(True):
                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)

                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                    className='RadioButton'
                                    count = len(element)
                                    if count == 0 :
                                        element=driver.find_elements_by_class_name('android.widget.TextView')
                                        className='TextView'
                                else :
                                    className='CheckedTextView'
                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)
                                if className !='TextView':
                                    for j in obj:
                                        if input is not None:
                                            selected=j.get_attribute("checked")
                                            if str(selected)== 'true':
                                                if input == j.text :
                                                    status=TEST_RESULT_PASS
                                                    result=TEST_RESULT_TRUE
                                                    #if status == TEST_RESULT_PASS :
                                                    driver.keyevent(4)
                                                    var='true'
                                                    flag=True
                                                    break
                                                else:
                                                    if var=='' :
                                                        driver.keyevent(4)
                                                        var='true'
                                                        break
                                        else :
                                            driver.keyevent(4)
                                            var = 'true'
                                            err_msg='invalid input'
                                            log.error('invalid input')
                                            logger.print_on_console(err_msg)
                                else:
                                    for j in obj:
                                        if input is not None:
                                            selected=j.get_attribute("selected")
                                            if str(selected) == 'true':
                                                if input == j.text :
                                                    flag=True
                                                    driver.keyevent(4)
                                                    var = 'true'
                                                    status=TEST_RESULT_PASS
                                                    result=TEST_RESULT_TRUE
                                                    break
                                                else :
                                                    driver.keyevent(4)
                                                    var='true'
                                                    err_msg='invalid input'
                                                    log.error('invalid input')
                                                    logger.print_on_console(err_msg)
                                                    break
                                if status == TEST_RESULT_PASS :
                                    break
                                if className !='TextView':
                                    length1=len(text)
                                    if length1 >4 :
                                        scrollele1=obj[length1-1]
                                        scrollele2=obj[length1-2]
                                        time.sleep(2)
                                        driver.scroll(scrollele2,scrollele1)

                                    for i in element:
                                        if i.text not in text:
                                            text.append(i.text)
                                            obj.append(i)
                                    if flag == False:
                                            for j in obj:
                                                if input is not None:
                                                    selected=j.get_attribute("checked")
                                                    if str(selected)== 'true':
                                                        if input == j.text :
                                                            status=TEST_RESULT_PASS
                                                            result=TEST_RESULT_TRUE
                                                            if var=='' :
                                                                driver.keyevent(4)
                                                                var='true'
                                                            flag=True
                                                            break
                                                        else :
                                                            if var=='' :
                                                                driver.keyevent(4)
                                                                var='true'
                                                            break

                                                else :
                                                    err_msg='invalid input'
                                                    log.error('invalid input')
                                                    logger.print_on_console(err_msg)

                                length2=len(text)
                                time.sleep(2)
                                ##driver.scroll(scrollele2,scrollele1)

                                if (length1==length2):
                                    if flag == False:
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                                        if var=='':
                                            driver.keyevent(4)
                                            var='true'

                                    break

    ##                        if className == 'CheckedTextView' :
    ##                            print '2222222'
    ##                            driver.keyevent(4)

                            if var=='' :
                                driver.keyevent(4)
                                var='true'
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


    def select_value_by_index(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text=[]
        className=''
        input=int(input[0])
        obj=[]
        global flag
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count= len(element)

                            if count == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                count=len(element)
                                className='RadioButton'
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'


                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)

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
                            if status == TEST_RESULT_PASS :
                                break
                            length1=len(text)
                            scrollele11=obj[0]
                            scrollele21=obj[(length1)-1]
                            time.sleep(2)
                            top_val=element[0].text
                            driver.scroll(scrollele11,scrollele21)
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                                if i.text ==top_val:
                                    break
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
                            if status == TEST_RESULT_PASS :
                                break
                            length3=len(text)
                            driver.scroll(scrollele11,scrollele21)

                            if length1 >4 :
                                scrollele1=obj[0]
                                scrollele2=obj[length1-2]
                                time.sleep(2)
                                driver.scroll(scrollele2,scrollele1)

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
                            time.sleep(2)
                            driver.scroll(scrollele2,scrollele1)

                            if (length1==length2):
                                if flag == False:
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                                    if className == 'CheckedTextView' :
                                        driver.keyevent(4)
                                        var = 'true'
                                break
                        if className == 'CheckedTextView' :
                            if var == '':
                                driver.keyevent(4)

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



    def select_multiple_value_by_index(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text=[]
        obj=[]
        className=''
        global flag
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count= len(element)

                            if count == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'

                            else :
                                className='CheckedTextView'
                            for i in element:
                                if i.text not in text :
                                    text.append(i.text)
                                    obj.append(i)

                                if input is not None:
                                    for k in input:
                                        if k<=len(obj) :
                                            obj[k].click()
                                            status=TEST_RESULT_PASS
                                            result=TEST_RESULT_TRUE
                                            flag=True
                                else :
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                            if flag :
                                break
                            else :
                                length1=len(text)
                                if length1 >4 :
                                    scrollele1=obj[length1-1]
                                    scrollele2=obj[length1-2]
                                    driver.scroll(scrollele1,scrollele2)
                        if className == 'CheckedTextView' :
                            driver.keyevent(4)

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



    def select_multiple_value_by_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text=[]
        className=''
        obj=[]
        global flag
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count= len(element)

                            if count == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'
                            for i in element:
                                if i.text not in text :
                                    text.append(i.text)
                                    obj.append(i)

                                if input is not None:
                                    for k in input:
                                        for j in obj:
                                            if k == j.text :
                                                j.click()
                                                status=TEST_RESULT_PASS
                                                result=TEST_RESULT_TRUE
                                                flag=True
                                else :
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                            if flag :
                                break
                            else :
                                length1=len(text)
                                if length1 >4 :
                                    scrollele1=obj[length1-1]
                                    scrollele2=obj[length1-2]
                                    driver.scroll(scrollele2,scrollele1)
                        if className != 'RadioButton' :
                            driver.keyevent(4)

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



    def get_value_by_index(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        temp=[]
        className=''
        err_msg=None
        text=[]
        obj=[]
##        input=int(input)
        count=0
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count= len(element)

                            if count == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'
                            k=int(input[0])
                            for i in element:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)

                                ##if k<len(obj) :
                                ##if text[k] not in temp:
                                    ##temp.append(text[k])
                                    ##count=count+1

                            length1=len(text)
                            scrollele11=obj[0]
                            scrollele21=obj[(length1)-1]
                            time.sleep(2)
                            top_val=element[0].text
                            driver.scroll(scrollele11,scrollele21)
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                                if i.text ==top_val:
                                    break
                                ##if k<len(obj) :
                                ##if text[k] not in temp:
                                    ##temp.append(text[k])
                                    ##count=count+1

                            driver.scroll(scrollele11,scrollele21)
                            if length1 >4 :
                                scrollele1=obj[length1-1]
                                scrollele2=obj[length1-2]
                                time.sleep(2)
                                driver.scroll(scrollele2,scrollele1)
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count= len(element)

                            if count == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'
                            for i in element:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)


                                ##if k<len(obj) :
                                ##if text[k] not in temp:
                                    ##temp.append(text[k])
                                    ##count=count+1
                            length2=len(text)
                            time.sleep(2)
                            driver.scroll(scrollele2,scrollele1)
                            ##if (length1==length2):
                                ##if len(input) == len(temp):
                                    ##output=temp[0]
                            if k<=len(obj):
                                output= obj[k].text
                                logger.print_on_console("Output: "+output)
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                                break

                            else :
                                    err_msg='invalid input'
                                    log.error('invalid input')
                                    logger.print_on_console(err_msg)
                                    break
                        if className != 'RadioButton' :
                            driver.keyevent(4)


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


    def get_selected_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        className=''
        text=[]
        obj=[]
##        input=int(input[0])
        global flag
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
                        element = driver.find_element_by_xpath(args[0]+'/android.widget.TextView[1]')
                        if (element):
                            output=element.text
                            logger.print_on_console("Output: "+output)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            action = TouchAction(driver)
                            action.tap(webelement).perform()
                            while(True):
                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)

                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                    className='RadioButton'
                                    count = len(element)
                                    if count == 0 :
                                        element=driver.find_elements_by_class_name('android.widget.TextView')
                                        className='TextView'
                                else :
                                    className='CheckedTextView'
                                for i in element:
                                    if i.text not in text :
                                        text.append(i.text)
                                        obj.append(i)

                                length1=len(text)
                                scrollele11=obj[0]
                                scrollele21=obj[(length1)-1]
                                time.sleep(2)
                                top_val=element[0].text
                                driver.scroll(scrollele11,scrollele21)
                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)
                                    if i.text ==top_val:
                                        break
                                length3=len(text)
                                driver.scroll(scrollele11,scrollele21)
                                if length1 >4 :
                                    scrollele1=obj[0]
                                    scrollele2=obj[length3-2]
                                    driver.scroll(scrollele2,scrollele1)
                                for i in element:
                                    if i.text not in text:
                                        text.append(i.text)
                                        obj.append(i)
                                driver.scroll(scrollele2,scrollele1)
                                if className !='TextView':
                                    for j in obj:
                                        selected=j.get_attribute("checked")
                                        if str(selected) == 'true':
                                            output=j.text
                                            logger.print_on_console("Output: "+output)
                                            status=TEST_RESULT_PASS
                                            result=TEST_RESULT_TRUE
                                            flag=True
                                            break
                                    break
                                else:
                                    for j in obj:
                                        selected=j.get_attribute("selected")
                                        if str(selected) == 'true':
                                            output=j.text
                                            flag=True
                                            logger.print_on_console("Output: "+output)
                                            status=TEST_RESULT_PASS
                                            result=TEST_RESULT_TRUE
                                            break
                                    break
                            if className != 'RadioButton' :
                                driver.keyevent(4)
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



    def get_multiple_values_by_indexes(self,webelement,input,*args):

        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        temp=[]
        className=''
        err_msg=None
        text=[]
        obj=[]
        count=0
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        try:
                            while(True):
                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                    className='RadioButton'
                                    if count == 0 :
                                        element=driver.find_elements_by_class_name('android.widget.TextView')
                                        className='TextView'
                                else :
                                    className='CheckedTextView'
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
                                    time.sleep(2)
                                    driver.scroll(scrollele1,scrollele2)
                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                    className='RadioButton'
                                    if count == 0 :
                                        element=driver.find_elements_by_class_name('android.widget.TextView')
                                        className='TextView'
                                else :
                                    className='CheckedTextView'

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

                                if (length1==length2):
                                    if len(input) ==  len(temp):
                                        output=str(temp)
                                        logger.print_on_console("Output: "+output)
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                        break
                                    else :
                                        err_msg='invalid input'
                                        log.error('invalid input')
                                        logger.print_on_console(err_msg)
                                        break
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console("Error occured in get_multiple_values_by_indexs")
                        if className != 'RadioButton' :
                            driver.keyevent(4)
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
            logger.print_on_console("Error occured in get_multiple_values_by_indexs")

        return status,result,output,err_msg



    def get_all_values(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        text=[]
        obj=[]
        className=''
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                eles = webelement.get_attribute("className")
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count= len(element)
                            if count == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                count= len(element)
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'

                            for i in element:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            length1=len(text)
                            scrollele11=obj[0]
                            scrollele21=obj[(length1)-1]
                            time.sleep(2)
                            top_val=element[0].text
                            driver.scroll(scrollele11,scrollele21)
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                                if i.text ==top_val:
                                    break
                            length3=len(text)
                            time.sleep(2)
                            driver.scroll(scrollele11,scrollele21)

                            if length1 >4 :
                                scrollele1=obj[0]
                                scrollele2=obj[length1-2]
                                time.sleep(2)
                                driver.scroll(scrollele2,scrollele1)
                                element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                                count= len(element)

                            if count == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                count= len(element)
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length2=len(text)
                            driver.scroll(scrollele2,scrollele1)

                            if (length1==length2):
                                output=str(text)
                                logger.print_on_console("Output: "+output)
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                                break
                            else:
                                output=str(text)
                                logger.print_on_console("Output: "+output)
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                                break

                        if className != 'RadioButton' :
                            driver.keyevent(4)
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



    def verify_all_values(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        count=0
        text=[]
        className=''
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
                        action = TouchAction(driver)
                        action.tap(webelement).perform()
                        while(True):
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count1= len(element)

                            if count1 == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'
                            for i in element:
                                if i.text not in text:
                                    text.append(str(i.text))
                                    obj.append(i)
                            length1=len(text)
                            scrollele11=obj[0]
                            scrollele21=obj[(length1)-1]
                            time.sleep(2)
                            top_val=element[0].text
                            driver.scroll(scrollele11,scrollele21)
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                                if i.text ==top_val:
                                    break
                            length3=len(text)
                            driver.scroll(scrollele11,scrollele21)
                            if length1 >4 :
                                scrollele1=obj[0]
                                scrollele2=obj[length1-2]
                                time.sleep(2)
                                driver.scroll(scrollele2,scrollele1)
                            element=driver.find_elements_by_class_name('android.widget.CheckedTextView')
                            count1= len(element)

                            if count1 == 0 :
                                element=driver.find_elements_by_class_name('android.widget.RadioButton')
                                className='RadioButton'
                                if count == 0 :
                                    element=driver.find_elements_by_class_name('android.widget.TextView')
                                    className='TextView'
                            else :
                                className='CheckedTextView'
                            for i in element:
                                if i.text not in text:
                                    text.append(i.text)
                                    obj.append(i)
                            length2=len(text)
                            time.sleep(2)
##                            driver.scroll(scrollele1,scrollele2)
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


                        if className != 'RadioButton' :
                            driver.keyevent(4)
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
