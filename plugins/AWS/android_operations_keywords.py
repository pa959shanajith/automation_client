#-------------------------------------------------------------------------------
# Name:        mobile_test.py
# Purpose:     Defining each actions performed in mobile automation
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import subprocess
import time
import logging

log = logging.getLogger('android_operations_keywords.py')

# import testcase_compile
##testcase_compile.keywords_list=[]

from testmobile_constants import *

class MobileOpeartions():
    """Basis for all tests."""

    def start_server(self):
        """Sets up desired capabilities and the Appium driver."""
        driver=None
        import platform
        if platform.system() != 'Darwin':
            url = 'http://127.0.0.1:4723/wd/hub'
        else:
            url = 'http://0.0.0.0:4723/wd/hub'
            SYSTEM_OS = 'Darwin'
        desired_caps = {}
        try:
            driver = webdriver.Remote(url, desired_caps)
        except Exception as e:
            logger.print_on_console('Error in webdriver')
            log.error(e)
            return None
        return driver

    def launch_application(self,apk_path):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        self.apk_path=''
        if apk_path is not None and apk_path.strip() != '':
            self.apk_path=apk_path
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output,err_msg

    def send_value(self,driver,element,input_val,*args):
        return self.set_text(driver,element,input_val,*args)

    def set_text(self, driver,element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if element is not None:
                visibility=element.is_displayed()
                visibility=True
                log.info('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.info(WEB_ELEMENT_ENABLED)
                    if enable:
                        if len(element.text)>0:
                            log.info('clearing  the existing text')
                            element.clear()
                        if SYSTEM_OS != 'Darwin': element.set_text(input_val)
                        else: element.set_value(input_val)
                        time.sleep(2)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_ERR_WEB_ELEMENT_DISABLED']

                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.error(err_msg)

        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def clear_text(self,driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.info(ELEMENT_VISIBLE)
                if visibility:
                    enable=element.is_enabled()
                    log.info(WEB_ELEMENT_ENABLED)
                    if enable:
                        if len(element.text)>0:
                            log.info('clearing  the existing text')
                            element.clear()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def press(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.info('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.info('element is Enabled')
                    if enable:
                        log.info('performing the action')
                        action = TouchAction(driver)
                        action.tap(element).perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg


    def long_press(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        action = TouchAction(driver)
                        action.long_press(element).perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def get_button_name(self, driver,webelement,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None

        try:
            if type(webelement) is list:
                   webelement=webelement[0]
            if webelement is not None:
                        log.debug(WEB_ELEMENT_ENABLED)
                        output=webelement.text
                        log.info("Button name: "+output)
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
        except Exception as e:
                log.error(e)
        return status,result,output,err_msg

    def verify_button_name(self, driver,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if len(input)>0 :
                if webelement is not None:
                    if webelement.text==input:
                        log.debug('text matched')
                        log.info("Button name: "+input)
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
        return status,result,output,err_msg

    def get_text(self, driver,webelement,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None

        try:
            if type(webelement) is list:
                webelement=webelement[0]
            if webelement is not None:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    output=webelement.text
                    log.info("Element text: "+output)
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,result,output,err_msg

    def verify_text(self, driver,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if len(input)>0 :
                if webelement is not None:
                    if webelement.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        if webelement.text==input:
                            log.debug('text matched')
                            log.info("Element text: "+input)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                        log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,result,output,err_msg

    def toggle_on(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug(ELEMENT_VISIBLE)
                if visibility:
                    enable=element.is_enabled()
                    if enable:
                        log.debug(WEB_ELEMENT_ENABLED)
                        log.debug('performing the action')
                        res = element.text
                        log.debug('Result is ' + str(res))
                        ios = str(res)
                        if ios == 'False' or res.upper() == 'OFF':
                            action = TouchAction(driver)
                            action.tap(element).perform()
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            err_msg='Toggle is already ON'
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']

                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def toggle_off(self,driver,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        status=None

        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    if enable:
                        log.debug(WEB_ELEMENT_ENABLED)
                        log.debug('performing the action')
                        res=webelement.text
                        ios = str(res)
                        if ios == 'True' or res.upper()=='ON':
                            action = TouchAction(driver)
                            action.tap(webelement).perform()
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            err_msg='Toggle is already OFF'

                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def verify_enabled(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                if visibility:
                    log.debug(ELEMENT_VISIBLE)
                    enable=element.is_enabled()
                    if enable:
                        log.info(WEB_ELEMENT_ENABLED)
                        log.debug('performing the action')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def verify_disabled(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                if visibility:
                    log.debug(ELEMENT_VISIBLE)
                    enable=element.is_enabled()
                    if not(enable):
                        log.info(ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED'])
                        log.debug('performing the action')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=WEB_ELEMENT_ENABLED
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def verify_visible(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                if visibility:
                    log.info(ELEMENT_VISIBLE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def verify_hidden(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                if not(visibility):
                    log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ELEMENT_VISIBLE
                    log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def verify_exists(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                log.info(ELEMENT_EXISTS)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                err_msg=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def verify_does_not_exists(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                err_msg=ELEMENT_EXISTS
                log.error(err_msg)
            else:
                log.info(ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS'])
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def getMobileElement(self,driver,objectname,*args):
        mobileElement = None
        print_loggers=True
        if len(args)>0 and args[0]=='waitforelement_exists':
            print_loggers=False
            log.info('Waiting for the element')
        if objectname.strip() != '':
            if SYSTEM_OS=='Darwin':
                objectname = objectname.replace("/AppiumAUT[1]/", "/")
                log.info(objectname)
            else:
                identifiers = objectname.split(';')
                if print_loggers:
                    log.info('Identifiers are ')
                    log.info(identifiers)
            try:
                if SYSTEM_OS=='Darwin':
                    mobileElement = driver.find_element_by_xpath(objectname)
                else:
                    if print_loggers:
                        log.debug('trying to find mobileElement by Xpath')
                    mobileElement = driver.find_element_by_xpath(identifiers[1])
            except Exception as Ex:
                if(identifiers[0]):
                    try:
                        if print_loggers:
                            log.info('Webelement not found by XPath')
                            log.debug('trying to find mobileElement by ID')
                        mobileElement = driver.find_element_by_id(identifiers[0])
                    except Exception as Ex:
                        log.info('Webelement not found')
                        err_msg=str(Ex)
                        log.error(err_msg)
            
        if mobileElement is not None:
            log.info('Web element found')
        return mobileElement

    def waitforelement_exists(self, driver,mob_ele,object_name,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            # configvalues = readconfig.configvalues
            # timeout= configvalues['timeOut']
            timeout='5'
            if len(args)>0:
                try:
                    timeout=int(args[0])
                except:
                    pass
            if timeout!=None:
                start_time = time.time()
                while True:
                    element=self.getMobileElement(driver,object_name,'waitforelement_exists')
                    later=time.time()
                    if int(later-start_time)>=int(timeout):
                        log.info('Delay timeout')
                        break
                    if element!=None:
                        log.info(ELEMENT_EXISTS)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        break
            else:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
                log.error(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def Set_Min_Value(self,driver,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.info(ELEMENT_VISIBLE)
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        ##webelement.send_keys('0')
                        location=webelement.location
                        size=webelement.size
                        start_x=location['x']
                        start_y=location['y'] + (size['height']/2)
                        end_x=location['x']
                        end_y=location['y'] + (size['height']/2)
                        
                        driver.swipe(start_x,start_y,end_x,end_y,3000)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def Set_Mid_Value(self,driver,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug(ELEMENT_VISIBLE)
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def Set_Max_Value(self, driver,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug(ELEMENT_VISIBLE)
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                       log.debug('performing the action')
                       location=webelement.location
                       size=webelement.size
                       start_x=location['x']
                       start_y=location['y'] + (size['height']/2)
                       end_x=location['x'] + (size['width'])
                       end_y=start_y
                       
                       driver.swipe(start_x,start_y,end_x,end_y,3000)
                       status=TEST_RESULT_PASS
                       methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def select_radio_button(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug(ELEMENT_VISIBLE)
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        action = TouchAction(driver)
                        action.tap(element).perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def get_status(self, driver,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None

        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug(ELEMENT_VISIBLE)
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        classname= webelement.get_attribute("className")
                        if 'Switch' in classname:
                            output=webelement.text
                            output=str(output).upper()
                        elif 'Radio' in classname:
                            output=webelement.get_attribute("checked")
                            if output=='true':
                                output='Selected'
                            else:
                                output="UnSelected"
                        elif 'CheckBox' in classname:
                            output=webelement.get_attribute("checked")
                            if output=='true':
                                output='Checked'
                            else:
                                output="UnChecked"
                        else :
                            output=webelement.get_attribute("checked")
                        if output!=None:
                            log.info(output)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def select_checkbox(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug(ELEMENT_VISIBLE)
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        action = TouchAction(driver)
                        action.tap(element).perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def unselect_checkbox(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug(ELEMENT_VISIBLE)
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        action = TouchAction(driver)
                        action.tap(element).perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg

    def Select_Number(self, driver,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        input_val=input[0]
        try:
            element = element.find_element_by_class_name("android.widget.EditText")
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        element.set_text(input_val)
                        android_home = os.environ['ANDROID_HOME']
                        if android_home is not None:
                            cmd = android_home + '\\platform-tools\\'
                            os.chdir(cmd)
                            cmd = cmd + 'adb.exe shell input keyevent 61'
                            op = subprocess.check_output(cmd)
                            #configvalues = readconfig.configvalues
                            hide_soft_key = 'Yes'
                            if driver.is_keyboard_shown() and hide_soft_key == "Yes":
                                driver.hide_keyboard()
                            if (element.text == input_val):
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                            else:
                                log.error("Failed to set the correct value")
                        else:
                            log.error('NO_ANDROID_HOME')
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,result,output,err_msg

    def Get_Selected_Number(self, driver,element,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        try:
            element = element.find_element_by_class_name("android.widget.EditText")
            if element is not None:
                if element.is_enabled():
                    log.debug(ELEMENT_ENABLED)
                    output = element.text
                    log.info("Selected number: "+output)
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_WEB_ELEMENT_DISABLED']
            else:
                err_msg=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
            if err_msg:
                log.erro(err_msg)
        except Exception as e:
            log.error(e)
        return status,result,output,err_msg

    def Verify_Selected_Number(self, driver,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            element = element.find_element_by_class_name("android.widget.EditText")
            input_val=input[0]
            if len(input_val)>0 :
                if element is not None:
                    elem_text = element.text
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        if elem_text==input_val:
                            log.debug('text matched')
                            log.info("Selected number: "+elem_text)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            log.info("Selected number: "+elem_text)
                    else:
                        log.error('ELEMENT_DISABLED')
                        if elem_text==input_val:
                            log.debug('text matched')
                            log.info("Selected number: "+elem_text)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            log.info("Selected number: ;"+elem_text)
                else:
                    log.error('ELEMENT DOES NOT EXIST')
            else:
                log.error('INVALID INPUT')
        except Exception as e:
            log.error(e)
        return status,result,output,err_msg


    def Set_Time(self, driver,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        #className=''
        err_msg=None
        #text=[]
        #obj=[]
        Tflag=False
        Tflag1 =False
        Tflag2 =False
        input_date=input[0].split(':')

        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        action = TouchAction(driver)
                        Date_picker=driver.find_elements_by_class_name('android.widget.TimePicker')
                        count= len(Date_picker)
                        Date_picker2=driver.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                        count2= len(Date_picker2)

                        if count2 == 12 :
                            if input_date[0] !='':
                                inphr = int(input_date[0]) - 1
                                action.tap(Date_picker2[inphr]).perform()
                                if input_date[1] !='':
                                    if int(input_date[1]) <= 59:
                                        inpmin = int(input_date[1]) / 5
                                        action.tap(Date_picker2[inpmin]).perform()
                                        if input_date[2] !='':
                                            ampm = driver.find_elements_by_class_name('android.widget.RadioButton')
                                            lenAMPM = len(ampm)
                                            if lenAMPM == 2:
                                                if input_date[2] == 'AM':
                                                    action.tap(ampm[0]).perform()
                                                else:
                                                    action.tap(ampm[1]).perform()
                                            else:
                                                log.info("More RadioButtons before Timepicker")
                                            status=TEST_RESULT_PASS
                                            result=TEST_RESULT_TRUE
                                        else:
                                            err_msg='Invalid input'
                                            log.error('Invalid input')
                                    else:
                                        err_msg='Invalid input'
                                        log.error('Invalid input')
                                else:
                                    err_msg='Invalid input'
                                    log.error('Invalid input')
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')

                        elif count == 1:
                            if input_date[0] !='':
                                element=driver.find_elements_by_class_name('android.widget.EditText')
                                element[0].set_text(input_date[0])
                                Tflag = True
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')

                            if input_date[1] !='':
                                element[1].set_text(input_date[1])
                                value=element[1].text
                                Tflag1 = True
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')

                            if input_date[2] !='':
                                element[2].set_text(input_date[2])
                                value=element[2].text
                                Tflag2 = True
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')

                            if Tflag == True and Tflag1 ==True and Tflag2== True:
                                value0=element[0].text
                                value1=element[1].text
                                value2=element[2].text
                                if value0 != input_date[0]:
                                    element[0].set_text(input_date[0])
                                    time.sleep(3)
                                    value0=element[0].text
                                if value1 != input_date[1]:
                                    element[1].set_text(input_date[1])
                                    time.sleep(3)
                                    value1=element[1].text
                                if value2 != input_date[2]:
                                    element[2].set_text(input_date[2])
                                    time.sleep(3)
                                    value2=element[2].text

                                if value0 == input_date[0] and value1== input_date[1] and value2==input_date[2]:
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                        else:
                            err_msg='Incompatible element'
                            log.error('Incompatible element')
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
            else:
                err_msg='webelement is None'
                log.error('webelement is None')
        except Exception as e:
                log.error(e)
        return status,result,output,err_msg

    def Get_Time(self, driver,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        #className=''
        err_msg=None
        #text=[]
        #obj=[]
        #input_date=input[0].split(':')

        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        Date_picker=driver.find_elements_by_class_name('android.widget.TimePicker')
                        count= len(Date_picker)
                        Date_picker2=driver.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                        count2= len(Date_picker2)
                        if count2 == 12 :
                            element1=driver.find_elements_by_class_name('android.widget.TextView')
                            AmorPm=driver.find_elements_by_class_name('android.widget.RadioButton')
                            Hour=element1[0].text
                            Min=element1[2].text
                            if AmorPm[0].get_attribute("checked"):
                                AMorPM="AM"
                            else:
                                AMorPM="PM"
                            output=Hour+':'+Min+':'+AMorPM
                            log.info("Time: "+output)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE

                        elif count == 1 :
                            element=driver.find_elements_by_class_name('android.widget.EditText')
                            Hour=element[0].text
                            Min=element[1].text
                            AMorPM=element[2].text
                            output=Hour+':'+Min+':'+AMorPM
                            log.info("Time: "+output)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
        except Exception as e:
                log.error(e)
        return status,result,output,err_msg

    def Set_Date(self,driver,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        className=''
        err_msg=None
        text=[]
        Tflag=False
        Tflag1=False
        Tflag2=False
        obj=[]
        input_date=input[0].split('/')

        years=[]
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        
                        action = TouchAction(driver)
                        Date_picker=driver.find_elements_by_class_name('android.widget.DatePicker')
                        count = len(Date_picker)
                        if count == 1 :
                            if int(input_date[1])>0 or int(input_date[2])>0 :
                                element=driver.find_elements_by_class_name('android.widget.EditText')
                                if input_date[0] !='':
                                    element[0].set_text(input_date[0])
                                    time.sleep(1)
                                    Tflag = True
                                else:
                                    err_msg='Invalid input'
                                    log.error('Invalid input')

                                if input_date[1] !='':
                                    element[1].set_text(input_date[1])
                                    time.sleep(2)
                                    Tflag1 = True
                                else:
                                    err_msg='Invalid input'
                                    log.error('Invalid input')

                                if input_date[2] !='':
                                    element[2].set_text(input_date[2])
                                    time.sleep(3)
                                    Tflag2=True
                                else:
                                    err_msg='Invalid input'
                                    log.error('Invalid input')

                                if Tflag == True and Tflag1 ==True and Tflag2== True:
                                    value0=element[0].text
                                    value1=element[1].text
                                    value2=element[2].text
                                    if value0 != input_date[0]:
                                        element[0].set_text(input_date[0])
                                        time.sleep(3)
                                        value00=element[0].text
                                    if value1 != input_date[1]:
                                        element[1].set_text(input_date[1])
                                        time.sleep(3)
                                        value11=element[1].text
                                    if value2 != input_date[2]:
                                        element[2].set_text(input_date[2])
                                        time.sleep(3)
                                        value22=element[2].text
                                    if value0 == input_date[0] and value1== input_date[1] and value2==input_date[2]:
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                    elif value00 == input_date[0] and value11== input_date[1] and value22==input_date[2]:
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')
                        else:
                            err_msg = 'Widget not compatible'
                            log.error('Widget not compatible')
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
        except Exception as e:
                log.error(e)
        return status,methodoutput,output,err_msg

    def Get_Date(self,driver,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        className=''
        err_msg=None
        text=[]
        obj=[]
        input_date=input[0].split('/')

        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        Date_picker=driver.find_elements_by_class_name('android.widget.DatePicker')
                        count= len(Date_picker)
                        if count == 1 :
                            element=driver.find_elements_by_class_name('android.widget.EditText')
                            Month=element[0].text
                            Date=element[1].text
                            Year=element[2].text
                            output=Month+'/'+Date+'/'+Year
                            log.info("Date: "+output)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else :
                            err_msg='Widget not compatible'
                            log.error('Widget not compatible')
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
        except Exception as e:
                log.error(e)
        return status,methodoutput,output,err_msg

    def find_coordinates_horizontal(self):
        size=driver.get_window_size()
        log.debug('Window size is '+str(size))
        startx=(size['width']*0.75)
        endx=(size['width']/4)
        starty=(size['height']/2)
        log.debug(startx,starty,endx)
        return startx,starty,endx


    def find_coordinates_vertical(self):
        size=driver.get_window_size()
        log.debug('Window size is '+str(size))
        min_y=(size['height']/4)
        max_y=(size['height']*0.75)
        x_Value=(size['width']/2)
        log.debug(x_Value,max_y,min_y)
        return x_Value,max_y,min_y


    def swipe_left(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            startx,starty,endx=self.find_coordinates_horizontal()
            #Swipe from Right to Left
            driver.swipe(startx, starty, endx, starty, 3000)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console("Error occurred in SwipeLeft")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def swipe_right(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            startx,starty,endx=self.find_coordinates_horizontal()
            #Swipe from left to Right
            driver.swipe(endx, starty, startx, starty, 3000)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console("Error occurred in SwipeRight")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def swipe_up(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            x_Value,max_y,min_y=self.find_coordinates_vertical()
            #Swipe from bottom to top
            driver.swipe(x_Value, max_y, x_Value, min_y, 3000)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console("Error occurred in SwipeUp")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def swipe_down(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            x_Value,max_y,min_y=self.find_coordinates_vertical()
            #Swipe from top to bottom
            driver.swipe(x_Value, min_y, x_Value, max_y, 3000)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console("Error occurred in SwipeDown")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg



    def backPress(self,inputval,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            driver.keyevent(4)
            time.sleep(1)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console("Error occurred in BackPress")
            log.error(e,exc_info=True)
            return status,methodoutput,output,err_msg








##    def start_server_nineteen68(self):
##        path = 'D:/AWS/node_modules/node_modules/appium/build/lib/main.js'
##        nodePath = 'D:/AWS/node.exe'
##        proc = subprocess.Popen([nodePath, path], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
##        time.sleep(10)
##        print('Server started')


##    def log_in(self):
##        """Types in inputted username and password and presses log in button."""
##        username='dbptest1000'
##        password='password1'
##        fields= self.self.driver.find_elements_by_class_name('android.widget.EditText')
##        username_field=fields[0]
##        password_field = fields[1]
##        buttons = self.self.driver.find_elements_by_class_name('android.widget.Button')
##        log_in_button=buttons[0]
##        username_field.click()
##        time.sleep(2)
##        username_field.send_keys(username)
##
##        password_field.click()
##        time.sleep(2)
##        password_field.send_keys(password)
##
##        log_in_button.click()
##        print ('Logged in Successfully')




##obj=MobileTest()
##obj.start_server()
##obj.self()
##time.sleep(10)
##obj.log_in()

