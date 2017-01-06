#-------------------------------------------------------------------------------
# Name:        scrape_dispatcher.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     15-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import utils
import oebs_fullscrape
import oebsclickandadd
import logger
import logging
import oebs_constants

log = logging.getLogger('scrape_dispatcher.py')

class ScrapeDispatcher:

    def __init__(self):
        self.utils_obj=utils.Utils()
        self.scrape_obj=oebs_fullscrape.FullScrape()
        self.clickandadd_obj=oebsclickandadd.ClickAndAdd()

    def scrape_dispatcher(self,keyword,*message):
             logger.print_on_console('Keyword is '+keyword)


             if keyword in oebs_constants.OEBS_SCRAPE_KEYWORDS:
                self.utils_obj.find_oebswindow_and_attach(message[0])
                if len(message)>1 and not(message[1].lower()=='stopclickandadd'):
                    self.utils_obj.set_to_foreground(message[0])

             try:
                dict={
                      'highlight':self.utils_obj.higlight,
                      'fullscrape': self.scrape_obj.getentireobjectlist,
                      'clickandadd':self.clickandadd_obj.clickandadd,
                    }
                keyword=keyword.lower()
                if keyword in dict.keys():
                    return dict[keyword](*message)
                else:
                    logger.print_on_console(oebs_constants.INVALID_INPUT)
             except Exception as e:
                log.error(e)
                logger.print_on_console(e)