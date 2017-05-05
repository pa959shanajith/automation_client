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
import launch_keywords
import button_link_keywords_sap
import text_keywords_sap
import element_keywords
import dropdown_keywords
import radio_checkbox_keywords_sap
import saputil_operations
import table_keywords
#-------------------------------------------------------------
import sap_constants
import constants



class SAPDispatcher:

    launch_keywords_obj = launch_keywords.Launch_Keywords()
    editable_text_obj = text_keywords_sap.Text_Keywords()
    button_link_obj =button_link_keywords_sap.ButtonLinkKeyword()
    dropdown_keywords_obj = dropdown_keywords.Dropdown_Keywords()
    radiocheckbox_keywords_obj= radio_checkbox_keywords_sap.Radio_Checkbox_keywords()
    element_keywords_obj=element_keywords.ElementKeywords()
    saputil_keywords_obj=saputil_operations.SapUtilKeywords()
    table_keywords_obj=table_keywords.Table_keywords()


    def __init__(self):

        self.exception_flag=''



    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name
        url = teststepproperty.url
        err_msg=None
        result=[sap_constants.TEST_RESULT_FAIL,sap_constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]

        try:


            dict={
                  'launchapplication' : self.launch_keywords_obj.launch_application,
                  'closeapplication':self.launch_keywords_obj.closeApplication,
                  'getpagetitle':self.launch_keywords_obj.getPageTitle,
                  'starttransaction':self.launch_keywords_obj.startTransaction,
                  'serverconnect':self.launch_keywords_obj.serverConnect,
                  'geterrormessage':self.launch_keywords_obj.getErrorMessage,
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
                  'click':self.button_link_obj.click,
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
                  'clickelement':self.element_keywords_obj.click_element,
                  'getelementtext':self.element_keywords_obj.get_element_text,
                  'gettooltiptext':self.element_keywords_obj.getTooltipText,
                  'verifyenabled':self.saputil_keywords_obj.verifyEnabled,
                  'verifydisabled':self.saputil_keywords_obj.verifyDisabled,
                  'verifyexists':self.saputil_keywords_obj.VerifyExists,
                  'setfocus':self.saputil_keywords_obj.setFocus,
                  'getrowcount':self.table_keywords_obj.getRowCount,
                  'getcolumncount':self.table_keywords_obj.getColumnCount,
                  'mousehover':self.table_keywords_obj.mouseHover,
                  'getcolnumbytext':self.table_keywords_obj.getColNumByText,
                  'getrownumbytext':self.table_keywords_obj.getRowNumByText,
                  'getcellvalue':self.table_keywords_obj.getCellValue,
                  'verifycellvalue':self.table_keywords_obj.verifyCellValue,
                  #commenting dropdown code inside table cell
                  'verifytextexists':self.table_keywords_obj.verifyTextExists,
                  'cellclick':self.table_keywords_obj.cellClick,
##                  'selectvaluebyindex':self.table_keywords_obj.selectValueByIndex,
##                  'selectvaluebytext':self.table_keywords_obj.selectValueByText,
##                  'getselected':self.table_keywords_obj.getSelected,
                  'gettablestatus':self.table_keywords_obj.getStatus,
                  'getcelltooltip':self.table_keywords_obj.getCellToolTip,
                  'tablecellclick':self.table_keywords_obj.tableCell_click,
                  'doubleclick':self.table_keywords_obj.tableCell_doubleClick,
                  'selectrow':self.table_keywords_obj.selectRow,
                  'unselectrow':self.table_keywords_obj.unselectRow
                   }



            keyword=keyword.lower()
            if keyword in dict.keys():
                if keyword=='serverconnect' or keyword=='launchapplication' or keyword=='starttransaction' :
                    result= dict[keyword](input,output)
                else:
                    result= dict[keyword](objectname,url,input,output)
                if not(sap_constants.ELEMENT_FOUND) and self.exception_flag:
                    logger.print_on_console('Element not found terminating')
                    result=constants.TERMINATE
            else:
                err_msg=sap_constants.INVALID_KEYWORD
                logger.print_on_console(err_msg)

                result[3]=err_msg
        except TypeError as e:
            logger.print_on_console('type error found')
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            import traceback
            traceback.print_exc()
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)

        return result



