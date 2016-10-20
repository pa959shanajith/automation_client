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

        elif data == 'SCRAPE':
            scrape = fullscrape.Fullscrape()
            res, dat = scrape.fullscrape()
            print 'Returned data from def fullscrape:',res , 'Data :',dat
        elif  data == 'CLICKANDADD':
            click =clickandadd.Clickandadd()
            res = click.startclickandadd()
            print 'Returned data from def startclickandadd:',res
        elif data == 'STOPCLICKANDADD' :
            stop =clickandadd.Clickandadd()
            res = stop.stopclickandadd()
            print 'Returned data from def stopclickandadd:',res
        elif "HIGHLIGHT" in data :
            light =highlight.Highlight()
            res = light.highlight(data,None)
            print 'Returned data from def highlight:',res

    if __name__ == '__main__':
        print 'Inside main'
        logging.basicConfig(filename='python-scrappy.log', level=logging.DEBUG, format='%(asctime)s--Line No:%(lineno)d--%(message)s')
        logging.debug('==================OBJECT IDENTIFICATION UTILITY STARTED============================')
        logging.debug('---------------------------------------------------------------------------------------')
        executor('FX')
        time.sleep(15)
        executor('CLICKANDADD')
        abc=raw_input("enter ok to stop click and add ")
        if abc=='ok':
            executor('STOPCLICKANDADD')
##
##        print 'End of main'

##        executor('SCRAPE')
##        time.sleep(5)
##        executor("""HIGHLIGHT,//*[@id="ctl00_LeftContent_SparNavigationDMS1_txtSearchButton"];ctl00_LeftContent_SparNavigationDMS1_txtSearchButton;/html/body/form/div[3]/div/div[2]/div[1]/div/div[1]/div/div/div[1]/div/table/tbody/tr/td[1]/input[1];ctl00$LeftContent$SparNavigationDMS1$txtSearchButton;input[19];SearchTbox,https://converge/Home.aspx""")
        print 'End of main'


