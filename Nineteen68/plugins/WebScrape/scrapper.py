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
            print 'Returned data from def openBrowser: ',res
            if res == 'SUCCESS':
                print 'OPENBROWSER : *****Browser opened successfully, Please enter the URL to perform Scrape (Full Scrape/ClickAndAdd).*****\n\n\n'

        elif data == 'SCRAPE':
            scrape = fullscrape.Fullscrape()
            res = scrape.fullscrape()
            print 'Returned data from def fullscrape:',res
            if res == 'SUCCESS':
                print 'FULL SCRAPE : *****Scraping completed successfully, Please check the domelements.json file.*****\n\n\n'
        elif  data == 'CLICKANDADD':
            click =clickandadd.Clickandadd()
            res = click.startclickandadd()
            print 'Returned data from def startclickandadd:',res
            if res == 'SUCCESS':
                print 'CLICKANDADD : *****Select the element from AUT using mouse left click*****\n\n\n'
        elif data == 'STOPCLICKANDADD' :
            stop =clickandadd.Clickandadd()
            res = stop.stopclickandadd()
            print 'Returned data from def stopclickandadd:',res
            if res == 'SUCCESS':
                print 'CLICKANDADD: ******Scraping completed successfully, Please check the domelements.json file.******\n\n\n'
        elif "HIGHLIGHT" in data :
            light =highlight.Highlight()
            res = light.highlight(data,None,None)
            print 'Returned data from def highlight:',res
            if res == 'SUCCESS':
                print 'HIGHLIGHT: ******Element highlighted successfully.******'

    if __name__ == '__main__':
        print '==================OBJECT IDENTIFICATION UTILITY STARTED============================'
        print('---------------------------------------------------------------------------------------')
        logging.basicConfig(filename='python-scrappy.log', level=logging.DEBUG, format='%(asctime)s--Line No:%(lineno)d--%(message)s')
        logging.debug('==================OBJECT IDENTIFICATION UTILITY STARTED============================')
        logging.debug('---------------------------------------------------------------------------------------')
        browser=raw_input("""Enter the browser name to  open : IE - Internet Explorer, CH - Google Chrome, FX - Mozilla Firefox""")
        if browser == 'IE' or browser == 'CH' or browser == 'FX':
            executor(browser)
        else:
            print 'Please select the valid browser name'
        while True:
            start=raw_input("""enter START to perform start click and add :  """)
            if start=='START':
                executor('CLICKANDADD')
            stop=raw_input("""Enter STOP to stop click and add """)
            if stop=='STOP':
                executor('STOPCLICKANDADD')
##        while True:
##            fullscrape=raw_input("""Enter SCRAPE to perform full scraping :  """)
##            if fullscrape=='SCRAPE':
##                executor('SCRAPE')
##        highlight=raw_input("""Enter HIGHLIGHT to perform full scraping :  """)
##        if highlight=='HIGHLIGHT':
##            executor("""HIGHLIGHT,//*[@id="ctl00_LeftContent_SparNavigationDMS1_txtSearchButton"];ctl00_LeftContent_SparNavigationDMS1_txtSearchButton;/html/body/form/div[3]/div/div[2]/div[1]/div/div[1]/div/div/div[1]/div/table/tbody/tr/td[1]/input[1];ctl00$LeftContent$SparNavigationDMS1$txtSearchButton;input[19];SearchTbox,https://converge/Home.aspx""")
        print('==================OBJECT IDENTIFICATION UTILITY STOPPED============================')
        print('---------------------------------------------------------------------------------------')
        logging.debug('==================OBJECT IDENTIFICATION UTILITY STOPPED============================')
        logging.debug('---------------------------------------------------------------------------------------')

