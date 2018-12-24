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
import Number_picker_Keywords
import swipe_keywords
import toggle_keywords
import device_keywords
import logging
import seekBar_Mobility
import logger
from mobile_app_constants import *
from constants import *
import action_keyowrds_app
import mob_screenshot
import readconfig
import spinner_keywords
import list_view_mobility
import DatePicker_Keywords_Mobility
import TimePicker_Keywords_Mobility
import picker_wheel_ios
import table_keywords_native
import socket
import commands
import os
import subprocess
import platform
import time
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
    table_keywords_object=table_keywords_native.Table_Keywords()
    date_keywords_object=DatePicker_Keywords_Mobility.Date_Keywords()
    time_keywords_object=TimePicker_Keywords_Mobility.Time_Keywords()
    number_picker_object=Number_picker_Keywords.Number_Picker()
    seekBar_object=seekBar_Mobility.Seek_Bar_Keywords()
    def __init__(self):
        self.exception_flag=''


    def dispatcher(self,teststepproperty,input,reporting_obj):

        global ELEMENT_FOUND
        #result=(TEST_RESULT_FAIL,TEST_RESULT_FALSE)

        objectname = teststepproperty.objectname
        object_name_ios = objectname





        output = teststepproperty.outputval
        objectname = objectname.strip()


        keyword = teststepproperty.name.lower()
        #hello= teststepproperty.custname
        #print keyword
        #print input

        global apptypes
        apptypes=teststepproperty.apptype
        err_msg=None
        result=[TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,err_msg]

        try:
            dict={'settext':self.textbox_keywords_object.set_text,
                    'cleartext' : self.textbox_keywords_object.clear_text,
                    'setsecuretext' : self.textbox_keywords_object.setsecuretext,
                    'sendvalue' : self.textbox_keywords_object.send_value,
                    'gettext' : self.textbox_keywords_object.get_text,
                    'verifytext' : self.textbox_keywords_object.verify_text,
                    'gettextboxlength': self.textbox_keywords_object.get_textBoxLength,
                    'verifytextboxlength' : self.textbox_keywords_object.verify_textBoxLength,
                    'selectradiobutton' : self.radio_button_object.select_radio_button,
                    'getstatus' : self.radio_button_object.get_status,
                    'selectcheckbox' : self.radio_button_object.select_checkbox,
                    'unselectcheckbox' : self.radio_button_object.unselect_checkbox,
                    'press' : self.button_link_object.press,
                    'longpress' : self.button_link_object.long_press,
                    'getbuttonname' : self.button_link_object.get_button_name,
                    'verifybuttonname' : self.button_link_object.verify_button_name,
                    'installapplication' : self.install_and_launch_object.installApplication,
                    'launchapplication' : self.install_and_launch_object.installApplication,
                    'uninstallapplication' : self.install_and_launch_object.uninstallApplication,
                    'closeapplication' : self.install_and_launch_object.closeApplication,
                    'swipeleft' : self.swipe_keywords_object.swipe_left,
                    'swiperight': self.swipe_keywords_object.swipe_right,
                    'swipeup': self.swipe_keywords_object.swipe_up,
                    'swipedown': self.swipe_keywords_object.swipe_down,
                    'toggleon' : self.toggle_keywords_object.toggle_on,
                    'toggleoff':self.toggle_keywords_object.toggle_off,
                    'verifyenabled' : self.slider_util_keywords_object.verify_enabled,
                    'verifydisabled' : self.slider_util_keywords_object.verify_disabled,
                    'verifyvisible' : self.slider_util_keywords_object.verify_visible,
                    'verifyhidden' : self.slider_util_keywords_object.verify_hidden,
                    'verifyexists' : self.slider_util_keywords_object.verify_exists,
                    'getdevices' : self.device_keywords_object.get_device_list,
                    'invokedevice' : self.device_keywords_object.invoke_device,
                    'stopserver':self.install_and_launch_object.stop_server,
                    'hidesoftkeyboard':self.swipe_keywords_object.hide_soft_keyboard,
                    'backpress':self.swipe_keywords_object.backPress,
                    'presselement':self.button_link_object.press,
                    'longpresselement':self.button_link_object.long_press,
                    'getelementtext':self.textbox_keywords_object.get_text,
                    'setslidevalue': self.slider_util_keywords_object.set_slide_value,
                    'getslidevalue': self.slider_util_keywords_object.get_slide_value,
                    'verifyelementexists':self.slider_util_keywords_object.verify_exists,
                    'verifyelementdisabled':self.slider_util_keywords_object.verify_disabled,
                    'verifyelementdoesnotexists':self.slider_util_keywords_object.verify_does_not_exists,
                    'verifyelementenabled':self.slider_util_keywords_object.verify_exists,
                    'verifyelementtext':self.textbox_keywords_object.verify_text,
                    'actionkey':self.action_keyowrds_object.action_key,
                    'waitforelementexists':self.slider_util_keywords_object.waitforelement_exists,
                    'getcount':self.spinner_keywords_object.get_count,
                    'verifycount':self.spinner_keywords_object.verify_count,
                    'selectvaluebyindex':self.spinner_keywords_object.select_value_by_index,
                    'selectvaluebytext':self.spinner_keywords_object.select_value_by_text,
                    'getmultiplevaluesbyindexes':self.spinner_keywords_object.get_multiple_values_by_indexs,
                    'getvaluebyindex':self.spinner_keywords_object.get_value_by_index,
                    'getallvalues':self.spinner_keywords_object.get_all_values,
                    'verifyallvalues':self.spinner_keywords_object.verify_all_values,
                    'getselectedvalue':self.spinner_keywords_object.get_selected_value,
                    'verifyselectedvalue':self.spinner_keywords_object.verify_selected_value,
                    'getlistcount':self.list_view_keywords_object.get_list_count,
                    'verifylistcount':self.list_view_keywords_object.verify_list_count,
                    'selectviewbyindex':self.list_view_keywords_object.select_view_by_index,
                    'selectviewbytext':self.list_view_keywords_object.select_view_by_text,
                    'getmultipleviewsbyindexes':self.list_view_keywords_object.get_multiple_views_by_indexs,
                    'getviewbyindex':self.list_view_keywords_object.get_list_view_by_index,
                    'getallviews':self.list_view_keywords_object.get_all_views,
                    'verifyallviews':self.list_view_keywords_object.verify_all_views,
                    'getselectedviews':self.list_view_keywords_object.get_selected_views,
                    'verifyselectedviews':self.list_view_keywords_object.verify_selected_views,
                    'selectmultipleviewsbyindexes':self.list_view_keywords_object.select_multiple_views_by_indexes,
                    'selectmultipleviewsbytext':self.list_view_keywords_object.select_multiple_views_by_text,
                    'setvalue': self.picker_wheel_keywords_object.set_value,
                    'getvalue': self.picker_wheel_keywords_object.get_value,
                    'getrowcount':self.table_keywords_object.get_row_count,
                    'verifyrowcount':self.table_keywords_object.verify_row_count,
                    'cellclick':self.table_keywords_object.cell_click,
                    'getcellvalue':self.table_keywords_object.get_cell_value,
                    'verifycellvalue':self.table_keywords_object.verify_cell_value,
                    'setdate' : self.date_keywords_object.Set_Date,
                    'getdate' : self.date_keywords_object.Get_Date,
                    'settime' : self.time_keywords_object.Set_Time,
                    'gettime' : self.time_keywords_object.Get_Time,
                    'setnumber':self.number_picker_object.Select_Number,
                    'setminvalue':self.seekBar_object.Set_Min_Value,
                    'setminvalue':self.seekBar_object.Set_Mid_Value,
                    'setmaxvalue':self.seekBar_object.Set_Max_Value


                }
            ELEMENT_FOUND=True
            if keyword in dict.keys():



                # input[0]=bundleid,input[1]=os version ,input[2]=IP,,input[3]=device_name
                if platform.system() == 'Darwin':


                    #current_dir = (os.getcwd())
                    dir_path = os.path.dirname(os.path.realpath(__file__))



                    # set IP
                    if (commands.getoutput('pgrep xcodebuild') == ''):

                        try:

                            with open(
                                            dir_path + "/Nineteen68UITests/data.txt",
                                    'wb') as f:
                                f.write(input[2])  # send IP
                        except Exception as e:
                            print e

                        # set run command
                        try:

                            with open(dir_path + "/run.command", "wb") as f:
                                f.write("#! /bin/bash \n")
                                f.write(
                                    "cd " + dir_path + "\n")
                                f.write(
                                    "xcodebuild -workspace Nineteen68.xcworkspace -scheme Nineteen68 -destination name=" +
                                    input[3] + " OS=" + input[1] + " test")

                        except Exception as e:
                            print e

                        # subprocess.call("chmod a+x run.command")
                        try:


                            subprocess.Popen( dir_path +"/run.command", shell=True)
                            #time.sleep(20)
                        except:
                            print "xcode server is down"




                    if(keyword == "launchapplication"):
                        global ip
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
                    while True:
                        try:
                            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            clientsocket.connect((ip, 8022))
                            clientsocket.send("execu")
                            break
                        except:
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




                    data = clientsocket.recv(100000)
                    string_data = data.decode('utf-8')



                    if (keyword == "launchapplication" and string_data == ""):
                        result = MobileDispatcher().dispatcher(teststepproperty,input,reporting_obj)
                        return result

                    if ( string_data == "" ):
                        result = MobileDispatcher().dispatcher(teststepproperty,input,reporting_obj)
                        return result


                    if string_data == "error":
                        data = clientsocket.recv(100000)
                        string_data = data.decode('utf-8')
                        log.error(string_data)
                        logger.print_on_console(string_data)
                        status = TEST_RESULT_FAIL
                        result1 = False
                        output = None
                        err_msg = None


                    elif string_data == ("passval") or string_data == ("pass"):
                        if string_data == ("passval"):
                            data = clientsocket.recv(100000)
                            string_data = data.decode('utf-8')
                            output = string_data

                            #print output
                        if string_data == ("pass"):
                            output = None
                        status = TEST_RESULT_PASS
                        result1 = True
                        err_msg = None
                    else:
                        status = TEST_RESULT_FAIL
                        result1 = False
                        output = None
                        err_msg = None
                    result=(status,result1,output,err_msg)

                else:
                    driver = install_and_launch.driver
                    if keyword==WAIT_FOR_ELEMENT_EXISTS:
                        result=dict[keyword](objectname,input)
                    else:
                        webelement=self.getMobileElement(driver,objectname)
                        result=dict[keyword](webelement,input)
                if not(ELEMENT_FOUND) and self.exception_flag:
                    result=TERMINATE
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
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            import traceback
            log.error(e)
            #logger.print_on_console('Exception at dispatcher')
        return result

    def getMobileElement(self,driver,objectname):
        objectname = str(objectname)
        mobileElement = None
        global ELEMENT_FOUND
        if objectname.strip() != '':
            import platform
            if SYSTEM_OS=='Darwin':
                objectname = objectname.replace("/AppiumAUT[1]/", "/")
                print objectname
            identifiers = objectname.split(';')
            log.debug('Identifiers are ')
            log.debug(identifiers)
            try:
                log.debug('trying to find mobileElement by Id')
                import platform
                if SYSTEM_OS=='Darwin':
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
