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
import objectmapper
import io
class Object_Mapper():

    def compare(self):
        a=browserops.BrowserOperations()
        a.openBrowser('CH')
        time.sleep(10)
        find_ele=objectmapper.Highlight()

        with open('domelements_scraped.json') as data_file:
            self.data = json.load(data_file)
            lst=[]
            for element  in self.data['view']:
                    updated_ele=find_ele.find_element(element['xpath']+','+element['url'],element)
                    lst.append(updated_ele)
            vie = {'view': lst}
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



a=Object_Mapper()
a.compare()
a.clickandadd()

