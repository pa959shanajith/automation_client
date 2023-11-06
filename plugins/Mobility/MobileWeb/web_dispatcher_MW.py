#-------------------------------------------------------------------------------
# Name:        web_dispatcher_MW.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import button_link_keyword_MW
import popup_keywords_MW
import browser_Keywords_MW
import radio_checkbox_operations_MW
import table_keywords_MW
import utilweb_operations_MW
import element_operations_MW
import textbox_operations_MW
import dropdown_listbox_MW
import static_text_keywords_MW
import device_keywords_MW
import mob_screenshot_web
import threading
import logger
import subprocess
from webconstants_MW import *
import custom_keyword_MW
import screenshot_keywords
from collections import OrderedDict
from constants import *
import action_keyowrds_web
import requests
import readconfig
import re
import web_keywords_MW
import browserstack_web_keywords
from selenium import webdriver  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import logging
local_wk=threading.local()

log = logging.getLogger('web_dispatcher_MW.py')

class Dispatcher:

    button_link_object = button_link_keyword_MW.ButtonLinkKeyword()
    popup_object = popup_keywords_MW.PopupKeywords()
    browser_object = browser_Keywords_MW.BrowserKeywords()
    radio_checkbox_object = radio_checkbox_operations_MW.RadioCheckboxKeywords()
    table_object = table_keywords_MW.TableOperationKeywords()
    element_object = element_operations_MW.ElementKeywords()
    textbox_object = textbox_operations_MW.TextboxKeywords()
    dropdown_list_object = dropdown_listbox_MW.DropdownKeywords()
    util_object = utilweb_operations_MW.UtilWebKeywords()
    action_keyowrds_object=action_keyowrds_web.Action_Key_App()
    statict_text_object = static_text_keywords_MW.StaticTextKeywords()
    custom_object=custom_keyword_MW.CustomKeyword()
    device_keywords_object = device_keywords_MW.Device_Keywords()
    webelement_map=OrderedDict()
    
    button_link_object_sl = web_keywords_MW.Button_link_Keywords()
    popup_object_sl = web_keywords_MW.Browser_Popup_Keywords()
    radio_check_obj_sl = web_keywords_MW.Radio_checkbox_Keywords()
    table_obj_sl = web_keywords_MW.Table_Keywords()
    element_obj_sl = web_keywords_MW.Element_Keywords()
    textbox_obj_sl = web_keywords_MW.Textbox_Keywords()
    dropdown_obj_sl = web_keywords_MW.Dropdown_Keywords()
    util_obj_sl = web_keywords_MW.Util_Keywords()
    browser_object_sl = web_keywords_MW.BrowserKeywords()

    MW_dict={
        'getobjectcount':custom_object.get_object_count,
        'click': button_link_object.click,
        'verifybuttonname' : button_link_object.verify_button_name,
        'getbuttonname' : button_link_object.get_button_name,
        'getlinktext'    : button_link_object.get_link_text,
        'verifylinktext' : button_link_object.verify_link_text,
        'press'  : button_link_object.press,
        'doubleclick' : button_link_object.double_click,
        'rightclick' : button_link_object.right_click,
        'uploadfile'  : button_link_object.upload_file,

        'acceptpopup' : popup_object.accept_popup,
        'dismisspopup':popup_object.dismiss_popup,
        'getpopuptext':popup_object.get_popup_text,
        'verifypopuptext':popup_object.verify_popup_text,
        'getdevices' : device_keywords_object.get_device_list,
        'invokedevice' : device_keywords_object.invoke_device,


        'getstatus': radio_checkbox_object.get_status,
        'selectradiobutton': radio_checkbox_object.select_radiobutton,
        'selectcheckbox': radio_checkbox_object.select_checkbox,
        'unselectcheckbox': radio_checkbox_object.unselect_checkbox,

        'getrowcount' : table_object.getRowCount,
        'getcolumncount' : table_object.getColoumnCount,
        'getcellvalue' : table_object.getCellValue,
        'verifycellvalue' : table_object.verifyCellValue,
        'cellclick' : table_object.cellClick,
        'getrownumbytext' : table_object.getRowNumByText,
        'getcolnumbytext' : table_object.getColNumByText,
        'getinnertable' : table_object.getInnerTable,
        'verifycelltooltip' : table_object.verifyCellToolTip,


        'getelementtext' : element_object.get_element_text,
        'verifyelementtext' : element_object.verify_element_text,
        'clickelement' : element_object.click_element,
        'gettooltiptext' : element_object.get_tooltip_text,
        'verifytooltiptext' :element_object.verify_tooltip_text,
        'drag':element_object.drag,
        'drop':element_object.drop,

        'settext':textbox_object.set_text,
        'sendvalue':textbox_object.send_value,
        'gettext':textbox_object.get_text,
        'verifytext':textbox_object.verify_text,
        'cleartext':textbox_object.clear_text,
        'gettextboxlength':textbox_object.gettextbox_length,
        'verifytextboxlength':textbox_object.verifytextbox_length,
        'setsecuretext':textbox_object.setsecuretext,
        'sendsecurevalue':textbox_object.sendSecureValue,

        'selectvaluebyindex':dropdown_list_object.selectValueByIndex,
        'getcount':dropdown_list_object.getCount,
        'selectvaluebytext':dropdown_list_object.selectValueByText,
        ## defect 360
        'verifyselectedvalue':dropdown_list_object.verifySelectedValue,
        'verifyselectedvalues':dropdown_list_object.verifySelectedValues,
        'verifycount':dropdown_list_object.verifyCount,
        'selectallvalues':dropdown_list_object.selectAllValues,
        'selectmultiplevaluesbyindexes':dropdown_list_object.selectMultipleValuesByIndexes,
        'getselected':dropdown_list_object.getSelected,
        'selectmultiplevaluesbytext':dropdown_list_object.selectMultipleValuesByText,
        'getmultiplevaluesbyindexes':dropdown_list_object.getMultipleValuesByIndexes,
        'verifyallvalues':dropdown_list_object.verifyAllValues,
        'getvaluebyindex':dropdown_list_object.getValueByIndex,
        'verifyvaluesexists':dropdown_list_object.verifyValuesExists,
        'deselectall':dropdown_list_object.deselectAll,
        'selectbyabsolutevalue':dropdown_list_object.selectByAbsoluteValue,
        'getallvalues':dropdown_list_object.getAllValues,


        'verifyvisible':util_object.verify_visible,
        'verifyexists':util_object.verify_exists,
        'verifydoesnotexists':util_object.verify_doesnot_exists,
        'verifyenabled':util_object.verify_enabled,
        'verifydisabled':util_object.verify_disabled,
        'verifyhidden':util_object.verify_hidden,
        'verifyreadonly':util_object.verify_readonly,
        'setfocus':util_object.setfocus,
        'tab':util_object.tab,
        'actionkey':action_keyowrds_object.action_key,
        'iossendkey': util_object.iossendkey,
        'mouseclick':util_object.mouse_click,
        'verifywebimages':util_object.verify_web_images,
        'imagesimilaritypercentage':util_object.image_similarity_percentage,
        'waitforelementvisible':element_object.waitforelement_visible,
        'getelementtagvalue': util_object.get_element_tag_value,

           
        # Added getAttributeValue and verifyAttribute keywords
        'getattributevalue': util_object.get_attribute_value,
        'verifyattribute': util_object.verify_attribute,



        'openbrowser':browser_object.openBrowser,
        'opennewtab':browser_object.openNewTab,
        'navigatetourl':browser_object.navigateToURL,
        # 'opennewbrowser':browser_object.openNewBrowser,
        'getpagetitle':browser_object.getPageTitle,
        'getcurrenturl':browser_object.getCurrentURL,
        'refresh':browser_object.refresh,
        'verifycurrenturl':browser_object.verifyCurrentURL,
        'closebrowser':browser_object.closeBrowser,
        'closesubwindows':browser_object.closeSubWindows,
        'switchtowindow':browser_object.switch_to_window,
        'verifytextexists':statict_text_object.verify_text_exists,
        'verifypagetitle':browser_object.verify_page_title,
        'clearcache':browser_object.clear_cache,
        'navigateback':browser_object.navigate_back,
        'navigatewithauthenticate':browser_object.navigate_with_authenticate,
        
    }

    sauce_mobile_web_dict = {
        'click': button_link_object.click,
        'press': button_link_object.press,
        'doubleClick': button_link_object.double_click,
        'rightClick': button_link_object.right_click,
        'verifyButtonName': button_link_object.verify_button_name,
        'getButtonName': button_link_object.get_button_name,
        'getLinkText': button_link_object.get_link_text,
        'verifyLinkText': button_link_object.verify_link_text,
        'uploadfile': button_link_object.upload_file,


        'acceptPopUp':  popup_object.accept_popup,
        'dismissPopUp': popup_object.dismiss_popup,
        'getPopUpText': popup_object.get_popup_text,
        'verifyPopUpText': popup_object.verify_popup_text,


        'getStatus':  radio_checkbox_object.get_status,
        'selectRadioButton': radio_checkbox_object.select_radiobutton,
        'selectCheckbox': radio_checkbox_object.select_checkbox,
        'unselectCheckbox': radio_checkbox_object.unselect_checkbox,


        'getRowCount': table_object.getRowCount,
        'getColumnCount': table_object.getColoumnCount,
        'getCellValue': table_object.getCellValue,
        'verifyCellValue': table_object.verifyCellValue,
        'cellClick': table_object.cellClick,
        'getRowNumByText': table_object.getRowNumByText,
        'getColNumByText': table_object.getColNumByText,
        'getInnerTable': table_object.getInnerTable,
        'verifyCellToolTip': table_object.verifyCellToolTip,

        'getElementText':  element_object.get_element_text,
        'verifyElementText': element_object.verify_element_text,
        'clickElement': element_object.click_element,
        'getToolTipText': element_object.get_tooltip_text,
        'verifyToolTipText': element_object.verify_tooltip_text,
        'setText': textbox_object.set_text,
        # 'setText': textbox_obj_sl.setText,
        'sendValue': textbox_object.send_value,
        'getText': textbox_object.get_text,
        # 'getText': textbox_obj_sl.getText,
        'verifyText': textbox_object.verify_text,
        'clearText': textbox_object.clear_text,
        # 'clearText': textbox_obj_sl.clearText,
        'getTextboxLength': textbox_object.gettextbox_length,
        'verifyTextboxLength': textbox_object.verifytextbox_length,
        'setSecureText': textbox_object.setsecuretext,
        'sendSecureValue': textbox_object.sendSecureValue,
        'selectValueByIndex': dropdown_list_object.selectValueByIndex,
        'getCount': dropdown_list_object.getCount,
        'selectValueByText': dropdown_list_object.selectValueByText,
        'verifySelectedValues': dropdown_list_object.verifySelectedValues,
        'verifySelectedValue': dropdown_list_object.verifySelectedValue,
        'verifyCount': dropdown_list_object.verifyCount,
        'selectAllValues': dropdown_list_object.selectAllValues,
        'selectMultipleValuesByIndexes': dropdown_list_object.selectMultipleValuesByIndexes,
        'getSelected': dropdown_list_object.getSelected,
        'selectMultipleValuesByText': dropdown_list_object.selectMultipleValuesByText,
        'getMultipleValuesByIndexes': dropdown_list_object.getMultipleValuesByIndexes,
        'verifyAllValues': dropdown_list_object.verifyAllValues,
        'selectByAbsoluteValue': dropdown_list_object.selectByAbsoluteValue,
        'getAllValues': dropdown_list_object.getAllValues,
        'getValueByIndex': dropdown_list_object.getValueByIndex,
        'verifyValuesExists': dropdown_list_object.verifyValuesExists,
        'deselectAll': dropdown_list_object.deselectAll,
        'actionkey': action_keyowrds_object.action_key,

        'drag': element_object.drag,
        'drop': element_object.drop,
        'verifyVisible': util_object.verify_visible,
        'verifyExists': util_object.verify_exists,
        'verifyDoesNotExists': util_object.verify_doesnot_exists,
        'verifyEnabled': util_object.verify_enabled,
        'verifyDisabled': util_object.verify_disabled,
        'verifyHidden': util_object.verify_hidden,
        'verifyReadOnly': util_object.verify_readonly,
        'tab': util_object.tab,
        'waitForElementVisible': element_object.waitforelement_visible,
        'setFocus': util_object.setfocus,
        'getElementTagValue':  util_object.get_element_tag_value,
        'getAttributeValue':  util_object.get_attribute_value,
        'verifyAttribute': util_object.verify_attribute,

        'openBrowser': browser_object_sl.openBrowser,
        'openNewTab': browser_object.openNewTab,
        'navigateToURL': browser_object.navigateToURL,
        'getPageTitle': browser_object.getPageTitle,
        'getCurrentURL': browser_object.getCurrentURL,
        'refresh': browser_object.refresh,
        'verifyCurrentURL': browser_object.verifyCurrentURL,
        'closeBrowser': browser_object_sl.closeBrowser,
        'closeSubWindows': browser_object.closeSubWindows,
        'switchToWindow': browser_object.switch_to_window,
        'verifyTextExists': statict_text_object.verify_text_exists,
        'verifyPageTitle': browser_object.verify_page_title,
        'clearCache': browser_object.clear_cache,
        'navigateBack': browser_object.navigate_back,
        'navigateWithAuthenticate': browser_object.navigate_with_authenticate,
    }

    Browserstack_mobile_web_dict = {

        'click': button_link_object.click,
        'press': button_link_object.press,
        'doubleClick': button_link_object.double_click,
        'rightClick': button_link_object.right_click,
        'verifyButtonName': button_link_object.verify_button_name,
        'getButtonName': button_link_object.get_button_name,
        'getLinkText': button_link_object.get_link_text,
        'verifyLinkText': button_link_object.verify_link_text,
        'uploadfile': button_link_object.upload_file,

        'acceptPopUp':  popup_object.accept_popup,
        'dismissPopUp': popup_object.dismiss_popup,
        'getPopUpText': popup_object.get_popup_text,
        'verifyPopUpText': popup_object.verify_popup_text,

        'getStatus':  radio_checkbox_object.get_status,
        'selectRadioButton': radio_checkbox_object.select_radiobutton,
        'selectCheckbox': radio_checkbox_object.select_checkbox,
        'unselectCheckbox': radio_checkbox_object.unselect_checkbox,

        'getRowCount': table_object.getRowCount,
        'getColumnCount': table_object.getColoumnCount,
        'getCellValue': table_object.getCellValue,
        'verifyCellValue': table_object.verifyCellValue,
        'cellClick': table_object.cellClick,
        'getRowNumByText': table_object.getRowNumByText,
        'getColNumByText': table_object.getColNumByText,
        'getInnerTable': table_object.getInnerTable,
        'verifyCellToolTip': table_object.verifyCellToolTip,

        'getElementText':  element_object.get_element_text,
        'verifyElementText': element_object.verify_element_text,
        'clickElement': element_object.click_element,
        'getToolTipText': element_object.get_tooltip_text,
        'verifyToolTipText': element_object.verify_tooltip_text,
        'setText': textbox_object.set_text,
        'sendValue': textbox_object.send_value,
        'getText': textbox_object.get_text,

        'verifyText': textbox_object.verify_text,
        'clearText': textbox_object.clear_text,

        'getTextboxLength': textbox_object.gettextbox_length,
        'verifyTextboxLength': textbox_object.verifytextbox_length,
        'setSecureText': textbox_object.setsecuretext,
        'sendSecureValue': textbox_object.sendSecureValue,
        'selectValueByIndex': dropdown_list_object.selectValueByIndex,
        'getCount': dropdown_list_object.getCount,
        'selectValueByText': dropdown_list_object.selectValueByText,
        'verifySelectedValues': dropdown_list_object.verifySelectedValues,
        'verifySelectedValue': dropdown_list_object.verifySelectedValue,
        'verifyCount': dropdown_list_object.verifyCount,
        'selectAllValues': dropdown_list_object.selectAllValues,
        'selectMultipleValuesByIndexes': dropdown_list_object.selectMultipleValuesByIndexes,
        'getSelected': dropdown_list_object.getSelected,
        'selectMultipleValuesByText': dropdown_list_object.selectMultipleValuesByText,
        'getMultipleValuesByIndexes': dropdown_list_object.getMultipleValuesByIndexes,
        'verifyAllValues': dropdown_list_object.verifyAllValues,
        'selectByAbsoluteValue': dropdown_list_object.selectByAbsoluteValue,
        'getAllValues': dropdown_list_object.getAllValues,
        'getValueByIndex': dropdown_list_object.getValueByIndex,
        'verifyValuesExists': dropdown_list_object.verifyValuesExists,
        'deselectAll': dropdown_list_object.deselectAll,
        'actionkey': action_keyowrds_object.action_key,
 
        'drag': element_object.drag,
        'drop': element_object.drop,
        'verifyVisible': util_object.verify_visible,
        'verifyExists': util_object.verify_exists,
        'verifyDoesNotExists': util_object.verify_doesnot_exists,
        'verifyEnabled': util_object.verify_enabled,
        'verifyDisabled': util_object.verify_disabled,
        'verifyHidden': util_object.verify_hidden,
        'verifyReadOnly': util_object.verify_readonly,
        'tab': util_object.tab,
        'waitForElementVisible': element_object.waitforelement_visible,
        'setFocus': util_object.setfocus,
        'getElementTagValue':  util_object.get_element_tag_value,
        'getAttributeValue':  util_object.get_attribute_value,
        'verifyAttribute': util_object.verify_attribute,
 
        'openBrowser': browser_object.openBrowser_BrowserStack,
        'openNewTab': browser_object.openNewTab,
        'navigateToURL': browser_object.navigateToURL,
        'getPageTitle': browser_object.getPageTitle,
        'getCurrentURL': browser_object.getCurrentURL,
        'refresh': browser_object.refresh,
        'verifyCurrentURL': browser_object.verifyCurrentURL,
        'closeBrowser': browser_object.closeBrowser_BrowserStack,
        'closeSubWindows': browser_object.closeSubWindows,
        'switchToWindow': browser_object.switch_to_window,
        'verifyTextExists': statict_text_object.verify_text_exists,
        'verifyPageTitle': browser_object.verify_page_title,
        'clearCache': browser_object.clear_cache,
        'navigateBack': browser_object.navigate_back,
        'navigateWithAuthenticate': browser_object.navigate_with_authenticate,
    }

    def __init__(self):
        self.exception_flag=''
        self.action=None
        self.sauce_conf = web_keywords_MW.Sauce_Config().get_sauceconf()
        self.browserstack_conf = browserstack_web_keywords.Browserstack_config().get_browserstackconf()

    def dispatcher(self,teststepproperty,input,reporting_obj,mythread,execution_env):
        global simple_debug_gwto, status_gwto
        status_gwto =False
        simple_debug_gwto=False
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        url = teststepproperty.url.strip() if(hasattr(teststepproperty, 'url')) else ""
        keyword = teststepproperty.name.lower()
        driver = browser_Keywords_MW.driver_obj
        webelement = None
        element = None
        err_msg=None

        configvalues = readconfig.configvalues
        log.info('In Web dispatcher')
        custom_dict={
                    'getstatus': ['radio','checkbox'],
                    'selectradiobutton': ['radio'],
                    'selectcheckbox': ['checkbox'],
                    'unselectcheckbox': ['checkbox'],

                    'selectvaluebyindex':['dropdown','listbox'],
                    'selectvaluebytext': ['dropdown','listbox'],
                    'getallvalues':['dropdown','listbox'],
                    'verifyallvalues': ['dropdown','listbox'],

                    'settext': ['textbox','textarea','password','number','email','url'],
                    'sendvalue':['textbox','textarea','password','number','email','url'],
                    'gettext': ['textbox','textarea','password','number','email','url'],
                    'setsecuretext':['textbox','password'],
                    'sendsecurevalue':['textbox','password'],

                    }
        custom_dict_element={'element':['clickelement','doubleclick','rightclick','getelementtext','verifyelementtext','verifyexists', 'verifydoesnotexists', 'verifyhidden','verifyvisible',
                                        'waitforelementvisible','savefile','getcelltooltip','verifycelltooltip','cellclick','getrownumbytext','getcolnumbytext','getrowcount','getcolumncount']}

        result=[TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,err_msg]

        def print_error(err_msg):
            err_msg=ERROR_CODE_DICT['ERR_CUSTOM_MISMATCH']
            logger.print_on_console(err_msg)
            log.error(err_msg)

        def send_webelement_to_keyword(driver,objectname,url):
            webelement=None
            getObjectFlag=False
            if driver:
                log.debug('In send_webelement_to_keyword method')
                #check if the element is in iframe or frame
                try:
                    if url and self.custom_object.is_int(url):
                        log.debug('Encountered iframe/frame url')
                        # self.custom_object.switch_to_iframe(url,driver.current_window_handle)
                        self.custom_object.switch_to_iframe(url,driver.current_window_handle)
                        driver = browser_Keywords_MW.driver_obj
                    if objectname==CUSTOM:
                        log.info('Encountered custom object')
                        log.info('Custom flag is ')
                        log.info(teststepproperty.custom_flag)
                        custom_input=teststepproperty.inputval[0].split(';')
                        if teststepproperty.custom_flag:
                            if len(input)>3 and custom_input[-1].startswith('{{') and custom_input[-1].endswith('}}'):
                                if isinstance(input[-1],webdriver.remote.webelement.WebElement):
                                    reference_element=input[-1]
                                    getObjectFlag=True
                                    log.info("getObjectFlag is True. Reference element is taken from getObject")
                                    logger.print_on_console("getObjectFlag is True. Reference element is taken from getObject")
                                else:
                                    reference_element=None
                                    err_msg=ERROR_CODE_DICT['INCORRECT_VARIABLE_FORMAT']
                                    logger.print_on_console(err_msg)
                                    log.error(err_msg)
                            else:
                                reference_element=self.getwebelement(driver,teststepproperty.parent_xpath,teststepproperty.stepnum,teststepproperty.custname)
                            log.debug('Reference_element ')
                            log.debug(reference_element)
                            if reference_element != None:
                                ##reference_element = reference_element[0]
                                log.info('Reference_element is found')
                                if keyword==GET_OBJECT_COUNT:
                                    log.info('Keyword is ')
                                    log.info(keyword)
                                    webelement=reference_element
                                elif len(input)>=3:
                                    if (keyword in custom_dict and input[0].lower() in custom_dict[keyword]) or keyword in list(custom_dict_element.values())[0]:
                                        webelement=self.custom_object.getCustomobject(reference_element,input[0],input[1],input[2],teststepproperty.url)
                                        log.debug(MSG_CUSTOM_FOUND)
                                        if getObjectFlag:
                                            input.pop()
                                        del input[:3]
                                    else:
                                        print_error('ERR_CUSTOM_MISMATCH')
                                else:
                                    print_error('ERR_PRECONDITION_NOTMET')
                                    print_error('ERR_CUSTOM_NOTFOUND')

                            else:
                                print_error('ERR_REF_ELE_NULL')
                                print_error('ERR_CUSTOM_NOTFOUND')

                        else:
                            print_error('ERR_REF_ELE_NULL')
                            print_error('ERR_CUSTOM_NOTFOUND')

                    else:
                        if objectname=="@Object":
                            webelement = input[0]
                            log.info(WEB_ELEMENT_FOUND_FROM_GetInnerTable)
                            logger.print_on_console(WEB_ELEMENT_FOUND_FROM_GetInnerTable)
                        elif teststepproperty.cord != None and teststepproperty.cord != "":
                            obj_props = teststepproperty.objectname.split(';')
                            coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                            webelement = {'cord': teststepproperty.cord, 'coordinates':coord}
                        else:
                            # import UserObjectScrape_MW
                            # webscrape=UserObjectScrape_MW.UserObject()
                            # obj1=UserObjectScrape_MW.update_data.copy()
                            # for k,v in obj1.items():
                            #     if teststepproperty.custname in v:
                            #         objectname=v[teststepproperty.custname]
                            #         UserObjectScrape_MW.update_data[str(teststepproperty.stepnum)]=v
                            webelement = self.getwebelement(driver,objectname,teststepproperty.stepnum,teststepproperty.custname)
                            # if(obj_flag!=False):
                            #     import UserObjectScrape_MW
                            #     webscrape=UserObjectScrape_MW.UserObject()
                            #     # obj=core_utils.CoreUtils()
                                # webscrape.update_scrape_object(url,objectname,obj_flag,teststepproperty.stepnum,teststepproperty.custname)
                            if webelement != None:
                                if isinstance(webelement,list):
                                    webelement = webelement[0]
                                    log.info(WEB_ELEMENT_FOUND)
                                    logger.print_on_console(WEB_ELEMENT_FOUND)
                except Exception as e:
                    log.error(e,exc_info=True)
                    print_error('Web element not found')

            elif teststepproperty.cord != None and teststepproperty.cord != "":
                obj_props = teststepproperty.objectname.split(';')
                coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                webelement = {'cord': teststepproperty.cord, 'coordinates':coord}
            return webelement
        
        

        def find_browser_info(reporting_obj,mythread):
            #Find the browser type and browser name if driver_obj is not None
            if browser_Keywords_MW.driver_obj is not None:
                log.info('Finding the browser information')
                browser_info=browser_Keywords_MW.driver_obj.capabilities
                if execution_env['env'] == 'default' and SYSTEM_OS == 'Windows':
                    adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
                    cmd = adb + ' -s '+ browser_info['deviceName']+ ' shell dumpsys package com.android.chrome | grep "versionName"'
                    s = subprocess.check_output(cmd.split(),universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW).strip()
                    reporting_obj.browser_version=s.split("=")[1]
                reporting_obj.browser_type=browser_info.get('browserName')
                log.info(reporting_obj.browser_version)
                log.info(reporting_obj.browser_type)
            elif browser_Keywords_MW.driver_obj is None:
                reporting_obj.browser_type=BROWSER_NAME[input[0]]
                reporting_obj.browser_version= 'N/A'
                log.info(reporting_obj.browser_version)
                log.info(reporting_obj.browser_type)


        try:
            # window_ops_list=['click','press','doubleclick','rightclick','uploadfile','acceptpopup','dismisspopup','selectradiobutton','selectcheckbox','unselectcheckbox','cellclick','clickelement','drag','drop','settext','sendvalue','cleartext','setsecuretext','sendsecurevalue','selectvaluebyindex','selectvaluebytext','selectallvalues','selectmultiplevaluesbyindexes','selectmultiplevaluesbytext','verifyvaluesexists','deselectall','setfocus','mousehover','tab','sendfunctionkeys','rightclick','mouseclick','openbrowser','navigatetourl','opennewbrowser','refresh','closebrowser','closesubwindows','switchtowindow','clearcache','navigatewithauthenticate']
            if browser_Keywords_MW.driver_obj is not None:
                browser_info=browser_Keywords_MW.driver_obj.capabilities
                if execution_env['env'] == 'default' and SYSTEM_OS == 'Windows':
                    adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
                    cmd = adb + ' -s '+ browser_info['deviceName']+ ' shell dumpsys package com.android.chrome | grep "versionName"'
                    s = subprocess.check_output(cmd.split(),universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW).strip()
                    reporting_obj.browser_version=s.split("=")[1]
                reporting_obj.browser_type=browser_info.get('browserName')
                log.info(reporting_obj.browser_version)
                log.info(reporting_obj.browser_type)
            if execution_env['env'] == 'default' and keyword in list(self.MW_dict.keys()):
                flag=False
                #Finding the webelement for NON_WEBELEMENT_KEYWORDS
                if (keyword not in NON_WEBELEMENT_KEYWORDS) and (keyword!="waitForElementVisible"):
                    flag=True
                    webelement=send_webelement_to_keyword(driver,objectname,url)
                    globalWait_to=int(configvalues['globalWaitTimeOut'])
                    if globalWait_to > 0 and webelement is None:
                        try:
                            identifiers = objectname.split(';')
                            ele_th={}
                            obj_type={0:By.XPATH,1:By.ID,2:By.XPATH,3:By.NAME,5:By.CLASS_NAME,11:By.CSS_SELECTOR}
                            for i in range(0,len(identifiers)):
                                obj_name=identifiers[i]
                                if  i in obj_type.keys() and not(obj_name in [None,'null']):
                                    element_present=EC.presence_of_element_located((obj_type[i], obj_name))
                                    ele_th[i]=threading.Thread(target = self.find_ele, name=i, args = (i,globalWait_to,browser_Keywords_MW.driver_obj,element_present,log))
                                    ele_th[i].start()
                            for i in ele_th:
                                ele_th[i].join()
                            if(status_gwto):
                                msg='Element Found. Global Wait Timeout completed'
                                log.info(msg)
                                logger.print_on_console(msg)
                                webelement=send_webelement_to_keyword(driver,objectname,url)
                            else:
                                msg1='Element not Found. Global Wait Timeout executed'
                                logger.print_on_console(msg1)
                                log.error(msg1)
                                if simple_debug_gwto:
                                    webelement=send_webelement_to_keyword(driver,objectname,url)
                        except Exception as e:
                            log.error(e)
                    if webelement == None and self.exception_flag:
                        result=TERMINATE

                elif keyword==WAIT_FOR_ELEMENT_VISIBLE:
                    if objectname==CUSTOM:
                        webelement=send_webelement_to_keyword(driver,objectname,url)
                        objectname=self.custom_object.getElementXPath(webelement)
                    if url !=  '' and self.custom_object.is_int(url):
                        log.debug('Encountered iframe/frame url')
                        self.custom_object.switch_to_iframe(url,driver.current_window_handle)
                        driver = browser_Keywords_MW.driver_obj
                    identifiers = objectname.split(';')
                    input=identifiers[0]

                if result != TERMINATE:

                    if keyword==OPEN_BROWSER:
                        input.append(self.action)
                    actual_input=teststepproperty.inputval[0].split(";")
                    if(keyword.lower() == "sendfunctionkeys"):
                        input.extend(actual_input)
                    ## Issue #190 Driver control won't switch back to parent window
                    if self.popup_object.check_if_no_popup_exists():
                        self.browser_object.validate_current_window_handle()
                    if objectname=="@Object":
                        ##webelement = input[0]
                        input =input[1:]
                        result= self.MW_dict[keyword](webelement,input)
                    elif teststepproperty.cord!='' and teststepproperty.cord!=None:
                        if teststepproperty.custom_flag:
                            result = self.MW_dict[keyword](webelement,input,output,teststepproperty.parent_xpath)
                        else:
                            result = self.MW_dict[keyword](webelement,input,output)
                    else:
                        result= self.MW_dict[keyword](webelement,input)
                    ## To terminate debug/execution if requested browser is not available in the system (Defect #846)
                    if(result[1] == TERMINATE):
                        result = TERMINATE
                    # if keyword in window_ops_list:
                    #     delay_time=configvalues['delay']
                    #     if delay_time.strip()=="":
                    #         delay_time=0
                    #     time.sleep(float(delay_time))
                    #     if self.popup_object.check_if_no_popup_exists():
                    #         self.browser_object.update_window_handles()
                    driver=browser_Keywords_MW.driver_obj
                    if self.popup_object.check_if_no_popup_exists() and (keyword not in [GET_POPUP_TEXT,VERIFY_POPUP_TEXT]):
                        driver.switch_to.default_content()
                    if flag and webelement==None and teststepproperty.custname!='@Browser':
                        result=list(result)
                        result[3]=WEB_ELEMENT_NOT_FOUND
                    if keyword == GET_INNER_TABLE and (output != '' and output.startswith('{') and output.endswith('}')):
                        webelement_map[output]=result[2]

                    elif keyword not in [OPEN_BROWSER,CLOSE_BROWSER,GET_POPUP_TEXT,VERIFY_POPUP_TEXT]:
                        if configvalues['httpStatusCode'].lower() == 'yes':
                            if result[0].lower() == 'fail':
                                res,value=self.check_url_error_code()
                                if res:
                                    result=TERMINATE

                    elif keyword==OPEN_BROWSER:
                        find_browser_info(reporting_obj,mythread)

            elif execution_env['env'] == 'saucelabs' and teststepproperty.name in list(self.sauce_mobile_web_dict.keys()):
                if teststepproperty.custname=='@Browser' or teststepproperty.custname=='@BrowserPopUp':
                    if(teststepproperty.name=="openBrowser"):
                        config = self.sauce_conf["mobile"]
                        desired_caps = {}
                        desired_caps['platformName'] = config["platformName"]
                        desired_caps['browserName'] = config["browserName"]
                        desired_caps['appium:deviceName'] = config["deviceName"]
                        desired_caps['appium:platformVersion'] = config["platformVersion"]
                        desired_caps['sauce:options'] = {}
                        desired_caps['sauce:options']['extendedDebugging'] = True
                        desired_caps['sauce:options']['capturePerformance'] = True
                        desired_caps["sauce:options"]["idleTimeout"] = 90
                        desired_caps["sauce:options"]["name"] = teststepproperty.testscript_name
                        result = self.sauce_mobile_web_dict[teststepproperty.name](self.sauce_conf['remote_url'],desired_caps)
                        driver = web_keywords_MW.local_wk.driver
                        browser_Keywords_MW.driver_obj = driver
                        find_browser_info(reporting_obj,mythread)
                    else:
                        result = self.sauce_mobile_web_dict[teststepproperty.name](webelement,input)
                elif teststepproperty.name in self.sauce_mobile_web_dict:
                    xpath=teststepproperty.objectname.split(';')[0]
                    if(teststepproperty.name=="waitForElementVisible"):
                        input=xpath
                    driver.switch_to.default_content()
                    webelement=send_webelement_to_keyword(web_keywords_MW.local_wk.driver,objectname,url)
                    result = self.sauce_mobile_web_dict[teststepproperty.name](webelement,input)
                else:
                    logger.print_on_console(teststepproperty.name+" keyword is not supported in saucelabs execution.")
                    return False
            elif execution_env['env'] == 'browserstack' and teststepproperty.name in list(self.Browserstack_mobile_web_dict.keys()):
                if teststepproperty.custname=='@Browser' or teststepproperty.custname=='@BrowserPopUp':
                    if(teststepproperty.name=="openBrowser"):
                        config = self.browserstack_conf["Mobile"]
                        desired_caps = {}
                        desired_caps["os_version"] = config["platformVersion"]
                        desired_caps["device"] = config["deviceName"]
                        desired_caps["build"] = "Mobile_Web"
                        desired_caps["name"] = teststepproperty.testscript_name
                        desired_caps["browserstack.appium_version"] = "1.16.0"
                        desired_caps["browserstack.idleTimeout"] = "60"
                        desired_caps["browserstack.networkLogs"] = "true"
                        desired_caps["interactiveDebugging"] = "true"
                        desired_caps['browserstack.debug'] = "true"
                        result = self.Browserstack_mobile_web_dict[teststepproperty.name](self.browserstack_conf['remote_url'],desired_caps)
                        # driver = web_keywords_MW.local_wk.driver
                        driver = browser_Keywords_MW.driver_obj
                        browser_Keywords_MW.driver_obj = driver
                        find_browser_info(reporting_obj,mythread)
                    else:
                        result = self.Browserstack_mobile_web_dict[teststepproperty.name](webelement,input)
                elif teststepproperty.name in self.Browserstack_mobile_web_dict:
                    xpath=teststepproperty.objectname.split(';')[0]
                    if(teststepproperty.name=="waitForElementVisible"):
                        input=xpath
                    driver.switch_to.default_content()
                    # webelement=send_webelement_to_keyword(web_keywords_MW.driver,objectname,url)
                    webelement=send_webelement_to_keyword(browser_Keywords_MW.driver_obj,objectname,url)
                    result = self.Browserstack_mobile_web_dict[teststepproperty.name](webelement,input)
                else:
                    logger.print_on_console(teststepproperty.name+" keyword is not supported in browserstack execution.")
                    return False  

            else:
                err_msg=INVALID_KEYWORD
                result=list(result)
                result[3]=err_msg
            screen_shot_obj = screenshot_keywords.Screenshot()
            if self.action == EXECUTE:
                if result != TERMINATE:
                    result=list(result)
                    screen_details=mythread.json_data['suitedetails'][0]
                    if configvalues['screenShot_Flag'].lower() == 'fail':
                        if result[0].lower() == 'fail':
                            file_path = screen_shot_obj.captureScreenshot(screen_details, web=True, driver=driver)
                            result.append(file_path[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        file_path = screen_shot_obj.captureScreenshot(screen_details, web=True, driver=driver)
                        result.append(file_path[2])
        except TypeError as e:
            log.error(e,exc_info=True)
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result=list(result)
            result[3]=err_msg
            result[2]=None
        except Exception as e:
            log.error(e)
##            logger.print_on_console('Exception at dispatcher')
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return result

        


    def is_alert_present(self,driver):
        flag = True
        try:
            driver.switch_to_alert()
            flag = True
        except Exception as e:
            flag = False
        return flag

    def check_url_error_code(self):
        status=False
        value=None
        if browser_Keywords_MW.driver_obj != None:
            log.info('checking for the url error')
            try:
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', browser_Keywords_MW.driver_obj.current_url)
                if urls != []:
                    response=requests.get(urls[0],verify=False,proxies=readconfig.proxies)
                    status_code=response.status_code
                    log.info(status_code)
                    if status_code in STATUS_CODE_DICT:
                        value=STATUS_CODE_DICT[status_code]
                        logger.print_on_console('Error code ',status_code,' : ',value)
                        log.error('Error code and value ')
                        log.error(status_code)
                        log.error(value)
                        status=True
                else:
                    log.info('Url is empty')
            except Exception as e:
                status_code=111
                if status_code in STATUS_CODE_DICT:
                    value=STATUS_CODE_DICT[status_code]
                    logger.print_on_console('Error code ',status_code,' : ',value)
                    log.error('Error code and value ')
                    log.error(status_code)
                    log.error(value)
                    status=True
                log.error(e)
        return status,value
    
    def find_ele(self,i,globalWait_to,driver,element_present,log):
        global status_gwto
        try:
            log.debug('starting Global Wait TimeOut with oi'+str(i))
            WebDriverWait(driver, globalWait_to).until(element_present)
            status_gwto=True
            msg1="Element Found with oi"+str(i)+". Global Wait Timeout executed"
        except TimeoutException as e:
            msg1="Element not Found with oi"+str(i)+". Global Wait Timeout executed"
            log.debug(msg1)
            log.error(e)

    def getwebelement(self,driver,objectname,stepnum,custname):
##        objectname = str(objectname)
        global obj_flag,simple_debug_gwto
        obj_flag=False
        webElement = None
        if objectname.strip() != '':
            identifiers = objectname.split(';')
            log.debug('Identifiers are ')
            log.debug(identifiers)
            if len(identifiers)>=3:
                try:
                    #find by rxpath
                    tempwebElement = driver.find_elements_by_xpath(identifiers[0])
                    if (len(tempwebElement) == 1):
                        logger.print_on_console('Webelement found by OI1')
                        log.debug('Webelement found by OI1')
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if (len(tempwebElement) == 1):
                            logger.print_on_console('Webelement found by OI2')
                            log.debug('Webelement found by OI2')
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if (len(tempwebElement) == 1):
                                logger.print_on_console('Webelement found by OI3')
                                log.debug('Webelement found by OI3')
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
##                    log.debug('Webelement found by relative xpath')
                    webElement = tempwebElement

                except Exception as webEx:
                    try:
                        #find by id
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if (len(tempwebElement) == 1):
                            logger.print_on_console('Webelement found by OI2')
                            log.debug('Webelement found by OI2')
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if (len(tempwebElement) == 1):
                                logger.print_on_console('Webelement found by OI3')
                                log.debug('Webelement found by OI3')
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
##                        log.debug('Webelement found by Id')
                        webElement = tempwebElement
                    except Exception as webEx:
                        #find by absolute Xpath
                        try:
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if (len(tempwebElement) == 1):
                                logger.print_on_console('Webelement found by OI3')
                                log.debug('Webelement found by OI3')
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                            webElement = tempwebElement
##                            log.debug('Webelement found by absolute Xpath')
                        except Exception as webEx:
                            try:
                                if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                    tempwebElement = driver.find_elements_by_name(identifiers[3])
                                    if (len(tempwebElement) == 1):
                                        logger.print_on_console('Webelement found by OI4')
                                        log.debug('Webelement found by OI4')
                                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                        tempwebElement = driver.find_elements_by_class_name(identifiers[5])
                                        if (len(tempwebElement) == 1):
                                            logger.print_on_console('Webelement found by OI5')
                                            log.debug('Webelement found by OI5')
                                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                        if(len(identifiers)==12):
                                            tempwebElement = driver.find_elements_by_css_selector(identifiers[11])
                                            if (len(tempwebElement) == 1):
                                                logger.print_on_console('Webelement found by OI6')
                                                log.debug('Webelement found by OI6')
                                            else:
                                                tempwebElement = None
                                webElement = tempwebElement
                            except Exception as webEx:
                                    try:
                                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                            tempwebElement = driver.find_elements_by_class_name(identifiers[5])
                                            if (len(tempwebElement) == 1):
                                                logger.print_on_console('Webelement found by OI5')
                                                log.debug('Webelement found by OI5')
                                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                                if(len(identifiers)==12):
                                                    tempwebElement = driver.find_elements_by_css_selector(identifiers[11])
                                                    if (len(tempwebElement) == 1):
                                                        logger.print_on_console('Webelement found by OI6')
                                                        log.debug('Webelement found by OI6')
                                                    else:
                                                        tempwebElement = None
                                        webElement = tempwebElement
                                    except Exception as webEx:
                                        try:
                                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                                if(len(identifiers)==12):
                                                    tempwebElement = driver.find_elements_by_css_selector(identifiers[11])
                                                    if (len(tempwebElement) == 1):
                                                        logger.print_on_console('Webelement found by OI6')
                                                        log.debug('Webelement found by OI6')
                                                    else:
                                                        tempwebElement = None
                                            webElement = tempwebElement
                                        except Exception as webEx:
                                            err_msg=WEB_ELEMENT_NOT_FOUND
            #enhance object reconition changes
            if(webElement == None):
                try:
                    coordinates=identifiers[6] + ',' +  identifiers[7] + ',' + identifiers[8] + ',' + identifiers[9]
                    script1 = """if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('*');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } if (!window.Element || !window.Element.prototype || !window.Element.prototype.getAttribute) {     (function() {         function getAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('*');         for (var i = 0; i < inputs.length; i++) {             inputs[i].getAttribute = getAttribute;         }     }()); }(function() {     if (!document.getElementsByClassName) {         var indexOf = [].indexOf || function(prop) {             for (var i = 0; i < this.length; i++) {                 if (this[i] === prop) return i;             }             return -1;         };         getElementsByClassName = function(className, context) {             var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function() {                 var all = context.getElementsByTagName("*"),                     elements = [],                     i = 0;                 for (; i < all.length; i++) {                     if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) elements.push(all[i]);                 }                 return elements;             })();             return elems;         };         document.getElementsByClassName = function(className) {             return getElementsByClassName(className, document);         };         if (window.Element) {             window.Element.prototype.getElementsByClassName = function(className) {                 return getElementsByClassName(className, this);             };         }     } })(); var suseIdx = true; var suseId = true; var suseClass = true; var srelative = true; var sae = []; var sarr = []; var sele = document.getElementsByTagName('*'); var smyid = 0; var stextvalue = ''; var stagname = 0; var scustname = ''; var smultipleFlag = false; var snonamecounter = 1; var txt_area_nonamecounter = 1; var select_nonamecounter = 1; var td_nonamecounter = 1; var a_nonamecounter = 1; var table_nonamecounter = 1; var input_nonamecounter = 1; var stagtype = ''; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var sclassname = 'null'; var top = 0; var left = 0; var height = 0; var width = 0; var coordinates = ''; var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); saddNodesOuter(sae, sele); for (var j = 0; j < sae.length; j++) {     stagtype = '';     ssname = 'null';     sstagname = 'null';     sid = sae[j].id;     sname = sae[j].name;     salttext = sae[j].alt;     splaceholder = sae[j].placeholder;     sclassname = sae[j].className;     sid = (String(sid));     sclassname = (String(sclassname));     sname = (String(sname));     splaceholder = (String(splaceholder));     stextvalue = stext_content(sae[j]);     stextvalue = (String(stextvalue));     stagname = sae[j].tagName.toLowerCase();     ssname = 'null';     sstagname = 'null';     ssclassname = 'null';     findCoordinates(sae[j]);     if (stagname.indexOf(':') != -1) {         stagname = stagname.replace(':', '');         stagname = 'custom' + stagname;     }     if (sname != '' && sname != 'undefined') {         snames = document.getElementsByName(sname);         if (snames.length > 1) {             for (var k = 0; k < snames.length; k++) {                 if (sae[j] == snames[k]) {                     ssname = sname + '[' + k + ']'                 }             }         } else {             ssname = sname;         }     }     if (stagname != '' && stagname != 'undefined') {         stagnames = document.getElementsByTagName(stagname);         if (stagnames.length > 1) {             for (var k = 0; k < stagnames.length; k++) {                 if (sae[j] == stagnames[k]) {                     sstagname = stagname + '[' + k + ']'                 }             }         } else {             sstagname = stagname;         }     }     if (sclassname != '' && sclassname != 'undefined') {         sclassnames = document.getElementsByClassName(sclassname);         if (sclassnames.length > 1) {             for (var k = 0; k < sclassnames.length; k++) {                 if (sae[j] == sclassnames[k]) {                     ssclassname = sclassname + '[' + k + ']'                 }             }         } else {             ssclassname = sclassname;         }     }     if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'br' && stagname != 'animatetransform') {         if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') {             if (sname != '' && sname != 'undefined') {                 snames = document.getElementsByName(sname);                 if (snames.length > 1) {                     for (var k = 0; k < snames.length; k++) {                         if (sae[j] == snames[k]) {                             stextvalue = sname + k;                         }                     }                 } else {                     stextvalue = sname;                 }             } else if (sid != '' && sid != 'undefined') {                 stextvalue = sid;             } else if (splaceholder != '' && splaceholder != 'undefined') {                 stextvalue = splaceholder;             } else { 				 				var eles = document.getElementsByTagName(stagname);                     for (var k = 0; k < eles.length; k++) {                         if (sae[j] == eles[k]) {                             stextvalue = stagname + '_NONAME' + (k+1);                         }                     }             }         }         if (sid == '') {             sid = 'null';         }         var sfirstpass = 0;         var srpath = '';         var setype = sae[j].getAttribute('type');         setype = (String(setype)).toLowerCase();         for (var spath = ''; sae[j] && sae[j].nodeType == 1; sae[j] = sae[j].parentNode) {             var spredicate = [];             var ssiblings = sae[j].parentNode.children;             var scount = 0;             var sunique = false;             var snewPath = '';             var sidx = 0;             for (var i = 0; ssiblings && (i < ssiblings.length); i++) {                 if (ssiblings[i].tagName == sae[j].tagName) {                     scount++;                     if (ssiblings[i] == sae[j]) {                         sidx = scount;                     }                 }             }             if (sidx == 1 && scount == 1) {                 sidx = null;             }             if (suseId && sae[j].id) {                 spredicate[spredicate.length] = '@id=' + '"' + sae[j].id + '"';                 sunique = true;             }             xidx = (suseIdx && sidx) ? ('[' + sidx + ']') : '';             sidx = (suseIdx && sidx && !sunique) ? ('[' + sidx + ']') : '';             spredicate = (spredicate.length > 0) ? ('[' + spredicate.join(' and ') + ']') : '';             spath = '/' + sae[j].tagName.toLowerCase() + xidx + spath;             if (sfirstpass == 0) {                 if (sunique && srelative) {                     srpath = '//*' + sidx + spredicate + srpath;                     sfirstpass = 1;                 } else {                     srpath = '/' + sae[j].tagName.toLowerCase() + sidx + spredicate + srpath;                 }             }         }         stextvalue = stextvalue.replace(">", "");         stextvalue = stextvalue.replace("</", "");         stextvalue = stextvalue.replace("<", "");         stextvalue = stextvalue.replace("/>", "");         if (stextvalue == '' || stextvalue.length == 0 || stextvalue == '0') {             stextvalue = 'NONAME' + snonamecounter;             snonamecounter = snonamecounter + 1;         }         coordinates = left + ',' + top + ',' + height + ',' + width;         coordinates = String(coordinates);         snewPath = String(srpath) + ';' + String(sid) + ';' + String(spath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + stextvalue;         sarr.push({             'xpath': snewPath,             'text': stextvalue,             'height': height,             'width': width,             'top': top,             'left': left         });     } } var coordinates = arguments[0]; var arr = coordinates.split(","); var top1 = 0,     left = 0,     height = 0,     width = 0; var j = 0; var resulrarr = []; doc = document.body; body_coors = doc.getClientRects(); body_width = body_coors[0].width; if (body_width == undefined) {     body_width = body_coors[0].right; } var height1 = parseInt(arr[2]) + 100,     width1 = parseInt(arr[3]) + 100; var diff = (body_width / 2) - arr[0]; var x1 = ((body_width / 2) - diff) - 100; var y1 = arr[1] - 120,     x2 = x1 + width1 + 70,     y2 = y1,     x3 = x1,     y3 = y1 + height1 + 70,     x4 = x2,     y4 = y3; for (var i = 0; i < sarr.length; i++) {     top1 = sarr[i].top;     left = sarr[i].left;     height = sarr[i].height;     width = sarr[i].width;     if ((left > x1 && left < x2) && (top1 > y1 && top1 < y3) && (height < height1) && (width < width1)) {         resulrarr.push(sarr[i]);     } } return resulrarr;  function findCoordinates(element) {     height = element.offsetHeight;     width = element.offsetWidth;     top = 0;     left = 0;     do {         top += element.offsetTop || 0;         left += element.offsetLeft || 0;         element = element.offsetParent;     } while (element); }  function saddNodesOuter(sarray, scollection) {     for (var i = 0; scollection && scollection.length && i < scollection.length; i++) {         sarray.push(scollection[i]);     } };  function stext_content(f) {     var sfirstText = '';     var stextdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     return (stextdisplay); };"""
                    a=driver.execute_script(script1,coordinates)
                    arrofsimilartags=[]
                    for i in range (len(a)):
                        xpath =a[i].get('xpath').split(';')
                        tagname=xpath[4]
                        if '[' in tagname:
                            tagname=tagname.split('[')[0]
                        if tagname in identifiers[4]:
                            arrofsimilartags.append(a[i])
                    elementname='null'
                    for i in range (len(arrofsimilartags)):
                        xpath =arrofsimilartags[i].get('xpath').split(';')
                        name=xpath[3]
                        if name == identifiers[3]:
                            elementname= name
                    if (elementname!='null'):
                            tempwebElement = driver.find_elements_by_name(elementname)
                            if (len(tempwebElement) == 1):
                                logger.print_on_console('Webelement found by OI7')
                                log.debug('Webelement found by OI7')
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                webElement=None
                    if(webElement==None):
                        script2="""var aTags = document.getElementsByTagName(arguments[2]); var arr = arguments[0]; var searchText = arguments[1]; var found = ''; var stextvalue = ''; var stagname = 0; for (var i = 0; i < arr.length; i++) {     for (var j = 0; j < aTags.length; j++) {         stextvalue = stext_content(aTags[j]);         stextvalue = (String(stextvalue));         var sname = aTags[j].name;         sname = (String(sname));         var splaceholder = aTags[j].placeholder;         splaceholder = (String(splaceholder));         var stagname = aTags[j].tagName.toLowerCase();         if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') {             if (sname != '' && sname != 'undefined') {                 snames = document.getElementsByName(sname);                 if (snames.length > 1) {                     for (var k = 0; k < snames.length; k++) {                         if (aTags[j] == snames[k]) {                             stextvalue = sname + k;                         }                     }                 } else {                     stextvalue = sname;                 }             } else if (splaceholder != '' && splaceholder != 'undefined') {                 stextvalue = splaceholder;             } else { 				stextvalue = stagname + '_NONAME' + (j+1);             }         }         if (arr[i].text == stextvalue) {             if (stextvalue == searchText) {                 found = aTags[j];                 break;             }         }     }      if (found != '') {         break;     } }  function stext_content(f) {     var sfirstText = '';     var stextdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     return (stextdisplay); }; return found;"""
                        tagname=identifiers[4].split('[')[0]
                        elementWithText=driver.execute_script(script2,arrofsimilartags,identifiers[10],tagname)
                        tempwebElement = elementWithText
                    webElement= tempwebElement
                except Exception as webEx:
                     webElement = None

            elif objectname.startswith('{') and objectname.endswith('}') and objectname in self.webelement_map:
                if len(self.webelement_map)<=4:
                    webElement=[]
                    webElement.append(self.webelement_map[objectname])
                else:
                    logger.print_on_console(MAX_SIZE_EXCEEDED)
                    log.error(MAX_SIZE_EXCEEDED)
                    err_msg=WEB_ELEMENT_NOT_FOUND
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
            #Fixing issue #381
            if webElement==None or webElement== '':
                webElement = None
                err_msg=WEB_ELEMENT_NOT_FOUND
                logger.print_on_console(err_msg)
                log.error(err_msg)
        configvalues = readconfig.configvalues
        if((webElement==None or webElement== '') and configvalues['extn_enabled'].lower() == 'yes' and self.action=='debug' and isinstance(driver, webdriver.Chrome)):
            if not(simple_debug_gwto):
                simple_debug_gwto=True
                if isinstance(webElement,list):
                    webElement=webElement[0]
                return webElement
            try:
                flag=True
                logger.print_on_console('Scrape the Element using extension')
                import pause_display_operation
                from itertools import combinations
                o = pause_display_operation.PauseAndDisplay()
                inputs={'stepnum':stepnum,'custname':custname}
                o.debug_object(inputs,self.wxObject,self.thread,driver)
                attributes=driver.execute_script("return JSON.parse(window.localStorage.attributes)")
                new_ele_type=driver.execute_script("return window.localStorage.element").lower()
                typemap={'btn': 'button',
                        'chkbox': 'checkbox',
                        'elmnt': 'elmnt',
                        'img': 'img',
                        'lst': 'list',
                        'radiobtn': 'radiobutton',
                        'select': 'select',
                        'tbl': 'table',
                        'txtbox': 'input',
                        'lnk':'a'
                }
                if (typemap[identifiers[4]]!=new_ele_type):
                    flag=False
                if(flag==False):
                    o = pause_display_operation.PauseAndDisplay()
                    inputs1={'custtype':typemap[identifiers[4]],'newtype':new_ele_type}
                    o.debug_error(inputs1,self.wxObject,self.thread)
                ele='//*'
                a=[]
                combo=''
                for k,v in list(attributes.items()):
                    if k != 'style':
                        ele=ele+'[@'+k+'="'+v+'"]'
                        a.append('[@'+k+'="'+v+'"]')
                tempwebElement=driver.find_elements_by_xpath(ele)
                if(len(tempwebElement)==1):
                    webElement=tempwebElement
                    identifiers[0]=ele
                    obj_flag=ele
                    log.debug('Element has been Captured with all properties')
                for i in range(len(a),1,-1):
                    comb=combinations(a,i)
                    for j in list(comb):
                        combo="//*"+"".join(j)
                        tempwebElement=driver.find_elements_by_xpath(combo)
                        if(len(tempwebElement)==1):
                            webElement=tempwebElement
                            identifiers[0]=combo
                            obj_flag=combo
                            log.debug('Element has been Captured using some properties')
                            break
                    else:
                        continue
                    break
                if(webElement==None):
                    logger.print_on_console("Webelement not found through extension")
            except Exception as e:
                log.debug(e)
        if isinstance(webElement,list):
            webElement=webElement[0]
        return webElement

    

