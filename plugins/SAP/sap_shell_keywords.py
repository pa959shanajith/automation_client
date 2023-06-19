#-------------------------------------------------------------------------------
# Name:        SAP_Shell_keywords
# Purpose:     Handling SAP-Shell elements
#
# Author:      anas.ahmed
#
# Created:     28-01-2020
# Copyright:   (c) anas.ahmed 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_constants
from constants import *
import logger
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import logging
import win32api, win32con
log = logging.getLogger("sap_shell_keywords.py")

class Shell_Keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

    def selectContextMenuByText(self, sap_id, input_val, *args):
        """
        Input : Text value of the context menu item
        Output : Select the context menu item
        Note: context menu should be displayed(right click on the element) inorder to select menu item
              other mentioned context menu methods(elem.ShowContextMenu(), elem.SelectContextMenuItem('<Fcode>'),
              elem.SelectContextMenuItemByPosition('Pos')) exists , but functionality does not work correctly for current win32
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    h=elem.__getattr__("Height")
                    w=elem.__getattr__("Width")
                    l=elem.__getattr__("ScreenLeft")
                    t=elem.__getattr__("ScreenTop")
                    #Right click on the shell object
                    def click(x,y):
                        win32api.SetCursorPos((x,y))
                        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
                    click (int(l + w / 2),int(t + h /2))
                    #select the context menu item by text
                    elem.SelectContextMenuItemByText(str(input_val[0])) # right click must be performed to get context menu
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    log.debug( "Selected Context menu item : " + str(input_val[0]) )
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in selectContextMenuByText' )
        return status, result, value, err_msg

"""
Other context menu related functions
elem.ShowContextMenu()
elem.SelectContextMenuItem('<Fcode>')
elem.SelectContextMenuItemByPosition('Pos')
"""