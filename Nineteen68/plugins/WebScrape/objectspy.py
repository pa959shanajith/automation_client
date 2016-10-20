#-------------------------------------------------------------------------------
# Name:        objectspy
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     28-09-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import json
import time

import browserops
import clickandadd
import highlight
import io
import logging

class Object_Mapper():

    def compare(self,browserType):
        a=browserops.BrowserOperations()
        a.openBrowser(browserType)
        time.sleep(10)
        find_ele=highlight.Highlight()

        with open('domelements_scraped.json') as data_file:
            self.data = json.load(data_file)

            for element  in self.data['view']:
                    updated_ele=find_ele.highlight('OBJECTMAPPER'+','+element['xpath']+','+element['url'],element)


            vie = {'view': highlight.lst}
            with open('domelements.json', 'w') as outfile:
                json.dump(vie, outfile, indent=4, sort_keys=False)



    def clickandadd(self):
        b=clickandadd.Clickandadd()
        b.startclickandadd()
        abc=raw_input("enter ok to stop click and add ")
        if abc=='ok':
            b.stopclickandadd()
        with open('domelements.json') as data_file:
            data = json.load(data_file)
            lst=self.data['view']
            for element  in data['view']:
                lst.append(element)
            vie = {'view': lst}
            with io.open('domelements.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(vie, ensure_ascii=False))




if __name__ == '__main__':
        print 'Inside main'
        logging.basicConfig(filename='python-scrappy.log', level=logging.DEBUG, format='%(asctime)s--Line No:%(lineno)d--%(message)s')
        logging.debug('==================OBJECT MAPPING UTILITY STARTED============================')
        logging.debug('---------------------------------------------------------------------------------------')
        a=Object_Mapper()
        a.compare('CH')
        a.clickandadd()

        print 'End of main'

