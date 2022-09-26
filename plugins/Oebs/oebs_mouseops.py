from ctypes import *
from ctypes.wintypes import *
from time import sleep
import win32ui
import win32gui
from oebs_constants import *


# START SENDINPUT TYPE DECLARATIONS
PUL = POINTER(c_ulong)

class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
             ("wScan", c_ushort),
             ("dwFlags", c_ulong),
             ("time", c_ulong),
             ("dwExtraInfo", PUL)]

class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
             ("wParamL", c_short),
             ("wParamH", c_ushort)]

class MouseInput(Structure):
    _fields_ = [("dx", c_long),
             ("dy", c_long),
             ("mouseData", c_ulong),
             ("dwFlags", c_ulong),
             ("time",c_ulong),
             ("dwExtraInfo", PUL)]

class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
              ("mi", MouseInput),
              ("hi", HardwareInput)]

class Input(Structure):
    _fields_ = [("type", c_ulong),
             ("ii", Input_I)]

class POINT(Structure):
    _fields_ = [("x", c_ulong),
             ("y", c_ulong)]
# END SENDINPUT TYPE DECLARATIONS

MIDDLEDOWN = 0x00000020
MIDDLEUP   = 0x00000040
MOVE       = 0x00000001
ABSOLUTE   = 0x00008000
RIGHTDOWN  = 0x00000008
RIGHTUP    = 0x00000010

FInputs = Input * 2
extra = c_ulong(0)

click = Input_I()
click.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
doubleClick = Input_I()
doubleClick.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
release = Input_I()
release.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))

x = FInputs( (0, click), (0, release) )
#user32.SendInput(2, pointer(x), sizeof(x[0])) CLICK & RELEASE

x4 = FInputs( (0, doubleClick), (0, release) )
#user32.SendInput(2, pointer(x), sizeof(x[0])) DOUBLECLICK & RELEASE

x2 = FInputs( (0, click) )
#user32.SendInput(2, pointer(x2), sizeof(x2[0])) CLICK & HOLD

x3 = FInputs( (0, release) )
#user32.SendInput(2, pointer(x3), sizeof(x3[0])) RELEASE HOLD

def move(x,y):
    windll.user32.SetCursorPos(x,y)

def getpos():
    global pt
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y

def slide(a,b,speed=0):
    while True:
        if speed == 'slow':
            sleep(0.005)
            Tspeed = 2
        if speed == 'fast':
            sleep(0.001)
            Tspeed = 5
        if speed == 0:
            sleep(0.001)
            Tspeed = 3

        x = getpos()[0]
        y = getpos()[1]
        if abs(x-a) < 5:
            if abs(y-b) < 5:
                break

        if a < x:
            x -= Tspeed
        if a > x:
            x += Tspeed
        if b < y:
            y -= Tspeed
        if b > y:
            y += Tspeed
        move(x,y)


def click():
    windll.user32.SendInput(2,pointer(x),sizeof(x[0]))

def doubleClick():
    windll.user32.SendInput(2,pointer(x4),sizeof(x4[0]))
    windll.user32.SendInput(2,pointer(x4),sizeof(x4[0]))

def hold():
    windll.user32.SendInput(2, pointer(x2), sizeof(x2[0]))

def release():
    windll.user32.SendInput(2, pointer(x3), sizeof(x3[0]))


def rightclick():
    windll.user32.mouse_event(RIGHTDOWN,0,0,0,0)
    windll.user32.mouse_event(RIGHTUP,0,0,0,0)

def righthold():
    windll.user32.mouse_event(RIGHTDOWN,0,0,0,0)

def rightrelease():
    windll.user32.mouse_event(RIGHTUP,0,0,0,0)


def middleclick():
    windll.user32.mouse_event(MIDDLEDOWN,0,0,0,0)
    windll.user32.mouse_event(MIDDLEUP,0,0,0,0)

def middlehold():
    windll.user32.mouse_event(MIDDLEDOWN,0,0,0,0)

def middlerelease():
    windll.user32.mouse_event(MIDDLEUP,0,0,0,0)

#Method to perform mouse operation
def MouseOperation(action, coord_x, coord_y):
    if (action == "click"):
        move(coord_x, coord_y)
        click()
        return True
    elif (action == "doubleClick"):
        move(coord_x, coord_y)
        doubleClick()
        return True
    elif (action == "hold"):
        move(coord_x, coord_y)
        hold()
        return True
    elif (action == "release"):
        # move(coord_x, coord_y)
        release()
        return True
    elif (action == "rightclick"):
        move(coord_x, coord_y)
        rightclick()
        return True
    elif (action == "righthold"):
        move(coord_x, coord_y)
        righthold()
        return True
    elif (action == "rightrelease"):
        move(coord_x, coord_y)
        rightrelease()
        return True
    elif (action == "middleclick"):
        move(coord_x, coord_y)
        middleclick()
        return True
    elif (action == "middlehold"):
        move(coord_x, coord_y)
        middlehold()
        return True
    elif (action == "middlerelease"):
        move(coord_x, coord_y)
        middlerelease()
        return True
    elif (action == "move"):
        move(coord_x, coord_y)
        return True
    elif (action == "getpos"):
        # returns x and y coordinates in a tuple
        return getpos()
    elif (action == "slide"):
        slide(coord_x,coord_y)
        return True
    else:
        return MSG_INVALID_ACTION_INFO

#provides the cursor information
def GetCursorInfo(info):
    cursorinfo=win32gui.GetCursorInfo()
    if (info == 'flag'):
        return cursorinfo[0]
    elif (info == 'state'):
        return cursorinfo[1]
    elif (info == 'coords'):
        return cursorinfo[2]
    else:
        return MSG_INVALID_ACTION_INFO

