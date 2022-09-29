import os
from constants import SYSTEM_OS, BROWSER_NAME

drivers_path = os.path.join(os.environ["AVO_ASSURE_HOME"], "lib", "Drivers")

assets_path = os.environ["AVO_ASSURE_HOME"] + os.sep + "assets"

EXTENSIONS_PATH = os.environ["AVO_ASSURE_HOME"] + os.sep + "extension"

GET_XPATH_JS="""function getElementXPath(elt) {var path = "";for (; elt && elt.nodeType == 1; elt = elt.parentNode){idx = getElementIdx(elt);xname = elt.tagName;if (idx >= 1){xname += "[" + idx + "]";}path = "/" + xname + path;}return path;}function getElementIdx(elt){var count = 1;for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){if(sib.nodeType == 1 && sib.tagName == elt.tagName){count++;}}return count;}return getElementXPath(arguments[0]).toLowerCase();"""

CLICK_JAVASCRIPT = """var evType; element=arguments[0]; if (document.createEvent) {     evType = 'Click executed through part-1';     var evt = document.createEvent('MouseEvents');     evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt)    }, 100); } else {     evType = 'Click executed through part-2';   	setTimeout(function() {     element.click();   	}, 100); } return (evType);"""

GET_CELL_JS="""var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };"""

VERIFY_VISIBLE = 'NO'

TEST_RESULT_PASS = "Pass"

TEST_RESULT_FAIL = "Fail"

VALUE = 'value'

NAME = 'name'

HREF = 'href'

TEST_RESULT_TRUE = "True"

TEST_RESULT_FALSE = "False"

METHOD_INVALID='Invalid Keyword'

INVALID_INPUT='Input is Invalid'

CHROME_DRIVER_PATH = drivers_path + os.sep + "chromedriver"

EDGE_DRIVER_PATH = drivers_path + os.sep + "MicrosoftWebDriver.exe"

EDGE_CHROMIUM_DRIVER_PATH = drivers_path + os.sep + "msedgedriver"

IE_DRIVER_PATH_64 =  drivers_path + os.sep + 'IEDriverServer64.exe'

IE_DRIVER_PATH_32 =   drivers_path + os.sep + 'IEDriverServer.exe'

PHANTOM_DRIVER_PATH =  drivers_path + os.sep + 'phantomjs.exe'

GECKODRIVER_PATH =  drivers_path + os.sep + 'geckodriver'

AVO_EXTENSION_PATH = assets_path + os.sep + 'AvoAssure.crx'

if SYSTEM_OS == "Windows":
    CHROME_DRIVER_PATH += ".exe"
    GECKODRIVER_PATH += ".exe"
    EDGE_CHROMIUM_DRIVER_PATH += ".exe"


SET_TEXT_SCRIPT="""arguments[0].value=arguments[1]"""

SET_TEXT_SCRIPT_DIV_SPAN="""arguments[0].textContent=arguments[1]"""

CLICK_RADIO_CHECKBOX="""arguments[0].click()"""

CLEAR_TEXT_SCRIPT="""arguments[0].value=''"""

HIGHLIGHT_SCRIPT_IE="""arguments[0].style.setAttribute('cssText', arguments[1]);"""

APPLY_CSS="""background: #fff300; border: 2px solid #cc3300;outline: 2px solid #fff300;"""

HIGHLIGHT_SCRIPT="""arguments[0].setAttribute('style', arguments[1]);"""

REMOVE_CSS_IE8="""background: 0; border: 0px none 0; outline: none"""

FOUCS_ELE="""arguments[0].focus();"""

LEFT_BUTTON='left'

RIGHT_BUTTON='right'

MOUSE_HOVER_FF="""return window.mozInnerScreenY"""

IFRAME = 'iframe'

FRAME = 'frame'

HTML = 'html'

CUSTOM='@Custom'

GET_XPATH_SCRIPT="""function getElementXPath(elt) {     var path = '';     for (; elt && elt.nodeType == 1; elt = elt.parentNode) {         idx = getElementIdx(elt);         xname = elt.tagName;         if (idx >= 1) {             xname += '[' + idx + ']';         }         path = '/' + xname + path;     }     return path; }  function getElementIdx(elt) {     var count = 1;     for (var sib = elt.previousSibling; sib; sib = sib.previousSibling) {         if (sib.nodeType == 1 && sib.tagName == elt.tagName) {             count++;         }     }     return count; } return getElementXPath(arguments[0]).toLowerCase(); """

FIND_INDEX_JS="""var abc = arguments[0]; var allele = document.getElementsByTagName('*'); var i; for (j = 0; j < allele.length; j++) {     if (abc === allele[j]) {       	i=j;         break;     } } return i;"""

#CUSTOM_JS="""var eleCollection = document.getElementsByTagName('*'); var startIndex = arguments[1]; var eleType = arguments[2]; eleType = eleType.toLowerCase(); var eleVisibleText = arguments[3]; var eleIndex = arguments[4]; var localIndex; localIndex = arguments[5]; var result = []; var result0 = 'null'; var result1 = 'null'; var result2 = localIndex; var result3 = eleCollection.length; var result4 = 'null'; var col = []; col['submit'] = 'button'; col['reset'] = 'button'; col['button'] = 'button'; col['file'] = 'button'; col['image'] = 'img'; col['search'] = 'text'; col['number'] = 'text'; col['url'] = 'text'; col['email'] = 'text'; col['tel'] = 'text'; col['textarea'] = 'text'; col['password'] = 'text'; var listFlag = false; var dropdown = false; if (eleType == 'listbox') {     listFlag = true; } else if (eleType == 'dropdown') {     dropdown = true; } if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('input');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })();  function stext_content(f, teleType) {     var sfirstText = '';     var stextdisplay = '';     var inlineText = '';     if (f.getAttribute('alt') != null) inlineText = inlineText.concat(f.getAttribute('alt'), ' ');     if (f.getAttribute('title') != null) inlineText = inlineText.concat(f.getAttribute('title'), ' ');     if (f.getAttribute('value') != null) inlineText = inlineText.concat(f.getAttribute('value'), ' ');     if (f.getAttribute('placeholder') != null) inlineText = inlineText.concat(f.getAttribute('placeholder'), ' ');     if (teleType == 'dropdown' || teleType == 'listbox') {         inlineText = inlineText.concat(f.textContent, ' ');     }     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     stextdisplay = inlineText.concat(stextdisplay);     return (stextdisplay); };  function findelement(feletype) {     for (i = startIndex; i < eleCollection.length; i++) {         if (sisVisible(eleCollection[i])) {             if (eleCollection[i].tagName.toLowerCase() == feletype || col[eleCollection[i].tagName.toLowerCase()] == feletype || (dropdown && eleCollection[i].tagName.toLowerCase() == 'select' && !eleCollection[i].hasAttribute('multiple')) || (listFlag && eleCollection[i].tagName.toLowerCase() == 'select' && eleCollection[i].hasAttribute('multiple'))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input') && (eleCollection[i].hasAttribute('type')) && ((eleCollection[i].getAttribute('type').toLowerCase() == feletype) || (col[eleCollection[i].getAttribute('type').toLowerCase()] == feletype))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input')&& (feletype == 'text')) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             }else if (eleCollection[i].tagName.toLowerCase() == 'iframe' || eleCollection[i].tagName.toLowerCase() == 'frame') {                 result0 = 'stf';                 result1 = eleCollection[i];                 result2 = localIndex;                 result3 = i + 1;                 result4 = 'null';                 break;             }         }     } }; findelement(eleType); result[0] = result0; result[1] = result1; result[2] = result2; result[3] = result3; result[4] = result4; return result;"""
#CUSTOM_JS="""var eleCollection = document.getElementsByTagName('*'); var startIndex = arguments[1]; var eleType = arguments[2]; eleType = eleType.toLowerCase(); var eleVisibleText = arguments[3]; var eleIndex = arguments[4]; var localIndex; localIndex = arguments[5]; var result = []; var result0 = 'null'; var result1 = 'null'; var result2 = localIndex; var result3 = eleCollection.length; var result4 = 'null'; var col = []; col['submit'] = 'button'; col['reset'] = 'button'; col['button'] = 'button'; col['file'] = 'button'; col['image'] = 'img'; col['search'] = 'text'; col['number'] = 'text'; col['url'] = 'text'; col['email'] = 'text'; col['tel'] = 'text'; col['textarea'] = 'text'; col['password'] = 'text'; var listFlag = false; var dropdown = false; if (eleType == 'listbox') {     listFlag = true; } else if (eleType == 'dropdown') {     dropdown = true; } if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('input');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })();  function stext_content(f, teleType) {     var sfirstText = '';     var stextdisplay = '';     var inlineText = '';     if (f.getAttribute('alt') != null) inlineText = inlineText.concat(f.getAttribute('alt'), ' ');     if (f.getAttribute('title') != null) inlineText = inlineText.concat(f.getAttribute('title'), ' ');     if (f.getAttribute('value') != null) inlineText = inlineText.concat(f.getAttribute('value'), ' ');     if (f.getAttribute('placeholder') != null) inlineText = inlineText.concat(f.getAttribute('placeholder'), ' ');     if (teleType == 'dropdown' || teleType == 'listbox') {         inlineText = inlineText.concat(f.textContent, ' ');     }     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     stextdisplay = inlineText.concat(stextdisplay);     return (stextdisplay); };  function findelement(feletype) {     for (i = startIndex; i < eleCollection.length; i++) {         if (sisVisible(eleCollection[i])) {
#if ((eleCollection[i].tagName.toLowerCase() == feletype && eleCollection[i].tagName.toLowerCase()!="text") || col[eleCollection[i].tagName.toLowerCase()] == feletype || (dropdown && eleCollection[i].tagName.toLowerCase() == 'select' && !eleCollection[i].hasAttribute('multiple')) || (listFlag && eleCollection[i].tagName.toLowerCase() == 'select' && eleCollection[i].hasAttribute('multiple'))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input') && (eleCollection[i].hasAttribute('type')) && ((eleCollection[i].getAttribute('type').toLowerCase() == feletype) || (col[eleCollection[i].getAttribute('type').toLowerCase()] == feletype))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input')&& (feletype == 'text')) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             }else if (eleCollection[i].tagName.toLowerCase() == 'iframe' || eleCollection[i].tagName.toLowerCase() == 'frame') {                 result0 = 'stf';                 result1 = eleCollection[i];                 result2 = localIndex;                 result3 = i + 1;                 result4 = 'null';                 break;             }         }     } }; findelement(eleType); result[0] = result0; result[1] = result1; result[2] = result2; result[3] = result3; result[4] = result4; return result;"""


CUSTOM_JS="""var eleCollection = document.getElementsByTagName("*"), startIndex = arguments[1], eleType = arguments[2]; eleType = eleType.toLowerCase();var absMatch=arguments[6]; var localIndex, eleVisibleText = arguments[3], eleIndex = arguments[4], result = [], result0 = "null", result1 = "null", result2 = localIndex = arguments[5], result3 = eleCollection.length, result4 = "null", col = []; col.select="select", col.submit = "button", col.reset = "button", col.button = "button", col.file = "button", col.image = "img", col.search = "text", col.number = "text", col.url = "text", col.email = "text", col.tel = "text", col.textarea = "text", col.password = "text"; var listFlag = !1, dropdown = !1, gridFlag = false; if (eleType == 'grid') {     gridFlag = true; } "listbox" == eleType ? listFlag = !0 : "dropdown" == eleType && (dropdown = !0), window.Element && window.Element.prototype && window.Element.prototype.hasAttribute || function () {     function e(e) {         return void 0 !== this[e]     }     for (var t = document.getElementsByTagName("input"), l = 0; l < t.length; l++)         t[l].hasAttribute = e } (); var sisVisible = function () {     return function (e) {         if (document.hidden || 0 == e.offsetWidth || 0 == e.offsetHeight || "hidden" == e.style.visibility || "none" == e.style.display || 0 === e.style.opacity)             return !1;         e.getBoundingClientRect();         if (window.getComputedStyle || e.currentStyle)             for (var t = e, l = null; t && t !== document; ) {                 if (!t.parentNode)                     return !1;                 if ((l = window.getComputedStyle ? window.getComputedStyle(t, null) : t.currentStyle) && ("hidden" == l.visibility || "none" == l.display || void 0 !== l.opacity && !(l.opacity > 0)))                     return !1;                 t = t.parentNode             }         return !0     } } (); function checkExactEqual(e, eleText) { if(absMatch) { if (eleText != '') {  if (e.innerText === eleText) return !0; return !1 } } return !0 } function stext_content(e, t) {     var l = "",     o = "";     null != e.getAttribute("alt") && (o = o.concat(e.getAttribute("alt"), " ")),     null != e.getAttribute("title") && (o = o.concat(e.getAttribute("title"), " ")),     null != e.getAttribute("value") && (o = o.concat(e.getAttribute("value"), " ")),     null != e.getAttribute("placeholder") && (o = o.concat(e.getAttribute("placeholder"), " ")),     "dropdown" != t && "listbox" != t || (o = o.concat(e.textContent, " "));     for (var i = 0; i < e.childNodes.length; i++) {         var n = e.childNodes[i];         swhitespace = /^\s*$/,         "#text" !== n.nodeName || swhitespace.test(n.nodeValue) || (l += n.nodeValue)     }     return l = o.concat(l) } function findelement(e) {     for (i = startIndex; i < eleCollection.length; i++)         if (sisVisible(eleCollection[i]))             if (eleCollection[i].tagName.toLowerCase() == e && " text " != eleCollection[i].tagName.toLowerCase() || col[eleCollection[i].tagName.toLowerCase()] == e || dropdown && "select" == eleCollection[i].tagName.toLowerCase() && !eleCollection[i].hasAttribute("multiple") || listFlag && "select" == eleCollection[i].tagName.toLowerCase() && eleCollection[i].hasAttribute("multiple") || (gridFlag && eleCollection[i].hasAttribute('role') && eleCollection[i].getAttribute('role') == 'grid' && eleCollection[i].tagName.toLowerCase() == 'div')) {                 if (stext_content(eleCollection[i], e.toLowerCase()).indexOf(eleVisibleText) >= 0 && checkExactEqual(eleCollection[i], eleVisibleText)) {                     if (localIndex == eleIndex) {                         result0 = "found",                         result1 = "null",                         result2 = localIndex,                         result3 = i + 1,                         result4 = eleCollection[i];                         break                     }                     localIndex += 1                 }             } else if ("input" != eleCollection[i].tagName.toLowerCase() || !eleCollection[i].hasAttribute("type") || eleCollection[i].getAttribute("type").toLowerCase() != e && col[eleCollection[i].getAttribute("type").toLowerCase()] != e) {                 if ("input" == eleCollection[i].tagName.toLowerCase() && eleCollection[i].type.toLowerCase() == e) {                     if (stext_content(eleCollection[i], e.toLowerCase()).indexOf(eleVisibleText) >= 0 && checkExactEqual(eleCollection[i], eleVisibleText)) {                         if (localIndex == eleIndex) {                             result0 = "found",                             result1 = "null",                             result2 = localIndex,                             result3 = i + 1,                             result4 = eleCollection[i];                             break                         }                         localIndex += 1                     }                 } else if ("iframe" == eleCollection[i].tagName.toLowerCase() || "frame" == eleCollection[i].tagName.toLowerCase()) {                     result0 = "stf",                     result1 = eleCollection[i],                     result2 = localIndex,                     result3 = i + 1,                     result4 = "null";                     break                 }             } else if (stext_content(eleCollection[i], e.toLowerCase()).indexOf(eleVisibleText) >= 0) {                 if (localIndex == eleIndex) {                     result0 = "found",                     result1 = "null",                     result2 = localIndex,                     result3 = i + 1,                     result4 = eleCollection[i];                     break                 }                 localIndex += 1             } } findelement(eleType), result[0] = result0, result[1] = result1, result[2] = result2, result[3] = result3, result[4] = result4; return result; """


#CUSTOM_IFRAME_JS="""var eleCollection = document.getElementsByTagName('*'); var startIndex = arguments[1]; var eleType = arguments[2]; eleType = eleType.toLowerCase(); var eleVisibleText = arguments[3]; var eleIndex = arguments[4]; var localIndex = arguments[5]; var result = []; var result0 = 'null'; var result1 = 'null'; var result2 = localIndex; var result3 = eleCollection.length; var result4 = 'null'; var col = []; col['submit'] = 'button'; col['reset'] = 'button'; col['button'] = 'button'; col['file'] = 'button'; col['image'] = 'img'; col['search'] = 'text'; col['number'] = 'text'; col['url'] = 'text'; col['email'] = 'text'; col['tel'] = 'text'; col['textarea'] = 'text'; col['password'] = 'text'; var listFlag = false; var dropdown = false; if (eleType == 'listbox') {     listFlag = true; } else if (eleType == 'dropdown') {     dropdown = true; } if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('input');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })();  function stext_content(f, teleType) {     var sfirstText = '';     var stextdisplay = '';     var inlineText = '';     if (f.getAttribute('alt') != null) inlineText = inlineText.concat(f.getAttribute('alt'), ' ');     if (f.getAttribute('title') != null) inlineText = inlineText.concat(f.getAttribute('title'), ' ');     if (f.getAttribute('value') != null) inlineText = inlineText.concat(f.getAttribute('value'), ' ');     if (f.getAttribute('placeholder') != null) inlineText = inlineText.concat(f.getAttribute('placeholder'), ' ');     if (teleType == 'dropdown' || teleType == 'listbox') {         inlineText = inlineText.concat(f.textContent, ' ');     }     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     stextdisplay = inlineText.concat(stextdisplay);     return (stextdisplay); };  function findelement(feletype) {     for (i = startIndex; i < eleCollection.length; i++) {         if (sisVisible(eleCollection[i])) {if (eleCollection[i].tagName.toLowerCase() == feletype || col[eleCollection[i].tagName.toLowerCase()] == feletype || (dropdown && eleCollection[i].tagName.toLowerCase() == 'select' && !eleCollection[i].hasAttribute('multiple')) || (listFlag && eleCollection[i].tagName.toLowerCase() == 'select' && eleCollection[i].hasAttribute('multiple'))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input') && (eleCollection[i].hasAttribute('type')) && ((eleCollection[i].getAttribute('type').toLowerCase() == feletype) || (col[eleCollection[i].getAttribute('type').toLowerCase()] == feletype))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             }         }     } }; findelement(eleType); result[0] = result0; result[1] = result1; result[2] = result2; result[3] = result3; result[4] = result4; return result;"""
CUSTOM_IFRAME_JS="""var eleCollection = document.getElementsByTagName('*'); var startIndex = arguments[1]; var eleType = arguments[2]; eleType = eleType.toLowerCase(); var eleVisibleText = arguments[3]; var eleIndex = arguments[4]; var localIndex = arguments[5]; var result = []; var result0 = 'null'; var result1 = 'null'; var result2 = localIndex; var result3 = eleCollection.length; var result4 = 'null'; var col = []; col['select'] = 'select'; col['submit'] = 'button'; col['reset'] = 'button'; col['button'] = 'button'; col['file'] = 'button'; col['image'] = 'img'; col['search'] = 'text'; col['number'] = 'text'; col['url'] = 'text'; col['email'] = 'text'; col['tel'] = 'text'; col['textarea'] = 'text'; col['password'] = 'text'; var listFlag = false; var dropdown = false; var gridFlag = false; if (eleType == 'listbox') {     listFlag = true; } else if (eleType == 'dropdown') {     dropdown = true; } else if (eleType == 'grid') {     gridFlag = true; } if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function () {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('input');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }         ()); } var sisVisible = (function () {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent)                 return true;             schild = schild.parentNode;         }         return false;     };     return function (selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0)             return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,             scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode)                     return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0))))                     return false;                 sel = sel.parentNode;             }         }         return true;     } })(); function stext_content(f, teleType) {     var sfirstText = '';     var stextdisplay = '';     var inlineText = '';     if (f.getAttribute('alt') != null)         inlineText = inlineText.concat(f.getAttribute('alt'), ' ');     if (f.getAttribute('title') != null)         inlineText = inlineText.concat(f.getAttribute('title'), ' ');     if (f.getAttribute('value') != null)         inlineText = inlineText.concat(f.getAttribute('value'), ' ');     if (f.getAttribute('placeholder') != null)         inlineText = inlineText.concat(f.getAttribute('placeholder'), ' ');     if (teleType == 'dropdown' || teleType == 'listbox') {         inlineText = inlineText.concat(f.textContent, ' ');     }     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     stextdisplay = inlineText.concat(stextdisplay);     return (stextdisplay); }; function findelement(feletype) {     for (i = startIndex; i < eleCollection.length; i++) {                  if (sisVisible(eleCollection[i])) {             if ((eleCollection[i].tagName.toLowerCase() == feletype && eleCollection[i].tagName.toLowerCase() != "text") || col[eleCollection[i].tagName.toLowerCase()] == feletype || (dropdown && eleCollection[i].tagName.toLowerCase() == 'select' && !eleCollection[i].hasAttribute('multiple')) || (listFlag && eleCollection[i].tagName.toLowerCase() == 'select' && eleCollection[i].hasAttribute('multiple')) || (gridFlag && eleCollection[i].hasAttribute('role') && eleCollection[i].getAttribute('role') == 'grid' && eleCollection[i].tagName.toLowerCase() == 'div')) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input') && (eleCollection[i].hasAttribute('type')) && ((eleCollection[i].getAttribute('type').toLowerCase() == feletype) || (col[eleCollection[i].getAttribute('type').toLowerCase()] == feletype))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             }         }     } }; findelement(eleType); result[0] = result0; result[1] = result1; result[2] = result2; result[3] = result3; result[4] = result4; return result; """


GET_OBJECT_COUNT_JS="""var temp = getCount(arguments[0], arguments[1], arguments[2], arguments[3]); return temp; function getCount(counter, user_input, index, flag) {     var i;     var result = [];     var req_eles = document.getElementsByTagName("*");     var max = req_eles.length;     console.log(max);     var sisVisible = (function () {         function inside(schild, sparent) {             while (schild) {                 if (schild === sparent)                     return true;                 schild = schild.parentNode;             }             return false;         };         return function (selem) {             if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0)                 return false;             var srect = selem.getBoundingClientRect();             if (window.getComputedStyle || selem.currentStyle) {                 var sel = selem,                 scomp = null;                 while (sel) {                     if (sel === document) {                         break;                     } else if (!sel.parentNode)                         return false;                     scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                     if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0))))                         return false;                     sel = sel.parentNode;                 }             }             return true;         }     })();     if (max > 0) {         if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {             (function () {                 function hasAttribute(attrName) {                     return typeof this[attrName] !== 'undefined';                 }                 var inputs = document.getElementsByTagName('input');                 for (var i = 0; i < inputs.length; i++) {                     inputs[i].hasAttribute = hasAttribute;                 }             }                 ());         }         for (i = index; i < max; i++) {             var tagname = req_eles[i].tagName;             var type = req_eles[i].type;             var role = 'NULL';             if (req_eles[i].hasAttribute('role')) {                 if (req_eles[i].getAttribute('role') === 'grid' && req_eles[i].tagName.toLowerCase() === 'div') {                     role = 'GRID';                 }             }             console.log(tagname, type, user_input, i, sisVisible(req_eles[i])); /*if (found == 1) {*/              if (sisVisible(req_eles[i])) {                 if ((tagname == "IFRAME") || (tagname == "FRAME")) {                     result[1] = req_eles[i];                     break;                 } else if (req_eles[i].hasAttribute("type")) {                     if (user_input == "button") {                         if ((type == "submit") || (type == "reset") || (type == "file") || (type == "button")) {                             counter = counter + 1;                         }                     } else if (user_input == "text") {                         if ((type == user_input) || (type == "password") || (type == "number") || (type == "url") || (type == "tel") || (type == "user_inputarea") || (type == "search")) {                             counter = counter + 1;                         }                     } else if (user_input == "img") {                         if ((type == "image") || (tagname == "IMAGE")) {                             counter = counter + 1;                         }                     } else {                         if ((type == user_input)) {                             counter = counter + 1;                         }                     }                 } else if (tagname == user_input.toUpperCase()) {                     if ((user_input.toUpperCase() == "SELECT") && (flag == 1)) {                         if (req_eles[i].multiple == true) {                             counter = counter + 1;                         }                     } else {                         counter = counter + 1;                     }                 } else if (role == user_input.toUpperCase()) {                     counter = counter + 1;                 }             } /*} else if (found == 0) {                 if ((tagname == "IFRAME") || (tagname == "FRAME")) {                     result[1] = req_eles[i];                     break;                 }             }*/         }     }     if (i >= max) {         result[3] = "done";     }     result[0] = counter;     result[2] = i;     console.log(result);     return result; }; """


STATUS_CODE_DICT={520: 'Unknown Error',
            521: 'Web Server Is Down',
            522: 'Connection Tmed Out',
            523: 'Origin Is Unreachable',
            524: 'A Timed out Occurred',
            525: 'SSL Handshake Failed',
            526: 'Invalid SSL Cirtificate',
            400: 'Bad Request',
            401: 'Unauthorized',
            402: 'PaymentRequired',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            406: 'Not Acceptable',
            407: 'Proxy Authentication Required ',
            408: 'Request Timeout',
            409: 'Conflict',
            410: 'Gone',
            411: 'Length Required',
            412: 'Precondition Failed',
            413: 'Pay Lood Too Large',
            414: 'URL Too Long',
            415: 'UnSupported Media Type',
            416: 'Range not Satisfiable',
            417: 'Expectation Failed',
            418: " I'm a teapot (RFC 2324)",
            421: ' Misdirected Request',
            422: 'Unprocessable Entity',
            423: 'Locked',
            424: 'Failed Dependency ',
            426: 'UpgradeRequired',
            428: 'Precondition Required',
            429: 'Too many Request',
            431: 'Request Header Fields Too Large',
            440: 'Login time out',
            444: 'No Response',
            449: 'Retry With',
            451: 'redirect',
            495: 'SSL Cirtificate Error',
            496: ' SSL Certificate Required',
            497: 'HTTP Request Sent to HTTPS Port',
            499: 'Client Closed Request',
            500: 'Internal Server Error',
            501: 'Not implemented',
            502: 'Service temporarily overloaded',
            503: 'Service Unavailable',
            504: 'Gateway Timeout',
            505: 'HTTP Version Not Supported',
            506: 'Variant Also Negotiates',
            507: 'Insufficient Storage',
            508: 'Loop Detected',
            510: 'Not Extended',
            511: 'Network Authentication Required',
            111 : 'Connection Refused'}

GET_OBJECT_COUNT='getobjectcount'

WAIT_FOR_ELEMENT_VISIBLE='waitforelementvisible'

GET_INNER_TABLE='getinnertable'

OPEN_BROWSER='openbrowser'

CLOSE_BROWSER='closebrowser'

GET_POPUP_TEXT = 'getpopuptext'

VERIFY_POPUP_TEXT = 'verifypopuptext'


NON_WEBELEMENT_KEYWORDS=['openbrowser','opennewtab','navigatetourl','getpagetitle','verifypagetitle','getcurrenturl','verifycurrenturl','closebrowser',
'switchtowindow','closesubwindows','waitforelementvisible','refresh','maximizebrowser','getcurrenturl','acceptpopup','dismisspopup',
'getpopuptext','verifypopuptext','clearcache','navigatewithauthenticate','getbrowsername']

FOUND='found'

BROWSER_NAME_MAP = {'chrome': 'Chrome', 'firefox': 'Firefox', 'internet explorer': 'Internet Explorer', 'MicrosoftEdge': 'Edge Legacy', 'msedge': 'Edge Chromium', 'Safari': 'Safari'}


"""
Accessibility testing keywords

"""


# User agent strings for all supported browsers
CHROME_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
FX_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/53.09"
IE_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
SAFARI_AGENT = "Mozilla/5.0 AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
EDGE_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43"
"""request timeout in seconds"""
REQUEST_URL_TIMEOUT=40

"""tuple of file extensions to ignore downloading entire body i.e. file"""
IGNORE_FILE_EXTENSIONS = ('.pdf','.docx','.zip','.dmg')

# check whether element is in viewport
INVIEW = """ var rect = arguments[0].getBoundingClientRect(); var windowHeight = (window.innerHeight || document.documentElement.clientHeight); var windowWidth = (window.innerWidth || document.documentElement.clientWidth); return ((rect.left >= 0) && (rect.top >= 0) && ((rect.left + rect.width) <= windowWidth) && ((rect.top + rect.height) <= windowHeight));"""

EVENTS_JS = """
var validEventList = ["blur", "change", "focus", "click", "keydown", "keypress", "keyup", "mousedown", "mousemove", "mouseup"];

function Trigger_Post(element){
    for (var event in validEventList) {
        element.dispatchEvent(new Event(validEventList[event]));
    }
}
Trigger_Post(arguments[0]);
"""

ELEMENT_LIST_JS = """
if ((arguments[0].tagName.toLowerCase() == 'input') && (arguments[0].getAttribute('role') == 'combobox')) {
    var ele_id;
    if (arguments[0].getAttribute('aria-expanded') == 'false') {
        arguments[0].click();
    }
    if (arguments[0].hasAttribute('aria-controls')) {
        ele_id = arguments[0].getAttribute('aria-controls');
    } 
    else {
        ele_id = arguments[0].getAttribute('aria-owns');
    }

    var element = document.getElementById(ele_id);
    return element.querySelectorAll('[role="option"]');
}
else {
    return arguments[0].children;
}
"""

SET_VALUE_ATTRIBUTE = """arguments[0].value=arguments[1];"""