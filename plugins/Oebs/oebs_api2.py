
startTime=0
desktopObject=None
foregroundObject=None
focusObject=None
focusAncestors=[]
focusDifferenceLevel=None
mouseObject=None
mouseOldX=None
mouseOldY=None
navigatorObject=None
reviewPosition=None
reviewPositionObj=None
lastProgressValue=0
appArgs=None
appArgsExtra=None
settingsRing = None
speechDictionaryProcessing=True
exitCode=0


def getFocusObject():
    global focusObject
    return focusObject


def setFocusObject(obj):
    global focusObject
    focusObject = obj