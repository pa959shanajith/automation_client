#-------------------------------------------------------------------------------
# Name:        highlight.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     29-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Exceptions
import domconstants
import clickandadd
import time
import browserops
import fullscrape
import logger
import objectspy
status =domconstants.STATUS_FAIL
currentdriverhandle = ''
lst=[]
class Highlight():
    def highlight(self,data,element,handle):
        try:
            logger.log('FILE: highlight.py , DEF: highlight() , MSG: Inside highlight method .....')
            driver = browserops.driver
            currentdriverhandle = clickandadd.currenthandle
            logger.log('FILE: highlight.py , DEF: highlight() , MSG: Obtained browser handle and driver from browserops.py class ......')
            if currentdriverhandle is  '' or currentdriverhandle is  None:
                currentdriverhandle = fullscrape.currenthandle
            if currentdriverhandle is  '' or currentdriverhandle is  None:
                currentdriverhandle = handle
            driver.switch_to.window(currentdriverhandle)
            #Split the string with delimiter ','
            highele = data.split(',')
            # find out if the highele[1] has id or name attrib

            identifiers = highele[0].split(';')
            url = highele[1]
            action=''
            def highlight1(element):
                logger.log('FILE: highlight.py , DEF: highlight() , MSG: Inside highlight1 method .....')
                if element is not None:
                    """Highlights (blinks) a Selenium Webdriver element"""
                    def apply_style(s, sec):
                        logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Inside apply_style method .....')
                        if driver.name == 'internet explorer' :
                            logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Before applying color to the element in IE browser .....')
                            driver.execute_script("arguments[0].style.setAttribute('cssText', arguments[1]);",
                                              element, s)
                            logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Applied color to the element in IE browser .....')
                        else:
                            logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Before applying color to the element in chrome/firefox browser .....')
                            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                              element, s)
                            logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Applied color to the element in chrome/firefox browser .....')
                        if(action=='OBJECTMAPPER'):
                            time.sleep(0.1)
                        else:
                            time.sleep(sec)
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Before getting the original style .....')
                    original_style = element.get_attribute('style')
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Original style obtained.....')
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Before highlighting .....')
                    apply_style(str(original_style) + "background: #fff300; border: 2px solid #cc3300;outline: 2px solid #fff300;", 3)
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Element highlighted .....')
                    if (driver.capabilities['version'] != unicode(8)):
                        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Before removing the style for ie8 .....')
                        if(action!='OBJECTMAPPER'):
                            apply_style(original_style, 0)
                            logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Removed the style for ie8 .....')
                    else:
                        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Before removing the style for other browsers .....')
                        if(action!='OBJECTMAPPER'):
                            apply_style(str(original_style) + "background: 0; border: 0px none 0; outline: none", 0)
                            logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Removed the style for other browsers .....')

            def is_int(url):
                try:
                    int(url[0])
                    logger.log('FILE: highlight.py , DEF: is_int() , MSG: The url is an iframe/frmae url .....')
                    return True
                except ValueError:
                    logger.log('FILE: highlight.py , DEF: is_int() , MSG: The url is an normal webpage url .....')
                    return False

            if is_int(url):
                logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Splitting Iframe/frame url by /')
                indiframes = url.split("/")
                driver.switch_to.window(currentdriverhandle)
##                driver.switch_to.default_content()
                logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = 'frame'
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'i':
                            frame_iframe = 'iframe'
                            logger.log('FILE: highlight.py , DEF: highlight1() , MSG: It is  iframe')
                        else:
                            logger.log('FILE: highlight.py , DEF: highlight1() , MSG: It is  frame')
                        if j=='':
                            continue
                        driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Switched to frame/iframe')

                try:
                    #find by rxpath
                    tempwebElement = driver.find_elements_by_xpath(identifiers[0])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                    webElement = tempwebElement

                except Exception as webEx:
                    try:
                        #find by id
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                        webElement = tempwebElement
                    except Exception as webEx:
                        try:
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                            webElement = tempwebElement
                        except Exception as webEx:
                            webElement = None
                if webElement is not None:
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Element found inside frame/iframe .....')
                    highlight1(webElement[0])
                    print 'Highlight method executed'
                    if(action=='OBJECTMAPPER'):
                            properties_script="""if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('select');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var useIdx = true; var useId = true; var useClass = true; var relative = true; var ae = []; var be = []; var element = arguments[0]; var url = arguments[1]; var ishidden = 0; var tagname = 0; var textvalue = ''; var arr = []; var custname = ''; var tagtype = ''; var multipleFlag = false; var uniqueFlag = false; var nonamecounter = 1; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var isIE = /*@cc_on!@*/ false || !!document.documentMode;   function getElementProperties(element) {     tagtype = '';     arr = [];     var e = element;     var f = element; 	ssclassname = 'null';     ssname = 'null';     sstagname = 'null';     var className = e.className;     var rpath = '';     var firstpass = 0;     for (var path = ''; e && e.nodeType == 1; e = e.parentNode) {         var predicate = [];         var siblings = e.parentNode.children;         var count = 0;         var unique = false;         for (var i = 0; siblings && (i < siblings.length); i++) {             if (siblings[i].tagName == e.tagName) {                 count++;                 if (siblings[i] == e) {                     idx = count;                 }             }         }         if (idx == 1 && count == 1) {             idx = null;         }         if (useId && e.id) {             predicate[predicate.length] = '@id=' + '"' + e.id + '"';             unique = true;         }         xidx = (useIdx && idx) ? ('[' + idx + ']') : '';         idx = (useIdx && idx && !unique) ? ('[' + idx + ']') : '';         predicate = (predicate.length > 0) ? ('[' + predicate.join(' and ') + ']') : '';         path = '/' + e.tagName.toLowerCase() + xidx + path;         if (firstpass == 0) {             if (unique && relative) {                 rpath = '//*' + idx + predicate + rpath;                 firstpass = 1;             } else {                 rpath = '/' + e.tagName.toLowerCase() + idx + predicate + rpath;             }         }     }     ishidden = isVisible(f);      if (ishidden == true || ishidden == 'True' || ishidden == 'true') {             ishidden = 'No';         } else {             ishidden = 'Yes';         }         var tagname = f.tagName.toLowerCase();         if (tagname.indexOf(':') != -1) {             tagname = tagname.replace(':', '');             tagname = 'custom' + tagname;         }         id = f.id;         name = f.name;         placeholder = f.placeholder;         id = (String(id));         name = (String(name));         placeholder = (String(placeholder));         var textvalue = text_content(f);         textvalue = (String(textvalue));         if (name != '' && name != 'undefined') {             names = document.getElementsByName(name);             if (names.length > 1) {                 for (var k = 0; k < names.length; k++) {                     if (f == names[k]) {                         ssname = name + '[' + k + ']'                     }                 }             } else {                 ssname = name;             }         }         if (tagname != '' && tagname != 'undefined') {             tagnames = document.getElementsByTagName(tagname);             if (tagnames.length > 1) {                 for (var k = 0; k < tagnames.length; k++) {                     if (f == tagnames[k]) {                         sstagname = tagname + '[' + k + ']'                     }                 }             } else {                 sstagname = tagname;             }         }         if (className != '' && className != 'undefined' && className != 'SLKNineteen68_Highlight') {             classnames = document.getElementsByClassName(className);             if (classnames.length > 1) {                 for (var k = 0; k < classnames.length; k++) {                     if (f == classnames[k]) {                         ssclassname = className + '[' + k + ']'                     }                 }             } else {                 ssclassname = className;             }         }     if (tagname != 'script' && tagname != 'meta' && tagname != 'html' && tagname != 'head' && tagname != 'style' && tagname != 'body' && tagname != 'form' && tagname != 'link' && tagname != 'noscript' && tagname != '!' && tagname != 'code' && tagname != 'animatetransform') {         if (textvalue == '' || textvalue == 'null' || textvalue == 'undefined' || textvalue == '0') {             if (name != '' && name != 'undefined') {                 names = document.getElementsByName(name);                 if (names.length > 1) {                     for (var k = 0; k < names.length; k++) {                         if (f == names[k]) {                             textvalue = name + k;                         }                     }                 } else {                     textvalue = name;                 }             } else if (id != '' && id != 'undefined') {                 textvalue = id;             } else if (placeholder != '' && placeholder != 'undefined') {                 textvalue = placeholder;             } else {                 textvalue = 'NONAME' + nonamecounter;                 nonamecounter = nonamecounter + 1;             }         }         if (tagname == 'select') {             f.setAttribute('disabled', 'disabled');             multipleFlag = f.hasAttribute('multiple');         }         var etype = f.getAttribute('type');         etype = (String(etype)).toLowerCase();         var newPath = path;         if (tagname == 'textarea') {             tagname = 'input';             tagtype = 'txtarea';         } else if (tagname == 'select' && multipleFlag) {             tagname = 'list';             tagtype = 'lst';         } else if (tagname == 'select') {             tagtype = 'select';         } else if (tagname == 'td') {             tagname = 'tablecell';             tagtype = 'tblcell';         } else if (tagname == 'a') {             tagtype = 'lnk';         } else if (tagname == 'table') {             tagtype = 'tbl';         } else if (tagname == 'img') {             tagtype = 'img';         } else if (tagname == 'input' && etype == 'image') {             tagname = 'img';             tagtype = 'img';         }         if (tagname == 'input' && (etype == 'button' || etype == 'submit' || etype == 'reset' || etype == 'file')) {             tagname = 'button';             tagtype = 'btn';         } else if (tagname == 'input' && etype == 'radio') {             tagname = 'radiobutton';             tagtype = 'radiobtn';         } else if (tagname == 'input' && etype == 'checkbox') {             tagname = 'checkbox';             tagtype = 'chkbox';         } else if (tagname == 'input' && (etype == 'text' || etype == 'email' || etype == 'number' || etype == 'password' || etype == 'range' || etype == 'search' || etype == 'url')) {             tagname = 'input';             tagtype = 'txtbox';         } else if (tagname == 'option' && f.parentNode.hasAttribute('multiple')) {             tagname = 'list';             var selectIndex1 = rpath.indexOf('select');             var selectIndex2 = path.indexOf('select');             rpath = rpath.substring(0, selectIndex1 + 6);             path = path.substring(0, selectIndex2 + 6);         }         if (id == '') {             id = 'null';         }         newPath = String(rpath) + ';' + String(id) + ';' + String(path) + ';'  + ssname + ';' + sstagname + ';' + ssclassname;         if (textvalue == '' || textvalue.length == 0 || textvalue == '0') {             textvalue = 'NONAME' + nonamecounter;             nonamecounter = nonamecounter + 1;             custname = textvalue;         } else {             custname = textvalue;         }         if (tagtype != '') {             custname = custname + '_' + tagtype;         } else {             custname = custname + '_elmnt';         }         if (tagname == 'select') {             f.removeAttribute('disabled');             f.setAttribute('enabled', 'enabled');         }         for (var i = 0; i < arr.length; i++) {             if (arr[i].xpath == newPath) {                 uniqueFlag = true;                 break;             }         };         if (uniqueFlag == false) {             arr.push({                 'xpath': newPath,                 'url': url,                 'text': textvalue,                 'hiddentag': ishidden,                 'custname': custname,                 'tag': tagname,                 'id': id             });         }     }     return arr; }  function isVisible(elem) {     function inside(child, parent) {         while (child) {             if (child === parent) return true;             child = child.parentNode;         }         return false;     };     if (document.hidden || elem.offsetWidth == 0 || elem.offsetHeight == 0 || elem.style.visibility == 'hidden' || elem.style.display == 'none' || elem.style.opacity === 0) return false;     var rect = elem.getBoundingClientRect();     if (window.getComputedStyle || elem.currentStyle) {         var el = elem,             comp = null;         while (el) {             if (el === document) {                 break;             } else if (!el.parentNode) return false;             comp = window.getComputedStyle ? window.getComputedStyle(el, null) : el.currentStyle;             if (comp && (comp.visibility == 'hidden' || comp.display == 'none' || (typeof comp.opacity !== 'undefined' && !(comp.opacity > 0)))) return false;             el = el.parentNode;         }     }     return true; };  function text_content(f) {     var firstText = '';     var textdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var curNode = f.childNodes[z];         whitespace = /^\s*$/;         if (curNode.nodeName === '#text' && !(whitespace.test(curNode.nodeValue))) {             firstText = curNode.nodeValue;             textdisplay = textdisplay + firstText;         }     }     return (textdisplay); };  function addNodesOuter(array, collection) {     for (var i = 0; collection && collection.length && i < collection.length; i++) {         array.push(collection[i]);     } };  return getElementProperties(element);"""
                            element_properties = []
                            element_properties = driver.execute_script(properties_script,webElement[0],url)
                            new_properties=element_properties[0];
                            if cmp(element,new_properties)!=0:
                                print 'object changed'
                                lst.append(new_properties)
                            else:
                                 lst.append(element)
                try:
##                            driver.switch_to.default_content()
                    driver.switch_to.window(currentdriverhandle)
                except Exception as e4:
                    evb = e4

            else:
                try:
##                    driver.switch_to.default_content()

                    driver.switch_to.window(currentdriverhandle)
                except Exception as e4:
                    evb = e4
                try:
                    tempwebElement = driver.find_elements_by_xpath(identifiers[0])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                    webElement = tempwebElement
                except Exception as webEx:
                    try:
                        #find by id
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                        webElement = tempwebElement
                    except Exception as webEx:
                        try:
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                            webElement = tempwebElement
                        except Exception as webEx:
                            webElement = None
                if webElement is not None:
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Element found inside main page .....')
                    highlight1(webElement[0])
                    print 'Highlight method executed'
                    if(action=='OBJECTMAPPER'):
                            properties_script="""if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('select');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var useIdx = true; var useId = true; var useClass = true; var relative = true; var ae = []; var be = []; var element = arguments[0]; var url = arguments[1]; var ishidden = 0; var tagname = 0; var textvalue = ''; var arr = []; var custname = ''; var tagtype = ''; var multipleFlag = false; var uniqueFlag = false; var nonamecounter = 1; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var isIE = /*@cc_on!@*/ false || !!document.documentMode;   function getElementProperties(element) {     tagtype = '';     arr = [];     var e = element;     var f = element; 	ssclassname = 'null';     ssname = 'null';     sstagname = 'null';     var className = e.className;     var rpath = '';     var firstpass = 0;     for (var path = ''; e && e.nodeType == 1; e = e.parentNode) {         var predicate = [];         var siblings = e.parentNode.children;         var count = 0;         var unique = false;         for (var i = 0; siblings && (i < siblings.length); i++) {             if (siblings[i].tagName == e.tagName) {                 count++;                 if (siblings[i] == e) {                     idx = count;                 }             }         }         if (idx == 1 && count == 1) {             idx = null;         }         if (useId && e.id) {             predicate[predicate.length] = '@id=' + '"' + e.id + '"';             unique = true;         }         xidx = (useIdx && idx) ? ('[' + idx + ']') : '';         idx = (useIdx && idx && !unique) ? ('[' + idx + ']') : '';         predicate = (predicate.length > 0) ? ('[' + predicate.join(' and ') + ']') : '';         path = '/' + e.tagName.toLowerCase() + xidx + path;         if (firstpass == 0) {             if (unique && relative) {                 rpath = '//*' + idx + predicate + rpath;                 firstpass = 1;             } else {                 rpath = '/' + e.tagName.toLowerCase() + idx + predicate + rpath;             }         }     }     ishidden = isVisible(f);      if (ishidden == true || ishidden == 'True' || ishidden == 'true') {             ishidden = 'No';         } else {             ishidden = 'Yes';         }         var tagname = f.tagName.toLowerCase();         if (tagname.indexOf(':') != -1) {             tagname = tagname.replace(':', '');             tagname = 'custom' + tagname;         }         id = f.id;         name = f.name;         placeholder = f.placeholder;         id = (String(id));         name = (String(name));         placeholder = (String(placeholder));         var textvalue = text_content(f);         textvalue = (String(textvalue));         if (name != '' && name != 'undefined') {             names = document.getElementsByName(name);             if (names.length > 1) {                 for (var k = 0; k < names.length; k++) {                     if (f == names[k]) {                         ssname = name + '[' + k + ']'                     }                 }             } else {                 ssname = name;             }         }         if (tagname != '' && tagname != 'undefined') {             tagnames = document.getElementsByTagName(tagname);             if (tagnames.length > 1) {                 for (var k = 0; k < tagnames.length; k++) {                     if (f == tagnames[k]) {                         sstagname = tagname + '[' + k + ']'                     }                 }             } else {                 sstagname = tagname;             }         }         if (className != '' && className != 'undefined' && className != 'SLKNineteen68_Highlight') {             classnames = document.getElementsByClassName(className);             if (classnames.length > 1) {                 for (var k = 0; k < classnames.length; k++) {                     if (f == classnames[k]) {                         ssclassname = className + '[' + k + ']'                     }                 }             } else {                 ssclassname = className;             }         }     if (tagname != 'script' && tagname != 'meta' && tagname != 'html' && tagname != 'head' && tagname != 'style' && tagname != 'body' && tagname != 'form' && tagname != 'link' && tagname != 'noscript' && tagname != '!' && tagname != 'code' && tagname != 'animatetransform') {         if (textvalue == '' || textvalue == 'null' || textvalue == 'undefined' || textvalue == '0') {             if (name != '' && name != 'undefined') {                 names = document.getElementsByName(name);                 if (names.length > 1) {                     for (var k = 0; k < names.length; k++) {                         if (f == names[k]) {                             textvalue = name + k;                         }                     }                 } else {                     textvalue = name;                 }             } else if (id != '' && id != 'undefined') {                 textvalue = id;             } else if (placeholder != '' && placeholder != 'undefined') {                 textvalue = placeholder;             } else {                 textvalue = 'NONAME' + nonamecounter;                 nonamecounter = nonamecounter + 1;             }         }         if (tagname == 'select') {             f.setAttribute('disabled', 'disabled');             multipleFlag = f.hasAttribute('multiple');         }         var etype = f.getAttribute('type');         etype = (String(etype)).toLowerCase();         var newPath = path;         if (tagname == 'textarea') {             tagname = 'input';             tagtype = 'txtarea';         } else if (tagname == 'select' && multipleFlag) {             tagname = 'list';             tagtype = 'lst';         } else if (tagname == 'select') {             tagtype = 'select';         } else if (tagname == 'td') {             tagname = 'tablecell';             tagtype = 'tblcell';         } else if (tagname == 'a') {             tagtype = 'lnk';         } else if (tagname == 'table') {             tagtype = 'tbl';         } else if (tagname == 'img') {             tagtype = 'img';         } else if (tagname == 'input' && etype == 'image') {             tagname = 'img';             tagtype = 'img';         }         if (tagname == 'input' && (etype == 'button' || etype == 'submit' || etype == 'reset' || etype == 'file')) {             tagname = 'button';             tagtype = 'btn';         } else if (tagname == 'input' && etype == 'radio') {             tagname = 'radiobutton';             tagtype = 'radiobtn';         } else if (tagname == 'input' && etype == 'checkbox') {             tagname = 'checkbox';             tagtype = 'chkbox';         } else if (tagname == 'input' && (etype == 'text' || etype == 'email' || etype == 'number' || etype == 'password' || etype == 'range' || etype == 'search' || etype == 'url')) {             tagname = 'input';             tagtype = 'txtbox';         } else if (tagname == 'option' && f.parentNode.hasAttribute('multiple')) {             tagname = 'list';             var selectIndex1 = rpath.indexOf('select');             var selectIndex2 = path.indexOf('select');             rpath = rpath.substring(0, selectIndex1 + 6);             path = path.substring(0, selectIndex2 + 6);         }         if (id == '') {             id = 'null';         }         newPath = String(rpath) + ';' + String(id) + ';' + String(path) + ';'  + ssname + ';' + sstagname + ';' + ssclassname;         if (textvalue == '' || textvalue.length == 0 || textvalue == '0') {             textvalue = 'NONAME' + nonamecounter;             nonamecounter = nonamecounter + 1;             custname = textvalue;         } else {             custname = textvalue;         }         if (tagtype != '') {             custname = custname + '_' + tagtype;         } else {             custname = custname + '_elmnt';         }         if (tagname == 'select') {             f.removeAttribute('disabled');             f.setAttribute('enabled', 'enabled');         }         for (var i = 0; i < arr.length; i++) {             if (arr[i].xpath == newPath) {                 uniqueFlag = true;                 break;             }         };         if (uniqueFlag == false) {             arr.push({                 'xpath': newPath,                 'url': url,                 'text': textvalue,                 'hiddentag': ishidden,                 'custname': custname,                 'tag': tagname,                 'id': id             });         }     }     return arr; }  function isVisible(elem) {     function inside(child, parent) {         while (child) {             if (child === parent) return true;             child = child.parentNode;         }         return false;     };     if (document.hidden || elem.offsetWidth == 0 || elem.offsetHeight == 0 || elem.style.visibility == 'hidden' || elem.style.display == 'none' || elem.style.opacity === 0) return false;     var rect = elem.getBoundingClientRect();     if (window.getComputedStyle || elem.currentStyle) {         var el = elem,             comp = null;         while (el) {             if (el === document) {                 break;             } else if (!el.parentNode) return false;             comp = window.getComputedStyle ? window.getComputedStyle(el, null) : el.currentStyle;             if (comp && (comp.visibility == 'hidden' || comp.display == 'none' || (typeof comp.opacity !== 'undefined' && !(comp.opacity > 0)))) return false;             el = el.parentNode;         }     }     return true; };  function text_content(f) {     var firstText = '';     var textdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var curNode = f.childNodes[z];         whitespace = /^\s*$/;         if (curNode.nodeName === '#text' && !(whitespace.test(curNode.nodeValue))) {             firstText = curNode.nodeValue;             textdisplay = textdisplay + firstText;         }     }     return (textdisplay); };  function addNodesOuter(array, collection) {     for (var i = 0; collection && collection.length && i < collection.length; i++) {         array.push(collection[i]);     } };  return getElementProperties(element);"""
                            element_properties = []
                            element_properties = driver.execute_script(properties_script,webElement[0],url)
                            new_properties=element_properties[0];
                            if cmp(element,new_properties)!=0:
                                print 'object changed'
                                lst.append(new_properties)
                            else:
                                lst.append(element)
                    try:
                        driver.switch_to.window(currentdriverhandle)
                    except Exception as e4:
                        evb = e4
                else:
                    print 'element not found'

            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            Exceptions.error(e)
            status= domconstants.STATUS_FAIL
        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Highlight method execution done ')
        return status


