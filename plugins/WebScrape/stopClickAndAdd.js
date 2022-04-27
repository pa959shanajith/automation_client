window.tastopflag = "true";
document.getElementsByTagName('HTML')[0].click();
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
if (document.getElementById('AvoAssureCheckboxHighlight') || document.getElementById('AvoAssureBorderHighlight')) {
    styleTag = document.getElementById('AvoAssureCheckboxHighlight');
    styleTagH = document.getElementById('AvoAssureBorderHighlight');
    head = document.head || document.getElementsByTagName('head')[0] || document.getElementById('AvoAssure_head');
    head.removeChild(styleTag);
    head.removeChild(styleTagH);
    var a = getElementsByClassName('AvoAssure_Highlight');
    for (var i = 0; i < a.length; i++) {
        a[i].removeAttribute('style');
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
    debugger;
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
return (temp);