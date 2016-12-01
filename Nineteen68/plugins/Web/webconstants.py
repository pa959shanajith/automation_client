import os

CLICK_JAVASCRIPT = """var evType; element=arguments[0]; if (document.createEvent) {     evType = 'Click executed through part-1';     var evt = document.createEvent('MouseEvents');     evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = 'Click executed through part-2';   	setTimeout(function() {     element.click();   	}, 100); } return (evType);"""

VERIFY_VISIBLE = 'NO'

TEST_RESULT_PASS = "Pass";

TEST_RESULT_FAIL = "Fail";

VALUE = 'value'

NAME = 'name'

HREF = 'href'

TEST_RESULT_TRUE = "True";

TEST_RESULT_FALSE = "False";

METHOD_INVALID='Invalid Keyword'

CHROME_DRIVER_PATH = os.getcwd()+'\chromedriver.exe'


IE_DRIVER_PATH_64 = os.getcwd()+'\IEDriverServer64.exe'

IE_DRIVER_PATH_32 = os.getcwd()+'\IEDriverServer.exe'

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

FIND_INDEX_JS="""var abc = arguments[0]; var allele = document.getElementsByTagName('*'); var result = 'OUT'; var i; for (i = 0; i < allele.length; i++) {     if (abc === allele[i]) {         break;     } } return i;"""

CUSTOM_JS="""var eleCollection = document.getElementsByTagName('*'); var startIndex = arguments[1]; var eleType = arguments[2]; eleType = eleType.toLowerCase(); var eleVisibleText = arguments[3]; var eleIndex = arguments[4]; var localIndex; localIndex = arguments[5]; var result = []; var result0 = 'null'; var result1 = 'null'; var result2 = localIndex; var result3 = eleCollection.length; var result4 = 'null'; var col = []; col['submit'] = 'button'; col['reset'] = 'button'; col['button'] = 'button'; col['file'] = 'button'; col['image'] = 'img'; col['search'] = 'text'; col['number'] = 'text'; col['url'] = 'text'; col['email'] = 'text'; col['tel'] = 'text'; col['textarea'] = 'text'; col['password'] = 'text'; var listFlag = false; var dropdown = false; if (eleType == 'listbox') {     listFlag = true; } else if (eleType == 'dropdown') {     dropdown = true; } if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('input');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })();  function stext_content(f, teleType) {     var sfirstText = '';     var stextdisplay = '';     var inlineText = '';     if (f.getAttribute('alt') != null) inlineText = inlineText.concat(f.getAttribute('alt'), ' ');     if (f.getAttribute('title') != null) inlineText = inlineText.concat(f.getAttribute('title'), ' ');     if (f.getAttribute('value') != null) inlineText = inlineText.concat(f.getAttribute('value'), ' ');     if (f.getAttribute('placeholder') != null) inlineText = inlineText.concat(f.getAttribute('placeholder'), ' ');     if (teleType == 'dropdown' || teleType == 'listbox') {         inlineText = inlineText.concat(f.textContent, ' ');     }     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     stextdisplay = inlineText.concat(stextdisplay);     return (stextdisplay); };  function findelement(feletype) {     for (i = startIndex; i < eleCollection.length; i++) {         if (sisVisible(eleCollection[i])) {             if (eleCollection[i].tagName.toLowerCase() == feletype || col[eleCollection[i].tagName.toLowerCase()] == feletype || (dropdown && eleCollection[i].tagName.toLowerCase() == 'select' && !eleCollection[i].hasAttribute('multiple')) || (listFlag && eleCollection[i].tagName.toLowerCase() == 'select' && eleCollection[i].hasAttribute('multiple'))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input') && (eleCollection[i].hasAttribute('type')) && ((eleCollection[i].getAttribute('type').toLowerCase() == feletype) || (col[eleCollection[i].getAttribute('type').toLowerCase()] == feletype))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if (eleCollection[i].tagName.toLowerCase() == 'iframe' || eleCollection[i].tagName.toLowerCase() == 'frame') {                 result0 = 'stf';                 result1 = eleCollection[i];                 result2 = localIndex;                 result3 = i + 1;                 result4 = 'null';                 break;             }         }     } }; findelement(eleType); result[0] = result0; result[1] = result1; result[2] = result2; result[3] = result3; result[4] = result4; return result;"""

CUSTOM_IFRAME_JS="""var eleCollection = document.getElementsByTagName('*'); var startIndex = arguments[1]; var eleType = arguments[2]; eleType = eleType.toLowerCase(); var eleVisibleText = arguments[3]; var eleIndex = arguments[4]; var localIndex = arguments[5]; var result = []; var result0 = 'null'; var result1 = 'null'; var result2 = localIndex; var result3 = eleCollection.length; var result4 = 'null'; var col = []; col['submit'] = 'button'; col['reset'] = 'button'; col['button'] = 'button'; col['file'] = 'button'; col['image'] = 'img'; col['search'] = 'text'; col['number'] = 'text'; col['url'] = 'text'; col['email'] = 'text'; col['tel'] = 'text'; col['textarea'] = 'text'; col['password'] = 'text'; var listFlag = false; var dropdown = false; if (eleType == 'listbox') {     listFlag = true; } else if (eleType == 'dropdown') {     dropdown = true; } if (!window.Element || !window.Element.prototype || !window.Element.prototype.hasAttribute) {     (function() {         function hasAttribute(attrName) {             return typeof this[attrName] !== 'undefined';         }         var inputs = document.getElementsByTagName('input');         for (var i = 0; i < inputs.length; i++) {             inputs[i].hasAttribute = hasAttribute;         }     }()); } var sisVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })();  function stext_content(f, teleType) {     var sfirstText = '';     var stextdisplay = '';     var inlineText = '';     if (f.getAttribute('alt') != null) inlineText = inlineText.concat(f.getAttribute('alt'), ' ');     if (f.getAttribute('title') != null) inlineText = inlineText.concat(f.getAttribute('title'), ' ');     if (f.getAttribute('value') != null) inlineText = inlineText.concat(f.getAttribute('value'), ' ');     if (f.getAttribute('placeholder') != null) inlineText = inlineText.concat(f.getAttribute('placeholder'), ' ');     if (teleType == 'dropdown' || teleType == 'listbox') {         inlineText = inlineText.concat(f.textContent, ' ');     }     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     stextdisplay = inlineText.concat(stextdisplay);     return (stextdisplay); };  function findelement(feletype) {     for (i = startIndex; i < eleCollection.length; i++) {         if (sisVisible(eleCollection[i])) {             if (eleCollection[i].tagName.toLowerCase() == feletype || col[eleCollection[i].tagName.toLowerCase()] == feletype || (dropdown && eleCollection[i].tagName.toLowerCase() == 'select' && !eleCollection[i].hasAttribute('multiple')) || (listFlag && eleCollection[i].tagName.toLowerCase() == 'select' && eleCollection[i].hasAttribute('multiple'))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             } else if ((eleCollection[i].tagName.toLowerCase() == 'input') && (eleCollection[i].hasAttribute('type')) && ((eleCollection[i].getAttribute('type').toLowerCase() == feletype) || (col[eleCollection[i].getAttribute('type').toLowerCase()] == feletype))) {                 if ((stext_content(eleCollection[i], feletype.toLowerCase()).indexOf(eleVisibleText)) >= 0) {                     if (localIndex == eleIndex) {                         result0 = 'found';                         result1 = 'null';                         result2 = localIndex;                         result3 = i + 1;                         result4 = eleCollection[i];                         break;                     }                     localIndex = localIndex + 1;                 }             }         }     } }; findelement(eleType); result[0] = result0; result[1] = result1; result[2] = result2; result[3] = result3; result[4] = result4; return result;"""



