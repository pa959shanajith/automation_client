#-------------------------------------------------------------------------------
# Name:        sap_dispatcher.py
# Purpose:
#
# Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import logging
import logging.config
log = logging.getLogger('sap_dispatcher.py')
#-------------------------------------------------------------importing  keywords
import sap_launch_keywords
import button_link_keywords_sap
import text_keywords_sap
import sap_element_keywords
import sap_dropdown_keywords
import radio_checkbox_keywords_sap
import saputil_operations
import sap_table_keywords
import sap_shell_keywords
#-------------------------------------------------------------
import sap_constants
import constants
import screenshot_keywords
import readconfig



class SAPDispatcher:

    launch_keywords_obj = sap_launch_keywords.Launch_Keywords()
    editable_text_obj = text_keywords_sap.Text_Keywords()
    button_link_obj =button_link_keywords_sap.ButtonLinkKeyword()
    dropdown_keywords_obj = sap_dropdown_keywords.Dropdown_Keywords()
    radiocheckbox_keywords_obj= radio_checkbox_keywords_sap.Radio_Checkbox_keywords()
    element_keywords_obj=sap_element_keywords.ElementKeywords()
    saputil_keywords_obj=saputil_operations.SapUtilKeywords()
    table_keywords_obj=sap_table_keywords.Table_keywords()
    shell_keywords_obj=sap_shell_keywords.Shell_Keywords()

    def __init__(self):

        self.exception_flag=''
        self.action = None
#-----------------------------------------------------------------for custom objects
    custom_dict = {
                    "click":['radiobutton','checkbox','input','button','select','table'],
                    "getelementtext":['radiobutton','checkbox','input','button','select','table'],
                    "getstatus":['radiobutton','checkbox'],
                    "gettext":['input'],
                    "selectcheckbox":['checkbox'],
                    "selectradiobutton":['radiobutton'],
                    "setsecuretext":['input'],
                    "selectvaluebytext":['select'],
                    "settext":['input'],
                    "unselectcheckbox":['checkbox'],
                    "verifyelementtext":['radiobutton','checkbox','input','button','select','table'],
                    "verifyexists":['radiobutton','checkbox','input','button','select','table']
                  }

    get_ele_type={
                'radio': 'radiobutton',
                'checkbox':'checkbox',
                'dropdown':'select',
                'textbox':'input',
                'button':'button',
                'table':'table',
                }
#-----------------------------------------------------------------for custom objects


    def dispatcher(self,teststepproperty,input,iris_flag):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name.lower()
        err_msg=None
        result=[sap_constants.TEST_RESULT_FAIL,sap_constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
#-----------------------------------------------------------------for custom objects
        try:
            if objectname==sap_constants.CUSTOM and teststepproperty.custom_flag:
                ele_type=input[0].lower()
                if ele_type in self.get_ele_type:
                    ele_type=self.get_ele_type[ele_type]
                parent_xpath=teststepproperty.parent_xpath
                if (keyword in self.custom_dict and ele_type in self.custom_dict[keyword]):
                    custom_sap_element=self.saputil_keywords_obj.getobjectforcustom(parent_xpath,ele_type,input[1])
                    if(custom_sap_element != '' or None):
                        objectname = custom_sap_element
        except Exception as e:
            logger.print_on_console(e)
#-----------------------------------------------------------------for custom objects

        try:


            dict={
                  'launchapplication' : self.launch_keywords_obj.launch_application,
                  'closeapplication':self.launch_keywords_obj.closeApplication,
                  'getpagetitle':self.launch_keywords_obj.getPageTitle,
                  'starttransaction':self.launch_keywords_obj.startTransaction,
                  'serverconnect':self.launch_keywords_obj.serverConnect,
                  'getpopuptext':self.launch_keywords_obj.getPopUpText,
                  'geterrormessage':self.launch_keywords_obj.getErrorMessage,
                  'toolbaraction':self.launch_keywords_obj.toolbar_actions,
                  'settext' : self.editable_text_obj.setText,
                  'setsecuretext':self.editable_text_obj.setSecureText,
                  'gettext':self.editable_text_obj.getText,
                  'cleartext':self.editable_text_obj.clearText,
                  'verifytext':self.editable_text_obj.verifyText,
                  'gettextboxlength':self.editable_text_obj.getTextboxLength,
                  'verifytextboxlength':self.editable_text_obj.verifyTextboxLength,
                  'selectcheckbox':self.radiocheckbox_keywords_obj.select_checkbox,
                  'unselectcheckbox':self.radiocheckbox_keywords_obj.unselect_checkbox,
                  'selectradiobutton':self.radiocheckbox_keywords_obj.select_radiobutton,
                  'getstatus': self.radiocheckbox_keywords_obj.get_status,
                  'getbuttonname':self.button_link_obj.get_button_name,
                  'verifybuttonname':self.button_link_obj.verify_button_name,
                  'uploadfile':self.button_link_obj.button_uploadFile,
                  'getselected':self.dropdown_keywords_obj.getSelected,
                  'getcount':self.dropdown_keywords_obj.getCount,
##                  'getvaluebyindex':self.dropdown_keywords_obj.getValueByIndex,
##                  'selectvaluebyindex':self.dropdown_keywords_obj.selectValueByIndex,
                  'selectvaluebytext':self.dropdown_keywords_obj.selectValueByText,
                  'verifycount':self.dropdown_keywords_obj.verifyCount,
                  'verifyselectedvalue':self.dropdown_keywords_obj.verifySelectedValue,
                  'verifyvaluesexists':self.dropdown_keywords_obj.verifyValuesExists,
                  'verifyallvalues':self.dropdown_keywords_obj.verifyAllValues,
                  'click':self.element_keywords_obj.click,
                  'rightclick':self.element_keywords_obj.rightClick,
                  'doubleclick':self.element_keywords_obj.doubleClick,
                  'mousehover':self.element_keywords_obj.mouseHover,
                  'getelementtext':self.element_keywords_obj.get_element_text,
                  'verifyelementtext':self.element_keywords_obj.verify_element_text,
                  'gettooltiptext':self.element_keywords_obj.getTooltipText,
                  'verifytooltiptext':self.element_keywords_obj.verifyTooltipText,
                  'geticonname':self.element_keywords_obj.getIconName,
                  'getinputhelp':self.element_keywords_obj.getInputHelp,
                  'setfocus':self.element_keywords_obj.setFocus,
                  'scrollup':self.element_keywords_obj.scrollUp,
                  'scrolldown':self.element_keywords_obj.scrollDown,
                  'scrollleft':self.element_keywords_obj.scrollLeft,
                  'scrollright':self.element_keywords_obj.scrollRight,
                  'movetabs':self.element_keywords_obj.moveTabs,
                  'selecttab':self.element_keywords_obj.selectTab,
                  'verifyenabled':self.saputil_keywords_obj.verifyEnabled,
                  'verifydisabled':self.saputil_keywords_obj.verifyDisabled,
                  'verifyexists':self.saputil_keywords_obj.verifyExists,
                  'verifyhidden':self.saputil_keywords_obj.verifyHidden,
                  'verifyvisible':self.saputil_keywords_obj.verifyVisible,
                  'getrowcount':self.table_keywords_obj.getRowCount,
                  'getcolumncount':self.table_keywords_obj.getColumnCount,
                  'getcolnumbytext':self.table_keywords_obj.getColNumByText,
                  'getrownumbytext':self.table_keywords_obj.getRowNumByText,
                  'getcellvalue':self.table_keywords_obj.getCellValue,
                  'verifycellvalue':self.table_keywords_obj.verifyCellValue,
                  #commenting dropdown code inside table cell
                  'verifytextexists':self.table_keywords_obj.verifyTextExists,
##                  'cellclick':self.table_keywords_obj.cellClick,
##                  'selectvaluebyindex':self.table_keywords_obj.selectValueByIndex,
##                  'selectvaluebytext':self.table_keywords_obj.selectValueByText,
##                  'getselected':self.table_keywords_obj.getSelected,
                  'getcellstatus':self.table_keywords_obj.getStatus,
                  'selectrow':self.table_keywords_obj.selectRow,
                  'unselectrow':self.table_keywords_obj.unselectRow,
                  'getcountofrows':self.shell_keywords_obj.get_rowCount,
                  'getcountofcolumns':self.shell_keywords_obj.get_colCount,
                  'selectrows':self.shell_keywords_obj.selectRows,
                  'presstoolbarbutton':self.shell_keywords_obj.pressToolBarButton,
                  'getcelltext': self.shell_keywords_obj.getCellText,
                  'clickcell':self.shell_keywords_obj.clickCell,
                  'doubleclickcell':self.shell_keywords_obj.doubleClickCell,
                  'selecttreenode':self.shell_keywords_obj.selectTreeNode,
                  'getnodenamebyindex':self.shell_keywords_obj.getNodeNameByIndex,
                  'setshelltext':self.shell_keywords_obj.setShellText,
                  'getrowcolbytext':self.shell_keywords_obj.getRowColByText,
                  'verifytreepath':self.shell_keywords_obj.verifyTreePath
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

            keyword=keyword.lower()
            if keyword in dict.keys():
                if keyword=='serverconnect' or keyword=='launchapplication' or keyword=='starttransaction' or keyword=='toolbaraction' :
                    result= dict[keyword](input,output)
                else:
                    if (teststepproperty.cord != None and teststepproperty.cord != ''):
                        obj_props = teststepproperty.objectname.split(';')
                        coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                        objectname = {'cord': teststepproperty.cord, 'coordinates':coord}
                        from sap_scraping import Scrape
                        scrapingObj=Scrape()
                        sapgui = self.saputil_keywords_obj.getSapObject()
                        if(sapgui != None):
                            wnd = scrapingObj.getWindow(sapgui)
                            wnd = wnd.Text + '/'
                            self.launch_keywords_obj.setWindowToForeground(wnd)
                        if(teststepproperty.custom_flag):
                            result = dict[keyword](objectname,input,output,teststepproperty.parent_xpath)
                        else:
                            result = dict[keyword](objectname,input,output)
                    else:
                        result= dict[keyword](objectname,input,output)
                if not(sap_constants.ELEMENT_FOUND) and self.exception_flag:
                    logger.print_on_console('Element not found terminating')
                    result=constants.TERMINATE
            else:
                err_msg=sap_constants.INVALID_KEYWORD
                logger.print_on_console(err_msg)
                result[3]=err_msg
            configvalues = readconfig.configvalues
            screen_shot_obj = screenshot_keywords.Screenshot()
            if self.action == constants.EXECUTE:
                if result !=constants.TERMINATE:
                    result=list(result)
                    if configvalues['screenShot_Flag'].lower() == 'fail':
                        if result[0].lower() == 'fail':
                            if keyword not in sap_constants.APPLICATION_KEYWORDS:
                                file_path = screen_shot_obj.captureScreenshot()
                                result.append(file_path[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        if keyword not in sap_constants.APPLICATION_KEYWORDS:
                            file_path = screen_shot_obj.captureScreenshot()
                            result.append(file_path[2])
        except TypeError as e:
            logger.print_on_console('type error found')
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return result
