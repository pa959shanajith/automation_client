#-------------------------------------------------------------------------------
# Name:        sap_highlight
# Purpose:     Module for highlighting objects
#
#Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import win32gui
import win32process
import win32api
import time
import sap_launch_keywords
import logger
import logging
import sap_constants

import ctypes
from ctypes import c_uint, c_long
from ctypes import \
   c_uint, c_long, c_ulong

log = logging.getLogger('sap_highlight.py')

class Structure(ctypes.Structure):

        """Override the Structure class from ctypes to add printing and comparison"""

        #----------------------------------------------------------------
        def __str__(self):
            """Print out the fields of the ctypes Structure

            fields in exceptList will not be printed"""
            lines = []
            for f in self._fields_:
                name = f[0]
                lines.append("%20s\t%s"% (name, getattr(self, name)))

            return "\n".join(lines)

        #----------------------------------------------------------------
        def __eq__(self, other_struct):
            """Return True if the two structures have the same coordinates"""
            if isinstance(other_struct, ctypes.Structure):
                try:
                    # pretend they are two structures - check that they both
                    # have the same value for all fields
                    are_equal = True
                    for field in self._fields_:
                        name = field[0]
                        if getattr(self, name) != getattr(other_struct, name):
                            are_equal = False
                            break

                    return are_equal

                except AttributeError:
                    return False

            if isinstance(other_struct, (list, tuple)):
                # Now try to see if we have been passed in a list or tuple
                try:
                    are_equal = True
                    for i, field in enumerate(self._fields_):
                        name = field[0]
                        if getattr(self, name) != other_struct[i]:
                            are_equal = False
                            break
                    return are_equal

                except Exception:
                    return False

            return False

class LOGBRUSH(Structure):
    _fields_ = [
        # C:/PROGRA~1/MIAF9D~1/VC98/Include/wingdi.h 1025
        ('lbStyle', c_uint),
        ('lbColor', c_ulong),
        ('lbHatch', c_long),
    ]

class highLight():
    def highlight_element(self, elem):
        """
        imput : element id
        output : highlights the element
        Working : 1. Brings the window to foreground
                  2. draws an outline around the element to be highlighted
        """
        try:
            launch = sap_launch_keywords.Launch_Keywords()
            ses, window = launch.getSessWindow()
            try:
                i = elem.index("/")
                elemId = window.Id + elem[i:]
                screen_name = elem[:i]
            except:
                elemId = window.Id
                screen_name = elem
            elem_to_highlight = ses.FindById(elemId)
            toplist, winlist = [], []
            def enum_cb(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
            win32gui.EnumWindows(enum_cb, toplist)
            app = [(hwnd, title) for hwnd, title in winlist if screen_name == title]
            app = app[0]
            hwnd = app[0]
            try:
                foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                appThread = win32api.GetCurrentThreadId()
                if ( foreThread != appThread ):
                    win32process.AttachThreadInput(foreThread[0], appThread, True)
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.ShowWindow(hwnd,5)
                    win32process.AttachThreadInput(foreThread[0], appThread, False)
                else:
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.ShowWindow(hwnd,3)
                time.sleep(1)
                if (elem_to_highlight): self.draw_outline(elem_to_highlight)
                else:
                    log.error( sap_constants.ELELMENT_NOT_FOUND_HIGHLIGHT )
                    logger.print_on_console( sap_constants.ELELMENT_NOT_FOUND_HIGHLIGHT )
            except Exception as e:
                print('some error',e)
                pass
        except Exception as e:
            log.error(e)
            log.error( sap_constants.ERROR_HIGHLIGHT )
            logger.print_on_console( sap_constants.ERROR_HIGHLIGHT )

    def draw_outline(self, elem):
        """
        Draw an outline around the window.

        * **colour** can be either an integer or one of 'red', 'green', 'blue'
          (default 'green')
        * **thickness** thickness of rectangle (default 2)
        * **fill** how to fill in the rectangle (default BS_NULL)
        * **rect** the coordinates of the rectangle to draw (defaults to
          the rectangle of the control)
        """
        rect = None
        colour='red'
        thickness = 4
        fill = 1 #default BS_NULL
        colours = {"green": 0x00ff00,"blue": 0xff0000,"red": 0x0000ff,'yellow':0x00aaff}

        # if it's a known colour
        if colour in colours : colour = colours[colour]

        # if rect is None:
        h=elem.__getattr__("Height") if hasattr(elem, "Height") else elem["height"]
        w=elem.__getattr__("Width") if hasattr(elem, "Width") else elem["width"]
        l=elem.__getattr__("ScreenLeft") if hasattr(elem, "ScreenLeft") else elem["left"]
        t=elem.__getattr__("ScreenTop") if hasattr(elem, "ScreenTop") else elem["top"]
        r=l+w
        b=t+h
        rect={
            'left' : l,
            'top' : t,
            'right' : r,
            'bottom' : b
        }

        # create the pen(outline)
        pen_handle = ctypes.windll.gdi32.CreatePen(0, thickness, colour)

        # create the brush (inside)
        brush = LOGBRUSH()
        brush.lbStyle = fill
        brush.lbHatch = 5 # Variable c_int
        brush_handle = ctypes.windll.gdi32.CreateBrushIndirect(ctypes.byref(brush))

        # get the Device Context
        dc = ctypes.windll.gdi32.CreateDCW("DISPLAY", None, None, None )

        # push our objects into it
        ctypes.windll.gdi32.SelectObject(dc, brush_handle)
        ctypes.windll.gdi32.SelectObject(dc, pen_handle)

        # draw the rectangle to the DC
        ctypes.windll.gdi32.Rectangle( dc, rect['left'], rect['top'], rect['right'], rect['bottom'] )
        time.sleep(0.5)

        # Delete the brush and pen we created
        ctypes.windll.gdi32.DeleteObject(brush_handle)
        ctypes.windll.gdi32.DeleteObject(pen_handle)

        # delete the Display context that we created
        ctypes.windll.gdi32.DeleteDC(dc)