#-------------------------------------------------------------------------------
# Name:        sap_dispatcher.py
# Purpose:     acts as a central dispatch unit, where inputs are dispatched to their respective keywords.
#
# Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import logging
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
import sap_shell_gridview_toolbar_keywords
import sap_shell_tree_keywords
import sap_shell_calendar_keywords
#-------------------------------------------------------------
import sap_constants
import constants
import screenshot_keywords
import readconfig

class SAPDispatcher:

    launch_keywords_obj = sap_launch_keywords.Launch_Keywords()
    editable_text_obj = text_keywords_sap.Text_Keywords()
    button_link_obj = button_link_keywords_sap.ButtonLinkKeyword()
    dropdown_keywords_obj = sap_dropdown_keywords.Dropdown_Keywords()
    radiocheckbox_keywords_obj = radio_checkbox_keywords_sap.Radio_Checkbox_keywords()
    element_keywords_obj = sap_element_keywords.ElementKeywords()
    saputil_keywords_obj = saputil_operations.SapUtilKeywords()
    table_keywords_obj = sap_table_keywords.Table_keywords()
    shell_keywords_obj = sap_shell_keywords.Shell_Keywords()
    shell_gridview_toolbar_keywords_obj = sap_shell_gridview_toolbar_keywords.Shell_GridView_Toolbar_Keywords()
    shell_tree_keywords_obj = sap_shell_tree_keywords.Shell_Tree_Keywords()
    shell_calendar_keywords_obj = sap_shell_calendar_keywords.Shell_Calendar_Keywords()
    sap_dict = {
            #------------------------------------------------------launch keywords
            'launchapplication' : launch_keywords_obj.launch_application,
            'closeapplication' : launch_keywords_obj.closeApplication,
            'getpagetitle' : launch_keywords_obj.getPageTitle,
            'starttransaction' : launch_keywords_obj.startTransaction,
            'serverconnect' : launch_keywords_obj.serverConnect,
            'getpopuptext' : launch_keywords_obj.getPopUpText,
            'getstatusbarmessage' : launch_keywords_obj.getStatusBarMessage,
            'toolbaraction' : launch_keywords_obj.toolbar_actions,
            'selectmenu': launch_keywords_obj.selectMenu,
            'doubleclickstatusbar': launch_keywords_obj.doubleClickStatusBar,
            #------------------------------------------------------textbox keywords
            'settext' : editable_text_obj.setText,
            'setsecuretext' : editable_text_obj.setSecureText,
            'gettext' : editable_text_obj.getText,
            'cleartext' : editable_text_obj.clearText,
            'verifytext' : editable_text_obj.verifyText,
            'gettextboxlength' : editable_text_obj.getTextboxLength,
            'verifytextboxlength' : editable_text_obj.verifyTextboxLength,
            #------------------------------------------------------radio btn keywords
            'selectcheckbox' : radiocheckbox_keywords_obj.select_checkbox,
            'unselectcheckbox' : radiocheckbox_keywords_obj.unselect_checkbox,
            'selectradiobutton' : radiocheckbox_keywords_obj.select_radiobutton,
            'getstatus' : radiocheckbox_keywords_obj.get_status,
            #------------------------------------------------------button keywords
            'getbuttonname' : button_link_obj.get_button_name,
            'verifybuttonname' : button_link_obj.verify_button_name,
            'uploadfile' : button_link_obj.button_uploadFile,
            #------------------------------------------------------dropdown keywords
            'getselected' : dropdown_keywords_obj.getSelected,
            'getcount' : dropdown_keywords_obj.getCount,
            'getvaluebyindex' : dropdown_keywords_obj.getValueByIndex,
            'selectvaluebyindex' : dropdown_keywords_obj.selectValueByIndex,
            'selectvaluebytext' : dropdown_keywords_obj.selectValueByText,
            'verifycount' : dropdown_keywords_obj.verifyCount,
            'verifyselectedvalue' : dropdown_keywords_obj.verifySelectedValue,
            'verifyvaluesexists' : dropdown_keywords_obj.verifyValuesExists,
            'verifyallvalues' : dropdown_keywords_obj.verifyAllValues,
            #------------------------------------------------------element keywords
            'click' : element_keywords_obj.click,
            'rightclick' : element_keywords_obj.rightClick,
            'doubleclick' : element_keywords_obj.doubleClick,
            'mousehover' : element_keywords_obj.mouseHover,
            'getelementtext' : element_keywords_obj.get_element_text,
            'verifyelementtext' : element_keywords_obj.verify_element_text,
            'gettooltiptext' : element_keywords_obj.getTooltipText,
            'verifytooltiptext' : element_keywords_obj.verifyTooltipText,
            'geticonname' : element_keywords_obj.getIconName,
            'verifyiconname' : element_keywords_obj.verifyIconName,
            'getinputhelp' : element_keywords_obj.getInputHelp,
            'setfocus' : element_keywords_obj.setFocus,
            'scrollup' : element_keywords_obj.scrollUp,
            'scrolldown' : element_keywords_obj.scrollDown,
            'scrollleft' : element_keywords_obj.scrollLeft,
            'scrollright' : element_keywords_obj.scrollRight,
            'movetabs' : element_keywords_obj.moveTabs,
            'selecttab' : element_keywords_obj.selectTab,
            #------------------------------------------------------sap util keywords
            'verifyenabled' : saputil_keywords_obj.verifyEnabled,
            'verifydisabled' : saputil_keywords_obj.verifyDisabled,
            'verifyexists' : saputil_keywords_obj.verifyExists,
            'verifyhidden' : saputil_keywords_obj.verifyHidden,
            'verifyvisible' : saputil_keywords_obj.verifyVisible,
            #-------------------------------------------------------table keywords
            'getrowcount' : table_keywords_obj.getRowCount,
            'getcolumncount' : table_keywords_obj.getColumnCount,
            'getcolnumbytext' : table_keywords_obj.getColNumByText,
            'getrownumbytext' : table_keywords_obj.getRowNumByText,
            'getcellvalue' : table_keywords_obj.getCellValue,
            'verifycellvalue' : table_keywords_obj.verifyCellValue,
            #commenting dropdown code inside table cell
            'verifytextexists' : table_keywords_obj.verifyTextExists,
            # 'cellclick':table_keywords_obj.cellClick,
            # 'selectvaluebyindex':table_keywords_obj.selectValueByIndex,
            # 'selectvaluebytext':table_keywords_obj.selectValueByText,
            # 'getselected':table_keywords_obj.getSelected,
            'getcellstatus' : table_keywords_obj.getStatus,
            'selectrow' : table_keywords_obj.selectRow,
            'unselectrow' : table_keywords_obj.unselectRow,
            'selectcolumn' : table_keywords_obj.selectColumn,
            'unselectColumn' : table_keywords_obj.unselectColumn,
            'setcelltext' : table_keywords_obj.setCellText,
            #Shell keywords
            #-----------------------------------------------------gridviewkeywords
            'getcountofrows' : shell_keywords_obj.get_rowCount,
            'getcountofcolumns' : shell_keywords_obj.get_colCount,
            'selectrows' : shell_keywords_obj.selectRows,
            'presstoolbarbutton' : shell_keywords_obj.pressToolBarButton,
            'getcelltext' : shell_keywords_obj.getCellText,
            'clickcell' : shell_keywords_obj.clickCell,
            'doubleclickcell' : shell_keywords_obj.doubleClickCell,
            'setshelltext' : shell_keywords_obj.setShellText,
            'getrowcolbytext' : shell_keywords_obj.getRowColByText,
            'toolbaractionkeys' : shell_keywords_obj.toolBarActionKeys,
            'settextincell' : shell_keywords_obj.setCellText,
            'selectallrows' : shell_keywords_obj.selectAllRows,
            'unselectallselections' : shell_keywords_obj.unselectAllSelections,
            'scrolltorownumber' : shell_keywords_obj.scrollToRowNumber,
            'getcellcolor' : shell_keywords_obj.getCellColor,
            #------------------------------------------------------treekeywords
            'selecttreeelement' : shell_tree_keywords_obj.selectTreeElement,
            'gettreenodetext' : shell_tree_keywords_obj.getTreeNodeText,
            'gettreenodecount' : shell_tree_keywords_obj.getTreeNodeCount,
            'singleselectparentofselected' : shell_tree_keywords_obj.singleSelectParentOfSelected,
            'collapsetree' : shell_tree_keywords_obj.collapseTree,
            'getcolvaluecorrtoselectednode' : shell_tree_keywords_obj.getColValueCorrToSelectedNode,
            'selecttreenode' : shell_tree_keywords_obj.selectTreeNode,
            'getnodenamebyindex' : shell_tree_keywords_obj.getNodeNameByIndex,
            'verifytreepath' : shell_tree_keywords_obj.verifyTreePath,
            #------------------------------------------------------callenderkeywords
            'selectdate' : shell_calendar_keywords_obj.select_date,
            'selectrange':shell_calendar_keywords_obj.select_range,
            'selectmonth':shell_calendar_keywords_obj.select_month,
            'selectweek':shell_calendar_keywords_obj.select_week
            }

    def __init__(self):

        self.exception_flag = ''
        self.action = None
#-----------------------------------------------------------------for custom objects
    custom_dict = {
                    "click" : ['radiobutton', 'checkbox', 'input', 'button', 'select', 'table'],
                    "getelementtext" : ['radiobutton', 'checkbox', 'input', 'button', 'select', 'table'],
                    "getstatus" : ['radiobutton', 'checkbox'],
                    "gettext" : ['input'],
                    "selectcheckbox" : ['checkbox'],
                    "selectradiobutton" : ['radiobutton'],
                    "setsecuretext" : ['input'],
                    "selectvaluebytext" : ['select'],
                    "settext" : ['input'],
                    "unselectcheckbox" : ['checkbox'],
                    "verifyelementtext" : ['radiobutton', 'checkbox', 'input', 'button', 'select', 'table'],
                    "verifyexists" : ['radiobutton', 'checkbox', 'input', 'button', 'select', 'table']
                  }

    get_ele_type = {
                    'radio' : 'radiobutton',
                    'checkbox' : 'checkbox',
                    'dropdown' : 'select',
                    'textbox' : 'input',
                    'button' : 'button',
                    'table' : 'table',
                    }
#-----------------------------------------------------------------for custom objects


    def dispatcher(self, teststepproperty, input, iris_flag):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name.lower()
        err_msg = None
        result = [sap_constants.TEST_RESULT_FAIL, sap_constants.TEST_RESULT_FALSE, constants.OUTPUT_CONSTANT, err_msg]
#-----------------------------------------------------------------for custom objects
        try:
            if ( objectname == sap_constants.CUSTOM and teststepproperty.custom_flag ):
                ele_type = input[0].lower()
                if ( ele_type in self.get_ele_type ):
                    ele_type = self.get_ele_type[ele_type]
                parent_xpath = teststepproperty.parent_xpath
                if ( keyword in self.custom_dict and ele_type in self.custom_dict[keyword] ):
                    custom_sap_element = self.saputil_keywords_obj.getobjectforcustom(parent_xpath, ele_type, input[1])
                    if ( custom_sap_element != '' or None ):
                        objectname = custom_sap_element
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in dispatcher" )
#-----------------------------------------------------------------for custom objects
        try:
            if ( iris_flag ):
                import iris_operations
                iris_object = iris_operations.IRISKeywords()
                self.sap_dict['clickiris'] = iris_object.clickiris
                self.sap_dict['doubleclickiris'] = iris_object.doubleclickiris
                self.sap_dict['rightclickiris'] = iris_object.rightclickiris
                self.sap_dict['settextiris'] = iris_object.settextiris
                self.sap_dict['gettextiris'] = iris_object.gettextiris
                self.sap_dict['getrowcountiris'] = iris_object.getrowcountiris
                self.sap_dict['getcolcountiris'] = iris_object.getcolcountiris
                self.sap_dict['getcellvalueiris'] = iris_object.getcellvalueiris
                self.sap_dict['verifyexistsiris'] = iris_object.verifyexistsiris
                self.sap_dict['verifytextiris'] = iris_object.verifytextiris

            keyword = keyword.lower()
            if ( keyword in list(self.sap_dict.keys()) ):
                if ( keyword == 'serverconnect' or keyword == 'launchapplication' or keyword == 'starttransaction' or keyword == 'toolbaraction' or keyword == 'selectmenu'):
                    result= self.sap_dict[keyword](input, output)
                else:
                    if ( teststepproperty.cord != None and teststepproperty.cord != '' ):
                        obj_props = teststepproperty.objectname.split(';')
                        coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                        objectname = {'cord' : teststepproperty.cord, 'coordinates' : coord}
                        from sap_scraping import Scrape
                        scrapingObj = Scrape()
                        sapgui = self.saputil_keywords_obj.getSapObject()
                        if ( sapgui ):
                            wnd = scrapingObj.getWindow(sapgui)
                            wnd = wnd.Text + '/'
                            self.launch_keywords_obj.setWindowToForeground(wnd)
                        if ( teststepproperty.custom_flag ):
                            result = self.sap_dict[keyword](objectname, input, output, teststepproperty.parent_xpath)
                        else:
                            result = self.sap_dict[keyword](objectname, input, output)
                    else:
                        result = self.sap_dict[keyword](objectname, input, output)
                if ( not (sap_constants.ELEMENT_FOUND) and self.exception_flag ):
                    logger.print_on_console( 'Element not found terminating' )
                    result = constants.TERMINATE
            else:
                err_msg = sap_constants.INVALID_KEYWORD
                logger.print_on_console( err_msg )
                result[3] = err_msg
            configvalues = readconfig.configvalues
            screen_shot_obj = screenshot_keywords.Screenshot()
            #------------------------------------------return null for get-keywords if keyword fails
            if ( keyword in sap_constants.GET_KEYWORDS and result[0] == sap_constants.TEST_RESULT_FAIL and result[1] == sap_constants.TEST_RESULT_FALSE ):
                try:
                    lst = list(result)
                    lst[2] = None
                    result = tuple(lst)
                except:
                    pass
            #------------------------------------------------------------------------------------------
            if ( self.action == constants.EXECUTE ):
                if ( result != constants.TERMINATE ):
                    result = list(result)
                    if ( configvalues['screenShot_Flag'].lower() == 'fail' ):
                        if ( result[0].lower() == 'fail' ):
                            if ( keyword not in sap_constants.APPLICATION_KEYWORDS ):
                                file_path = screen_shot_obj.captureScreenshot()
                                result.append(file_path[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        if ( keyword not in sap_constants.APPLICATION_KEYWORDS ):
                            file_path = screen_shot_obj.captureScreenshot()
                            result.append(file_path[2])
        except TypeError as e:
            logger.print_on_console( 'Type error found' )
            err_msg = constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION'] + ' : ' + str(e)
            result[3] = err_msg
            log.error( err_msg )
            logger.print_on_console( "Error occured in dispatcher" )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in dispatcher" )
        if ( err_msg ):
            log.error( err_msg )
            logger.print_on_console( err_msg )
        return result