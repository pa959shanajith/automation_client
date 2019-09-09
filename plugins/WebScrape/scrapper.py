#-------------------------------------------------------------------------------
# Name:        scrapper.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     28-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import browserops
import fullscrape
import clickandadd
import highlight
import time
import logging
import logger

log = logging.getLogger('scrapper.py')

class Scrapper():
    def executor(data):
        if data == 'IE'  or  data == 'CH' or  data == 'FX':
            browser = browserops.BrowserOperations()
            res = browser.openBrowser(data)
            logger.print_on_console('Returned data from def openBrowser: ',res)
            if res == 'SUCCESS':
                logger.print_on_console('OPENBROWSER : *****Browser opened successfully, Please enter the URL to perform Scrape (Full Scrape/ClickAndAdd).*****\n\n\n')

        elif data == 'SCRAPE':
            scrape = fullscrape.Fullscrape()
            res = scrape.fullscrape()
            logger.print_on_console('Returned data from def fullscrape:',res)
            if res == 'SUCCESS':
                logger.print_on_console('FULL SCRAPE : *****Scraping completed successfully, Please check the domelements.json file.*****\n\n\n')
        elif  data == 'CLICKANDADD':
            click =clickandadd.Clickandadd()
            res = click.startclickandadd()
            logger.print_on_console('Returned data from def startclickandadd:',res)
            if res == 'SUCCESS':
                logger.print_on_console('CLICKANDADD : *****Select the element from AUT using mouse left click*****\n\n\n')
        elif data == 'STOPCLICKANDADD' :
            stop =clickandadd.Clickandadd()
            res = stop.stopclickandadd()
            logger.print_on_console('Returned data from def stopclickandadd:',res)
            if res == 'SUCCESS':
                logger.print_on_console('CLICKANDADD: ******Scraping completed successfully, Please check the domelements.json file.******\n\n\n')
        elif "HIGHLIGHT" in data :
            light =highlight.Highlight()
            res = light.highlight(data,None,None)
            logger.print_on_console('Returned data from def highlight:',res)
            if res == 'SUCCESS':
                logger.print_on_console('HIGHLIGHT: ******Element highlighted successfully.******')

