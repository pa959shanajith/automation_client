#-------------------------------------------------------------------------------
# Name:        scrape_utils.py
# Purpose:     Defined utility methods and variables used in web scraping
#
# Author:      nikunj.jain
#
# Created:     11-04-2018
# Copyright:   (c) nikunj.jain 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import os
import base64
import codecs
from constants import SYSTEM_OS
if SYSTEM_OS=='Windows':
    import win32gui
    import win32process
    import win32con
from PIL import Image
import domconstants
import logging
log = logging.getLogger("webscrape_utils.py")

class WebScrape_Utils:

    """"Scrape data limit in MB"""
    SCRAPE_DATA_LIMIT = 30
    """Javascript logic to check if current frame is an iframe"""
    javascript_in_iframe = """function inIframe () { 	try { 		return window.self !== window.top; 	} catch (e) { 		return true; 	} } return inIframe()"""
    
    """Javascript logic used in fullscrape operation"""
    javascript_fullscrape = """
        if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {
            (function () {
                function hasAttribute(attrName) {
                    return typeof this[attrName] !== 'undefined';
                }
                var inputs = document.getElementsByTagName('*');
                for (var i = 0; i < inputs.length; i++) {
                    inputs[i].hasAttribute = hasAttribute;
                }
            }());
        }
        if (!window.Element || !window.Element.prototype || !window.Element.prototype.getAttribute) {
            (function () {
                function getAttribute(attrName) {
                    return typeof this[attrName] !== 'undefined';
                }
                var inputs = document.getElementsByTagName('*');
                for (var i = 0; i < inputs.length; i++) {
                    inputs[i].getAttribute = getAttribute;
                }
            }());
        }(function () {
            if (!document.getElementsByClassName) {
                var indexOf = [].indexOf || function (prop) {
                    for (var i = 0; i < this.length; i++) {
                        if (this[i] === prop) return i;
                    }
                    return -1;
                };
                getElementsByClassName = function (className, context) {
                    var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function () {
                        var all = context.getElementsByTagName("*"),
                            elements = [],
                            i = 0;
                        for (; i < all.length; i++) {
                            if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) elements.push(all[i]);
                        }
                        return elements;
                    })();
                    return elems;
                };
                document.getElementsByClassName = function (className) {
                    return getElementsByClassName(className, document);
                };
                if (window.Element) {
                    window.Element.prototype.getElementsByClassName = function (className) {
                        return getElementsByClassName(className, this);
                    };
                }
            }
        })();
        var suseIdx = true;
        var suseId = true;
        var suseClass = true;
        var srelative = true;
        var sae = [];
        var sarr = [];
        var sele = [];
        var smyid = 0;
        var stextvalue = '';
        var slabel = '';
        var stagname = 0;
        var sishidden = 0;
        var scustname = '';
        var smultipleFlag = false;
        var surl = arguments[0];
        var snonamecounter = 1;
        var txt_area_nonamecounter = 1;
        var select_nonamecounter = 1;
        var td_nonamecounter = 1;
        var a_nonamecounter = 1;
        var table_nonamecounter = 1;
        var input_nonamecounter = 1;
        var ssalesforcecounter = 1;
        var stagtype = '';
        var ssname = 'null';
        var sstagname = 'null';
        var ssclassname = 'null';
        var sclassname = 'null';
        var parentele = 'null';
        var top = 0;
        var left = 0;
        var height = 0;
        var width = 0;
        var coordinates = '';
        var scrapeOption = arguments[1][0];
        var scrapeOptionValue;
        var salesF = false;
        if (arguments[1].length > 1) scrapeOptionValue = arguments[1][1];
        var sisVisible = (function () {
            function inside(schild, sparent) {
                while (schild) {
                    if (schild === sparent) return true;
                    schild = schild.parentNode;
                }
                return false;
            };
            return function (selem) {
                if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;
                var srect = selem.getBoundingClientRect();
                if (window.getComputedStyle || selem.currentStyle) {
                    var sel = selem,
                        scomp = null;
                    while (sel) {
                        if (sel === document) {
                            break;
                        } else if (sel.nodeName == '#document-fragment') {
                            sel = sel.host;
                        } else if (!sel.parentNode) return false;
                        if (sel instanceof(HTMLElement)) scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;
                        if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;
                        sel = sel.parentNode;
                    }
                }
                return true;
            }
        })();
        Array.prototype.extend = function (other_array) {
            other_array.forEach(function (v) {
                this.push(v)
            }, this);
        };
        sae = sgetNodesOuter();
        for (var j = 0; j < sae.length; j++) {
            parentele = 'null';
            stagtype = '';
            ssname = 'null';
            sstagname = 'null';
            sid = sae[j].id;
            sname = sae[j].name;
            salttext = sae[j].alt;
            splaceholder = sae[j].placeholder;
            sclassname = sae[j].className;
            sid = (String(sid));
            sclassname = (String(sclassname));
            sname = (String(sname));
            splaceholder = (String(splaceholder));
            stextvalue = stext_content(sae[j]);
            stextvalue = (String(stextvalue));
            slabel = stext_content(sae[j]);
            slabel = (String(slabel));
            stagname = sae[j].tagName.toLowerCase();
            ssname = 'null';
            sstagname = 'null';
            role = 'null';
            ssclassname = 'null';
            findCoordinates(sae[j]);
            salesF = (sae[j].tagName.toLowerCase().indexOf('lightning') != -1);
            if (stagname == 'lightning-datatable') {
                parentele = sae[j];
                sae[j] = sae[j].getElementsByTagName('table')[0];
                sid = sae[j].id;
                sname = sae[j].name;
                salttext = sae[j].alt;
                splaceholder = sae[j].placeholder;
                sclassname = sae[j].className;
                sid = (String(sid));
                sclassname = (String(sclassname));
                sname = (String(sname));
                splaceholder = (String(splaceholder));
                stextvalue = stext_content(sae[j]);
                stextvalue = (String(stextvalue));
                stagname = sae[j].tagName.toLowerCase();
            }
            if (sae[j].hasAttribute('role')) {
                if (sae[j].getAttribute('role') === 'grid' && sae[j].tagName.toLowerCase() === 'div') {
                    role = 'grid';
                }
            }
            if (stagname.indexOf(':') != -1) {
                stagname = stagname.replace(':', '');
                stagname = 'custom' + stagname;
            }
            if (sname != '' && sname != 'undefined') {
                snames = document.getElementsByName(sname);
                if (snames.length > 1) {
                    for (var k = 0; k < snames.length; k++) {
                        if (sae[j] == snames[k]) {
                            ssname = sname + '[' + k + ']'
                        }
                    }
                } else {
                    ssname = sname;
                }
            }
            if (stagname != '' && stagname != 'undefined') {
                stagnames = document.getElementsByTagName(stagname);
                if (stagnames.length > 1) {
                    for (var k = 0; k < stagnames.length; k++) {
                        if (sae[j] == stagnames[k]) {
                            sstagname = stagname + '[' + k + ']'
                        }
                    }
                } else {
                    sstagname = stagname;
                }
            }
            if (sclassname != '' && sclassname != 'undefined') {
                try {
                    sclassnames = document.getElementsByClassName(sclassname);
                    if (sclassnames.length > 1) {
                        for (var k = 0; k < sclassnames.length; k++) {
                            if (sae[j] == sclassnames[k]) {
                                ssclassname = sclassname + '[' + k + ']'
                            }
                        }
                    } else {
                        ssclassname = sclassname;
                    }
                } catch (err) {
                    console.log(sclassname);
                    console.log("skipping this element: " + err);
                }
            }
            if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') {
                if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') {
                    if (sname != '' && sname != 'undefined') {
                        snames = document.getElementsByName(sname);
                        if (snames.length > 1) {
                            for (var k = 0; k < snames.length; k++) {
                                if (sae[j] == snames[k]) {
                                    stextvalue = sname + k;
                                }
                            }
                        } else {
                            stextvalue = sname;
                        }
                    } else if (sid != '' && sid != 'undefined') {
                        stextvalue = sid;
                    } else if (splaceholder != '' && splaceholder != 'undefined') {
                        stextvalue = splaceholder;
                    } else {
                        var seles = document.getElementsByTagName(stagname);
                        for (var k = 0; k < seles.length; k++) {
                            if (sae[j] == seles[k]) {
                                stextvalue = stagname + '_NONAME' + (k + 1);
                            }
                        }
                    }
                }
                // capture label content of the element
                function findLableForControl(ele) {
                    try {
                        var idVal = ele.id;
                        labels = document.getElementsByTagName('label');
                        if (labels.length !== 0) {
                            for( var i = 0; i < labels.length; i++ ) {
                                if (labels[i].htmlFor == idVal) {
                                    return labels[i].textContent;
                                }
                            }
                        }
                        else {
                            return null;
                        }
                    } catch (err) {
                        console.log("skipping this element: " + err);
                    }
                }
                if (slabel == '' || slabel == 'null' || slabel == 'undefined' || slabel == '0') {
                    if (splaceholder != '' && splaceholder != 'undefined') {
                        slabel = splaceholder;
                    } else if (sae[j].nodeName.toLowerCase() == 'input' || sae[j].nodeName.toLowerCase() == 'select' || sae[j].nodeName.toLowerCase() == 'textarea' || sae[j].nodeName.toLowerCase() == 'progress' || sae[j].nodeName.toLowerCase() == 'meter') {
                        slabel = findLableForControl(sae[j]);
                    }
                    if (sae[j].nodeName.toLowerCase() == 'input' && (slabel == null || slabel == '')) {
                        if (sae[j].hasAttribute('value')) {
                            slabel = sae[j].getAttribute('value');
                        }
                        else {
                            slabel = null;
                        }
                    }
                }

                // capture css selector of the element
                var sCssSelector = '';
                function getElementCount(ele, tag) {
                    try {
                        let tagIndex = '';
                        let arr = Array.from(ele.parentNode.children);
                        let tagNameArr = [];
                        for (i = 0; i < arr.length; i++) {
                            let tag = arr[i].tagName.toLowerCase();
                            tagNameArr.push(tag);
                        }
                        let count = tagNameArr.toString().match(new RegExp(tag, 'g')).length;
                        if (count > 1) {
                            let sib = ele.previousSibling, nth = 1;
                            while((sib != null) && nth++) {
                                if ((sib.nodeName.toLowerCase() == '#text') || (sib.nodeName.toLowerCase() == '#comment')) {
                                    nth--;
                                }
                                sib = sib.previousSibling;
                            }
                            tagIndex = ":nth-child("+nth+")";
                        }
                        return tagIndex;
                    } catch (err) {
                        console.log(err);
                    }
                }
                function getAttr(ele) {
                    try {
                        let arr = ['id','class','name','value','placeholder','title', 'href'];
                        let nodes=[], values=[];
                        for (var att, i = 0, atts = ele.attributes, n = atts.length; i < n; i++){
                            att = atts[i];
                            if (arr.includes(att.nodeName)) {
                                nodes.push(att.nodeName);
                                values.push(att.nodeValue);
                            }
                        }
                        return [nodes, values];
                    } catch (err) {
                        console.log(err);
                    }
                }
                function getCssSelector(ele) {
                    try {
                        let selector = parentSelector = childSelector = '';
                        let parentFlag = false;
                        let tag = ele.nodeName.toLowerCase();
                        if (ele != null && ele.attributes.length) {
                            let [nodes, values] = getAttr(ele);
                            for (let index=0; index < nodes.length; index++) {
                                if (values[index] != '') {
                                    if (document.querySelectorAll(`${tag}[${nodes[index]}="${values[index]}"]`).length == 1) {
                                        selector = `${tag}[${nodes[index]}="${values[index]}"]`;
                                        break;
                                    }
                                }
                            }
                            if (selector == '' && !parentFlag && nodes.length != 0 && values.slice(-1) != '') {
                                childSelector = `${tag}[${nodes.slice(-1)}="${values.slice(-1)}"]`;
                                parentFlag = true;
                            }
                            else if (selector == '' && nodes.length != 0 && values.slice(-1) == '') {
                                if (childSelector == '' && nodes.length > 1 && nodes.slice(-1) == 'class') {
                                    childSelector = `${tag}[${nodes[nodes.length-2]}="${values[values.length-2]}"]`;
                                    parentFlag = true;
                                }
                                else {
                                    let tagIndex = getElementCount(ele, tag);
                                    if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                                        selector = `${tag}${tagIndex}`;
                                    }
                                    else {
                                        childSelector = `${tag}${tagIndex}`;
                                        parentFlag = true;
                                    }
                                }
                            }
                            else if (selector == '' && childSelector == '') {
                                let tagIndex = getElementCount(ele, tag);
                                if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                                    selector = `${tag}${tagIndex}`;
                                }
                                else {
                                    childSelector = tag;
                                    parentFlag = true;
                                }
                            }
                        }
                        else {
                            let tagIndex = getElementCount(ele, tag);
                            if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                                selector = `${tag}${tagIndex}`;
                            }
                            else {
                                childSelector = `${tag}${tagIndex}`;
                                parentFlag = true;
                            }
                        }
                        if (parentFlag) {
                            let parentEle = ele.parentNode;
                            while (parentFlag && parentEle.nodeName.toLowerCase() != 'body') {
                                let parentTag = parentEle.nodeName.toLowerCase();
                                if (parentEle != null && parentEle.attributes.length) {
                                    let [parentNodes, parentValues] = getAttr(parentEle);
                                    for (let index=0; index < parentNodes.length; index++) {
                                        if (parentValues[index] != '') {
                                            if (document.querySelectorAll(`${parentTag}[${parentNodes[index]}="${parentValues[index]}"] ${childSelector}`).length == 1) {
                                                parentSelector = `${parentTag}[${parentNodes[index]}="${parentValues[index]}"]`;
                                                selector = `${parentSelector} ${childSelector}`;
                                                parentFlag = false;
                                                break;
                                            }
                                        }
                                    }
                                    if (selector == '') {
                                        if (document.querySelectorAll(`${parentTag} ${childSelector}`).length == 1) {
                                            selector = `${parentTag} ${childSelector}`;
                                            parentFlag = false;
                                        }
                                        else if (document.querySelectorAll(`${parentTag} ${childSelector}`).length > 1) {
                                            let tagIndex = getElementCount(parentEle, parentTag);
                                            if (document.querySelectorAll(`${parentTag}${tagIndex} ${childSelector}`).length == 1) {
                                                selector = `${parentTag}${tagIndex} ${childSelector}`;
                                                parentFlag = false;
                                            }
                                            else {
                                                parentEle = parentEle.parentNode;
                                            }
                                        }
                                        else {
                                            parentEle = parentEle.parentNode;
                                        }
                                    }
                                    else {
                                        parentFlag = false;
                                    }
                                }
                                else {
                                    let tagIndex = getElementCount(parentEle, parentTag);
                                    if (document.querySelectorAll(`${parentTag}${tagIndex} ${childSelector}`).length == 1) {
                                        selector = `${parentTag}${tagIndex} ${childSelector}`;
                                        parentFlag = false;
                                    }
                                    else {
                                        parentEle = parentEle.parentNode;
                                    }
                                }
                            }
                        }
                        return selector;
                    } catch (err) {
                        console.log("ERROR in get getCssSelector(): " + err);
                    }
                }
                sCssSelector = getCssSelector(sae[j]);

                // capture href of the element
                var shref='';
                function getHref(ele) {
                    try {
                        var href='';
                        if (ele.hasAttribute('href')) {
                            href = ele.getAttribute('href');
                        }
                        else {
                            href = null;
                        }
                        return href
                    } catch (err) {
                        console.log("skipping this element: " + err);
                    }
                }
                shref = getHref(sae[j]);

                if (sid == '') {
                    sid = 'null';
                }
                smultipleFlag = sae[j].hasAttribute('multiple');
                sishidden = sisVisible(sae[j]);
                if (sishidden == true || sishidden == 'True' || sishidden == 'true') {
                    sishidden = 'No';
                } else {
                    sishidden = 'Yes';
                }
                var sfirstpass = 0;
                var srpath = '';
                var setype = sae[j].getAttribute('type');
                setype = (String(setype)).toLowerCase();
                for (var spath = ''; sae[j] && sae[j].nodeType == 1; sae[j] = sae[j].parentNode.host || sae[j].parentNode) {
                    var spredicate = [];
                    var ssiblings = sae[j].parentNode.children;
                    var scount = 0;
                    var sunique = false;
                    var snewPath = '';
                    var sidx = 0;
                    for (var i = 0; ssiblings && (i < ssiblings.length); i++) {
                        if (ssiblings[i].tagName == sae[j].tagName) {
                            scount++;
                            if (ssiblings[i] == sae[j]) {
                                sidx = scount;
                            }
                        }
                    }
                    if (sidx == 1 && scount == 1) {
                        sidx = null;
                    }
                    if (suseId && sae[j].id) {
                        spredicate[spredicate.length] = '@id=' + '"' + sae[j].id + '"';
                        sunique = true;
                    }
                    xidx = (suseIdx && sidx) ? ('[' + sidx + ']') : '';
                    sidx = (suseIdx && sidx && !sunique) ? ('[' + sidx + ']') : '';
                    spredicate = (spredicate.length > 0) ? ('[' + spredicate.join(' and ') + ']') : '';
                    spath = '/' + sae[j].tagName.toLowerCase() + xidx + spath;
                    if (sfirstpass == 0) {
                        if (sunique && srelative) {
                            srpath = '//*' + sidx + spredicate + srpath;
                            sfirstpass = 1;
                        } else if (salesF) {
                            srpath = '//' + sae[j].tagName.toLowerCase() + sidx + spredicate + srpath;
                        } else {
                            srpath = '/' + sae[j].tagName.toLowerCase() + sidx + spredicate + srpath;
                        }
                    }
                }
                var firstpass = 0;
                var rpath1 = '';
                if (parentele != 'null') {
                    g = parentele;
                    for (var path1 = ''; g && g.nodeType == 1; g = g.parentNode) {
                        var predicate1 = [];
                        var siblings1 = g.parentNode.children;
                        var count1 = 0;
                        var unique1 = false;
                        for (var i = 0; siblings1 && (i < siblings1.length); i++) {
                            if (siblings1[i].tagName == g.tagName) {
                                count1++;
                                if (siblings1[i] == g) {
                                    idx1 = count1;
                                }
                            }
                        }
                        if (idx1 == 1 && count1 == 1) {
                            idx1 = null;
                        }
                        if (suseId && g.id) {
                            predicate1[predicate1.length] = '@id=' + '"' + g.id + '"';
                            unique1 = true;
                        }
                        xidx1 = (suseIdx && idx1) ? ('[' + idx1 + ']') : '';
                        idx1 = (suseIdx && idx1 && !unique1) ? ('[' + idx1 + ']') : '';
                        predicate1 = (predicate1.length > 0) ? ('[' + predicate1.join(' and ') + ']') : '';
                        path1 = '/' + g.tagName.toLowerCase() + xidx1 + path1;
                        if (firstpass == 0) {
                            if (unique1 && srelative) {
                                rpath1 = '//*' + idx1 + predicate1 + rpath1;
                                firstpass = 1;
                            } else {
                                rpath1 = '/' + g.tagName.toLowerCase() + idx1 + predicate1 + rpath1;
                            }
                        }
                    }
                    spath = path1 + spath;
                    srpath = rpath1 + srpath;
                }
                if (stagname == 'textarea') {
                    stagname = 'input';
                    stagtype = 'txtarea';
                } else if (stagname == 'select' && smultipleFlag) {
                    stagname = 'list';
                    stagtype = 'lst';
                } else if (stagname == 'select') {
                    stagtype = 'select';
                } else if (stagname == 'td' || stagname == 'tr') {
                    stagname = 'tablecell';
                    stagtype = 'tblcell';
                } else if (stagname == 'a') {
                    stagtype = 'lnk';
                } else if (stagname == 'table') {
                    stagtype = 'tbl';
                } else if (stagname == 'img') {
                    stagtype = 'img';
                } else if (stagname == 'input' && setype == 'image') {
                    stagname = 'img';
                    stagtype = 'img';
                }
                if (stagname == 'input' && (setype == 'button' || setype == 'submit' || setype == 'reset' || setype == 'file')) {
                    stagname = 'button';
                    stagtype = 'btn';
                } else if (stagname == 'input' && setype == 'radio') {
                    stagname = 'radiobutton';
                    stagtype = 'radiobtn';
                } else if (stagname == 'input' && setype == 'checkbox') {
                    stagname = 'checkbox';
                    stagtype = 'chkbox';
                } else if (stagname == 'input' && (setype == 'text' || setype == 'email' || setype == 'number' || setype == 'password' || setype == 'range' || setype == 'search' || setype == 'url')) {
                    stagname = 'input';
                    stagtype = 'txtbox';
                } else if (stagname == 'input' && stagtype == '' && (setype == 'hidden' || setype == 'null')) {
                    stagname = 'div';
                    stagtype = 'elmnt';
                } else if (stagname == 'button') {
                    stagname = 'button';
                    stagtype = 'btn';
                } else if (stagname == 'lightning-combobox' || stagname == 'lightning-grouped-combobox') {
                    stagtype = stagname;
                    stagname = 'select';
                }
                if (role == 'grid') {
                    stagname = 'grid';
                    stagtype = 'grid';
                }
                if (salesF) {
                    stextvalue = stagname + '_Salesforce' + ssalesforcecounter + '_sfc';
                    ssalesforcecounter = ssalesforcecounter + 1;
                }
                stextvalue = stextvalue.replace(">", "");
                stextvalue = stextvalue.replace("</", "");
                stextvalue = stextvalue.replace("<", "");
                stextvalue = stextvalue.replace("/>", "");
                stextvalue = stextvalue.split("\\n").join("");
                stextvalue = stextvalue.split("\\t").join("");
                stextvalue = stextvalue.split("\\r").join("");
                stextvalue = stextvalue.split("  ").join("");
                stextvalue = stextvalue.split("\\u00a0").join("");
                if (stextvalue == '' || stextvalue.length == 0 || stextvalue == '0') {
                    stextvalue = 'NONAME' + snonamecounter;
                    snonamecounter = snonamecounter + 1;
                    scustname = stextvalue;
                } else {
                    scustname = stextvalue;
                }
                if (stagtype != '') {
                    scustname = scustname + '_' + stagtype;
                } else {
                    scustname = scustname + '_elmnt';
                }
                coordinates = left + ';' + top + ';' + height + ';' + width;
                coordinates = String(coordinates);
                snewPath = String(spath) + ';' + String(sid) + ';' + String(srpath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + slabel + ';' + shref + ';' + sCssSelector;
                sarr.push({
                    'xpath': snewPath,
                    'tag': stagname,
                    'hiddentag': sishidden,
                    'url': surl,
                    'height': height,
                    'width': width,
                    'custname': scustname,
                    'top': top,
                    'left': left
                });
            }
        }
        return sarr;

        function findCoordinates(element) {
            height = element.offsetHeight || 0;
            width = element.offsetWidth || 0;
            top = 0;
            left = 0;
            do {
                top += element.offsetTop || 0;
                left += element.offsetLeft || 0;
                element = element.offsetParent;
            } while (element);
        }

        function sgetNodesOuter() {
            var elementsarray = [];
            scrapeOption = scrapeOption.toLowerCase();
            if (scrapeOption === 'full') {
                elementsarray = HTMLCollectionToArray(document.getElementsByTagName('*'));
                salele = document.getElementsByTagName('one-record-home-flexipage2');
                salele1 = document.getElementsByTagName('records-lwc-detail-panel');
                if (salele.length > 0) {
                    for (var i = 0; i < salele.length; i++) {
                        elementsarray = elementsarray.concat(HTMLCollectionToArray(salele[i].getElementsByTagName('*')));
                    }
                }
                if (salele1.length > 0) {
                    for (var i = 0; i < salele1.length; i++) {
                        elementsarray = elementsarray.concat(HTMLCollectionToArray(salele1[i].getElementsByTagName('*')));
                    }
                }
            } else if (scrapeOption === 'button') {
                var array1 = HTMLCollectionToArray(document.getElementsByTagName('button'));
                var temparray2 = HTMLCollectionToArray(document.getElementsByTagName('input'));
                var array2 = [];
                temparray2.forEach(function (element) {
                    elementType = element.getAttribute('type');
                    if (elementType) {
                        elementType = elementType.toLowerCase();
                        if (elementType == 'button' || elementType == 'submit' || elementType == 'reset' || elementType == 'file') array2.push(element);
                    }
                });
                elementsarray.extend(array1);
                elementsarray.extend(array2);
            } else if (scrapeOption === 'checkbox' || scrapeOption === 'radiobutton') {
                var temparray1 = HTMLCollectionToArray(document.getElementsByTagName('input'));
                var array1 = [];
                var typeCheck = scrapeOption === 'checkbox' ? 'checkbox' : 'radio';
                temparray1.forEach(function (element) {
                    elementType = element.getAttribute('type');
                    if (elementType) {
                        if (elementType.toLowerCase() == typeCheck) array1.push(element);
                    }
                });
                elementsarray.extend(array1);
            } else if (scrapeOption === 'textbox') {
                var temparray1 = HTMLCollectionToArray(document.getElementsByTagName('input'));
                var array1 = [];
                var typeCheck = ["text", "email", "number", "password", "range", "search", "url"];
                temparray1.forEach(function (element) {
                    elementType = element.getAttribute('type');
                    if (elementType) {
                        if (typeCheck.indexOf(elementType.toLowerCase()) != -1) array1.push(element);
                    }
                });
                elementsarray.extend(array1);
            } else if (scrapeOption === 'dropdown' || scrapeOption === 'listbox') {
                var temparray1 = HTMLCollectionToArray(document.getElementsByTagName('select'));
                var array1 = [];
                var array2 = [];
                temparray1.forEach(function (element) {
                    if (element.hasAttribute('multiple')) {
                        if (scrapeOption === 'listbox') array2.push(element);
                    } else array1.push(element);
                });
                scrapeOption === 'dropdown' ? elementsarray.extend(array1) : elementsarray.extend(array2);
            } else if (scrapeOption === 'image' || scrapeOption === 'link' || scrapeOption === 'table') {
                var tagCheck = {
                    "image": "img",
                    "link": "a",
                    "table": "table"
                };
                elementsarray = HTMLCollectionToArray(document.getElementsByTagName(tagCheck[scrapeOption]));
            } else if (scrapeOption === 'grid') {
                var array1 = HTMLCollectionToArray(document.getElementsByTagName('*'));
                array1.forEach(function (element) {
                    if (element.hasAttribute('role')) {
                        if (element.getAttribute('role') === 'grid' && element.tagName.toLowerCase() === 'div') {
                            elementsarray.push(element);
                        }
                    }
                });
            } else if (scrapeOption === 'element') {
                var temparray1 = HTMLCollectionToArray(document.getElementsByTagName('*'));
                excludeTagList = ["button", "input", "select", "img", "a", "textarea", "table", "td", "tr"];
                temparray1.forEach(function (element) {
                    elementTagName = element.tagName;
                    if (elementTagName) {
                        if (excludeTagList.indexOf(elementTagName.toLowerCase()) == -1) elementsarray.push(element);
                    }
                });
            } else if (scrapeOption == 'other tag') {
                elementsarray = HTMLCollectionToArray(document.getElementsByTagName(scrapeOptionValue));
            } else if (scrapeOption.toLowerCase() == 'select a section using xpath') {
                elementsarray.push(scrapeOptionValue);
                elementsarray.extend(HTMLCollectionToArray(scrapeOptionValue.getElementsByTagName('*')));
            } else {
                elementsarray = HTMLCollectionToArray(document.getElementsByTagName('*'));
            }
            return elementsarray;
        };

        function HTMLCollectionToArray(x) {
            for (var i = 0, a = []; i < x.length; i++) a.push(x[i]);
            return a
        };

        function saddNodesOuter(sarray, scollection) {
            for (var i = 0; scollection && scollection.length && i < scollection.length; i++) {
                sarray.push(scollection[i]);
            }
        };

        function stext_content(f) {
            var sfirstText = '';
            var stextdisplay = '';
            for (var z = 0; z < f.childNodes.length; z++) {
                var scurNode = f.childNodes[z];
                swhitespace = /^\s*$/;
                if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {
                    sfirstText = scurNode.nodeValue;
                    stextdisplay = stextdisplay + sfirstText;
                }
            }
            return (stextdisplay);
        };
    """

    """Javascript logic used in fullscrape operation with Visibility Flag"""
    javascript_fullscrape_Visiblity = """if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {	(function () {		function hasAttribute(attrName) {			return typeof this[attrName] !== 'undefined';		}		var inputs = document.getElementsByTagName('*');		for (var i = 0; i < inputs.length; i++) {			inputs[i].hasAttribute = hasAttribute;		}	}		());}if (!window.Element || !window.Element.prototype || !window.Element.prototype.getAttribute) {	(function () {		function getAttribute(attrName) {			return typeof this[attrName] !== 'undefined';		}		var inputs = document.getElementsByTagName('*');		for (var i = 0; i < inputs.length; i++) {			inputs[i].getAttribute = getAttribute;		}	}		());}(function () {	if (!document.getElementsByClassName) {		var indexOf = [].indexOf || function (prop) {			for (var i = 0; i < this.length; i++) {				if (this[i] === prop)					return i;			}			return -1;		};		getElementsByClassName = function (className, context) {			var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function () {					var all = context.getElementsByTagName("*"),					elements = [],					i = 0;					for (; i < all.length; i++) {						if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1)							elements.push(all[i]);					}					return elements;				})();			return elems;		};		document.getElementsByClassName = function (className) {			return getElementsByClassName(className, document);		};		if (window.Element) {			window.Element.prototype.getElementsByClassName = function (className) {				return getElementsByClassName(className, this);			};		}	}})();var suseIdx = true;var suseId = true;var suseClass = true;var srelative = true;var sae = [];var sarr = [];var sele = [];var smyid = 0;var stextvalue = '';var stagname = 0;var sishidden = 0;var scustname = '';var smultipleFlag = false;var surl = arguments[0];var snonamecounter = 1;var txt_area_nonamecounter = 1;var select_nonamecounter = 1;var td_nonamecounter = 1;var a_nonamecounter = 1;var table_nonamecounter = 1;var input_nonamecounter = 1;var ssalesforcecounter = 1;var stagtype = '';var ssname = 'null';var sstagname = 'null';var ssclassname = 'null';var sclassname = 'null';var top = 0;var left = 0;var height = 0;var width = 0;var coordinates = '';var scrapeOption = arguments[1][0];var scrapeOptionValue;var salesF = false;if (arguments[1].length > 1)	scrapeOptionValue = arguments[1][1];var sisVisible = (function () {	function inside(schild, sparent) {		while (schild) {			if (schild === sparent)				return true;			schild = schild.parentNode;		}		return false;	};	return function (selem) {		if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0)			return false;		var srect = selem.getBoundingClientRect();		if (window.getComputedStyle || selem.currentStyle) {			var sel = selem,			scomp = null;			var sal = (selem.tagName.toLowerCase().indexOf('lightning') != -1);			while (sel) {				if (sel === document) {					break;				} else if (sel.nodeName == '#document-fragment') {					sel = sel.host;				} else if (!sel.parentNode)					return false;				if (sel instanceof(HTMLElement))					scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;				if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0))))					return false;				sel = sel.parentNode;			}		}		return true;	}})();Array.prototype.extend = function (other_array) {	other_array.forEach(function (v) {		this.push(v)	}, this);};sae = sgetNodesOuter();for (var j = 0; j < sae.length; j++) {	stagtype = '';	ssname = 'null';	sstagname = 'null';	sid = sae[j].id;	sname = sae[j].name;	salttext = sae[j].alt;	splaceholder = sae[j].placeholder;	sclassname = sae[j].className;	sid = (String(sid));	sclassname = (String(sclassname));	sname = (String(sname));	splaceholder = (String(splaceholder));	stextvalue = stext_content(sae[j]);	stextvalue = (String(stextvalue));	stagname = sae[j].tagName.toLowerCase();	ssname = 'null';	sstagname = 'null';	ssclassname = 'null';	findCoordinates(sae[j]);	salesF = (sae[j].tagName.toLowerCase().indexOf('lightning') != -1);	if (stagname.indexOf(':') != -1) {		stagname = stagname.replace(':', '');		stagname = 'custom' + stagname;	}	if (sname != '' && sname != 'undefined') {		snames = document.getElementsByName(sname);		if (snames.length > 1) {			for (var k = 0; k < snames.length; k++) {				if (sae[j] == snames[k]) {					ssname = sname + '[' + k + ']'				}			}		} else {			ssname = sname;		}	}	if (stagname != '' && stagname != 'undefined') {		stagnames = document.getElementsByTagName(stagname);		if (stagnames.length > 1) {			for (var k = 0; k < stagnames.length; k++) {				if (sae[j] == stagnames[k]) {					sstagname = stagname + '[' + k + ']'				}			}		} else {			sstagname = stagname;		}	}	if (sclassname != '' && sclassname != 'undefined') {		try {			sclassnames = document.getElementsByClassName(sclassname);			if (sclassnames.length > 1) {				for (var k = 0; k < sclassnames.length; k++) {					if (sae[j] == sclassnames[k]) {						ssclassname = sclassname + '[' + k + ']'					}				}			} else {				ssclassname = sclassname;			}		} catch (err) {			console.log(sclassname);			console.log("skipping this element: " + err);		}	}	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') {		if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') {			if (sname != '' && sname != 'undefined') {				snames = document.getElementsByName(sname);				if (snames.length > 1) {					for (var k = 0; k < snames.length; k++) {						if (sae[j] == snames[k]) {							stextvalue = sname + k;						}					}				} else {					stextvalue = sname;				}			} else if (sid != '' && sid != 'undefined') {				stextvalue = sid;			} else if (splaceholder != '' && splaceholder != 'undefined') {				stextvalue = splaceholder;			} else {				var seles = document.getElementsByTagName(stagname);				for (var k = 0; k < seles.length; k++) {					if (sae[j] == seles[k]) {						stextvalue = stagname + '_NONAME' + (k + 1);					}				}			}		}		if (sid == '') {			sid = 'null';		}		smultipleFlag = sae[j].hasAttribute('multiple');		sishidden = sisVisible(sae[j]);		if (sishidden == true || sishidden == 'True' || sishidden == 'true') {			sishidden = 'No';		} else {			sishidden = 'Yes';		}		var sfirstpass = 0;		var srpath = '';		var setype = sae[j].getAttribute('type');		setype = (String(setype)).toLowerCase();		for (var spath = ''; sae[j] && sae[j].nodeType == 1; sae[j] = sae[j].parentNode.host || sae[j].parentNode) {			var spredicate = [];			var ssiblings = sae[j].parentNode.children;			var scount = 0;			var sunique = false;			var snewPath = '';			var sidx = 0;			for (var i = 0; ssiblings && (i < ssiblings.length); i++) {				if (ssiblings[i].tagName == sae[j].tagName) {					scount++;					if (ssiblings[i] == sae[j]) {						sidx = scount;					}				}			}			if (sidx == 1 && scount == 1) {				sidx = null;			}			if (suseId && sae[j].id) {				spredicate[spredicate.length] = '@id=' + '"' + sae[j].id + '"';				sunique = true;			}			xidx = (suseIdx && sidx) ? ('[' + sidx + ']') : '';			sidx = (suseIdx && sidx && !sunique) ? ('[' + sidx + ']') : '';			spredicate = (spredicate.length > 0) ? ('[' + spredicate.join(' and ') + ']') : '';			spath = '/' + sae[j].tagName.toLowerCase() + xidx + spath;			if (sfirstpass == 0) {				if (sunique && srelative) {					srpath = '//*' + sidx + spredicate + srpath;					sfirstpass = 1;				} else if (salesF) {					srpath = '//' + sae[j].tagName.toLowerCase() + sidx + spredicate + srpath;				} else {					srpath = '/' + sae[j].tagName.toLowerCase() + sidx + spredicate + srpath;				}			}		}		if (stagname == 'textarea') {			stagname = 'input';			stagtype = 'txtarea';		} else if (stagname == 'select' && smultipleFlag) {			stagname = 'list';			stagtype = 'lst';		} else if (stagname == 'select') {			stagtype = 'select';		} else if (stagname == 'td' || stagname == 'tr') {			stagname = 'tablecell';			stagtype = 'tblcell';		} else if (stagname == 'a') {			stagtype = 'lnk';		} else if (stagname == 'table') {			stagtype = 'tbl';		} else if (stagname == 'img') {			stagtype = 'img';		} else if (stagname == 'input' && setype == 'image') {			stagname = 'img';			stagtype = 'img';		}		if (stagname == 'input' && (setype == 'button' || setype == 'submit' || setype == 'reset' || setype == 'file')) {			stagname = 'button';			stagtype = 'btn';		} else if (stagname == 'input' && setype == 'radio') {			stagname = 'radiobutton';			stagtype = 'radiobtn';		} else if (stagname == 'input' && setype == 'checkbox') {			stagname = 'checkbox';			stagtype = 'chkbox';		} else if (stagname == 'input' && (setype == 'text' || setype == 'email' || setype == 'number' || setype == 'password' || setype == 'range' || setype == 'search' || setype == 'url')) {			stagname = 'input';			stagtype = 'txtbox';		} else if (stagname == 'input' && stagtype == '' && (setype == 'hidden' || setype == 'null')) {			stagname = 'div';			stagtype = 'elmnt';		} else if (stagname == 'button') {			stagname = 'button';			stagtype = 'btn';		} else if (stagname == 'lightning-combobox' || stagname == 'lightning-grouped-combobox') {			stagtype = stagname;			stagname = 'select';		}		if (salesF) {			stextvalue = stagname + '_Salesforce' + ssalesforcecounter + '_sfc';			ssalesforcecounter = ssalesforcecounter + 1;		}		stextvalue = stextvalue.replace(">", "");		stextvalue = stextvalue.replace("</", "");		stextvalue = stextvalue.replace("<", "");	stextvalue = stextvalue.replace("/>", "");		stextvalue = stextvalue.split("\\n").join("");		stextvalue = stextvalue.split("\\t").join("");		stextvalue = stextvalue.split("\\r").join("");		stextvalue = stextvalue.split("  ").join("");		stextvalue = stextvalue.split("\\u00a0").join("");		if (stextvalue == '' || stextvalue.length == 0 || stextvalue == '0') {			stextvalue = 'NONAME' + snonamecounter;			snonamecounter = snonamecounter + 1;			scustname = stextvalue;		} else {			scustname = stextvalue;		}		if (stagtype != '') {			scustname = scustname + '_' + stagtype;		} else {			scustname = scustname + '_elmnt';		}		coordinates = left + ';' + top + ';' + height + ';' + width;		coordinates = String(coordinates);		snewPath = String(srpath) + ';' + String(sid) + ';' + String(spath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + stextvalue;		if (sishidden === 'No') {			sarr.push({				'xpath': snewPath,				'tag': stagname,				'hiddentag': sishidden,				'url': surl,				'height': height,				'width': width,				'custname': scustname,				'top': top,				'left': left			});		}	}}return sarr;function findCoordinates(element) {	height = element.offsetHeight || 0;	width = element.offsetWidth || 0;	top = 0;	left = 0;	do {		top += element.offsetTop || 0;		left += element.offsetLeft || 0;		element = element.offsetParent;	} while (element);}function sgetNodesOuter() {	var elementsarray = [];	scrapeOption = scrapeOption.toLowerCase();	if (scrapeOption === 'full') {		elementsarray = HTMLCollectionToArray(document.getElementsByTagName('*'));		salele = document.getElementsByTagName('one-record-home-flexipage2');		salele1 = document.getElementsByTagName('records-lwc-detail-panel');		if (salele.length > 0) {			for (var i = 0; i < salele.length; i++) {				elementsarray = elementsarray.concat(HTMLCollectionToArray(salele[i].getElementsByTagName('*')));			}		}		if (salele1.length > 0) {			for (var i = 0; i < salele1.length; i++) {				elementsarray = elementsarray.concat(HTMLCollectionToArray(salele1[i].getElementsByTagName('*')));			}		}	} else if (scrapeOption === 'button') {		var array1 = HTMLCollectionToArray(document.getElementsByTagName('button'));		var temparray2 = HTMLCollectionToArray(document.getElementsByTagName('input'));		var array2 = [];		temparray2.forEach(function (element) {			elementType = element.getAttribute('type');			if (elementType) {				elementType = elementType.toLowerCase();				if (elementType == 'button' || elementType == 'submit' || elementType == 'reset' || elementType == 'file')					array2.push(element);			}		});		elementsarray.extend(array1);		elementsarray.extend(array2);	} else if (scrapeOption === 'checkbox' || scrapeOption === 'radiobutton') {		var temparray1 = HTMLCollectionToArray(document.getElementsByTagName('input'));		var array1 = [];		var typeCheck = scrapeOption === 'checkbox' ? 'checkbox' : 'radio';		temparray1.forEach(function (element) {			elementType = element.getAttribute('type');			if (elementType) {				if (elementType.toLowerCase() == typeCheck)					array1.push(element);			}		});		elementsarray.extend(array1);	} else if (scrapeOption === 'textbox') {		var temparray1 = HTMLCollectionToArray(document.getElementsByTagName('input'));		var array1 = [];		var typeCheck = ["text", "email", "number", "password", "range", "search", "url"];		temparray1.forEach(function (element) {			elementType = element.getAttribute('type');			if (elementType) {				if (typeCheck.indexOf(elementType.toLowerCase()) != -1)					array1.push(element);			}		});		elementsarray.extend(array1);	} else if (scrapeOption === 'dropdown' || scrapeOption === 'listbox') {		var temparray1 = HTMLCollectionToArray(document.getElementsByTagName('select'));		var array1 = [];		var array2 = [];		temparray1.forEach(function (element) {			if (element.hasAttribute('multiple')) {				if (scrapeOption === 'listbox')					array2.push(element);			} else				array1.push(element);		});		scrapeOption === 'dropdown' ? elementsarray.extend(array1) : elementsarray.extend(array2);	} else if (scrapeOption === 'image' || scrapeOption === 'link' || scrapeOption === 'table') {		var tagCheck = {			"image": "img",			"link": "a",			"table": "table"		};		elementsarray = HTMLCollectionToArray(document.getElementsByTagName(tagCheck[scrapeOption]));	} else if (scrapeOption === 'element') {		var temparray1 = HTMLCollectionToArray(document.getElementsByTagName('*'));		excludeTagList = ["button", "input", "select", "img", "a", "textarea", "table", "td", "tr"];		temparray1.forEach(function (element) {			elementTagName = element.tagName;			if (elementTagName) {				if (excludeTagList.indexOf(elementTagName.toLowerCase()) == -1)					elementsarray.push(element);			}		});	} else if (scrapeOption == 'other tag') {		elementsarray = HTMLCollectionToArray(document.getElementsByTagName(scrapeOptionValue));	} else if (scrapeOption.toLowerCase() == 'select a section using xpath') {		elementsarray.push(scrapeOptionValue);		elementsarray.extend(HTMLCollectionToArray(scrapeOptionValue.getElementsByTagName('*')));	} else {		elementsarray = HTMLCollectionToArray(document.getElementsByTagName('*'));	}	return elementsarray;};function HTMLCollectionToArray(x) {	for (var i = 0, a = []; i < x.length; i++)		a.push(x[i]);	return a};function saddNodesOuter(sarray, scollection) {	for (var i = 0; scollection && scollection.length && i < scollection.length; i++) {		sarray.push(scollection[i]);	}};function stext_content(f) {	var sfirstText = '';	var stextdisplay = '';	for (var z = 0; z < f.childNodes.length; z++) {		var scurNode = f.childNodes[z];		swhitespace = /^\s*$/;		if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {			sfirstText = scurNode.nodeValue;			stextdisplay = stextdisplay + sfirstText;		}	}	return (stextdisplay);};"""

    """Javascript logic used in start click and add operation"""
    javascript_clicknadd = """
        //window.location.href = 'https://google.com';
        if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {
            (function () {
                function hasAttribute(attrName) {
                    return typeof this[attrName] !== 'undefined';
                }
                var inputs = document.getElementsByTagName('select');
                for (var i = 0; i < inputs.length; i++) {
                    inputs[i].hasAttribute = hasAttribute;
                }
            }());
        } (function () {
            if (!document.getElementsByClassName) {
                var indexOf = [].indexOf || function (prop) {
                    for (var i = 0; i < this.length; i++) {
                        if (this[i] === prop) return i;
                    }
                    return -1;
                };
                getElementsByClassName = function (className, context) {
                    var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function () {
                        var all = context.getElementsByTagName("*"),
                            elements = [],
                            i = 0;
                        for (; i < all.length; i++) {
                            if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) elements.push(all[i]);
                        }
                        return elements;
                    })();
                    return elems;
                };
                document.getElementsByClassName = function (className) {
                    return getElementsByClassName(className, document);
                };
                if (window.Element) {
                    window.Element.prototype.getElementsByClassName = function (className) {
                        return getElementsByClassName(className, this);
                    };
                }
            }
        })();
        var useIdx = true;
        var useId = true;
        var useClass = true;
        var relative = true;
        var ae = [];
        var be = [];
        var url = arguments[0];
        var browser = arguments[1];
        var ishidden = 0;
        var tagname = 0;
        var textvalue = '';
        var label = '';
        var arr = [];
        var custname = '';
        var tagtype = '';
        var multipleFlag = false;
        var uniqueFlag = false;
        var nonamecounter = 1;
        var txt_area_nonamecounter = 1;
        var select_nonamecounter = 1;
        var td_nonamecounter = 1;
        var a_nonamecounter = 1;
        var table_nonamecounter = 1;
        var input_nonamecounter = 1;
        var salesforcecounter = 1;
        var ssname = 'null';
        var sstagname = 'null';
        var ssclassname = 'null';
        var top = 0;
        var left = 0;
        var height = 0;
        var width = 0;
        var co = 0;
        var coordinates = '';
        var viewTop = 0;
        var isIE = false || !!document.documentMode;
        var salesF = false;
        var isVisible = (function () {
            function inside(child, parent) {
                while (child) {
                    if (child === parent) return true;
                    child = child.parentNode;
                }
                return false;
            };
            return function (elem) {
                if (document.hidden || elem.offsetWidth == 0 || elem.offsetHeight == 0 || elem.style.visibility == 'hidden' || elem.style.display == 'none' || elem.style.opacity === 0) return false;
                var rect = elem.getBoundingClientRect();
                if (window.getComputedStyle || elem.currentStyle) {
                    var el = elem,
                        comp = null;
                    while (el) {
                        if (el === document) {
                            break;
                        } else if (el.nodeName == '#document-fragment') {
                            el = el.host;
                        } else if (!el.parentNode) return false;
                        if (el instanceof (HTMLElement)) comp = window.getComputedStyle ? window.getComputedStyle(el, null) : el.currentStyle;
                        if (comp && (comp.visibility == 'hidden' || comp.display == 'none' || (typeof comp.opacity !== 'undefined' && !(comp.opacity > 0)))) return false;
                        el = el.parentNode;
                    }
                }
                return true;
            }
        })();
        window.tastopflag = false;
        ele = document.getElementsByTagName('*');
        for (var i=0;i<ele.length;i++)
        {
            ae.push(ele[i]);
            if (ele[i].shadowRoot)
                addNodesOuter(ae, ele[i].getElementsByTagName('*'));
        }
        // addNodesOuter(ae, document.getElementsByTagName('*'));
        // salele = document.getElementsByTagName('one-record-home-flexipage2');
        // if (salele.length > 0) addNodesOuter(ae, salele[0].getElementsByTagName('*'));
        // salele = document.getElementsByTagName('records-lwc-detail-panel');
        // if (salele.length > 0) addNodesOuter(ae, salele[0].getElementsByTagName('*'));
        var css = '.AvoAssureCheckboxHighlight {outline:2px solid black!important;opacity:1!important; box-shadow: 0px 0px 0px 4px yellow !important;}',
            head = document.head || document.getElementsByTagName('head')[0],
            style = document.createElement('style');
        style.type = 'text/css';
        style.id = 'AvoAssureCheckboxHighlight';
        if (style.styleSheet) {
            style.styleSheet.cssText = css;
        } else {
            style.appendChild(document.createTextNode(css));
        }
        var css0 = 'table:hover{border:6px solid !important}'; 
        head = document.head || document.getElementsByTagName('head')[0], style0 = document.createElement('style'); 
        style0.type = 'text/css'; style0.id = 'AvoAssure_Table';
        if (style0.styleSheet) 
        { 
            style0.styleSheet.cssText = css0; } 
        else { 
            style0.appendChild(document.createTextNode(css0)); 
            }

        style_new = document.createElement('style');
        style_new.type = 'text/css';
        style_new.id = 'AvoAssureBorderHighlight';
        var css2 = '.AvoAssureBorderHighlight { border: 2px black solid !important; outline: 2px yellow solid !important; }';
        if (style_new.styleSheet) {
            style_new.styleSheet.cssText = css2;
        } else {
            style_new.appendChild(document.createTextNode(css2));
        }
        if (head == undefined) {
            Avo_head = document.createElement('head');
            Avo_head.id = 'AvoAssure_head';
            var html = document.children[0];
            Avo_head.appendChild(style);
            Avo_head.appendChild(style_new);
            Avo_head.appendChild(style0);
            html.appendChild(Avo_head);
        } else {
            head.appendChild(style);
            head.appendChild(style_new);
            head.appendChild(style0);
        }

        function getElementsByClassName(classname) {
            var a = [];
            var re = new RegExp('(^| )' + classname + '( |$)');
            var els = document.getElementsByTagName("*");
            var elesal = document.getElementsByTagName("one-record-home-flexipage2");
            var elesal1 = document.getElementsByTagName("records-lwc-detail-panel");
            for (var i = 0, j = els.length; i < j; i++)
                if (re.test(els[i].className)) a.push(els[i]);
            if (elesal.length > 0) {
                els1 = elesal[0].getElementsByTagName("*");
                for (var i = 0, j = els1.length; i < j; i++) {
                    if (re.test(els1[i].className)) {
                        a.push(els1[i]);
                    }
                }
            }
            if (elesal1.length > 0) {
                els2 = elesal1[0].getElementsByTagName("*");
                for (var i = 0, j = els2.length; i < j; i++) {
                    if (re.test(els2[i].className)) {
                        a.push(els2[i]);
                    }
                }
            }
            return a;
        }

        function leave_handler(event) {
            var event = event || window.event;
            if (event.ctrlKey) {
                return true;
            }
            if (event.preventDefault) {
                event.preventDefault();
                event.stopPropagation();
            }
            var f = event.fromElement || event.target || event.srcElement;
            var classNameT = 'AvoAssureBorderHighlight';
            var classNameTT = 'AvoAssureCheckboxHighlight';
            if (f.classList) {
                f.classList.remove(classNameT);
                f.classList.remove(classNameTT);
            } else if (hasClass(f, classNameT)) {
                var reg = new RegExp('(\\s|^)' + classNameT + '(\\s|$)');
                f.className = f.className.replace(reg, ' ');
            } else if (hasClass(f, classNameTT)) {
                var reg = new RegExp('(\\s|^)' + classNameTT + '(\\s|$)');
                f.className = f.className.replace(reg, ' ');
            }
        }

        function hov_handler(event) {
            var event = event || window.event;
            if (event.ctrlKey) {
                return true;
            }
            if (event.preventDefault) {
                event.preventDefault();
                event.stopPropagation();
            }
            var f = event.toElement || event.target || event.srcElement;
            var tagname = f.tagName.toLowerCase();
            var classNameT = 'AvoAssureBorderHighlight';
            var classNameTT = 'AvoAssureCheckboxHighlight';
            var a = getElementsByClassName(classNameT);
            var b = getElementsByClassName(classNameTT);
            i = 0;
            if (a.length > 0) {
                if (a[i].classList) {
                    a[i].classList.remove(classNameT);
                } else if (hasClass(a[i], classNameT)) {
                    var reg = new RegExp('(\\s|^)' + classNameT + '(\\s|$)');
                    a[i].className = a[i].className.replace(reg, ' ');
                }
            }
            if (b.length > 0) {
                if (b[i].classList) {
                    b[i].classList.remove(classNameTT);
                } else if (hasClass(b[i], classNameTT)) {
                    var reg = new RegExp('(\\s|^)' + classNameTT + '(\\s|$)');
                    b[i].className = b[i].className.replace(reg, ' ');
                }
            }
            if (tagname != 'script' && tagname != 'meta' && tagname != 'html' && tagname != 'head' && tagname != 'style' && tagname != 'body' && tagname != 'form' && tagname != 'link' && tagname != 'noscript' && tagname != '!' && tagname != 'pre' && tagname != 'code' && tagname != 'animatetransform' && tagname != 'noembed' && tagname != 'iframe' && tagname != 'frame') {
                if (browser == 3) {
                    if (f.type == 'checkbox' || f.type == 'radio' || tagname == 'td' || tagname == 'th') {
                        f.className += ' ' + classNameTT;
                    } else {
                        f.className += ' ' + classNameT;
                    }
                } else {
                    if (f.type == 'checkbox' || f.type == 'radio' || tagname == 'td' || tagname == 'th') {
                        console.log('hover highlight radio/checkbox');
                        f.classList.add(classNameTT);
                    } else {
                        console.log('hover highlight');
                        f.classList.add(classNameT);
                    }
                }
            }
        }
        var currentElement;
        function handler(event) {
        debugger;
            tagtype = '';
            if (window.tastopflag == 'true') {
                if (window.Prototype) {
                    var _arr_tojson = Array.prototype.toJSON;
                    delete Array.prototype.toJSON;
                    window.tasarr = arr;
                    Array.prototype.toJSON = _arr_tojson;
                } else {
                    window.tasarr = arr;
                }
                clickStop(ae, isIE, be);
                function clickStop(ae, isIE, be) {
                    if (isIE) {
                        for (var i = 0; i < ae.length; i++) {
                            if (ae[i].removeEventListener) {
                                ae[i].removeEventListener('click', handler, true);
                                ae[i].removeEventListener('mouseover', hov_handler, true);
                                ae[i].removeEventListener('mouseleave', leave_handler, true);
                                ae[i].removeEventListener('mousedown', block_handler, true);
                                ae[i].removeEventListener('mouseup', block_handler, true);
                            } else if (ae[i].detachEvent) {
                                ae[i].detachEvent('onclick', handler);
                                ae[i].detachEvent('onmouseover', hov_handler);
                                ae[i].detachEvent('onmouseleave', leave_handler);
                                ae[i].detachEvent('onmousedown', block_handler);
                                ae[i].detachEvent('onmouseup', block_handler);
                            }
                            if ((ae[i].getAttribute("_onclick")) != null) {
                                ae[i].parentNode.replaceChild(be[i], ae[i]);
                            }
                        }
                    } else {
                        for (var i = 0; i < ae.length; i++) {
                            if (ae[i].removeEventListener) {
                                ae[i].removeEventListener('click', handler, true);
                                ae[i].removeEventListener('mouseover', hov_handler, true);
                                ae[i].removeEventListener('mouseleave', leave_handler, true);
                                ae[i].removeEventListener('mousedown', block_handler, true);
                                ae[i].removeEventListener('mouseup', block_handler, true);
                            } else if (ae[i].detachEvent) {
                                ae[i].detachEvent('onclick', handler);
                                ae[i].detachEvent('onmouseover', hov_handler);
                                ae[i].detachEvent('onmouseleave', leave_handler);
                                ae[i].detachEvent('onmousedown', block_handler);
                                ae[i].detachEvent('onmouseup', block_handler);
                            }
                            if ((ae[i].getAttribute("_onclick")) != null) {
                                var _onclickval = ae[i].getAttribute("_onclick");
                                ae[i].removeAttribute("_onclick");
                                ae[i].setAttribute("onclick", _onclickval);
                            }
                        }
                    }
                }
                window.tastopflag = false;
                arr = [];
                return true;
            } else {
                ssclassname = 'null';
                ssname = 'null';
                sstagname = 'null';
                if (event.ctrlKey) {
                    return true;
                }
                if (event.preventDefault) {
                    event.preventDefault();
                    event.stopPropagation();
                    event.cancelBubble = true;
                    event.returnValue = false;
                } else {
                    window.event.cancelBubble = true;
                    window.event.returnValue = false;
                }
                var e = currentElement || event.target || event.srcElement;
                var f = currentElement || event.target || event.srcElement;
                if (event.srcElement.nodeName.toLowerCase() == 'one-record-home-flexipage2' || event.srcElement.nodeName.toLowerCase() == 'records-lwc-detail-panel') {
                    // e = event.toElement;
                    // f = event.toElement;
                    // if ((event.toElement.closest('lightning-combobox') || event.toElement.closest('lightning-grouped-combobox')) && event.toElement.nodeName.toLowerCase() == 'input') {
                    //     e = event.toElement.closest('lightning-combobox') || event.toElement.closest('lightning-grouped-combobox');
                    //     f = event.toElement.closest('lightning-combobox') || event.toElement.closest('lightning-grouped-combobox');
                    // }
                    salesF = true
                }
                var parentele = 'null';
                // if (f != null && f.tagName.toLowerCase() == 'lightning-datatable') {
                //     temp2 = f.getElementsByTagName('table')[0];
                //     parentele = f;
                //     f = temp2;
                //     e = temp2;
                // }
                var className = e.className;
                var rpath = '';
                var cpath = '';
                var healedXpath = '';
                debugger;
                var firstpass = 0;
                var role = 'null';
                var svgTags = ['svg', 'circle', 'rect', 'ellipse', 'line', 'polygon', 'polyline', 'path', 'g', 'text', 'image', 'use'];
                if (e.hasAttribute('role')) {
                    if (e.getAttribute('role') === 'grid' && e.tagName.toLowerCase() === 'div') {
                        role = 'grid';
                    }
                }
                for (var path = ''; e &&(e.nodeName=='#document-fragment'|| e.nodeType == 1); e = e.assignedSlot||e.parentNode) {
                    if (e.nodeName=='#document-fragment')
                        e=e.host;
                    if (e.tagName.indexOf(':')!=-1) {
                        if (!(path[0]=='/' && path[1]=='/'))
                            path = '/' + path;
                    continue;
                    }
                    
                    var predicate = [];
                    var parentNode;
                    parentNode = e.parentNode;
                    if (parentNode.shadowRoot&&parentNode.shadowRoot.toString()=='[object ShadowRoot]'&&e.assignedSlot)
                        var siblings = e.assignedSlot.assignedNodes();
                    else
                        var siblings = parentNode.children;
                    var count = 0;
                    var xpathTag = ''
                    var unique = false;
                    var isSizeZero = false;
                    for (var i = 0; siblings && (i < siblings.length); i++) {
                        isSizeZero = isSizeZero||(siblings[i].getBoundingClientRect().height==0 && siblings[i].getBoundingClientRect().width==0);
                        if (siblings[i].tagName == e.tagName) {
                            count++;
                            if (siblings[i] == e) {
                                idx = count;
                            }
                        }
                    }
                    if (idx == 1 && count == 1) {
                        idx = null;
                    }
                    if (useId && e.id) {        
                        predicate[predicate.length] = '@id=' + '"' + e.id + '"';
                        unique = true;
                    }
                    xidx = (useIdx && idx) ? ('[' + idx + ']') : '';
                    idx = (useIdx && idx && !unique) ? ('[' + idx + ']') : '';
                    predicate = (predicate.length > 0) ? ('[' + predicate.join(' and ') + ']') : '';
                    if (svgTags.indexOf(e.tagName.toLowerCase()) !== -1) {
                        xpathTag = '*[local-name()="' + e.tagName.toLowerCase() + '"]';
                        path = '/*[local-name()="' + e.tagName.toLowerCase() + '"]' + xidx + path;
                    } else if (e.tagName.toLowerCase() === 'foreignobject') {
                        xpathTag = '*[local-name()="foreignObject"]';
                        path = '/*[local-name()="foreignObject"]' + xidx + path;
                    } else {
                        xpathTag = e.tagName.toLowerCase();
                        path = '/' + e.tagName.toLowerCase() + xidx + path;
                    }
                    if (healedXpath==''){
                        if (e.dynamicComponentType!=undefined){
                            if (cpath[0]!='/' || cpath[1]!='/')
                                cpath = '/' + cpath;
                        }
                        else if (isSizeZero)
                            cpath = '/' + xpathTag + cpath;
                        else
                            cpath = '/' + xpathTag + xidx + cpath;

                        var xres = document.evaluate('/'+cpath,document);
                        xres.iterateNext();
                        if (xres.iterateNext()==null)
                            healedXpath = '/'+cpath
                    }
                    if (firstpass == 0) {
                        if (unique && relative) {
                            rpath = '//*' + idx + predicate + rpath;
                            firstpass = 1;
                        } else if (salesF) {
                            rpath = '//' + e.tagName.toLowerCase() + idx + predicate + rpath;
                        } else {
                            if (svgTags.indexOf(e.tagName.toLowerCase()) !== -1) {
                                rpath = '/*[local-name()="' + e.tagName.toLowerCase() + '"]' + idx + predicate + rpath;
                            } else if (e.tagName.toLowerCase() === 'foreignobject') {
                                rpath = '/*[local-name()="foreignObject"]' + idx + predicate + rpath;
                            } else {
                                rpath = '/' + e.tagName.toLowerCase() + idx + predicate + rpath;
                            }
                        }
                    }
                }
                var firstpass1 = 0;
                var rpath1 = '';
                var cpath1 = '';
                if (parentele != 'null') {
                    g = parentele;
                    for (var path1 = ''; g && g.nodeType == 1; g = g.parentNode.host || g.parentNode) {
                        var predicate1 = [];
                        var siblings1 = g.parentNode.children;
                        var count1 = 0;
                        var unique1 = false;
                        isSizeZero = false;
                        for (var i = 0; siblings1 && (i < siblings1.length); i++) {
                            isSizeZero = isSizeZero||(siblings[i].getBoundingClientReact().height==0 && siblings[i].getBoundingClientReact().width==0);
                            if (siblings1[i].tagName == g.tagName) {
                                count1++;
                                if (siblings1[i] == g) {
                                    idx1 = count1;
                                }
                            }
                        }
                        if (idx1 == 1 && count1 == 1) {
                            idx1 = null;
                        }
                        if (useId && g.id) {
                            predicate1[predicate1.length] = '@id=' + '"' + g.id + '"';
                            unique1 = true;
                        }
                        xidx1 = (useIdx && idx1) ? ('[' + idx1 + ']') : '';
                        idx1 = (useIdx && idx1 && !unique1) ? ('[' + idx1 + ']') : '';
                        predicate1 = (predicate1.length > 0) ? ('[' + predicate1.join(' and ') + ']') : '';
                        if (svgTags.indexOf(g.tagName.toLowerCase()) !== -1) {
                            path1 = '/*[local-name()="' + g.tagName.toLowerCase() + '"]' + xidx1 + path1;
                        } else if (g.tagName.toLowerCase() == 'foreignobject') {
                            path1 = '/*[local-name()="foreignObject"]' + xidx1 + path1;
                        } else {
                            path1 = '/' + g.tagName.toLowerCase() + xidx1 + path1;
                            if (g.dynamicComponentType!=undefined)
                                if (c1path[0]!='/' || c1path[1]!='/'){
                                    cpath1 = '/' + cpath1;
                            }
                            else if (isSizeZero)
                                cpath1 = '/' + g.tagName.toLowerCase() + cpath1;
                            else
                                cpath1 = '/' + g.tagName.toLowerCase() + xidx1 + cpath1;
                        }
                        if (firstpass1 == 0) {
                            if (unique1 && relative) {
                                rpath1 = '//*' + idx1 + predicate1 + rpath1;
                                firstpass1 = 1;
                            } else {
                                if (svgTags.indexOf(g.tagName.toLowerCase()) !== -1) {
                                    rpath1 = '/*[local-name()="' + g.tagName.toLowerCase() + '"]' + idx1 + predicate1 + rpath1;
                                } else if (g.tagName.toLowerCase() == 'foreignobject') {
                                    rpath1 = '/*[local-name()="foreignObject"]' + idx1 + predicate1 + rpath1;
                                } else {
                                    rpath1 = '/' + g.tagName.toLowerCase() + idx1 + predicate1 + rpath1;
                                }
                            }
                        }
                    }
                    path = path1 + path;
                    cpath = cpath1 + cpath;
                    rpath = rpath1 + rpath;
                }
                ishidden = isVisible(f);
                if (ishidden == true || ishidden == 'True' || ishidden == 'true') {
                    ishidden = 'No';
                } else {
                    ishidden = 'Yes';
                }
                var tagname = f.tagName.toLowerCase();
                if (tagname.indexOf(':') != -1) {
                    tagname = tagname.replace(':', '');
                    tagname = 'custom' + tagname;
                }
                id = f.id;
                name = f.name;
                placeholder = f.placeholder;
                id = (String(id));
                name = (String(name));
                placeholder = (String(placeholder));
                var textvalue = text_content(f);
                textvalue = (String(textvalue));
                var label = text_content(f);
                label = (String(label));
                findCoordinates(f);
                if (name != '' && name != 'undefined') {
                    names = document.getElementsByName(name);
                    if (names.length > 1) {
                        for (var k = 0; k < names.length; k++) {
                            if (f == names[k]) {
                                ssname = name + '[' + k + ']'
                            }
                        }
                    } else {
                        ssname = name;
                    }
                }
                if (tagname != '' && tagname != 'undefined') {
                    tagnames = document.getElementsByTagName(tagname);
                    if (tagnames.length > 1) {
                        for (var k = 0; k < tagnames.length; k++) {
                            if (f == tagnames[k]) {
                                if (svgTags.indexOf(tagname) !== -1) {
                                    sstagname = '/*[local-name()="' + tagname + '"]' + '[' + k + ']';
                                } else if (tagname == 'foreignobject') {
                                    sstagname = '/*[local-name()="foreignObject"]' + '[' + k + ']';
                                } else {
                                    sstagname = tagname + '[' + k + ']';
                                }
                            }
                        }
                    } else {
                        if (svgTags.indexOf(tagname) !== -1) {
                            sstagname = '/*[local-name()="' + tagname + '"]';
                        } else if (tagname == 'foreignobject') {
                            sstagname = '/*[local-name()="foreignObject"]';
                        } else {
                            sstagname = tagname;
                        }
                    }
                }
                if (className != '' && className != 'undefined' && className != 'AvoAssure_Highlight') {
                    try {
                        classnames = document.getElementsByClassName(className);
                        if (classnames.length > 1) {
                            for (var k = 0; k < classnames.length; k++) {
                                if (f == classnames[k]) {
                                    ssclassname = className + '[' + k + ']'
                                }
                            }
                        } else {
                            ssclassname = className;
                        }
                    } catch (err) {
                        console.log("skipping this element: " + err);
                    }
                }
                if (tagname != 'script' && tagname != 'meta' && tagname != 'html' && tagname != 'head' && tagname != 'style' && tagname != 'body' && tagname != 'form' && tagname != 'link' && tagname != 'noscript' && tagname != '!' && tagname != 'pre' && tagname != 'code' && tagname != 'animatetransform' && tagname != 'noembed') {
                    if (textvalue == '' || textvalue == 'null' || textvalue == 'undefined' || textvalue == '0') {
                        if (name != '' && name != 'undefined') {
                            names = document.getElementsByName(name);
                            if (names.length > 1) {
                                for (var k = 0; k < names.length; k++) {
                                    if (f == names[k]) {
                                        textvalue = name + k;
                                    }
                                }
                            } else {
                                textvalue = name;
                            }
                        } else if (id != '' && id != 'undefined') {
                            textvalue = id;
                        } else if (placeholder != '' && placeholder != 'undefined') {
                            textvalue = placeholder;
                        } else {
                            var eles = document.getElementsByTagName(tagname);
                            for (var k = 0; k < eles.length; k++) {
                                if (f == eles[k]) {
                                    textvalue = tagname + '_NONAME' + (k + 1);
                                }
                            }
                        }
                    }
                    // capture label content of the element
                    function findLableForControl(ele) {
                        try {
                            var idVal = ele.id;
                            labels = document.getElementsByTagName('label');
                            if (labels.length !== 0) {
                                for( var i = 0; i < labels.length; i++ ) {
                                    if (labels[i].htmlFor == idVal) {
                                        return labels[i].textContent;
                                    }
                                }
                            }
                            else {
                                return null;
                            }
                        } catch (err) {
                            console.log("skipping this element: " + err);
                        }
                    }
                    if (label == '' || label == 'null' || label == 'undefined' || label == '0') {
                        if (placeholder != '' && placeholder != 'undefined') {
                            label = placeholder;
                        } else if (f.nodeName.toLowerCase() == 'input' || f.nodeName.toLowerCase() == 'select' || f.nodeName.toLowerCase() == 'textarea' || f.nodeName.toLowerCase() == 'progress' || f.nodeName.toLowerCase() == 'meter') {
                            label = findLableForControl(f);
                        }
                        if (f.nodeName.toLowerCase() == 'input' && (label == null || label == '')) {
                            if (f.hasAttribute('value')) {
                                label = f.getAttribute('value');
                            }
                            else {
                                label = null;
                            }
                        }
                    }
                    if (tagname == 'select') {
                        f.setAttribute('disabled', 'disabled');
                        multipleFlag = f.hasAttribute('multiple');
                    }
                    var etype = f.getAttribute('type');
                    etype = (String(etype)).toLowerCase();
                    var newPath = path;
                    if (tagname == 'textarea') {
                        tagname = 'input';
                        tagtype = 'txtarea';
                    } else if (tagname == 'select' && multipleFlag) {
                        tagname = 'list';
                        tagtype = 'lst';
                    } else if (tagname == 'select') {
                        tagtype = 'select';
                    } else if (tagname == 'lightning-combobox' || tagname == 'lightning-grouped-combobox') {
                        tagtype = tagname;
                        tagname = 'select';
                    } else if (tagname == 'td') {
                        tagname = 'tablecell';
                        tagtype = 'tblcell';
                    } else if (tagname == 'a') {
                        tagtype = 'lnk';
                    } else if (tagname == 'table') {
                        tagtype = 'tbl';
                    } else if (tagname == 'img') {
                        tagtype = 'img';
                    } else if (tagname == 'input' && etype == 'image') {
                        tagname = 'img';
                        tagtype = 'img';
                    }
                    if (tagname == 'input' && (etype == 'button' || etype == 'submit' || etype == 'reset' || etype == 'file')) {
                        tagname = 'button';
                        tagtype = 'btn';
                    } else if (tagname == 'input' && etype == 'radio') {
                        tagname = 'radiobutton';
                        tagtype = 'radiobtn';
                    } else if (tagname == 'input' && etype == 'checkbox') {
                        tagname = 'checkbox';
                        tagtype = 'chkbox';
                    } else if (tagname == 'input' && (etype == 'text' || etype == 'email' || etype == 'number' || etype == 'password' || etype == 'range' || etype == 'search' || etype == 'url')) {
                        tagname = 'input';
                        tagtype = 'txtbox';
                    } else if (tagname == 'input' && tagtype == '' && (etype == 'hidden' || etype == 'null')) {
                        tagname = 'div';
                        tagtype = 'elmnt';
                    } else if (tagname == 'option' && f.parentNode.hasAttribute('multiple')) {
                        tagname = 'list';
                        var selectIndex1 = rpath.indexOf('select');
                        var selectIndex2 = path.indexOf('select');
                        rpath = rpath.substring(0, selectIndex1 + 6);
                        path = path.substring(0, selectIndex2 + 6);
                    } else if (tagname == 'button') {
                        tagname = 'button';
                        tagtype = 'btn';
                    }
                    if (role == 'grid') {
                        tagname = 'grid';
                        tagtype = 'grid';
                    }
                    if (id == '') {
                        id = 'null';
                    }
                    if (salesF) {
                        textvalue = tagname + '_Salesforce' + salesforcecounter + '_sfc';
                        salesforcecounter = salesforcecounter + 1;
                    }
                    textvalue = textvalue.replace(">", "");
                    textvalue = textvalue.replace("</", "");
                    textvalue = textvalue.replace("<", "");
                    textvalue = textvalue.replace("/>", "");
                    textvalue = textvalue.split("\\n").join("");
                    textvalue = textvalue.split("\\t").join("");
                    textvalue = textvalue.split("\\r").join("");
                    textvalue = textvalue.split("  ").join("");
                    textvalue = textvalue.split("\\u00a0").join("");
                    if (textvalue == '' || textvalue.length == 0 || textvalue == '0') {
                        textvalue = 'NONAME' + nonamecounter;
                        nonamecounter = nonamecounter + 1;
                        custname = textvalue;
                    } else {
                        custname = textvalue;
                    }
                    if (tagtype != '') {
                        custname = custname + '_' + tagtype;
                    } else {
                        custname = custname + '_elmnt';
                    }
                    if (tagname == 'select') {
                        f.removeAttribute('disabled');
                        f.setAttribute('enabled', 'enabled');
                    } else if (tagname == "list") {
                        f.removeAttribute('disabled');
                        f.setAttribute('enabled', 'enabled');
                    }
                    coordinates = left + ';' + top + ';' + height + ';' + width;
                    coordinates = String(coordinates);
                    if (browser == 3) {
                        if (svgTags.indexOf(tagname) === -1) {
                            ssclassname = ssclassname.replace(/AvoAssure_Highlight/g, '');
                            ssclassname = ssclassname.replace(/AvoAssureBorderHighlight/g, '');
                            ssclassname = ssclassname.trim();
                        } else {
                            ssclassname.animVal = ssclassname.animVal.replace(/AvoAssure_Highlight/g, '');
                            ssclassname.baseVal = ssclassname.baseVal.replace(/AvoAssure_Highlight/g, '');
                            ssclassname.animVal = ssclassname.animVal.replace(/AvoAssureBorderHighlight/g, '');
                            ssclassname.baseVal = ssclassname.baseVal.replace(/AvoAssureBorderHighlight/g, '');
                            ssclassname.animVal = ssclassname.animVal.trim();
                            ssclassname.baseVal = ssclassname.baseVal.trim();
                        }
                    } else {
                        if (svgTags.indexOf(tagname) === -1) {
                            ssclassname = ssclassname.replaceAll('AvoAssure_Highlight', '');
                            ssclassname = ssclassname.replaceAll('AvoAssureBorderHighlight', '');
                            ssclassname = ssclassname.trim();
                        } else {
                            ssclassname.animVal = ssclassname.animVal.replaceAll('AvoAssure_Highlight', '');
                            ssclassname.baseVal = ssclassname.baseVal.replaceAll('AvoAssure_Highlight', '');
                            ssclassname.animVal = ssclassname.animVal.replaceAll('AvoAssureBorderHighlight', '');
                            ssclassname.baseVal = ssclassname.baseVal.replaceAll('AvoAssureBorderHighlight', '');
                            ssclassname.animVal = ssclassname.animVal.trim();
                            ssclassname.baseVal = ssclassname.baseVal.trim();
                        }
                    }

                    // capture css selector of the element
                    var cssSelector = '';
                    function getElementCount(ele, tag) {
                        try {
                            let tagIndex = '';
                            let arr = Array.from(ele.parentNode.children);
                            let tagNameArr = [];
                            for (i = 0; i < arr.length; i++) {
                                let tag = arr[i].tagName.toLowerCase();
                                tagNameArr.push(tag);
                            }
                            let count = tagNameArr.toString().match(new RegExp(tag, 'g')).length;
                            if (count > 1) {
                                let sib = ele.previousSibling, nth = 1;
                                while((sib != null) && nth++) {
                                    if ((sib.nodeName.toLowerCase() == '#text') || (sib.nodeName.toLowerCase() == '#comment')) {
                                        nth--;
                                    }
                                    sib = sib.previousSibling;
                                }
                                tagIndex = ":nth-child("+nth+")";
                            }
                            return tagIndex;
                        } catch (err) {
                            console.log(err);
                        }
                    }
                    function getAttr(ele) {
                        try {
                            let arr = ['id','class','name','value','placeholder','title', 'href'];
                            let nodes=[], values=[];
                            for (var att, i = 0, atts = ele.attributes, n = atts.length; i < n; i++){
                                att = atts[i];
                                if (arr.includes(att.nodeName)) {
                                    nodes.push(att.nodeName);
                                    values.push(att.nodeValue);
                                }
                            }
                            return [nodes, values];
                        } catch (err) {
                            console.log(err);
                        }
                    }
                    function getCssSelector(ele) {
                        try {
                            let selector = parentSelector = childSelector = '';
                            let parentFlag = false;
                            let tag = ele.nodeName.toLowerCase();
                            if (ele != null && ele.attributes.length) {
                                let [nodes, values] = getAttr(ele);
                                for (let index=0; index < nodes.length; index++) {
                                    if (values[index] != '' && !(values[index].includes('AvoAssure'))) {
                                        let elementCount = '';
                                        if (nodes[index] == 'class') {
                                            elementCount = document.querySelectorAll(`${tag}[${nodes[index]}="${values[index]}"]`).length + document.querySelectorAll(`${tag}[${nodes[index]}="${values[index]} AvoAssure_Highlight"]`).length;
                                        }
                                        else {
                                            elementCount = document.querySelectorAll(`${tag}[${nodes[index]}="${values[index]}"]`).length;
                                        }
                                        if (elementCount == 1) {
                                            selector = `${tag}[${nodes[index]}="${values[index]}"]`;
                                            break;
                                        }
                                    }
                                }
                                if (selector == '' && !parentFlag && nodes.length != 0 && values.slice(-1) != '' && !(values.slice(-1)[0].includes('AvoAssure'))) {
                                    childSelector = `${tag}[${nodes.slice(-1)}="${values.slice(-1)}"]`;
                                    parentFlag = true;
                                }
                                else if (selector == '' && nodes.length != 0 && (values.slice(-1) == '' || !(values.slice(-1)[0].includes('AvoAssure')))) {
                                    if (childSelector == '' && nodes.length > 1 && nodes.slice(-1) == 'class') {
                                        childSelector = `${tag}[${nodes[nodes.length-2]}="${values[values.length-2]}"]`;
                                        parentFlag = true;
                                    }
                                    else {
                                        let tagIndex = getElementCount(ele, tag);
                                        if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                                            selector = `${tag}${tagIndex}`;
                                        }
                                        else {
                                            childSelector = `${tag}${tagIndex}`;
                                            parentFlag = true;
                                        }
                                    }
                                }
                                else if (selector == '' && childSelector == '') {
                                    let tagIndex = getElementCount(ele, tag);
                                    if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                                        selector = `${tag}${tagIndex}`;
                                    }
                                    else {
                                        childSelector = tag;
                                        parentFlag = true;
                                    }
                                }
                            }
                            else {
                                let tagIndex = getElementCount(ele, tag);
                                if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                                    selector = `${tag}${tagIndex}`;
                                }
                                else {
                                    childSelector = `${tag}${tagIndex}`;
                                    parentFlag = true;
                                }
                            }
                            if (parentFlag) {
                                let parentEle = ele.parentNode;
                                while (parentFlag && parentEle.nodeName.toLowerCase() != 'body') {
                                    let parentTag = parentEle.nodeName.toLowerCase();
                                    if (parentEle != null && parentEle.attributes.length) {
                                        let [parentNodes, parentValues] = getAttr(parentEle);
                                        for (let index=0; index < parentNodes.length; index++) {
                                            if (parentValues[index] != '') {
                                                if (document.querySelectorAll(`${parentTag}[${parentNodes[index]}="${parentValues[index]}"] ${childSelector}`).length == 1) {
                                                    parentSelector = `${parentTag}[${parentNodes[index]}="${parentValues[index]}"]`;
                                                    selector = `${parentSelector} ${childSelector}`;
                                                    parentFlag = false;
                                                    break;
                                                }
                                            }
                                        }
                                        if (selector == '') {
                                            if (document.querySelectorAll(`${parentTag} ${childSelector}`).length == 1) {
                                                selector = `${parentTag} ${childSelector}`;
                                                parentFlag = false;
                                            }
                                            else if (document.querySelectorAll(`${parentTag} ${childSelector}`).length > 1) {
                                                let tagIndex = getElementCount(parentEle, parentTag);
                                                if (document.querySelectorAll(`${parentTag}${tagIndex} ${childSelector}`).length == 1) {
                                                    selector = `${parentTag}${tagIndex} ${childSelector}`;
                                                    parentFlag = false;
                                                }
                                                else {
                                                    parentEle = parentEle.parentNode;
                                                }
                                            }
                                            else {
                                                parentEle = parentEle.parentNode;
                                            }
                                        }
                                        else {
                                            parentFlag = false;
                                        }
                                    }
                                    else {
                                        let tagIndex = getElementCount(parentEle, parentTag);
                                        if (document.querySelectorAll(`${parentTag}${tagIndex} ${childSelector}`).length == 1) {
                                            selector = `${parentTag}${tagIndex} ${childSelector}`;
                                            parentFlag = false;
                                        }
                                        else {
                                            parentEle = parentEle.parentNode;
                                        }
                                    }
                                }
                            }
                            return selector;
                        } catch (err) {
                            console.log("ERROR in get getCssSelector(): " + err);
                        }
                    }
                    cssSelector = getCssSelector(f);

                    // capture href of the element
                    var href='';
                    function getHref(ele) {
                        try {
                            var hrefValue='';
                            if (ele.hasAttribute('href')) {
                                hrefValue = ele.getAttribute('href');
                            }
                            else {
                                hrefValue = null;
                            }
                            return hrefValue;
                        } catch (err) {
                            console.log("skipping this element: " + err);
                        }
                    }
                    href = getHref(f);

                    //We will be using absolute xpath first as relative xpath has id that may change and incorrect element may get selected.
                    debugger;
                    newPath = String(path) + ';' + String(id) + ';' + String(healedXpath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + label + ';' + String(href) + ';' + cssSelector;
                    for (var i = 0; i < arr.length; i++) {
                        if (arr[i].xpath == newPath) {
                            uniqueFlag = true;
                            break;
                        }
                    };
                    if (uniqueFlag == false) {
                        arr.push({
                            'xpath': newPath,
                            'url': url,
                            'hiddentag': ishidden,
                            'custname': custname,
                            'tag': tagname,
                            'top': top,
                            'left': left,
                            'height': height,
                            'width': width,
                            'viewTop': viewTop,
                        });
                    }
                    uniqueFlag = false;
                    if (browser == '3') {
                        f.setAttribute('class', className + ' AvoAssure_Highlight');
                        f.setAttribute('className', className + ' AvoAssure_Highlight');
                        f.style.setAttribute('cssText', 'background: #fff300 !important;opacity:1!important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;');
                    } else {
                        var styleElement = 'background: #fff300 !important;opacity:1!important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;'
                        if ((f.hasAttribute('style') && f.getAttribute('style').indexOf(styleElement)==-1)||!f.hasAttribute('style'))
                        {
                            f.setAttribute('class', className + ' AvoAssure_Highlight');
                            if (f.hasAttribute('style'))
                                styleElement += f.getAttribute('style');    //Taking care of existing css on element
                            f.setAttribute('style', styleElement);          
                        }
                    }
                    //Using CSS to make pointer events auto after highlighting.
                    //if (browser!='2' && currentElement.tagName!='HTML')   //Excluding the changes for firefox
                    //    document.getElementsByTagName('html')[0].style.pointerEvents='auto';
                }
                return false;
            }
        }
        function block_handler(event) {
            event = event || window.event;
            if (event.type=="mousedown")
                currentElement = event.toElement;
            if (event.ctrlKey) {
                return true;
            }
            //Using CSS to make pointer events none as event.preventDefault can't cancel sometimes.
            //if (browser!='2' && currentElement.tagName!='HTML'  && currentElement._scopedScroll==undefined)   //Excluding the changes for firefox and for scrollbar
             //   document.getElementsByTagName('html')[0].style.pointerEvents='none';
            if (event.preventDefault) {
                event.preventDefault();
                event.stopPropagation();
                event.cancelBubble = true;
                event.returnValue = false;
            } else {
                window.event.cancelBubble = true;
                window.event.returnValue = false;
            }
            return false;
        }
        click(ae, isIE, be);
        function click(ae, isIE, be) {
            if (isIE) {
                for (var i = 0; i < ae.length; i++) {
                    if ((ae[i].getAttribute("onclick")) != null) {
                        var onclickval = ae[i].attributes["onclick"].value;
                        be[i] = ae[i].cloneNode(true);
                        ae[i].onclick = null;
                        ae[i].setAttribute('_onclick', onclickval);
                    }
                    if (ae[i].addEventListener) {
                        ae[i].addEventListener('click', handler, true);
                        ae[i].addEventListener('mouseover', hov_handler, true);
                        ae[i].addEventListener('mouseleave', leave_handler, true);
                        ae[i].addEventListener('mousedown', block_handler, true);
                        ae[i].addEventListener('mouseup', block_handler, true);
                    } else if (ae[i].attachEvent) {
                        ae[i].attachEvent('onclick', handler);
                        ae[i].attachEvent('onmouseover', hov_handler);
                        ae[i].attachEvent('onmouseleave', leave_handler);
                        ae[i].attachEvent('onmousedown', block_handler);
                        ae[i].attachEvent('onmouseup', block_handler);
                    }
                }
            } else {
                for (var i = 0; i < ae.length; i++) {
                    if ((ae[i].getAttribute("onclick")) != null) {
                        var onclickval = ae[i].getAttribute("onclick");
                        ae[i].removeAttribute("onclick");
                        ae[i].setAttribute("_onclick", onclickval);
                    }
                    if (ae[i].addEventListener) {
                        ae[i].addEventListener('click', handler, true);
                        ae[i].addEventListener('mouseover', hov_handler, true);
                        ae[i].addEventListener('mouseleave', leave_handler, true);
                        ae[i].addEventListener('mousedown', block_handler, true);
                        ae[i].addEventListener('mouseup', block_handler, true);
                    } else if (ae[i].attachEvent) {
                        ae[i].attachEvent('onclick', handler);
                        ae[i].attachEvent('onmouseover', hov_handler);
                        ae[i].attachEvent('onmouseleave', leave_handler);
                        ae[i].attachEvent('onmousedown', block_handler);
                        ae[i].attachEvent('onmouseup', block_handler);
                    }
                }
            }
        }

        function findCoordinates(element) {
            height = element.offsetHeight || 0;
            width = element.offsetWidth || 0;
            viewTop = element.getBoundingClientRect()['top'];
            top = 0;
            left = 0;
            do {
                top += element.offsetTop || 0;
                left += element.offsetLeft || 0;
                element = element.offsetParent;
            } while (element);
        };

        function text_content(f) {
            var firstText = '';
            var textdisplay = '';
            for (var z = 0; z < f.childNodes.length; z++) {
                var curNode = f.childNodes[z];
                whitespace = /^\s*$/;
                if (curNode.nodeName === '#text' && !(whitespace.test(curNode.nodeValue))) {
                    firstText = curNode.nodeValue;
                    textdisplay = textdisplay + firstText;
                }
            }
            return (textdisplay);
        };

        function addNodesOuter(array, collection) {
            for (var i = 0; collection && collection.length && i < collection.length; i++) {
                    array.push(collection[i]);
            }
        };"""
    """Javascript logic used in stop click and add operation in IE"""
    javascript_stopclicknadd_IE = """window.tastopflag = "true";document.getElementsByTagName('HTML')[0].click();function getElementsByClassName(classname) {    var a = [];    var re = new RegExp('(^| )' + classname + '( |$)');    var els = document.getElementsByTagName("*");    var elesal = document.getElementsByTagName("one-record-home-flexipage2");    var elesal1 = document.getElementsByTagName("records-lwc-detail-panel");    for (var i = 0, j = els.length; i < j; i++)        if (re.test(els[i].className)) a.push(els[i]);    if (elesal.length > 0) {        els1 = elesal[0].getElementsByTagName("*");        for (var i = 0, j = els1.length; i < j; i++) {            if (re.test(els1[i].className)) {                a.push(els1[i]);            }        }    }    if (elesal1.length > 0) {        els2 = elesal1[0].getElementsByTagName("*");        for (var i = 0, j = els2.length; i < j; i++) {            if (re.test(els2[i].className)) {                a.push(els2[i]);            }        }    }    return a;}if (document.getElementById('AvoAssureCheckboxHighlight') || document.getElementById('AvoAssureBorderHighlight')) {    styleTag = document.getElementById('AvoAssureCheckboxHighlight');    styleTagH = document.getElementById('AvoAssureBorderHighlight');    head = document.head || document.getElementsByTagName('head')[0] || document.getElementById('AvoAssure_head');    head.removeChild(styleTag);    head.removeChild(styleTagH);    var a = getElementsByClassName('AvoAssure_Highlight');    for (var i = 0; i < a.length; i++) {        a[i].removeAttribute('style');    }    var elms = document.querySelectorAll("*[style]");    Array.prototype.forEach.call(elms, function(elm) {        var clr = elm.style.background || "";        clr = clr.replace(/\s/g, "").toLowerCase();        if (clr === '#fff300' || clr === 'rgb(255,243,0)' || clr === 'rgb(255,243,0)nonerepeatscroll0%0%') {            elm.removeAttribute('style');        }    });    if (document.getElementById('AvoAssure_head') != undefined) {        var html = document.children[0];        if (html.childElementCount > 1) html.removeChild(html.children[1]);    }    var b = getElementsByClassName('AvoAssureBorderHighlight');    var c = getElementsByClassName('AvoAssureCheckboxHighlight');    var className = "AvoAssure_Highlight";    var classNameB = "AvoAssureBorderHighlight";    var classNameC = "AvoAssureCheckboxHighlight";    for (var i = 0; i < a.length; i++) {        if (a[i].classList) {            a[i].classList.remove(className);        } else if (hasClass(a[i], className)) {            var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');            a[i].className = a[i].className.replace(reg, ' ');        }    }    for (var i = 0; i < b.length; i++) {        if (b[i].classList) {            b[i].classList.remove(classNameB);        } else if (hasClass(b[i], classNameB)) {            var reg = new RegExp('(\\s|^)' + classNameB + '(\\s|$)');            b[i].className = b[i].className.replace(reg, ' ');        }    }    for (var i = 0; i < c.length; i++) {        if (c[i].classList) {            c[i].classList.remove(classNameC);        } else if (hasClass(c[i], classNameC)) {            var reg = new RegExp('(\\s|^)' + classNameC + '(\\s|$)');            c[i].className = c[i].className.replace(reg, ' ');        }    }}var temp = window.tasarr;window.tasarr = null;return (temp);"""

    """Javascript logic used in stop click and add operation"""
    javascript_stopclicknadd = """
    debugger;
    window.tastopflag = "true";
    document.getElementsByTagName('HTML')[0].click();
    //If HTML element doesnt receive click, clicking the first scraped element to trigger handler of start click and add to get all scraped elements.
    if (window.tasarr!=undefined && window.tasarr.length==0 && document.getElementsByClassName('AvoAssure_Highlight').length)
        document.getElementsByClassName('AvoAssure_Highlight')[0].click();
    var elements=[];
    function addNodesOuter(elements, collection) {
        for (var i = 0; collection && collection.length && i < collection.length; i++) {
                elements.push(collection[i]);
        }
    };
    ele = document.getElementsByTagName('*');
    for (var i=0;i<ele.length;i++)
    {
        elements.push(ele[i]);
        if (ele[i].shadowRoot)
            addNodesOuter(elements, ele[i].getElementsByTagName('*'));
    }

    function getElementsByClassName(classname) {
        var a = [];
        
        for ( i = 0, j = elements.length; i < j; i++) {
            if (Object.values(elements[i].classList).includes(classname)) {
                a.push(elements[i]);
            }
        }
        return a;
    }
    if (document.getElementById('AvoAssure_Table'))
        document.getElementById('AvoAssure_Table').remove()
    if (document.getElementById('AvoAssureCheckboxHighlight') || document.getElementById('AvoAssureBorderHighlight')) {
        styleTag = document.getElementById('AvoAssureCheckboxHighlight');
        styleTagH = document.getElementById('AvoAssureBorderHighlight');
        head = document.head || document.getElementsByTagName('head')[0] || document.getElementById('AvoAssure_head');
        head.removeChild(styleTag);
        head.removeChild(styleTagH);
        var a = getElementsByClassName('AvoAssure_Highlight');
        for (var i = 0; i < a.length; i++) {
            a[i].setAttribute('style',a[i].getAttribute('style').replace('background: #fff300 !important;opacity:1!important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;',''));
        }
        var elms = document.querySelectorAll("*[style]");
        Array.prototype.forEach.call(elms, function(elm) {
            var clr = elm.style.background || "";
            clr = clr.replace(/\s/g, "").toLowerCase();
            if (clr === '#fff300' || clr === 'rgb(255,243,0)' || clr === 'rgb(255,243,0)nonerepeatscroll0%0%') {
                elm.removeAttribute('style');
            }
        });
        if (document.getElementById('AvoAssure_head') != undefined) {
            var html = document.children[0];
            if (html.childElementCount > 1) html.removeChild(html.children[1]);
        }
        var b = getElementsByClassName('AvoAssureBorderHighlight');
        var c = getElementsByClassName('AvoAssureCheckboxHighlight');
        var className = "AvoAssure_Highlight";
        var classNameB = "AvoAssureBorderHighlight";
        var classNameC = "AvoAssureCheckboxHighlight";
        for (var i = 0; i < a.length; i++) {
            if (a[i].classList) {
                a[i].classList.remove(className);
            } else if (hasClass(a[i], className)) {
                var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
                a[i].className = a[i].className.replace(reg, ' ');
            }
        }
        for (var i = 0; i < b.length; i++) {
            if (b[i].classList) {
                b[i].classList.remove(classNameB);
            } else if (hasClass(b[i], classNameB)) {
                var reg = new RegExp('(\\s|^)' + classNameB + '(\\s|$)');
                b[i].className = b[i].className.replace(reg, ' ');
            }
        }
        for (var i = 0; i < c.length; i++) {
            if (c[i].classList) {
                c[i].classList.remove(classNameC);
            } else if (hasClass(c[i], classNameC)) {
                var reg = new RegExp('(\\s|^)' + classNameC + '(\\s|$)');
                c[i].className = c[i].className.replace(reg, ' ');
            }
        }
    }
    var temp = window.tasarr;
    window.tasarr = null;
    return (temp);"""

    javascript_get_object_properties = """
    if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {
    (function () {
        function hasAttribute(attrName) {
            return typeof this[attrName] !== 'undefined';
        }
        var inputs = document.getElementsByTagName('*');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].hasAttribute = hasAttribute;
        }
    }());
    }
    if (!window.Element || !window.Element.prototype || !window.Element.prototype.getAttribute) {
        (function () {
            function getAttribute(attrName) {
                return typeof this[attrName] !== 'undefined';
            }
            var inputs = document.getElementsByTagName('*');
            for (var i = 0; i < inputs.length; i++) {
                inputs[i].getAttribute = getAttribute;
            }
        }());
    }(function () {
        if (!document.getElementsByClassName) {
            var indexOf = [].indexOf || function (prop) {
                for (var i = 0; i < this.length; i++) {
                    if (this[i] === prop) return i;
                }
                return -1;
            };
            getElementsByClassName = function (className, context) {
                var elems = document.querySelectorAll ? context.querySelectorAll("." + className) : (function () {
                    var all = context.getElementsByTagName("*"),
                        elements = [],
                        i = 0;
                    for (; i < all.length; i++) {
                        if (all[i].className && (" " + all[i].className + " ").indexOf(" " + className + " ") > -1 && indexOf.call(elements, all[i]) === -1) elements.push(all[i]);
                    }
                    return elements;
                })();
                return elems;
            };
            document.getElementsByClassName = function (className) {
                return getElementsByClassName(className, document);
            };
            if (window.Element) {
                window.Element.prototype.getElementsByClassName = function (className) {
                    return getElementsByClassName(className, this);
                };
            }
        }
    })();
    var suseIdx = true;
    var suseId = true;
    var suseClass = true;
    var srelative = true;
    var sae = [];
    var sarr = [];
    var sele = document.getElementsByTagName('*');
    var smyid = 0;
    var stextvalue = '';
    var slabel = '';
    var stagname = 0;
    var sishidden = 0;
    var scustname = '';
    var smultipleFlag = false;
    var element = arguments[0];
    console.log(element);
    var surl = arguments[1];
    var snonamecounter = 1;
    var txt_area_nonamecounter = 1;
    var select_nonamecounter = 1;
    var td_nonamecounter = 1;
    var a_nonamecounter = 1;
    var table_nonamecounter = 1;
    var input_nonamecounter = 1;
    var stagtype = '';
    var ssname = 'null';
    var sstagname = 'null';
    var ssclassname = 'null';
    var sclassname = 'null';
    var top = 0;
    var left = 0;
    var height = 0;
    var width = 0;
    var coordinates = '';
    var sisVisible = (function () {
        function inside(schild, sparent) {
            while (schild) {
                if (schild === sparent) return true;
                schild = schild.parentNode;
            }
            return false;
        };
        return function (selem) {
            if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;
            var srect = selem.getBoundingClientRect();
            if (window.getComputedStyle || selem.currentStyle) {
                var sel = selem,
                    scomp = null;
                while (sel) {
                    if (sel === document) {
                        break;
                    } else if (!sel.parentNode) return false;
                    scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;
                    if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;
                    sel = sel.parentNode;
                }
            }
            return true;
        }
    })();

    function getElementProperties(element) {
        stagtype = '';
        ssname = 'null';
        sstagname = 'null';
        sid = element.id;
        sname = element.name;
        salttext = element.alt;
        splaceholder = element.placeholder;
        sclassname = element.className;
        sid = (String(sid));
        sclassname = (String(sclassname));
        sname = (String(sname));
        splaceholder = (String(splaceholder));
        stextvalue = stext_content(element);
        stextvalue = (String(stextvalue));
        var slabel = stext_content(element);
        slabel = (String(slabel));
        stagname = element.tagName.toLowerCase();
        ssname = 'null';
        sstagname = 'null';
        ssclassname = 'null';
        var role = 'null';
        if (element.hasAttribute('role')) {
            if (element.getAttribute('role') === 'grid' && element.tagName.toLowerCase() === 'div') {
                role = 'grid';
            }
        }
        findCoordinates(element);
        if (stagname.indexOf(':') != -1) {
            stagname = stagname.replace(':', '');
            stagname = 'custom' + stagname;
        }
        if (sname != '' && sname != 'undefined') {
            snames = document.getElementsByName(sname);
            if (snames.length > 1) {
                for (var k = 0; k < snames.length; k++) {
                    if (element == snames[k]) {
                        ssname = sname + '[' + k + ']'
                    }
                }
            } else {
                ssname = sname;
            }
        }
        if (stagname != '' && stagname != 'undefined') {
            stagnames = document.getElementsByTagName(stagname);
            if (stagnames.length > 1) {
                for (var k = 0; k < stagnames.length; k++) {
                    if (element == stagnames[k]) {
                        sstagname = stagname + '[' + k + ']'
                    }
                }
            } else {
                sstagname = stagname;
            }
        }
        if (sclassname != '' && sclassname != 'undefined') {
            try {
                sclassnames = document.getElementsByClassName(sclassname);
                if (sclassnames.length > 1) {
                    for (var k = 0; k < sclassnames.length; k++) {
                        if (element == sclassnames[k]) {
                            ssclassname = sclassname + '[' + k + ']'
                        }
                    }
                } else {
                    ssclassname = sclassname;
                }
            } catch (err) {
                console.log(sclassname);
                console.log("skipping this element: " + err);
            }
        }
        if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') {
            if (stextvalue == '' || stextvalue == 'null' || stextvalue == 'undefined' || stextvalue == '0') {
                if (sname != '' && sname != 'undefined') {
                    snames = document.getElementsByName(sname);
                    if (snames.length > 1) {
                        for (var k = 0; k < snames.length; k++) {
                            if (element == snames[k]) {
                                stextvalue = sname + k;
                            }
                        }
                    } else {
                        stextvalue = sname;
                    }
                } else if (sid != '' && sid != 'undefined') {
                    stextvalue = sid;
                } else if (splaceholder != '' && splaceholder != 'undefined') {
                    stextvalue = splaceholder;
                } else {
                    var seles = document.getElementsByTagName(stagname);
                    for (var k = 0; k < seles.length; k++) {
                        if (element == seles[k]) {
                            stextvalue = stagname + '_NONAME' + (k + 1);
                        }
                    }
                }
            }
            // capture label content of the element
            function findLableForControl(ele) {
                try {
                    var idVal = ele.id;
                    labels = document.getElementsByTagName('label');
                    if (labels.length !== 0) {
                        for( var i = 0; i < labels.length; i++ ) {
                            if (labels[i].htmlFor == idVal) {
                                return labels[i].textContent;
                            }
                        }
                    }
                    else {
                        return null;
                    }
                } catch (err) {
                    console.log("skipping this element: " + err);
                }
            }
            if (slabel == '' || slabel == 'null' || slabel == 'undefined' || slabel == '0') {
                if (splaceholder != '' && splaceholder != 'undefined') {
                    slabel = splaceholder;
                } else if (element.nodeName.toLowerCase() == 'input' || element.nodeName.toLowerCase() == 'select' || element.nodeName.toLowerCase() == 'textarea' || element.nodeName.toLowerCase() == 'progress' || element.nodeName.toLowerCase() == 'meter') {
                    slabel = findLableForControl(element);
                }
                if (element.nodeName.toLowerCase() == 'input' && (slabel == null || slabel == '')) {
                    if (element.hasAttribute('value')) {
                        slabel = element.getAttribute('value');
                    }
                    else {
                        slabel = null;
                    }
                }
            }

            // capture css selector of the element
            var sCssSelector = '';
            function getElementCount(ele, tag) {
                try {
                    let tagIndex = '';
                    let arr = Array.from(ele.parentNode.children);
                    let tagNameArr = [];
                    for (i = 0; i < arr.length; i++) {
                        let tag = arr[i].tagName.toLowerCase();
                        tagNameArr.push(tag);
                    }
                    let count = tagNameArr.toString().match(new RegExp(tag, 'g')).length;
                    if (count > 1) {
                        let sib = ele.previousSibling, nth = 1;
                        while((sib != null) && nth++) {
                            if ((sib.nodeName.toLowerCase() == '#text') || (sib.nodeName.toLowerCase() == '#comment')) {
                                nth--;
                            }
                            sib = sib.previousSibling;
                        }
                        tagIndex = ":nth-child("+nth+")";
                    }
                    return tagIndex;
                } catch (err) {
                    console.log(err);
                }
            }
            function getAttr(ele) {
                try {
                    let arr = ['id','class','name','value','placeholder','title', 'href'];
                    let nodes=[], values=[];
                    for (var att, i = 0, atts = ele.attributes, n = atts.length; i < n; i++){
                        att = atts[i];
                        if (arr.includes(att.nodeName)) {
                            nodes.push(att.nodeName);
                            values.push(att.nodeValue);
                        }
                    }
                    return [nodes, values];
                } catch (err) {
                    console.log(err);
                }
            }
            function getCssSelector(ele) {
                try {
                    let selector = parentSelector = childSelector = '';
                    let parentFlag = false;
                    let tag = ele.nodeName.toLowerCase();
                    if (ele != null && ele.attributes.length) {
                        let [nodes, values] = getAttr(ele);
                        for (let index=0; index < nodes.length; index++) {
                            if (values[index] != '') {
                                if (document.querySelectorAll(`${tag}[${nodes[index]}="${values[index]}"]`).length == 1) {
                                    selector = `${tag}[${nodes[index]}="${values[index]}"]`;
                                    break;
                                }
                            }
                        }
                        if (selector == '' && !parentFlag && nodes.length != 0 && values.slice(-1) != '') {
                            childSelector = `${tag}[${nodes.slice(-1)}="${values.slice(-1)}"]`;
                            parentFlag = true;
                        }
                        else if (selector == '' && nodes.length != 0 && values.slice(-1) == '') {
                            if (childSelector == '' && nodes.length > 1 && nodes.slice(-1) == 'class') {
                                childSelector = `${tag}[${nodes[nodes.length-2]}="${values[values.length-2]}"]`;
                                parentFlag = true;
                            }
                            else {
                                let tagIndex = getElementCount(ele, tag);
                                if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                                    selector = `${tag}${tagIndex}`;
                                }
                                else {
                                    childSelector = `${tag}${tagIndex}`;
                                    parentFlag = true;
                                }
                            }
                        }
                        else if (selector == '' && childSelector == '') {
                            let tagIndex = getElementCount(ele, tag);
                            if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                                selector = `${tag}${tagIndex}`;
                            }
                            else {
                                childSelector = tag;
                                parentFlag = true;
                            }
                        }
                    }
                    else {
                        let tagIndex = getElementCount(ele, tag);
                        if (document.querySelectorAll(`${tag}${tagIndex}`).length == 1) {
                            selector = `${tag}${tagIndex}`;
                        }
                        else {
                            childSelector = `${tag}${tagIndex}`;
                            parentFlag = true;
                        }
                    }
                    if (parentFlag) {
                        let parentEle = ele.parentNode;
                        while (parentFlag && parentEle.nodeName.toLowerCase() != 'body') {
                            let parentTag = parentEle.nodeName.toLowerCase();
                            if (parentEle != null && parentEle.attributes.length) {
                                let [parentNodes, parentValues] = getAttr(parentEle);
                                for (let index=0; index < parentNodes.length; index++) {
                                    if (parentValues[index] != '') {
                                        if (document.querySelectorAll(`${parentTag}[${parentNodes[index]}="${parentValues[index]}"] ${childSelector}`).length == 1) {
                                            parentSelector = `${parentTag}[${parentNodes[index]}="${parentValues[index]}"]`;
                                            selector = `${parentSelector} ${childSelector}`;
                                            parentFlag = false;
                                            break;
                                        }
                                    }
                                }
                                if (selector == '') {
                                    if (document.querySelectorAll(`${parentTag} ${childSelector}`).length == 1) {
                                        selector = `${parentTag} ${childSelector}`;
                                        parentFlag = false;
                                    }
                                    else if (document.querySelectorAll(`${parentTag} ${childSelector}`).length > 1) {
                                        let tagIndex = getElementCount(parentEle, parentTag);
                                        if (document.querySelectorAll(`${parentTag}${tagIndex} ${childSelector}`).length == 1) {
                                            selector = `${parentTag}${tagIndex} ${childSelector}`;
                                            parentFlag = false;
                                        }
                                        else {
                                            parentEle = parentEle.parentNode;
                                        }
                                    }
                                    else {
                                        parentEle = parentEle.parentNode;
                                    }
                                }
                                else {
                                    parentFlag = false;
                                }
                            }
                            else {
                                let tagIndex = getElementCount(parentEle, parentTag);
                                if (document.querySelectorAll(`${parentTag}${tagIndex} ${childSelector}`).length == 1) {
                                    selector = `${parentTag}${tagIndex} ${childSelector}`;
                                    parentFlag = false;
                                }
                                else {
                                    parentEle = parentEle.parentNode;
                                }
                            }
                        }
                    }
                    return selector;
                } catch (err) {
                    console.log("ERROR in get getCssSelector(): " + err);
                }
            }
            sCssSelector = getCssSelector(element);

            // capture href of the element
            var shref='';
            function getHref(ele) {
                try {
                    var href='';
                    if (ele.hasAttribute('href')) {
                        href = ele.getAttribute('href');
                    }
                    else {
                        href = null;
                    }
                    return href
                } catch (err) {
                    console.log("skipping this element: " + err);
                }
            }
            shref = getHref(element);

            if (sid == '') {
                sid = 'null';
            }
            smultipleFlag = element.hasAttribute('multiple');
            sishidden = sisVisible(element);
            if (sishidden == true || sishidden == 'True' || sishidden == 'true') {
                sishidden = 'No';
            } else {
                sishidden = 'Yes';
            }
            var sfirstpass = 0;
            var srpath = '';
            var setype = element.getAttribute('type');
            setype = (String(setype)).toLowerCase();
            for (var spath = ''; element && element.nodeType == 1; element = element.parentNode) {
                var spredicate = [];
                var ssiblings = element.parentNode.children;
                var scount = 0;
                var sunique = false;
                var snewPath = '';
                var sidx = 0;
                for (var i = 0; ssiblings && (i < ssiblings.length); i++) {
                    if (ssiblings[i].tagName == element.tagName) {
                        scount++;
                        if (ssiblings[i] == element) {
                            sidx = scount;
                        }
                    }
                }
                if (sidx == 1 && scount == 1) {
                    sidx = null;
                }
                if (suseId && element.id) {
                    spredicate[spredicate.length] = '@id=' + '"' + element.id + '"';
                    sunique = true;
                }
                xidx = (suseIdx && sidx) ? ('[' + sidx + ']') : '';
                sidx = (suseIdx && sidx && !sunique) ? ('[' + sidx + ']') : '';
                spredicate = (spredicate.length > 0) ? ('[' + spredicate.join(' and ') + ']') : '';
                spath = '/' + element.tagName.toLowerCase() + xidx + spath;
                if (sfirstpass == 0) {
                    if (sunique && srelative) {
                        srpath = '//*' + sidx + spredicate + srpath;
                        sfirstpass = 1;
                    } else {
                        srpath = '/' + element.tagName.toLowerCase() + sidx + spredicate + srpath;
                    }
                }
            }
            if (stagname == 'textarea') {
                stagname = 'input';
                stagtype = 'txtarea';
            } else if (stagname == 'select' && smultipleFlag) {
                stagname = 'list';
                stagtype = 'lst';
            } else if (stagname == 'select') {
                stagtype = 'select';
            } else if (stagname == 'td' || stagname == 'tr') {
                stagname = 'tablecell';
                stagtype = 'tblcell';
            } else if (stagname == 'a') {
                stagtype = 'lnk';
            } else if (stagname == 'table') {
                stagtype = 'tbl';
            } else if (stagname == 'img') {
                stagtype = 'img';
            } else if (stagname == 'input' && setype == 'image') {
                stagname = 'img';
                stagtype = 'img';
            }
            if (stagname == 'input' && (setype == 'button' || setype == 'submit' || setype == 'reset' || setype == 'file')) {
                stagname = 'button';
                stagtype = 'btn';
            } else if (stagname == 'input' && setype == 'radio') {
                stagname = 'radiobutton';
                stagtype = 'radiobtn';
            } else if (stagname == 'input' && setype == 'checkbox') {
                stagname = 'checkbox';
                stagtype = 'chkbox';
            } else if (stagname == 'input' && (setype == 'text' || setype == 'email' || setype == 'number' || setype == 'password' || setype == 'range' || setype == 'search' || setype == 'url')) {
                stagname = 'input';
                stagtype = 'txtbox';
            } else if (stagname == 'input' && stagtype == '' && (setype == 'hidden' || setype == 'null')) {
                stagname = 'div';
                stagtype = 'elmnt';
            } else if (stagname == 'button') {
                stagname = 'button';
                stagtype = 'btn';
            }
            if (role == 'grid') {
                stagname = 'grid';
                stagtype = 'grid';
            }
            stextvalue = stextvalue.replace(">", "");
            stextvalue = stextvalue.replace("</", "");
            stextvalue = stextvalue.replace("<", "");
            stextvalue = stextvalue.replace("/>", "");
            stextvalue = stextvalue.split("\\n").join("");
            stextvalue = stextvalue.split("\\t").join("");
            stextvalue = stextvalue.split("\\r").join("");
            stextvalue = stextvalue.split("  ").join("");
            stextvalue = stextvalue.split("\\u00a0").join("");
            if (stextvalue == '' || stextvalue.length == 0 || stextvalue == '0') {
                stextvalue = 'NONAME' + snonamecounter;
                snonamecounter = snonamecounter + 1;
                scustname = stextvalue;
            } else {
                scustname = stextvalue;
            }
            if (stagtype != '') {
                scustname = scustname + '_' + stagtype;
            } else {
                scustname = scustname + '_elmnt';
            }
            coordinates = left + ';' + top + ';' + height + ';' + width;
            coordinates = String(coordinates);
            snewPath = String(spath) + ';' + String(sid) + ';' + String(srpath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + slabel + ';' + shref + ';' + sCssSelector + ';' + 'null' + ';' + stagname;
            sarr.push({
                'xpath': snewPath,
                'tag': stagname,
                'hiddentag': sishidden,
                'url': surl,
                'height': height,
                'width': width,
                'custname': scustname,
                'top': top,
                'left': left
            });
        }
        return sarr;
    }

    function findCoordinates(element) {
        height = element.offsetHeight || 0;
        width = element.offsetWidth || 0;
        top = 0;
        left = 0;
        do {
            top += element.offsetTop || 0;
            left += element.offsetLeft || 0;
            element = element.offsetParent;
        } while (element);
    }

    function saddNodesOuter(sarray, scollection) {
        for (var i = 0; scollection && scollection.length && i < scollection.length; i++) {
            sarray.push(scollection[i]);
        }
    };

    function stext_content(f) {
        var sfirstText = '';
        var stextdisplay = '';
        for (var z = 0; z < f.childNodes.length; z++) {
            var scurNode = f.childNodes[z];
            swhitespace = /^\s*$/;
            if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {
                sfirstText = scurNode.nodeValue;
                stextdisplay = stextdisplay + sfirstText;
            }
        }
        return (stextdisplay);
    };
    return getElementProperties(element);
    """

    AVO_ASSURE_WEBELEMENT_HIGHLIGHT_STYLE = "background: #fff300 !important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;"

    """Method to take screenshot of the current web page, returns the image as a base64 string"""
    def fullpage_screenshot(self,driver, screen_shot_path):
        log.info("Performing full page screenshot")
        screen = None
        #If you have an approach to get full screenshot without cropping all sides, remove the try and execute block of code.
        try:
            if not os.path.exists(os.path.dirname(screen_shot_path)):
                os.makedirs(os.path.dirname(screen_shot_path))
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            import webconstants
            options = Options()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--headless")  # Use headless mode for running in the background
            options.add_argument("--disable-gpu")
            exec_path = webconstants.CHROME_DRIVER_PATH
            log.debug("Performing full page screenshot in headless mode")
            driver_headless = webdriver.Chrome(executable_path = exec_path, options = options) # Using by default chrome driver
            driver_headless.maximize_window()
            driver_headless.get(driver.current_url)
            total_width = driver_headless.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
            total_height = driver_headless.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
            if total_width > 0 and total_height > 0:
                # Set the window size to match the entire webpage
                driver_headless.set_window_size(total_width, total_height)
                driver_headless.save_screenshot(f"{screen_shot_path}")
                driver_headless.quit()
                with open(screen_shot_path, "rb") as f:
                    b64_screen = base64.b64encode(f.read())
                    screen=codecs.decode(b64_screen)
        except:
            try:
                total_width = driver.execute_script("return document.body.offsetWidth")
                total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
                viewport_width = driver.execute_script("return window.innerWidth")
                viewport_height = driver.execute_script("return window.innerHeight")
                driver.execute_script("window.scrollTo({0}, {1})".format(0, total_height))
                time.sleep(1)
                total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
                #scroll to the top of the page
                driver.execute_script("window.scrollTo(0,0)")
                rectangles = []
                if total_width == 0:
                    total_width = driver.execute_script("return document.documentElement.offsetWidth")

                if total_height < viewport_height:
                    total_height = viewport_height

                if total_width < viewport_width:
                    total_width = viewport_width

                if total_width > 0 and total_height > 0 and viewport_width > 0 and viewport_height > 0:

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

                            rectangles.append((ii, i, top_width, top_height))

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
                        driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                        code = '''var elems = document.body.getElementsByTagName("*"); var len = elems.length; document.body.style.removeProperty('max-width'); document.body.style.removeProperty('overflow-x'); for (var i=0;i<len;i++) { 	if (window.getComputedStyle(elems[i],null).getPropertyValue('position') == 'fixed') { 		elems[i].style.removeProperty('opacity'); 	} }'''
                        driver.execute_script(code)
                    stitched_image.save(screen_shot_path)
                    with open(screen_shot_path, "rb") as f:
                        b64_screen = base64.b64encode(f.read())
                        screen=codecs.decode(b64_screen)
                else:
                    screen = driver.get_screenshot_as_base64()
            except Exception as e:
                log.debug("Error while performing full page screenshot")
                log.debug(e,exc_info=True)
                screen = driver.get_screenshot_as_base64()
        finally:
            return screen, total_width, total_height

    """Method to switch into frames and iframes"""
    def switchtoframe_webscrape(self,driver,currenthandle,mypath):
        log.info('Inside switchtoframe_webscrape method')
        cond_flag = False
        log.info('Splitting Iframe/frame url by /')
        allframes = mypath.split("/")
        # switching to focused tab
        driver.switch_to.window(currenthandle)
        log.info('Switched to current window handle')
        # switching to outer page of the focused tab
        driver.switch_to_default_content()
        log.info('Switched to default content')
        for i in allframes:
            if i != '':
                # find the integer number attached with frame/iframe e.g. 2 in 2f or 2i
                j = i.rstrip(i[-1:])
                j = int(j)
                frame_or_iframe = domconstants.FRAME if i[-1:] == 'f' else domconstants.IFRAME
                # now we know its frame or iframe, let's try to switch into it
                try:
                    if j >=0 and j < len(driver.find_elements_by_tag_name(frame_or_iframe)):
                        if driver.find_elements_by_tag_name(frame_or_iframe)[j]:
                            driver.switch_to.frame(driver.find_elements_by_tag_name(frame_or_iframe)[j])
                            cond_flag = True
                        else:
                            cond_flag = False
                            break
                except Exception as e:
                    log.error(e)
                    cond_flag = False
        return cond_flag

    """Method to locate webelement using provided identifiers"""
    def locate_webelement(self,driver,identifiers):
        webElement = None
        try:
            # find by relative xpath
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
                # find by id
                tempwebElement = driver.find_elements_by_id(identifiers[1])
                if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                    tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = None
                webElement = tempwebElement
            except Exception as webEx:
                try:
                    # find by absolute xpath
                    tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_name(identifiers[3])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_class_name(identifiers[5])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = driver.find_elements_by_css_selector(identifiers[11])
                                if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                    tempwebElement = None
                    webElement = tempwebElement
                except Exception as webEx:
                    try:
                        # find by name
                        tempwebElement = driver.find_elements_by_name(identifiers[3])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_class_name(identifiers[5])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = driver.find_elements_by_css_selector(identifiers[11])
                                if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                    tempwebElement = None
                        webElement = tempwebElement
                    except Exception as webEx:
                        try:
                            # find by class_name
                            tempwebElement = driver.find_elements_by_class_name(identifiers[5])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = driver.find_elements_by_css_selector(identifiers[11])
                                if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                    tempwebElement = None
                            webElement = tempwebElement
                        except Exception as webEx:
                            try:
                                # find by css_selector
                                tempwebElement = driver.find_elements_by_css_selector(identifiers[11])
                                if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                    tempwebElement = None
                                webElement = tempwebElement
                            except Exception as webEx:
                                webElement = None
        return webElement

    """Method to check whether a given element URL belongs to frame/iframe page or to the outer page"""
    def is_iframe_frame_url(self,url):
        try:
            int(url[0])
            log.debug('The url %s is an iframe/frmae url',url)
            return True
        except ValueError:
            log.debug('The url %s is an normal webpage url',url)
            return False

    def get_hwnds_for_pid(self, pid):
        def callback(hwnd, hwnds):

            if win32gui.IsWindowVisible(hwnd):
                # logging.warning('inside 2nd def function')
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                # logging.warning('found id is == %s ', found_pid)
                if found_pid == pid:
                    # logging.warning('found pid %s ', pid)

                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds

    """win32 utilities
        def : bring_Window_Front
        param : pid of the browser opened by driver
        Brings the browser window to front
    """
    def bring_Window_Front(self, pid):
        hwnd = WebScrape_Utils.get_hwnds_for_pid(self, pid)
        winSize = len(hwnd)
        win32gui.ShowWindow(hwnd[winSize - 1], win32con.SW_MAXIMIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        return hwnd[winSize - 1]


# def test(a,b,part):
#     part=2
#     for rectangle in rectangles:
#         driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
#         file_name = "part_{0}.png".format(part)
#         driver.get_screenshot_as_file(file_name)
#         screenshot = Image.open(file_name)
#         if rectangle[1] + viewport_height > total_height:
#             offset = (rectangle[0], total_height - viewport_height)
#         else:
#             offset = (rectangle[0], rectangle[1])
#         stitched_image.paste(screenshot, offset)
#         # screenshot.close()
#         del screenshot
#         os.remove(file_name)
#         part = part + 1
#         previous = rectangle
#         driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
#         code = '''var elems = document.body.getElementsByTagName("*"); var len = elems.length; document.body.style.removeProperty('max-width'); document.body.style.removeProperty('overflow-x'); for (var i=0;i<len;i++) { 	if (window.getComputedStyle(elems[i],  null).getPropertyValue('position') == 'fixed') { 		elems[i].style.removeProperty  ('opacity'); 	} }'''
#         driver.execute_script(code)
