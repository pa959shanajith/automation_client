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
import wx
import iris_operations
import web_keywords
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
local_Wd = threading.local()

class Dispatcher:

    def __init__(self):
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
        # local_Wd.driver_util = browser_Keywords.Singleton_DriverUtil()

        local_Wd.browser_obj_sl = web_keywords.Browser_Keywords()
        local_Wd.browser_popup_obj_sl = web_keywords.Browser_Popup_Keywords()
        local_Wd.button_link_obj_sl = web_keywords.Button_link_Keywords()
        local_Wd.dropdown_obj_sl = web_keywords.Dropdown_Keywords()
        local_Wd.element_obj_sl = web_keywords.Element_Keywords()
        local_Wd.radio_check_obj_sl = web_keywords.Radio_checkbox_Keywords()
        local_Wd.table_obj_sl = web_keywords.Table_Keywords()
        local_Wd.textbox_obj_sl = web_keywords.Textbox_Keywords()
        local_Wd.util_obj_sl = web_keywords.Util_Keywords()

        local_Wd.webelement_map=OrderedDict()
        iris_object = iris_operations.IRISKeywords()
        local_Wd.log = logging.getLogger('web_dispatcher.py')
        self.identifier_dict={
            'rxpath': 'find_elements_by_xpath',
            'id': 'find_elements_by_id',
            'xpath': 'find_elements_by_xpath',
            'name':'find_elements_by_name',
            'classname':'find_elements_by_class_name',
            'css_selector': 'find_elements_by_css_selector'
        }

        self.web_dict={
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
            'doublecellclick' : local_Wd.table_object.doubleCellClick,
            # grid keywords
            'horizontalscroll' : local_Wd.table_object.horizontalScroll,
            'verticalscroll' : local_Wd.table_object.verticalScroll,
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
            'sendsecurefunctionkeys':local_Wd.util_object.sendsecurefunction_keys,
            'rightclick':local_Wd.util_object.rightclick,
            'mouseclick':local_Wd.util_object.mouse_click,
            'verifywebimages':local_Wd.util_object.verify_web_images,
            'imagesimilaritypercentage':local_Wd.util_object.image_similarity_percentage,
            'waitforelementvisible':local_Wd.element_object.waitforelement_visible,
            'getelementtagvalue': local_Wd.util_object.get_element_tag_value,
            'getattributevalue': local_Wd.util_object.get_attribute_value,
            'verifyattribute': local_Wd.util_object.verify_attribute,

            'openbrowser':local_Wd.browser_object.openBrowser,
            'getbrowsertoforeground':local_Wd.browser_object.get_foreground_window,
            'navigatetourl':local_Wd.browser_object.navigateToURL,
            'getpagetitle':local_Wd.browser_object.getPageTitle,
            'getcurrenturl':local_Wd.browser_object.getCurrentURL,
            'maximizebrowser':local_Wd.browser_object.maximizeBrowser,
            'refresh':local_Wd.browser_object.refresh,
            'verifycurrenturl':local_Wd.browser_object.verifyCurrentURL,
            'closebrowser':local_Wd.browser_object.closeBrowser,
            'closesubwindows':local_Wd.browser_object.closeSubWindows,
            'switchtowindow':local_Wd.browser_object.switch_to_window,
            'sendkeys':local_Wd.util_object.send_keys,
            'verifytextexists':local_Wd.statict_text_object.verify_text_exists,
            'verifypagetitle':local_Wd.browser_object.verify_page_title,
            'clearcache':local_Wd.browser_object.clear_cache,
            'navigatewithauthenticate':local_Wd.browser_object.navigate_with_authenticate,
            'navigateback':local_Wd.browser_object.navigate_back,
            'opennewtab':local_Wd.browser_object.openNewTab,
            'execute_js':local_Wd.browser_object.execute_js,
            'getbrowsername': local_Wd.browser_object.getBrowserName,
            'savefile': local_Wd.browser_object.save_file,

            'clickiris':iris_object.clickiris,
            'doubleclickiris':iris_object.doubleclickiris,
            'rightclickiris':iris_object.rightclickiris,
            'settextiris':iris_object.settextiris,
            'setsecuretextiris':iris_object.setsecuretextiris,
            'gettextiris':iris_object.gettextiris,
            'getrowcountiris':iris_object.getrowcountiris,
            'getcolcountiris':iris_object.getcolcountiris,
            'getcellvalueiris':iris_object.getcellvalueiris,
            'verifyexistsiris':iris_object.verifyexistsiris,
            'verifytextiris':iris_object.verifytextiris,
            'cleartextiris':iris_object.cleartextiris,
            'dragiris':iris_object.dragiris,
            'dropiris':iris_object.dropiris,
            'mousehoveriris':iris_object.mousehoveriris,
            'setcellvalueiris':iris_object.setcellvalueiris,
            'verifycellvalueiris':iris_object.verifycellvalueiris,
            'clickcelliris':iris_object.clickcelliris,
            'doubleclickcelliris':iris_object.doubleclickcelliris,
            'rightclickcelliris':iris_object.rightclickcelliris,
            'mousehovercelliris':iris_object.mousehovercelliris,
            'getstatusiris':iris_object.getstatusiris,
            'scrollupiris':iris_object.scrollupiris,
            'scrolldowniris':iris_object.scrolldowniris,
            'scrollleftiris':iris_object.scrollleftiris,
            'scrollrightiris':iris_object.scrollrightiris
        }

        self.sauce_web_dict = {
            # 'getobjectcount':local_Wd.custom_object.get_object_count,
            # 'getobject':local_Wd.custom_object.get_object,
            'click': local_Wd.element_obj_sl.click,
            'press'  : local_Wd.element_obj_sl.press,
            'doubleClick' : local_Wd.element_obj_sl.doubleClick,
            'rightClick' : local_Wd.element_obj_sl.rightClick,
            # 'uploadFile'  : local_Wd.element_obj_sl.uploadFile,

            'verifyButtonName' : local_Wd.button_link_obj_sl.verifyButtonName,
            'getButtonName': local_Wd.button_link_obj_sl.getButtonName,
            'getLinkText'    : local_Wd.button_link_obj_sl.getLinkText,
            'verifyLinkText' : local_Wd.button_link_obj_sl.verifyLinkText,

            'acceptPopUp' : local_Wd.browser_popup_obj_sl.acceptPopUp,
            'dismissPopUp': local_Wd.browser_popup_obj_sl.dismissPopUp,
            'getPopUpText': local_Wd.browser_popup_obj_sl.getPopUpText,
            'verifyPopUpText': local_Wd.browser_popup_obj_sl.verifyPopUpText,

            'getStatus': local_Wd.radio_check_obj_sl.getStatus,
            'selectRadioButton': local_Wd.radio_check_obj_sl.selectRadioButton,
            'selectCheckbox': local_Wd.radio_check_obj_sl.selectCheckbox,
            'unselectCheckbox': local_Wd.radio_check_obj_sl.unselectCheckbox,

            'getRowCount' : local_Wd.table_obj_sl.getRowCount,
            'getColumnCount' : local_Wd.table_obj_sl.getColumnCount,
            'getCellValue' : local_Wd.table_obj_sl.getCellValue,
            'verifyCellValue' : local_Wd.table_obj_sl.verifyCellValue,
            'cellClick' : local_Wd.table_obj_sl.cellClick,
            'getRowNumByText' : local_Wd.table_obj_sl.getRowNumByText,
            'getColNumByText' : local_Wd.table_obj_sl.getColNumByText,
            'getInnerTable' : local_Wd.table_obj_sl.getInnerTable,
            'getCellToolTip' : local_Wd.table_obj_sl.getCellToolTip,
            'verifyCellToolTip' : local_Wd.table_obj_sl.verifyCellToolTip,

            'getElementText' : local_Wd.element_obj_sl.getElementText,
            'verifyElementText' : local_Wd.element_obj_sl.verifyElementText,
            'clickElement' : local_Wd.element_obj_sl.click,
            'getToolTipText' : local_Wd.element_obj_sl.getToolTipText,
            'verifyToolTipText' : local_Wd.element_obj_sl.verifyToolTipText,
            'drag': local_Wd.util_obj_sl.drag,
            'drop': local_Wd.util_obj_sl.drop,
            # 'dropFile': local_Wd.element_obj_sl.dropFile,

            'setText': local_Wd.textbox_obj_sl.setText,
            'sendValue': local_Wd.textbox_obj_sl.sendValue,
            'getText': local_Wd.textbox_obj_sl.getText,
            'verifyText': local_Wd.textbox_obj_sl.verifyText,
            'clearText': local_Wd.textbox_obj_sl.clearText,
            'getTextboxLength': local_Wd.textbox_obj_sl.getTextboxLength,
            'verifyTextboxLength': local_Wd.textbox_obj_sl.verifyTextboxLength,
            'setSecureText': local_Wd.textbox_obj_sl.setSecureText,
            'sendSecureValue': local_Wd.textbox_obj_sl.sendSecureValue,

            'selectValueByIndex': local_Wd.dropdown_obj_sl.selectValueByIndex,
            'getCount': local_Wd.dropdown_obj_sl.getCount,
            'selectValueByText': local_Wd.dropdown_obj_sl.selectValueByText,
            'verifySelectedValues': local_Wd.dropdown_obj_sl.verifySelectedValues,
            'verifySelectedValue': local_Wd.dropdown_obj_sl.verifySelectedValue,
            'verifyCount': local_Wd.dropdown_obj_sl.verifyCount,
            'selectAllValues': local_Wd.dropdown_obj_sl.selectAllValues,
            'selectMultipleValuesByIndexes': local_Wd.dropdown_obj_sl.selectMultipleValuesByIndexes,
            'getSelected': local_Wd.dropdown_obj_sl.getSelected,
            'selectMultipleValuesByText': local_Wd.dropdown_obj_sl.selectMultipleValuesByText,
            'getMultipleValuesByIndexes': local_Wd.dropdown_obj_sl.getMultipleValuesByIndexes,
            'verifyAllValues': local_Wd.dropdown_obj_sl.verifyAllValues,
            'selectByAbsoluteValue': local_Wd.dropdown_obj_sl.selectByAbsoluteValue,
            'getAllValues': local_Wd.dropdown_obj_sl.getAllValues,
            'getValueByIndex': local_Wd.dropdown_obj_sl.getValueByIndex,
            'verifyValuesExists': local_Wd.dropdown_obj_sl.verifyValuesExists,
            'deselectAll': local_Wd.dropdown_obj_sl.deselectAll,

            'verifyVisible': local_Wd.util_obj_sl.verifyVisible,
            'verifyExists': local_Wd.util_obj_sl.verifyExists,
            'verifyDoesNotExists': local_Wd.util_obj_sl.verifyDoesNotExists,
            'verifyEnabled': local_Wd.util_obj_sl.verifyEnabled,
            'verifyDisabled': local_Wd.util_obj_sl.verifyDisabled,
            'verifyHidden': local_Wd.util_obj_sl.verifyHidden,
            'verifyReadOnly': local_Wd.util_obj_sl.verifyReadOnly,
            'tab': local_Wd.util_obj_sl.tab,
            'sendFunctionKeys': local_Wd.util_obj_sl.sendFunctionKeys,
            'setFocus': local_Wd.element_obj_sl.setFocus,
            'mouseHover': local_Wd.element_obj_sl.mouseHover,
            # 'rightclick':obj.rightclick,
            # 'mouseclick': local_Wd.util_obj_sl.mouseClick,
            # 'verifywebimages': local_Wd.util_obj_sl.verify_web_images,
            # 'imagesimilaritypercentage': local_Wd.util_obj_sl.image_similarity_percentage,
            'waitForElementVisible': local_Wd.util_obj_sl.waitForElementVisible,
            'getElementTagValue': local_Wd.element_obj_sl.getElementTagValue,
            'getAttributeValue': local_Wd.element_obj_sl.getAttributeValue,
            'verifyAttribute': local_Wd.element_obj_sl.verifyAttribute,

            'openBrowser': local_Wd.browser_obj_sl.openBrowser,
            'navigateToURL': local_Wd.browser_obj_sl.navigateToURL,
            'getPageTitle': local_Wd.browser_obj_sl.getPageTitle,
            'getCurrentURL': local_Wd.browser_obj_sl.getCurrentURL,
            'maximizeBrowser': local_Wd.browser_obj_sl.maximizeBrowser,
            'refresh': local_Wd.browser_obj_sl.refresh,
            'verifyCurrentURL': local_Wd.browser_obj_sl.verifyCurrentURL,
            'closeBrowser': local_Wd.browser_obj_sl.closeBrowser,
            'closeSubWindows': local_Wd.browser_obj_sl.closeSubWindows,
            'switchToWindow': local_Wd.browser_obj_sl.switchToWindow,
            'verifyTextExists': local_Wd.browser_obj_sl.verifyTextExists,
            'verifyPageTitle': local_Wd.browser_obj_sl.verifyPageTitle,
            'clearCache': local_Wd.browser_obj_sl.clearCache,
            'navigateWithAuthenticate': local_Wd.browser_obj_sl.navigateWithAuthenticate,
            'navigateBack': local_Wd.browser_obj_sl.navigateBack,
            'openNewTab': local_Wd.browser_obj_sl.openNewTab,
            'execute_js': local_Wd.browser_obj_sl.execute_js,
            'getBrowserName': local_Wd.browser_obj_sl.getBrowserName
        }

        self.browsers_sl={'1':{'browserName': "chrome", 'sauce:options':{}},'2':{'browserName': "firefox", 'sauce:options':{}},'3':{'browserName': "internet explorer", 'sauce:options':{}},'7':{'browserName': "MicrosoftEdge", 'sauce:options':{}},'8':{'browserName': "MicrosoftEdge", 'sauce:options':{}}}
        self.sauce_conf = web_keywords.Sauce_Config().get_sauceconf()
        self.exception_flag=''
        self.action=None
        self.wxObject=None
        self.thread=None

    def dispatcher(self,teststepproperty,input,reporting_obj,wxObject,mythread,execution_env):
        global simple_debug_gwto, status_gwto
        status_gwto =False
        simple_debug_gwto=False
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        url=teststepproperty.url.strip()
        keyword = teststepproperty.name
        keyword = keyword.lower()
        if self.action == DEBUG and browser_Keywords.driver_pre != None:
            browser_Keywords.local_bk.driver_obj = browser_Keywords.driver_pre
            driver_util = browser_Keywords.Singleton_DriverUtil()
            v = driver_util.check_if_driver_exists_in_map(teststepproperty.browser_type[0])
            if v and v != 'stale':
                browser_Keywords.local_bk.driver_obj = v
                browser_Keywords.driver_pre = v
        driver = browser_Keywords.local_bk.driver_obj
        self.wxObject=wxObject
        self.thread=mythread
        webelement = None
        err_msg=None
        configvalues = readconfig.configvalues

        local_Wd.log.info('In Web dispatcher')
        custom_dict={
            'getstatus': ['radio','checkbox'],
            'selectradiobutton': ['radio'],
            'selectcheckbox': ['checkbox'],
            'unselectcheckbox': ['checkbox'],
            'selectvaluebyindex':['dropdown','listbox','select'],
            'selectvaluebytext': ['dropdown','listbox','select'],
            'getallvalues':['dropdown','listbox','select'],
            'verifyallvalues': ['dropdown','listbox','select'],
            'getcount': ['dropdown','listbox','select'],
            'getselected': ['dropdown','listbox','select'],
            'getvaluebyindex': ['dropdown','listbox','select'],
            'verifycount': ['dropdown','listbox','select'],
            'verifyselectedvalue': ['dropdown','listbox','select'],
            'verifyvaluesexists': ['dropdown','listbox','select'],
            'settext': ['textbox','textarea','password','number','email','url','div','span'],
            'cleartext': ['textbox','textarea','password','number','email','url'],
            'gettextboxlength': ['textbox','textarea','password','number','email','url'],
            'verifytext': ['textbox','textarea','password','number','email','url'],
            'sendvalue':['textbox','textarea','password','number','email','url','div','span'],
            'gettext': ['textbox','textarea','password','number','email','url'],
            'setsecuretext':['textbox','password'],
            'sendsecurevalue':['textbox','password'],
            'getattributevalue':['radio','checkbox','dropdown','select','listbox','textbox','textarea','password','number','email','url','grid'],
            'verifyattribute':['radio','checkbox','dropdown','select','listbox','textbox','textarea','password','number','email','url','grid'],
            'getbuttonname': ['button','submit','reset'],
            'verifybuttonname': ['button','submit','reset'],
            'getlinktext': ['a','link'],
            'verifylinktext': ['a','link'],
            'verifywebimages': ['img'],
            'imagesimilaritypercentage': ['img']
        }
        custom_dict_element={'element':['getobjectcount','getobject','clickelement','doubleclick','rightclick','getelementtext','verifyelementtext','drag', 'drop','gettooltiptext','verifytooltiptext','verifyexists', 'verifydoesnotexists','verifyvisible', 'switchtotab','switchtowindow','setfocus','sendfunctionkeys', 'sendsecurefunctionkeys',
            'tab','waitforelementvisible','mousehover','press','verifyenabled','verifydisabled','verifyreadonly','getattributevalue','verifyattribute','getrowcount','getcolumncount','getcellvalue','verifycellvalue','getcelltooltip','verifycelltooltip','cellclick','getrownumbytext','getcolnumbytext','getinnertable','selectbyabsolutevalue','horizontalscroll','verticalscroll','click','uploadfile','dropfile']}

        result=[TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,err_msg]

        def print_error(err_msg):
            err_msg=ERROR_CODE_DICT[err_msg]
            logger.print_on_console(err_msg)
            local_Wd.log.error(err_msg)

        def send_webelement_to_keyword(driver,objectname,url):
            webelement=None
            getObjectFlag=False
            if driver:
                local_Wd.log.debug('In send_webelement_to_keyword method')
                #check if the element is in iframe or frame
                try:
                    if url and local_Wd.custom_object.is_int(url):
                        local_Wd.log.debug('Encountered iframe/frame url')
                        local_Wd.custom_object.switch_to_iframe(url,driver.current_window_handle)
                        driver = browser_Keywords.local_bk.driver_obj
                    if objectname==CUSTOM:
                        local_Wd.log.info('Encountered custom object')
                        local_Wd.log.info('Custom flag is ')
                        local_Wd.log.info(teststepproperty.custom_flag)
                        custom_input=teststepproperty.inputval[0].split(';')
                        if teststepproperty.custom_flag:
                            if len(input)>3 and custom_input[-1].startswith('{{') and custom_input[-1].endswith('}}'):
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
                                reference_element=self.getwebelement(driver,teststepproperty.parent_xpath,teststepproperty.stepnum,teststepproperty.custname)
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
                                        absMatch=False
                                        if input[-1]=='abs':
                                            absMatch=True
                                        webelement=local_Wd.custom_object.getCustomobject(reference_element,input[0],input[1],input[2],teststepproperty.url,absMatch)
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
                            import UserObjectScrape
                            webscrape=UserObjectScrape.UserObject()
                            obj1=UserObjectScrape.update_data.copy()
                            for k,v in obj1.items():
                                if teststepproperty.custname in v:
                                    objectname=v[teststepproperty.custname]
                                    UserObjectScrape.update_data[str(teststepproperty.stepnum)]=v
                            webelement = self.getwebelement(driver,objectname,teststepproperty.stepnum,teststepproperty.custname)
                            if(obj_flag!=False):
                                import UserObjectScrape
                                webscrape=UserObjectScrape.UserObject()
                                # obj=core_utils.CoreUtils()
                                webscrape.update_scrape_object(url,objectname,obj_flag,teststepproperty.stepnum,teststepproperty.custname)
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


        def find_browser_info(reporting_obj,mythread):
            #Find the browser type and browser name if driver_obj is not None
            if browser_Keywords.local_bk.driver_obj is not None:
                local_Wd.log.info('Finding the browser information')
                browser_info=browser_Keywords.local_bk.driver_obj.capabilities
                reporting_obj.browser_version=browser_info.get('version')
                if(reporting_obj.browser_version == '' or reporting_obj.browser_version == None):
                    reporting_obj.browser_version= browser_info['browserVersion']
                reporting_obj.browser_type=BROWSER_NAME[input[0]]
            elif browser_Keywords.local_bk.driver_obj is None:
                reporting_obj.browser_type=BROWSER_NAME[input[0]]
                reporting_obj.browser_version = 'N/A'
                local_Wd.log.info(reporting_obj.browser_version)
                local_Wd.log.info(reporting_obj.browser_type)


        try:
            browsername = ''
            if browser_Keywords.local_bk.driver_obj is not None:
                browsername = BROWSER_NAME_MAP[browser_Keywords.local_bk.driver_obj.name.strip()]
            if self.action == DEBUG and keyword != 'openbrowser':
                req_browsername = BROWSER_NAME.get(teststepproperty.browser_type[0], 'N/A')
                if req_browsername != browsername:
                    err_msg = 'Requested browser not Active, please open browser'
                    logger.print_on_console(err_msg)
                    local_Wd.log.error(err_msg)
                    result[3] = "Requested Browser not Available"
                    return result
            window_ops_list=['click','press','doubleclick','rightclick','uploadfile','acceptpopup',
                'dismisspopup','selectradiobutton','selectcheckbox','unselectcheckbox','cellclick',
                'clickelement','drag','drop','settext','sendvalue','cleartext','setsecuretext',
                'sendsecurevalue','selectvaluebyindex','selectvaluebytext','selectallvalues',
                'selectmultiplevaluesbyindexes','selectmultiplevaluesbytext','verifyvaluesexists',
                'deselectall','setfocus','mousehover','tab','sendfunctionkeys','rightclick',
                'mouseclick','openbrowser','navigatetourl','refresh','closebrowser','closesubwindows',
                'switchtowindow','clearcache','navigatewithauthenticate','sendsecurefunctionkeys']
            if browser_Keywords.local_bk.driver_obj is not None:
                browser_info=browser_Keywords.local_bk.driver_obj.capabilities
                reporting_obj.browser_type=browsername
                reporting_obj.browser_version=browser_info.get('version')
                if(reporting_obj.browser_version == '' or reporting_obj.browser_version == None):
                    reporting_obj.browser_version= browser_info['browserVersion']
            if execution_env['env'] == 'saucelabs' and teststepproperty.name in list(self.sauce_web_dict.keys()):
                if teststepproperty.custname=='@Browser' or teststepproperty.custname=='@BrowserPopUp':
                    if(teststepproperty.name=="openBrowser"):
                        browser=teststepproperty.inputval[0]
                        self.browsers_sl[browser]["platform"]=self.sauce_conf["platform"]
                        if browser in ['7','8'] and self.sauce_conf["platform"]!='Windows 10':
                            logger.print_on_console('Microsoft Edge browser is supported only in Windows 10')
                            return 'Terminate'
                        self.browsers_sl[browser]["sauce:options"].update({"name":teststepproperty.testscript_name})
                        self.browsers_sl[browser]["sauce:options"].update({"idleTimeout":90})
                        result = self.sauce_web_dict[teststepproperty.name](self.sauce_conf['remote_url'],self.browsers_sl[browser],execution_env['scenario'])
                        driver = web_keywords.local_wk.driver
                        browser_Keywords.local_bk.driver_obj = web_keywords.local_wk.driver
                        find_browser_info(reporting_obj,mythread)
                    else:
                        result = self.sauce_web_dict[teststepproperty.name](input)
                elif teststepproperty.name in self.sauce_web_dict:
                    xpath=teststepproperty.objectname.split(';')[0]
                    if(teststepproperty.name=="waitForElementVisible"):
                        input=xpath
                    driver.switch_to.default_content()
                    webelement=send_webelement_to_keyword(web_keywords.local_wk.driver,objectname,url)
                    result = self.sauce_web_dict[teststepproperty.name](webelement,input)
                else:
                    logger.print_on_console(teststepproperty.name+" keyword is not supported in saucelabs execution.")
                    return False
            elif execution_env['env'] == 'default' and keyword in list(self.web_dict.keys()):
                flag=False
                #Finding the webelement for NON_WEBELEMENT_KEYWORDS
                if (keyword not in NON_WEBELEMENT_KEYWORDS) and (teststepproperty.name!="waitForElementVisible"):
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
                                    ele_th[i]=threading.Thread(target = self.find_ele, name=i, args = (i,globalWait_to,browser_Keywords.local_bk.driver_obj,element_present,local_Wd.log))
                                    ele_th[i].start()
                            for i in ele_th:
                                ele_th[i].join()
                            if(status_gwto):
                                msg='Element Found. Global Wait Timeout completed'
                                local_Wd.log.info(msg)
                                logger.print_on_console(msg)
                                webelement=send_webelement_to_keyword(driver,objectname,url)
                            else:
                                msg1='Element not Found. Global Wait Timeout executed'
                                logger.print_on_console(msg1)
                                local_Wd.log.error(msg1)
                                if simple_debug_gwto:
                                    webelement=send_webelement_to_keyword(driver,objectname,url)
                        except Exception as e:
                            local_Wd.log.error(e)
                    if webelement == None and self.exception_flag:
                        result=TERMINATE

                elif keyword==WAIT_FOR_ELEMENT_VISIBLE:
                    if objectname==CUSTOM:
                        webelement=send_webelement_to_keyword(driver,objectname,url)
                        objectname=local_Wd.custom_object.getElementXPath(webelement)
                    if url !=  '' and local_Wd.custom_object.is_int(url):
                        try:
                            local_Wd.log.debug('Encountered iframe/frame url')
                            local_Wd.custom_object.switch_to_iframe(url,driver.current_window_handle,flag=True)
                            driver = browser_Keywords.local_bk.driver_obj
                        except Exception as e:
                            local_Wd.log.error(e,exc_info=True)
                            err_msg='Control failed to switch to frame/iframe'
                            result[3]=err_msg
                        if(err_msg): return result
                    identifiers = objectname.split(';')
                    input=identifiers[0]

                if result != TERMINATE:

                    if keyword==OPEN_BROWSER:
                        input.append(self.action)
                    actual_input=teststepproperty.inputval[0].split(";")
                    if(keyword.lower() in ["sendfunctionkeys","sendkeys"]):
                        input.extend(actual_input)
                    ## Issue #190 Driver control won't switch back to parent window
                    if local_Wd.popup_object.check_if_no_popup_exists():
                        local_Wd.browser_object.validate_current_window_handle()
                    if driver is not None and self.action == EXECUTE and configvalues['browser_screenshots'].lower() == 'yes':
                        window_handles_count_begin=len(driver.window_handles)
                    if objectname=="@Object":
                        ##webelement = input[0]
                        input =input[1:]
                        result= self.web_dict[keyword](webelement,input)
                    elif teststepproperty.cord!='' and teststepproperty.cord!=None:
                        if teststepproperty.custom_flag:
                            if (keyword.lower() == 'getstatusiris') : result = self.web_dict[keyword](webelement,input,output,teststepproperty.parent_xpath,teststepproperty.objectname.split(';')[-2])
                            else : result = self.web_dict[keyword](webelement,input,output,teststepproperty.parent_xpath)
                        elif (teststepproperty.objectname.split(';')[-1] == 'constant' and keyword.lower() == 'verifyexistsiris'):
                            result = self.web_dict[keyword](webelement,input,output,'constant')
                        else:
                            if (keyword.lower() == 'getstatusiris') : result = self.web_dict[keyword](webelement,input,output,teststepproperty.objectname.split(';')[-2])
                            else : result = self.web_dict[keyword](webelement,input,output)
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
                    if flag and webelement==None and teststepproperty.custname!='@Browser' and teststepproperty.name!='verifyDoesNotExists':
                        result=list(result)
                        result[3]=WEB_ELEMENT_NOT_FOUND

                    if keyword == GET_INNER_TABLE and (output != '' and output.startswith('{') and output.endswith('}')):
                        local_Wd.webelement_map[output]=result[2]
                    elif keyword not in [OPEN_BROWSER,CLOSE_BROWSER,GET_POPUP_TEXT,VERIFY_POPUP_TEXT]:
                        if configvalues['httpStatusCode'].lower() == 'yes':
                            if result[0].lower() == 'fail':
                                res,_=self.check_url_error_code()
                                if res:
                                    result=TERMINATE
                    elif keyword==OPEN_BROWSER:
                        find_browser_info(reporting_obj,mythread)

            else:
                err_msg=INVALID_KEYWORD
                result=list(result)
                result[3]=err_msg
            screen_shot_obj = screenshot_keywords.Screenshot()
            if self.action == EXECUTE:
                if result != TERMINATE:
                    result=list(result)
                    headless_mode = str(configvalues['headless_mode'])=='Yes'
                    sauceFlag = execution_env['env'] == 'saucelabs'
                    screenShot_Flag = configvalues['screenShot_Flag'].lower()
                    browser_screenshots = configvalues['browser_screenshots'].lower() == 'yes'
                    screen_details=mythread.json_data['suitedetails'][0]
                    file_path=None
                    if ((screenShot_Flag == 'fail' and result[0].lower() == 'fail')
                      or screenShot_Flag == 'all'):
                        if browser_screenshots or headless_mode or sauceFlag:
                            if local_Wd.popup_object.check_if_no_popup_exists():
                                window_handles_count_end=len(driver.window_handles)
                                diff_whc=window_handles_count_end-window_handles_count_begin
                                if keyword.lower() in ["click","press","clickelement","mouseclick","clickiris"] and diff_whc==1:
                                    local_Wd.log.debug("Look up window detected")  
                                    try:
                                        local_Wd.log.debug("checking if system is locked or not")
                                        process_name='LogonUI.exe'
                                        callall='TASKLIST'
                                        import subprocess
                                        outputall=subprocess.check_output(callall)
                                        outputstringall=str(outputall)
                                        if process_name in outputstringall:
                                            logger.print_on_console("System is Locked, Taking the screenshot using Driver")
                                            local_Wd.log.debug("System is Locked, Taking the screenshot using Driver")
                                            # file_path = screen_shot_obj.captureScreenshot(screen_details,web=True, driver=driver)
                                            # logger.print_on_console(file_path)
                                            temp=driver.current_window_handle
                                            driver.switch_to_window(driver.window_handles[-1]) 
                                            # driver.save_screenshot(file_path[2])
                                            file_path = screen_shot_obj.captureScreenshot(screen_details,web=True, driver=driver)
                                            driver.switch_to_window(temp)
                                        else: 
                                            logger.print_on_console("System is Unlocked, Taking the screenshot using generic functions")
                                            local_Wd.log.debug("System is Unlocked, Taking the screenshot using generic functions")
                                            file_path = screen_shot_obj.captureScreenshot(screen_details,web=False)
                                    except Exception as e:
                                        local_Wd.log.error(e,exc_info=True)
                                else:
                                    file_path = screen_shot_obj.captureScreenshot(screen_details,web=True, driver=driver)
                                    # driver.save_screenshot(file_path[2])
                            elif not (headless_mode or sauceFlag):
                                local_Wd.log.debug("Pop up exists; Taking the screenshot using generic functions")
                                file_path = screen_shot_obj.captureScreenshot(screen_details,web=False)
                        else:
                            file_path = screen_shot_obj.captureScreenshot(screen_details,web=False)
                        if (file_path): result.append(file_path[2])

        except TypeError as e:
            local_Wd.log.error(e,exc_info=True)
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result=list(result)
            result[3]=err_msg
            result[2]=None
        except KeyError as e:
            local_Wd.log.error(e,exc_info=True)
            err_msg=WEB_ELEMENT_NOT_FOUND
            result[3]=err_msg
        except Exception as e:
            local_Wd.log.error(e,exc_info=True)
            # logger.print_on_console('Exception at dispatcher')
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
                if urls!=[] and urlparse(urls[0]).netloc == "ntp.msn.com":
                    urls=[]
                if urls != []:
                    headers = {'User-Agent': 'AvoAssure/' + os.getenv('AVO_ASSURE_VERSION')}
                    response=requests.get(urls[0], headers=headers, verify=False, proxies=readconfig.proxies)
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

    def element_locator(self,driver,type,identifier,id_num):
        if identifier=='null': return None
        webElement = None
        try:
            index = 0
            if type == "classname" :
                if '[' and ']' in identifier:
                    index = int(identifier.split('[')[1].split(']')[0])
                    identifier = identifier.split('[')[0]
                if ' ' in identifier.strip():
                    identifier = '.'+identifier.replace(' ','.')
                    type = 'css_selector'
                webElement=getattr(driver,self.identifier_dict[type])(identifier)
                if len(webElement) > index:
                    webElement = [webElement[index]]
            else:
                webElement=getattr(driver,self.identifier_dict[type])(identifier)
            if len(webElement) == 1:
                webElement=webElement[0]
                logger.print_on_console('Webelement found by OI '+id_num)
                local_Wd.log.info('Webelement found by OI '+id_num)
            else: webElement = None
        except Exception as e:
            local_Wd.log.error(e,exc_info=True)
        return webElement

    def getwebelement(self,driver,objectname,stepnum,custname):
        ##objectname = str(objectname)
        global obj_flag,simple_debug_gwto
        obj_flag=False
        webElement = None
        if objectname.strip() != '':
            identifiers = objectname.split(';')
            local_Wd.log.debug('Identifiers are ')
            local_Wd.log.debug(identifiers)
            if len(identifiers)>=3:
                #find by Relative xpath
                webElement=self.element_locator(driver,'rxpath',identifiers[0],'1')
                if not(webElement):
                    #find by id
                    webElement=self.element_locator(driver,'id',identifiers[1],'2')
                    if not(webElement):
                        #find by absolute xpath
                        webElement=self.element_locator(driver,'xpath',identifiers[2],'3')
                        if not(webElement):
                            #find by name
                            webElement=self.element_locator(driver,'name',identifiers[3],'4')
                            if not(webElement):
                                 #find by classname
                                webElement=self.element_locator(driver,'classname',identifiers[5],'5')
                                if not(webElement):
                                #find by css selector
                                    if len(identifiers) > 11:
                                        webElement=self.element_locator(driver,'css_selector',identifiers[11],'6')
                                    if not(webElement):
                                        webElement=None
                                        local_Wd.log.info("Weblement not found with Primary identifers")
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
                    elementxpath='null'
                    for i in range (len(arrofsimilartags)):
                        local_Wd.log.debug("Elements found with similar tag names in the given boundary")
                        xpath =arrofsimilartags[i].get('xpath').split(';')
                        name=xpath[3]
                        textvalue=xpath[7]
                        #Matching with name attribute, on success , find the element by it's name
                        if name == identifiers[3]:
                            elementname= name
                        #Matching with textcontent, on success , find the element by it's xpath
                        elif textvalue==identifiers[10]:
                            elementxpath=xpath
                    if (elementname!='null') or elementxpath!='null':
                        webElement = self.element_locator(driver,'name',elementname,'7')
                        if not(webElement):
                            webElement = self.element_locator(driver,'xpath',elementxpath[2],'8')
                        else: local_Wd.log.info("Weblement not found with Advanced object recognition - 1")
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
        configvalues = readconfig.configvalues
        if((webElement==None or webElement== '') and configvalues['extn_enabled'].lower() == 'yes' and self.action=='debug' and isinstance(driver, webdriver.Chrome)):
            if not(simple_debug_gwto) and (int(configvalues['globalWaitTimeOut']))>0:
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
                if (typemap[tagname]!=new_ele_type):
                    flag=False
                if(flag==False):
                    o = pause_display_operation.PauseAndDisplay()
                    inputs1={'custtype':typemap[tagname],'newtype':new_ele_type}
                    o.debug_error(inputs1,self.wxObject,self.thread)
                ele='//*'
                a=[]
                combo=''
                for k,v in list(attributes.items()):
                    if k in ['id','class','name','type']:
                        ele=ele+'[@'+k+'="'+v+'"]'
                        a.append('[@'+k+'="'+v+'"]')
                tempwebElement=driver.find_elements_by_xpath(ele)
                if(len(tempwebElement)==1):
                    webElement=tempwebElement
                    identifiers[0]=ele
                    obj_flag=ele
                    local_Wd.log.debug('Element has been Captured with all properties')
                for i in range(len(a),1,-1):
                    comb=combinations(a,i)
                    for j in list(comb):
                        combo="//*"+"".join(j)
                        tempwebElement=driver.find_elements_by_xpath(combo)
                        if(len(tempwebElement)==1):
                            webElement=tempwebElement
                            identifiers[0]=combo
                            obj_flag=combo
                            local_Wd.log.debug('Element has been Captured using some properties')
                            break
                    else:
                        continue
                    break
                if(webElement==None):
                    logger.print_on_console("Webelement not found through extension")
            except Exception as e:
                local_Wd.log.debug(e)
        if isinstance(webElement,list):
            webElement=webElement[0]
        return webElement
