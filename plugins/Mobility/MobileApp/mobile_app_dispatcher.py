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
import android_scrapping
import textbox_keywords_mobility
import slider_util_keywords
import Number_picker_Keywords
import swipe_keywords
import toggle_keywords
import device_keywords
import logging
import seekBar_Mobility
import logger
from mobile_app_constants import *
from constants import *
import action_keywords_app
import mob_screenshot
import readconfig
import spinner_keywords
import list_view_mobility
import DatePicker_Keywords_Mobility
import TimePicker_Keywords_Mobility
import picker_wheel_ios
import table_keywords_native
import socket
import os
import subprocess
import platform
import time
import android_custom
import sys
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
    action_keywords_object=action_keywords_app.Action_Key_App()
    spinner_keywords_object=spinner_keywords.Spinner_Keywords()
    list_view_keywords_object=list_view_mobility.List_Keywords()
    picker_wheel_keywords_object = picker_wheel_ios.Picker_Wheel_Keywords()
    table_keywords_object=table_keywords_native.Table_Keywords()
    date_keywords_object=DatePicker_Keywords_Mobility.Date_Keywords()
    time_keywords_object=TimePicker_Keywords_Mobility.Time_Keywords()
    number_picker_object=Number_picker_Keywords.Number_Picker()
    seekBar_object=seekBar_Mobility.Seek_Bar_Keywords()
    custom_object=android_custom.custom()

    mob_dict={
        'settext':textbox_keywords_object.set_text,
        'cleartext' : textbox_keywords_object.clear_text,
        'setsecuretext' : textbox_keywords_object.setsecuretext,
        'sendvalue' : textbox_keywords_object.send_value,
        'gettext' : textbox_keywords_object.get_text,
        'verifytext' : textbox_keywords_object.verify_text,
        #'verifytextboxlength' : textbox_keywords_object.verify_textBoxLength,
        'selectradiobutton' : radio_button_object.select_radio_button,
        'getstatus' : radio_button_object.get_status,
        'selectcheckbox' : radio_button_object.select_checkbox,
        'unselectcheckbox' : radio_button_object.unselect_checkbox,
        'press' : button_link_object.press,
        'click' : button_link_object.click,
        'longpress' : button_link_object.long_press,
        'getbuttonname' : button_link_object.get_button_name,
        'verifybuttonname' : button_link_object.verify_button_name,
        'installapplication' : install_and_launch_object.installApplication,
        'launchapplication' : install_and_launch_object.launchApp,
        'uninstallapplication' : install_and_launch_object.uninstallApplication,
        'closeapplication' : install_and_launch_object.closeApplication,
        'swipeleft' : swipe_keywords_object.swipe_left,
        'swiperight': swipe_keywords_object.swipe_right,
        'swipeup': swipe_keywords_object.swipe_up,
        'swipedown': swipe_keywords_object.swipe_down,
        'toggleon' : toggle_keywords_object.toggle_on,
        'toggleoff':toggle_keywords_object.toggle_off,
        'verifyenabled' : slider_util_keywords_object.verify_enabled,
        'verifydisabled' : slider_util_keywords_object.verify_disabled,
        'verifyvisible' : slider_util_keywords_object.verify_visible,
        'verifyhidden' : slider_util_keywords_object.verify_hidden,
        'verifyexists' : slider_util_keywords_object.verify_exists,
        'verifydoesnotexists': slider_util_keywords_object.verify_does_not_exists,
        'getdevices' : device_keywords_object.get_device_list,
        'invokedevice' : device_keywords_object.invoke_device,
        'stopserver':install_and_launch_object.stop_server,
        'hidesoftkeyboard':swipe_keywords_object.hide_soft_keyboard,
        'backpress':swipe_keywords_object.backPress,
        'setslidevalue': slider_util_keywords_object.set_slide_value,
        'getslidevalue': slider_util_keywords_object.get_slide_value,
        'actionkey':action_keywords_object.action_key,
        'waitforelementexists':slider_util_keywords_object.waitforelement_exists,
        'getcount':spinner_keywords_object.get_count,
        'verifycount':spinner_keywords_object.verify_count,
        'selectvaluebyindex':spinner_keywords_object.select_value_by_index,
        'selectvaluebytext':spinner_keywords_object.select_value_by_text,
        'getmultiplevaluesbyindexes':spinner_keywords_object.get_multiple_values_by_indexes,
        'getvaluebyindex':spinner_keywords_object.get_value_by_index,
        'getallvalues':spinner_keywords_object.get_all_values,
        'verifyallvalues':spinner_keywords_object.verify_all_values,
        'getselectedvalue':spinner_keywords_object.get_selected_value,
        'verifyselectedvalue':spinner_keywords_object.verify_selected_value,
        'getlistcount':list_view_keywords_object.get_list_count,
        'verifylistcount':list_view_keywords_object.verify_list_count,
        'selectviewbyindex':list_view_keywords_object.select_view_by_index,
        'selectviewbytext':list_view_keywords_object.select_view_by_text,
        'getmultipleviewsbyindexes':list_view_keywords_object.get_multiple_views_by_indexes,
        'getviewbyindex':list_view_keywords_object.get_list_view_by_index,
        'getallviews':list_view_keywords_object.get_all_views,
        'verifyallviews':list_view_keywords_object.verify_all_views,
        'getselectedviews':list_view_keywords_object.get_selected_views,
        'verifyselectedviews':list_view_keywords_object.verify_selected_views,
        'selectmultipleviewsbyindexes':list_view_keywords_object.select_multiple_views_by_indexes,
        'selectmultipleviewsbytext':list_view_keywords_object.select_multiple_views_by_text,
        'setvalue': seekBar_object.Set_Mid_Value if (SYSTEM_OS != 'Darwin') else picker_wheel_keywords_object.set_value,
        'getvalue': picker_wheel_keywords_object.get_value,
        'getrowcount':table_keywords_object.get_row_count,
        'verifyrowcount':table_keywords_object.verify_row_count,
        'cellclick':table_keywords_object.cell_click,
        'getcellvalue':table_keywords_object.get_cell_value,
        'verifycellvalue':table_keywords_object.verify_cell_value,
        'setdate' : date_keywords_object.Set_Date,
        'getdate' : date_keywords_object.Get_Date,
        'settime' : time_keywords_object.Set_Time,
        'gettime' : time_keywords_object.Get_Time,
        'setnumber':number_picker_object.Select_Number,
        'getnumber':number_picker_object.Get_Selected_Number,
        'verifynumber':number_picker_object.Verify_Selected_Number,
        'setminvalue':seekBar_object.Set_Min_Value,
        'setmidvalue':seekBar_object.Set_Mid_Value,
        'setmaxvalue':seekBar_object.Set_Max_Value,
        'verifytime':time_keywords_object.verify_time,
        'verifydate':date_keywords_object.verify_date
    }

    def dispatcher(self,teststepproperty,input,reporting_obj, mythread):
        global apptypes,ip
        objectname = teststepproperty.objectname
        object_name_ios = objectname
        # SOME IRIS FLAG FUNCTIONS
        if SYSTEM_OS=='Darwin':
            path=os.environ['AVO_ASSURE_HOME']+os.sep+'plugins'+os.sep+'Mobility'+os.sep+'iris_mobile'
            sys.path.append(path)
        import iris_mobile
        iris_mobile_object = iris_mobile.iris_mobile_class()
        self.mob_dict['pressiris'] = iris_mobile_object.Press
        self.mob_dict['longpressiris'] = iris_mobile_object.LongPress
        self.mob_dict['settextiris'] = iris_mobile_object.SetText
        self.mob_dict['verifyexistsiris'] = iris_mobile_object.VerifyExists
        self.mob_dict['verifytextiris'] = iris_mobile_object.VerifyText
        self.mob_dict['cleartextiris'] = iris_mobile_object.ClearText
        self.mob_dict['gettextiris'] = iris_mobile_object.GetText
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name.lower()
        apptypes=teststepproperty.apptype
        err_msg=None
        result=[TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,err_msg]

        try:
            if keyword in list(self.mob_dict.keys()):
                if teststepproperty.custname in ["@Android_Custom", "@CustomiOS"]:
                    if (input[0] and (input[1] is not None) and input[2]):
                        logger.print_on_console("Element type is ",input[0])
                        logger.print_on_console("Visible text is ",input[1])
                        logger.print_on_console("Index is ",input[2])
                        if self.custom_object.custom_check(input,keyword) == False:
                            logger.print_on_console("The object and the keyword do not match")
                        elif (keyword==WAIT_FOR_ELEMENT_EXISTS):
                            result=self.custom_object.waitforelement_exists(input)
                        else:
                            element,input=self.custom_object.custom_element(input,keyword)
                            result=self.mob_dict[keyword](element,input)
                    else:
                        logger.print_on_console(INVALID_INPUT,": NULL object used in input")
                        result[3]=INVALID_INPUT+": NULL object used in input"
                elif teststepproperty.cord != '' and teststepproperty.cord != None:
                    #cord to change to img and operations to add here
                    result = self.mob_dict[keyword](objectname , input[0], teststepproperty.cord, teststepproperty.original_device_width, teststepproperty.original_device_height)
                elif keyword==WAIT_FOR_ELEMENT_EXISTS:
                    result=self.mob_dict[keyword](objectname,input)
                else:
                    globalWait_to = int(readconfig.configvalues['globalWaitTimeOut'])
                    if globalWait_to>0:
                        element = xpath = None
                        globalWait_to_delay = 0.25
                        for _ in range(int(globalWait_to/globalWait_to_delay)+1):
                            element, xpath=self.getMobileElement(android_scrapping.driver,objectname)
                            if element is not None:
                                break
                            time.sleep(globalWait_to_delay)
                        if element is not None:
                            msg1="Element found. Global Wait Timeout completed"
                        else:
                            msg1="Element not found. Global Wait Timeout exceeded"
                        logger.print_on_console(msg1)
                        log.info(msg1)
                    else:
                        element, xpath=self.getMobileElement(android_scrapping.driver,objectname)
                        result=self.mob_dict[keyword](element,input,xpath)
            else:
                err_msg=INVALID_KEYWORD
                result[3]=err_msg
            if keyword not in NON_WEBELEMENT_KEYWORDS:
                if self.action == 'execute':
                    result=list(result)
                    screen_shot_obj = mob_screenshot.Screenshot()
                    configobj = readconfig.readConfig()
                    configvalues = configobj.readJson()
                    screen_details=mythread.json_data['suitedetails'][0]
                    if configvalues['screenShot_Flag'].lower() == 'fail':
                        if result[0].lower() == 'fail':
                            file_path =screen_shot_obj.captureScreenshot(screen_details)
                            result.append(file_path[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        file_path = screen_shot_obj.captureScreenshot(screen_details)
                        result.append(file_path[2])
        except TypeError as e:
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console('Exception at dispatcher')
        return result

    def getMobileElement(self,driver,objectname):
        objectname = str(objectname)
        mobileElement = None
        xpath = None
        id = None
        if objectname.strip() != '':
            identifiers = objectname.split(';')
            if SYSTEM_OS=='Darwin':
                xpath = identifiers[0].replace("/AppiumAUT[1]/", "/")
                log.debug(identifiers)
            else:
                if identifiers[0]!='': id = identifiers[0]
                xpath = identifiers[1]
                log.debug('Identifiers are ')
                log.debug(identifiers)
            try:
                if id:
                    log.debug('trying to find mobileElement by id')
                    mobileElement = driver.find_element_by_id(id)
                else:
                    try:
                        log.debug('trying to find mobileElement by xpath')
                        if xpath:
                            mobileElement = driver.find_element_by_xpath(xpath)
                        else:
                            log.debug('Invalid Element')
                    except Exception as Ex:
                        log.debug('Element not found')
                        log.debug(str(Ex))
            except Exception as Ex:
                log.debug(str(Ex))
                log.debug('Element not found by id')
                try:
                    if xpath:
                        log.debug('trying to find mobileElement by xpath')
                        mobileElement = driver.find_element_by_xpath(xpath)
                    else:
                        log.debug('Invalid Element')
                except Exception as Ex:
                    log.debug('Element not found')
                    log.debug(str(Ex))
        return mobileElement, xpath

