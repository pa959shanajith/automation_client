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

from oebsServer import OebsKeywords
import oebs_fullscrape
import oebsclickandadd
import utils
import logger
import logging
import oebs_constants
windowname=None
import constants
import oebs_msg

log = logging.getLogger('oebs_dispatcher.py')

class OebsDispatcher:

    oebs_keywords=OebsKeywords()
    utils_obj=utils.Utils()
    scrape_obj=oebs_fullscrape.FullScrape()
    clickandadd_obj=oebsclickandadd.ClickAndAdd()

    def __init__(self):
        self.exception_flag=''


    custom_dict={
                    'getstatus': ['radio button','check box'],
                    'selectradiobutton': ['radio button'],
                    'selectcheckbox': ['check box'],
                    'unselectcheckbox': ['check box'],

                    'selectvaluebyindex':['combo box','list'],
                    'selectvaluebytext': ['combo box','list'],

                    'settext': ['text'],
                    'gettext': ['text']

                    }

    get_ele_type={
                    'radio': 'radio button',
                    'checkbox':'check box',
                    'dropdown':'combo box',
                    'listbox':'list',
                    'textbox':'text',
                    'button':'push button'
                    }
    custom_dict_element={'element':['clickelement','setfocus','doubleclick','rightclick','getelementtext','verifyelementtext','verifyexists', 'verifydoesnotexists', 'verifyreadonly','verifyhidden','verifyvisible','sendfunctionkeys','waitforelementvisible']}

    def clear_oebs_window_name(self):
        log.info('Clearing the window name')
        windowname=None

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
            if len(input)>=3:
                ele_type=input[0].lower()
                if ele_type in self.get_ele_type:
                    ele_type=self.get_ele_type[ele_type]
                if (keyword in self.custom_dict and ele_type in self.custom_dict[keyword]) or keyword in self.custom_dict_element.values()[0]:
                    custom_oebs_element=self.oebs_keywords.getobjectforcustom(windowname,parent_xpath,ele_type,input[2])
                    log.info('custom_oebs_element')
                    log.info(custom_oebs_element)
                    if custom_oebs_element != '':
                        input.reverse()
                        for x in range(0,3):
                            input.pop()
                        input.reverse()
                        objectname=custom_oebs_element
                    else:
                        self.print_error('ERR_CUSTOM_MISMATCH')

                else:
                    self.print_error('ERR_PRECONDITION_NOTMET')
                    self.print_error('ERR_CUSTOM_NOTFOUND')
            else:
                 self.print_error('ERR_REF_ELE_NULL')
                 self.print_error('ERR_CUSTOM_NOTFOUND')
        message=[tsp.url,objectname,tsp.name,input,tsp.outputval]
        return message

    def dispatcher(self,tsp,input,*message):
         logger.print_on_console('Keyword is '+tsp.name)
         keyword=tsp.name
         result=(constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE)
         if windowname is not None:
            self.utils_obj.set_to_foreground(windowname)
         message=self.assign_url_objectname(tsp,input)

         try:
            dict={'findwindowandattach':self.utils_obj.find_window_and_attach,
                  'getobjectforcustom' : self.oebs_keywords.getobjectforcustom,
                  'drop'    : self.oebs_keywords.drop,
                  'drag'     : self.oebs_keywords.drag,
                  'waitforelementvisible'  : self.oebs_keywords.waitforelementvisible,
                  'toggleminimize' : self.oebs_keywords.toggleminimize,
                  'togglemaximize'      : self.oebs_keywords.togglemaximize,
                  'closeframe'      : self.oebs_keywords.closeframe,
                  'switchtoframe':self.oebs_keywords.switchtoframe,

                  'down':self.oebs_keywords.down,
                  'up' : self.oebs_keywords.up,
                  'left' : self.oebs_keywords.left,
                  'right':self.oebs_keywords.right,

                  'cellclick' : self.oebs_keywords.cellclick,
                  'verifycellvalue' : self.oebs_keywords.verifycellvalue,
                  'getcellvalue': self.oebs_keywords.getcellvalue,
                  'getcolumncount' : self.oebs_keywords.getcolumncount,
                  'getrowcount'    : self.oebs_keywords.getrowcount,

                  'verifyelementtext' : self.oebs_keywords.verifyelementtext,
                  'getelementtext'  : self.oebs_keywords.getelementtext,
                  'clickelement':self.oebs_keywords.clickelement,

                  'selectmultiplevaluesbytext':self.oebs_keywords.selectmultiplevaluesbytext,
                  'selectvaluebyindex':self.oebs_keywords.selectvaluebyindex,
                  'getvaluebyindex':self.oebs_keywords.getvaluebyindex,
                  'deselectall':self.oebs_keywords.deselectall,
                  'getmultiplevaluesbyindexes':self.oebs_keywords.getmultiplevaluesbyindexes,
                  'verifyselectedvalues':self.oebs_keywords.verifyselectedvalues,
                  'verifyselectedvalue':self.oebs_keywords.verifyselectedvalue,
                  'verifyvaluesexists':self.oebs_keywords.verifyvaluesexists,
                  'verifyallvalues':self.oebs_keywords.verifyallvalues,
                  'verifycount':self.oebs_keywords.verifycount,
                  'getcount':self.oebs_keywords.getcount,
                  'selectmultiplevaluesbyindexes':self.oebs_keywords.selectmultiplevaluesbyindexes,
                  'selectvaluebytext':self.oebs_keywords.selectvaluebytext,
                  'selectallvalues':self.oebs_keywords.selectallvalues,

                  'getselected':self.oebs_keywords.getselected,
                  'getstatus':self.oebs_keywords.getstatus,
                  'unselectcheckbox':self.oebs_keywords.unselectcheckbox,
                  'selectcheckbox':self.oebs_keywords.selectcheckbox,
                  'selectradiobutton':self.oebs_keywords.selectradiobutton,

                  'verifylinktext':self.oebs_keywords.verifylinktext,
                  'getlinktext':self.oebs_keywords.getlinktext,
                  'doubleclick':self.oebs_keywords.doubleclick,
                  'click':self.oebs_keywords.click,
                  'verifybuttonname':self.oebs_keywords.verifybuttonname,
                  'getbuttonname':self.oebs_keywords.getbuttonname,

                  'sendfunctionkeys':self.oebs_keywords.sendfunctionkeys,
                  'rightclick':self.oebs_keywords.rightclick,
                  'verifydoesnotexists':self.oebs_keywords.verifydoesnotexists,
                  'verifyexists':self.oebs_keywords.verifyexists,
                  'gettooltiptext':self.oebs_keywords.gettooltiptext,
                  'verifytooltiptext':self.oebs_keywords.verifytooltiptext,
                  'verifyreadonly':self.oebs_keywords.verifyreadonly,
                  'verifyhidden':self.oebs_keywords.verifyhidden,
                  'verifyvisible':self.oebs_keywords.verifyvisible,
                  'verifydisabled':self.oebs_keywords.verifydisabled,
                  'verifyenabled':self.oebs_keywords.verifyenabled,
                  'setfocus':self.oebs_keywords.setfocus,

                  'cleartext':self.oebs_keywords.cleartext,
                  'verifytext':self.oebs_keywords.verifytext,
                  'verifytextboxlength':self.oebs_keywords.verifytextboxlength,
                  'gettextboxlength':self.oebs_keywords.gettextboxlength,
                  'settext':self.oebs_keywords.settext,
                  'gettext':self.oebs_keywords.gettext,
                  'closeapplictaion':''

                }
            keyword=keyword.lower()
            if keyword in dict.keys():
                result=dict[keyword](*message)
                if not(oebs_msg.ELEMENT_FOUND) and self.exception_flag:
                    result=constants.TERMINATE
            else:
                logger.print_on_console(generic_constants.INVALID_INPUT)
         except Exception as e:
            log.error(e)
            logger.print_on_console(e)
         return result




