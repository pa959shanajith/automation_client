#-------------------------------------------------------------------------------
# Name:        clickandadd.py
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
import logging.config
import logging
import os
import time
from selenium import webdriver
from PIL import Image
log = logging.getLogger('clickandadd.py')
currenthandle = ''
status = domconstants.STATUS_FAIL

class Clickandadd():
    def startclickandadd(self):
        try:
            log.info('Inside startclickandadd method .....')
            driver = browserops.driver
            browser = browserops.browser
            log.info('Obtained browser handle and driver from browserops.py class .....')
            toolwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            actwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            log.info('Minimizing the foreground window i.e tool and assuming AUT on top .....')
            javascript_hasfocus = """return(document.hasFocus());"""
            time.sleep(6)
            for eachdriverhand in driver.window_handles:
                log.info('Iterating through the number of windows open by the driver')
                driver.switch_to.window(eachdriverhand)
                log.info('Switching to each handle and checking weather it has focus ')

                if (driver.execute_script(javascript_hasfocus)):
                    log.info('Got the window which has the focus')
                    global currenthandle
                    currenthandle = eachdriverhand
                    break
            javascript_clicknadd = """if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) { 	(function () { 		function hasAttribute(attrName) { 			return typeof this[attrName] !== 'undefined'; 		} 		var inputs = document.getElementsByTagName('select'); 		for (var i = 0; i < inputs.length; i++) { 			inputs[i].hasAttribute = hasAttribute; 		} 	} 		()); } (function () { 	if (!document.getElementsByClassName) { 		var indexOf = [].indexOf || function (prop) { 			for (var i = 0; i < this.length; i++) { 				if (this[i] === prop) 					return i; 			} 			return -1; 		}; 		getElementsByClassName = function (className, context) { 			var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function () { 					var all = context.getElementsByTagName("*"), 					elements = [], 					i = 0; 					for (; i < all.length; i++) { 						if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) 							elements.push(all[i]); 					} 					return elements; 				})(); 			return elems; 		}; 		document.getElementsByClassName = function (className) { 			return getElementsByClassName(className, document); 		}; 		if (window.Element) { 			window.Element.prototype.getElementsByClassName = function (className) { 				return getElementsByClassName(className, this); 			}; 		} 	} })(); var useIdx = true; var useId = true; var useClass = true; var relative = true; var ae = []; var be = []; var url = arguments[0]; var browser = arguments[1]; var ishidden = 0; var tagname = 0; var textvalue = ''; var arr = []; var custname = ''; var tagtype = ''; var multipleFlag = false; var uniqueFlag = false; var nonamecounter = 1; var txt_area_nonamecounter = 1; var select_nonamecounter = 1; var td_nonamecounter = 1; var a_nonamecounter = 1; var table_nonamecounter = 1; var input_nonamecounter = 1; var ssname = 'null'; var sstagname = 'null'; var ssclassname = 'null'; var top = 0; var left = 0; var height = 0; var width = 0; var coordinates = ''; var isIE = /*@cc_on!@*/ false || !!document.documentMode; var isVisible = (function () { 	function inside(child, parent) { 		while (child) { 			if (child === parent) 				return true; 			child = child.parentNode; 		} 		return false; 	}; 	return function (elem) { 		if (document.hidden || elem.offsetWidth == 0 || elem.offsetHeight == 0 || elem.style.visibility == 'hidden' || elem.style.display == 'none' || elem.style.opacity === 0) 			return false; 		var rect = elem.getBoundingClientRect(); 		if (window.getComputedStyle || elem.currentStyle) { 			var el = elem, 			comp = null; 			while (el) { 				if (el === document) { 					break; 				} else if (!el.parentNode) 					return false; 				comp = window.getComputedStyle ? window.getComputedStyle(el, null) : el.currentStyle; 				if (comp && (comp.visibility == 'hidden' || comp.display == 'none' || (typeof comp.opacity !== 'undefined' && !(comp.opacity > 0)))) 					return false; 				el = el.parentNode; 			} 		} 		return true; 	} })(); localStorage.tastopflag = false; addNodesOuter(ae, document.getElementsByTagName('*')); var css = 'table:hover{border:6px solid !important}', head = document.head || document.getElementsByTagName('head')[0], style = document.createElement('style'); style.type = 'text/css'; style.id = 'SLKNineteen68_Table'; if (style.styleSheet) { 	style.styleSheet.cssText = css; } else { 	style.appendChild(document.createTextNode(css)); } head.appendChild(style); function handler(event) { 	tagtype = ''; 	if (localStorage.getItem('tastopflag') == 'true') { 		if (window.Prototype) { 			var _arr_tojson = Array.prototype.toJSON; 			delete Array.prototype.toJSON; 			window.tasarr = arr; 			Array.prototype.toJSON = _arr_tojson; 		} else { 			window.tasarr = arr; 		} 		clickStop(ae, isIE, be); 		function clickStop(ae, isIE, be) { 			if (isIE) { 				for (var i = 0; i < ae.length; i++) { 					if (ae[i].removeEventListener) { 						ae[i].removeEventListener('click', handler, true); 						ae[i].removeEventListener('mousedown', block_handler, true); 						ae[i].removeEventListener('mouseup', block_handler, true); 					} else if (ae[i].detachEvent) { 						ae[i].detachEvent('onclick', handler); 						ae[i].detachEvent('onmousedown', block_handler); 						ae[i].detachEvent('onmouseup', block_handler); 					} 					if ((ae[i].getAttribute("_onclick")) != null) { 						ae[i].parentNode.replaceChild(be[i], ae[i]); 					} 				} 			} else { 				for (var i = 0; i < ae.length; i++) { 					if (ae[i].removeEventListener) { 						ae[i].removeEventListener('click', handler, true); 						ae[i].removeEventListener('mousedown', block_handler, true); 						ae[i].removeEventListener('mouseup', block_handler, true); 					} else if (ae[i].detachEvent) { 						ae[i].detachEvent('onclick', handler); 						ae[i].detachEvent('onmousedown', block_handler); 						ae[i].detachEvent('onmouseup', block_handler); 					} 					if ((ae[i].getAttribute("_onclick")) != null) { 						var _onclickval = ae[i].getAttribute("_onclick"); 						ae[i].removeAttribute("_onclick"); 						ae[i].setAttribute("onclick", _onclickval); 					} 				} 			} 		} 		localStorage.tastopflag = false; 		arr = []; 		return true; 	} else { 		ssclassname = 'null'; 		ssname = 'null'; 		sstagname = 'null'; 		if (event.ctrlKey) { 			return true; 		} 		if (event.preventDefault) { 			event.preventDefault(); 			event.stopPropagation(); 			event.cancelBubble = true; 			event.returnValue = false; 		} else { 			window.event.cancelBubble = true; 			window.event.returnValue = false; 		} 		var e = event.target || event.srcElement; 		var f = event.target || event.srcElement; 		var className = e.className; 		var rpath = ''; 		var firstpass = 0; 		for (var path = ''; e && e.nodeType == 1; e = e.parentNode) { 			var predicate = []; 			var siblings = e.parentNode.children; 			var count = 0; 			var unique = false; 			for (var i = 0; siblings && (i < siblings.length); i++) { 				if (siblings[i].tagName == e.tagName) { 					count++; 					if (siblings[i] == e) { 						idx = count; 					} 				} 			} 			if (idx == 1 && count == 1) { 				idx = null; 			} 			if (useId && e.id) { 				predicate[predicate.length] = '@id=' + '"' + e.id + '"'; 				unique = true; 			} 			xidx = (useIdx && idx) ? ('[' + idx + ']') : ''; 			idx = (useIdx && idx && !unique) ? ('[' + idx + ']') : ''; 			predicate = (predicate.length > 0) ? ('[' + predicate.join(' and ') + ']') : ''; 			path = '/' + e.tagName.toLowerCase() + xidx + path; 			if (firstpass == 0) { 				if (unique && relative) { 					rpath = '//*' + idx + predicate + rpath; 					firstpass = 1; 				} else { 					rpath = '/' + e.tagName.toLowerCase() + idx + predicate + rpath; 				} 			} 		} 		ishidden = isVisible(f); 		if (ishidden == true || ishidden == 'True' || ishidden == 'true') { 			ishidden = 'No'; 		} else { 			ishidden = 'Yes'; 		} 		var tagname = f.tagName.toLowerCase(); 		if (tagname.indexOf(':') != -1) { 			tagname = tagname.replace(':', ''); 			tagname = 'custom' + tagname; 		} 		id = f.id; 		name = f.name; 		placeholder = f.placeholder; 		id = (String(id)); 		name = (String(name)); 		placeholder = (String(placeholder)); 		var textvalue = text_content(f); 		textvalue = (String(textvalue)); 		findCoordinates(f); 		if (name != '' && name != 'undefined') { 			names = document.getElementsByName(name); 			if (names.length > 1) { 				for (var k = 0; k < names.length; k++) { 					if (f == names[k]) { 						ssname = name + '[' + k + ']' 					} 				} 			} else { 				ssname = name; 			} 		} 		if (tagname != '' && tagname != 'undefined') { 			tagnames = document.getElementsByTagName(tagname); 			if (tagnames.length > 1) { 				for (var k = 0; k < tagnames.length; k++) { 					if (f == tagnames[k]) { 						sstagname = tagname + '[' + k + ']' 					} 				} 			} else { 				sstagname = tagname; 			} 		} 		if (className != '' && className != 'undefined' && className != 'SLKNineteen68_Highlight') { 			classnames = document.getElementsByClassName(className); 			if (classnames.length > 1) { 				for (var k = 0; k < classnames.length; k++) { 					if (f == classnames[k]) { 						ssclassname = className + '[' + k + ']' 					} 				} 			} else { 				ssclassname = className; 			} 		} 		if (tagname != 'script' && tagname != 'meta' && tagname != 'html' && tagname != 'head' && tagname != 'style' && tagname != 'body' && tagname != 'form' && tagname != 'link' && tagname != 'noscript' && tagname != '!' && tagname != 'pre' && tagname != 'code' && tagname != 'animatetransform' && tagname != 'noembed') { 			if (textvalue == '' || textvalue == 'null' || textvalue == 'undefined' || textvalue == '0') { 				if (name != '' && name != 'undefined') { 					names = document.getElementsByName(name); 					if (names.length > 1) { 						for (var k = 0; k < names.length; k++) { 							if (f == names[k]) { 								textvalue = name + k; 							} 						} 					} else { 						textvalue = name; 					} 				} else if (id != '' && id != 'undefined') { 					textvalue = id; 				} else if (placeholder != '' && placeholder != 'undefined') { 					textvalue = placeholder; 				} else { 					var eles = document.getElementsByTagName(tagname); 					for (var k = 0; k < eles.length; k++) { 						if (f == eles[k]) { 							textvalue = tagname + '_NONAME' + (k + 1); 						} 					} 				} 			} 			if (tagname == 'select') { 				f.setAttribute('disabled', 'disabled'); 				multipleFlag = f.hasAttribute('multiple'); 			} 			var etype = f.getAttribute('type'); 			etype = (String(etype)).toLowerCase(); 			var newPath = path; 			if (tagname == 'textarea') { 				tagname = 'input'; 				tagtype = 'txtarea'; 			} else if (tagname == 'select' && multipleFlag) { 				tagname = 'list'; 				tagtype = 'lst'; 			} else if (tagname == 'select') { 				tagtype = 'select'; 			} else if (tagname == 'td') { 				tagname = 'tablecell'; 				tagtype = 'tblcell'; 			} else if (tagname == 'a') { 				tagtype = 'lnk'; 			} else if (tagname == 'table') { 				tagtype = 'tbl'; 			} else if (tagname == 'img') { 				tagtype = 'img'; 			} else if (tagname == 'input' && etype == 'image') { 				tagname = 'img'; 				tagtype = 'img'; 			} 			if (tagname == 'input' && (etype == 'button' || etype == 'submit' || etype == 'reset' || etype == 'file')) { 				tagname = 'button'; 				tagtype = 'btn'; 			} else if (tagname == 'input' && etype == 'radio') { 				tagname = 'radiobutton'; 				tagtype = 'radiobtn'; 			} else if (tagname == 'input' && etype == 'checkbox') { 				tagname = 'checkbox'; 				tagtype = 'chkbox'; 			} else if (tagname == 'input' && (etype == 'text' || etype == 'email' || etype == 'number' || etype == 'password' || etype == 'range' || etype == 'search' || etype == 'url')) { 				tagname = 'input'; 				tagtype = 'txtbox'; 			} else if (tagname == 'input' && tagtype == '' && (etype == 'hidden' || etype == 'null')) { 				tagname = 'div'; 				tagtype = 'elmnt'; 			} else if (tagname == 'option' && f.parentNode.hasAttribute('multiple')) { 				tagname = 'list'; 				var selectIndex1 = rpath.indexOf('select'); 				var selectIndex2 = path.indexOf('select'); 				rpath = rpath.substring(0, selectIndex1 + 6); 				path = path.substring(0, selectIndex2 + 6); 			} else if (tagname == 'button') { 				tagname = 'button'; 				tagtype = 'btn'; 			} 			if (id == '') { 				id = 'null'; 			} 			textvalue = textvalue.replace(">", ""); 			textvalue = textvalue.replace("</", ""); 			textvalue = textvalue.replace("<", ""); 			textvalue = textvalue.replace("/>", ""); 			textvalue = textvalue.split("\\n").join(""); 			textvalue = textvalue.split("\\t").join(""); 			textvalue = textvalue.split("\\r").join(""); 			textvalue = textvalue.split("  ").join(""); 			textvalue = textvalue.split("\u00a0").join(""); 			if (textvalue == '' || textvalue.length == 0 || textvalue == '0') { 				textvalue = 'NONAME' + nonamecounter; 				nonamecounter = nonamecounter + 1; 				custname = textvalue; 			} else { 				custname = textvalue; 			} 			if (tagtype != '') { 				custname = custname + '_' + tagtype; 			} else { 				custname = custname + '_elmnt'; 			} 			if (tagname == 'select') { 				f.removeAttribute('disabled'); 				f.setAttribute('enabled', 'enabled'); 			} else if (tagname == "list") { 				f.removeAttribute('disabled'); 				f.setAttribute('enabled', 'enabled'); 			} 			coordinates = left + ';' + top + ';' + height + ';' + width; 			coordinates = String(coordinates); 			newPath = String(rpath) + ';' + String(id) + ';' + String(path) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + textvalue; 			for (var i = 0; i < arr.length; i++) { 				var res = (arr[i].xpath).split(";"); 				if (res[0] == rpath) { 					uniqueFlag = true; 					break; 				} 			}; 			if (uniqueFlag == false) { 				arr.push({ 					'xpath': newPath, 					'url': url, 					'hiddentag': ishidden, 					'custname': custname, 					'tag': tagname, 					'top': top, 					'left': left, 					'height': height, 					'width': width 				}); 			} 			uniqueFlag = false; 			if (browser == 3) { 				f.setAttribute('class', className + ' SLKNineteen68_Highlight'); 				f.setAttribute('className', className + ' SLKNineteen68_Highlight'); 				f.style.setAttribute('cssText', 'background: #fff300 !important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;'); 			} else { 				f.setAttribute('class', className + ' SLKNineteen68_Highlight'); 				f.setAttribute('style', 'background: #fff300 !important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;'); 			} 		} 		return false; 	} } function block_handler(event) { 	event = event || window.event; 	if (event.ctrlKey) { 		return true; 	} 	if (event.preventDefault) { 		event.preventDefault(); 		event.stopPropagation(); 		event.cancelBubble = true; 		event.returnValue = false; 	} else { 		window.event.cancelBubble = true; 		window.event.returnValue = false; 	} 	return false; } click(ae, isIE, be); function click(ae, isIE, be) { 	if (isIE) { 		for (var i = 0; i < ae.length; i++) { 			if ((ae[i].getAttribute("onclick")) != null) { 				var onclickval = ae[i].attributes["onclick"].value; 				be[i] = ae[i].cloneNode(true); 				ae[i].onclick = null; 				ae[i].setAttribute('_onclick', onclickval); 			} 			if (ae[i].addEventListener) { 				ae[i].addEventListener('click', handler, true); 				ae[i].addEventListener('mousedown', block_handler, true); 				ae[i].addEventListener('mouseup', block_handler, true); 			} else if (ae[i].attachEvent) { 				ae[i].attachEvent('onclick', handler); 				ae[i].attachEvent('onmousedown', block_handler); 				ae[i].attachEvent('onmouseup', block_handler); 			} 		} 	} else { 		for (var i = 0; i < ae.length; i++) { 			if ((ae[i].getAttribute("onclick")) != null) { 				var onclickval = ae[i].getAttribute("onclick"); 				ae[i].removeAttribute("onclick"); 				ae[i].setAttribute("_onclick", onclickval); 			} 			if (ae[i].addEventListener) { 				ae[i].addEventListener('click', handler, true); 				ae[i].addEventListener('mousedown', block_handler, true); 				ae[i].addEventListener('mouseup', block_handler, true); 			} else if (ae[i].attachEvent) { 				ae[i].attachEvent('onclick', handler); 				ae[i].attachEvent('onmousedown', block_handler); 				ae[i].attachEvent('onmouseup', block_handler); 			} 		} 	} } function findCoordinates(element) { 	height = element.offsetHeight; 	width = element.offsetWidth; 	top = 0; 	left = 0; 	do { 		top += element.offsetTop || 0; 		left += element.offsetLeft || 0; 		element = element.offsetParent; 	} while (element); }; function text_content(f) { 	var firstText = ''; 	var textdisplay = ''; 	for (var z = 0; z < f.childNodes.length; z++) { 		var curNode = f.childNodes[z]; 		whitespace = /^\s*$/; 		if (curNode.nodeName === '#text' && !(whitespace.test(curNode.nodeValue))) { 			firstText = curNode.nodeValue; 			textdisplay = textdisplay + firstText; 		} 	} 	return (textdisplay); }; function addNodesOuter(array, collection) { 	for (var i = 0; collection && collection.length && i < collection.length; i++) { 		array.push(collection[i]); 	} };"""
            driver.switch_to.window(currenthandle)
            log.info('Performing the click and add operation on default/outer page')
            driver.execute_script(javascript_clicknadd, driver.current_url,browser)
            log.info('Performing the click and add operation on default/outer page done')

            def switchtoframe_clicknadd1(mypath):
                cond_flag_cna = False
                log.info('Inside switchtoframe_clicknadd1 method')
                indiframes = mypath.split("/")
                log.info('Splitting Iframe/frame url by /')
                global currenthandle
                driver.switch_to.window(currenthandle)
                log.info('Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = domconstants.IFRAME
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'f':
                            frame_iframe =domconstants.FRAME
                            log.info('MSG: It is  frame')
                        else:
                            log.info('It is  iframe')
                        try:
                            if (driver.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                                driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                                log.info('Switched to frame/iframe')
                                cond_flag_cna = True
                            else:
                                cond_flag_cna = False
                                break
                        except Exception as e:
                            cond_flag_cna = False
                return cond_flag_cna



            def callback_clicknadd1(myipath):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' + '/'
                    if(switchtoframe_clicknadd1(path)):
                        log.info('Performing the click and add operation on iframe/frame page')
                        driver.execute_script(javascript_clicknadd, path,browser)
                        log.info('Performing the click and add operation on iframe/frame page done')
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            inpath = path + str(frames) + 'f' + '/'
                            if switchtoframe_clicknadd1(inpath):
                                log.info('Performing the click and add operation on frame/iframe page')
                                driver.execute_script(javascript_clicknadd, inpath,browser)
                                log.info('Performing the click and add operation on frame/iframe page done')
                            callback_clicknadd1(inpath)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            inpath = path + str(frames) + 'i' + '/'
                            if switchtoframe_clicknadd1(inpath):
                                log.info('Performing the click and add operation on frame/iframe page')
                                driver.execute_script(javascript_clicknadd, inpath,browser)
                                log.info('Performing the click and add operation on frame/iframe page done')
                            callback_clicknadd2(inpath)
                        callback_clicknadd1(path)
                for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(frames) + 'f' + '/'
                    if(switchtoframe_clicknadd1(path)):
                        log.info('Performing the click and add operation on iframe/frame page')
                        driver.execute_script(javascript_clicknadd, path,browser)
                        log.info('Performing the click and add operation on iframe/frame page done')
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            inpath = path + str(frames) + 'f' + '/'
                            if switchtoframe_clicknadd1(inpath):
                                log.info('Performing the click and add operation on frame/iframe page')
                                driver.execute_script(javascript_clicknadd, inpath,browser)
                                log.info('Performing the click and add operation on frame/iframe page done')
                            callback_clicknadd1(inpath)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            inpath = path + str(frames) + 'i' + '/'
                            if switchtoframe_clicknadd1(inpath):
                                log.info('Performing the click and add operation on frame/iframe page')
                                driver.execute_script(javascript_clicknadd, inpath,browser)
                                log.info('Performing the click and add operation on frame/iframe page done')
                            callback_clicknadd2(inpath)
                        callback_clicknadd1(path)

            def callback_clicknadd2(myipath):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'f' + '/'
                    if(switchtoframe_clicknadd1(path)):
                        log.info('Performing the click and add operation on frame/iframe page')
                        driver.execute_script(javascript_clicknadd, path,browser)
                        log.info('Performing the click and add operation on frame/iframe page done')
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            inpath = path + str(frames) + 'i' + '/'
                            if switchtoframe_clicknadd1(inpath):
                                log.info('Performing the click and add operation on iframe/frame page')
                                driver.execute_script(javascript_clicknadd, inpath,browser)
                                log.info('Performing the click and add operation on iframe/frame page done')
                            callback_clicknadd2(inpath)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            inpath = path + str(frames) + 'f' + '/'
                            if switchtoframe_clicknadd1(inpath):
                                log.info(' Performing the click and add operation on iframe/frame page')
                                driver.execute_script(javascript_clicknadd, inpath,browser)
                                log.info(' Performing the click and add operation on iframe/frame page done')
                            callback_clicknadd1(inpath)
                        callback_clicknadd2(path)
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' + '/'
                    if(switchtoframe_clicknadd1(path)):
                        log.info('Performing the click and add operation on frame/iframe page')
                        driver.execute_script(javascript_clicknadd, path,browser)
                        log.info('Performing the click and add operation on frame/iframe page done')
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                            inpath = path + str(frames) + 'i' + '/'
                            if switchtoframe_clicknadd1(inpath):
                                log.info('Performing the click and add operation on iframe/frame page')
                                driver.execute_script(javascript_clicknadd, inpath,browser)
                                log.info('Performing the click and add operation on iframe/frame page done')
                            callback_clicknadd2(inpath)
                        for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                            inpath = path + str(frames) + 'f' + '/'
                            if switchtoframe_clicknadd1(inpath):
                                log.info(' Performing the click and add operation on iframe/frame page')
                                driver.execute_script(javascript_clicknadd, inpath,browser)
                                log.info(' Performing the click and add operation on iframe/frame page done')
                            callback_clicknadd1(inpath)
                        callback_clicknadd2(path)



            callback_clicknadd1('')
            log.info('clickandadd scrape operation on iframe/frame pages is completed')
            driver.switch_to.window(currenthandle)
            callback_clicknadd2('')
            log.info('clickandadd scrape operation on frame/iframe pages is completed')
            driver.switch_to.window(currenthandle)
            driver.switch_to_default_content()
            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            status = domconstants.STATUS_FAIL
            print 'Error while performing start click and add scrape'
            if (isinstance(driver,webdriver.Ie)):
                print 'Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry'
        return status

    def stopclickandadd(self):
##        vie = {}
        data = {}
        pathlist = list()
        try:
            log.info('Inside stopclickandadd method .....')
            driver = browserops.driver
            maindir = os.environ["NINETEEN68_HOME"]
            screen_shot_path = maindir + '\Nineteen68\plugins\WebScrape' + domconstants.SCREENSHOT_IMG
            log.info('Obtained driver from browserops.py class .....')
            javascript_stopclicknadd = """localStorage.tastopflag= true; document.getElementsByTagName('HTML')[0].click(); function getElementsByClassName(classname) {     var a = [];     var re = new RegExp('(^| )'+classname+'( |$)');     var els = document.getElementsByTagName("*");     for(var i=0,j=els.length; i<j; i++)         if(re.test(els[i].className))a.push(els[i]);     return a; } if(document.getElementById('SLKNineteen68_Table')){ styleTag = document.getElementById('SLKNineteen68_Table'); head = document.head || document.getElementsByTagName('head')[0]; head.removeChild(styleTag); var a=getElementsByClassName('SLKNineteen68_Highlight'); for (var i = 0; i < a.length; i++) { a[i].removeAttribute('style'); }}var temp = window.tasarr; window.tasarr = null; return (temp);"""
            tempne_stopclicknadd = []
            log.info('Performing the stopclickandd operation on default/outer page')
            tempreturn_stopclicknadd = driver.execute_script(javascript_stopclicknadd)
            log.info('stopclickandd operation on default/outer page is done and data is obtained')
            tempne_stopclicknadd.extend(tempreturn_stopclicknadd)

            def switchtoframe_stopclicknadd1(mypath):
                log.info('Inside switchtoframe_stopclicknadd1 method')
                cond_flag_scna = False
                log.info('Splitting Iframe/frame url by /')
                indiframes = mypath.split("/")
                driver.switch_to.window(currenthandle)
                log.info('Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = domconstants.IFRAME
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'f':
                            frame_iframe = domconstants.FRAME
                            log.info('It is  frame')
                        else:
                            log.info('It is iframe')
                        try:
                            if (driver.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                                driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                                log.info('Switched to frame/iframe')
                                cond_flag_scna = True
                            else:
                                cond_flag_scna = False
                                break
                        except Exception as e:
                            cond_flag_scna = False
                return cond_flag_scna

            def callback_stopclicknadd1(myipath, tempne_stopclicknadd):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' + '/'
                    pathlist.append(path)
                    if pathlist.count(path) == 1:
                        if(switchtoframe_stopclicknadd1(path)):
                            log.info('before stopclicknadd operation on iframe page is done and data is obtained')
                            temp = driver.execute_script(javascript_stopclicknadd)
                            log.info('stopclicknadd operation on iframe page is done and data is obtained')
                            if temp is not None:
                                tempne_stopclicknadd.extend(temp)
                            for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                                inpath = path + str(frames) + 'f' + '/'
                                pathlist.append(inpath)
                                if pathlist.count(inpath) == 1:
                                    if switchtoframe_stopclicknadd1(inpath):
                                        itemp = driver.execute_script(javascript_stopclicknadd)
                                        log.info('before stopclicknadd operation on frame page is done and data is obtained')
                                        if itemp is not None:
                                            tempne_stopclicknadd.extend(itemp)
                                            log.info('stopclicknadd operation on frame page is done and data is obtained')
                                    callback_stopclicknadd1(inpath, tempne_stopclicknadd)
                            for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                                inpath = path + str(frames) + 'i' + '/'
                                pathlist.append(inpath)
                                if pathlist.count(inpath) == 1:
                                    if switchtoframe_stopclicknadd1(inpath):
                                            itemp = driver.execute_script(javascript_stopclicknadd)
                                            log.info('stopclicknadd operation on frame page is done and data is obtained')
                                            if itemp is not None:
                                                tempne_stopclicknadd.extend(itemp)
                                                log.info('stopclicknadd operation on frame page is done and data is obtained')
                                    callback_stopclicknadd2(inpath, tempne_stopclicknadd)
                            callback_stopclicknadd1(path, tempne_stopclicknadd)

                for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(frames) + 'f' + '/'
                    pathlist.append(path)
                    if pathlist.count(path) == 1:
                        if(switchtoframe_stopclicknadd1(path)):
                            log.info('before stopclicknadd operation on iframe page is done and data is obtained')
                            temp = driver.execute_script(javascript_stopclicknadd)
                            log.info('stopclicknadd operation on iframe page is done and data is obtained')
                            if temp is not None:
                                tempne_stopclicknadd.extend(temp)
                            for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                                inpath = path + str(frames) + 'f' + '/'
                                pathlist.append(inpath)
                                if pathlist.count(inpath) == 1:
                                    if switchtoframe_stopclicknadd1(inpath):
                                            itemp = driver.execute_script(javascript_stopclicknadd)
                                            log.info('before stopclicknadd operation on frame page is done and data is obtained')
                                            if itemp is not None:
                                                tempne_stopclicknadd.extend(itemp)
                                                log.info('stopclicknadd operation on frame page is done and data is obtained')
                                    callback_stopclicknadd1(inpath, tempne_stopclicknadd)
                            for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                                inpath = path + str(frames) + 'i' + '/'
                                pathlist.append(inpath)
                                if pathlist.count(inpath) == 1:
                                    if switchtoframe_stopclicknadd1(inpath):
                                            itemp = driver.execute_script(javascript_stopclicknadd)
                                            log.info('stopclicknadd operation on frame page is done and data is obtained')
                                            if itemp is not None:
                                                tempne_stopclicknadd.extend(itemp)
                                                log.info('stopclicknadd operation on frame page is done and data is obtained')
                                    callback_stopclicknadd2(inpath, tempne_stopclicknadd)
                            callback_stopclicknadd1(path, tempne_stopclicknadd)

            def callback_stopclicknadd2(myipath, tempne_stopclicknadd):
                path = myipath
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'f' + '/'
                    pathlist.append(path)
                    if pathlist.count(path) == 1:
                        if(switchtoframe_stopclicknadd1(path)):
                            log.info('before stopclicknadd operation on frame page is done and data is obtained')
                            temp = driver.execute_script(javascript_stopclicknadd)
                            log.info('stopclicknadd operation on frame page is done and data is obtained')
                            if temp is not None:
                                tempne_stopclicknadd.extend(temp)
                            for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                                inpath = path + str(frames) + 'i' + '/'
                                pathlist.append(inpath)
                                if pathlist.count(inpath) == 1:
                                    if switchtoframe_stopclicknadd1(inpath):
                                        log.info('before stopclicknadd operation on iframe page is done and data is obtained')
                                        itemp = driver.execute_script(javascript_stopclicknadd)
                                        log.info('stopclicknadd operation on iframe page is done and data is obtained')
                                        if itemp is not None:
                                            tempne_stopclicknadd.extend(itemp)
                                            log.info('stopclicknadd operation on iframe page is done and data is obtained')
                                    callback_stopclicknadd2(inpath, tempne_stopclicknadd)
                            for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                                inpath = path + str(frames) + 'f' + '/'
                                pathlist.append(inpath)
                                if pathlist.count(inpath) == 1:
                                    if switchtoframe_stopclicknadd1(inpath):
                                        itemp = driver.execute_script(javascript_stopclicknadd)
                                        log.info('before stopclicknadd operation on frame page is done and data is obtained')
                                        if itemp is not None:
                                            tempne_stopclicknadd.extend(itemp)
                                            log.info('stopclicknadd operation on frame page is done and data is obtained')
                                    callback_stopclicknadd1(inpath, tempne_stopclicknadd)
                            callback_stopclicknadd2(path, tempne_stopclicknadd)
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    #custom switchtoframe:
                    path = myipath + str(iframes) + 'i' + '/'
                    pathlist.append(path)
                    if pathlist.count(path) == 1:
                        if(switchtoframe_stopclicknadd1(path)):
                            log.info('before stopclicknadd operation on frame page is done and data is obtained')
                            temp = driver.execute_script(javascript_stopclicknadd)
                            log.info('stopclicknadd operation on frame page is done and data is obtained')
                            if temp is not None:
                                tempne_stopclicknadd.extend(temp)
                            for frames in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                                inpath = path + str(frames) + 'i' + '/'
                                pathlist.append(inpath)
                                if pathlist.count(inpath) == 1:
                                    if switchtoframe_stopclicknadd1(inpath):
                                        log.info('before stopclicknadd operation on iframe page is done and data is obtained')
                                        itemp = driver.execute_script(javascript_stopclicknadd)
                                        log.info('stopclicknadd operation on iframe page is done and data is obtained')
                                        if itemp is not None:
                                            tempne_stopclicknadd.extend(itemp)
                                    callback_stopclicknadd2(inpath, tempne_stopclicknadd)
                            for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                                inpath = path + str(frames) + 'f' + '/'
                                pathlist.append(inpath)
                                if pathlist.count(inpath) == 1:
                                    if switchtoframe_stopclicknadd1(inpath):
                                        itemp = driver.execute_script(javascript_stopclicknadd)
                                        log.info('before stopclicknadd operation on frame page is done and data is obtained')
                                        if itemp is not None:
                                            tempne_stopclicknadd.extend(itemp)
                                        log.info('stopclicknadd operation on frame page is done and data is obtained')
                                    callback_stopclicknadd1(inpath, tempne_stopclicknadd)
                            callback_stopclicknadd2(path, tempne_stopclicknadd)

            def fullpage_screenshot(driver, screen_shot_path):
                try:
                    total_width = driver.execute_script("return document.body.offsetWidth")
                    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
                    viewport_width = driver.execute_script("return window.innerWidth")
                    viewport_height = driver.execute_script("return window.innerHeight")
                    rectangles = []
                    screen = None
                    if(total_width == 0):
                        total_width = driver.execute_script("return document.documentElement.offsetWidth")

                    if total_height < viewport_height:
                        total_height = viewport_height

                    if total_width  < viewport_width:
                        total_width = viewport_width

                    if(total_width > 0 and total_height > 0 and viewport_width > 0 and viewport_height > 0):

                        i = 0
                        while i < total_height:
                            ii = 0
                            top_height = i + viewport_height

                            if top_height > total_height:
                                top_height = total_height

                            while ii < total_width:
                                top_width = ii + viewport_width

                                if top_width > total_width:
                                    top_width = total_width

                                rectangles.append((ii, i, top_width,top_height))

                                ii = ii + viewport_width

                            i = i + viewport_height

                        stitched_image = Image.new('RGB', (total_width, total_height))
                        previous = None
                        part = 0
                        for rectangle in rectangles:
                            if not previous is None:
                                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                                time.sleep(0.2)
                            file_name = "part_{0}.png".format(part)
                            driver.get_screenshot_as_file(file_name)
                            screenshot = Image.open(file_name)
                            if rectangle[1] + viewport_height > total_height:
                                offset = (rectangle[0], total_height - viewport_height)
                            else:
                                offset = (rectangle[0], rectangle[1])
                            stitched_image.paste(screenshot, offset)
                            del screenshot
                            os.remove(file_name)
                            part = part + 1
                            previous = rectangle
                        stitched_image.save(screen_shot_path)
                        with open(screen_shot_path, "rb") as f:
                            data = f.read()
                            screen =  data.encode("base64")
                    else:
                        screen = driver.get_screenshot_as_base64()
                except Exception as e:
                    screen = driver.get_screenshot_as_base64()
                return screen
            callback_stopclicknadd1('', tempne_stopclicknadd)
            log.info('stopclickandadd operation on iframe/frame pages is completed')
            driver.switch_to.window(currenthandle)
            callback_stopclicknadd2('', tempne_stopclicknadd)
            log.info('stopclickandadd operation on frame/iframe pages is completed')
            driver.switch_to.window(currenthandle)
            driver.switch_to_default_content()

##            global vie
##            vie = {'view': tempne_stopclicknadd}
##            global data
##            data.append(vie)
##            screen = driver.get_screenshot_as_base64()
            if (isinstance(driver,webdriver.Firefox) or isinstance(driver,webdriver.Chrome)):
                screen = fullpage_screenshot(driver, screen_shot_path )
            else:
                screen = driver.get_screenshot_as_base64()
##            scrapetype = {'scrapetype' : 'cna'}
##            screenshot = {'mirror':screen}
            scrapedin = ''
            if browserops.browser == 2:
                scrapedin = 'FX'
            elif browserops.browser == 3:
                scrapedin = 'IE'
            elif browserops.browser == 1:
                scrapedin = 'CH'
##            data.append(scrapetype)
##            data.append(scrapedin)
##            data.append(screenshot)
            data['scrapetype'] = 'cna'
            data['scrapedin'] = scrapedin
            data['view'] = tempne_stopclicknadd
            data['mirror'] = screen

            log.info('Creating a json object with key vie with value as return data')
            with open('domelements.json', 'w') as outfile:
                log.info('Opening domelements.json file to write vie object')
                json.dump(data, outfile, indent=4, sort_keys=False)
                log.info('vie is dumped into  domelements.json file ')
            outfile.close()
            log.info('domelements.json file closed ')
            if driver.current_url == domconstants.BLANK_PAGE:
                log.info('url is blank so cannot perform clickandadd operation')
                status = domconstants.STATUS_FAIL
                data = domconstants.STATUS_FAIL
            else:
                status = domconstants.STATUS_SUCCESS
        except Exception as e:
            status = domconstants.STATUS_FAIL
            data = domconstants.STATUS_FAIL
            print 'Error while performing stop click and add scrape'
            if (isinstance(driver,webdriver.Ie)):
                print 'Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry'
        return data


