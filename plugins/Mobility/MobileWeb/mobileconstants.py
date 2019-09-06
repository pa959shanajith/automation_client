import os

GET_XPATH_JS="""function getElementXPath(elt) {var path = "";for (; elt && elt.nodeType == 1; elt = elt.parentNode){idx = getElementIdx(elt);xname = elt.tagName;if (idx >= 1){xname += "[" + idx + "]";}path = "/" + xname + path;}return path;}function getElementIdx(elt){var count = 1;for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){if(sib.nodeType == 1 && sib.tagName == elt.tagName){count++;}}return count;}return getElementXPath(arguments[0]).toLowerCase();"""

CLICK_JAVASCRIPT = """var evType; element=arguments[0]; if (document.createEvent) {     evType = 'Click executed through part-1';     var evt = document.createEvent('MouseEvents');     evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = 'Click executed through part-2';   	setTimeout(function() {     element.click();   	}, 100); } return (evType);"""

GET_CELL_JS="""var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };"""


VERIFY_VISIBLE = 'NO'

TEST_RESULT_PASS = "Pass";

TEST_RESULT_FAIL = "Fail";

VALUE = 'value'

NAME = 'name'

HREF = 'href'

TEST_RESULT_TRUE = "True";

TEST_RESULT_FALSE = "False";

METHOD_INVALID='Invalid Keyword'

CHROME_DRIVER_PATH = 'D:\chromedriver.exe'


IE_DRIVER_PATH_64 = 'D:\IEDriverServer64.exe'

IE_DRIVER_PATH_32 = os.getcwd()+'\IEDriverServer.exe'

PHANTOM_DRIVER_PATH = os.getcwd()+'\phantomjs.exe'

SET_TEXT_SCRIPT="""arguments[0].value=arguments[1]"""

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

CUSTOM_JS="""var eleCollection = document.getElementsByTagName('*'); var startIndex = arguments[1]; var eleType = arguments[2]; eleType = eleType.toLowerCase(); var eleVisibleText = arguments[3]; var eleIndex = arguments[4]; var localIndex; localIndex = arguments[5]; var result = []; var result0 = 'null'; var result1 = 'null'; var result2 = localIndex; var result3 = eleCollection.length; var result4 = 'null'; var col = []; col['submit'] = 'button'; col['reset'] = 'button'; col['button'] = 'button'; col['file'] = 'button'; col['image'] = 'img'; col['search'] = 'text'; col['number'] = 'text'; col['url'] = 'text'; col['email'] = 'text'; col['tel'] = 'text'; col['textarea'] = 'text'; col['password'] = 'text'; var listFlag = false; var dropdown = false; if (eleType == 'listbox') {     listFlag = true; } else if (eleType == 'dropdown') {     dropdown = true; } if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('input');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })();  function stext_content(f, teleType) {     var sfirstText = '';     var stextdisplay = '';     var inlineText = '';     if (f.getAttribute('alt') != null) inlineText = inlineText.concat(f.getAttribute('alt'), ' ');     if (f.getAttribute('title') != null) inlineText = inlineText.concat(f.getAttribute('title'), ' ');     if (f.getAttribute('value') != null) inlineText = inlineText.concat(f.getAttribute('value'), ' ');     if (f.getAttribute('placeholder') != null) inlineText = inlineText.concat(f.getAttribute('placeholder'), ' ');     if (teleType == 'dropdown' || teleType == 'listbox') {         inlineText = inlineText.concat(f.textContent, ' ');     }     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     stextdisplay = inlineText.concat(stextdisplay);     return (stextdisplay); };  function findelement(feletype) {     for (i = startIndex; i < eleCollection.length; i++) {         if (sisVisible(eleCollection[i])) {             if (eleCollection[i].tagName.toLowerCase() == feletype || col[eleCollection[i].tagName.toLowerCase()] == feletype || (dropdown && eleCollection[i].tagName.toLowerCase() == 'select' && !eleCollection[i].hasAttribute('multiple')) || (listFlag && eleCollection[i].tagName.toLowerCase() == 'select' && eleCollection[i].hasAttribute('multiple'))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input') && (eleCollection[i].hasAttribute('type')) && ((eleCollection[i].getAttribute('type').toLowerCase() == feletype) || (col[eleCollection[i].getAttribute('type').toLowerCase()] == feletype))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if (eleCollection[i].tagName.toLowerCase() == 'iframe' || eleCollection[i].tagName.toLowerCase() == 'frame') {                 result0 = 'stf';                 result1 = eleCollection[i];                 result2 = localIndex;                 result3 = i + 1;                 result4 = 'null';                 break;             }         }     } }; findelement(eleType); result[0] = result0; result[1] = result1; result[2] = result2; result[3] = result3; result[4] = result4; return result;"""

CUSTOM_IFRAME_JS="""var eleCollection = document.getElementsByTagName('*'); var startIndex = arguments[1]; var eleType = arguments[2]; eleType = eleType.toLowerCase(); var eleVisibleText = arguments[3]; var eleIndex = arguments[4]; var localIndex = arguments[5]; var result = []; var result0 = 'null'; var result1 = 'null'; var result2 = localIndex; var result3 = eleCollection.length; var result4 = 'null'; var col = []; col['submit'] = 'button'; col['reset'] = 'button'; col['button'] = 'button'; col['file'] = 'button'; col['image'] = 'img'; col['search'] = 'text'; col['number'] = 'text'; col['url'] = 'text'; col['email'] = 'text'; col['tel'] = 'text'; col['textarea'] = 'text'; col['password'] = 'text'; var listFlag = false; var dropdown = false; if (eleType == 'listbox') {     listFlag = true; } else if (eleType == 'dropdown') {     dropdown = true; } if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('input');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })();  function stext_content(f, teleType) {     var sfirstText = '';     var stextdisplay = '';     var inlineText = '';     if (f.getAttribute('alt') != null) inlineText = inlineText.concat(f.getAttribute('alt'), ' ');     if (f.getAttribute('title') != null) inlineText = inlineText.concat(f.getAttribute('title'), ' ');     if (f.getAttribute('value') != null) inlineText = inlineText.concat(f.getAttribute('value'), ' ');     if (f.getAttribute('placeholder') != null) inlineText = inlineText.concat(f.getAttribute('placeholder'), ' ');     if (teleType == 'dropdown' || teleType == 'listbox') {         inlineText = inlineText.concat(f.textContent, ' ');     }     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     stextdisplay = inlineText.concat(stextdisplay);     return (stextdisplay); };  function findelement(feletype) {     for (i = startIndex; i < eleCollection.length; i++) {         if (sisVisible(eleCollection[i])) {             if (eleCollection[i].tagName.toLowerCase() == feletype || col[eleCollection[i].tagName.toLowerCase()] == feletype || (dropdown && eleCollection[i].tagName.toLowerCase() == 'select' && !eleCollection[i].hasAttribute('multiple')) || (listFlag && eleCollection[i].tagName.toLowerCase() == 'select' && eleCollection[i].hasAttribute('multiple'))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input') && (eleCollection[i].hasAttribute('type')) && ((eleCollection[i].getAttribute('type').toLowerCase() == feletype) || (col[eleCollection[i].getAttribute('type').toLowerCase()] == feletype))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             }         }     } }; findelement(eleType); result[0] = result0; result[1] = result1; result[2] = result2; result[3] = result3; result[4] = result4; return result;"""

GET_OBJECT_COUNT_JS="""var temp = getCount(arguments[0], arguments[1], arguments[2], arguments[3]); return temp;  function getCount(counter, user_input, index, flag) {     var i;     var result = [];     var req_eles = document.getElementsByTagName("*");     var max = req_eles.length;     console.log(max);     var sisVisible = (function() {         function inside(schild, sparent) {             while (schild) {                 if (schild === sparent) return true;                 schild = schild.parentNode;             }             return false;         };         return function(selem) {             if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;             var srect = selem.getBoundingClientRect();             if (window.getComputedStyle || selem.currentStyle) {                 var sel = selem,                     scomp = null;                 while (sel) {                     if (sel === document) {                         break;                     } else if (!sel.parentNode) return false;                     scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                     if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                     sel = sel.parentNode;                 }             }             return true;         }     })();     if (max > 0) {         if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {             (function() {                 function hasAttribute(attrName) {                     return typeof this[attrName] !== 'undefined';                 }                 var inputs = document.getElementsByTagName('input');                 for (var i = 0; i < inputs.length; i++) {                     inputs[i].hasAttribute = hasAttribute;                 }             }());         }         for (i = index; i < max; i++) {             var tagname = req_eles[i].tagName;             var type = req_eles[i].type;             console.log(tagname, type, user_input, i,sisVisible(req_eles[i]));              /*if (found == 1) {*/             if (sisVisible(req_eles[i])) {                 if ((tagname == "IFRAME") || (tagname == "FRAME")) {                     result[1] = req_eles[i];                     break;                 } else if (req_eles[i].hasAttribute("type")) {                     if (user_input == "button") {                         if ((type == "submit") || (type == "reset") || (type == "file")) {                             counter = counter + 1;                         }                     } else if (user_input == "text") {                         if ((type == user_input) || (type == "password") || (type == "number") || (type == "url") || (type == "tel") || (type == "user_inputarea") || (type == "search")) {                             counter = counter + 1;                         }                     } else if (user_input == "img") {                         if ((type == "image") || (tagname == "IMAGE")) {                             counter = counter + 1;                         }                     } else {                         if ((type == user_input)) {                             counter = counter + 1;                         }                     }                 } else if (tagname == user_input.toUpperCase()) {                     if ((user_input.toUpperCase() == "SELECT") && (flag == 1)) {                         if (req_eles[i].multiple == true) {                             counter = counter + 1;                         }                     } else {                         counter = counter + 1;                     }                 }             } /*} else if (found == 0) {                 if ((tagname == "IFRAME") || (tagname == "FRAME")) {                     result[1] = req_eles[i];                     break;                 }             }*/         }     }     if (i >= max) {         result[3] = "done";     }     result[0] = counter;     result[2] = i;     console.log(result);     return result; }; """

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
            511: 'Network Authentication Required'}

GET_OBJECT_COUNT='getobjectcount'

WAIT_FOR_ELEMENT_VISIBLE='waitforelementvisible'

GET_INNER_TABLE='getinnertable'

OPEN_BROWSER='openbrowser'

OPEN_NEW_BROWSER='opennewbrowser'

CLOSE_BROWSER='closebrowser'


NON_WEBELEMENT_KEYWORDS=['openbrowser','opennewbrowser','navigatetourl','getpagetitle','verifypagetitle','getcurrenturl','verifycurrenturl','closebrowser',
'switchtowindow','closesubwindows','verifytextexists','waitforelementvisible','refresh','actionkey','maximizebrowser','getcurrenturl','acceptpopup','dismisspopup',
'getpopuptext','verifypopuptext','clearcache','navigatewithauthenticate']

FOUND='found'

