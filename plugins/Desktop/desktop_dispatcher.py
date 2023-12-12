#-------------------------------------------------------------------------------
# Name:        desktop_dispatcher.py
# Purpose:     Dispatcher acts like a terminal for the flow of input/output.
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
import iris_operations_ai
log = logging.getLogger( 'desktop_dispatcher.py' )

class DesktopDispatcher:
    button_link_keywords_obj = button_link_keywords_desktop.ButtonLinkKeyword()
    editable_text_obj = desktop_editable_text.Text_Box()
    element_keywords_obj = desktop_element_keywords.ElementKeywords()
    launch_keywords_obj = desktop_launch_keywords.Launch_Keywords()
    util_keywords_obj = desktop_util_keywords.Util_Keywords()
    dropdown_keywords_obj = desktop_dropdown_keywords.Dropdown_Keywords()
    radio_checkbox_keywords_obj = radio_checkbox_keywords_desktop.Radio_Checkbox_keywords()
    tab_control_keywords_obj = desktop_tab_control_keywords.Tab_Control_Keywords()
    date_control_keywords_obj = desktop_date_control_keywords.DateControlKeywords()
    desktop_custom_object_obj = desktop_custom_object.CustomObjectHandler()
    tree_keywords_obj = desktop_treeview_keywords.Tree_View_Keywords()
    table_keywords_obj = desktop_table_keywords.Table_Keywords()
    outook_obj = outlook.OutlookKeywords()
    iris_object = iris_operations_ai.IRISKeywords()

    desktop_dict = { 'click': button_link_keywords_obj.click,
        'press' : button_link_keywords_obj.press,
        'doubleclick' : button_link_keywords_obj.double_click,
        'verifybuttonname' : button_link_keywords_obj.verify_button_name,
        'getbuttonname' : button_link_keywords_obj.get_button_name,
        'rightclick' : button_link_keywords_obj.right_click,
        'settext' : editable_text_obj.set_text,
        'setsecuretext' : editable_text_obj.set_secure_text,
        'gettext' : editable_text_obj.get_text,
        'cleartext' : editable_text_obj.clear_text,
        'verifytext' :  editable_text_obj.verify_text,
        'sendsecurefunctionkeys' :  editable_text_obj.sendsecurefunction_keys,
        'verifyelementexists' : element_keywords_obj.verify_element_exists,
        'verifyelementdoesnotexists' : element_keywords_obj.verify_element_doesNot_exists,
        'clickelement' : element_keywords_obj.click_element,
        'getelementtext' : element_keywords_obj.get_element_text,
        'verifyelementtext' : element_keywords_obj.verify_element_text,
        'mousehover' : element_keywords_obj.mouseHover,
        'getelementcolor' : element_keywords_obj.get_element_color,
        'drag' : element_keywords_obj.drag,
        'drop' : element_keywords_obj.drop,
        'launchapplication' : launch_keywords_obj.launch_application,
        'findwindowandattach' : launch_keywords_obj.find_window_and_attach,
        'selectmenu': launch_keywords_obj.select_menu,
        'maximizewindow' : launch_keywords_obj.maximize_window,
        'minimizewindow' : launch_keywords_obj.minimize_window,
        'getpagetitle' : launch_keywords_obj.getPageTitle,
        'closeapplication' : launch_keywords_obj.closeApplication,
        'verifyenabled' : util_keywords_obj.verifyEnabled,
        'verifydisabled' : util_keywords_obj.verifyDisabled,
        'verifyvisible' : util_keywords_obj.verifyVisible,
        'verifyexists' : util_keywords_obj.verifyExists,
        'verifyhidden' : util_keywords_obj.verifyHidden,
        'verifyreadonly' : util_keywords_obj.verifyReadOnly,
        'setfocus' : util_keywords_obj.setFocus,
        'selectvaluebyindex': dropdown_keywords_obj.selectValueByIndex,
        'selectvaluebytext': dropdown_keywords_obj.selectValueByText,
        'getselected': dropdown_keywords_obj.getSelected,
        'verifyselectedvalue': dropdown_keywords_obj.verifySelected,
        'getcount': dropdown_keywords_obj.getCount,
        'verifycount': dropdown_keywords_obj.verifyCount,
        'verifyvaluesexists' : dropdown_keywords_obj.verifyValuesExists,
        'verifyallvalues' : dropdown_keywords_obj.verifyAllValues,
        'getvaluebyindex' : dropdown_keywords_obj.getValueByIndex,
        'getmultiplevaluesbyindexes' : dropdown_keywords_obj.getMultpleValuesByIndexs,
        'selectallvalues' : dropdown_keywords_obj.selectAllValues,
        'deselectall' : dropdown_keywords_obj.deSelectAll,
        'selectmultiplevaluesbyindexes' : dropdown_keywords_obj.selectMultpleValuesByIndexs,
        'selectmultiplevaluesbytext' : dropdown_keywords_obj.selectMultpleValuesByText,
        'selectradiobutton' : radio_checkbox_keywords_obj.select_radiobutton,
        'selectcheckbox' : radio_checkbox_keywords_obj.select_checkbox,

        #author : priyanka.r
        #added mapping of 'getAllValues' to dropdown list object
        'getallvalues':dropdown_keywords_obj.getAllValues,

        'unselectcheckbox' : radio_checkbox_keywords_obj.unselect_checkbox,
        'getstatus' : radio_checkbox_keywords_obj.get_status,
        'selecttabbyindex' : tab_control_keywords_obj.selectTabByIndex,
        'selecttabbytext' : tab_control_keywords_obj.selectTabByText,
        'getselectedtab' : tab_control_keywords_obj.getSelectedTab,
        'verifyselectedtab' : tab_control_keywords_obj.verifySelectedTab,
        'getdate' : date_control_keywords_obj.getDate,
        'setdate' : date_control_keywords_obj.setDate,
        'selecttreenode' : tree_keywords_obj.click_tree_element,
        'getnodenamebyindex' : tree_keywords_obj.getElementTextByIndex,
        'getcellvalue' : table_keywords_obj.get_cell_value,
        'getcolcount' : table_keywords_obj.get_col_count,
        'getcolnumbytext':table_keywords_obj.get_col_num_by_text,
        'getrowcount' : table_keywords_obj.get_row_count,
        'getrownumbytext':table_keywords_obj.get_row_num_by_text,
        'selectrow' : table_keywords_obj.select_row,
        'clickcell' : table_keywords_obj.click_cell,
        'doubleclickcell' : table_keywords_obj.double_click_cell,
        'verifycellvalue' : table_keywords_obj.verify_cell_value,
        'getemail' : outook_obj.GetEmail,
        'getfrommailid' : outook_obj.GetFromMailId,
        'getattachmentstatus' : outook_obj.GetAttachmentStatus,
        'getsubject' : outook_obj.GetSubject,
        'gettomailid' : outook_obj.GetToMailID,
        'getbody' : outook_obj.GetBody,
        'verifyemail' : outook_obj.VerifyEmail,
        'switchtofolder' : outook_obj.switchToFolder,
        'settomailid' : outook_obj.send_to_mail,
        'setcc' : outook_obj.send_CC,
        'setbcc' : outook_obj.send_BCC,
        'setsubject' : outook_obj.send_subject,
        'setbody' : outook_obj.send_body,
        'setattachments' : outook_obj.send_attachments,
        'sendemail' : outook_obj.send_mail,
        'verifyattachmentcontent' : outook_obj.verify_attachment_content,
        'clickiris' : iris_object.clickiris,
        'doubleclickiris' : iris_object.doubleclickiris,
        'rightclickiris' : iris_object.rightclickiris,
        'settextiris' : iris_object.settextiris,
        'setsecuretextiris' : iris_object.setsecuretextiris,
        'gettextiris' : iris_object.gettextiris,
        'getrowcountiris' : iris_object.getrowcountiris,
        'getcolcountiris' : iris_object.getcolcountiris,
        'getcellvalueiris' : iris_object.getcellvalueiris,
        'verifyexistsiris' : iris_object.verifyexistsiris,
        'verifytextiris' : iris_object.verifytextiris,
        'cleartextiris' : iris_object.cleartextiris,
        'dragiris' : iris_object.dragiris,
        'dropiris' : iris_object.dropiris,
        'mousehoveriris' : iris_object.mousehoveriris,
        'setcellvalueiris' : iris_object.setcellvalueiris,
        'verifycellvalueiris' : iris_object.verifycellvalueiris,
        'clickcelliris' : iris_object.clickcelliris,
        'doubleclickcelliris' : iris_object.doubleclickcelliris,
        'rightclickcelliris' : iris_object.rightclickcelliris,
        'mousehovercelliris' : iris_object.mousehovercelliris,
        'getstatusiris' : iris_object.getstatusiris,
        'scrollupiris':iris_object.scrollupiris,
        'scrolldowniris':iris_object.scrolldowniris,
        'scrollleftiris':iris_object.scrollleftiris,
        'scrollrightiris':iris_object.scrollrightiris
    }


    email_dict = {'getemail' : 1,
          'getfrommailid' : 2,
          'getattachmentstatus' : 3,
          'getsubject' : 4,
          'gettomailid'  : 5,
          'getbody' : 6,
          'verifyemail' : 7,
          'switchtofolder' : 8,
          'settomailid' : 9,
          'setcc' : 10,
          'setbcc' : 11,
          'setsubject' : 12,
          'setbody' : 13,
          'setattachments' : 14,
          'sendemail' : 15,
          'verifyattachmentcontent': 16
    }

    # For custom objects
    custom_dict = {
        "clickelement" : ['radiobutton', 'checkbox', 'input', 'button', 'select'],
        "doubleclick" : ['radiobutton', 'checkbox', 'input', 'button', 'select'],
        "getelementtext" : ['radiobutton', 'checkbox', 'input', 'button', 'select'],
        "getstatus" : ['radiobutton', 'checkbox'],
        "gettext" : ['input'],
        "rightclick" : ['button'],
        "selectcheckbox" : ['checkbox'],
        "selectradiobutton" : ['radiobutton'],
        "setfocus" : ['radiobutton', 'checkbox', 'input', 'button', 'select'],
        "setsecuretext" : ['input'],
        "selectvaluebyindex" : ['select'],
        "selectvaluebytext" : ['select'],
        "settext" : ['input'],
        "unselectcheckbox" : ['checkbox'],
        'verifyhidden' : ['radiobutton', 'checkbox', 'input', 'button', 'select'],
        'verifyvisible': ['radiobutton', 'checkbox', 'input', 'button', 'select'],
        "verifyelementtext" : ['radiobutton', 'checkbox', 'input', 'button', 'select'],
        "verifyexists" : ['radiobutton', 'checkbox', 'input', 'button', 'select'],
        "mousehover" : ['radiobutton', 'checkbox', 'input', 'button'],
        "verifyallvalues" : ['select'],
        "getallvalues" : ['select','list'],
        "selecttreenode" : ['tree'],
        "getnodenamebyindex" : ['tree'],
        "sendsecurefunctionkeys" : ['input']
    }

    get_ele_type = {
        'radio' : 'radiobutton',
        'checkbox' : 'checkbox',
        'dropdown' : 'select',
        'textbox' : 'input',
        'button' : 'button',
        'list' : 'list',
        'tree' : 'tree'
    }


    def __init__(self):
        self.exception_flag = ''
        self.action = None

    def dispatcher(self,teststepproperty, input, mythread):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name.lower()
        url = teststepproperty.url
        err_msg = None
        result = [desktop_constants.TEST_RESULT_FAIL, desktop_constants.TEST_RESULT_FALSE, constants.OUTPUT_CONSTANT, err_msg]

        try:
            if ( objectname == desktop_constants.CUSTOM and teststepproperty.custom_flag ):
                ele_type = input[0].lower()
                if ( ele_type in self.get_ele_type ):
                    ele_type=self.get_ele_type[ele_type]
                parent_xpath=teststepproperty.parent_xpath
                if ( keyword in self.custom_dict and ele_type in self.custom_dict[keyword] ):
                    custom_desktop_element = self.desktop_custom_object_obj.getobjectforcustom(parent_xpath, ele_type, input[2])
                    if ( custom_desktop_element != '' or None ):
                        objectname = custom_desktop_element
                else:
                    logger.print_on_console( "Unmapped or non existant custom objects" )
                    log.error( "Unmapped or non existant custom objects" )
        except Exception as e:
            logger.print_on_console( "Error has occured in custom objects" )
            log.error( "Error has occured in custom objects" )
#-----------------------------------------------------------------for custom objects

        try:

            keyword = keyword.lower()
            ele = None
            if ( keyword in list(self.desktop_dict.keys()) ):
                if ( keyword == 'launchapplication' or keyword == 'findwindowandattach' or keyword == 'selectmenu' or keyword in list(self.email_dict.keys()) ):
                    result = self.desktop_dict[keyword](input,output)
                else:
                    self.launch_keywords_obj.verifyWindowTitle()
                    if ( objectname != '' and teststepproperty.cord != None and teststepproperty.cord != '' ):
                        if( desktop_launch_keywords.window_name != None ):
                            SetForegroundWindow(find_window(title=self.launch_keywords_obj.windowname))
                        obj_props = teststepproperty.objectname.split(';')
                        coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                        ele = {'cord': teststepproperty.cord, 'coordinates': coord}
                        if ( teststepproperty.custom_flag ):
                            if (keyword.lower() == 'getstatusiris') : result = self.desktop_dict[keyword](ele, input, output, teststepproperty.parent_xpath, teststepproperty.objectname.split(';')[-2])
                            else : result = self.desktop_dict[keyword](ele, input, output, teststepproperty.parent_xpath)
                        elif ( teststepproperty.objectname.split(';')[-1] == 'constant' and keyword.lower() == 'verifyexistsiris' ):
                            result = self.desktop_dict[keyword](ele, input, output, 'constant')
                        else:
                            if (keyword.lower() == 'getstatusiris') : result = self.desktop_dict[keyword](ele, input, output, teststepproperty.objectname.split(';')[-2])
                            else : result = self.desktop_dict[keyword](ele, input, output)
                    else:
                        if ( objectname != '' ):
                            ele = self.get_desktop_element(objectname, url)
                        result = self.desktop_dict[keyword](ele, url, input, output)

                if ( not(desktop_constants.ELEMENT_FOUND) and self.exception_flag ):
                    result = constants.TERMINATE
            else:
                err_msg = desktop_constants.INVALID_KEYWORD
                result = list(result)
                result[3] = err_msg
            configvalues = readconfig.configvalues
            screen_shot_obj = screenshot_keywords.Screenshot()
            #------------------------------------------return null for get-keywords if keyword fails
            if ( keyword in desktop_constants.GET_KEYWORDS and result[0] == desktop_constants.TEST_RESULT_FAIL and result[1] == desktop_constants.TEST_RESULT_FALSE ):
                try:
                    lst = list(result)
                    lst[2] = None
                    result = tuple(lst)
                except:
                    pass
            #------------------------------------------------------------------------------------------
            if ( self.action == constants.EXECUTE ):
                if  ( result != constants.TERMINATE  ):
                    result = list(result)
                    screen_details=mythread.json_data['suitedetails'][0]
                    if ( configvalues['screenShot_Flag'].lower() == 'fail' ):
                        if ( result[0].lower() == 'fail' ):
                            if ( keyword not in desktop_constants.APPLICATION_KEYWORDS ):
                                file_path = screen_shot_obj.captureScreenshot(screen_details)
                                result.append(file_path[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        if  ( keyword not in desktop_constants.APPLICATION_KEYWORDS ):
                            file_path = screen_shot_obj.captureScreenshot(screen_details)
                            result.append(file_path[2])
        except TypeError as e:
            err_msg = constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result = list(result)
            result[3] = err_msg
        except Exception as e:
            log.error( e )
        if  ( err_msg != None ):
            log.error( err_msg )
            logger.print_on_console( err_msg )

        return result

    def get_desktop_element(self, xPath, url):
        index = None
        ele = ''
        backend = 'A'
        prev_flag = False
        if ( ";" in xPath ):
            x_var = xPath.split(';')
            xpath = x_var[0]
            xclass = x_var[1]
            try:
                xconID = int(x_var[2])
            except:
                pass #as uia element sometimes has no conID
            if ( len(x_var) == 4 ):
                xname = x_var[3]
            if ( len(x_var) == 5 ):
                """checking for backend process"""
                xname = x_var[3]
                backend = x_var[4].strip()
        else:
            xpath = xPath
            prev_flag = True # setting prev_flag to True since the xpath recieved is of an old test case.
        #logic to find the desktop element using the xpath
        if ( backend == 'A' ):
            app = desktop_launch_keywords.app_win32
            app2 = app
            try:
                win = app.top_window()
                ch = win.children()
                split_xpath = xpath.split('/')
                parent = split_xpath[0]
                index = int(parent[parent.index('[') + 1 : parent.index(']')])
                ele = ch[int(index)]
                for i in range(1, len(split_xpath)):
                    child = split_xpath[i]
                    index = child[child.index('[') + 1 : child.index(']')]
                    ch = ele.children()
                    ele = ch[int(index)]
                #---------------------------------------------------
                try:
                    if ( ele != '' ):     #checking if element is not empty
                        if ( xclass == ele.friendly_class_name() ): #comparing top window element class with the one obtained from TSP
                            if ( ele.friendly_class_name() == 'TabControl' ):
                                if ( xconID != ele.control_id() ): #comparing if the control ID of top window element is same as one from TSP
                                    #-------element dosent handles matched
                                    ele=''
                            else:
                                #-------------------------------------getting text and comparing with xname
                                handle= ele.handle
                                try:
                                    element_text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                                except:
                                    pass
                                if ( element_text != '' ):
                                    try:
                                        comp_text = str(element_text)
                                    except:
                                        comp_text = element_text.encode('ascii', 'replace')
                                else :
                                    comp_text = ele.texts()
                                try:
                                    comp_text = comp_text.strip()
                                except:
                                    comp_text = comp_text[0].strip()
                                #----------------------------------------------------------------------------------
                                if ( xname != comp_text ):
                                    ele = ''
                        else:
                            ele = ''
                except Exception as e:
                    if ( prev_flag == False ):#checking if previous test case flag is True or not.
                        ele = ''  #If false then new test case and AUT structure has changed, so setting the ele to ''
                #---------------------------------------------------
            except Exception as e:
                log.error( "Unable to get desktop elements because : ", e)
            if ( ele == '' ):
                try:
                    ele = self.get_element_if_empty(xclass, xname, app2)
                except:# only for tables
                    ele = self.get_desktop_static_element(xclass, xconID, app)
            if ( ele == '' ):#last attempt if the element is still empty, then find element using original index
                try:
                    ele = ch[int(index)]
                except Exception as e:
                    log.error( e )
                    logger.print_on_console( "Unable to get desktop element because : ", e )
        elif ( backend == 'B' ):
            try:
                import pythoncom
                pythoncom.CoInitialize()
                win = desktop_launch_keywords.app_uia.top_window()
                ch = []
                def rec_ch(child):
                    ch.append(child)
                    for c in child.children():
                        rec_ch(c)
                rec_ch(win)
                split_xpath = xpath.split('/')
                parent = split_xpath[0]
                index = int(parent[parent.index('[') + 1 : parent.index(']')])
                ele = ch[int(index)]
                for i in range(1,len(split_xpath)):
                    child = split_xpath[i]
                    index = child[child.index('[') + 1 : child.index(']')]
                    ch = ele.children()
                    ele = ch[int(index)]
                #warning message
                if ( ele.friendly_class_name() == 'ListView' or ele.friendly_class_name() == 'ListBox' ):
                    log.info( 'List keywords return inconsistant values for elements scraped via method B' )
                    log.error( 'List keywords return inconsistant values for elements scraped via method B' )
                    logger.print_on_console( 'List keywords return inconsistant values for elements scraped via method B' )
            except Exception as e:
                log.error( "Unable to get desktop element because : ", e)
                logger.print_on_console( "Unable to get desktop element because : ", e )
        return ele

    def get_desktop_static_element(self, xclass, xconID, app):
        """This method was added to handle change in tabs, when different tabs are selected, the xpath of all elements will change
        This will result in increment or decrement of objects also!. Hence using this method to comapre the calss name and control ID of object
        returned from UI with all the elements of the top window. The first object whoes class name and control ID is the same is returned."""
        #logic to find the desktop element using custname of the element returned from UI
        ele = ''
        try:
            win1 = app.top_window()
            ch1 = win1.children()
            for i in range(0, len(ch1)):
                try:
                    conID = ch1[i].control_id()
                    className = ch1[i].friendly_class_name()
                    if ( xclass == className ):
                        if ( xconID == conID ):
                            ele = ch1[i]
                except Exception as e:
                    log.error( 'Error occoured in get_desktop_static_element, Err Msg : ', e )
        except Exception as e:
            log.error( 'Error occoured in get_desktop_static_element, Err Msg : ', e )
        return ele
    def get_element_if_empty(self, xclass, xname, app):
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
                    handle = ch2[i].handle
                    try:
                        element_text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                    except:
                        pass
                    if ( element_text != '' ):
                                try:
                                    comp_text = str(element_text)
                                except:
                                    comp_text = element_text.encode('ascii', 'replace')
                    else :
                        comp_text = ch2[i].texts()
                    #------------------------------------------------
                    className = ch2[i].friendly_class_name()
                    try:
                        comp_text = comp_text.strip()
                    except:
                        comp_text = comp_text[0].strip()
                    if ( xclass == className ):
                        if ( xname == comp_text ):
                            ele=ch2[i]
                            break
                except Exception as e:
                    log.error( 'Error occoured in get_element_if_empty, Err Msg : ', e )
        except Exception as e:
            log.error( 'Error occoured in get_element_if_empty, Err Msg : ', e )
        return ele