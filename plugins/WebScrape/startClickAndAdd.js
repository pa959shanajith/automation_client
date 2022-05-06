
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
var css = '.AvoAssureCheckboxHighlight {outline:2px solid black!important; box-shadow: 0px 0px 0px 4px yellow !important;}',
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
    var f = event.fromElement;
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
    var f = event.toElement;
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
        var e = currentElement;
        var f = currentElement;
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
            var predicate = [];
            var parentNode;
            parentNode = e.parentNode;
            if (parentNode.shadowRoot&&parentNode.shadowRoot.toString()=='[object ShadowRoot]'&&e.assignedSlot)
                var siblings = e.assignedSlot.assignedNodes();
            else
                var siblings = parentNode.children;
            var count = 0;
            var unique = false;
            for (var i = 0; siblings && (i < siblings.length); i++) {
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
                path = '/*[local-name()="' + e.tagName.toLowerCase() + '"]' + xidx + path;
            } else if (e.tagName.toLowerCase() === 'foreignobject') {
                path = '/*[local-name()="foreignObject"]' + xidx + path;
            } else {
                path = '/' + e.tagName.toLowerCase() + xidx + path;
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
        if (parentele != 'null') {
            g = parentele;
            for (var path1 = ''; g && g.nodeType == 1; g = g.parentNode.host || g.parentNode) {
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
            newPath = String(path) + ';' + String(id) + ';' + String(rpath) + ';' + ssname + ';' + sstagname + ';' + ssclassname + ';' + coordinates + ';' + textvalue;

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
            if (browser == 3) {
                f.setAttribute('class', className + ' AvoAssure_Highlight');
                f.setAttribute('className', className + ' AvoAssure_Highlight');
                f.style.setAttribute('cssText', 'background: #fff300 !important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;');
            } else {
                f.setAttribute('class', className + ' AvoAssure_Highlight');
                f.setAttribute('style', 'background: #fff300 !important; border: 2px solid #cc3300 !important;outline: 2px solid #fff300 !important;');
            }
        }
        return false;
    }
}

function block_handler(event) {
    event = event || window.event;
    currentElement = event.toElement;
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
    height = element.offsetHeight;
    width = element.offsetWidth;
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
};