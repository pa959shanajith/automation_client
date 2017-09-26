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
from selenium import webdriver
status =domconstants.STATUS_FAIL
currentdriverhandle = None
import logging
import logging.config
log = logging.getLogger('highlight.py')
class Highlight():
    changedobject = []
    notchangedobject = []
    notfoundobject= []

    def __init__(self):
        self.changedobject=[]
        self.notchangedobject=[]
        self.notfoundobject=[]
    def highlight(self,data,element,handle):
        try:
            action=''
            log.info('Inside highlight method .....')
            driver = browserops.driver
            currentdriverhandle = clickandadd.currenthandle
            log.info(' Obtained browser handle and driver from browserops.py class ......')
            if currentdriverhandle is  '' or currentdriverhandle is  None:
                currentdriverhandle = fullscrape.currenthandle
            if currentdriverhandle is  '' or currentdriverhandle is  None:
                currentdriverhandle = handle
            try:
                if currentdriverhandle!= None:
                    driver.switch_to.window(currentdriverhandle)
                else:
                    driver.switch_to.default_content()
            except Exception as e4:
                evb = e4

            if(type(data)== tuple):
                highele = list(data)
            else:
            #Split the string with delimiter ','
                highele = data.split(',')
            # find out if the highele[1] has id or name attrib
            if  highele[0] == 'OBJECTMAPPER':
                action='OBJECTMAPPER'
                identifiers = highele[1].split(';')
                url = highele[len(highele) - 1]
            else:
                identifiers = highele[0].split(';')
                url = highele[len(highele) - 2]

            def highlight1(element):
                log.info(' Inside highlight1 method .....')
                if element is not None:
                    """Highlights (blinks) a Selenium Webdriver element"""
                    def apply_style(s, sec):
                        log.info('Inside apply_style method .....')
                        if driver.name == 'internet explorer' :
                            log.info('Before applying color to the element in IE browser .....')
                            driver.execute_script("arguments[0].style.setAttribute('cssText', arguments[1]);",
                                              element, s)
                            log.info('Applied color to the element in IE browser .....')
                        else:
                            log.info('Before applying color to the element in chrome/firefox browser .....')
                            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                              element, s)
                            log.info('Applied color to the element in chrome/firefox browser .....')
                        if(action=='OBJECTMAPPER'):
                            driver.execute_script("""element = arguments[0]; className = element.className; element.setAttribute('class', className + ' SLKNineteen68_Highlight');""",element)
                            time.sleep(0.1)
                        else:
                            time.sleep(sec)
                    log.info('Before getting the original style .....')
                    original_style = element.get_attribute('style')

                    original_style_background = element.value_of_css_property('background')
                    original_style_border = element.value_of_css_property('border')
                    original_style_outline = element.value_of_css_property('outline')

                    log.info('Original style obtained.....')
                    log.info('Before highlighting .....')
                    apply_style(str(original_style) + "background: #fff300 !important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;", 3)
                    log.info('Element highlighted .....')

                    if driver.name == 'internet explorer' :
                        if (driver.capabilities['version'] != unicode(8)):
                            log.info('FILE: highlight.py , DEF: highlight1() , MSG: Before removing the style for ie8 .....')
                            if(action!='OBJECTMAPPER'):
                                apply_style(original_style, 0)
                                log.info('Removed the style for ie8 .....')
                    else:
                        log.info('Before removing the style for other browsers .....')
                        if(action!='OBJECTMAPPER'):
                            extra_style = ""
                            if original_style_background is None:
                                extra_style = extra_style + "background: 0; "
                            if original_style_border is None:
                                extra_style = extra_style + "border: 0px none; "
                            if original_style_outline is None:
                                extra_style = extra_style + "outline: none"


                            apply_style(str(original_style) + extra_style, 0)
                            log.info('Removed the style for other browsers .....')

            def is_int(url):
                try:
                    int(url[0])
                    log.info('The url is an iframe/frmae url .....')
                    return True
                except ValueError:
                    log.info('The url is an normal webpage url .....')
                    return False
            if is_int(url):
                log.info('Splitting Iframe/frame url by /')
                indiframes = url.split("/")
                try:
                    if currentdriverhandle!= None:
                        driver.switch_to.window(currentdriverhandle)
                    else:
                        driver.switch_to.default_content()
                except Exception as e4:
                    evb = e4
##                driver.switch_to.default_content()
                log.info('Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = 'frame'
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'i':
                            frame_iframe = 'iframe'
                            log.info('It is  iframe')
                        else:
                            log.info('It is  frame')
                        if j=='':
                            continue
##                        print 'Driver url befor switch :', driver.current_url
                        driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
##                        print 'Driver urlafter switch:', driver.current_url
                        log.info('Switched to frame/iframe')


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
                    log.info('Element found inside frame/iframe .....')
                    if(action=='OBJECTMAPPER'):
                            properties_script="""if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) { 	(function () { 		function hasAttribute(attrName) { 			return typeof this[attrName] !== 'undefined'; 		} 		var inputs = document.getElementsByTagName('*'); 		for (var i = 0; i < inputs.length; i++) { 			inputs[i].hasAttribute = hasAttribute; 		} 	} 		()); } if (!window.Element || !window.Element.prototype || !window.Element.prototype.getAttribute) { 	(function () { 		function getAttribute(attrName) { 			return typeof this[attrName] !== 'undefined'; 		} 		var inputs = document.getElementsByTagName('*'); 		for (var i = 0; i < inputs.length; i++) { 			inputs[i].getAttribute = getAttribute; 		} 	} 		()); } (function () { 	if (!document.getElementsByClassName) { 		var indexOf = [].indexOf || function (prop) { 			for (var i = 0; i < this.length; i++) { 				if (this[i] === prop) 					return i; 			} 			return -1; 		}; 		getElementsByClassName = function (className, context) { 			var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function () { 					var all = context.getElementsByTagName("*"), 					elements = [], 					i = 0; 					for (; i < all.length; i++) { 						if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) 							elements.push(all[i]); 					} 					return elements; 				})(); 			return elems; 		}; 		document.getElementsByClassName = function (className) { 			return getElementsByClassName(className, document); 		}; 		if (window.Element) { 			window.Element.prototype.getElementsByClassName = function (className) { 				return getElementsByClassName(className, this); 			}; 		} 	} })(); var suseIdx = true; var suseId = true; var suseClass = true; var srelative = true; var sae = []; var sarr = []; var sele = document.getElementsByTagName('*'); var smyid = 0; var stextvalue = ''; var stagname = 0; var sishidden = 0; var scustname = ''; var smultipleFlag = false; var element = arguments[0]; var surl = arguments[1]; var snonamecounter = 1; var txt_area_nonamecounter = 1; var select_nonamecounter = 1; var td_nonamecounter = 1; var a_nonamecounter = 1; var table_nonamecounter = 1; var input_nonamecounter = 1; var stagtype = ''; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var sclassname = 'null'; var top = 0; var left = 0; var height = 0; var width = 0; var coordinates = ''; var sisVisible = (function () { 	function inside(schild, sparent) { 		while (schild) { 			if (schild === sparent) 				return true; 			schild = schild.parentNode; 		} 		return false; 	}; 	return function (selem) { 		if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) 			return false; 		var srect = selem.getBoundingClientRect(); 		if (window.getComputedStyle || selem.currentStyle) { 			var sel = selem, 			scomp = null; 			while (sel) { 				if (sel === document) { 					break; 				} else if (!sel.parentNode) 					return false; 				scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle; 				if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) 					return false; 				sel = sel.parentNode; 			} 		} 		return true; 	} })(); function getElementProperties(element) { 									  	stagtype = ''; 	ssname = 'null'; 	sstagname = 'null'; 	sid = element.id; 	sname = element.name; 	salttext = element.alt; 	splaceholder = element.placeholder; 	sclassname = element.className; 	sid = (String(sid)); 	sclassname = (String(sclassname)); 	sname = (String(sname)); 	splaceholder = (String(splaceholder)); 	stextvalue = stext_content(element); 	stextvalue = (String(stextvalue)); 	stagname = element.tagName.toLowerCase(); 	ssname = 'null'; 	sstagname = 'null'; 	ssclassname = 'null'; 	findCoordinates(element); 	if (stagname.indexOf(':') != -1) { 		stagname = stagname.replace(':', ''); 		stagname = 'custom' + stagname; 	} 	if (sname != '' && sname != 'undefined') { 		snames = document.getElementsByName(sname); 		if (snames.length > 1) { 			for (var k = 0; k < snames.length; k++) { 				if (element == snames[k]) { 					ssname = sname + '[' + k + ']' 				} 			} 		} else { 			ssname = sname; 		} 	} 	if (stagname != '' && stagname != 'undefined') { 		stagnames = document.getElementsByTagName(stagname); 		if (stagnames.length > 1) { 			for (var k = 0; k < stagnames.length; k++) { 				if (element == stagnames[k]) { 					sstagname = stagname + '[' + k + ']' 				} 			} 		} else { 			sstagname = stagname; 		} 	} 	if (sclassname != '' && sclassname != 'undefined') { 		sclassnames = document.getElementsByClassName(sclassname); 		if (sclassnames.length > 1) { 			for (var k = 0; k < sclassnames.length; k++) { 				if (element == sclassnames[k]) { 					ssclassname = sclassname + '[' + k + ']' 				} 			} 		} else { 			ssclassname = sclassname; 		} 	} 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') { 			if (sname != '' && sname != 'undefined') { 				snames = document.getElementsByName(sname); 				if (snames.length > 1) { 					for (var k = 0; k < snames.length; k++) { 						if (element == snames[k]) { 							stextvalue = sname + k; 						} 					} 				} else { 					stextvalue = sname; 				} 			} else if (sid != '' && sid != 'undefined') { 				stextvalue = sid; 			} else if (splaceholder != '' && splaceholder != 'undefined') { 				stextvalue = splaceholder; 			} else { 				var seles = document.getElementsByTagName(stagname); 				for (var k = 0; k < seles.length; k++) { 					if (element == seles[k]) { 														 		   				  															  													 		   			  														  											 		   			 														 										   		   				 						stextvalue = stagname + '_NONAME' + (k + 1); 					} 		   				 															 												   		   			 											 										 				} 			} 		} 		if (sid == '') { 			sid = 'null'; 		} 		smultipleFlag = element.hasAttribute('multiple'); 		sishidden = sisVisible(element); 		if (sishidden == true || sishidden == 'True' || sishidden == 'true') { 			sishidden = 'No'; 		} else { 			sishidden = 'Yes'; 		} 		var sfirstpass = 0; 		var srpath = ''; 		var setype = element.getAttribute('type'); 		setype = (String(setype)).toLowerCase(); 		for (var spath = ''; element && element.nodeType == 1; element = element.parentNode) { 			var spredicate = []; 			var ssiblings = element.parentNode.children; 			var scount = 0; 			var sunique = false; 			var snewPath = ''; 			var sidx = 0; 			for (var i = 0; ssiblings && (i < ssiblings.length); i++) { 				if (ssiblings[i].tagName == element.tagName) { 					scount++; 					if (ssiblings[i] == element) { 						sidx = scount; 					} 				} 			} 			if (sidx == 1 && scount == 1) { 				sidx = null; 			} 			if (suseId && element.id) { 				spredicate[spredicate.length] = '@id=' + '"' + element.id + '"'; 				sunique = true; 			} 			xidx = (suseIdx && sidx) ? ('[' + sidx + ']') : ''; 			sidx = (suseIdx && sidx && !sunique) ? ('[' + sidx + ']') : ''; 			spredicate = (spredicate.length > 0) ? ('[' + spredicate.join(' and ') + ']') : ''; 			spath = '/' + element.tagName.toLowerCase() + xidx + spath; 			if (sfirstpass == 0) { 				if (sunique && srelative) { 					srpath = '//*' + sidx + spredicate + srpath; 					sfirstpass = 1; 				} else { 					srpath = '/' + element.tagName.toLowerCase() + sidx + spredicate + srpath; 				} 			} 		} 		if (stagname == 'textarea') { 			stagname = 'input'; 			stagtype = 'txtarea'; 		} else if (stagname == 'select' && smultipleFlag) { 			stagname = 'list'; 			stagtype = 'lst'; 		} else if (stagname == 'select') { 			stagtype = 'select'; 		} else if (stagname == 'td' || stagname == 'tr') { 			stagname = 'tablecell'; 			stagtype = 'tblcell'; 		} else if (stagname == 'a') { 			stagtype = 'lnk'; 		} else if (stagname == 'table') { 			stagtype = 'tbl'; 		} else if (stagname == 'img') { 			stagtype = 'img'; 		} else if (stagname == 'input' && setype == 'image') { 			stagname = 'img'; 			stagtype = 'img'; 		} 		if (stagname == 'input' && (setype == 'button' || setype == 'submit' || setype == 'reset' || setype == 'file')) { 			stagname = 'button'; 			stagtype = 'btn'; 		} else if (stagname == 'input' && setype == 'radio') { 			stagname = 'radiobutton'; 			stagtype = 'radiobtn'; 		} else if (stagname == 'input' && setype == 'checkbox') { 			stagname = 'checkbox'; 			stagtype = 'chkbox'; 		} else if (stagname == 'input' && (setype == 'text' || setype == 'email' || setype == 'number' || setype == 'password' || setype == 'range' || setype == 'search' || setype == 'url')) { 			stagname = 'input'; 			stagtype = 'txtbox'; 																								 					 					  									 					   					 		} 		else if (stagname == 'input' && stagtype == '' && (setype == 'hidden' || setype == 'null')) { 			stagname = 'div'; 			stagtype = 'elmnt'; 		} else if (stagname == 'button') { 			stagname = 'button'; 			stagtype = 'btn'; 		} 		stextvalue = stextvalue.replace(">", ""); 		stextvalue = stextvalue.replace("</", ""); 		stextvalue = stextvalue.replace("<", ""); 		stextvalue = stextvalue.replace("/>", ""); 		stextvalue = stextvalue.split("\\n").join(""); 		stextvalue = stextvalue.split("\\t").join(""); 		stextvalue = stextvalue.split("\\r").join(""); 		stextvalue = stextvalue.split("  ").join(""); 		stextvalue = stextvalue.split("\u00a0").join("");										 					   										  		  									 		if (stextvalue == '' || stextvalue.length == 0 || stextvalue == '0') { 			stextvalue = 'NONAME' + snonamecounter; 			snonamecounter = snonamecounter + 1; 			scustname = stextvalue; 		} else { 			scustname = stextvalue; 		} 		if (stagtype != '') { 			scustname = scustname + '_' + stagtype; 		} else { 			scustname = scustname + '_elmnt'; 		} 		coordinates = left + ';' + top + ';' + height + ';' + width; 		coordinates = String(coordinates); 		snewPath = String(srpath) + ';' + String(sid) + ';' + String(spath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + stextvalue; 		sarr.push({ 			'xpath': snewPath, 			'tag': stagname, 			'hiddentag': sishidden, 			'url': surl, 			'height': height, 			'width': width, 			'custname': scustname, 			'top': top, 			'left': left 		}); 	} 	return sarr; }  function findCoordinates(element) { 	height = element.offsetHeight; 	width = element.offsetWidth; 	top = 0; 	left = 0; 	do { 		top += element.offsetTop || 0; 		left += element.offsetLeft || 0; 		element = element.offsetParent; 	} while (element); } function saddNodesOuter(sarray, scollection) { 	for (var i = 0; scollection && scollection.length && i < scollection.length; i++) { 		sarray.push(scollection[i]); 	} }; function stext_content(f) { 	var sfirstText = ''; 	var stextdisplay = ''; 	for (var z = 0; z < f.childNodes.length; z++) { 		var scurNode = f.childNodes[z]; 		swhitespace = /^\s*$/; 		if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) { 			sfirstText = scurNode.nodeValue; 			stextdisplay = stextdisplay + sfirstText; 		} 	} 	return (stextdisplay); }; return getElementProperties(element);"""
                            element_properties = []
                            element_properties = driver.execute_script(properties_script,webElement[0],url)
                            new_properties=element_properties[0];
                            if cmp(element['xpath'],new_properties['xpath'])!=0:
                                self.changedobject.append(new_properties)
                                highlight1(webElement[0])
                            else:
                                 self.notchangedobject.append(element)
                    else:
                        highlight1(webElement[0])
                else:
                    self.notfoundobject.append(element)
                try:
                    if currentdriverhandle!= None:
                        driver.switch_to.window(currentdriverhandle)
                    else:
                        driver.switch_to.default_content()
                except Exception as e4:
                    evb = e4

            else:
                try:
                    if currentdriverhandle!= None:
                        driver.switch_to.window(currentdriverhandle)
                    else:
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
                            webElement = None
                if webElement is not None:
                    log.info('Element found inside main page .....')
                    if(action=='OBJECTMAPPER'):
                            properties_script="""if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) { 	(function () { 		function hasAttribute(attrName) { 			return typeof this[attrName] !== 'undefined'; 		} 		var inputs = document.getElementsByTagName('*'); 		for (var i = 0; i < inputs.length; i++) { 			inputs[i].hasAttribute = hasAttribute; 		} 	} 		()); } if (!window.Element || !window.Element.prototype || !window.Element.prototype.getAttribute) { 	(function () { 		function getAttribute(attrName) { 			return typeof this[attrName] !== 'undefined'; 		} 		var inputs = document.getElementsByTagName('*'); 		for (var i = 0; i < inputs.length; i++) { 			inputs[i].getAttribute = getAttribute; 		} 	} 		()); } (function () { 	if (!document.getElementsByClassName) { 		var indexOf = [].indexOf || function (prop) { 			for (var i = 0; i < this.length; i++) { 				if (this[i] === prop) 					return i; 			} 			return -1; 		}; 		getElementsByClassName = function (className, context) { 			var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function () { 					var all = context.getElementsByTagName("*"), 					elements = [], 					i = 0; 					for (; i < all.length; i++) { 						if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) 							elements.push(all[i]); 					} 					return elements; 				})(); 			return elems; 		}; 		document.getElementsByClassName = function (className) { 			return getElementsByClassName(className, document); 		}; 		if (window.Element) { 			window.Element.prototype.getElementsByClassName = function (className) { 				return getElementsByClassName(className, this); 			}; 		} 	} })(); var suseIdx = true; var suseId = true; var suseClass = true; var srelative = true; var sae = []; var sarr = []; var sele = document.getElementsByTagName('*'); var smyid = 0; var stextvalue = ''; var stagname = 0; var sishidden = 0; var scustname = ''; var smultipleFlag = false; var element = arguments[0]; var surl = arguments[1]; var snonamecounter = 1; var txt_area_nonamecounter = 1; var select_nonamecounter = 1; var td_nonamecounter = 1; var a_nonamecounter = 1; var table_nonamecounter = 1; var input_nonamecounter = 1; var stagtype = ''; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var sclassname = 'null'; var top = 0; var left = 0; var height = 0; var width = 0; var coordinates = ''; var sisVisible = (function () { 	function inside(schild, sparent) { 		while (schild) { 			if (schild === sparent) 				return true; 			schild = schild.parentNode; 		} 		return false; 	}; 	return function (selem) { 		if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) 			return false; 		var srect = selem.getBoundingClientRect(); 		if (window.getComputedStyle || selem.currentStyle) { 			var sel = selem, 			scomp = null; 			while (sel) { 				if (sel === document) { 					break; 				} else if (!sel.parentNode) 					return false; 				scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle; 				if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) 					return false; 				sel = sel.parentNode; 			} 		} 		return true; 	} })(); function getElementProperties(element) { 									  	stagtype = ''; 	ssname = 'null'; 	sstagname = 'null'; 	sid = element.id; 	sname = element.name; 	salttext = element.alt; 	splaceholder = element.placeholder; 	sclassname = element.className; 	sid = (String(sid)); 	sclassname = (String(sclassname)); 	sname = (String(sname)); 	splaceholder = (String(splaceholder)); 	stextvalue = stext_content(element); 	stextvalue = (String(stextvalue)); 	stagname = element.tagName.toLowerCase(); 	ssname = 'null'; 	sstagname = 'null'; 	ssclassname = 'null'; 	findCoordinates(element); 	if (stagname.indexOf(':') != -1) { 		stagname = stagname.replace(':', ''); 		stagname = 'custom' + stagname; 	} 	if (sname != '' && sname != 'undefined') { 		snames = document.getElementsByName(sname); 		if (snames.length > 1) { 			for (var k = 0; k < snames.length; k++) { 				if (element == snames[k]) { 					ssname = sname + '[' + k + ']' 				} 			} 		} else { 			ssname = sname; 		} 	} 	if (stagname != '' && stagname != 'undefined') { 		stagnames = document.getElementsByTagName(stagname); 		if (stagnames.length > 1) { 			for (var k = 0; k < stagnames.length; k++) { 				if (element == stagnames[k]) { 					sstagname = stagname + '[' + k + ']' 				} 			} 		} else { 			sstagname = stagname; 		} 	} 	if (sclassname != '' && sclassname != 'undefined') { 		sclassnames = document.getElementsByClassName(sclassname); 		if (sclassnames.length > 1) { 			for (var k = 0; k < sclassnames.length; k++) { 				if (element == sclassnames[k]) { 					ssclassname = sclassname + '[' + k + ']' 				} 			} 		} else { 			ssclassname = sclassname; 		} 	} 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') { 			if (sname != '' && sname != 'undefined') { 				snames = document.getElementsByName(sname); 				if (snames.length > 1) { 					for (var k = 0; k < snames.length; k++) { 						if (element == snames[k]) { 							stextvalue = sname + k; 						} 					} 				} else { 					stextvalue = sname; 				} 			} else if (sid != '' && sid != 'undefined') { 				stextvalue = sid; 			} else if (splaceholder != '' && splaceholder != 'undefined') { 				stextvalue = splaceholder; 			} else { 				var seles = document.getElementsByTagName(stagname); 				for (var k = 0; k < seles.length; k++) { 					if (element == seles[k]) { 														 		   				  															  													 		   			  														  											 		   			 														 										   		   				 						stextvalue = stagname + '_NONAME' + (k + 1); 					} 		   				 															 												   		   			 											 										 				} 			} 		} 		if (sid == '') { 			sid = 'null'; 		} 		smultipleFlag = element.hasAttribute('multiple'); 		sishidden = sisVisible(element); 		if (sishidden == true || sishidden == 'True' || sishidden == 'true') { 			sishidden = 'No'; 		} else { 			sishidden = 'Yes'; 		} 		var sfirstpass = 0; 		var srpath = ''; 		var setype = element.getAttribute('type'); 		setype = (String(setype)).toLowerCase(); 		for (var spath = ''; element && element.nodeType == 1; element = element.parentNode) { 			var spredicate = []; 			var ssiblings = element.parentNode.children; 			var scount = 0; 			var sunique = false; 			var snewPath = ''; 			var sidx = 0; 			for (var i = 0; ssiblings && (i < ssiblings.length); i++) { 				if (ssiblings[i].tagName == element.tagName) { 					scount++; 					if (ssiblings[i] == element) { 						sidx = scount; 					} 				} 			} 			if (sidx == 1 && scount == 1) { 				sidx = null; 			} 			if (suseId && element.id) { 				spredicate[spredicate.length] = '@id=' + '"' + element.id + '"'; 				sunique = true; 			} 			xidx = (suseIdx && sidx) ? ('[' + sidx + ']') : ''; 			sidx = (suseIdx && sidx && !sunique) ? ('[' + sidx + ']') : ''; 			spredicate = (spredicate.length > 0) ? ('[' + spredicate.join(' and ') + ']') : ''; 			spath = '/' + element.tagName.toLowerCase() + xidx + spath; 			if (sfirstpass == 0) { 				if (sunique && srelative) { 					srpath = '//*' + sidx + spredicate + srpath; 					sfirstpass = 1; 				} else { 					srpath = '/' + element.tagName.toLowerCase() + sidx + spredicate + srpath; 				} 			} 		} 		if (stagname == 'textarea') { 			stagname = 'input'; 			stagtype = 'txtarea'; 		} else if (stagname == 'select' && smultipleFlag) { 			stagname = 'list'; 			stagtype = 'lst'; 		} else if (stagname == 'select') { 			stagtype = 'select'; 		} else if (stagname == 'td' || stagname == 'tr') { 			stagname = 'tablecell'; 			stagtype = 'tblcell'; 		} else if (stagname == 'a') { 			stagtype = 'lnk'; 		} else if (stagname == 'table') { 			stagtype = 'tbl'; 		} else if (stagname == 'img') { 			stagtype = 'img'; 		} else if (stagname == 'input' && setype == 'image') { 			stagname = 'img'; 			stagtype = 'img'; 		} 		if (stagname == 'input' && (setype == 'button' || setype == 'submit' || setype == 'reset' || setype == 'file')) { 			stagname = 'button'; 			stagtype = 'btn'; 		} else if (stagname == 'input' && setype == 'radio') { 			stagname = 'radiobutton'; 			stagtype = 'radiobtn'; 		} else if (stagname == 'input' && setype == 'checkbox') { 			stagname = 'checkbox'; 			stagtype = 'chkbox'; 		} else if (stagname == 'input' && (setype == 'text' || setype == 'email' || setype == 'number' || setype == 'password' || setype == 'range' || setype == 'search' || setype == 'url')) { 			stagname = 'input'; 			stagtype = 'txtbox'; 																								 					 					  									 					   					 		} 		else if (stagname == 'input' && stagtype == '' && (setype == 'hidden' || setype == 'null')) { 			stagname = 'div'; 			stagtype = 'elmnt'; 		} else if (stagname == 'button') { 			stagname = 'button'; 			stagtype = 'btn'; 		} 		stextvalue = stextvalue.replace(">", ""); 		stextvalue = stextvalue.replace("</", ""); 		stextvalue = stextvalue.replace("<", ""); 		stextvalue = stextvalue.replace("/>", ""); 		stextvalue = stextvalue.split("\\n").join(""); 		stextvalue = stextvalue.split("\\t").join(""); 		stextvalue = stextvalue.split("\\r").join(""); 		stextvalue = stextvalue.split("  ").join(""); 		stextvalue = stextvalue.split("\u00a0").join("");										 					   										  		  									 		if (stextvalue == '' || stextvalue.length == 0 || stextvalue == '0') { 			stextvalue = 'NONAME' + snonamecounter; 			snonamecounter = snonamecounter + 1; 			scustname = stextvalue; 		} else { 			scustname = stextvalue; 		} 		if (stagtype != '') { 			scustname = scustname + '_' + stagtype; 		} else { 			scustname = scustname + '_elmnt'; 		} 		coordinates = left + ';' + top + ';' + height + ';' + width; 		coordinates = String(coordinates); 		snewPath = String(srpath) + ';' + String(sid) + ';' + String(spath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + stextvalue; 		sarr.push({ 			'xpath': snewPath, 			'tag': stagname, 			'hiddentag': sishidden, 			'url': surl, 			'height': height, 			'width': width, 			'custname': scustname, 			'top': top, 			'left': left 		}); 	} 	return sarr; }  function findCoordinates(element) { 	height = element.offsetHeight; 	width = element.offsetWidth; 	top = 0; 	left = 0; 	do { 		top += element.offsetTop || 0; 		left += element.offsetLeft || 0; 		element = element.offsetParent; 	} while (element); } function saddNodesOuter(sarray, scollection) { 	for (var i = 0; scollection && scollection.length && i < scollection.length; i++) { 		sarray.push(scollection[i]); 	} }; function stext_content(f) { 	var sfirstText = ''; 	var stextdisplay = ''; 	for (var z = 0; z < f.childNodes.length; z++) { 		var scurNode = f.childNodes[z]; 		swhitespace = /^\s*$/; 		if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) { 			sfirstText = scurNode.nodeValue; 			stextdisplay = stextdisplay + sfirstText; 		} 	} 	return (stextdisplay); }; return getElementProperties(element);"""
                            element_properties = []
                            element_properties = driver.execute_script(properties_script,webElement[0],url)
                            new_properties=element_properties[0];
                            if cmp(element['xpath'],new_properties['xpath'])!=0:
                                self.changedobject.append(new_properties)
                                highlight1(webElement[0])
                            else:
                                self.notchangedobject.append(element)
                    else:
                        highlight1(webElement[0])
                    try:
                        if currentdriverhandle!= None:
                            driver.switch_to.window(currentdriverhandle)
                        else:
                            driver.switch_to.default_content()
                    except Exception as e4:
                        evb = e4
                else:
                    self.notfoundobject.append(element)

            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            status= domconstants.STATUS_FAIL
            print 'Error while highlighting'
            if (isinstance(driver,webdriver.Ie)):
                print 'Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked)'
        log.info('Highlight method execution done ')
        return status


