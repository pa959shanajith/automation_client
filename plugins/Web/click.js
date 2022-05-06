var evType;
element = arguments[0];

if (document.createEvent && element.getRootNode().toString() != '[object ShadowRoot]') {
    evType = 'Click executed through part-1';
    var evt = document.createEvent('MouseEvents');
    evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    try {
        setTimeout(function () {
            element.dispatchEvent(evt)
        }, 100);
    } catch (error) {
        return false;
    }
} else {
    evType = 'Click executed through part-2';
    try {
        setTimeout(function () {
            element.click();
        }, 100);
    } catch (error) {
        return false;
    }
}

return true;