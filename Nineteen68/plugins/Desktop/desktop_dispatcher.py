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
import desktop_treeview_keywords
import desktop_table_keywords
import screenshot_keywords
import json
import logger
import desktop_constants
import radio_checkbox_keywords_desktop
import outlook
import constants
import logging
import readconfig
import desktop_custom_object
from pywinauto.application import Application
import pywinauto
from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow
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
    tree_keywords_obj=desktop_treeview_keywords.Tree_View_Keywords()
    table_keywords_obj=desktop_table_keywords.Table_Keywords()
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
                    "verifyexists":['radiobutton','checkbox','input','button','select'],
                    "mousehover":['radiobutton','checkbox','input','button'],
                    "verifyallvalues":['select']
                  }

    get_ele_type={
                'radio': 'radiobutton',
                'checkbox':'checkbox',
                'dropdown':'select',
                'textbox':'input',
                'button':'button',
                }
#-----------------------------------------------------------------for custom objects

    def dispatcher(self,teststepproperty,input,iris_flag):
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
                backendType='A'
                ele_type=input[0].lower()
                if ele_type in self.get_ele_type:
                    ele_type=self.get_ele_type[ele_type]
                try:
                    if len(input)==3:
                        input.append(backendType)
                    elif len(input)>=3:
                        if input[3]=='B':
                            backendType='B'
                except:
                    import traceback
                    traceback.print_exc()
                parent_xpath=teststepproperty.parent_xpath
                if (keyword in self.custom_dict and ele_type in self.custom_dict[keyword]):
                    try:
                        custom_desktop_element=self.desktop_custom_object_obj.getobjectforcustom(parent_xpath,ele_type,input[1],backendType)
                    except:
                        pass
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
                    'mousehover':self.element_keywords_obj.mouseHover,
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
                    'switchtofolder':self.outook_obj.switchToFolder,
                    'settomailid':self.outook_obj.send_to_mail,
                    'setcc':self.outook_obj.send_CC,
                    'setbcc':self.outook_obj.send_BCC,
                    'setsubject':self.outook_obj.send_subject,
                    'setbody':self.outook_obj.send_body,
                    'setattachments':self.outook_obj.send_attachments,
                    'sendemail':self.outook_obj.send_mail,
##                    'getnodecount':self.tree_keywords_obj.get_item_count,
##                    'verifynodecount':self.tree_keywords_obj.verify_item_count,
##                    'expandall':self.tree_keywords_obj.expand_all,
##                    'collapseall':self.tree_keywords_obj.collapse_all,
##                    'getchildren':self.tree_keywords_obj.get_children,
##                    'verifychildren':self.tree_keywords_obj.verify_children,
##                    'getrootnodes':self.tree_keywords_obj.get_root_elements,
##                    'selecttreeelement':self.tree_keywords_obj.select_element,
                    'selecttreenode':self.tree_keywords_obj.click_tree_element,
##                    'doubleclicktreenode':self.tree_keywords_obj.double_click_tree_element,
                    'getnodenamebyindex':self.tree_keywords_obj.getElementTextByIndex,
                    'getcellvalue':self.table_keywords_obj.get_cell_value,
                    'getcolcount':self.table_keywords_obj.get_col_count,
                    'getcolnumbytext':self.table_keywords_obj.get_col_num_by_text,
                    'getrowcount':self.table_keywords_obj.get_row_count,
                    'getrownumbytext':self.table_keywords_obj.get_row_num_by_text,
                    'selectrow':self.table_keywords_obj.select_row,
                    'clickcell':self.table_keywords_obj.click_cell,
                    'doubleclickcell':self.table_keywords_obj.double_click_cell,
                    'vaerifycellvalue':self.table_keywords_obj.verify_cell_value
                }
            if(iris_flag):
                import iris_operations
                iris_object = iris_operations.IRISKeywords()
                dict['clickiris'] = iris_object.clickiris
                dict['settextiris'] = iris_object.settextiris
                dict['gettextiris'] = iris_object.gettextiris
                dict['getrowcountiris'] = iris_object.getrowcountiris
                dict['getcolcountiris'] = iris_object.getcolcountiris
                dict['getcellvalueiris'] = iris_object.getcellvalueiris
                dict['verifyexistsiris'] = iris_object.verifyexistsiris
                dict['verifytextiris'] = iris_object.verifytextiris

            email_dict={'getemail': 1,
                  'getfrommailid' : 2,
                  'getattachmentstatus'    : 3,
                  'getsubject'     : 4,
                  'gettomailid'  : 5,
                  'getbody' : 6,
                  'verifyemail' : 7,
                  'switchtofolder':8,
                  'settomailid' : 9,
                  'setcc'    : 10,
                  'setbcc'     :11,
                  'setsubject'  : 12,
                  'setbody' : 13,
                  'setattachments' : 14,
                  'sendemail':15
                }
            keyword=keyword.lower()
            ele = None
            if keyword in list(dict.keys()):
                if keyword=='launchapplication' or keyword=='findwindowandattach' or keyword=='selectmenu' or keyword in list(email_dict.keys()) :
                    result= dict[keyword](input,output)
                else:
                    self.launch_keywords_obj.verifyWindowTitle()
                    if objectname != '' and teststepproperty.cord != None and teststepproperty.cord != '':
                        if(desktop_launch_keywords.window_name != None):
                            SetForegroundWindow(find_window(title=self.launch_keywords_obj.windowname))
                        obj_props = teststepproperty.objectname.split(';')
                        coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                        ele = {'cord': teststepproperty.cord, 'coordinates': coord}
                        if(teststepproperty.custom_flag):
                            result = dict[keyword](ele,input,output,teststepproperty.parent_xpath)
                        else:
                            result= dict[keyword](ele,input,output)
                    else:
                        if objectname != '':
                            ele = self.get_desktop_element(objectname,url)
                        result= dict[keyword](ele,url,input,output)

                if not(desktop_constants.ELEMENT_FOUND) and self.exception_flag:
                    result=constants.TERMINATE
            else:
                err_msg=desktop_constants.INVALID_KEYWORD
                result=list(result)
                result[3]=err_msg
            configvalues = readconfig.configvalues
            screen_shot_obj = screenshot_keywords.Screenshot()
            if self.action == constants.EXECUTE:
                if result !=constants.TERMINATE:
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
            log.error(e)
            #logger.print_on_console('Exception at dispatcher')
        if err_msg!=None:
            import traceback
            traceback.print_exc()
            log.error(err_msg)
            logger.print_on_console(err_msg)

        return result

    def get_desktop_element(self,xPath,url):
        index=None
        ele = ''
        backend='A'
        prev_flag=False
        if ";" in xPath:
            x_var=xPath.split(';')
            xpath=x_var[0]
            xclass=x_var[1]
            try:
                xconID=int(x_var[2])
            except:
                pass #as uia element sometimes has no conID
            if len(x_var)==4:
                xname=x_var[3]
            if len(x_var)==5:
                """checking for backend process"""
                xname=x_var[3]
                backend=x_var[4].strip()
        else:
            xpath=xPath
            prev_flag=True # setting prev_flag to True since the xpath recieved is of an old test case.
        #logic to find the desktop element using the xpath
        if backend=='A':
            app = desktop_launch_keywords.app_win32
            app2=app
            try:
                win = app.top_window()
                ch = win.children()
                split_xpath = xpath.split('/')
                parent = split_xpath[0]
                index = int(parent[parent.index('[') + 1 : parent.index(']')])
                ele = ch[int(index)]
                for i in range(1,len(split_xpath)):
                    child = split_xpath[i]
                    index = child[child.index('[') + 1 : child.index(']')]
                    ch = ele.children()
                    ele = ch[int(index)]
                #---------------------------------------------------
                try:
                    if ele!='':     #checking if element is not empty
                        if xclass==ele.friendly_class_name(): #comparing top window element class with the one obtained from TSP
                            if ele.friendly_class_name()=='TabControl':
                                if xconID!=ele.control_id(): #comparing if the control ID of top window element is same as one from TSP
                                    #-------element dosent handles matched
                                    ele=''
                            else:
                                #-------------------------------------getting text and comparing with xname
                                handle= ele.handle
                                try:
                                    element_text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                                except:
                                    pass
                                if element_text!='':
                                    try:
                                        comp_text=str(element_text)
                                    except:
                                        comp_text=element_text.encode('ascii', 'replace')
                                else :
                                    comp_text=ele.texts()
                                try:
                                    comp_text=comp_text.strip()
                                except:
                                    comp_text=comp_text[0].strip()
                                #----------------------------------------------------------------------------------
                                if xname!=comp_text:
                                    ele=''
                        else:
                            #print "friendly class name does not match",ele.friendly_class_name()
                            ele=''
                except Exception as e:
                    if prev_flag==False:#checking if previous test case flag is True or not.
                        ele=''  #If false then new test case and AUT structure has changed, so setting the ele to ''
                #---------------------------------------------------
            except :
                #logger.print_on_console("Unable to get desktop elements because :")
                import traceback
                traceback.print_exc()
            if ele=='':
                #logger.print_on_console("Warning! AUT Structure has changed")
                try:
                    ele=self.get_element_if_empty(xclass,xname,app2)
                except:# only for tables
                    ele=self.get_desktop_static_element(xclass,xconID,app)
            if ele=='':#last attempt if the element is still empty, then find element using original index
                try:
                    ele = ch[int(index)]
                except Exception as e:
                    log.error(e)
                    import traceback
                    traceback.print_exc()
                    logger.print_on_console("Unable to get desktop element because :")
                    logger.print_on_console(e)
        elif backend =='B':
            try:
                import pythoncom
                pythoncom.CoInitialize()
                win = desktop_launch_keywords.app_uia.top_window()
                ch=win.children()[:]
                for i in range(0,len(ch)):
                    if len(ch[i].children()):
                        c=ch[i].children()
                        for a in c:
                            ch.append(a)
                split_xpath = xpath.split('/')
                parent = split_xpath[0]
                index = int(parent[parent.index('[') + 1 : parent.index(']')])
                ele = ch[int(index)]
                for i in range(1,len(split_xpath)):
                    child = split_xpath[i]
                    index = child[child.index('[') + 1 : child.index(']')]
                    ch = ele.children()
                    ele = ch[int(index)]
            except Exception as e:
                log.error(e)
                import traceback
                traceback.print_exc()
                logger.print_on_console("Unable to get desktop element because :")
                logger.print_on_console(e)
        return ele

    def get_desktop_static_element(self,xclass,xconID,app):
        """This method was added to handle change in tabs, when different tabs are selected, the xpath of all elements will change
        This will result in increment or decrement of objects also!. Hence using this method to comapre the calss name and control ID of object
        returned from UI with all the elements of the top window. The first object whoes class name and control ID is the same is returned."""
        #logic to find the desktop element using custname of the element returned from UI
        ele = ''
        try:
            win1 = app.top_window()
            ch1 = win1.children()
            for i in range(0,len(ch1)):
                try:
                    conID = ch1[i].control_id()
                    className=ch1[i].friendly_class_name()
                    if xclass==className:
                        if xconID==conID:
                            ele=ch1[i]
                except:
                    import traceback
                    traceback.print_exc()
        except :
            import traceback
            traceback.print_exc()
        return ele
    def get_element_if_empty(self,xclass,xname,app):
        """This method was added as a check, The name of the element is passed as an argument,it
        comes to this method only when the friendly class name does not match"""
        #logic to find the desktop element using custname of the element returned from UI
        import pythoncom
        pythoncom.CoInitialize()
        ele = ''
        className=''
        comp_text=''
        element_text=''
        try:
            win2 = app.top_window()
            ch2 = win2.children()
            for i in range(0,len(ch2)):
                try:
                    #------------------------------------------------
                    handle= ch2[i].handle
                    try:
                        element_text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                    except:
                        pass
                    if element_text!='':
                                try:
                                    comp_text=str(element_text)
                                except:
                                    comp_text=element_text.encode('ascii', 'replace')
                    else :
                        comp_text=ch2[i].texts()
                    #------------------------------------------------
                    className=ch2[i].friendly_class_name()
                    try:
                        comp_text=comp_text.strip()
                    except:
                        comp_text=comp_text[0].strip()
                    if xclass==className:
                        if xname==comp_text:
                            ele=ch2[i]
                            break
                except:
                    import traceback
                    traceback.print_exc()
        except :
            import traceback
            traceback.print_exc()
        return ele