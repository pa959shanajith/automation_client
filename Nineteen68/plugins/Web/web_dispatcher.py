#-------------------------------------------------------------------------------
# Name:        web_dispatcher.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import button_link_keyword
import popup_keywords
import browser_Keywords
import radio_checkbox_operations
import table_keywords
import utilweb_operations
import element_operations
import textbox_operations
import dropdown_listbox
import utilweb_operations
import static_text_keywords
import logger
from webconstants import *
import custom_keyword
import screenshot_keywords
from collections import OrderedDict
from constants import *
import requests
import time
import re
import readconfig
import logging
import json
from selenium import webdriver
import threading
local_Wd = threading.local()
local_Wd.log = logging.getLogger('web_dispatcher.py')

class Dispatcher:
    local_Wd.popup_object = popup_keywords.PopupKeywords()
    local_Wd.browser_object = browser_Keywords.BrowserKeywords()
    local_Wd.button_link_object = button_link_keyword.ButtonLinkKeyword()
    local_Wd.radio_checkbox_object = radio_checkbox_operations.RadioCheckboxKeywords()
    local_Wd.table_object = table_keywords.TableOperationKeywords()
    local_Wd.element_object = element_operations.ElementKeywords()
    local_Wd.textbox_object = textbox_operations.TextboxKeywords()
    local_Wd.dropdown_list_object = dropdown_listbox.DropdownKeywords()
    local_Wd.util_object = utilweb_operations.UtilWebKeywords()
    local_Wd.statict_text_object = static_text_keywords.StaticTextKeywords()
    local_Wd.custom_object=custom_keyword.CustomKeyword()
    local_Wd.webelement_map=OrderedDict()
    web_dict={
        'getobjectcount':local_Wd.custom_object.get_object_count,
        'getobject':local_Wd.custom_object.get_object,
        'click': local_Wd.button_link_object.click,
        'verifybuttonname' : local_Wd.button_link_object.verify_button_name,
        'getbuttonname': local_Wd.button_link_object.get_button_name,
        'getlinktext'    : local_Wd.button_link_object.get_link_text,
        'verifylinktext' : local_Wd.button_link_object.verify_link_text,
        'press'  : local_Wd.button_link_object.press,
        'doubleclick' : local_Wd.button_link_object.double_click,
        'rightclick' : local_Wd.button_link_object.right_click,
        'uploadfile'  : local_Wd.button_link_object.upload_file,

        'acceptpopup' : local_Wd.popup_object.accept_popup,
        'dismisspopup':local_Wd.popup_object.dismiss_popup,
        'getpopuptext':local_Wd.popup_object.get_popup_text,
        'verifypopuptext':local_Wd.popup_object.verify_popup_text,


        'getstatus': local_Wd.radio_checkbox_object.get_status,
        'selectradiobutton': local_Wd.radio_checkbox_object.select_radiobutton,
        'selectcheckbox': local_Wd.radio_checkbox_object.select_checkbox,
        'unselectcheckbox': local_Wd.radio_checkbox_object.unselect_checkbox,

        'getrowcount' : local_Wd.table_object.getRowCount,
        'getcolumncount' : local_Wd.table_object.getColoumnCount,
        'getcellvalue' : local_Wd.table_object.getCellValue,
        'verifycellvalue' : local_Wd.table_object.verifyCellValue,
        'cellclick' : local_Wd.table_object.cellClick,
        'getrownumbytext' : local_Wd.table_object.getRowNumByText,
        'getcolnumbytext' : local_Wd.table_object.getColNumByText,
        'getinnertable' : local_Wd.table_object.getInnerTable,
        #author : arpitha.b.v
        #added mapping of 'getCellToolTip' and 'verifyCellToolTip' to table object
        'getcelltooltip' : local_Wd.table_object.getCellToolTip,
        'verifycelltooltip' : local_Wd.table_object.verifyCellToolTip,
        'getelementtext' : local_Wd.element_object.get_element_text,
        'verifyelementtext' : local_Wd.element_object.verify_element_text,
        'clickelement' : local_Wd.element_object.click_element,
        'gettooltiptext' : local_Wd.element_object.get_tooltip_text,
        'verifytooltiptext' : local_Wd.element_object.verify_tooltip_text,
        'drag':local_Wd.element_object.drag,
        'drop':local_Wd.element_object.drop,
        'dropfile':local_Wd.element_object.drop_file,
        'settext':local_Wd.textbox_object.set_text,
        'sendvalue':local_Wd.textbox_object.send_value,
        'gettext':local_Wd.textbox_object.get_text,
        'verifytext':local_Wd.textbox_object.verify_text,
        'cleartext':local_Wd.textbox_object.clear_text,
        'gettextboxlength':local_Wd.textbox_object.gettextbox_length,
        'verifytextboxlength':local_Wd.textbox_object.verifytextbox_length,
        'setsecuretext':local_Wd.textbox_object.setsecuretext,
        'sendsecurevalue':local_Wd.textbox_object.sendSecureValue,

        'selectvaluebyindex':local_Wd.dropdown_list_object.selectValueByIndex,
        'getcount':local_Wd.dropdown_list_object.getCount,
        'selectvaluebytext':local_Wd.dropdown_list_object.selectValueByText,
        'verifyselectedvalues':local_Wd.dropdown_list_object.verifySelectedValues,
        'verifyselectedvalue':local_Wd.dropdown_list_object.verifySelectedValue,
        'verifycount':local_Wd.dropdown_list_object.verifyCount,
        'selectallvalues':local_Wd.dropdown_list_object.selectAllValues,
        'selectmultiplevaluesbyindexes':local_Wd.dropdown_list_object.selectMultipleValuesByIndexes,
        'getselected':local_Wd.dropdown_list_object.getSelected,
        'selectmultiplevaluesbytext':local_Wd.dropdown_list_object.selectMultipleValuesByText,
        'getmultiplevaluesbyindexes':local_Wd.dropdown_list_object.getMultipleValuesByIndexes,
        'verifyallvalues':local_Wd.dropdown_list_object.verifyAllValues,
        'selectbyabsolutevalue':local_Wd.dropdown_list_object.selectByAbsoluteValue,

        #author :arpitha.b.v
        #Added mapping of "getAllValues" keyword values to dropdown's object

        'getallvalues':local_Wd.dropdown_list_object.getAllValues,
        'getvaluebyindex':local_Wd.dropdown_list_object.getValueByIndex,
        'verifyvaluesexists':local_Wd.dropdown_list_object.verifyValuesExists,
        'deselectall':local_Wd.dropdown_list_object.deselectAll,


        'verifyvisible':local_Wd.util_object.verify_visible,
        'verifyexists':local_Wd.util_object.verify_exists,
        'verifydoesnotexists':local_Wd.util_object.verify_doesnot_exists,
        'verifyenabled':local_Wd.util_object.verify_enabled,
        'verifydisabled':local_Wd.util_object.verify_disabled,
        'verifyhidden':local_Wd.util_object.verify_hidden,
        'verifyreadonly':local_Wd.util_object.verify_readonly,
        'setfocus':local_Wd.util_object.setfocus,
        'mousehover':local_Wd.util_object.mouse_hover,
        'tab':local_Wd.util_object.tab,
        'sendfunctionkeys':local_Wd.util_object.sendfunction_keys,
        'rightclick':local_Wd.util_object.rightclick,
        'mouseclick':local_Wd.util_object.mouse_click,
        'verifywebimages':local_Wd.util_object.verify_web_images,
        'imagesimilaritypercentage':local_Wd.util_object.image_similarity_percentage,
        'waitforelementvisible':local_Wd.element_object.waitforelement_visible,
        'getelementtagvalue': local_Wd.util_object.get_element_tag_value,


        'openbrowser':local_Wd.browser_object.openBrowser,
        'navigatetourl':local_Wd.browser_object.navigateToURL,
        'opennewbrowser':local_Wd.browser_object.openNewBrowser,
        'getpagetitle':local_Wd.browser_object.getPageTitle,
        'getcurrenturl':local_Wd.browser_object.getCurrentURL,
        'maximizebrowser':local_Wd.browser_object.maximizeBrowser,
        'refresh':local_Wd.browser_object.refresh,
        'verifycurrenturl':local_Wd.browser_object.verifyCurrentURL,
        'closebrowser':local_Wd.browser_object.closeBrowser,
        'closesubwindows':local_Wd.browser_object.closeSubWindows,
        'switchtowindow':local_Wd.util_object.switch_to_window,
        'verifytextexists':local_Wd.statict_text_object.verify_text_exists,
        'verifypagetitle':local_Wd.browser_object.verify_page_title,
        'clearcache':local_Wd.browser_object.clear_cache,
        'navigatewithauthenticate':local_Wd.browser_object.navigate_with_authenticate
    }



    def __init__(self):
        
        self.exception_flag=''
        self.action=None

    def dispatcher(self,teststepproperty,input,reporting_obj,iris_flag):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        url=teststepproperty.url.strip()
        keyword = teststepproperty.name
        keyword = keyword.lower()
        if self.action == DEBUG and browser_Keywords.driver_pre != None:
            browser_Keywords.local_bk.driver_obj=browser_Keywords.driver_pre
        driver = browser_Keywords.local_bk.driver_obj
        webelement = None
        element = None
        err_msg=None
        configvalues = readconfig.configvalues

        local_Wd.log.info('In Web dispatcher')
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
                    'sendsecurevalue':['textbox','password']

                    }
        custom_dict_element={'element':['getobjectcount','getobject','clickelement','doubleclick','rightclick','getelementtext','verifyelementtext','drag', 'drop','gettooltiptext','verifytooltiptext','verifyexists', 'verifydoesnotexists', 'verifyhidden','verifyvisible', 'switchtotab','switchtowindow','setfocus','sendfunctionkeys',
                                        'tab','waitforelementvisible','mousehover','savefile','press','verifyenabled','verifydisabled','verifyreadonly']}

        result=[TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,err_msg]

        if(iris_flag):
            import iris_operations
            iris_object = iris_operations.IRISKeywords()
            self.web_dict['clickiris'] = iris_object.clickiris
            self.web_dict['settextiris'] = iris_object.settextiris
            self.web_dict['gettextiris'] = iris_object.gettextiris
            self.web_dict['getrowcountiris'] = iris_object.getrowcountiris
            self.web_dict['getcolcountiris'] = iris_object.getcolcountiris
            self.web_dict['getcellvalueiris'] = iris_object.getcellvalueiris
            self.web_dict['verifyexistsiris'] = iris_object.verifyexistsiris
            self.web_dict['verifytextiris'] = iris_object.verifytextiris

        def print_error(err_msg):
            err_msg=ERROR_CODE_DICT[err_msg]
            logger.print_on_console(err_msg)
            local_Wd.log.error(err_msg)

        def send_webelement_to_keyword(driver,objectname,url):
            webelement=None
            getObjectFlag=False
            if driver != None:
                local_Wd.log.debug('In send_webelement_to_keyword method')
                #check if the element is in iframe or frame
                try:
                    if url !=  '' and local_Wd.custom_object.is_int(url):
                        local_Wd.log.debug('Encountered iframe/frame url')
                        local_Wd.custom_object.switch_to_iframe(url,driver.current_window_handle)
                        driver = browser_Keywords.local_bk.driver_obj
                    if objectname==CUSTOM:
                        local_Wd.log.info('Encountered custom object')
                        local_Wd.log.info('Custom flag is ')
                        local_Wd.log.info(teststepproperty.custom_flag)
                        if teststepproperty.custom_flag:
                            if len(input)>3:
                                if isinstance(input[-1],webdriver.remote.webelement.WebElement):
                                    reference_element=input[-1]
                                    getObjectFlag=True
                                    local_Wd.log.info("getObjectFlag is True. Reference element is taken from getObject")
                                    logger.print_on_console("getObjectFlag is True. Reference element is taken from getObject")
                                else:
                                    reference_element=None
                                    err_msg=ERROR_CODE_DICT['INCORRECT_VARIABLE_FORMAT']
                                    logger.print_on_console(err_msg)
                                    local_Wd.log.error(err_msg)
                            else:
                                reference_element=self.getwebelement(driver,teststepproperty.parent_xpath)
                            local_Wd.log.debug('Reference_element ')
                            local_Wd.log.debug(reference_element)
                            if reference_element != None:
                                ##reference_element = reference_element[0]
                                local_Wd.log.info('Reference_element is found')
                                if keyword==GET_OBJECT_COUNT:
                                    local_Wd.log.info('Keyword is ')
                                    local_Wd.log.info(keyword)
                                    webelement=reference_element
                                elif len(input)>=3:
                                    if (keyword in custom_dict and input[0].lower() in custom_dict[keyword]) or keyword in list(custom_dict_element.values())[0]:
                                        webelement=local_Wd.custom_object.getCustomobject(reference_element,input[0],input[1],input[2],teststepproperty.url)
                                        local_Wd.log.debug(MSG_CUSTOM_FOUND)
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
                            local_Wd.log.info(WEB_ELEMENT_FOUND_FROM_GetInnerTable)
                            logger.print_on_console(WEB_ELEMENT_FOUND_FROM_GetInnerTable)
                        elif teststepproperty.cord != None and teststepproperty.cord != "":
                            obj_props = teststepproperty.objectname.split(';')
                            coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                            webelement = {'cord': teststepproperty.cord, 'coordinates':coord}
                        else:
                            webelement = self.getwebelement(driver,objectname)
                            if webelement != None:
                                if isinstance(webelement,list):
                                    webelement = webelement[0]
                                    local_Wd.log.info(WEB_ELEMENT_FOUND)
                                    logger.print_on_console(WEB_ELEMENT_FOUND)
                except Exception as e:
                    local_Wd.log.error(e,exc_info=True)
                    print_error('Web element not found')

            elif teststepproperty.cord != None and teststepproperty.cord != "":
                obj_props = teststepproperty.objectname.split(';')
                coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                webelement = {'cord': teststepproperty.cord, 'coordinates':coord}
            return webelement


        def find_browser_info(reporting_obj):
            #Find the browser type and browser name if driver_obj is not None
            if browser_Keywords.local_bk.driver_obj is not None:
                local_Wd.log.info('Finding the browser information')
                browser_info=browser_Keywords.local_bk.driver_obj.capabilities
                reporting_obj.browser_version=browser_info.get('version')
                if(reporting_obj.browser_version == '' or reporting_obj.browser_version == None):
                    reporting_obj.browser_version= browser_info['browserVersion']
                reporting_obj.browser_type=browser_info.get('browserName')
                local_Wd.log.info(reporting_obj.browser_version)
                local_Wd.log.info(reporting_obj.browser_type)
            elif browser_Keywords.local_bk.driver_obj is None:
                reporting_obj.browser_type=BROWSER_NAME[int(input[0])]
                reporting_obj.browser_version= 'NA'
                local_Wd.log.info(reporting_obj.browser_version)
                local_Wd.log.info(reporting_obj.browser_type)


        try:
            window_ops_list=['click','press','doubleclick','rightclick','uploadfile','acceptpopup','dismisspopup','selectradiobutton','selectcheckbox','unselectcheckbox','cellclick','clickelement','drag','drop','settext','sendvalue','cleartext','setsecuretext','sendsecurevalue','selectvaluebyindex','selectvaluebytext','selectallvalues','selectmultiplevaluesbyindexes','selectmultiplevaluesbytext','verifyvaluesexists','deselectall','setfocus','mousehover','tab','sendfunctionkeys','rightclick','mouseclick','openbrowser','navigatetourl','opennewbrowser','refresh','closebrowser','closesubwindows','switchtowindow','clearcache','navigatewithauthenticate']
            if browser_Keywords.local_bk.driver_obj is not None:
                browser_info=browser_Keywords.local_bk.driver_obj.capabilities
                reporting_obj.browser_type=browser_info.get('browserName')
                reporting_obj.browser_version=browser_info.get('version')
                if(reporting_obj.browser_version == '' or reporting_obj.browser_version == None):
                    reporting_obj.browser_version= browser_info['browserVersion']
            if keyword in list(self.web_dict.keys()):
                flag=False
                #Finding the webelement for NON_WEBELEMENT_KEYWORDS
                if keyword not in NON_WEBELEMENT_KEYWORDS:
                    flag=True
                    webelement=send_webelement_to_keyword(driver,objectname,url)
                    if webelement == None and self.exception_flag:
                        result=TERMINATE

                elif keyword==WAIT_FOR_ELEMENT_VISIBLE:
                    if objectname==CUSTOM:
                        webelement=send_webelement_to_keyword(driver,objectname,url)
                        objectname=local_Wd.custom_object.getElementXPath(webelement)
                    if url !=  '' and local_Wd.custom_object.is_int(url):
                        local_Wd.log.debug('Encountered iframe/frame url')
                        local_Wd.custom_object.switch_to_iframe(url,driver.current_window_handle)
                        driver = browser_Keywords.local_bk.driver_obj
                    identifiers = objectname.split(';')
                    input=identifiers[0]

                if result != TERMINATE:

                    if keyword==OPEN_BROWSER:
                        input.append(self.action)
                    actual_input=teststepproperty.inputval[0].split(";")
                    if(keyword.lower() == "sendfunctionkeys"):
                        input.extend(actual_input)
                    ## Issue #190 Driver control won't switch back to parent window
                    if local_Wd.popup_object.check_if_no_popup_exists():
                        local_Wd.browser_object.validate_current_window_handle()
                    if objectname=="@Object":
                        ##webelement = input[0]
                        input =input[1:]
                        result= self.web_dict[keyword](webelement,input)
                    elif teststepproperty.cord!='' and teststepproperty.cord!=None:
                        if teststepproperty.custom_flag:
                            result = self.web_dict[keyword](webelement,input,output,teststepproperty.parent_xpath)
                        else:
                            result = self.web_dict[keyword](webelement,input,output)
                    else:
                        result= self.web_dict[keyword](webelement,input)
                    ## To terminate debug/execution if requested browser is not available in the system (Defect #846)
                    if(result[1] == TERMINATE):
                        result = TERMINATE
                    if keyword in window_ops_list:
                        delay_time=configvalues['delay']
                        if delay_time.strip()=="":
                            delay_time=0
                        time.sleep(float(delay_time))
                        if local_Wd.popup_object.check_if_no_popup_exists():
                            local_Wd.browser_object.update_window_handles()
                    driver=browser_Keywords.local_bk.driver_obj
                    if local_Wd.popup_object.check_if_no_popup_exists() and (keyword not in [GET_POPUP_TEXT,VERIFY_POPUP_TEXT]):
                        driver.switch_to.default_content()
                    if flag and webelement==None and teststepproperty.custname!='@Browser':
                        result=list(result)
                        result[3]=WEB_ELEMENT_NOT_FOUND
                    if keyword == GET_INNER_TABLE and (output != '' and output.startswith('{') and output.endswith('}')):
                        local_Wd.webelement_map[output]=result[2]

                    elif keyword not in [OPEN_BROWSER,OPEN_NEW_BROWSER,CLOSE_BROWSER,GET_POPUP_TEXT,VERIFY_POPUP_TEXT]:
                        if configvalues['retrieveURL'].lower() == 'yes':
                            if result[0].lower() == 'fail':
                                res,value=self.check_url_error_code()
                                if res:
                                    result=TERMINATE

                    elif keyword==OPEN_BROWSER:
                        find_browser_info(reporting_obj)


            else:
                err_msg=INVALID_KEYWORD
                result=list(result)
                result[3]=err_msg
            screen_shot_obj = screenshot_keywords.Screenshot()
            if self.action == EXECUTE:
                if result != TERMINATE:
                    result=list(result)
                    if configvalues['screenShot_Flag'].lower() == 'fail':
                        if result[0].lower() == 'fail':
                            file_path = screen_shot_obj.captureScreenshot()
                            result.append(file_path[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        file_path = screen_shot_obj.captureScreenshot()
                        result.append(file_path[2])
        except TypeError as e:
            log.error(e,exc_info=True)
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result=list(result)
            result[3]=err_msg
        except Exception as e:
            local_Wd.log.error(e)
##            logger.print_on_console('Exception at dispatcher')
        if err_msg!=None:
            local_Wd.log.error(err_msg)
            logger.print_on_console(err_msg)
        return result


    def check_url_error_code(self):
        status=False
        value=None
        if browser_Keywords.local_bk.driver_obj != None:
            local_Wd.log.info('checking for the url error')
            try:
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', browser_Keywords.local_bk.driver_obj.current_url)
                if urls != []:
                    response=requests.get(urls[0],verify=False)
                    status_code=response.status_code
                    local_Wd.log.info(status_code)
                    if status_code in STATUS_CODE_DICT:
                        value=STATUS_CODE_DICT[status_code]
                        logger.print_on_console('Error code ',status_code,' : ',value)
                        local_Wd.log.error('Error code and value ')
                        local_Wd.log.error(status_code)
                        local_Wd.log.error(value)
                        status=True
                else:
                    local_Wd.log.info('Url is empty')
            except Exception as e:
                status_code=111
                if status_code in STATUS_CODE_DICT:
                    value=STATUS_CODE_DICT[status_code]
                    logger.print_on_console('Error code ',status_code,' : ',value)
                    local_Wd.log.error('Error code and value ')
                    local_Wd.log.error(status_code)
                    local_Wd.log.error(value)
                    status=True
                local_Wd.log.error(e)
        return status,value


    def getwebelement(self,driver,objectname):
##        objectname = str(objectname)
        webElement = None
        if objectname.strip() != '':
            identifiers = objectname.split(';')
            local_Wd.log.debug('Identifiers are ')
            local_Wd.log.debug(identifiers)
            if len(identifiers)>=3:
                try:
                    #find by rxpath
                    tempwebElement = driver.find_elements_by_xpath(identifiers[0])
                    if (len(tempwebElement) == 1):
                        logger.print_on_console('Webelement found by OI1')
                        local_Wd.log.debug('Webelement found by OI1')
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if (len(tempwebElement) == 1):
                            logger.print_on_console('Webelement found by OI2')
                            local_Wd.log.debug('Webelement found by OI2')
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if (len(tempwebElement) == 1):
                                logger.print_on_console('Webelement found by OI3')
                                local_Wd.log.debug('Webelement found by OI3')
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
##                    local_Wd.log.debug('Webelement found by relative xpath')
                    webElement = tempwebElement

                except Exception as webEx:
                    try:
                        #find by id
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if (len(tempwebElement) == 1):
                            logger.print_on_console('Webelement found by OI2')
                            local_Wd.log.debug('Webelement found by OI2')
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if (len(tempwebElement) == 1):
                                logger.print_on_console('Webelement found by OI3')
                                local_Wd.log.debug('Webelement found by OI3')
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
##                        local_Wd.log.debug('Webelement found by Id')
                        webElement = tempwebElement
                    except Exception as webEx:
                        #find by absolute Xpath
                        try:
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if (len(tempwebElement) == 1):
                                logger.print_on_console('Webelement found by OI3')
                                local_Wd.log.debug('Webelement found by OI3')
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                            webElement = tempwebElement
##                            local_Wd.log.debug('Webelement found by absolute Xpath')
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
                                local_Wd.log.debug('Webelement found by OI7')
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

            elif objectname.startswith('{') and objectname.endswith('}') and objectname in local_Wd.webelement_map:
                if len(local_Wd.webelement_map)<=4:
                    webElement=[]
                    webElement.append(local_Wd.webelement_map[objectname])
                else:
                    logger.print_on_console(MAX_SIZE_EXCEEDED)
                    local_Wd.log.error(MAX_SIZE_EXCEEDED)
                    err_msg=WEB_ELEMENT_NOT_FOUND
                    logger.print_on_console(err_msg)
                    local_Wd.log.error(err_msg)
            #Fixing issue #381
            if webElement==None or webElement== '':
                webElement = None
                err_msg=WEB_ELEMENT_NOT_FOUND
                logger.print_on_console(err_msg)
                local_Wd.log.error(err_msg)
        if isinstance(webElement,list):
            webElement=webElement[0]
        return webElement
