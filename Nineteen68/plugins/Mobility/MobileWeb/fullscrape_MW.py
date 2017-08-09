#-------------------------------------------------------------------------------
# Name:        fullscrape_MW.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     28-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import browserops_MW
import platform
if platform.system() != "Darwin":
        import win32gui
        import win32con
import time
import json
import domconstants_MW
import logger
import Exceptions_MW
import logging.config
import logging
log = logging.getLogger('fullscrape_MW.py')
currenthandle = ''
status = domconstants_MW.STATUS_FAIL

class fullscrape_MW():
    def fullscrape_MW(self):
##        vie = {}
        data = {}
        try:
            log.info(' Inside fullscrape_MW method .....')
##            vie = {}
            driver = browserops_MW.driver
            hwndg = browserops_MW.hwndg
            log.info('Obtained browser handle and driver from browserops_MW.py class .....')
            if platform.system() != "Darwin":
                toolwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            log.info(' Minimizing the foreground window i.e tool and assuming AUT on top .....')
            time.sleep(2)
            if platform.system() != "Darwin":
                actwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            javascript_hasfocus = """return(document.hasFocus());"""
##            time.sleep(6)
            if platform.system()!="Darwin":
                for eachdriverhand in driver.window_handles:
                    log.info('Iterating through the number of windows open by the driver')
                    driver.switch_to.window(eachdriverhand)
                    log.info('Switching to each handle and checking weather it has focus ')
                    if (driver.execute_script(javascript_hasfocus)):
                            log.info('Got the window which has the focus')
                            global currenthandle
                            currenthandle = eachdriverhand
                            break
            javascript_scrape = """if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('*');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } if (!window.Element || !window.Element.prototype || !window.Element.prototype.getAttribute) {     (function() {         function getAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('*');         for (var i = 0; i < inputs.length; i++) {             inputs[i].getAttribute = getAttribute;         }     }()); }(function() {     if (!document.getElementsByClassName) {         var indexOf = [].indexOf || function(prop) {             for (var i = 0; i < this.length; i++) {                 if (this[i] === prop) return i;             }             return -1;         };         getElementsByClassName = function(className, context) {             var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function() {                 var all = context.getElementsByTagName("*"),                     elements = [],                     i = 0;                 for (; i < all.length; i++) {                     if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) elements.push(all[i]);                 }                 return elements;             })();             return elems;         };         document.getElementsByClassName = function(className) {             return getElementsByClassName(className, document);         };         if (window.Element) {             window.Element.prototype.getElementsByClassName = function(className) {                 return getElementsByClassName(className, this);             };         }     } })(); var suseIdx = true; var suseId = true; var suseClass = true; var srelative = true; var sae = []; var sarr = []; var sele = document.getElementsByTagName('*'); var smyid = 0; var stextvalue = ''; var stagname = 0; var sishidden = 0; var scustname = ''; var smultipleFlag = false; var surl = arguments[0]; var snonamecounter = 1; var txt_area_nonamecounter = 1; var select_nonamecounter = 1; var td_nonamecounter = 1; var a_nonamecounter = 1; var table_nonamecounter = 1; var input_nonamecounter = 1; var stagtype = ''; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var sclassname = 'null'; var top = 0; var left = 0; var height = 0; var width = 0; var coordinates = ''; var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); saddNodesOuter(sae, sele); for (var j = 0; j < sae.length; j++) {     stagtype = '';     ssname = 'null';     sstagname = 'null';     sid = sae[j].id;     sname = sae[j].name;     salttext = sae[j].alt;     splaceholder = sae[j].placeholder;     sclassname = sae[j].className;     sid = (String(sid));     sclassname = (String(sclassname));     sname = (String(sname));     splaceholder = (String(splaceholder));     stextvalue = stext_content(sae[j]);     stextvalue = (String(stextvalue));     stagname = sae[j].tagName.toLowerCase();     ssname = 'null';     sstagname = 'null';     ssclassname = 'null';     findCoordinates(sae[j]);     if (stagname.indexOf(':') != -1) {         stagname = stagname.replace(':', '');         stagname = 'custom' + stagname;     }     if (sname != '' && sname != 'undefined') {         snames = document.getElementsByName(sname);         if (snames.length > 1) {             for (var k = 0; k < snames.length; k++) {                 if (sae[j] == snames[k]) {                     ssname = sname + '[' + k + ']'                 }             }         } else {             ssname = sname;         }     }     if (stagname != '' && stagname != 'undefined') {         stagnames = document.getElementsByTagName(stagname);         if (stagnames.length > 1) {             for (var k = 0; k < stagnames.length; k++) {                 if (sae[j] == stagnames[k]) {                     sstagname = stagname + '[' + k + ']'                 }             }         } else {             sstagname = stagname;         }     }     if (sclassname != '' && sclassname != 'undefined') {         sclassnames = document.getElementsByClassName(sclassname);         if (sclassnames.length > 1) {             for (var k = 0; k < sclassnames.length; k++) {                 if (sae[j] == sclassnames[k]) {                     ssclassname = sclassname + '[' + k + ']'                 }             }         } else {             ssclassname = sclassname;         }     }     if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') {         if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') {             if (sname != '' && sname != 'undefined') {                 snames = document.getElementsByName(sname);                 if (snames.length > 1) {                     for (var k = 0; k < snames.length; k++) {                         if (sae[j] == snames[k]) {                             stextvalue = sname + k;                         }                     }                 } else {                     stextvalue = sname;                 }             } else if (sid != '' && sid != 'undefined') {                 stextvalue = sid;             } else if (splaceholder != '' && splaceholder != 'undefined') {                 stextvalue = splaceholder;             } else {                 switch (stagname) {                     case "textarea":                         stextvalue = stagname + '_NONAME' + txt_area_nonamecounter;                         txt_area_nonamecounter = txt_area_nonamecounter + 1;                         break;                     case "select":                         stextvalue = stagname + '_NONAME' + select_nonamecounter;                         select_nonamecounter = select_nonamecounter + 1;                         break;                     case "td":                         stextvalue = stagname + '_NONAME' + td_nonamecounter;                         td_nonamecounter = td_nonamecounter + 1;                         break;                     case "a":                         stextvalue = stagname + '_NONAME' + a_nonamecounter;                         a_nonamecounter = a_nonamecounter + 1;                         break;                     case "table":                         stextvalue = stagname + '_NONAME' + table_nonamecounter;                         table_nonamecounter = table_nonamecounter + 1;                         break;                     case "input":                         stextvalue = stagname + '_NONAME' + input_nonamecounter;                         input_nonamecounter = input_nonamecounter + 1;                         break;                     default:                         stextvalue = 'NONAME' + snonamecounter;                         snonamecounter = snonamecounter + 1;                 }             }         }         if (sid == '') {             sid = 'null';         }         smultipleFlag = sae[j].hasAttribute('multiple');         sishidden = sisVisible(sae[j]);         if (sishidden == true || sishidden == 'True' || sishidden == 'true') {             sishidden = 'No';         } else {             sishidden = 'Yes';         }         var sfirstpass = 0;         var srpath = '';         var setype = sae[j].getAttribute('type');         setype = (String(setype)).toLowerCase();         for (var spath = ''; sae[j] && sae[j].nodeType == 1; sae[j] = sae[j].parentNode) {             var spredicate = [];             var ssiblings = sae[j].parentNode.children;             var scount = 0;             var sunique = false;             var snewPath = '';             var sidx = 0;             for (var i = 0; ssiblings && (i < ssiblings.length); i++) {                 if (ssiblings[i].tagName == sae[j].tagName) {                     scount++;                     if (ssiblings[i] == sae[j]) {                         sidx = scount;                     }                 }             }             if (sidx == 1 && scount == 1) {                 sidx = null;             }             if (suseId && sae[j].id) {                 spredicate[spredicate.length] = '@id=' + '"' + sae[j].id + '"';                 sunique = true;             }             xidx = (suseIdx && sidx) ? ('[' + sidx + ']') : '';             sidx = (suseIdx && sidx && !sunique) ? ('[' + sidx + ']') : '';             spredicate = (spredicate.length > 0) ? ('[' + spredicate.join(' and ') + ']') : '';             spath = '/' + sae[j].tagName.toLowerCase() + xidx + spath;             if (sfirstpass == 0) {                 if (sunique && srelative) {                     srpath = '//*' + sidx + spredicate + srpath;                     sfirstpass = 1;                 } else {                     srpath = '/' + sae[j].tagName.toLowerCase() + sidx + spredicate + srpath;                 }             }         }         if (stagname == 'textarea') {             stagname = 'input';             stagtype = 'txtarea';         } else if (stagname == 'select' && smultipleFlag) {             stagname = 'list';             stagtype = 'lst';         } else if (stagname == 'select') {             stagtype = 'select';         } else if (stagname == 'td' || stagname == 'tr') {             stagname = 'tablecell';             stagtype = 'tblcell';         } else if (stagname == 'a') {             stagtype = 'lnk';         } else if (stagname == 'table') {             stagtype = 'tbl';         } else if (stagname == 'img') {             stagtype = 'img';         } else if (stagname == 'input' && setype == 'image') {             stagname = 'img';             stagtype = 'img';         }         if (stagname == 'input' && (setype == 'button' || setype == 'submit' || setype == 'reset' || setype == 'file')) {             stagname = 'button';             stagtype = 'btn';         } else if (stagname == 'input' && setype == 'radio') {             stagname = 'radiobutton';             stagtype = 'radiobtn';         } else if (stagname == 'input' && setype == 'checkbox') {             stagname = 'checkbox';             stagtype = 'chkbox';         } else if (stagname == 'input' && (setype == 'text' || setype == 'email' || setype == 'number' || setype == 'password' || setype == 'range' || setype == 'search' || setype == 'url')) {             stagname = 'input';             stagtype = 'txtbox';         }         stextvalue = stextvalue.replace(">", "");         stextvalue = stextvalue.replace("</", "");         stextvalue = stextvalue.replace("<", "");         stextvalue = stextvalue.replace("/>", "");         stextvalue = stextvalue.split("\\n").join("");         stextvalue = stextvalue.split("\\t").join("");         stextvalue = stextvalue.split("\\r").join("");         stextvalue = stextvalue.split("  ").join("");         stextvalue = stextvalue.split("\u00a0").join("");         if (stextvalue == '' || stextvalue.length == 0 || stextvalue == '0') {             stextvalue = 'NONAME' + snonamecounter;             snonamecounter = snonamecounter + 1;             scustname = stextvalue;         } else {             scustname = stextvalue;         }         if (stagtype != '') {             scustname = scustname + '_' + stagtype;         } else {             scustname = scustname + '_elmnt';         }         coordinates = left + ';' + top + ';' + height + ';' + width;         coordinates = String(coordinates);         snewPath = String(srpath) + ';' + String(sid) + ';' + String(spath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + stextvalue;         sarr.push({             'xpath': snewPath,             'tag': stagname,             'hiddentag': sishidden,             'url': surl,             'height': height,             'width': width,             'custname': scustname,             'top': top,             'left': left         });     } } return sarr;  function findCoordinates(element) {     height = element.offsetHeight;     width = element.offsetWidth;     top = 0;     left = 0;     do {         top += element.offsetTop || 0;         left += element.offsetLeft || 0;         element = element.offsetParent;     } while (element); }  function saddNodesOuter(sarray, scollection) {     for (var i = 0; scollection && scollection.length && i < scollection.length; i++) {         sarray.push(scollection[i]);     } };  function stext_content(f) {     var sfirstText = '';     var stextdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     return (stextdisplay); };"""
            tempne = []
            log.info('Performing the full scrape operation on default/outer page')
            tempreturn = driver.execute_script(javascript_scrape, driver.current_url)
            log.info('full scrape operation on default/outer page is done and data is obtained')
            tempne.extend(tempreturn)

            def switchtoframe_scrape1(mypath):
                log.info('Inside switchtoframe_scrape1 method')
                cond_flag = False
                log.info('Splitting Iframe/frame url by /')
                indiframes = mypath.split("/")
                if platform.system()!= "Darwin":
                    driver.switch_to.window(currenthandle)
                log.info(' Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = domconstants_MW.IFRAME
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'f':
                            frame_iframe = domconstants_MW.FRAME
                            log.info('switchtoframe_scrape1() , MSG: It is  frame')
                        else:
                            log.info('It is iframe')
                        try:
                            if (driver.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                                driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                                log.info('MSG: Switched to frame/iframe')
                                cond_flag = True
                            else:
                                cond_flag = False
                                break
                        except Exception as e:
                            cond_flag = False
                return cond_flag



            def callback_scrape1(myipath, tempne):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants_MW.IFRAME)))):
                    # check if it is really a valid iframe before performing any further actions!
    ##                            if (driver.find_elements_by_tag_name('iframe')[iframes]).is_displayed():
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' +  '/'
                    if switchtoframe_scrape1(path):
                        temp = driver.execute_script(javascript_scrape, path)
                        log.info('full scrape operation on iframe page is done and data is obtained')
                        tempne.extend(temp)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants_MW.FRAME)))):
                            inpath = path + str(frames) + 'f' +  '/'
                            if switchtoframe_scrape1(inpath):
                                itemp = driver.execute_script(javascript_scrape, inpath)
                                log.info('full scrape operation on frame page is done and data is obtained')
                                tempne.extend(itemp)
                            callback_scrape2(inpath, tempne)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants_MW.IFRAME)))):
                            inpath = path + str(frames) + 'i' +  '/'
                            if switchtoframe_scrape1(inpath):
                                itemp = driver.execute_script(javascript_scrape, inpath)
                                log.info('full scrape operation on frame page is done and data is obtained')
                                tempne.extend(itemp)
                            callback_scrape1(inpath, tempne)

                        callback_scrape1(path, tempne)

            def callback_scrape2(myipath, tempne):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants_MW.FRAME)))):
                    # check if it is really a valid iframe before performing any further actions!
    ##                            if (driver.find_elements_by_tag_name('iframe')[iframes]).is_displayed():
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'f' +  '/'
                    if switchtoframe_scrape1(path):
                        temp = driver.execute_script(javascript_scrape, path)
                        log.info('full scrape operation on frame page is done and data is obtained')
                        tempne.extend(temp)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants_MW.IFRAME)))):
                            inpath = path + str(frames) + 'i' +  '/'
                            if switchtoframe_scrape1(inpath):
                                itemp = driver.execute_script(javascript_scrape, inpath)
                                log.info('full scrape operation on iframe page is done and data is obtained')
                                tempne.extend(itemp)
                            callback_scrape1(inpath, tempne)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants_MW.FRAME)))):
                            inpath = path + str(frames) + 'f' +  '/'
                            if switchtoframe_scrape1(inpath):
                                itemp = driver.execute_script(javascript_scrape, inpath)
                                log.info(' full scrape operation on frame page is done and data is obtained')
                                tempne.extend(itemp)
                            callback_scrape2(inpath, tempne)
                        callback_scrape2(path, tempne)
            callback_scrape1('', tempne)
            log.info('full scrape operation on iframe/frame pages is completed')
            if platform.system()!= "Darwin":
                driver.switch_to.window(currenthandle)
            callback_scrape2('', tempne)
            log.info('full scrape operation on iframe/frame pages is completed')
            if platform.system() != "Darwin":
                driver.switch_to.window(currenthandle)
            tempne = json.dumps(tempne)
            tempne = json.loads(tempne)
            log.info('json opertions dumps and loads are performed on the return data')
##            win32gui.ShowWindow(hwndg, win32con.SW_MINIMIZE)
##            global vie
##            vie = {"view": tempne}
##            global data
##            data.append(vie)
            screen = driver.get_screenshot_as_base64()
            scrapedin = ''
            if browserops_MW.browser == 2:
                scrapedin = 'FX'
            elif browserops_MW.browser == 3:
                scrapedin =  'IE'
            elif browserops_MW.browser == 1:
                scrapedin =  'CH'
##            screenshot = {'mirror':screen}
##            scrapetype = {'scrapetype' : 'fs'}
##            data.append(scrapetype)
##            data.append(scrapedin)
##            data.append(screenshot)
            data['scrapetype'] = 'fs'
            data['scrapedin'] = scrapedin
            data['view'] = tempne
            data['mirror'] = screen
            data['mirrorwidth'] = driver.execute_script("return window.innerWidth")
            data['mirrorheight'] = driver.execute_script("return window.innerHeight")
            log.info('Creating a json object with key vie with value as return data')
            with open('domelements.json', 'w') as outfile:
                log.info('Opening domelements.json file to write vie object')
                json.dump(data, outfile, indent=4, sort_keys=False)
                log.info('vie is dumped into  domelements.json file ')
            outfile.close()
            log.info('domelements.json file closed ')
            if driver.current_url == domconstants_MW.BLANK_PAGE:
                log.info('url is blank so cannot perform full scrape operation ')
                status = domconstants_MW.STATUS_FAIL
                data = domconstants_MW.STATUS_FAIL
            else:
                status = domconstants_MW.STATUS_SUCCESS
##            log.info('FILE: fullscrape_MW.py , DEF: fullscrape_MW() , MSG: Maximizing the tool once full scrape is done ')
##            win32gui.ShowWindow(toolwindow, win32con.SW_MAXIMIZE)
        except Exception as e:
            status = domconstants_MW.STATUS_FAIL
            data = domconstants_MW.STATUS_FAIL
        return data

##    def save_json_data(self):
##        global vie
####        data = {'view' : vie}
##        data = []
##        driver = browserops_MW.driver
##        data.append(vie)
##        screen = driver.get_screenshot_as_base64()
##        screenshot = {'mirror':screen}
##        scrapetype = {'scrapetype' : 'fs'}
##        data.append(screenshot)
##        data.append(scrapetype)
##        with open('domelements.json', 'w') as outfile:
##                log.info('FILE: fullscrape_MW.py , DEF: save_json_data() , MSG: Opening domelements.json file to write vie object')
##                json.dump(data, outfile, indent=4, sort_keys=False)
##                log.info('FILE: fullscrape_MW.py , DEF: save_json_data() , MSG: vie is dumped into  domelements.json file ')
##        outfile.close()
##        return data

