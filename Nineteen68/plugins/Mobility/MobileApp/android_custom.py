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
log = logging.getLogger('android_custom.py')

class custom():

    def custom_check(self,input,keyword):
        try:
            input[2] = int(input[2])
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console("Incorrect input!!")
            return False
        if len(input) >= 3 and input[0] != "" and isinstance(input[2], int) and isinstance(input[1], str):
            class_name = input[0]
            custom_dict = {
                'button': ["getbuttonname", "longpress", "press", "verifybuttonname", "verifydisabled", "verifyenabled", "verifyexists",
                           "verifyhidden", "verifyvisible", "waitforelementexists"],
                'element': ["getelementtext", "longpresselement", "presselement", "verifyelementdisabled", "verifyelementdoesnotexists",
                            "verifyelementenabled", "verifyelementexists", "verifyvisible", "verifyelementtext",
                            "verifyhidden", "waitforelementexists"],
                'textbox': ["cleartext", "gettext", "longpress", "press", "sendvalue", "setsecuretext", "settext",
                             "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifytext",
                             "verifyvisible", "waitforelementexists"],
                'timepicker': ["gettime", "settime", "verifydisabled", "verifyenabled", "verifyexists", "VerifyHidden", "verifytime", "verifyvisible", "waitforelementexists"],
                'datepicker': ["getdate", "setdate", "verifydate", "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'radio': ["getstatus", "selectradiobutton", "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'switch': ["getstatus", "toggleoff", "toggleon", "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'checkbox': ["getstatus", "selectcheckbox", "unselectcheckbox", "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'spinner': ["getallvalues", "getcount", "getmultiplevaluesbyindexes", "getselectedvalue", "getvaluebyindex", "selectvaluebyindex", "selectvaluebytext", "verifyallvalues", "verifycount",
                            "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'numberpicker': ["setnumber", "getnumber", "verifynumber", "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'seekbar': ["setvalue", "setmaxvalue", "setmidvalue", "setminvalue", "verifydisabled", "verifyenabled", "verifyexists", "verifyhidden", "verifyvisible", "waitforelementexists"],
                'listview':["getelementtext", "longpresselement", "presselement", "verifyelementdisabled", "verifyelementdoesnotexists",
                            "verifyelementenabled", "verifyelementexists", "verifyvisible", "verifyelementtext",
                            "verifyhidden", "waitforelementexists"],
                'text': ["getelementtext", "longpresselement", "presselement", "verifyelementdisabled", "verifyelementdoesnotexists",
                        "verifyelementenabled", "verifyelementexists", "verifyvisible", "verifyelementtext",
                        "verifyhidden", "waitforelementexists"],
                'image': ["getelementtext", "longpresselement", "presselement", "verifyelementdisabled", "verifyelementdoesnotexists",
                        "verifyelementenabled", "verifyelementexists", "verifyvisible", "verifyelementtext",
                        "verifyhidden", "waitforelementexists"],
                'layout': ["getelementtext", "longpresselement", "presselement", "verifyelementdisabled", "verifyelementdoesnotexists",
                            "verifyelementenabled", "verifyelementexists", "verifyvisible", "verifyelementtext",
                            "verifyhidden", "waitforelementexists"]
            }
            try:
                if keyword in custom_dict[class_name]:
                    return True
                else:
                    return False
            except Exception as e:
                log.error(e,exc_info=True)
                logger.print_on_console("Object name incorrect!!")
                return False
        logger.print_on_console("Incorrect input!!")
        return False


    def custom_element(self,input):
        element = None
        driver_flag = False
        object_name = input[0]
        visible_text = input[1]
        logger.print_on_console(input)
        driver = android_scrapping.driver
        classes = {
            'textbox': ['android.widget.EditText'],
            'timepicker': ['android.widget.TimePicker'],
            'datepicker': ['android.widget.DatePicker'],
            'radio': ['android.widget.RadioButton'],
            'button': ['android.widget.Button','android.widget.ImageButton'],
            'switch': ['android.widget.Switch'],
            'checkbox': ['android.widget.CheckBox'],
            'spinner': ['android.widget.Spinner'],
            'numberpicker': ['android.widget.NumberPicker'],
            'seekbar': ['android.widget.SeekBar'],
            'listview': ['android.widget.ListView'],
            'text': ['android.widget.TextView'],
            'image': ['android.widget.ImageView'],
            'layout': ['android.widget.LinearLayout','android.widget.RelativeLayout'],
            'element': ['android.widget.ScrollView','android.view.View','android.view.ViewGroup','android.widget.FrameLayout']
        }
        elements = []
        element_list = []
        try:
            index = int(input[2])
            processes = psutil.net_connections()
            for line in processes:
                p = line.laddr
                if p[1] == 4723 and driver is not None:
                    driver_flag = True
                    break
            if driver_flag is True:
                elem_count = 0
                if len(visible_text) > 0:
                    for item in classes[object_name]:
                        xpath_str = '//'+item+'[@text="'+visible_text+'"]'
                        element_list = element_list + driver.find_elements_by_xpath(xpath_str)
                else:
                    for item in classes[object_name]:
                        element_list = element_list + driver.find_elements_by_class_name(item)
                if index < len(element_list):
                    element = element_list[index]
                else:
                    logger.print_on_console("The custom element with index '"+str(index)+"' not found on the Screen!! Please make sure the element is visible on the screen")
                if len(input) == 3:
                    input = [""]
                elif len(input) > 3:
                    input = input[3:]
            else:
                logger.print_on_console("The driver is not running!! Please launch or install the application to continue")
        except Exception as e:
            log.error(e, exc_info=True)
            logger.print_on_console("Error in fetching the Custom Element")
        return element,input