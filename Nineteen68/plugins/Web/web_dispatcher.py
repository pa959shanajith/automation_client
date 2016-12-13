#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      wasimakram.sutar
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
import Exceptions
import logger
import webconstants
import custom_keyword

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



    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name
        driver = browser_Keywords.driver_obj
        webelement = None
        element = None
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



        if driver != None:

            #check if the element is in iframe or frame
            url=teststepproperty.url.strip()
            if url !=  '' and self.custom_object.is_int(url):
                self.custom_object.switch_to_iframe(url,driver.current_window_handle)
                driver = browser_Keywords.driver_obj
            if objectname==webconstants.CUSTOM:
                reference_element=self.getwebelement(driver,teststepproperty.parent_xpath)
                if reference_element != None:
                    reference_element = reference_element[0]
                    if len(input)>=3:
                        if (keyword in custom_dict and input[0].lower() in custom_dict[keyword]) or keyword in custom_dict_element.values()[0]:
                            webelement=self.custom_object.getCustomobject(reference_element,input[0],input[1],input[2],teststepproperty.url)
                            input.reverse()
                            for x in range(0,3):
                                input.pop()
                        else:
                            logger.log('Keyword and Type Mismatch')
                    else:
                        logger.log('Insufficient Input to find custom object')
                        logger.log('Custom object not found')
                else:
                    logger.log('Reference Element is null')
                    logger.log('Custom object not found')

            else:
                webelement = self.getwebelement(driver,objectname)
                if webelement != None:
                    webelement = webelement[0]
                    logger.log('WebElement is found')






        try:
            dict={ 'click': self.button_link_object.click,
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
                  'clearCache':self.browser_object.clear_cache
                }
            if keyword in dict.keys():
                if keyword.lower()=='waitforelementvisible':
                    identifiers = objectname.split(';')
                    input=identifiers[0]
                return dict[keyword](webelement,input,output)
            else:
                logger.log(webconstants.METHOD_INVALID)
        except Exception as e:
            print 'Exception at dispatcher'
            Exceptions.error(e)

    def getwebelement(self,driver,objectname):
        objectname = str(objectname)
        webElement = None
        if objectname.strip() != '':
            identifiers = objectname.split(';')

            try:
                #find by rxpath
                tempwebElement = driver.find_elements_by_xpath(identifiers[0])
                if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                    tempwebElement = driver.find_elements_by_id(identifiers[1])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = None
                webElement = tempwebElement

            except Exception as webEx:
                try:
                    #find by id
                    tempwebElement = driver.find_elements_by_id(identifiers[1])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = None
                    webElement = tempwebElement
                except Exception as webEx:
                    try:
                        tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = None
                        webElement = tempwebElement
                    except Exception as webEx:
                        logger.log('WebElement is not found')
        return webElement

