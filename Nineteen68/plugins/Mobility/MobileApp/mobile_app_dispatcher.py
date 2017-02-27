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
            dict={'SetText':self.textbox_keywords_object.set_text,
                    'ClearText' : self.textbox_keywords_object.clear_text,
                    'Setsecuretext' : self.textbox_keywords_object.setsecuretext,
                    'SendValue' : self.textbox_keywords_object.send_value,
                    'GetText' : self.textbox_keywords_object.get_text,
                    'VerifyText' : self.textbox_keywords_object.verify_text,
                    'GetTextBoxLength': self.textbox_keywords_object.get_textBoxLength,
                    'VerifyTextBoxLength' : self.textbox_keywords_object.verify_textBoxLength,
                    'SelectRadioButton' : self.radio_button_object.select_radio_button,
                    'GetStatus' : self.radio_button_object.get_status,
                    'SelectCheckbox' : self.radio_button_object.select_checkbox,
                    'UnSelectCheckbox' : self.radio_button_object.unselect_checkbox,
                    'Press' : self.button_link_object.press,
                    'LongPress' : self.button_link_object.long_press,
                    'GetButtonName' : self.button_link_object.get_button_name,
                    'VerifyButtonName' : self.button_link_object.get_button_name,
                    'InstallApplication' : self.install_and_launch_object.installApplication,
                    'LaunchApplication' : self.install_and_launch_object.installApplication,
                    'UnInstallApplication' : self.install_and_launch_object.uninstallApplication,
                    'CloseApplication' : self.install_and_launch_object.closeApplication,
                    'SwipeLeft' : self.swipe_keywords_object.swipe_left,
                    'SwipeRight': self.swipe_keywords_object.swipe_right,
                    'SwipeUp': self.swipe_keywords_object.swipe_up,
                    'SwipeDown': self.swipe_keywords_object.swipe_down,
                    'ToggleOn' : self.toggle_keywords_object.toggle_on,
                    'ToggleOff':self.toggle_keywords_object.toggle_off,
                    'VerifyEnabled' : self.slider_util_keywords_object.verify_enabled,
                    'VerifyDisabled' : self.slider_util_keywords_object.verify_disabled,
                    'VerifyVisible' : self.slider_util_keywords_object.verify_visible,
                    'VerifyHidden' : self.slider_util_keywords_object.verify_hidden,
                    'VerifyExists' : self.slider_util_keywords_object.verify_exists,
                    'GetDevices' : self.device_keywords_object.get_device_list,
                    'InvokeDevice' : self.device_keywords_object.invoke_device,
                    'StopServer':self.install_and_launch_object.stop_server

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
