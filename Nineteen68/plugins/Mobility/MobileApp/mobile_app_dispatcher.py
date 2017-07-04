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
import action_keyowrds_app
import mob_screenshot
import readconfig
import spinner_keywords
import list_view_mobility
import picker_wheel_ios
apptypes = None

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
    action_keyowrds_object=action_keyowrds_app.Action_Key_App()
    spinner_keywords_object=spinner_keywords.Spinner_Keywords()
    list_view_keywords_object=list_view_mobility.List_Keywords()
    picker_wheel_keywords_object = picker_wheel_ios.Picker_Wheel_Keywords()
    def __init__(self):
        self.exception_flag=''


    def dispatcher(self,teststepproperty,input,reporting_obj):
        global ELEMENT_FOUND
        result=(TEST_RESULT_FAIL,TEST_RESULT_FALSE)
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name
        global apptypes
        apptypes=teststepproperty.apptype
        err_msg=None
        result=[constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]

        try:
            dict={'SetText':self.textbox_keywords_object.set_text,
                    'ClearText' : self.textbox_keywords_object.clear_text,
                    'SetSecureText' : self.textbox_keywords_object.setsecuretext,
                    'SendValue' : self.textbox_keywords_object.send_value,
                    'GetText' : self.textbox_keywords_object.get_text,
                    'VerifyText' : self.textbox_keywords_object.verify_text,
                    'GetTextboxLength': self.textbox_keywords_object.get_textBoxLength,
                    'VerifyTextboxLength' : self.textbox_keywords_object.verify_textBoxLength,
                    'SelectRadioButton' : self.radio_button_object.select_radio_button,
                    'GetStatus' : self.radio_button_object.get_status,
                    'SelectCheckbox' : self.radio_button_object.select_checkbox,
                    'UnSelectCheckbox' : self.radio_button_object.unselect_checkbox,
                    'Press' : self.button_link_object.press,
                    'LongPress' : self.button_link_object.long_press,
                    'GetButtonName' : self.button_link_object.get_button_name,
                    'VerifyButtonName' : self.button_link_object.verify_button_name,
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
                    'StopServer':self.install_and_launch_object.stop_server,
                    'HideSoftKeyBoard':self.swipe_keywords_object.hide_soft_keyboard,
                    'BackPress':self.swipe_keywords_object.backPress,
                    'PressElement':self.button_link_object.press,
                    'LongPressElement':self.button_link_object.long_press,
                    'GetElementText':self.textbox_keywords_object.get_text,
                    'SetSlideValue': self.slider_util_keywords_object.set_slide_value,
                    'GetSlideValue': self.slider_util_keywords_object.get_slide_value,
                    'VerifyElementExists':self.slider_util_keywords_object.verify_exists,
                    'VerifyElementDisabled':self.slider_util_keywords_object.verify_disabled,
                    'VerifyElementDoesNotExists':self.slider_util_keywords_object.verify_does_not_exists,
                    'VerifyElementEnabled':self.slider_util_keywords_object.verify_exists,
                    'VerifyElementText':self.textbox_keywords_object.verify_text,
                    'ActionKey':self.action_keyowrds_object.action_key,
                    'WaitForElementExists':self.slider_util_keywords_object.waitforelement_exists,
                    'GetCount':self.spinner_keywords_object.get_count,
                    'VerifyCount':self.spinner_keywords_object.verify_count,
                    'SelectValueByIndex':self.spinner_keywords_object.select_value_by_index,
                    'SelectValueByText':self.spinner_keywords_object.select_value_by_text,
                    'GetMultipleValuesByIndexes':self.spinner_keywords_object.get_multiple_values_by_indexs,
                    'GetValueByIndex':self.spinner_keywords_object.get_value_by_index,
                    'GetAllValues':self.spinner_keywords_object.get_all_values,
                    'VerifyAllValues':self.spinner_keywords_object.verify_all_values,
                    'GetSelectedValue':self.spinner_keywords_object.get_selected_value,
                    'VerifySelectedValue':self.spinner_keywords_object.verify_selected_value,
                    'GetListCount':self.list_view_keywords_object.get_list_count,
                    'VerifyListCount':self.list_view_keywords_object.verify_list_count,
                    'SelectViewByIndex':self.list_view_keywords_object.select_view_by_index,
                    'SelectViewByText':self.list_view_keywords_object.select_view_by_text,
                    'GetMultipleViewsByIndexes':self.list_view_keywords_object.get_multiple_views_by_indexs,
                    'GetViewByIndex':self.list_view_keywords_object.get_list_view_by_index,
                    'GetAllViews':self.list_view_keywords_object.get_all_views,
                    'VerifyAllViews':self.list_view_keywords_object.verify_all_views,
                    'GetSelectedViews':self.list_view_keywords_object.get_selected_views,
                    'VerifySelectedViews':self.list_view_keywords_object.verify_selected_views,
                    'SelectMultipleViewsByIndexes':self.list_view_keywords_object.select_multiple_views_by_indexes,
                    'SelectMultipleViewsByText':self.list_view_keywords_object.select_multiple_views_by_text,
                    'SetValue': self.picker_wheel_keywords_object.set_value,
                    'GetValue': self.picker_wheel_keywords_object.get_value



                }
            ELEMENT_FOUND=True
            if keyword in dict.keys():
                driver = install_and_launch.driver
                if keyword==WAIT_FOR_ELEMENT_EXISTS:
                    result=dict[keyword](objectname,input)
                else:
                    webelement=self.getMobileElement(driver,objectname)
                    result=dict[keyword](webelement,input)
                if not(ELEMENT_FOUND) and self.exception_flag:
                    result=constants.TERMINATE
            else:
                err_msg=INVALID_KEYWORD
                result[3]=err_msg
            if keyword not in NON_WEBELEMENT_KEYWORDS:
                if self.action == 'execute':
                    result=list(result)
                    screen_shot_obj = mob_screenshot.Screenshot()
                    configobj = readconfig.readConfig()
                    configvalues = configobj.readJson()

                    if configvalues['screenShot_Flag'].lower() == 'fail':
                        if result[0].lower() == 'fail':
                            file_path =screen_shot_obj.captureScreenshot()
                            result.append(file_path[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        file_path = screen_shot_obj.captureScreenshot()
                        result.append(file_path[2])
        except TypeError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            import traceback
            log.error(e)
            logger.print_on_console('Exception at dispatcher')
        return result

    def getMobileElement(self,driver,objectname):
        objectname = str(objectname)
        mobileElement = None
        global ELEMENT_FOUND
        if objectname.strip() != '':
            import platform
            if platform.system()=='Darwin':
                objectname = objectname.replace("/AppiumAUT[1]/", "/")
                print objectname
            identifiers = objectname.split(';')
            log.debug('Identifiers are ')
            log.debug(identifiers)
            try:
                log.debug('trying to find mobileElement by Id')
                import platform
                if platform.system()=='Darwin':
                    mobileElement = driver.find_element_by_xpath(objectname)
                else:
                    mobileElement = driver.find_element_by_xpath(identifiers[1])
            except Exception as Ex:
                try:
                    log.debug('Webelement not found by Id')
                    log.debug('trying to find mobileElement by xpath')
                    mobileElement = driver.find_element_by_id(identifiers[0])
                except Exception as Ex:
                    log.debug('Webelement not found')
                    err_msg=str(Ex)
##                    logger.print_on_console(err_msg)
                    log.error(err_msg)
        if mobileElement==None:
            ELEMENT_FOUND=False
        return mobileElement
