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
    def __init__(self):
        self.exception_flag=''

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
        'setvalue': seekBar_object.Set_Mid_Value,
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

    def dispatcher(self,teststepproperty,input,reporting_obj):

        global ELEMENT_FOUND,apptypes,ip
        #result=(TEST_RESULT_FAIL,TEST_RESULT_FALSE)

        objectname = teststepproperty.objectname
        object_name_ios = objectname





        output = teststepproperty.outputval
        objectname = objectname.strip()


        keyword = teststepproperty.name.lower()
        #hello= teststepproperty.custname
        #print keyword
        #print input

        apptypes=teststepproperty.apptype
        err_msg=None
        result=[TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,err_msg]

        try:
            ELEMENT_FOUND=True
            if keyword in list(self.mob_dict.keys()):


#################################                 IOS                ###################################
                # input[0]=bundleid,input[1]=os version ,input[2]=IP,,input[3]=device_name
                if SYSTEM_OS == 'Darwin':


                    #current_dir = (os.getcwd())
                    dir_path = os.path.dirname(os.path.realpath(__file__))



                    # set IP
                    if (subprocess.getoutput('pgrep xcodebuild') == ''):

                        try:

                            with open(
                                            dir_path + "/Nineteen68UITests/data.txt",
                                    'wb') as f:
                                f.write(input[2])  # send IP
                        except Exception as e:
                            log.error(e)

                    # set run command
                        input[3] = input[3].split(" ")
                        input[3] = "\ ".join(input[3])
                        if (input[3].split("=")[0] == "id"):
                            name = input[3]
                        else:
                            name = "name=" + input[3]

                        try:
                            with open(dir_path + "/run.command", "wb") as f:
                                f.write("#! /bin/bash \n")
                                f.write(
                                    "cd " + dir_path + "\n")
                                f.write(
                                    "xcodebuild -workspace Nineteen68.xcworkspace -scheme Nineteen68 -destination " +
                                    name + " OS=" + input[1] +" >/dev/null "+ " test")

                        except Exception as e:
                            log.error(e)

                        # subprocess.call("chmod a+x run.command")
                        try:
                            subprocess.Popen( dir_path +"/run.command", shell=True)

                        except:
                            log.error(ERROR_CODE_DICT["ERR_XCODE_DOWN"])

                    if(keyword == "launchapplication"):
                        ip = input[2]


                    if object_name_ios == " " or keyword == "launchapplication":
                        label = ""
                        label_type = ""
                    else:
                        label = object_name_ios.split("&$#")[0]
                        label_type =object_name_ios.split("&$#")[1]

                    input_text=input[0]
                    #print "keyword = "+ keyword
                    #print "label = "+ label
                    #print "labeltype = "+ label_type
                    #print "input = "+ input_text


                    length_keyword = len(keyword.encode('utf-8'))
                    length_input_text = len(input_text.encode('utf-8'))
                    try:
                        length_label = len(label.encode('utf-8'))
                    except:
                        length_label = len(label.decode('utf-8').encode('utf-8'))

                    length_label_type = len(label_type.encode('utf-8'))


                    # create socket
                    timer = 0
                    while True:
                        try:
                            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            clientsocket.connect((ip, 8022))
                            clientsocket.send(XCODE_EXECUTE)
                            break
                        except:
                            timer+=1
                            if timer == 130:
                                log.error(ERROR_CODE_DICT["ERR_TIMEOUT"])
                                break
                            time.sleep(1)


                    # keyword
                    clientsocket.send(str(len(str(length_keyword))))
                    clientsocket.send(str(length_keyword))
                    clientsocket.send(keyword)

                    # label
                    if label == "":
                        clientsocket.send("0")
                    else:
                        clientsocket.send(str(len(str(length_label))))
                        clientsocket.send(str(length_label))
                        clientsocket.send(label)

                    # label type
                    if label_type == "":
                        clientsocket.send("0")
                    else:
                        clientsocket.send(str(len(str(length_label_type))))
                        clientsocket.send(str(length_label_type))
                        clientsocket.send(label_type)

                    # input
                    if input_text == "":
                        clientsocket.send("0")
                    else:
                        clientsocket.send(str(len(str(length_input_text))))
                        clientsocket.send(str(length_input_text))
                        clientsocket.send(input_text)
                    #edit
                    EOF="terminate"
                    fragments=""
                    while True:
                        chunck = clientsocket.recv(10000)
                        if chunck.endswith(EOF):
                            idx = chunck.index(EOF)
                            fragments += chunck[:idx]
                            break
                        fragments += chunck

                    img_data = fragments.split("!@#$%^&*()")[0]
                    data = fragments.split("!@#$%^&*()")[1]
                    try:
                        string_value = fragments.split("!@#$%^&*()")[2]
                    except:
                        string_value = ""

                    #edit

                    string_data = data.decode('utf-8')



                    if (keyword == "launchapplication" and string_data == ""):
                        result = MobileDispatcher().dispatcher(teststepproperty,input,reporting_obj)
                        return result

                    if ( string_data == "" ):
                        result = MobileDispatcher().dispatcher(teststepproperty,input,reporting_obj)
                        return result


                    if string_data == XCODE_ERROR:
                        log.error(string_value)
                        logger.print_on_console(string_value)
                        status = TEST_RESULT_FAIL
                        result1 = TEST_RESULT_FALSE
                        output = None
                        err_msg = None


                    elif string_data == (XCODE_PASSVALUE) or string_data == (XCODE_PASS):
                        if string_data == (XCODE_PASSVALUE):
                            string_value = string_value.decode('utf-8')
                            output = string_value

                            #print output
                        if string_data == (XCODE_PASS):
                            output = None
                        status = TEST_RESULT_PASS
                        result1 = TEST_RESULT_TRUE
                        err_msg = None
                    else:
                        status = TEST_RESULT_FAIL
                        result1 = False
                        output = None
                        err_msg = None
                    result=(status,result1,output,err_msg)
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
                            import base64
                            try:
                                if img_data == "":
                                        log.error("screenshot capture failed")
                                else:
                                    img_data += "=" * ((4 - len(img_data) % 4) % 4)
                                    png_recovered = base64.decodestring(img_data)
                                    f = open(file_path[2], "w")
                                    f.write(png_recovered)
                                    f.close()
                            except Exception as e:
                                log.error(e)


#################################                 Android                ###################################
                else:
                    driver = android_scrapping.driver
                    if teststepproperty.custname == "@Android_Custom":
                        if (input[0] and (input[1] is not None) and input[2]):
                            logger.print_on_console("Element type is ",input[0])
                            logger.print_on_console("Visible text is ",input[1])
                            logger.print_on_console("Index is ",input[2])
                            if self.custom_object.custom_check(input,keyword) == False:
                                logger.print_on_console("The object and the keyword do not match")
                                result=TERMINATE
                            elif (keyword==WAIT_FOR_ELEMENT_EXISTS):
                                result=self.custom_object.waitforelement_exists(input)
                            else:
                                element,input=self.custom_object.custom_element(input,keyword)
                                result=self.mob_dict[keyword](element,input)
                        else:
                            logger.print_on_console(INVALID_INPUT,": NULL object used in input")
                            result[3]=INVALID_INPUT+": NULL object used in input"
                    elif keyword==WAIT_FOR_ELEMENT_EXISTS:
                        result=self.mob_dict[keyword](objectname,input)
                    else:
                        element, xpath=self.getMobileElement(driver,objectname)
                        result=self.mob_dict[keyword](element,input,xpath)
                if not(ELEMENT_FOUND) and self.exception_flag:
                    result=TERMINATE
            else:
                err_msg=INVALID_KEYWORD
                result[3]=err_msg
            if keyword not in NON_WEBELEMENT_KEYWORDS:
                if SYSTEM_OS != "Darwin":
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
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console('Exception at dispatcher')
        return result

    def getMobileElement(self,driver,objectname):
        objectname = str(objectname)
        mobileElement = None
        global ELEMENT_FOUND
        xpath = None
        if objectname.strip() != '':
            if SYSTEM_OS=='Darwin':
                objectname = objectname.replace("/AppiumAUT[1]/", "/")
                print(objectname)
            identifiers = objectname.split(';')
            id = identifiers[0]
            xpath = identifiers[1]
            log.debug('Identifiers are ')
            log.debug(identifiers)
            try:
                log.debug('trying to find mobileElement by xpath')
                import platform
                if SYSTEM_OS=='Darwin':
                    mobileElement = driver.find_element_by_xpath(objectname)
                else:
                    mobileElement = driver.find_element_by_xpath(xpath)
            except Exception as Ex:
                log.debug(str(Ex))
                log.debug('Element not found by xpath')
                if (id):
                    try:
                        log.debug('trying to find mobileElement by id')
                        mobileElement = driver.find_element_by_id(id)
                    except Exception as Ex:
                        log.debug('Element not found')
                        log.debug(str(Ex))
        if mobileElement==None:
            ELEMENT_FOUND=False
        return mobileElement, xpath
