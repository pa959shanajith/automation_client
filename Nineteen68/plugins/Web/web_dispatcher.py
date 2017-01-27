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
from collections import OrderedDict
from constants import *
import requests
import re

import logging

log = logging.getLogger('web_dispatcher.py')

class Dispatcher:

    button_link_object = button_link_keyword.ButtonLinkKeyword()
    popup_object = popup_keywords.PopupKeywords()
    browser_object = browser_Keywords.BrowserKeywords()
    radio_checkbox_object = radio_checkbox_operations.RadioCheckboxKeywords()
    table_object = table_keywords.TableOperationKeywords()
    element_object = element_operations.ElementKeywords()
    textbox_object = textbox_operations.TextboxKeywords()
    dropdown_list_object = dropdown_listbox.DropdownKeywords()
    util_object = utilweb_operations.UtilWebKeywords()
    statict_text_object = static_text_keywords.StaticTextKeywords()
    custom_object=custom_keyword.CustomKeyword()
    webelement_map=OrderedDict()

    def __init__(self):
        self.exception_flag=''

    def dispatcher(self,teststepproperty,input,reporting_obj):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        url=teststepproperty.url.strip()
        keyword = teststepproperty.name
        driver = browser_Keywords.driver_obj
        webelement = None
        element = None

        log.info('In Web dispatcher')
        custom_dict={
                    'getStatus': ['radio','checkbox'],
                    'selectRadioButton': ['radio'],
                    'selectCheckbox': ['checkbox'],
                    'unselectCheckbox': ['checkbox'],

                    'selectValueByIndex':['dropdown','listbox'],
                    'selectValueByText': ['dropdown','listbox'],

                    'setText': ['textbox','textarea','password','number','email','url'],
                    'sendValue':['textbox','textarea','password','number','email','url'],
                    'getText': ['textbox','textarea','password','number','email','url'],
                    'setSecureText':['textbox','password']

                    }
        custom_dict_element={'element':['clickElement','doubleClick','rightClick','getElementText','verifyElementText','drag', 'drop','getToolTipText','verifyToolTipText','verifyExists', 'verifyDoesNotExists', 'verifyHidden','verifyVisible', 'switchToTab','switchToWindow','setFocus','sendFunctionKeys',
                                        'tab','waitForElementVisible','mouseHover','saveFile']}

        result=(TEST_RESULT_FAIL,TEST_RESULT_FALSE,None,None)

        def print_error(err_msg):
            err_msg=ERROR_CODE_DICT['ERR_CUSTOM_MISMATCH']
            logger.print_on_console(err_msg)
            log.error(err_msg)

        def send_webelement_to_keyword(driver,objectname,url):
            webelement=None
            if driver != None:

                log.debug('In send_webelement_to_keyword method')
                #check if the element is in iframe or frame

                if url !=  '' and self.custom_object.is_int(url):
                    log.debug('Encountered iframe/frame url')
                    self.custom_object.switch_to_iframe(url,driver.current_window_handle)
                    driver = browser_Keywords.driver_obj
                if objectname==CUSTOM:
                    log.info('Encountered custom object')
                    log.info('Custom flag is ')
                    log.info(teststepproperty.custom_flag)
                    if teststepproperty.custom_flag:
                        reference_element=self.getwebelement(driver,teststepproperty.parent_xpath)
                        log.debug('Reference_element ')
                        log.debug(reference_element)
                        if reference_element != None:
                            reference_element = reference_element[0]
                            log.info('Reference_element is found')
                            if keyword==GET_OBJECT_COUNT:
                                log.info('Keyword is ')
                                log.info(keyword)
                                webelement=reference_element
                            elif len(input)>=3:
                                if (keyword in custom_dict and input[0].lower() in custom_dict[keyword]) or keyword in custom_dict_element.values()[0]:
                                    webelement=self.custom_object.getCustomobject(reference_element,input[0],input[1],input[2],teststepproperty.url)
                                    log.debug(MSG_CUSTOM_FOUND)
                                    input.reverse()
                                    for x in range(0,3):
                                        input.pop()
                                    input.reverse()
                                else:
                                    print_error('ERR_CUSTOM_MISMATCH')
                            else:
                                print_error('ERR_PRECONDITION_NOTMET')
                                print_error('ERR_CUSTOM_NOTFOUND')

                        else:
                            print_error('ERR_REF_ELE_NULL')
                            print_error('ERR_CUSTOM_NOTFOUND')

                else:
                    webelement = self.getwebelement(driver,objectname)
                    if webelement != None:
                        webelement = webelement[0]
                        log.info(WEB_ELEMENT_FOUND)
                        logger.print_on_console(WEB_ELEMENT_FOUND)
            return webelement


        def find_browser_info(reporting_obj):
            #Find the browser type and browser name if driver_obj is not None
            if browser_Keywords.driver_obj is not None:
                log.info('Finding the browser information')
                browser_info=browser_Keywords.driver_obj.capabilities
                reporting_obj.browser_version=browser_info.get('version')
                reporting_obj.browser_type=browser_info.get('browserName')
                log.info(reporting_obj.browser_version)
                log.info(reporting_obj.browser_type)



        try:
            dict={'getObjectCount':self.custom_object.get_object_count,
                  'click': self.button_link_object.click,
                  'verifyButtonName' : self.button_link_object.verify_button_name,
                  'getLinkText'    : self.button_link_object.get_link_text,
                  'verifyLinkText' : self.button_link_object.verify_link_text,
                  'press'  : self.button_link_object.press,
                  'doubleClick' : self.button_link_object.double_click,
                  'rightClick' : self.button_link_object.right_click,
                  'uploadFile'  : self.button_link_object.upload_file,

                  'acceptPopUp' : self.popup_object.accept_popup,
                  'dismissPopUp':self.popup_object.dismiss_popup,
                  'getPopUpText':self.popup_object.get_popup_text,
                  'verifyPopUpText':self.popup_object.verify_popup_text,


                  'getStatus': self.radio_checkbox_object.get_status,
                  'selectRadioButton': self.radio_checkbox_object.select_radiobutton,
                  'selectCheckbox': self.radio_checkbox_object.select_checkbox,
                  'unselectCheckbox': self.radio_checkbox_object.unselect_checkbox,

                  'getRowCount' : self.table_object.getRowCount,
                  'getColumnCount' : self.table_object.getColoumnCount,
                  'getCellValue' : self.table_object.getCellValue,
                  'verifyCellValue' : self.table_object.verifyCellValue,
                  'cellClick' : self.table_object.cellClick,
                  'getRowNumByText' : self.table_object.getRowNumByText,
                  'getColNumByText' : self.table_object.getColNumByText,
                  'getInnerTable' : self.table_object.getInnerTable,


                  'getElementText' : self.element_object.get_element_text,
                  'verifyElementText' : self.element_object.verify_element_text,
                  'clickElement' : self.element_object.click_element,
                  'getToolTipText' : self.element_object.get_tooltip_text,
                  'verifyToolTipText' : self.element_object.verify_tooltip_text,
                  'drag':self.element_object.drag,
                  'drop':self.element_object.drop,

                  'setText':self.textbox_object.set_text,
                  'sendValue':self.textbox_object.send_value,
                  'getText':self.textbox_object.get_text,
                  'verifyText':self.textbox_object.verify_text,
                  'clearText':self.textbox_object.clear_text,
                  'getTextboxLength':self.textbox_object.gettextbox_length,
                  'verifyTextboxLength':self.textbox_object.verifytextbox_length,
                  'setSecureText':self.textbox_object.setsecuretext,

                  'selectValueByIndex':self.dropdown_list_object.selectValueByIndex,
                  'getCount':self.dropdown_list_object.getCount,
                  'selectValueByText':self.dropdown_list_object.selectValueByText,
                  'verifySelectedValue':self.dropdown_list_object.verifySelectedValue,
                  'verifyCount':self.dropdown_list_object.verifyCount,
                  'selectAllValues':self.dropdown_list_object.selectAllValues,
                  'selectMultipleValuesByIndexes':self.dropdown_list_object.selectMultipleValuesByIndexes,
                  'getSelected':self.dropdown_list_object.getSelected,
                  'selectMultipleValuesByText':self.dropdown_list_object.selectMultipleValuesByText,
                  'getMultipleValuesByIndexes':self.dropdown_list_object.getMultipleValuesByIndexes,
                  'verifyAllValues':self.dropdown_list_object.verifyAllValues,
                  'getValueByIndex':self.dropdown_list_object.getValueByIndex,
                  'verifyValuesExists':self.dropdown_list_object.verifyValuesExists,
                  'deselectAll':self.dropdown_list_object.deselectAll,


                  'verifyVisible':self.util_object.verify_visible,
                  'verifyExists':self.util_object.verify_exists,
                  'verifyDoesNotExists':self.util_object.verify_doesnot_exists,
                  'verifyEnabled':self.util_object.verify_enabled,
                  'verifyDisabled':self.util_object.verify_disabled,
                  'verifyHidden':self.util_object.verify_hidden,
                  'verifyReadOnly':self.util_object.verify_readonly,
                  'setFocus':self.util_object.setfocus,
                  'mouseHover':self.util_object.mouse_hover,
                  'tab':self.util_object.tab,
                  'sendFunctionKeys':self.util_object.sendfunction_keys,
                  'rightClick':self.util_object.rightclick,
                  'mouseClick':self.util_object.mouse_click,
                  'verifyWebImages':self.util_object.verify_web_images,
                  'waitForElementVisible':self.element_object.waitforelement_visible,



                  'openBrowser':self.browser_object.openBrowser,
                  'navigateToURL':self.browser_object.navigateToURL,
                  'openNewBrowser':self.browser_object.openNewBrowser,
                  'getPageTitle':self.browser_object.getPageTitle,
                  'getCurrentURL':self.browser_object.getCurrentURL,
                  'maximizeBrowser':self.browser_object.maximizeBrowser,
                  'refresh':self.browser_object.refresh,
                  'verifyCurrentURL':self.browser_object.verifyCurrentURL,
                  'closeBrowser':self.browser_object.closeBrowser,
                  'closeSubWindows':self.browser_object.closeSubWindows,
                  'switchToWindow':self.util_object.switch_to_window,
                  'verifyTextExists':self.statict_text_object.verify_text_exists,
                  'verifyPageTitle':self.browser_object.verify_page_title,
                  'clearCache':self.browser_object.clear_cache,
                  'navigateWithAuthenticate':self.browser_object.navigate_with_authenticate
                }

            if keyword in dict.keys():

                #Finding the webelement for NON_WEBELEMENT_KEYWORDS
                if keyword not in NON_WEBELEMENT_KEYWORDS:
                    webelement=send_webelement_to_keyword(driver,objectname,url)
                    if webelement == None and self.exception_flag:
                        result=TERMINATE

                elif keyword==WAIT_FOR_ELEMENT_VISIBLE:
                    identifiers = objectname.split(';')
                    input=identifiers[0]

                if result != TERMINATE:

                    result= dict[keyword](webelement,input)
                    if keyword == GET_INNER_TABLE and (output != '' and output.startswith('{') and output.endswith('}')):
                        self.webelement_map[output]=result[2]

                    elif keyword not in [OPEN_BROWSER,OPEN_NEW_BROWSER,CLOSE_BROWSER]:
                        res,value=self.check_url_error_code()
                        if res:
                            result=TERMINATE

                    elif keyword==OPEN_BROWSER:
                        find_browser_info(reporting_obj)


            else:
                logger.print_on_console(INVALID_KEYWORD)
                log.error(INVALID_KEYWORD)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        return result


    def check_url_error_code(self):
        status=False
        value=None
        if browser_Keywords.driver_obj != None:
            log.info('checking for the url error')
            try:
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', browser_Keywords.driver_obj.current_url)
                response=requests.get(urls[0])
                status_code=response.status_code
                log.info(status_code)
                if status_code in STATUS_CODE_DICT:
                    value=STATUS_CODE_DICT[status_code]
                    logger.print_on_console('Error code ',status_code,' : ',value)
                    log.error('Error code ',status_code,' : ',value)
                    status=True
            except Exception as e:
                log.error(e)
        return status,value


    def getwebelement(self,driver,objectname):
        objectname = str(objectname)
        webElement = None
        if objectname.strip() != '':

            identifiers = objectname.split(';')
            log.debug('Identifiers are ')
            log.debug(identifiers)
            if len(identifiers)>=3:
                try:
                    #find by rxpath
                    tempwebElement = driver.find_elements_by_xpath(identifiers[0])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                    log.debug('Webelement found by relative xpath')
                    webElement = tempwebElement

                except Exception as webEx:
                    try:
                        #find by id
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                        log.debug('Webelement found by Id')
                        webElement = tempwebElement
                    except Exception as webEx:
                        #find by absolute Xpath
                        try:
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                            webElement = tempwebElement
                            log.debug('Webelement found by absolute Xpath')
                        except Exception as webEx:
                            err_msg=WEB_ELEMENT_NOT_FOUND
                            logger.print_on_console(err_msg)
                            log.error(err_msg)

            elif objectname.startswith('{') and objectname.endswith('}') and self.webelement_map.has_key(objectname):
                if len(self.webelement_map)<=4:
                    webElement=[]
                    webElement.append(self.webelement_map[objectname])
                else:
                    logger.print_on_console(MAX_SIZE_EXCEEDED)
                    log.error(MAX_SIZE_EXCEEDED)
                    err_msg=WEB_ELEMENT_NOT_FOUND
                    logger.print_on_console(err_msg)
                    log.error(err_msg)


        return webElement

