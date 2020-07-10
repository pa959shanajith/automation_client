#-------------------------------------------------------------------------------
# Name:        Mobility Android_Custom
# Purpose:
#
# Author:      veeresh.koti
#
# Created:     10-04-2019
# Copyright:   (c) veeresh.koti 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from constants import *
from mobile_app_constants import *
import android_scrapping
import logging
import logger
import psutil
import readconfig
import time

log = logging.getLogger('android_custom.py')

class custom():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def custom_check(self,input,keyword):
        try:
            input[2] = int(input[2])
        except Exception as e:
            self.print_error(INVALID_INPUT)
            log.error(e,exc_info=True)
            return False
        if len(input) >= 3 and input[0] != "" and isinstance(input[2], int) and isinstance(input[1], str):
            class_name = input[0].lower()
            custom_dict = {
                'button': ["getbuttonname", "longpress", "press", "click", "verifybuttonname", "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'element': ["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'textbox': ["cleartext", "gettext", "longpress", "press", "click", "sendvalue", "setsecuretext", "settext",
                             "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifytext",
                             "verifyvisible", "waitforelementexists"],
                'timepicker': ["gettime", "settime", "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifytime", "verifyvisible", "waitforelementexists"],
                'datepicker': ["getdate", "setdate", "verifydate", "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'radio': ["getstatus", "selectradiobutton", "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'switch': ["getstatus", "toggleoff", "toggleon", "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'checkbox': ["getstatus", "selectcheckbox", "unselectcheckbox", "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'spinner': ["getallvalues", "getcount", "getmultiplevaluesbyindexes", "getselectedvalue", "verifyselectedvalue", "getvaluebyindex", "selectvaluebyindex", "selectvaluebytext", "verifyallvalues", "verifycount",
                            "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'numberpicker': ["setnumber", "getnumber", "verifynumber", "verifydisabled", "verifyenabled", "verifyexists", "verifydoesnotexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'seekbar': ["setvalue", "setmaxvalue", "setmidvalue", "setminvalue", "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifyvisible", "verifydoesnotexists", "waitforelementexists"],
                'listview':["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'text': ["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'image': ["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'layout': ["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'picker': ["setvalue", "gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'slider': ["setslidevalue", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'link': ["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'table': ["getcellvalue", "cellclick", "getrowcount", "verifyrowcount", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifycellvalue",
                            "verifyhidden", "waitforelementexists"],
                'cell' : ["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'key' : ["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"],
                'view' : ["gettext", "longpress", "press", "click", "verifydisabled", "verifydoesnotexists",
                            "verifyenabled", "verifyexists", "verifyvisible", "verifytext",
                            "verifyhidden", "waitforelementexists"]
            }
            try:
                if keyword in custom_dict[class_name]:
                    return True
                else:
                    return False
            except Exception as e:
                self.print_error("Object name incorrect!!")
                log.error(e,exc_info=True)
                return False
        self.print_error(INVALID_INPUT)
        return False


    def custom_element(self,input,*args):
        element = None
        driver_flag = False
        object_name = input[0].lower()
        visible_text = input[1]
        driver = android_scrapping.driver
        if SYSTEM_OS != 'Darwin':
            classes = {
                'textbox': ['android.widget.EditText'], 'timepicker': ['android.widget.TimePicker'], 'datepicker': ['android.widget.DatePicker'], 'radio': ['android.widget.RadioButton'], 'button': ['android.widget.Button','android.widget.ImageButton'], 'switch': ['android.widget.Switch'], 'checkbox': ['android.widget.CheckBox'],
                'spinner': ['android.widget.Spinner'], 'numberpicker': ['android.widget.NumberPicker'], 'seekbar': ['android.widget.SeekBar'], 'listview': ['android.widget.ListView'], 'text': ['android.widget.TextView'], 'image': ['android.widget.ImageView'],
                'layout': ['android.widget.LinearLayout','android.widget.RelativeLayout'], 'view':['android.view.View'], 'element': ['android.widget.ScrollView','android.view.ViewGroup','android.widget.FrameLayout','android.widget.LinearLayout','android.widget.RelativeLayout']
            }
        else:
            classes = {
                'textbox': ['XCUIElementTypeTextField','XCUIElementTypeSearchField','XCUIElementTypeSecureTextField'], 'radio': ['XCUIElementTypeRadioButton'], 'button': ['XCUIElementTypeButton'], 'switch': ['XCUIElementTypeSwitch','XCUIElementTypeToggle'],
                'checkbox': ['XCUIElementTypeCheckBox'], 'picker': ['XCUIElementTypePickerWheel'], 'slider': ['XCUIElementTypeSlider'], 'link': ['XCUIElementTypeLink'], 'text': ['XCUIElementTypeStaticText','XCUIElementTypeTextView'],
                'image': ['XCUIElementTypeImage','XCUIElementTypeIcon'], 'table': ['XCUIElementTypeTable'], 'cell' : ['XCUIElementTypeCell'], 'key' : ['XCUIElementTypeKey'],
                'element': ['XCUIElementTypeApplication','XCUIElementTypeWindow','XCUIElementTypeOther','XCUIElementTypeNavigationBar','XCUIElementTypeScrollView','XCUIElementTypeSheet','XCUIElementTypeAlert']
            }
            
        element_list = []
        try:
            index = int(input[2])
            if SYSTEM_OS != 'Darwin':
                processes = psutil.net_connections()
                for line in processes:
                    p = line.laddr
                    if p[1] == 4723 and driver is not None:
                        driver_flag = True
                        break
            else: driver_flag = True
            if driver_flag is True:
                elem_count = 0
                if len(visible_text) > 0:
                   for item in classes[object_name]:
                        xpath_str = "//"+item+"[starts-with(@text,'"+visible_text+"')]"
                        element_list = element_list + driver.find_elements_by_xpath(xpath_str)
                else:
                    for item in classes[object_name]:
                        element_list = element_list + driver.find_elements_by_class_name(item)
                if index < len(element_list):
                    log.info(CUSTOM_ELEMENT_FOUND)
                    logger.print_on_console(CUSTOM_ELEMENT_FOUND)
                    element = element_list[index]
                elif not (args[0] == VERIFY_DOESNOT_EXISTS or args[0] == WAIT_FOR_ELEMENT_EXISTS):
                    self.print_error(CUSTOM_ELEMENT_NOT_FOUND)
                if len(input) == 3:
                    new_input = [""]
                elif len(input) > 3:
                    new_input = input[3:]
            else:
                self.print_error(DRIVER_ERROR)
        except Exception as e:
            self.print_error("Error occurred in Finding Custom element")
            log.error(e, exc_info=True)
        return element,new_input


    def waitforelement_exists(self,input):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            configvalues = readconfig.configvalues
            timeout= configvalues['timeOut']
            if timeout!=None:
                start_time = time.time()
                while True:
                    element, inp = self.custom_element(input,WAIT_FOR_ELEMENT_EXISTS)
                    later=time.time()
                    if int(later-start_time)>=int(timeout):
                        err_msg = self.print_error('Delay timeout')
                        break
                    if element is not None:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        break
            else:
                err_msg = self.print_error(INVALID_INPUT)
        except Exception as e:
            err_msg = self.print_error(e)
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg
