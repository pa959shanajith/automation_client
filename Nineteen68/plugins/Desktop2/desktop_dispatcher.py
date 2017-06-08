#-------------------------------------------------------------------------------
# Name:        desktop_dispatcher.py
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

import logger
import desktop_constants
import radio_checkbox_keywords_desktop
import outlook
import constants
import logging
import readconfig
from pywinauto.application import Application

log = logging.getLogger('desktop_dispatcher.py')

class DesktopDispatcher:
    button_link_keywords_obj = button_link_keywords_desktop.ButtonLinkKeyword()
    editable_text_obj = editable_text.Text_Box()
    element_keywords_obj = element_keywords.ElementKeywords()
    launch_keywords_obj = launch_keywords.Launch_Keywords()
    util_keywords_obj = util_keywords.Util_Keywords()
    dropdown_keywords_obj=dropdown_keywords.Dropdown_Keywords()
    radio_checkbox_keywords_obj = radio_checkbox_keywords_desktop.Radio_Checkbox_keywords()
##    outook_obj=outlook.OutlookKeywords()

    def __init__(self):
        self.exception_flag=''
        self.outook_obj=outlook.OutlookKeywords()



    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name
        url = teststepproperty.url
        err_msg=None
        result=[desktop_constants.TEST_RESULT_FAIL,desktop_constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
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
                    'findwindowandattach' : self.launch_keywords_obj.find_window_and_attach,
                    'selectmenu': self.launch_keywords_obj.select_menu,
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
            ele = None
            if keyword in dict.keys():
                if keyword=='launchapplication' or keyword=='findwindowandattach' or keyword=='selectmenu' or keyword in email_dict.keys() :
                    result= dict[keyword](input,output)
                else:
                    self.launch_keywords_obj.verifyWindowTitle()
                    if objectname != '':
                        app_uia = launch_keywords.app_uia
                        ele = self.get_desktop_element(objectname,url,app_uia)
                    result= dict[keyword](ele,url,input,output)

                if not(desktop_constants.ELEMENT_FOUND) and self.exception_flag:
                    result=constants.TERMINATE
            else:
                err_msg=desktop_constants.INVALID_KEYWORD
                result[3]=err_msg
            configobj = readconfig.readConfig()
            configvalues = configobj.readJson()
            if configvalues['screenShot_Flag'].lower() == 'fail':
                if result[0].lower() == 'fail':
                    if keyword not in desktop_constants.APPLICATION_KEYWORDS:
                        self.launch_keywords_obj.save_screeenshot()
            elif configvalues['screenShot_Flag'].lower() == 'all':
                if keyword not in desktop_constants.APPLICATION_KEYWORDS:
                    self.launch_keywords_obj.save_screeenshot()
        except TypeError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            import traceback
            traceback.print_exc()
            log.error(e)
            logger.print_on_console('Exception at dispatcher')
        if err_msg!=None:
            import traceback
            traceback.print_exc()
            log.error(err_msg)
            logger.print_on_console(err_msg)

        return result

    def get_desktop_element(self,xpath,url,app):
        #logic to find the desktop element using the xpath
        ele = ''
        try:
            win = app.top_window()
            ch = win.children()
            split_xpath = xpath.split('/')
            parent = split_xpath[0]
            index = parent[parent.index('[') + 1 : parent.index(']')]
            ele = ch[int(index)]
            for i in range(1,len(split_xpath)):
                child = split_xpath[i]
                index = child[child.index('[') + 1 : child.index(']')]
                ch = ele.children()
                ele = ch[int(index)]
        except Exception as e:
            print e
        return ele



