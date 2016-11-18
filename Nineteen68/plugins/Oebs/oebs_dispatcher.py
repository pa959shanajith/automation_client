#-------------------------------------------------------------------------------
# Name:        module1
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
import Exceptions
import oebs_constants
windowname=None


class OebsDispatcher:

    oebs_keywords=OebsKeywords()
    utils_obj=utils.Utils()
    scrape_obj=oebs_fullscrape.FullScrape()
    clickandadd_obj=oebsclickandadd.ClickAndAdd()

    def assign_url_objectname(self,tsp,input):
        message=[tsp.url,tsp.objectname,tsp.name,input,tsp.outputval]
        return message

    def dispatcher(self,tsp,input,*message):
         logger.log('Keyword is '+tsp.name)
         keyword=tsp.name

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
                return dict[keyword](*message)
            else:
                logger.log(generic_constants.INVALID_INPUT)
         except Exception as e:
            Exceptions.error(e)




