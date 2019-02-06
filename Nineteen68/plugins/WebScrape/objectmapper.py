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

import browserops
import time
import logging
log = logging.getLogger("objectmapper.py")
class Highlight():

        def highlight(self,element):
                if element is not None:
                    """Highlights (blinks) a Selenium Webdriver element"""

                    driver=browserops.driver
                    def apply_style(s, sec):
                        try:
                            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                                  element, s)
                        except Exception as e1:
                            evb = e1
                        time.sleep(0.1)
                    try:
                        original_style = element.get_attribute('style')
                    except Exception as e6:
                        evb = e6
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'end', behavior: 'smooth'});", element)
                    except Exception as e2:
                        evb = e2
                    apply_style(original_style + "background: #fff300; border: 2px solid #cc3300;outline: 2px solid #fff300;", 3)


        def find_element(self,data,element):

                    highele = data.split(',')

                    # find out if the highele[1] has id or name attrib
                    identifiers = highele[0].split(';')
                    self.url = highele[1]

                    try:
                            #find by rxpath
                            driver=browserops.driver

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

                            self.highlight(webElement[0])
                            properties_script="""if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('select');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var useIdx = true; var useId = true; var useClass = true; var relative = true; var ae = []; var be = []; var element = arguments[0]; var url = arguments[1]; var ishidden = 0; var tagname = 0; var textvalue = ''; var arr = []; var custname = ''; var tagtype = ''; var multipleFlag = false; var uniqueFlag = false; var nonamecounter = 1; var isIE = /*@cc_on!@*/ false || !!document.documentMode;   return getElementProperties(element);   function getElementProperties(element) {     tagtype = '';     arr = [];     var e = element;     var f = element;     var className = e.className;     var rpath = '';     var firstpass = 0;     for (var path = ''; e && e.nodeType == 1; e = e.parentNode) {         var predicate = [];         var siblings = e.parentNode.children;         var count = 0;         var unique = false;         for (var i = 0; siblings && (i < siblings.length); i++) {             if (siblings[i].tagName == e.tagName) {                 count++;                 if (siblings[i] == e) {                     idx = count;                 }             }         }         if (idx == 1 && count == 1) {             idx = null;         }         if (useId && e.id) {             predicate[predicate.length] = '@id=' + '"' + e.id + '"';             unique = true;         }         xidx = (useIdx && idx) ? ('[' + idx + ']') : '';         idx = (useIdx && idx && !unique) ? ('[' + idx + ']') : '';         predicate = (predicate.length > 0) ? ('[' + predicate.join(' and ') + ']') : '';         path = '/' + e.tagName.toLowerCase() + xidx + path;         if (firstpass == 0) {             if (unique && relative) {                 rpath = '//*' + idx + predicate + rpath;                 firstpass = 1;             } else {                 rpath = '/' + e.tagName.toLowerCase() + idx + predicate + rpath;             }         }     }     ishidden = isVisible(f);     if (ishidden == true || ishidden == 'True' || ishidden == 'true') {         ishidden = 'No';     } else {         ishidden = 'Yes';     }     var tagname = f.tagName.toLowerCase();     if (tagname.indexOf(':') != -1) {         tagname = tagname.replace(':', '');         tagname = 'custom' + tagname;     }     id = f.id;     name = f.name;     placeholder = f.placeholder;     id = (String(id));     name = (String(name));     placeholder = (String(placeholder));     var textvalue = text_content(f);     textvalue = (String(textvalue));     if (tagname != 'script' && tagname != 'meta' && tagname != 'html' && tagname != 'head' && tagname != 'style' && tagname != 'body' && tagname != 'form' && tagname != 'link' && tagname != 'noscript' && tagname != '!' && tagname != 'code' && tagname != 'animatetransform') {         if (textvalue == '' || textvalue == 'null' || textvalue == 'undefined' || textvalue == '0') {             if (name != '' && name != 'undefined') {                 names = document.getElementsByName(name);                 if (names.length > 1) {                     for (var k = 0; k < names.length; k++) {                         if (f == names[k]) {                             textvalue = name + k;                         }                     }                 } else {                     textvalue = name;                 }             } else if (id != '' && id != 'undefined') {                 textvalue = id;             } else if (placeholder != '' && placeholder != 'undefined') {                 textvalue = placeholder;             } else {                 textvalue = 'NONAME' + nonamecounter;                 nonamecounter = nonamecounter + 1;             }         }         if (tagname == 'select') {             f.setAttribute('disabled', 'disabled');             multipleFlag = f.hasAttribute('multiple');         }         var etype = f.getAttribute('type');         etype = (String(etype)).toLowerCase();         var newPath = path;         if (tagname == 'textarea') {             tagname = 'input';             tagtype = 'txtarea';         } else if (tagname == 'select' && multipleFlag) {             tagname = 'list';             tagtype = 'lst';         } else if (tagname == 'select') {             tagtype = 'select';         } else if (tagname == 'td') {             tagname = 'tablecell';             tagtype = 'tblcell';         } else if (tagname == 'a') {             tagtype = 'lnk';         } else if (tagname == 'table') {             tagtype = 'tbl';         } else if (tagname == 'img') {             tagtype = 'img';         } else if (tagname == 'input' && etype == 'image') {             tagname = 'img';             tagtype = 'img';         }         if (tagname == 'input' && (etype == 'button' || etype == 'submit' || etype == 'reset' || etype == 'file')) {             tagname = 'button';             tagtype = 'btn';         } else if (tagname == 'input' && etype == 'radio') {             tagname = 'radiobutton';             tagtype = 'radiobtn';         } else if (tagname == 'input' && etype == 'checkbox') {             tagname = 'checkbox';             tagtype = 'chkbox';         } else if (tagname == 'input' && (etype == 'text' || etype == 'email' || etype == 'number' || etype == 'password' || etype == 'range' || etype == 'search' || etype == 'url')) {             tagname = 'input';             tagtype = 'txtbox';         } else if (tagname == 'option' && f.parentNode.hasAttribute('multiple')) {             tagname = 'list';             var selectIndex1 = rpath.indexOf('select');             var selectIndex2 = path.indexOf('select');             rpath = rpath.substring(0, selectIndex1 + 6);             path = path.substring(0, selectIndex2 + 6);         }         if (id == '') {             id = 'null';         }         newPath = String(rpath) + ';' + String(id) + ';' + String(path) + ';' + 'null' + ';' + 'null' + ';' + 'null';         if (textvalue == '' || textvalue.length == 0 || textvalue == '0') {             textvalue = 'NONAME' + nonamecounter;             nonamecounter = nonamecounter + 1;             custname = textvalue;         } else {             custname = textvalue;         }         if (tagtype != '') {             custname = custname + '_' + tagtype;         } else {             custname = custname + '_elmnt';         }         if (tagname == 'select') {             f.removeAttribute('disabled');             f.setAttribute('enabled', 'enabled');         }         for (var i = 0; i < arr.length; i++) {             if (arr[i].xpath == newPath) {                 uniqueFlag = true;                 break;             }         };         if (uniqueFlag == false) {             arr.push({                 'xpath': newPath,                 'url': url,                 'text': textvalue,                 'hiddentag': ishidden,                 'custname': custname,                 'tag': tagname,                 'id': id             });         }     }     return arr; }    function  isVisible(elem){ 	function inside(child, parent) {         while (child) {             if (child === parent) return true;             child = child.parentNode;         }         return false;     };             if (document.hidden || elem.offsetWidth == 0 || elem.offsetHeight == 0 || elem.style.visibility == 'hidden' || elem.style.display == 'none' || elem.style.opacity === 0) return false;         var rect = elem.getBoundingClientRect();         if (window.getComputedStyle || elem.currentStyle) {             var el = elem,                 comp = null;             while (el) {                 if (el === document) {                     break;                 } else if (!el.parentNode) return false;                 comp = window.getComputedStyle ? window.getComputedStyle(el, null) : el.currentStyle;                 if (comp && (comp.visibility == 'hidden' || comp.display == 'none' || (typeof comp.opacity !== 'undefined' && !(comp.opacity > 0)))) return false;                 el = el.parentNode;             }         }             return true; }; function text_content(f) {     var firstText = '';     var textdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var curNode = f.childNodes[z];         whitespace = /^\s*$/;         if (curNode.nodeName === '#text' && !(whitespace.test(curNode.nodeValue))) {             firstText = curNode.nodeValue;             textdisplay = textdisplay + firstText;         }     }     return (textdisplay); };   function addNodesOuter(array, collection) {     for (var i = 0; collection && collection.length && i < collection.length; i++) {         array.push(collection[i]);     } };"""
                            element_properties = []
                            element_properties = driver.execute_script(properties_script,webElement[0],self.url)
                            new_properties=element_properties[0];
                            if (element>new_properties)-(element<new_properties)!=0:
                                log.info('object is changed')
                                return new_properties
                        try:
                            driver.switch_to.default_content()
                        except Exception as e4:
                            evb = e4

                    else:

                        try:

                            driver.switch_to.default_content()

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
                                    evb = webEx
                        if webElement is not None:

                            self.highlight(webElement[0])

                            properties_script="""if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('select');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var useIdx = true; var useId = true; var useClass = true; var relative = true; var ae = []; var be = []; var element = arguments[0]; var url = arguments[1]; var ishidden = 0; var tagname = 0; var textvalue = ''; var arr = []; var custname = ''; var tagtype = ''; var multipleFlag = false; var uniqueFlag = false; var nonamecounter = 1; var isIE = /*@cc_on!@*/ false || !!document.documentMode;   return getElementProperties(element);   function getElementProperties(element) {     tagtype = '';     arr = [];     var e = element;     var f = element;     var className = e.className;     var rpath = '';     var firstpass = 0;     for (var path = ''; e && e.nodeType == 1; e = e.parentNode) {         var predicate = [];         var siblings = e.parentNode.children;         var count = 0;         var unique = false;         for (var i = 0; siblings && (i < siblings.length); i++) {             if (siblings[i].tagName == e.tagName) {                 count++;                 if (siblings[i] == e) {                     idx = count;                 }             }         }         if (idx == 1 && count == 1) {             idx = null;         }         if (useId && e.id) {             predicate[predicate.length] = '@id=' + '"' + e.id + '"';             unique = true;         }         xidx = (useIdx && idx) ? ('[' + idx + ']') : '';         idx = (useIdx && idx && !unique) ? ('[' + idx + ']') : '';         predicate = (predicate.length > 0) ? ('[' + predicate.join(' and ') + ']') : '';         path = '/' + e.tagName.toLowerCase() + xidx + path;         if (firstpass == 0) {             if (unique && relative) {                 rpath = '//*' + idx + predicate + rpath;                 firstpass = 1;             } else {                 rpath = '/' + e.tagName.toLowerCase() + idx + predicate + rpath;             }         }     }     ishidden = isVisible(f);     if (ishidden == true || ishidden == 'True' || ishidden == 'true') {         ishidden = 'No';     } else {         ishidden = 'Yes';     }     var tagname = f.tagName.toLowerCase();     if (tagname.indexOf(':') != -1) {         tagname = tagname.replace(':', '');         tagname = 'custom' + tagname;     }     id = f.id;     name = f.name;     placeholder = f.placeholder;     id = (String(id));     name = (String(name));     placeholder = (String(placeholder));     var textvalue = text_content(f);     textvalue = (String(textvalue));     if (tagname != 'script' && tagname != 'meta' && tagname != 'html' && tagname != 'head' && tagname != 'style' && tagname != 'body' && tagname != 'form' && tagname != 'link' && tagname != 'noscript' && tagname != '!' && tagname != 'code' && tagname != 'animatetransform') {         if (textvalue == '' || textvalue == 'null' || textvalue == 'undefined' || textvalue == '0') {             if (name != '' && name != 'undefined') {                 names = document.getElementsByName(name);                 if (names.length > 1) {                     for (var k = 0; k < names.length; k++) {                         if (f == names[k]) {                             textvalue = name + k;                         }                     }                 } else {                     textvalue = name;                 }             } else if (id != '' && id != 'undefined') {                 textvalue = id;             } else if (placeholder != '' && placeholder != 'undefined') {                 textvalue = placeholder;             } else {                 textvalue = 'NONAME' + nonamecounter;                 nonamecounter = nonamecounter + 1;             }         }         if (tagname == 'select') {             f.setAttribute('disabled', 'disabled');             multipleFlag = f.hasAttribute('multiple');         }         var etype = f.getAttribute('type');         etype = (String(etype)).toLowerCase();         var newPath = path;         if (tagname == 'textarea') {             tagname = 'input';             tagtype = 'txtarea';         } else if (tagname == 'select' && multipleFlag) {             tagname = 'list';             tagtype = 'lst';         } else if (tagname == 'select') {             tagtype = 'select';         } else if (tagname == 'td') {             tagname = 'tablecell';             tagtype = 'tblcell';         } else if (tagname == 'a') {             tagtype = 'lnk';         } else if (tagname == 'table') {             tagtype = 'tbl';         } else if (tagname == 'img') {             tagtype = 'img';         } else if (tagname == 'input' && etype == 'image') {             tagname = 'img';             tagtype = 'img';         }         if (tagname == 'input' && (etype == 'button' || etype == 'submit' || etype == 'reset' || etype == 'file')) {             tagname = 'button';             tagtype = 'btn';         } else if (tagname == 'input' && etype == 'radio') {             tagname = 'radiobutton';             tagtype = 'radiobtn';         } else if (tagname == 'input' && etype == 'checkbox') {             tagname = 'checkbox';             tagtype = 'chkbox';         } else if (tagname == 'input' && (etype == 'text' || etype == 'email' || etype == 'number' || etype == 'password' || etype == 'range' || etype == 'search' || etype == 'url')) {             tagname = 'input';             tagtype = 'txtbox';         } else if (tagname == 'option' && f.parentNode.hasAttribute('multiple')) {             tagname = 'list';             var selectIndex1 = rpath.indexOf('select');             var selectIndex2 = path.indexOf('select');             rpath = rpath.substring(0, selectIndex1 + 6);             path = path.substring(0, selectIndex2 + 6);         }         if (id == '') {             id = 'null';         }         newPath = String(rpath) + ';' + String(id) + ';' + String(path) + ';' + 'null' + ';' + 'null' + ';' + 'null';         if (textvalue == '' || textvalue.length == 0 || textvalue == '0') {             textvalue = 'NONAME' + nonamecounter;             nonamecounter = nonamecounter + 1;             custname = textvalue;         } else {             custname = textvalue;         }         if (tagtype != '') {             custname = custname + '_' + tagtype;         } else {             custname = custname + '_elmnt';         }         if (tagname == 'select') {             f.removeAttribute('disabled');             f.setAttribute('enabled', 'enabled');         }         for (var i = 0; i < arr.length; i++) {             if (arr[i].xpath == newPath) {                 uniqueFlag = true;                 break;             }         };         if (uniqueFlag == false) {             arr.push({                 'xpath': newPath,                 'url': url,                 'text': textvalue,                 'hiddentag': ishidden,                 'custname': custname,                 'tag': tagname,                 'id': id             });         }     }     return arr; }    function  isVisible(elem){ 	function inside(child, parent) {         while (child) {             if (child === parent) return true;             child = child.parentNode;         }         return false;     };             if (document.hidden || elem.offsetWidth == 0 || elem.offsetHeight == 0 || elem.style.visibility == 'hidden' || elem.style.display == 'none' || elem.style.opacity === 0) return false;         var rect = elem.getBoundingClientRect();         if (window.getComputedStyle || elem.currentStyle) {             var el = elem,                 comp = null;             while (el) {                 if (el === document) {                     break;                 } else if (!el.parentNode) return false;                 comp = window.getComputedStyle ? window.getComputedStyle(el, null) : el.currentStyle;                 if (comp && (comp.visibility == 'hidden' || comp.display == 'none' || (typeof comp.opacity !== 'undefined' && !(comp.opacity > 0)))) return false;                 el = el.parentNode;             }         }             return true; }; function text_content(f) {     var firstText = '';     var textdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var curNode = f.childNodes[z];         whitespace = /^\s*$/;         if (curNode.nodeName === '#text' && !(whitespace.test(curNode.nodeValue))) {             firstText = curNode.nodeValue;             textdisplay = textdisplay + firstText;         }     }     return (textdisplay); };   function addNodesOuter(array, collection) {     for (var i = 0; collection && collection.length && i < collection.length; i++) {         array.push(collection[i]);     } };"""
                            element_properties = []
                            element_properties = driver.execute_script(properties_script,webElement[0],self.url)
                            new_properties=element_properties[0];
                            if (element>new_properties)-(element<new_properties)!=0:
                                log.info('object is changed')
                                return new_properties
                            else:
                                return element
                        else:
                            log.info('The element '+ str(element['custname']) +'  is not found')
                            return element

                    #win32gui.ShowWindow(hwndg, win32con.SW_MINIMIZE)
