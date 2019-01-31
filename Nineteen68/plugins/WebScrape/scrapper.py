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

    if __name__ == '__main__':
        logger.print_on_console('==================OBJECT IDENTIFICATION UTILITY STARTED============================')
        logger.print_on_console('---------------------------------------------------------------------------------------')
        logging.basicConfig(filename='python-scrappy.log', level=logging.DEBUG, format='%(asctime)s--Line No:%(lineno)d--%(message)s')
        logging.debug('==================OBJECT IDENTIFICATION UTILITY STARTED============================')
        logging.debug('---------------------------------------------------------------------------------------')
        browser=input("""Enter the browser name to  open : IE - Internet Explorer, CH - Google Chrome, FX - Mozilla Firefox""")
        if browser == 'IE' or browser == 'CH' or browser == 'FX':
            executor(browser)
        else:
            logger.print_on_console('Please select the valid browser name')
        while True:
            start=input("""enter START to perform start click and add :  """)
            if start=='START':
                executor('CLICKANDADD')
            stop=input("""Enter STOP to stop click and add """)
            if stop=='STOP':
                executor('STOPCLICKANDADD')
        logger.print_on_console('==================OBJECT IDENTIFICATION UTILITY STOPPED============================')
        logger.print_on_console('---------------------------------------------------------------------------------------')
        logging.debug('==================OBJECT IDENTIFICATION UTILITY STOPPED============================')
        logging.debug('---------------------------------------------------------------------------------------')

