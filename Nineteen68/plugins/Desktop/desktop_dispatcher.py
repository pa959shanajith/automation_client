#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     23-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import button_link_keywords_desktop
import editable_text
import element_keywords
import launch_keywords
import util_keywords
import dropdown_keywords
import Exceptions
import logger
import desktop_constants
import radio_checkbox_keywords_desktop

class DesktopDispatcher:
    button_link_keywords_obj = button_link_keywords_desktop.ButtonLinkKeyword()
    editable_text_obj = editable_text.Text_Box()
    element_keywords_obj = element_keywords.ElementKeywords()
    launch_keywords_obj = launch_keywords.Launch_Keywords()
    util_keywords_obj = util_keywords.Util_Keywords()
    dropdown_keywords_obj=dropdown_keywords.Dropdown_Keywords()
    radio_checkbox_keywords_obj = radio_checkbox_keywords_desktop.Radio_Checkbox_keywords()


    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name
        url = teststepproperty.url
##        if objectname != '@Browser' or objectname != '@BrowserPopUp' or objectname != '@Custom':


        try:
            dict={ 'click': self.button_link_keywords_obj.click,
                    'doubleClick' : self.button_link_keywords_obj.double_click,
                    'verifyButtonName' : self.button_link_keywords_obj.verify_button_name,
                    'getButtonName' : self.button_link_keywords_obj.get_button_name,
                    'rightClick' : self.button_link_keywords_obj.right_click,
                    'getLinkText' : self.button_link_keywords_obj.get_link_text,
                    'verifyLinkText' : self.button_link_keywords_obj.verify_link_text,
                    'setText' : self.editable_text_obj.set_text,
                    'setSecureText' : self.editable_text_obj.set_secure_text,
                    'getText' : self.editable_text_obj.get_text,
                    'clearText' : self.editable_text_obj.clear_text,
                    'verifyText' :  self.editable_text_obj.verify_text,
                    'verifyElementExists' : self.element_keywords_obj.verify_element_exists,
                    'verifyElementDoesNotExists' : self.element_keywords_obj.verify_element_doesNot_exists,
                    'clickElement' : self.element_keywords_obj.click_element,
                    'getElementText' : self.element_keywords_obj.get_element_text,
                    'verifyElementText' : self.element_keywords_obj.verify_element_text,
                    'launchApplication' : self.launch_keywords_obj.launch_application,
                    'getPageTitle' : self.launch_keywords_obj.getPageTitle,
                    'closeApplication' : self.launch_keywords_obj.closeApplication,
                    'verifyEnabled' : self.util_keywords_obj.verifyEnabled,
                    'verifyDisabled' : self.util_keywords_obj.verifyDisabled,
                    'verifyVisible' : self.util_keywords_obj.verifyVisible,
                    'verifyExists' : self.util_keywords_obj.verifyExists,
                    'verifyHidden' : self.util_keywords_obj.verifyHidden,
                    'verifyReadOnly' : self.util_keywords_obj.verifyReadOnly,
                    'setFocus' : self.util_keywords_obj.setFocus,
                    'selectValueByIndex': self.dropdown_keywords_obj.selectValueByIndex,
                    'selectValueByText': self.dropdown_keywords_obj.selectValueByText,
                    'getSelected': self.dropdown_keywords_obj.getSelected,
                    'verifySelected': self.dropdown_keywords_obj.verifySelected,
                    'getCount': self.dropdown_keywords_obj.getCount,
                    'verifyCount': self.dropdown_keywords_obj.verifyCount,
                    'verifyValuesExists': self.dropdown_keywords_obj.verifyValuesExists,
                    'verifyAllValues': self.dropdown_keywords_obj.verifyAllValues,
                    'getValueByIndex': self.dropdown_keywords_obj.getValueByIndex,
                    'getMultpleValuesByIndexs': self.dropdown_keywords_obj.getMultpleValuesByIndexs,
                    'selectAllValues': self.dropdown_keywords_obj.selectAllValues,
                    'deSelectAll': self.dropdown_keywords_obj.deSelectAll,
                    'selectMultpleValuesByIndexs': self.dropdown_keywords_obj.selectMultpleValuesByIndexs,
                    'selectMultpleValuesByText': self.dropdown_keywords_obj.selectMultpleValuesByText,
                    'selectRadiobutton' : self.radio_checkbox_keywords_obj.select_radiobutton,
                    'selectCheckbox' : self.radio_checkbox_keywords_obj.select_checkbox,
                    'unselectCheckbox' : self.radio_checkbox_keywords_obj.unselect_checkbox,
                    'getStatus' : self.radio_checkbox_keywords_obj.get_status

                }
            if keyword in dict.keys():
                if keyword=='launchApplication':
                    return dict[keyword](input,output)
                else:
                    self.launch_keywords_obj.verifyWindowTitle()
                    return dict[keyword](objectname,url,input,output)
            else:
                logger.log(desktop_constants.INVALID_KEYWORD)
        except Exception as e:
            print 'Exception at dispatcher'
            Exceptions.error(e)



