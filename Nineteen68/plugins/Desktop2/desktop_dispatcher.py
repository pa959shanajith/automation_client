#-------------------------------------------------------------------------------
# Name:        desktop_dispatcher.py
# Purpose:
#
# Author:      rakesh.v,anas.ahmed
#
# Created:     23-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import button_link_keywords_desktop
import desktop_editable_text
import desktop_element_keywords
import desktop_launch_keywords
import desktop_util_keywords
import desktop_dropdown_keywords
import desktop_tab_control_keywords
import desktop_date_control_keywords
import screenshot_keywords
import logger
import desktop_constants
import radio_checkbox_keywords_desktop
import outlook
import constants
import logging
import readconfig
import desktop_custom_object
from pywinauto.application import Application

log = logging.getLogger('desktop_dispatcher.py')

class DesktopDispatcher:
    button_link_keywords_obj = button_link_keywords_desktop.ButtonLinkKeyword()
    editable_text_obj = desktop_editable_text.Text_Box()
    element_keywords_obj = desktop_element_keywords.ElementKeywords()
    launch_keywords_obj = desktop_launch_keywords.Launch_Keywords()
    util_keywords_obj = desktop_util_keywords.Util_Keywords()
    dropdown_keywords_obj=desktop_dropdown_keywords.Dropdown_Keywords()
    radio_checkbox_keywords_obj = radio_checkbox_keywords_desktop.Radio_Checkbox_keywords()
    tab_control_keywords_obj = desktop_tab_control_keywords.Tab_Control_Keywords()
    date_control_keywords_obj = desktop_date_control_keywords.DateControlKeywords()
    desktop_custom_object_obj =desktop_custom_object.CustomObjectHandler()
##    outook_obj=outlook.OutlookKeywords()

    def __init__(self):
        self.exception_flag=''
        self.action = None
        self.outook_obj=outlook.OutlookKeywords()

#-----------------------------------------------------------------for custom objects
    custom_dict = {
                    "clickelement":['radiobutton','checkbox','input','button','select'],
                    "doubleclick":['radiobutton','checkbox','input','button','select'],
                    "getelementtext":['radiobutton','checkbox','input','button','select'],
                    "getstatus":['radiobutton','checkbox'],
                    "gettext":['input'],
                    "rightclick":['button'],
                    "selectcheckbox":['checkbox'],
                    "selectradiobutton":['radiobutton'],
                    "setfocus" :['radiobutton','checkbox','input','button','select'],
                    "setsecuretext":['input'],
                    "selectvaluebyindex":['select'],
                    "selectvaluebytext":['select'],
                    "settext":['input'],
                    "unselectcheckbox":['checkbox'],
                    'verifyhidden' :['radiobutton','checkbox','input','button','select'],
                    'verifyvisible':['radiobutton','checkbox','input','button','select'],
                    "verifyelementtext":['radiobutton','checkbox','input','button','select'],
                    "verifyexists":['radiobutton','checkbox','input','button','select']
                  }

    get_ele_type={
                'radio': 'radiobutton',
                'checkbox':'checkbox',
                'dropdown':'select',
                'textbox':'input',
                'button':'button',
                }
#-----------------------------------------------------------------for custom objects

    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name.lower()
        url = teststepproperty.url
        err_msg=None
        result=[desktop_constants.TEST_RESULT_FAIL,desktop_constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
##        if objectname != '@Browser' or objectname != '@BrowserPopUp' or objectname != '@Custom':
#-----------------------------------------------------------------for custom objects
        try:
            if objectname==desktop_constants.CUSTOM and teststepproperty.custom_flag:
                ele_type=input[0].lower()
                if ele_type in self.get_ele_type:
                    ele_type=self.get_ele_type[ele_type]
                parent_xpath=teststepproperty.parent_xpath
                if (keyword in self.custom_dict and ele_type in self.custom_dict[keyword]):
                    try:
                        custom_desktop_element=self.desktop_custom_object_obj.getobjectforcustom(parent_xpath,ele_type,input[1])
                    except:
                        import traceback
                        traceback.print_exc()
                    if(custom_desktop_element != '' or None):
                        objectname = custom_desktop_element
                else:
                    logger.print_on_console("unmapped or non existant custom objects")
        except Exception as e:
            logger.print_on_console("error has occured from custom objects")
#-----------------------------------------------------------------for custom objects

        try:
            dict={ 'click': self.button_link_keywords_obj.click,
                    'press':self.button_link_keywords_obj.press,
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
                    'maximizewindow' : self.launch_keywords_obj.maximize_window,
                    'minimizewindow' : self.launch_keywords_obj.minimize_window,
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
                    'selecttabbyindex': self.tab_control_keywords_obj.selectTabByIndex,
                    'selecttabbytext' : self.tab_control_keywords_obj.selectTabByText,
                    'getselectedtab' : self.tab_control_keywords_obj.getSelectedTab,
                    'verifyselectedtab' : self.tab_control_keywords_obj.verifySelectedTab,
                    'getdate' : self.date_control_keywords_obj.getDate,
                    'setdate' : self.date_control_keywords_obj.setDate,
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
                        app_uia = desktop_launch_keywords.app_uia
                        ele = self.get_desktop_element(objectname,url,app_uia)
                    result= dict[keyword](ele,url,input,output)

                if not(desktop_constants.ELEMENT_FOUND) and self.exception_flag:
                    result=constants.TERMINATE
            else:
                err_msg=desktop_constants.INVALID_KEYWORD
                result=list(result)
                result[3]=err_msg
            configobj = readconfig.readConfig()
            configvalues = configobj.readJson()
            screen_shot_obj = screenshot_keywords.Screenshot()
            if self.action == constants.EXECUTE:
                result=list(result)
                if configvalues['screenShot_Flag'].lower() == 'fail':
                    if result[0].lower() == 'fail':
                        if keyword not in desktop_constants.APPLICATION_KEYWORDS:
                            file_path = screen_shot_obj.captureScreenshot()
                            result.append(file_path[2])
                elif configvalues['screenShot_Flag'].lower() == 'all':
                    if keyword not in desktop_constants.APPLICATION_KEYWORDS:
                        file_path = screen_shot_obj.captureScreenshot()
                        result.append(file_path[2])
        except TypeError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result=list(result)
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
            logger.print_on_console("Unable to get desktop elements because :",e)
        return ele



