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
import outlook
import constants

class DesktopDispatcher:
    button_link_keywords_obj = button_link_keywords_desktop.ButtonLinkKeyword()
    editable_text_obj = editable_text.Text_Box()
    element_keywords_obj = element_keywords.ElementKeywords()
    launch_keywords_obj = launch_keywords.Launch_Keywords()
    util_keywords_obj = util_keywords.Util_Keywords()
    dropdown_keywords_obj=dropdown_keywords.Dropdown_Keywords()
    radio_checkbox_keywords_obj = radio_checkbox_keywords_desktop.Radio_Checkbox_keywords()
    outook_obj=outlook.OutlookKeywords()



    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name
        url = teststepproperty.url
        result=(desktop_constants.TEST_RESULT_FAIL,desktop_constants.TEST_RESULT_FALSE)
##        if objectname != '@Browser' or objectname != '@BrowserPopUp' or objectname != '@Custom':


        try:
            dict={ 'click': self.button_link_keywords_obj.click,
                    'doubleclick' : self.button_link_keywords_obj.double_click,
                    'verifybuttonname' : self.button_link_keywords_obj.verify_button_name,
                    'getbuttonname' : self.button_link_keywords_obj.get_button_name,
                    'rightclick' : self.button_link_keywords_obj.right_click,
                    'getlinktext' : self.button_link_keywords_obj.get_link_text,
                    'verifylinktext' : self.button_link_keywords_obj.verify_link_text,
                    'settext' : self.editable_text_obj.set_text,
                    'setsecuretext' : self.editable_text_obj.set_secure_text,
                    'gettext' : self.editable_text_obj.get_text,
                    'cleartext' : self.editable_text_obj.clear_text,
                    'verifytext' :  self.editable_text_obj.verify_text,
                    'verifyelementexists' : self.element_keywords_obj.verify_element_exists,
                    'verifyelementdoesnotexists' : self.element_keywords_obj.verify_element_doesNot_exists,
                    'clickelement' : self.element_keywords_obj.click_element,
                    'getelementtext' : self.element_keywords_obj.get_element_text,
                    'verifyelementtext' : self.element_keywords_obj.verify_element_text,
                    'launchapplication' : self.launch_keywords_obj.launch_application,
                    'getpagetitle' : self.launch_keywords_obj.getPageTitle,
                    'closeapplication' : self.launch_keywords_obj.closeApplication,
                    'verifyenabled' : self.util_keywords_obj.verifyEnabled,
                    'verifydisabled' : self.util_keywords_obj.verifyDisabled,
                    'verifyvisible' : self.util_keywords_obj.verifyVisible,
                    'verifyexists' : self.util_keywords_obj.verifyExists,
                    'verifyhidden' : self.util_keywords_obj.verifyHidden,
                    'verifyreadonly' : self.util_keywords_obj.verifyReadOnly,
                    'setfocus' : self.util_keywords_obj.setFocus,
                    'selectvaluebyindex': self.dropdown_keywords_obj.selectValueByIndex,
                    'selectvaluebytext': self.dropdown_keywords_obj.selectValueByText,
                    'getselected': self.dropdown_keywords_obj.getSelected,
                    'verifyselectedvalue': self.dropdown_keywords_obj.verifySelected,
                    'getcount': self.dropdown_keywords_obj.getCount,
                    'verifycount': self.dropdown_keywords_obj.verifyCount,
                    'verifyvaluesexists': self.dropdown_keywords_obj.verifyValuesExists,
                    'verifyallvalues': self.dropdown_keywords_obj.verifyAllValues,
                    'getvaluebyindex': self.dropdown_keywords_obj.getValueByIndex,
                    'getmultiplevaluesbyindexes': self.dropdown_keywords_obj.getMultpleValuesByIndexs,
                    'selectallvalues': self.dropdown_keywords_obj.selectAllValues,
                    'deselectall': self.dropdown_keywords_obj.deSelectAll,
                    'selectmultiplevaluesbyindexes': self.dropdown_keywords_obj.selectMultpleValuesByIndexs,
                    'selectmultiplevaluesbytext': self.dropdown_keywords_obj.selectMultpleValuesByText,
                    'selectradiobutton' : self.radio_checkbox_keywords_obj.select_radiobutton,
                    'selectcheckbox' : self.radio_checkbox_keywords_obj.select_checkbox,
                    'unselectcheckbox' : self.radio_checkbox_keywords_obj.unselect_checkbox,
                    'getstatus' : self.radio_checkbox_keywords_obj.get_status,
                    'getemail': self.outook_obj.GetEmail,
                    'getfrommailid' : self.outook_obj.GetFromMailId,
                    'getattachmentstatus'    : self.outook_obj.GetAttachmentStatus,
                    'getsubject'     : self.outook_obj.GetSubject,
                    'gettomailid'  : self.outook_obj.GetToMailID,
                    'getbody' : self.outook_obj.GetBody,
                    'verifyemail' : self.outook_obj.VerifyEmail,
                    'switchtofolder':self.outook_obj.switchToFolder

                }

            email_dict={'getemail': 1,
                  'getfrommailid' : 2,
                  'getattachmentstatus'    : 3,
                  'getsubject'     : 4,
                  'gettomailid'  : 5,
                  'getbody' : 6,
                  'verifyemail' : 7,
                  'switchtofolder':8
                }
            keyword=keyword.lower()
            if keyword in dict.keys():
                if keyword=='launchapplication' or keyword in email_dict.keys() :
                    result= dict[keyword](input,output)
                else:
                    self.launch_keywords_obj.verifyWindowTitle()
                    result= dict[keyword](objectname,url,input,output)

                if not(desktop_constants.ELEMENT_FOUND):
                    result=constants.TERMINATE
            else:
                logger.log(desktop_constants.INVALID_KEYWORD)
        except Exception as e:
            print 'Exception at dispatcher'
            Exceptions.error(e)

        return result



