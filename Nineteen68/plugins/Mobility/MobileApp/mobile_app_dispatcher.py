#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     23-01-2017
# Copyright:   (c) rakesh.v 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import button_link_keyword_mobility
import radio_button_keywords_mobility
import install_and_launch
import textbox_keywords_mobility
import slider_util_keywords
import swipe_keywords
import toggle_keywords
import device_keywords
import logging
import logger
from mobile_app_constants import *
import constants

log = logging.getLogger('mobile_app_dispatcher.py')
class MobileDispatcher:
    button_link_object = button_link_keyword_mobility.Button_Keywords()
    radio_button_object = radio_button_keywords_mobility.Radio_Button_Keywords()
    install_and_launch_object = install_and_launch.LaunchAndInstall()
    textbox_keywords_object = textbox_keywords_mobility.Textbox_keywords()
    slider_util_keywords_object = slider_util_keywords.SliderKeywords()
    swipe_keywords_object = swipe_keywords.SliderKeywords()
    toggle_keywords_object = toggle_keywords.ToggleKeywords()
    device_keywords_object = device_keywords.Device_Keywords()

    def __init__(self):
        self.exception_flag=''


    def dispatcher(self,teststepproperty,input,reporting_obj):
        global ELEMENT_FOUND
        result=(TEST_RESULT_FAIL,TEST_RESULT_FALSE)
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name
        err_msg=None
        result=[constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]

        try:
            dict={'setText':self.textbox_keywords_object.set_text,
                    'clearText' : self.textbox_keywords_object.clear_text,
                    'setsecuretext' : self.textbox_keywords_object.setsecuretext,
                    'sendValue' : self.textbox_keywords_object.send_value,
                    'getText' : self.textbox_keywords_object.get_text,
                    'verifyText' : self.textbox_keywords_object.verify_text,
                    'getTextBoxLength': self.textbox_keywords_object.get_textBoxLength,
                    'verifyTextBoxLength' : self.textbox_keywords_object.verify_textBoxLength,
                    'selectRadioButton' : self.radio_button_object.select_radio_button,
                    'getStatus' : self.radio_button_object.get_status,
                    'selectCheckbox' : self.radio_button_object.select_checkbox,
                    'unselectCheckbox' : self.radio_button_object.unselect_checkbox,
                    'press' : self.button_link_object.press,
                    'longPress' : self.button_link_object.long_press,
                    'getButtonName' : self.button_link_object.get_button_name,
                    'verifyButtonName' : self.button_link_object.get_button_name,
                    'installApplication' : self.install_and_launch_object.installApplication,
                    'unInstallApplication' : self.install_and_launch_object.uninstallApplication,
                    'closeApplication' : self.install_and_launch_object.closeApplication,
                    'swipeLeft' : self.swipe_keywords_object.swipe_left,
                    'swipeRight': self.swipe_keywords_object.swipe_right,
                    'swipeUp': self.swipe_keywords_object.swipe_up,
                    'swipeDown': self.swipe_keywords_object.swipe_down,
                    'toggleOn' : self.toggle_keywords_object.toggle_on,
                    'toggleOff':self.toggle_keywords_object.toggle_off,
                    'verify_enabled' : self.slider_util_keywords_object.verify_enabled,
                    'verify_disabled' : self.slider_util_keywords_object.verify_disabled,
                    'verify_visible' : self.slider_util_keywords_object.verify_visible,
                    'verify_hidden' : self.slider_util_keywords_object.verify_hidden,
                    'verify_exists' : self.slider_util_keywords_object.verify_exists,
                    'getDevices' : self.device_keywords_object.get_device_list,
                    'invokeDevice' : self.device_keywords_object.invoke_device

                }
            ELEMENT_FOUND=True
            if keyword in dict.keys():
                driver = install_and_launch.driver
                webelement=self.getMobileElement(driver,objectname)
                result=dict[keyword](webelement,input)
                if not(ELEMENT_FOUND) and self.exception_flag:
                    result=constants.TERMINATE
            else:
                err_msg=INVALID_KEYWORD
                result[3]=err_msg
        except TypeError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception at dispatcher')
        return result

    def getMobileElement(self,driver,objectname):
        objectname = str(objectname)
        mobileElement = None
        global ELEMENT_FOUND
        if objectname.strip() != '':

            identifiers = objectname.split(';')
            log.debug('Identifiers are ')
            log.debug(identifiers)
            try:
                log.debug('trying to find mobileElement by Id')
                mobileElement = driver.find_element_by_id(identifiers[0])
            except Exception as Ex:
                try:
                    log.debug('Webelement not found by Id')
                    log.debug('trying to find mobileElement by xpath')
                    mobileElement = driver.find_element_by_xpath(identifiers[1])
                except Exception as Ex:
                    log.debug('Webelement not found')
                    err_msg=str(Ex)
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
        if mobileElement==None:
            ELEMENT_FOUND=False
        return mobileElement
