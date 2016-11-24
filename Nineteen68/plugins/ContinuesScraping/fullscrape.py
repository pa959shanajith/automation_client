#-------------------------------------------------------------------------------
# Name:        fullscrape.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     28-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import browserops
import win32gui
import win32con
import time
import json
import domconstants
import logger
import Exceptions

currenthandle = ''
vie = []
##screenindex = 0
status = domconstants.STATUS_FAIL
class Fullscrape():
    def fullscrape(self,screenname,depscreens):
        try:
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Inside fullscrape method .....')
##            vie = {}
            driver = browserops.driver
            hwndg = browserops.hwndg
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Obtained browser handle and driver from browserops.py class .....')
            toolwindow = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Minimizing the foreground window i.e tool and assuming AUT on top .....')
            time.sleep(2)
            actwindow = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            javascript_hasfocus = """return(document.hasFocus());"""
            time.sleep(6)
            for eachdriverhand in driver.window_handles:
                logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Iterating through the number of windows open by the driver')
                driver.switch_to.window(eachdriverhand)
                logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Switching to each handle and checking weather it has focus ')
                if (driver.execute_script(javascript_hasfocus)):
                    logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Got the window which has the focus')
                    global currenthandle
                    currenthandle = eachdriverhand
                    break
            javascript_scrape = """if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('*');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } if (!window.Element || !window.Element.prototype || !window.Element.prototype.getAttribute) {     (function() {         function getAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('*');         for (var i = 0; i < inputs.length; i++) {             inputs[i].getAttribute = getAttribute;         }     }()); }  (function() { if (!document.getElementsByClassName) {     var indexOf = [].indexOf || function(prop) {         for (var i = 0; i < this.length; i++) {             if (this[i] === prop) return i;         }         return -1;     };     getElementsByClassName = function(className, context) {         var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function() {             var all = context.getElementsByTagName("*"),                 elements = [],                 i = 0;             for (; i < all.length; i++) {                 if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) elements.push(all[i]);             }             return elements;         })();         return elems;     };     document.getElementsByClassName = function(className) {         return getElementsByClassName(className, document);     };      if(window.Element) {         window.Element.prototype.getElementsByClassName = function(className) {             return getElementsByClassName(className, this);         };     } } })(); var suseIdx = true; var suseId = true; var suseClass = true; var srelative = true; var sae = []; var sarr = []; var sele = document.getElementsByTagName('*'); var smyid = 0; var stextvalue = ''; var stagname = 0; var sishidden = 0; var surl = arguments[0]; var scustname = ''; var smultipleFlag = false; var snonamecounter = 1; var stagtype = ''; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var sclassname = 'null'; var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); saddNodesOuter(sae, sele); for (var j = 0; j < sae.length; j++) {     stagtype = ''; 	ssname = 'null'; 	sstagname = 'null';     sid = sae[j].id;     sname = sae[j].name;     salttext = sae[j].alt;     splaceholder = sae[j].placeholder; 	sclassname = sae[j].className;     sid = (String(sid)); 	sclassname = (String(sclassname));     sname = (String(sname));     splaceholder = (String(splaceholder));     stextvalue = stext_content(sae[j]);     stextvalue = (String(stextvalue));     stagname = sae[j].tagName.toLowerCase(); 	ssname = 'null'; 	sstagname = 'null'; 	ssclassname = 'null';     if (stagname.indexOf(':') != -1) {         stagname = stagname.replace(':', '');         stagname = 'custom' + stagname;     } 	if (sname != '' && sname != 'undefined') { 	snames = document.getElementsByName(sname);     if (snames.length > 1) {         for (var k = 0; k < snames.length; k++) {             if (sae[j] == snames[k]) { 				ssname = sname + '[' + k + ']'             }         }     } else { 		ssname = sname;     } 	} 	 	if (stagname != '' && stagname != 'undefined') {	 	stagnames = document.getElementsByTagName(stagname);     if (stagnames.length > 1) {         for (var k = 0; k < stagnames.length; k++) {             if (sae[j] == stagnames[k]) { 				sstagname = stagname + '[' + k + ']'             }         }     } else { 		sstagname = stagname;     } 	} 	if (sclassname != '' && sclassname != 'undefined') {	 	sclassnames = document.getElementsByClassName(sclassname);     if (sclassnames.length > 1) {         for (var k = 0; k < sclassnames.length; k++) {             if (sae[j] == sclassnames[k]) { 				ssclassname = sclassname + '[' + k + ']'             }         }     } else { 		ssclassname = sclassname;     } 	}     if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'br' && stagname != 'animatetransform') {         if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') {             if (sname != '' && sname != 'undefined') {                 snames = document.getElementsByName(sname);                 if (snames.length > 1) {                     for (var k = 0; k < snames.length; k++) {                         if (sae[j] == snames[k]) {                             stextvalue = sname + k;                         }                     }                 } else {                     stextvalue = sname;                 }             } else if (sid != '' && sid != 'undefined') {                 stextvalue = sid;             } else if (splaceholder != '' && splaceholder != 'undefined') {                 stextvalue = splaceholder;             }else {                 stextvalue = 'NONAME' + snonamecounter;                 snonamecounter = snonamecounter + 1;             }         }         if (sid == '') {             sid = 'null';         } 		 		         smultipleFlag = sae[j].hasAttribute('multiple');         sishidden = sisVisible(sae[j]);         if (sishidden == true || sishidden == 'True' || sishidden == 'true') {             sishidden = 'No';         } else {             sishidden = 'Yes';         }         var sfirstpass = 0;         var srpath = '';         var setype = sae[j].getAttribute('type');         setype = (String(setype)).toLowerCase();         for (var spath = ''; sae[j] && sae[j].nodeType == 1; sae[j] = sae[j].parentNode) {             var spredicate = [];             var ssiblings = sae[j].parentNode.children;             var scount = 0;             var sunique = false;             var snewPath = '';             var sidx = 0;             for (var i = 0; ssiblings && (i < ssiblings.length); i++) {                 if (ssiblings[i].tagName == sae[j].tagName) {                     scount++;                     if (ssiblings[i] == sae[j]) {                         sidx = scount;                     }                 }             }             if (sidx == 1 && scount == 1) {                 sidx = null;             }             if (suseId && sae[j].id) {                 spredicate[spredicate.length] = '@id=' + '"' + sae[j].id + '"';                 sunique = true;             }             xidx = (suseIdx && sidx) ? ('[' + sidx + ']') : '';             sidx = (suseIdx && sidx && !sunique) ? ('[' + sidx + ']') : '';             spredicate = (spredicate.length > 0) ? ('[' + spredicate.join(' and ') + ']') : '';             spath = '/' + sae[j].tagName.toLowerCase() + xidx + spath;             if (sfirstpass == 0) {                 if (sunique && srelative) {                     srpath = '//*' + sidx + spredicate + srpath;                     sfirstpass = 1;                 } else {                     srpath = '/' + sae[j].tagName.toLowerCase() + sidx + spredicate + srpath;                 }             }         }         if (stagname == 'textarea') {             stagname = 'input';             stagtype = 'txtarea';         } else if (stagname == 'select' && smultipleFlag) {             stagname = 'list';             stagtype = 'lst';         } else if (stagname == 'select') {             stagtype = 'select';         } else if (stagname == 'td' || stagname == 'tr') {             stagname = 'tablecell';             stagtype = 'tblcell';         } else if (stagname == 'a') {             stagtype = 'lnk';         } else if (stagname == 'table') {             stagtype = 'tbl';         } else if (stagname == 'img') {             stagtype = 'img';         } else if (stagname == 'input' && setype == 'image') {             stagname = 'img';             stagtype = 'img';         }         if (stagname == 'input' && (setype == 'button' || setype == 'submit' || setype == 'reset' || setype == 'file')) {             stagname = 'button';             stagtype = 'btn';         } else if (stagname == 'input' && setype == 'radio') {             stagname = 'radiobutton';             stagtype = 'radiobtn';         } else if (stagname == 'input' && setype == 'checkbox') {             stagname = 'checkbox';             stagtype = 'chkbox';         } else if (stagname == 'input' && (setype == 'text' || setype == 'email' || setype == 'number' || setype == 'password' || setype == 'range' || setype == 'search' || setype == 'url')) {             stagname = 'input';             stagtype = 'txtbox';         }         snewPath = String(srpath) + ';' + String(sid) + ';' + String(spath) + ';' + ssname + ';' + sstagname + ';' + ssclassname;         stextvalue = stextvalue.replace(">", "");         stextvalue = stextvalue.replace("</", "");         stextvalue = stextvalue.replace("<", "");         stextvalue = stextvalue.replace("/>", "");         if (stextvalue == '' || stextvalue.length == 0 || stextvalue == '0') {             stextvalue = 'NONAME' + snonamecounter;             snonamecounter = snonamecounter + 1;             scustname = stextvalue;         } else {             scustname = stextvalue;         }         if (stagtype != '') {             scustname = scustname + '_' + stagtype;         } else {             scustname = scustname + '_elmnt';         }         sarr.push({             'xpath': snewPath,             'url': surl,                          'hiddentag': sishidden,             'custname': scustname,             'tag': stagname         });     } } return sarr;  function saddNodesOuter(sarray, scollection) {     for (var i = 0; scollection && scollection.length && i < scollection.length; i++) {         sarray.push(scollection[i]);     } };  function stext_content(f) {     var sfirstText = '';     var stextdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     return (stextdisplay); };"""
            tempne = []
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Performing the full scrape operation on default/outer page')
            tempreturn = driver.execute_script(javascript_scrape, driver.current_url)
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: full scrape operation on default/outer page is done and data is obtained')
            tempne.extend(tempreturn)

            def switchtoframe_scrape1(mypath):
                logger.log('FILE: fullscrape.py , DEF: switchtoframe_scrape1() , MSG: Inside switchtoframe_scrape1 method')
                cond_flag = False
                logger.log('FILE: fullscrape.py , DEF: switchtoframe_scrape1() , MSG: Splitting Iframe/frame url by /')
                indiframes = mypath.split("/")
                driver.switch_to.window(currenthandle)
                logger.log('FILE: fullscrape.py , DEF: switchtoframe_scrape1() , MSG: Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = domconstants.IFRAME
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'f':
                            frame_iframe = domconstants.FRAME
                            logger.log('FILE: fullscrape.py , DEF: switchtoframe_scrape1() , MSG: It is  frame')
                        else:
                            logger.log('FILE: fullscrape.py , DEF: switchtoframe_scrape1() , MSG: It is iframe')
                        try:
                            if (driver.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                                driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                                logger.log('FILE: fullscrape.py , DEF: switchtoframe_scrape1() , MSG: Switched to frame/iframe')
                                cond_flag = True
                            else:
                                cond_flag = False
                                break
                        except Exception as e:
                            Exceptions.error(e)
                            cond_flag = False
                return cond_flag



            def callback_scrape1(myipath, tempne):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    # check if it is really a valid iframe before performing any further actions!
    ##                            if (driver.find_elements_by_tag_name('iframe')[iframes]).is_displayed():
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' +  '/'
                    if switchtoframe_scrape1(path):
                        temp = driver.execute_script(javascript_scrape, path)
                        logger.log('FILE: fullscrape.py , DEF: callback_scrape1() , MSG: full scrape operation on iframe page is done and data is obtained')
                        tempne.extend(temp)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            path = path + str(frames) + 'f' +  '/'
                            if switchtoframe_scrape1(path):
                                itemp = driver.execute_script(javascript_scrape, path)
                                logger.log('FILE: fullscrape.py , DEF: callback_scrape1() , MSG: full scrape operation on frame page is done and data is obtained')
                                tempne.extend(itemp)

                        callback_scrape1(path, tempne)

            def callback_scrape2(myipath, tempne):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    # check if it is really a valid iframe before performing any further actions!
    ##                            if (driver.find_elements_by_tag_name('iframe')[iframes]).is_displayed():
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'f' +  '/'
                    if switchtoframe_scrape1(path):
                        temp = driver.execute_script(javascript_scrape, path)
                        logger.log('FILE: fullscrape.py , DEF: callback_scrape2() , MSG: full scrape operation on frame page is done and data is obtained')
                        tempne.extend(temp)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            path = path + str(frames) + 'i' +  '/'
                            if switchtoframe_scrape1(path):
                                itemp = driver.execute_script(javascript_scrape, path)
                                logger.log('FILE: fullscrape.py , DEF: callback_scrape2() , MSG: full scrape operation on iframe page is done and data is obtained')
                                tempne.extend(itemp)
                        callback_scrape2(path, tempne)
            callback_scrape1('', tempne)
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: full scrape operation on iframe/frame pages is completed')
            driver.switch_to.window(currenthandle)
            callback_scrape2('', tempne)
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: full scrape operation on iframe/frame pages is completed')
            driver.switch_to.window(currenthandle)
            tempne = json.dumps(tempne)
            tempne = json.loads(tempne)
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: json opertions dumps and loads are performed on the return data')
            win32gui.ShowWindow(hwndg, win32con.SW_MINIMIZE)
##            global screenindex
##            screenname = 'screen' + str(screenindex)
##            screenindex = screenindex + 1
            v = []
            v.append({'data':tempne})
            v.append({'dependent':depscreens})


            global vie
            vie.append({screenname: v})
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Creating a json object with key vie with value as return data')
##            with open('domelements.json', 'w') as outfile:
##                logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Opening domelements.json file to write vie object')
##                json.dump(vie, outfile, indent=4, sort_keys=False)
##                logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: vie is dumped into  domelements.json file ')
##            outfile.close()
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: domelements.json file closed ')
            if driver.current_url == domconstants.BLANK_PAGE:
                logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: url is blank so cannot perform full scrape operation ')
                status = domconstants.STATUS_FAIL
            else:
                status = domconstants.STATUS_SUCCESS
            logger.log('FILE: fullscrape.py , DEF: fullscrape() , MSG: Maximizing the tool once full scrape is done ')
            win32gui.ShowWindow(toolwindow, win32con.SW_MAXIMIZE)
        except Exception as e:
            status = domconstants.STATUS_FAIL
            Exceptions.error(e)
        return status

    def startclickandadd(self):
        try:
            logger.log('FILE: clickandadd.py , DEF: startclickandadd() , MSG: Inside startclickandadd method .....')
            driver = browserops.driver
            browser = browserops.browser
            logger.log('FILE: clickandadd.py , DEF: startclickandadd() , MSG: Obtained browser handle and driver from browserops.py class .....')
            toolwindow = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            actwindow = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            logger.log('FILE: clickandadd.py , DEF: startclickandadd()  , MSG: Minimizing the foreground window i.e tool and assuming AUT on top .....')
            javascript_hasfocus = """return(document.hasFocus());"""
            time.sleep(6)
            for eachdriverhand in driver.window_handles:
                logger.log('FILE: clickandadd.py , DEF: startclickandadd() , MSG: Iterating through the number of windows open by the driver')
                driver.switch_to.window(eachdriverhand)
                logger.log('FILE: clickandadd.py , DEF: startclickandadd() , MSG: Switching to each handle and checking weather it has focus ')
                if (driver.execute_script(javascript_hasfocus)):
                    logger.log('FILE: clickandadd.py , DEF: startclickandadd() , MSG: Got the window which has the focus')
                    global currenthandle
                    currenthandle = eachdriverhand
                    break
            javascript_clicknadd = """if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('select');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); }(function() {     if (!document.getElementsByClassName) {         var indexOf = [].indexOf || function(prop) {             for (var i = 0; i < this.length; i++) {                 if (this[i] === prop) return i;             }             return -1;         };         getElementsByClassName = function(className, context) {             var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function() {                 var all = context.getElementsByTagName("*"),                     elements = [],                     i = 0;                 for (; i < all.length; i++) {                     if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) elements.push(all[i]);                 }                 return elements;             })();             return elems;         };         document.getElementsByClassName = function(className) {             return getElementsByClassName(className, document);         };         if (window.Element) {             window.Element.prototype.getElementsByClassName = function(className) {                 return getElementsByClassName(className, this);             };         }     } })(); var useIdx = true; var useId = true; var useClass = true; var relative = true; var ae = []; var be = []; var url = arguments[0]; var browser = arguments[1]; var ishidden = 0; var tagname = 0; var textvalue = ''; var arr = []; var custname = ''; var tagtype = ''; var multipleFlag = false; var uniqueFlag = false; var nonamecounter = 1; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var isIE = /*@cc_on!@*/ false || !!document.documentMode; var isVisible = (function() {     function inside(child, parent) {         while (child) {             if (child === parent) return true;             child = child.parentNode;         }         return false;     };     return function(elem) {         if (document.hidden || elem.offsetWidth == 0 || elem.offsetHeight == 0 || elem.style.visibility == 'hidden' || elem.style.display == 'none' || elem.style.opacity === 0) return false;         var rect = elem.getBoundingClientRect();         if (window.getComputedStyle || elem.currentStyle) {             var el = elem,                 comp = null;             while (el) {                 if (el === document) {                     break;                 } else if (!el.parentNode) return false;                 comp = window.getComputedStyle ? window.getComputedStyle(el, null) : el.currentStyle;                 if (comp && (comp.visibility == 'hidden' || comp.display == 'none' || (typeof comp.opacity !== 'undefined' && !(comp.opacity > 0)))) return false;                 el = el.parentNode;             }         }         return true;     } })(); localStorage.setItem('tastopflag', 'false'); addNodesOuter(ae, document.getElementsByTagName('*')); var css = 'table:hover{border:6px solid !important}',     head = document.head || document.getElementsByTagName('head')[0],     style = document.createElement('style'); style.type = 'text/css'; style.id = 'SLKNineteen68_Table'; if (style.styleSheet) {     style.styleSheet.cssText = css; } else {     style.appendChild(document.createTextNode(css)); } head.appendChild(style);  function handler(event) {     tagtype = '';     if (localStorage.getItem('tastopflag') == 'true') {         if (window.Prototype) {             var _arr_tojson = Array.prototype.toJSON;             delete Array.prototype.toJSON;             window.tasarr = arr;             Array.prototype.toJSON = _arr_tojson;         } else {             window.tasarr = arr;         }         clickStop(ae, isIE, be);          function clickStop(ae, isIE, be) {             if (isIE) {                 for (var i = 0; i < ae.length; i++) {                     if (ae[i].removeEventListener) {                         ae[i].removeEventListener('click', handler, true);                     } else if (ae[i].detachEvent) {                         ae[i].detachEvent('onclick', handler);                     }                     if ((ae[i].getAttribute("_onclick")) != null) {                         ae[i].parentNode.replaceChild(be[i], ae[i]);                     }                 }             } else {                 for (var i = 0; i < ae.length; i++) {                     if (ae[i].removeEventListener) {                         ae[i].removeEventListener('click', handler, true);                     } else if (ae[i].detachEvent) {                         var res = ae[i].detachEvent('onclick', handler);                     }                     if ((ae[i].getAttribute("_onclick")) != null) {                         var _onclickval = ae[i].getAttribute("_onclick");                         ae[i].removeAttribute("_onclick");                         ae[i].setAttribute("onclick", _onclickval);                     }                 }             }         }         localStorage.setItem('tastopflag', 'false');         arr = [];         return true;     } else {         ssclassname = 'null';         ssname = 'null';         sstagname = 'null';         if (event.ctrlKey) {             return true;         }         if (event.preventDefault) {             event.preventDefault();             event.stopPropagation();             event.cancelBubble = true;             event.returnValue = false;         } else {             window.event.cancelBubble = true;             window.event.returnValue = false;         }         var e = event.target || event.srcElement;         var f = event.target || event.srcElement;         var className = e.className;         var rpath = '';         var firstpass = 0;         for (var path = ''; e && e.nodeType == 1; e = e.parentNode) {             var predicate = [];             var siblings = e.parentNode.children;             var count = 0;             var unique = false;             for (var i = 0; siblings && (i < siblings.length); i++) {                 if (siblings[i].tagName == e.tagName) {                     count++;                     if (siblings[i] == e) {                         idx = count;                     }                 }             }             if (idx == 1 && count == 1) {                 idx = null;             }             if (useId && e.id) {                 predicate[predicate.length] = '@id=' + '"' + e.id + '"';                 unique = true;             }             xidx = (useIdx && idx) ? ('[' + idx + ']') : '';             idx = (useIdx && idx && !unique) ? ('[' + idx + ']') : '';             predicate = (predicate.length > 0) ? ('[' + predicate.join(' and ') + ']') : '';             path = '/' + e.tagName.toLowerCase() + xidx + path;             if (firstpass == 0) {                 if (unique && relative) {                     rpath = '//*' + idx + predicate + rpath;                     firstpass = 1;                 } else {                     rpath = '/' + e.tagName.toLowerCase() + idx + predicate + rpath;                 }             }         }         ishidden = isVisible(f);         if (ishidden == true || ishidden == 'True' || ishidden == 'true') {             ishidden = 'No';         } else {             ishidden = 'Yes';         }         var tagname = f.tagName.toLowerCase();         if (tagname.indexOf(':') != -1) {             tagname = tagname.replace(':', '');             tagname = 'custom' + tagname;         }         id = f.id;         name = f.name;         placeholder = f.placeholder;         id = (String(id));         name = (String(name));         placeholder = (String(placeholder));         var textvalue = text_content(f);         textvalue = (String(textvalue));         if (name != '' && name != 'undefined') {             names = document.getElementsByName(name);             if (names.length > 1) {                 for (var k = 0; k < names.length; k++) {                     if (f == names[k]) {                         ssname = name + '[' + k + ']'                     }                 }             } else {                 ssname = name;             }         }         if (tagname != '' && tagname != 'undefined') {             tagnames = document.getElementsByTagName(tagname);             if (tagnames.length > 1) {                 for (var k = 0; k < tagnames.length; k++) {                     if (f == tagnames[k]) {                         sstagname = tagname + '[' + k + ']'                     }                 }             } else {                 sstagname = tagname;             }         }         if (className != '' && className != 'undefined' && className != 'SLKNineteen68_Highlight') {             classnames = document.getElementsByClassName(className);             if (classnames.length > 1) {                 for (var k = 0; k < classnames.length; k++) {                     if (f == classnames[k]) {                         ssclassname = className + '[' + k + ']'                     }                 }             } else {                 ssclassname = className;             }         }         if (tagname != 'script' && tagname != 'meta' && tagname != 'html' && tagname != 'head' && tagname != 'style' && tagname != 'body' && tagname != 'form' && tagname != 'link' && tagname != 'noscript' && tagname != '!' && tagname != 'code' && tagname != 'animatetransform') {             if (textvalue == '' || textvalue == 'null' || textvalue == 'undefined' || textvalue == '0') {                 if (name != '' && name != 'undefined') {                     names = document.getElementsByName(name);                     if (names.length > 1) {                         for (var k = 0; k < names.length; k++) {                             if (f == names[k]) {                                 textvalue = name + k;                             }                         }                     } else {                         textvalue = name;                     }                 } else if (id != '' && id != 'undefined') {                     textvalue = id;                 } else if (placeholder != '' && placeholder != 'undefined') {                     textvalue = placeholder;                 } else {                     textvalue = 'NONAME' + nonamecounter;                     nonamecounter = nonamecounter + 1;                 }             }             if (tagname == 'select') {                 f.setAttribute('disabled', 'disabled');                 multipleFlag = f.hasAttribute('multiple');             }             var etype = f.getAttribute('type');             etype = (String(etype)).toLowerCase();             var newPath = path;             if (tagname == 'textarea') {                 tagname = 'input';                 tagtype = 'txtarea';             } else if (tagname == 'select' && multipleFlag) {                 tagname = 'list';                 tagtype = 'lst';             } else if (tagname == 'select') {                 tagtype = 'select';             } else if (tagname == 'td') {                 tagname = 'tablecell';                 tagtype = 'tblcell';             } else if (tagname == 'a') {                 tagtype = 'lnk';             } else if (tagname == 'table') {                 tagtype = 'tbl';             } else if (tagname == 'img') {                 tagtype = 'img';             } else if (tagname == 'input' && etype == 'image') {                 tagname = 'img';                 tagtype = 'img';             }             if (tagname == 'input' && (etype == 'button' || etype == 'submit' || etype == 'reset' || etype == 'file')) {                 tagname = 'button';                 tagtype = 'btn';             } else if (tagname == 'input' && etype == 'radio') {                 tagname = 'radiobutton';                 tagtype = 'radiobtn';             } else if (tagname == 'input' && etype == 'checkbox') {                 tagname = 'checkbox';                 tagtype = 'chkbox';             } else if (tagname == 'input' && (etype == 'text' || etype == 'email' || etype == 'number' || etype == 'password' || etype == 'range' || etype == 'search' || etype == 'url')) {                 tagname = 'input';                 tagtype = 'txtbox';             } else if (tagname == 'option' && f.parentNode.hasAttribute('multiple')) {                 tagname = 'list';                 var selectIndex1 = rpath.indexOf('select');                 var selectIndex2 = path.indexOf('select');                 rpath = rpath.substring(0, selectIndex1 + 6);                 path = path.substring(0, selectIndex2 + 6);             }             if (id == '') {                 id = 'null';             }             newPath = String(rpath) + ';' + String(id) + ';' + String(path) + ';' + ssname + ';' + sstagname + ';' + ssclassname;             if (textvalue == '' || textvalue.length == 0 || textvalue == '0') {                 textvalue = 'NONAME' + nonamecounter;                 nonamecounter = nonamecounter + 1;                 custname = textvalue;             } else {                 custname = textvalue;             }             if (tagtype != '') {                 custname = custname + '_' + tagtype;             } else {                 custname = custname + '_elmnt';             }             if (tagname == 'select') {                 f.removeAttribute('disabled');                 f.setAttribute('enabled', 'enabled');             }             for (var i = 0; i < arr.length; i++) {                 if (arr[i].xpath == newPath) {                     uniqueFlag = true;                     break;                 }             };             if (uniqueFlag == false) {                 arr.push({                     'xpath': newPath,                     'url': url,                                       'hiddentag': ishidden,                     'custname': custname,                     'tag': tagname                 });             }             if (browser == 3) {                 f.setAttribute('class', className + ' SLKNineteen68_Highlight');                 f.setAttribute('className', className + ' SLKNineteen68_Highlight');                 f.style.setAttribute('cssText', 'background: #fff300; border: 2px solid #cc3300;outline: 2px solid #fff300;');             } else {                 f.setAttribute('class', className + ' SLKNineteen68_Highlight');                 f.setAttribute('style', 'background: #fff300; border: 2px solid #cc3300;outline: 2px solid #fff300;');             }         }         return false;     } } click(ae, isIE, be);  function click(ae, isIE, be) {     if (isIE) {         for (var i = 0; i < ae.length; i++) {             if ((ae[i].getAttribute("onclick")) != null) {                 var onclickval = ae[i].attributes["onclick"].value;                 be[i] = ae[i].cloneNode(true);                 ae[i].onclick = null;                 ae[i].setAttribute('_onclick', onclickval);             }             if (ae[i].addEventListener) {                 ae[i].addEventListener('click', handler, true);             } else if (ae[i].attachEvent) {                 ae[i].attachEvent('onclick', handler);             }         }     } else {         for (var i = 0; i < ae.length; i++) {             if ((ae[i].getAttribute("onclick")) != null) {                 var onclickval = ae[i].getAttribute("onclick");                 ae[i].removeAttribute("onclick");                 ae[i].setAttribute("_onclick", onclickval);             }             if (ae[i].addEventListener) {                 ae[i].addEventListener('click', handler, true);             } else if (ae[i].attachEvent) {                 ae[i].attachEvent('onclick', handler);             }         }     } }  function text_content(f) {     var firstText = '';     var textdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var curNode = f.childNodes[z];         whitespace = /^\s*$/;         if (curNode.nodeName === '#text' && !(whitespace.test(curNode.nodeValue))) {             firstText = curNode.nodeValue;             textdisplay = textdisplay + firstText;         }     }     return (textdisplay); };  function addNodesOuter(array, collection) {     for (var i = 0; collection && collection.length && i < collection.length; i++) {         array.push(collection[i]);     } };"""
            driver.switch_to.window(currenthandle)
            logger.log('FILE: clickandadd.py , DEF: startclickandadd() , MSG: Performing the click and add operation on default/outer page')
            driver.execute_script(javascript_clicknadd, driver.current_url,browser)
            logger.log('FILE: clickandadd.py , DEF: startclickandadd() , MSG: Performing the click and add operation on default/outer page done')

            def switchtoframe_clicknadd1(mypath):
                cond_flag_cna = False
                logger.log('FILE:  clickandadd.py , DEF: switchtoframe_clicknadd1() , MSG: Inside switchtoframe_clicknadd1 method')
                indiframes = mypath.split("/")
                logger.log('FILE: clickandadd.py , DEF: switchtoframe_clicknadd1()  , MSG: Splitting Iframe/frame url by /')
                global currenthandle
                driver.switch_to.window(currenthandle)
                logger.log('FILE: clickandadd.py , DEF: switchtoframe_clicknadd1() , MSG: Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = domconstants.IFRAME
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'f':
                            frame_iframe =domconstants.FRAME
                            logger.log('FILE: clickandadd.py , DEF: switchtoframe_clicknadd1() , MSG: It is  frame')
                        else:
                            logger.log('FILE: clickandadd.py , DEF: switchtoframe_clicknadd1() , MSG: It is  iframe')
                        try:
                            if (driver.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                                driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                                logger.log('FILE: clickandadd.py , DEF: switchtoframe_clicknadd1() , MSG: Switched to frame/iframe')
                                cond_flag_cna = True
                            else:
                                cond_flag_cna = False
                                break
                        except Exception as e:
                            Exceptions.error(e)
                            cond_flag_cna = False
                return cond_flag_cna



            def callback_clicknadd1(myipath):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' + '/'
                    if(switchtoframe_clicknadd1(path)):
                        logger.log('FILE: clickandadd.py , DEF: callback_clicknadd1() , MSG: Performing the click and add operation on iframe/frame page')
                        driver.execute_script(javascript_clicknadd, path,browser)
                        logger.log('FILE: clickandadd.py , DEF: callback_clicknadd1() , MSG: Performing the click and add operation on iframe/frame page done')
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            path = path + str(frames) + 'f' + '/'
                            if switchtoframe_clicknadd1(path):
                                logger.log('FILE: clickandadd.py , DEF: callback_clicknadd1() , MSG: Performing the click and add operation on frame/iframe page')
                                driver.execute_script(javascript_clicknadd, path,browser)
                                logger.log('FILE: clickandadd.py , DEF: callback_clicknadd1() , MSG: Performing the click and add operation on frame/iframe page done')
                        callback_clicknadd1(path)

            def callback_clicknadd2(myipath):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'f' + '/'
                    if(switchtoframe_clicknadd1(path)):
                        logger.log('FILE: clickandadd.py , DEF: callback_clicknadd2() , MSG: Performing the click and add operation on frame/iframe page')
                        driver.execute_script(javascript_clicknadd, path,browser)
                        logger.log('FILE: clickandadd.py , DEF: callback_clicknadd2() , MSG: Performing the click and add operation on frame/iframe page done')
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            path = path + str(frames) + 'i' + '/'
                            if switchtoframe_clicknadd1(path):
                                logger.log('FILE: clickandadd.py , DEF: callback_clicknadd2() , MSG: Performing the click and add operation on iframe/frame page')
                                driver.execute_script(javascript_clicknadd, path,browser)
                                logger.log('FILE: clickandadd.py , DEF: callback_clicknadd2() , MSG: Performing the click and add operation on iframe/frame page done')
                        callback_clicknadd2(path)

            callback_clicknadd1('')
            logger.log('FILE: clickandadd.py, DEF: startclickandadd() , MSG: clickandadd scrape operation on iframe/frame pages is completed')
            driver.switch_to.window(currenthandle)
            callback_clicknadd2('')
            logger.log('FILE: clickandadd.py, DEF: startclickandadd() , MSG: clickandadd scrape operation on frame/iframe pages is completed')
            driver.switch_to.window(currenthandle)
            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            status = domconstants.STATUS_FAIL
            Exceptions.error(e)
        return status

    def stopclickandadd(self,screenname,depscreens):
        try:
            logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: Inside stopclickandadd method .....')
            driver = browserops.driver
            logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: Obtained driver from browserops.py class .....')
            javascript_stopclicknadd = """localStorage.setItem('tastopflag', 'true'); document.getElementsByTagName('HTML')[0].click(); function getElementsByClassName(classname) {     var a = [];     var re = new RegExp('(^| )'+classname+'( |$)');     var els = document.getElementsByTagName("*");     for(var i=0,j=els.length; i<j; i++)         if(re.test(els[i].className))a.push(els[i]);     return a; } if(document.getElementById('SLKNineteen68_Table')){ styleTag = document.getElementById('SLKNineteen68_Table'); head = document.head || document.getElementsByTagName('head')[0]; head.removeChild(styleTag); var a=getElementsByClassName('SLKNineteen68_Highlight'); for (var i = 0; i < a.length; i++) { a[i].removeAttribute('style'); }}var temp = window.tasarr; window.tasarr = null; return (temp);"""
            tempne_stopclicknadd = []
            logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: Performing the stopclickandd operation on default/outer page')
            tempreturn_stopclicknadd = driver.execute_script(javascript_stopclicknadd)
            logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: stopclickandd operation on default/outer page is done and data is obtained')
            tempne_stopclicknadd.extend(tempreturn_stopclicknadd)


            def switchtoframe_stopclicknadd1(mypath):
                logger.log('FILE: clickandadd.py , DEF: switchtoframe_stopclicknadd1() , MSG: Inside switchtoframe_stopclicknadd1 method')
                cond_flag_scna = False
                logger.log('FILE: clickandadd.py , DEF: switchtoframe_stopclicknadd1() , MSG: Splitting Iframe/frame url by /')
                indiframes = mypath.split("/")
                driver.switch_to.window(currenthandle)
                logger.log('FILE: clickandadd.py , DEF: switchtoframe_stopclicknadd1() , MSG: Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = domconstants.IFRAME
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'f':
                            frame_iframe = domconstants.FRAME
                            logger.log('FILE: clickandadd.py , DEF: switchtoframe_stopclicknadd1() , MSG: It is  frame')
                        else:
                            logger.log('FILE: clickandadd.py , DEF: switchtoframe_stopclicknadd1() , MSG: It is iframe')
                        try:
                            if (driver.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                                driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                                logger.log('FILE: clickandadd.py , DEF: switchtoframe_stopclicknadd1() , MSG: Switched to frame/iframe')
                                cond_flag_scna = True
                            else:
                                cond_flag_scna = False
                                break
                        except Exception as e:
                            Exceptions.error(e)
                            cond_flag_scna = False
                return cond_flag_scna

            def callback_stopclicknadd1(myipath, tempne_stopclicknadd):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' + '/'
                    if(switchtoframe_stopclicknadd1(path)):
                        logger.log('FILE: clickandadd.py , DEF: callback_stopclicknadd1() , MSG: before stopclicknadd operation on iframe page is done and data is obtained')
                        temp = driver.execute_script(javascript_stopclicknadd)
                        logger.log('FILE: clickandadd.py , DEF: callback_stopclicknadd1() , MSG: stopclicknadd operation on iframe page is done and data is obtained')
                        tempne_stopclicknadd.extend(temp)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            path = path + str(frames) + 'f' + '/'
                            if switchtoframe_clicknadd1(path):
                                itemp = driver.execute_script(javascript_stopclicknadd)
                                logger.log('FILE: clickandadd.py , DEF: callback_stopclicknadd1() , MSG: before stopclicknadd operation on frame page is done and data is obtained')
                                tempne_stopclicknadd.extend(itemp)
                                logger.log('FILE: clickandadd.py , DEF: callback_stopclicknadd1() , MSG: stopclicknadd operation on frame page is done and data is obtained')
                        callback_stopclicknadd1(path, tempne_stopclicknadd)

            def callback_stopclicknadd2(myipath, tempne_stopclicknadd):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'f' + '/'
                    if(switchtoframe_stopclicknadd1(path)):
                        logger.log('FILE: clickandadd.py , DEF: callback_stopclicknadd2() , MSG: before stopclicknadd operation on frame page is done and data is obtained')
                        temp = driver.execute_script(javascript_stopclicknadd)
                        logger.log('FILE: clickandadd.py , DEF: callback_stopclicknadd2() , MSG: stopclicknadd operation on frame page is done and data is obtained')
                        tempne_stopclicknadd.extend(temp)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            path = path + str(frames) + 'i' + '/'
                            if switchtoframe_clicknadd1(path):
                                logger.log('FILE: clickandadd.py , DEF: callback_stopclicknadd2() , MSG: before stopclicknadd operation on iframe page is done and data is obtained')
                                itemp = driver.execute_script(javascript_stopclicknadd)
                                logger.log('FILE: clickandadd.py , DEF: callback_stopclicknadd2() , MSG: stopclicknadd operation on iframe page is done and data is obtained')
                                tempne_stopclicknadd.extend(itemp)
                        callback_stopclicknadd2(path, tempne_stopclicknadd)
            callback_stopclicknadd1('', tempne_stopclicknadd)
            logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: stopclickandadd operation on iframe/frame pages is completed')
            driver.switch_to.window(currenthandle)
            callback_stopclicknadd2('', tempne_stopclicknadd)
            logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: stopclickandadd operation on frame/iframe pages is completed')
            driver.switch_to.window(currenthandle)
##            global screenindex
##            screenname = 'screen' + str(screenindex)
##            screenindex = screenindex + 1
            v = []
            v.append({'data':tempne_stopclicknadd})
            v.append({'dependent':depscreens})
            global vie
            vie.append({screenname: v})
            logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: Creating a json object with key vie with value as return data')
##            with open('dom.json', 'a') as outfile:
##                logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: Opening domelements.json file to write vie object')
##                json.dump(vie, outfile, indent=4, sort_keys=False)
##                logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: vie is dumped into  domelements.json file ')
##            outfile.close()
            logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: domelements.json file closed ')
            if driver.current_url == domconstants.BLANK_PAGE:
                logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: url is blank so cannot perform clickandadd operation')
                status = domconstants.STATUS_FAIL
            else:
                status = domconstants.STATUS_SUCCESS
        except Exception as e:
            status = domconstants.STATUS_FAIL
            Exceptions.error(e)
        return status

    def save_json_data(self):
        global vie
        data = {'view' : vie}
        with open('domelements.json', 'w') as outfile:
                logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: Opening domelements.json file to write vie object')
                json.dump(data, outfile, indent=4, sort_keys=False)
                logger.log('FILE: clickandadd.py , DEF: stopclickandadd() , MSG: vie is dumped into  domelements.json file ')
        outfile.close()


