#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakshak.kamath
#
# Created:     13-06-2019
# Copyright:   (c) rakshak.kamath 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import core_utils
import logging
import wx
##import logger
log = logging.getLogger('userobjectscrape_MW.py')
update_data={}
class UserObject:
    def __init__(self):
        pass

    def get_user_object(self,d,socketIO):
        data={}
        if d['operation']=='encrypt':
            obj=core_utils.CoreUtils()
            data['url']= obj.scrape_wrap(d['url'])
            left_part=obj.scrape_wrap(d['apath']+";"+d["id"])
            right_part=obj.scrape_wrap(d["name"]+";"+d["tagname"]+";"+d["classname"]+"; ; ; ; ; ;"+d['selector'])
            data['xpath'] = left_part+';'+d["rpath"]+';'+right_part
            log.debug('data encrypt',data)
            socketIO.emit('scrape',data)
        elif d['operation']=='decrypt':
            obj=core_utils.CoreUtils()
            xpath_string=d['xpath'].split(';')
            if len(xpath_string) == 3:
                left_part=obj.scrape_unwrap(xpath_string[0])
                right_part=obj.scrape_unwrap(xpath_string[2])
            else:
                left_part = ';'.join(map(str,xpath_string[:2]))
                right_part = ';'.join(map(str,xpath_string[2:]))
            data['url']=obj.scrape_unwrap(d['url'])
            data['apath']=left_part.split(';')[0]
            data['rpath']=xpath_string[1]
            data['id']=left_part.split(';')[1]
            data['tag']=d['tag']
            data["name"]=right_part.split(';')[0]
            data["tagname"]=right_part.split(';')[1]
            data["classname"]=right_part.split(';')[2]
            data["selector"]=right_part.split(';')[8]
            log.debug('data decrypt',data)
            socketIO.emit('scrape',data)

    def update_scrape_object(self,url,objectname,obj_flag,stepnum,custname):
        data={}
        identifier=objectname.split(';')
        obj=core_utils.CoreUtils()
        left_part=obj.scrape_wrap(obj_flag+";"+identifier[1])
        right_part=obj.scrape_wrap(';'.join(identifier[3:]))
        data['url']= obj.scrape_wrap(url)
        data['xpath'] = left_part+';'+identifier[2]+';'+right_part
        for i in range(1,len(identifier)):
            obj_flag=obj_flag+';'+identifier[i]
        data[custname]=obj_flag
        update_data[str(stepnum)]=data
