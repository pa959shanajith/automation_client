#-------------------------------------------------------------------------------
# Name:        oebs_dispatcher.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     25-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import oebs_fullscrape
import oebs_utils
import logger
import logging
import oebs_constants
import constants
import screenshot_keywords
import oebs_mouseops
import oebs_key_objects
import oebs_textops
import oebs_serverUtilities
from oebs_utilops import UtilOperations
from oebs_buttonops import ButtonOperations
from oebs_radiocheckboxops import RadioCheckboxOperations
from oebs_dropdownlistboxops import DropdownListboxOperations
from oebs_elementsops import ElementOperations
from oebs_tableops import TableOperations
from oebs_scrollbarops import ScrollbarOperations
from oebs_internalframeops import InternalFrameOperations
import readconfig
import time

import readconfig
import iris_operations
log = logging.getLogger('oebs_dispatcher.py')

class OebsDispatcher:

    utils_obj=oebs_utils.Utils()
    scrape_obj=oebs_fullscrape.FullScrape()

    def __init__(self):
        self.exception_flag=''
        self.action = None
        self.iris_object = iris_operations.IRISKeywords()
        self.windowname = None

        self.txtops_obj=oebs_textops.TextOperations()
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()
        self.buttonops_obj=ButtonOperations()
        self.radiocheckboxops_obj=RadioCheckboxOperations()
        self.dropdownlistboxops_obj=DropdownListboxOperations()

        self.elementsops_obj=ElementOperations()
        self.tableops_obj=TableOperations()
        self.scrollbarops_obj=ScrollbarOperations()
        self.internalframeops_obj=InternalFrameOperations()
        self.utils_obj=oebs_utils.Utils()
        self.required_on_top = {
                            'mousehover': 1,
                            'down': 1,
                            'up' : 1,
                            'left' : 1,
                            'right': 1,
                            'cellclick' : 1,
                            'clickelement': 1,
                            'selectmultiplevaluesbytext': 1,
                            'selectvaluebyindex': 1,
                            'deselectall': 1,
                            'selectmultiplevaluesbyindexes': 1,
                            'selectvaluebytext': 1,
                            'selectallvalues': 1,
                            'unselectcheckbox': 1,
                            'selectcheckbox': 1,
                            'selectradiobutton': 1,
                            'doubleclick': 1,
                            'click': 1,
                            'rightclick': 1,
                            'setfocus': 1,
                            'setsecuretext': 1,
                            'cleartext': 1,
                            'selectfromnavigator': 1
                        }
        self.keyword_dict = {
                            'findwindowandattach':self.utils_obj.find_window_and_attach,
                            'launchapplication':self.utils_obj.launch_application,
                            'closeapplication':self.utils_obj.close_application,
                            'getobjectforcustom' : self.utilities_obj.getobjectforcustom,
                            'drop'    : self.utilops_obj.drop,
                            'drag'     : self.utilops_obj.drag,
                            'mousehover'     : self.utilops_obj.mousehover,
                            'waitforelementvisible'  : self.elementsops_obj.waitforelementvisible,
                            'toggleminimize' : self.internalframeops_obj.toggleminimize,
                            'togglemaximize'      : self.internalframeops_obj.togglemaximize,
                            'closeframe'      : self.internalframeops_obj.closeframe,
                            'switchtoframe':self.utilops_obj.switchtoframe,
                            'selectmenu':self.utilops_obj.select_menu,

                            'down':self.scrollbarops_obj.down,
                            'up' : self.scrollbarops_obj.up,
                            'left' : self.scrollbarops_obj.left,
                            'right':self.scrollbarops_obj.right,

                            'cellclick' : self.tableops_obj.cellclick,
                            'verifycellvalue' : self.tableops_obj.verifycellvalue,
                            'getcellvalue': self.tableops_obj.getcellvalue,
                            'getcolumncount' : self.tableops_obj.getcolumncount,
                            'getrowcount'    : self.tableops_obj.getrowcount,

                            'verifyelementtext' : self.elementsops_obj.verifyelementtext,
                            'getelementtext'  : self.elementsops_obj.getelementtext,
                            'clickelement':self.elementsops_obj.clickelement,


                            'selectmultiplevaluesbytext':self.dropdownlistboxops_obj.selectmultiplevaluesbytext,
                            'selectvaluebyindex':self.dropdownlistboxops_obj.selectvaluebyindex,
                            'getvaluebyindex':self.dropdownlistboxops_obj.getvaluebyindex,
                            'deselectall':self.dropdownlistboxops_obj.deselectall,
                            'getmultiplevaluesbyindexes':self.dropdownlistboxops_obj.getmultiplevaluesbyindexes,
                            'verifyselectedvalues':self.dropdownlistboxops_obj.verifyselectedvalues,
                            'verifyselectedvalue':self.dropdownlistboxops_obj.verifyselectedvalue,
                            'verifyvaluesexists':self.dropdownlistboxops_obj.verifyvaluesexists,
                            'verifyallvalues':self.dropdownlistboxops_obj.verifyallvalues,
                            'verifycount':self.dropdownlistboxops_obj.verifycount,
                            'getcount':self.dropdownlistboxops_obj.getcount,
                            'selectmultiplevaluesbyindexes':self.dropdownlistboxops_obj.selectmultiplevaluesbyindexes,
                            'selectvaluebytext':self.dropdownlistboxops_obj.selectvaluebytext,
                            'selectallvalues':self.dropdownlistboxops_obj.selectallvalues,
                            'getselected':self.dropdownlistboxops_obj.getselected,
                            'getallvalues':self.dropdownlistboxops_obj.getallvalues,
                            'selectfromnavigator':self.dropdownlistboxops_obj.select_from_navigator,

                        
                            'getstatus':self.radiocheckboxops_obj.getstatus,
                            'unselectcheckbox':self.radiocheckboxops_obj.unselectcheckbox,
                            'selectcheckbox':self.radiocheckboxops_obj.selectcheckbox,
                            'selectradiobutton':self.radiocheckboxops_obj.selectradiobutton,

                            'verifylinktext':self.buttonops_obj.verifylinktext,
                            'getlinktext':self.buttonops_obj.getlinktext,
                            'doubleclick':self.buttonops_obj.doubleclick,
                            'click':self.buttonops_obj.click,
                            'verifybuttonname':self.buttonops_obj.verifybuttonname,
                            'getbuttonname':self.buttonops_obj.getbuttonname,

                            'sendfunctionkeys':self.utilops_obj.sendfunctionkeys,
                            'rightclick':self.utilops_obj.rightclick,
                            'verifydoesnotexists':self.utilops_obj.verifydoesnotexists,
                            'verifyexists':self.utilops_obj.verifyexists,
                            'gettooltiptext':self.utilops_obj.gettooltiptext,
                            'verifytooltiptext':self.utilops_obj.verifytooltiptext,
                            'verifyreadonly':self.utilops_obj.verifyreadonly,
                            'verifyhidden':self.utilops_obj.verifyhidden,
                            'verifyvisible':self.utilops_obj.verifyvisible,
                            'verifydisabled':self.utilops_obj.verifydisabled,
                            'verifyenabled':self.utilops_obj.verifyenabled,
                            'setfocus':self.utilops_obj.setfocus,

                            'setsecuretext':self.txtops_obj.setsecuretext,
                            'cleartext':self.txtops_obj.cleartext,
                            'verifytext':self.txtops_obj.verifytext,
                            'settext':self.txtops_obj.settext,
                            'gettext':self.txtops_obj.gettext,

                            'closeapplictaion':self.utils_obj.close_application,

                            'clickiris':self.iris_object.clickiris,
                            'doubleclickiris':self.iris_object.doubleclickiris,
                            'rightclickiris':self.iris_object.rightclickiris,
                            'settextiris':self.iris_object.settextiris,
                            'setsecuretextiris':self.iris_object.setsecuretextiris,
                            'gettextiris':self.iris_object.gettextiris,
                            'getrowcountiris':self.iris_object.getrowcountiris,
                            'getcolcountiris':self.iris_object.getcolcountiris,
                            'getcellvalueiris':self.iris_object.getcellvalueiris,
                            'verifyexistsiris':self.iris_object.verifyexistsiris,
                            'verifytextiris':self.iris_object.verifytextiris,
                            'cleartextiris':self.iris_object.cleartextiris,
                            'dragiris':self.iris_object.dragiris,
                            'dropiris':self.iris_object.dropiris,
                            'mousehoveriris':self.iris_object.mousehoveriris,
                            'setcellvalueiris':self.iris_object.setcellvalueiris,
                            'verifycellvalueiris':self.iris_object.verifycellvalueiris,
                            'clickcelliris':self.iris_object.clickcelliris,
                            'doubleclickcelliris':self.iris_object.doubleclickcelliris,
                            'rightclickcelliris':self.iris_object.rightclickcelliris,
                            'mousehovercelliris':self.iris_object.mousehovercelliris,
                            'getstatusiris':self.iris_object.getstatusiris,
                            'scrollupiris':self.iris_object.scrollupiris,
                            'scrolldowniris':self.iris_object.scrolldowniris,
                            'scrollleftiris':self.iris_object.scrollleftiris,
                            'scrollrightiris':self.iris_object.scrollrightiris
                        }


    custom_dict={
                    'getstatus': ['radio button','check box'],
                    'selectradiobutton': ['radio button'],
                    'selectcheckbox': ['check box'],
                    'unselectcheckbox': ['check box'],

                    'selectvaluebyindex':['combo box','list'],
                    'selectvaluebytext': ['combo box','list'],

                    'settext': ['text'],
                    'gettext': ['text'],
                    'cleartext': ['text'],
                    'setsecuretext': ['text'],
                    'verifytext': ['text'],

                    'getbuttonname': ['push button'],
                    'mousehover': ['push button','combo box'],
                    'verifybuttonname': ['push button'],

                    'getallvalues': ['combo box',  'list'],
                    'getcount': ['combo box', 'list'],
                    'getselected': ['combo box', 'list'],
                    'getvaluebyindex': ['combo box', 'list'],
                    'verifyallvalues': ['combo box', 'list'],
                    'verifycount': ['combo box', 'list'],
                    'verifyvaluesexists' : ['combo box', 'list']
                    }

    get_ele_type={
                    'radio': 'radio button',
                    'checkbox':'check box',
                    'dropdown':'combo box',
                    'listbox':'list',
                    'textbox':'text',
                    'button':'push button'
                    }
    custom_dict_element={'element':['clickelement','setfocus','doubleclick','rightclick','getelementtext','verifyelementtext','verifyexists', 'verifydoesnotexists', 'verifyreadonly','verifyhidden','verifyvisible','sendfunctionkeys','waitforelementvisible', 'verifydisabled', 'verifyenabled']}

    def clear_oebs_window_name(self):
        log.info('Clearing the window name')
        self.windowname=None

    def print_error(self,err_msg):
        err_msg1=constants.ERROR_CODE_DICT[err_msg]
        logger.print_on_console(err_msg1)
        log.error(err_msg1)


    def assign_url_objectname(self,tsp,input):
        keyword=tsp.name.lower()
        objectname=tsp.objectname
        if objectname==oebs_constants.CUSTOM and tsp.custom_flag:
            log.info('Encountered Custom object')
            parent_xpath=tsp.parent_xpath
            log.info('parent_xpath is ')
            log.info(parent_xpath)
            if len(input)>=2:
                ele_type=input[0].lower()
                if ele_type in self.get_ele_type:
                    ele_type=self.get_ele_type[ele_type]
                if (keyword in self.custom_dict and ele_type in self.custom_dict[keyword]) or keyword in list(self.custom_dict_element.values())[0]:
                    custom_oebs_element=self.utilities_obj.getobjectforcustom(self.windowname,parent_xpath,ele_type,input[1])
                    log.info('custom_oebs_element')
                    log.info(custom_oebs_element)
                    if custom_oebs_element != '':
                        input.reverse()
                        for x in range(0,2):
                            input.pop()
                        input.reverse()
                        objectname=custom_oebs_element
                    else:
                        self.print_error('ERR_CUSTOM_NOTFOUND')
                else:
                    self.print_error('ERR_CUSTOM_MISMATCH')
            else:
                self.print_error('ERR_PRECONDITION_NOTMET')
        message=[self.windowname,objectname,tsp.name,input,tsp.outputval,tsp.objectname,tsp.top,tsp.left,tsp.width,tsp.height]
        return message

    def dispatcher(self,tsp,input,mythread,*message):
        logger.print_on_console('Keyword is '+tsp.name)
        keyword=tsp.name
        err_msg=None
        output = tsp.outputval
        result = [constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
        self.windowname = tsp.url or self.windowname 
        if self.windowname is not None and tsp.name.lower()!='findwindowandattach':
            self.utils_obj.set_to_foreground(self.windowname)
        elif tsp.name.lower() == 'findwindowandattach':
            self.windowname = input[0]
        message=self.assign_url_objectname(tsp,input)
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',message[0],message[1],message[2],message[3],message[4])
        try:
            keyword=keyword.lower()
            if keyword in self.keyword_dict:
                if(tsp.cord != '' and tsp.cord != None):
                    obj_props = tsp.objectname.split(';')
                    coord = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                    ele = {'cord': tsp.cord, 'coordinates': coord}
                    if ( tsp.custom_flag ):
                        if (keyword.lower() == 'getstatusiris') : result = self.keyword_dict[keyword](ele, input, output, tsp.parent_xpath, tsp.objectname.split(';')[-2])
                        else : result = self.keyword_dict[keyword](ele, input, output, tsp.parent_xpath)
                    elif ( tsp.objectname.split(';')[-1] == 'constant' and keyword.lower() == 'verifyexistsiris' ):
                        result = self.keyword_dict[keyword](ele, input, output, 'constant')
                    else:
                        if (keyword.lower() == 'getstatusiris') : result = self.keyword_dict[keyword](ele, input, output, tsp.objectname.split(';')[-2])
                        else : result = self.keyword_dict[keyword](ele, input, output)
                elif keyword in ['findwindowandattach', 'waitforelementvisible','switchtoframe','getobjectforcustom','selectmenu']:
                    result = self.keyword_dict[keyword](*message)
                else:
                    configvalues = readconfig.configvalues
                    delay_constant = int(configvalues['element_load_timeout'])
                    oebs_object_indentification_order = "1"
                    if "oebs_object_indentification_order" in configvalues:
                        oebs_object_indentification_order = configvalues["oebs_object_indentification_order"]
                    if oebs_object_indentification_order == "1":
                        for _ in range(delay_constant):
                            log.info('Finding the OEBS element by XPATH')
                            accessContext, visible, active_parent =  self.utilities_obj.object_generator(*message)
                            if accessContext and str(accessContext) != 'fail':
                                if (keyword in self.required_on_top and active_parent) or (keyword not in self.required_on_top):
                                    if keyword in ['selectvaluebytext', 'selectvaluebyindex', 'setfocus']:
                                        result = self.keyword_dict[keyword](accessContext, {'top': message[6], 'left': message[7], 'width': message[8], 'height': message[9]})
                                    else:
                                        result = self.keyword_dict[keyword](accessContext)
                                else:
                                    err_msg = oebs_constants.ERROR_CODE_DICT['err_object_background']
                                break
                            else:
                                log.info('Finding the OEBS element by XPATH failed so finding the element by POSITION')
                                accessContext, visible, active_parent =  self.utilities_obj.object_generator_using_coordinates(*message)
                                if accessContext and str(accessContext) != 'fail':
                                    if (keyword in self.required_on_top and active_parent) or (keyword not in self.required_on_top):
                                        if keyword in ['selectvaluebytext', 'selectvaluebyindex', 'setfocus']:
                                            result = self.keyword_dict[keyword](accessContext, {'top': message[6], 'left': message[7], 'width': message[8], 'height': message[9]})
                                        else:
                                            result = self.keyword_dict[keyword](accessContext)
                                    else:
                                        err_msg = oebs_constants.ERROR_CODE_DICT['err_object_background']
                                    break
                                else:
                                    err_msg = oebs_constants.ERROR_CODE_DICT['err_finding_object']
                                    log.info(err_msg)
                                    time.sleep(1)
                    else:
                        for _ in range(delay_constant):
                            log.info('Finding the OEBS element by POSITION')
                            accessContext, visible, active_parent =  self.utilities_obj.object_generator_using_coordinates(*message)
                            if accessContext and str(accessContext) != 'fail':
                                if (keyword in self.required_on_top and active_parent) or (keyword not in self.required_on_top):
                                    if keyword in ['selectvaluebytext', 'selectvaluebyindex', 'setfocus']:
                                        result = self.keyword_dict[keyword](accessContext, {'top': message[6], 'left': message[7], 'width': message[8], 'height': message[9]})
                                    else:
                                        result = self.keyword_dict[keyword](accessContext)
                                else:
                                    err_msg = oebs_constants.ERROR_CODE_DICT['err_object_background']
                                break
                            else:
                                log.info('Finding the OEBS element by POSITION failed so finding the element by XPATH')
                                accessContext, visible, active_parent =  self.utilities_obj.object_generator(*message)
                                if accessContext and str(accessContext) != 'fail':
                                    if (keyword in self.required_on_top and active_parent) or (keyword not in self.required_on_top):
                                        if keyword in ['selectvaluebytext', 'selectvaluebyindex', 'setfocus']:
                                            result = self.keyword_dict[keyword](accessContext, {'top': message[6], 'left': message[7], 'width': message[8], 'height': message[9]})
                                        else:
                                            result = self.keyword_dict[keyword](accessContext)
                                    else:
                                        err_msg = oebs_constants.ERROR_CODE_DICT['err_object_background']
                                    break
                                else:
                                    err_msg = oebs_constants.ERROR_CODE_DICT['err_finding_object']
                                    log.info(err_msg)
                                    time.sleep(1)

                    log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
                if not result or len(result) <= 0: result = [constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
                if not(oebs_constants.ELEMENT_FOUND) and self.exception_flag:
                    result=constants.TERMINATE
            else:
                err_msg=constants.INVALID_KEYWORD
                result[3]=err_msg
            #capture screenshot feature has been implemented for OEBS
            screen_shot_obj = screenshot_keywords.Screenshot()
            configvalues = readconfig.configvalues
            if self.action == constants.EXECUTE:
                if result !=constants.TERMINATE:
                    result=list(result)
                    screen_details=mythread.json_data['suitedetails'][0]
                    if configvalues['screenShot_Flag'].lower() == 'fail':
                        if result[0].lower() == 'fail':
                            filepath = screen_shot_obj.captureScreenshot(screen_details)
                            result.append(filepath[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        filepath = screen_shot_obj.captureScreenshot(screen_details)
                        result.append(filepath[2])
        except TypeError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except RuntimeError as e:
            log.error(e)
            if e.args[0] == 'Result 0':
                logger.print_on_console('Element Not Found')
            else:
                log.debug('Exception at dispatcher')
        except Exception as e:
            log.error(e)
            log.debug('Exception at dispatcher')
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return result




