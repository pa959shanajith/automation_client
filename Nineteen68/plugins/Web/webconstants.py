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

