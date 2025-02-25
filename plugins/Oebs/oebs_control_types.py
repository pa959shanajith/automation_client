#controlTypes.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2016 NV Access Limited, Babbage B.V.

ROLE_UNKNOWN=0
ROLE_WINDOW=1
ROLE_TITLEBAR=2
ROLE_PANE=3
ROLE_DIALOG=4
ROLE_CHECKBOX=5
ROLE_RADIOBUTTON=6
ROLE_STATICTEXT=7
ROLE_EDITABLETEXT=8
ROLE_BUTTON=9
ROLE_MENUBAR=10
ROLE_MENUITEM=11
ROLE_POPUPMENU=12
ROLE_COMBOBOX=13
ROLE_LIST=14
ROLE_LISTITEM=15
ROLE_GRAPHIC=16
ROLE_HELPBALLOON=17
ROLE_TOOLTIP=18
ROLE_LINK=19
ROLE_TREEVIEW=20
ROLE_TREEVIEWITEM=21
ROLE_TAB=22
ROLE_TABCONTROL=23
ROLE_SLIDER=24
ROLE_PROGRESSBAR=25
ROLE_SCROLLBAR=26
ROLE_STATUSBAR=27
ROLE_TABLE=28
ROLE_TABLECELL=29
ROLE_TABLECOLUMN=30
ROLE_TABLEROW=31
ROLE_TABLECOLUMNHEADER=32
ROLE_TABLEROWHEADER=33
ROLE_FRAME=34
ROLE_TOOLBAR=35
ROLE_DROPDOWNBUTTON=36
ROLE_CLOCK=37
ROLE_SEPARATOR=38
ROLE_FORM=39
ROLE_HEADING=40
ROLE_HEADING1=41
ROLE_HEADING2=42
ROLE_HEADING3=43
ROLE_HEADING4=44
ROLE_HEADING5=45
ROLE_HEADING6=46
ROLE_PARAGRAPH=47
ROLE_BLOCKQUOTE=48
ROLE_TABLEHEADER=49
ROLE_TABLEBODY=50
ROLE_TABLEFOOTER=51
ROLE_DOCUMENT=52
ROLE_ANIMATION=53
ROLE_APPLICATION=54
ROLE_BOX=55
ROLE_GROUPING=56
ROLE_PROPERTYPAGE=57
ROLE_CANVAS=58
ROLE_CAPTION=59
ROLE_CHECKMENUITEM=60
ROLE_DATEEDITOR=61
ROLE_ICON=62
ROLE_DIRECTORYPANE=63
ROLE_EMBEDDEDOBJECT=64
ROLE_ENDNOTE=65
ROLE_FOOTER=66
ROLE_FOOTNOTE=67
ROLE_GLASSPANE=69
ROLE_HEADER=70
ROLE_IMAGEMAP=71
ROLE_INPUTWINDOW=72
ROLE_LABEL=73
ROLE_NOTE=74
ROLE_PAGE=75
ROLE_RADIOMENUITEM=76
ROLE_LAYEREDPANE=77
ROLE_REDUNDANTOBJECT=78
ROLE_ROOTPANE=79
ROLE_EDITBAR=80
ROLE_TERMINAL=82
ROLE_RICHEDIT=83
ROLE_RULER=84
ROLE_SCROLLPANE=85
ROLE_SECTION=86
ROLE_SHAPE=87
ROLE_SPLITPANE=88
ROLE_VIEWPORT=89
ROLE_TEAROFFMENU=90
ROLE_TEXTFRAME=91
ROLE_TOGGLEBUTTON=92
ROLE_BORDER=93
ROLE_CARET=94
ROLE_CHARACTER=95
ROLE_CHART=96
ROLE_CURSOR=97
ROLE_DIAGRAM=98
ROLE_DIAL=99
ROLE_DROPLIST=100
ROLE_SPLITBUTTON=101
ROLE_MENUBUTTON=102
ROLE_DROPDOWNBUTTONGRID=103
ROLE_MATH=104
ROLE_EQUATION=ROLE_MATH # Deprecated; for backwards compatibility.
ROLE_GRIP=105
ROLE_HOTKEYFIELD=106
ROLE_INDICATOR=107
ROLE_SPINBUTTON=108
ROLE_SOUND=109
ROLE_WHITESPACE=110
ROLE_TREEVIEWBUTTON=111
ROLE_IPADDRESS=112
ROLE_DESKTOPICON=113
ROLE_ALERT=114
ROLE_INTERNALFRAME=115
ROLE_DESKTOPPANE=116
ROLE_OPTIONPANE=117
ROLE_COLORCHOOSER=118
ROLE_FILECHOOSER=119
ROLE_FILLER=120
ROLE_MENU=121
ROLE_PANEL=122
ROLE_PASSWORDEDIT=123
ROLE_FONTCHOOSER=124
ROLE_LINE=125
ROLE_FONTNAME=126
ROLE_FONTSIZE=127
ROLE_BOLD=128
ROLE_ITALIC=129
ROLE_UNDERLINE=130
ROLE_FGCOLOR=131
ROLE_BGCOLOR=132
ROLE_SUPERSCRIPT=133
ROLE_SUBSCRIPT=134
ROLE_STYLE=135
ROLE_INDENT=136
ROLE_ALIGNMENT=137
ROLE_ALERT=138
ROLE_DATAGRID=139
ROLE_DATAITEM=140
ROLE_HEADERITEM=141
ROLE_THUMB=142
ROLE_CALENDAR=143
ROLE_VIDEO=144
ROLE_AUDIO=145
ROLE_CHARTELEMENT=146
ROLE_DELETED_CONTENT=147
ROLE_INSERTED_CONTENT=148

STATE_UNAVAILABLE=0X1
STATE_FOCUSED=0X2
STATE_SELECTED=0X4
STATE_BUSY=0X8
STATE_PRESSED=0X10
STATE_CHECKED=0X20
STATE_HALFCHECKED=0X40
STATE_READONLY=0X80
STATE_EXPANDED=0X100
STATE_COLLAPSED=0X200
STATE_INVISIBLE=0X400
STATE_VISITED=0X800
STATE_LINKED=0X1000
STATE_HASPOPUP=0X2000
STATE_PROTECTED=0X4000
STATE_REQUIRED=0X8000
STATE_DEFUNCT=0X10000
STATE_INVALID_ENTRY=0X20000
STATE_MODAL=0X40000
STATE_AUTOCOMPLETE=0x80000
STATE_MULTILINE=0X100000
STATE_ICONIFIED=0x200000
STATE_OFFSCREEN=0x400000
STATE_SELECTABLE=0x800000
STATE_FOCUSABLE=0x1000000
STATE_CLICKABLE=0x2000000
STATE_EDITABLE=0x4000000
STATE_CHECKABLE=0x8000000
STATE_DRAGGABLE=0x10000000
STATE_DRAGGING=0x20000000
STATE_DROPTARGET=0x40000000
STATE_SORTED=0x80000000
STATE_SORTED_ASCENDING=0x100000000
STATE_SORTED_DESCENDING=0x200000000
STATES_SORTED=frozenset([STATE_SORTED,STATE_SORTED_ASCENDING,STATE_SORTED_DESCENDING])
STATE_HASLONGDESC=0x400000000
STATE_PINNED=0x800000000
STATE_HASFORMULA=0x1000000000 #Mostly for spreadsheets
STATE_HASCOMMENT=0X2000000000
STATE_OBSCURED=0x4000000000
STATE_CROPPED=0x8000000000
STATE_OVERFLOWING=0x10000000000
STATE_UNLOCKED=0x20000000000

#Originally part of oebs_key_labels.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2016 NV Access Limited, Aleksey Sadovoy, Babbage B.v.

localizedKeyLabels = {
	# Translators: This is the name of the back key found on multimedia keyboards for controlling the web-browser.
	'browserback': ("back"),
	# Translators: This is the name of the forward key found on multimedia keyboards for controlling the web-browser.
	'browserforward': ("forward"),
	# Translators: This is the name of the refresh key found on multimedia keyboards for controlling the web-browser.
	'browserrefresh': ("refresh"),
	# Translators: This is the name of the stop key found on multimedia keyboards for controlling the web-browser.
	'browserstop': ("browser stop"),
	# Translators: This is the name of the back key found on multimedia keyboards to goto the search page of the web-browser.
	'browsersearch': ("search page"),
	# Translators: This is the name of the favorites key found on multimedia keyboards to open favorites in the web-browser.
	'browserfavorites': ("favorites"),
	# Translators: This is the name of the home key found on multimedia keyboards to goto the home page in the web-browser.
	'browserhome': ("home page"),
	# Translators: This is the name of the mute key found on multimedia keyboards to control playback volume.
	'volumemute': ("mute"),
	# Translators: This is the name of the volume down key found on multimedia keyboards to reduce playback volume.
	'volumedown': ("volume down"),
	# Translators: This is the name of the volume up key found on multimedia keyboards to increase playback volume.
	'volumeup': ("volume up"),
	# Translators: This is the name of the next track key found on multimedia keyboards to skip to next track in the mediaplayer.
	'medianexttrack': ("next track"),
	# Translators: This is the name of the next track key found on multimedia keyboards to skip to next track in the mediaplayer.
	'mediaprevtrack': ("previous track"),
	# Translators: This is the name of the stop key found on multimedia keyboards to stop the current playing track in the mediaplayer.
	'mediastop': ("stop"),
	# Translators: This is the name of the play/pause key found on multimedia keyboards to play/pause the current playing track in the mediaplayer.
	'mediaplaypause': ("play pause"),
	# Translators: This is the name of the launch email key found on multimedia keyboards to open an email client.
	'launchmail': ("email"),
	# Translators: This is the name of the launch mediaplayer key found on multimedia keyboards to launch the mediaplayer.
	'launchmediaplayer': ("media player"),
	# Translators: This is the name of the launch custom application 1 key found on multimedia keyboards to launch a user-defined application.
	'launchapp1': ("custom application 1"),
	# Translators: This is the name of the launch custom application 2 key found on multimedia keyboards to launch a user-defined application.
	'launchapp2': ("custom application 2"),
	# Translators: This is the name of a key on the keyboard.
	'backspace': ("backspace"),
	# Translators: This is the name of a key on the keyboard.
	'capslock': ("caps lock"),
	# Translators: This is the name of a key on the keyboard.
	'control': ("ctrl"),
	# Translators: This is the name of a key on the keyboard.
	'alt': ("alt"),
	# Translators: This is the name of a key on the keyboard.
	'shift': ("shift"),
	# Translators: This is the name of a key on the keyboard.
	'windows': ("windows"),
	# Translators: This is the name of a key on the keyboard.
	'enter': ("enter"),
	# Translators: This is the name of a key on the keyboard.
	'numpadenter': ("numpad enter"),
	# Translators: This is the name of a key on the keyboard.
	'escape': ("escape"),
	# Translators: This is the name of a key on the keyboard.
	'space': ("space"),
	# Translators: This is the name of a key on the keyboard.
	'pageup': ("page up"),
	# Translators: This is the name of a key on the keyboard.
	'pagedown': ("page down"),
	# Translators: This is the name of a key on the keyboard.
	'end': ("end"),
	# Translators: This is the name of a key on the keyboard.
	'home': ("home"),
	# Translators: This is the name of a key on the keyboard.
	'delete': ("delete"),
	# Translators: This is the name of a key on the keyboard.
	'numpaddelete': ("numpad delete"),
	# Translators: This is the name of a key on the keyboard.
	'leftarrow': ("left arrow"),
	# Translators: This is the name of a key on the keyboard.
	'rightarrow': ("right arrow"),
	# Translators: This is the name of a key on the keyboard.
	'uparrow': ("up arrow"),
	# Translators: This is the name of a key on the keyboard.
	'downarrow': ("down arrow"),
	# Translators: This is the name of a key on the keyboard.
	'applications': ("applications"),
	# Translators: This is the name of a key on the keyboard.
	'numlock': ("num lock"),
	# Translators: This is the name of a key on the keyboard.
	'printscreen': ("print screen"),
	# Translators: This is the name of a key on the keyboard.
	'scrolllock': ("scroll lock"),
	# Translators: This is the name of a key on the keyboard.
	'numpad4': ("numpad 4"),
	# Translators: This is the name of a key on the keyboard.
	'numpad6': ("numpad 6"),
	# Translators: This is the name of a key on the keyboard.
	'numpad8': ("numpad 8"),
	# Translators: This is the name of a key on the keyboard.
	'numpad2': ("numpad 2"),
	# Translators: This is the name of a key on the keyboard.
	'numpad9': ("numpad 9"),
	# Translators: This is the name of a key on the keyboard.
	'numpad3': ("numpad 3"),
	# Translators: This is the name of a key on the keyboard.
	'numpad1': ("numpad 1"),
	# Translators: This is the name of a key on the keyboard.
	'numpad7': ("numpad 7"),
	# Translators: This is the name of a key on the keyboard.
	'numpad5': ("numpad 5"),
	# Translators: This is the name of a key on the keyboard.
	'numpaddivide': ("numpad divide"),
	# Translators: This is the name of a key on the keyboard.
	'numpadmultiply': ("numpad multiply"),
	# Translators: This is the name of a key on the keyboard.
	'numpadminus': ("numpad minus"),
	# Translators: This is the name of a key on the keyboard.
	'numpadplus': ("numpad plus"),
	# Translators: This is the name of a key on the keyboard.
	'numpaddecimal': ("numpad decimal"),
	# Translators: This is the name of a key on the keyboard.
	'numpadinsert': ("numpad insert"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad0': ("numLock numpad 0"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad1': ("numLock numpad 1"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad2': ("numLock numpad 2"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad3': ("numLock numpad 3"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad4': ("numLock numpad 4"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad5': ("numLock numpad 5"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad6': ("numLock numpad 6"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad7': ("numLock numpad 7"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad8': ("numLock numpad 8"),
	# Translators: This is the name of a key on the keyboard.
	'numlocknumpad9': ("numLock numpad 9"),
	# Translators: This is the name of a key on the keyboard.
	'insert': ("insert"),
	# Translators: This is the name of a key on the keyboard.
	'leftcontrol': ("left control"),
	# Translators: This is the name of a key on the keyboard.
	'rightcontrol': ("right control"),
	# Translators: This is the name of a key on the keyboard.
	'leftwindows': ("left windows"),
	# Translators: This is the name of a key on the keyboard.
	'leftshift': ("left shift"),
	# Translators: This is the name of a key on the keyboard.
	'rightshift': ("right shift"),
	# Translators: This is the name of a key on the keyboard.
	'leftalt': ("left alt"),
	# Translators: This is the name of a key on the keyboard.
	'rightalt': ("right alt"),
	# Translators: This is the name of a key on the keyboard.
	'rightwindows': ("right windows"),
	# Translators: This is the name of a key on the keyboard.
	'break': ("break"),
	# Translators: This is the name of a key on the keyboard.
	'tab':  ("tab"),
}

def getKeyCombinationLabel(keyCombination):
	"""
	Fetches a localized label for a combination of multiple keys.
	@param keyCombination: The key combination identifier to get the localized label for, usually plus-separated key identifiers.
	@type keyCombination: string
	@returns: A localized key combination
	@rtype: string
	"""
	keys = keyCombination.lower().split("+")
	return "+".join(localizedKeyLabels.get(key, key) for key in keys)


'''
roleLabels={
	# Translators: The word for an unknown control type.
	ROLE_UNKNOWN:_("unknown"),
	# Translators: The word for window of a program such as document window.
	ROLE_WINDOW:_("window"),
	# Translators: Used to identify title bar of a program.
	ROLE_TITLEBAR:_("title bar"),
	# Translators: The word used for pane such as desktop pane.
	ROLE_PANE:_("pane"),
	# Translators: The word used to denote a dialog box such as open dialog.
	ROLE_DIALOG:_("dialog"),
	# Translators: The text used to identify check boxes such as select check box.
	ROLE_CHECKBOX:_("check box"),
	# Translators: The text used to identify radio buttons such as yes or no radio button.
	ROLE_RADIOBUTTON:_("radio button"),
	# Translators: The word used to identify a static text such as dialog text.
	ROLE_STATICTEXT:_("text"),
	# Translators: The word used to identify edit fields such as subject edit field.
	ROLE_EDITABLETEXT:_("edit"),
	# Translators: The word used to identify a button such as OK button.
	ROLE_BUTTON:_("button"),
	# Translators: Text used to identify menu bar of a program.
	ROLE_MENUBAR:_("menu bar"),
	# Translators: Used to identify a menu item such as an item in file menu.
	ROLE_MENUITEM:_("menu item"),
	# Translators: The word used for menus such as edit menu.
	ROLE_POPUPMENU:_("menu"),
	# Translators: Used to identify combo boxes such as file type combo box.
	ROLE_COMBOBOX:_("combo box"),
	# Translators: The word used for lists such as folder list.
	ROLE_LIST:_("list"),
	# Translators: Used to identify a list item such as email list items.
	ROLE_LISTITEM:_("list item"),
	# Translators: The word used to identify graphics such as webpage graphics.
	ROLE_GRAPHIC:_("graphic"),
	# Translators: Used to identify help balloon (a circular window with helpful text such as notification text).
	ROLE_HELPBALLOON:_("help balloon"),
	# Translators: Used to identify a tooltip (a small window with additional text about selected item such as file information).
	ROLE_TOOLTIP:_("tool tip"),
	# Translators: Identifies a link in webpage documents.
	ROLE_LINK:_("link"),
	# Translators: Identifies a treeview (a tree-like structure such as treeviews for subfolders).
	ROLE_TREEVIEW:_("tree view"),
	# Translators: Identifies a tree view item.
	ROLE_TREEVIEWITEM:_("tree view item"),
	# Translators: The word presented for tabs in a tab enabled window.
	ROLE_TAB: pgettext("controlType", "tab"),
	# Translators: Identifies a tab control such as webpage tabs in web browsers.
	ROLE_TABCONTROL:_("tab control"),
	# Translators: Identifies a slider such as volume slider.
	ROLE_SLIDER:_("slider"),
	# Translators: Identifies a progress bar such as NvDA update progress.
	ROLE_PROGRESSBAR:_("progress bar"),
	# Translators: Identifies a scroll bar.
	ROLE_SCROLLBAR:_("scroll bar"),
	# Translators: Identifies a status bar (text at the bottom bar of the screen such as cursor position in a document).
	ROLE_STATUSBAR:_("status bar"),
	# Translators: Identifies a table such as ones used in various websites.
	ROLE_TABLE:_("table"),
	# Translators: Identifies a cell in a table.
	ROLE_TABLECELL:_("cell"),
	# Translators: Identifies a column (a group of vertical cells in a table).
	ROLE_TABLECOLUMN:_("column"),
	# Translators: Identifies a row (a group of horizontal cells in a table).
	ROLE_TABLEROW:_("row"),
	# Translators: Identifies a frame (a smaller window in a webpage or a document).
	ROLE_FRAME:_("frame"),
	# Translators: Identifies a tool bar.
	ROLE_TOOLBAR:_("tool bar"),
	# Translators: Identifies a column header in tables and spreadsheets.
	ROLE_TABLECOLUMNHEADER:_("column header"),
	# Translators: Identifies a row header in tables and spreadsheets.
	ROLE_TABLEROWHEADER:_("row header"),
	# Translators: Identifies a drop down button (a button that, when clicked, opens a menu of its own).
	ROLE_DROPDOWNBUTTON:_("drop down button"),
	# Translators: Identifies an element.
	ROLE_CLOCK:_("clock"),
	# Translators: Identifies a separator (a horizontal line drawn on the screen).
	ROLE_SEPARATOR:_("separator"),
	# Translators: Identifies a form (controls such as edit boxes, combo boxes and so on).
	ROLE_FORM:_("form"),
	# Translators: Identifies a heading (a bold text used for identifying a section).
	ROLE_HEADING:_("heading"),
	# Translators: Identifies a heading level.
	ROLE_HEADING1:_("heading 1"),
	# Translators: Identifies a heading level.
	ROLE_HEADING2:_("heading 2"),
	# Translators: Identifies a heading level.
	ROLE_HEADING3:_("heading 3"),
	# Translators: Identifies a heading level.
	ROLE_HEADING4:_("heading 4"),
	# Translators: Identifies a heading level.
	ROLE_HEADING5:_("heading 5"),
	# Translators: Identifies a heading level.
	ROLE_HEADING6:_("heading 6"),
	# Translators: Identifies a paragraph (a group of text surrounded by blank lines).
	ROLE_PARAGRAPH:_("paragraph"),
	# Translators: Presented for a section in a document which is a block quotation;
	# i.e. a long quotation in a separate paragraph distinguished by indentation, etc.
	# See http://en.wikipedia.org/wiki/Block_quotation
	ROLE_BLOCKQUOTE:_("block quote"),
	# Translators: Identifies a table header (a short text at the start of a table which describes what the table is about).
	ROLE_TABLEHEADER:_("table header"),
	# Translators: Identifies a table body (the main body of the table).
	ROLE_TABLEBODY:_("table body"),
	# Translators: Identifies a table footer (text placed at the end of the table).
	ROLE_TABLEFOOTER:_("table footer"),
	# Translators: Identifies a document (for example, a webpage document).
	ROLE_DOCUMENT:_("document"),
	# Translators: Identifies an animation in a document or a webpage.
	ROLE_ANIMATION:_("animation"),
	# Translators: Identifies an application in webpages.
	ROLE_APPLICATION:_("application"),
	# Translators: Identifies a box element.
	ROLE_BOX:_("box"),
	# Translators: Identifies a grouping (a number of related items grouped together, such as related options in dialogs).
	ROLE_GROUPING:_("grouping"),
	# Translators: Identifies a property page such as drive properties dialog.
	ROLE_PROPERTYPAGE:_("property page"),
	# Translators: Identifies a canvas element on webpages (a box with some background color with some text drawn on the box, like a canvas).
	ROLE_CANVAS:_("canvas"),
	# Translators: Identifies a caption (usually a short text identifying a picture or a graphic on websites).
	ROLE_CAPTION:_("caption"),
	# Translators: Identifies a check menu item (a menu item with a checkmark as part of the menu item's name).
	ROLE_CHECKMENUITEM:_("check menu item"),
	# Translators: Identifies a data edit field.
	ROLE_DATEEDITOR:_("date edit"),
	# Translators: Identifies an icon.
	ROLE_ICON:_("icon"),
	# Translators: Identifies a directory pane.
	ROLE_DIRECTORYPANE:_("directory pane"),
	# Translators: Identifies an embedded object such as flash content on webpages.
	ROLE_EMBEDDEDOBJECT:_("embedded object"),
	# Translators: Identifies an end note.
	ROLE_ENDNOTE:_("end note"),
	# Translators: Identifies a footer (usually text).
	ROLE_FOOTER:_("footer"),
	# Translators: Identifies a foot note (text at the end of a passage or used for anotations).
	ROLE_FOOTNOTE:_("foot note"),
	# Translators: Reported for an object which is a glass pane; i.e.
	# a pane that is guaranteed to be on top of all panes beneath it.
	ROLE_GLASSPANE:_("glass pane"),
	# Translators: Identifies a header (usually text at top of documents or on tops of pages).
	ROLE_HEADER:_("header"),
	# Translators: Identifies an image map (a type of graphical link).
	ROLE_IMAGEMAP:_("image map"),
	# Translators: Identifies an input window.
	ROLE_INPUTWINDOW:_("input window"),
	# Translators: Identifies a label.
	ROLE_LABEL:_("label"),
	# Translators: Identifies a note field.
	ROLE_NOTE:_("note"),
	# Translators: Identifies a page.
	ROLE_PAGE:_("page"),
	# Translators: Identifies a radio menu item.
	ROLE_RADIOMENUITEM:_("radio menu item"),
	# Translators: Identifies a layered pane.
	ROLE_LAYEREDPANE:_("layered pane"),
	# Translators: Identifies a redundant object.
	ROLE_REDUNDANTOBJECT:_("redundant object"),
	# Translators: Identifies a root pane.
	ROLE_ROOTPANE:_("root pane"),
	# Translators: May be reported for an editable text object in a toolbar.
	# This is deprecated and is not often (if ever) used.
	ROLE_EDITBAR:_("edit bar"),
	# Translators: Identifies a terminal window such as command prompt.
	ROLE_TERMINAL:_("terminal"),
	# Translators: Identifies a rich edit box (an edit box which allows entering formatting commands in addition to text; encountered on webpages and NvDA log viewer).
	ROLE_RICHEDIT:_("rich edit"),
	# Translators: Identifies a ruler object (commonly seen on some webpages and in some Office programs).
	ROLE_RULER:_("ruler"),
	# Translators: Identifies a scroll pane.
	ROLE_SCROLLPANE:_("scroll pane"),
	# Translators: Identifies a section of text.
	ROLE_SECTION:_("section"),
	# Translators: Identifies a shape.
	ROLE_SHAPE:_("shape"),
	# Translators: Identifies a split pane.
	ROLE_SPLITPANE:_("split pane"),
	# Translators: Reported for a view port; i.e. an object usually used in a scroll pane
	# which represents the portion of the entire data that the user can see.
	# As the user manipulates the scroll bars, the contents of the view port can change.
	ROLE_VIEWPORT:_("view port"),
	# Translators: Reported for an object that forms part of a menu system
	# but which can be undocked from or torn off the menu system
	# to exist as a separate window.
	ROLE_TEAROFFMENU:_("tear off menu"),
	# Translators: Identifies a text frame (a frame window which contains text).
	ROLE_TEXTFRAME:_("text frame"),
	# Translators: Identifies a toggle button (a button used to toggle something).
	ROLE_TOGGLEBUTTON:_("toggle button"),
	ROLE_BORDER:_("border"),
	# Translators: Identifies a caret object.
	ROLE_CARET:_("caret"),
	# Translators: Identifies a character field (should not be confused with edit fields).
	ROLE_CHARACTER:_("character"),
	# Translators: Identifies a chart (commonly seen on some websites and in some Office documents).
	ROLE_CHART:_("chart"),
	# Translators: Identifies a cursor object.
	ROLE_CURSOR:_("cursor"),
	# Translators: Identifies a diagram (seen on some websites and on Office documents).
	ROLE_DIAGRAM:_("diagram"),
	# Translators: Identifies a dial object.
	ROLE_DIAL:_("dial"),
	# Translators: Identifies a drop list.
	ROLE_DROPLIST:_("drop list"),
	# Translators: Identifies a split button (a control which performs different actions when different parts are clicked).
	ROLE_SPLITBUTTON:_("split button"),
	# Translators: Identifies a menu button (a button which opens a menu of items).
	ROLE_MENUBUTTON:_("menu button"),
	# Translators: Reported for a button which expands a grid when it is pressed.
	ROLE_DROPDOWNBUTTONGRID:_("drop down button grid"),
	# Translators: Identifies mathematical content.
	ROLE_MATH:_("math"),
	# Translators: Identifies a grip control.
	ROLE_GRIP:_("grip"),
	# Translators: Identifies a hot key field (a field where one can enter a hot key for something, such as assigning shortcut for icons on the desktop).
	ROLE_HOTKEYFIELD:_("hot key field"),
	# Translators: Identifies an indicator control.
	ROLE_INDICATOR:_("indicator"),
	# Translators: Identifies a spin button (a button used to go through options in a spinning fashion).
	ROLE_SPINBUTTON:_("spin button"),
	# Translators: Identifies a sound clip on websites.
	ROLE_SOUND:_("sound"),
	# Translators: Identifies a whitespace.
	ROLE_WHITESPACE:_("white space"),
	# Translators: Identifies a tree view button.
	ROLE_TREEVIEWBUTTON:_("tree view button"),
	# Translators: Identifies an IP address (an IP address field element).
	ROLE_IPADDRESS:_("IP address"),
	# Translators: Identifies a desktop icon (the icons on the desktop such as computer and various shortcuts for programs).
	ROLE_DESKTOPICON:_("desktop icon"),
	# Translators: Identifies an alert message such as file download alert in Internet explorer 9 and above.
	ROLE_ALERT:_("alert"),
	# Translators: Identifies an internal frame. This is usually a frame on a web page; i.e. a web page embedded within a web page.
	ROLE_INTERNALFRAME:_("frame"),
	# Translators: Identifies desktop pane (the desktop window).
	ROLE_DESKTOPPANE:_("desktop pane"),
	# Translators: Identifies an option pane.
	ROLE_OPTIONPANE:_("option pane"),
	# Translators: Identifies a color chooser.
	ROLE_COLORCHOOSER:_("color chooser"),
	# Translators: Identifies a file chooser (to select a file or groups of files from a list).
	ROLE_FILECHOOSER:_("file chooser"),
	ROLE_FILLER:_("filler"),
	# Translators: Identifies a menu such as file menu.
	ROLE_MENU:_("menu"),
	# Translators: Identifies a panel control for grouping related options.
	ROLE_PANEL:_("panel"),
	# Translators: Identifies a password field (a protected edit field for entering passwords such as when logging into web-based email sites).
	ROLE_PASSWORDEDIT:_("password edit"),
	# Translators: Identifies a font chooser.
	ROLE_FONTCHOOSER:_("font chooser"),
	ROLE_LINE:_("line"),
	# Translators: Identifies a font name.
	ROLE_FONTNAME:_("font name"),
	# Translators: Identifies font size.
	ROLE_FONTSIZE:_("font size"),
	# Translators: Describes text formatting.
	ROLE_BOLD:_("bold"),
	# Translators: Describes text formatting.
	ROLE_ITALIC:_("italic"),
	# Translators: Describes text formatting.
	ROLE_UNDERLINE:_("underline"),
	# Translators: Describes text formatting.
	ROLE_FGCOLOR:_("foreground color"),
	# Translators: Describes text formatting.
	ROLE_BGCOLOR:_("background color"),
	# Translators: Describes text formatting.
	ROLE_SUPERSCRIPT:_("superscript"),
	# Translators: Describes text formatting.
	ROLE_SUBSCRIPT:_("subscript"),
	# Translators: Describes style of text.
	ROLE_STYLE:_("style"),
	# Translators: Describes text formatting.
	ROLE_INDENT:_("indent"),
	# Translators: Describes text formatting.
	ROLE_ALIGNMENT:_("alignment"),
	# Translators: Identifies an alert window or bar (usually on Internet Explorer 9 and above for alerts such as file downloads or pop-up blocker).
	ROLE_ALERT:_("alert"),
	# Translators: Identifies a data grid control (a grid which displays data).
	ROLE_DATAGRID:_("data grid"),
	ROLE_DATAITEM:_("data item"),
	ROLE_HEADERITEM:_("header item"),
	# Translators: Identifies a thumb control (a button-like control for changing options).
	ROLE_THUMB:_("thumb control"),
	ROLE_CALENDAR:_("calendar"),
	ROLE_VIDEO:_("video"),
	ROLE_AUDIO:_("audio"),
	# Translators: Identifies a chart element.
	ROLE_CHARTELEMENT:_("chart element"),
	# Translators: Identifies deleted content. 
	ROLE_DELETED_CONTENT:_("deleted"),
	# Translators: Identifies inserted content. 
	ROLE_INSERTED_CONTENT:_("inserted"),
}

stateLabels={
	# Translators: This is presented when a control or document is unavailable.
	STATE_UNAVAILABLE:_("unavailable"),
	# Translators: This is presented when a control has focus.
	STATE_FOCUSED:_("focused"),
	# Translators: This is presented when the control is selected.
	STATE_SELECTED:_("selected"),
	# Translators: This is presented when a document is busy.
	STATE_BUSY:_("busy"),
	# Translators: This is presented when a button is pressed.
	STATE_PRESSED:_("pressed"),
	# Translators: This is presented when a check box is checked.
	STATE_CHECKED:_("checked"),
	# Translators: This is presented when a three state check box is half checked.
	STATE_HALFCHECKED:_("half checked"),
	# Translators: This is presented when the control is a read-only control such as read-only edit box.
	STATE_READONLY:_("read only"),
	# Translators: This is presented when a tree view or submenu item is expanded.
	STATE_EXPANDED:_("expanded"),
	# Translators: This is presented when a tree view or submenu is collapsed.
	STATE_COLLAPSED:_("collapsed"),
	# Translators: This is presented when a control or a document becomes invisible.
	STATE_INVISIBLE:_("invisible"),
	# Translators: This is presented when a visited link is encountered.
	STATE_VISITED:_("visited"),
	# Translators: This is presented when a link is encountered.
	STATE_LINKED:_("linked"),
	# Translators: This is presented when the control menu item has a submenu.
	STATE_HASPOPUP:_("subMenu"),
	# Translators: This is presented when a protected control or a document is encountered.
	STATE_PROTECTED:_("protected"),
	# Translators: This is presented when a required form field is encountered.
	STATE_REQUIRED:_("required"),
	# Translators: Reported when an object no longer exists in the user interface;
	# i.e. it is dead and is no longer usable.
	STATE_DEFUNCT:_("defunct"),
	# Translators: This is presented when an invalid entry has been made.
	STATE_INVALID_ENTRY:_("invalid entry"),
	STATE_MODAL:_("modal"),
	# Translators: This is presented when a field supports auto completion of entered text such as email address field in Microsoft Outlook.
	STATE_AUTOCOMPLETE:_("has auto complete"),
	# Translators: This is presented when an edit field allows typing multiple lines of text such as comment fields on websites.
	STATE_MULTILINE:_("multi line"),
	STATE_ICONIFIED:_("iconified"),
	# Translators: Presented when the current control is located off screen.
	STATE_OFFSCREEN:_("off screen"),
	# Translators: Presented when the control allows selection such as text fields.
	STATE_SELECTABLE:_("selectable"),
	# Translators: Presented when a control can be moved to using system focus.
	STATE_FOCUSABLE:_("focusable"),
	# Translators: Presented when a control allows clicking via mouse (mostly presented on web controls).
	STATE_CLICKABLE:_("clickable"),
	STATE_EDITABLE:_("editable"),
	STATE_CHECKABLE:_("checkable"),
	STATE_DRAGGABLE:_("draggable"),
	STATE_DRAGGING:_("dragging"),
	# Translators: Reported where an object which is being dragged can be dropped.
	# This is only reported for objects that support accessible drag and drop.
	STATE_DROPTARGET:_("drop target"),
	STATE_SORTED:_("sorted"),
	STATE_SORTED_ASCENDING:_("sorted ascending"),
	STATE_SORTED_DESCENDING:_("sorted descending"),
	# Translators: a state that denotes that an object (usually a graphic) has a long description.
	STATE_HASLONGDESC:_("has long description"),
	# Translators: a state that denotes that an object is pinned in its current location
	STATE_PINNED:_("pinned"),
	# Translators: a state that denotes the existance of a formula on a spreadsheet cell
	STATE_HASFORMULA:_("has formula"),
	# Translators: a state that denotes the existance of a comment.
	STATE_HASCOMMENT:_("has comment"),
	# Translators: a state that denotes that the object is covered partially or fully by another object
	STATE_OBSCURED:_("obscured"),
	# Translators: a state that denotes that the object(text) is cropped as it couldn't be accommodated in the allocated/available space
	STATE_CROPPED:_("cropped"),
	# Translators: a state that denotes that the object(text) is overflowing into the adjacent space
	STATE_OVERFLOWING:_("overflowing"),
	# Translators: a state that denotes that the object is unlocked (such as an unlocked cell in a protected Excel spreadsheet). 
	STATE_UNLOCKED:_("unlocked"),
}

negativeStateLabels={
	# Translators: This is presented when a selectable object (e.g. a list item) is not selected.
	STATE_SELECTED:_("not selected"),
	# Translators: This is presented when a button is not pressed.
	STATE_PRESSED:_("not pressed"),
	# Translators: This is presented when a checkbox is not checked.
	STATE_CHECKED:_("not checked"),
	# Translators: This is presented when drag and drop is finished.
	# This is only reported for objects which support accessible drag and drop.
	STATE_DROPTARGET:_("done dragging"),
}

silentRolesOnFocus={
	ROLE_PANE,
	ROLE_ROOTPANE,
	ROLE_FRAME,
	ROLE_UNKNOWN,
	ROLE_APPLICATION,
	ROLE_TABLECELL,
	ROLE_LISTITEM,
	ROLE_MENUITEM,
	ROLE_CHECKMENUITEM,
	ROLE_TREEVIEWITEM,
	ROLE_STATICTEXT,
	ROLE_BORDER,
}

silentValuesForRoles={
	ROLE_CHECKBOX,
	ROLE_RADIOBUTTON,
	ROLE_LINK,
	ROLE_MENUITEM,
	ROLE_APPLICATION,
}

#{ Output reasons
# These constants are used to specify the reason that a given piece of output was generated.
#: An object to be reported due to a focus change or similar.
REASON_FOCUS="focus"
#: An ancestor of the focus object to be reported due to a focus change or similar.
REASON_FOCUSENTERED="focusEntered"
#: An item under the mouse.
REASON_MOUSE="mouse"
#: A response to a user query.
REASON_QUERY="query"
#: Reporting a change to an object.
REASON_CHANGE="change"
#: A generic, screen reader specific message.
REASON_MESSAGE="message"
#: Text reported as part of a say all.
REASON_SAYALL="sayAll"
#: Content reported due to caret movement or similar.
REASON_CARET="caret"
#: No output, but any state should be cached as if output had occurred.
REASON_ONLYCACHE="onlyCache"
#}

#: Text to use for 'current' values. These describe if an item is the current item 
#: within a particular kind of selection.
isCurrentLabels = {
	# Translators: Presented when an item is marked as current in a collection of items
	True:_("current"),
	# Translators: Presented when a page item is marked as current in a collection of page items
	"page":_("current page"),
	# Translators: Presented when a step item is marked as current in a collection of step items
	"step":_("current step"),
	# Translators: Presented when a location item is marked as current in a collection of location items
	"location":_("current location"),
	# Translators: Presented when a date item is marked as current in a collection of date items
	"date":_("current date"),
	# Translators: Presented when a time item is marked as current in a collection of time items
	"time":_("current time"),
}

def processPositiveStates(role, states, reason, positiveStates=None):
	"""Processes the states for an object and returns the positive states to output for a specified reason.
	For example, if C{STATE_CHECKED} is in the returned states, it means that the processed object is checked.
	@param role: The role of the object to process states for (e.g. C{ROLE_CHECKBOX}.
	@type role: int
	@param states: The raw states for an object to process.
	@type states: set
	@param reason: The reason to process the states (e.g. C{REASON_FOCUS}.
	@type reason: str
	@param positiveStates: Used for C{REASON_CHANGE}, specifies states changed from negative to positive;
	@type positiveStates: set
	@return: The processed positive states.
	@rtype: set
	"""
	positiveStates = positiveStates.copy() if positiveStates is not None else states.copy()
	# The user never cares about certain states.
	if role==ROLE_EDITABLETEXT:
		positiveStates.discard(STATE_EDITABLE)
	if role!=ROLE_LINK:
		positiveStates.discard(STATE_VISITED)
	positiveStates.discard(STATE_SELECTABLE)
	positiveStates.discard(STATE_FOCUSABLE)
	positiveStates.discard(STATE_CHECKABLE)
	if STATE_DRAGGING in positiveStates:
		# It's obvious that the control is draggable if it's being dragged.
		positiveStates.discard(STATE_DRAGGABLE)
	if role == ROLE_COMBOBOX:
		# Combo boxes inherently have a popup, so don't report it.
		positiveStates.discard(STATE_HASPOPUP)
	import config
	if not config.conf['documentFormatting']['reportClickable'] or role in (ROLE_LINK, ROLE_BUTTON, ROLE_CHECKBOX, ROLE_RADIOBUTTON, ROLE_TOGGLEBUTTON, ROLE_MENUITEM, ROLE_TAB, ROLE_SLIDER, ROLE_DOCUMENT, ROLE_CHECKMENUITEM, ROLE_RADIOMENUITEM):
		# This control is clearly clickable according to its role,
		# or reporting clickable just isn't useful,
		# or the user has explicitly requested no reporting clickable
		positiveStates.discard(STATE_CLICKABLE)
	if reason == REASON_QUERY:
		return positiveStates
	positiveStates.discard(STATE_DEFUNCT)
	positiveStates.discard(STATE_MODAL)
	positiveStates.discard(STATE_FOCUSED)
	positiveStates.discard(STATE_OFFSCREEN)
	positiveStates.discard(STATE_INVISIBLE)
	if reason != REASON_CHANGE:
		positiveStates.discard(STATE_LINKED)
		if role in (ROLE_LISTITEM, ROLE_TREEVIEWITEM, ROLE_MENUITEM, ROLE_TABLEROW) and STATE_SELECTABLE in states:
			positiveStates.discard(STATE_SELECTED)
	if role not in (ROLE_EDITABLETEXT, ROLE_CHECKBOX):
		positiveStates.discard(STATE_READONLY)
	if role == ROLE_CHECKBOX:
		positiveStates.discard(STATE_PRESSED)
	if role == ROLE_MENUITEM and STATE_HASPOPUP in positiveStates:
		# The user doesn't usually care if a submenu is expanded or collapsed.
		positiveStates.discard(STATE_COLLAPSED)
		positiveStates.discard(STATE_EXPANDED)
	if STATE_FOCUSABLE not in states:
		positiveStates.discard(STATE_EDITABLE)
	return positiveStates

def processNegativeStates(role, states, reason, negativeStates=None):
	"""Processes the states for an object and returns the negative states to output for a specified reason.
	For example, if C{STATE_CHECKED} is in the returned states, it means that the processed object is not checked.
	@param role: The role of the object to process states for (e.g. C{ROLE_CHECKBOX}.
	@type role: int
	@param states: The raw states for an object to process.
	@type states: set
	@param reason: The reason to process the states (e.g. C{REASON_FOCUS}.
	@type reason: str
	@param negativeStates: Used for C{REASON_CHANGE}, specifies states changed from positive to negative;
	@type negativeStates: set
	@return: The processed negative states.
	@rtype: set
	"""
	if reason == REASON_CHANGE and not isinstance(negativeStates, set):
		raise TypeError("negativeStates must be a set for this reason")
	speakNegatives = set()
	# Add the negative selected state if the control is selectable,
	# but only if it is reported for the reason of focus, or this is a change to the focused object. 
	# The condition stops "not selected" from being spoken in some broken controls
	# when the state change for the previous focus is issued before the focus change.
	if (
		# Only include if the object is actually selectable
		STATE_SELECTABLE in states
		# Only include if the object is focusable (E.g. ARIA grid cells, but not standard html tables)
		and STATE_FOCUSABLE in states
		# Only include  if reporting the focus or when states are changing on the focus.
		# This is to avoid exposing it for things like caret movement in browse mode. 
		and (reason == REASON_FOCUS or (reason == REASON_CHANGE and STATE_FOCUSED in states))
		and role in (
			ROLE_LISTITEM, 
			ROLE_TREEVIEWITEM, 
			ROLE_TABLEROW,
			ROLE_TABLECELL,
			ROLE_TABLECOLUMNHEADER,
			ROLE_TABLEROWHEADER
		)
	):
		speakNegatives.add(STATE_SELECTED)
	# Restrict "not checked" in a similar way to "not selected".
	if (role in (ROLE_CHECKBOX, ROLE_RADIOBUTTON, ROLE_CHECKMENUITEM) or STATE_CHECKABLE in states)  and (STATE_HALFCHECKED not in states) and (reason != REASON_CHANGE or STATE_FOCUSED in states):
		speakNegatives.add(STATE_CHECKED)
	if role == ROLE_TOGGLEBUTTON:
		speakNegatives.add(STATE_PRESSED)
	if reason == REASON_CHANGE:
		# We want to speak this state only if it is changing to negative.
		speakNegatives.add(STATE_DROPTARGET)
		# We were given states which have changed to negative.
		# Return only those supplied negative states which should be spoken;
		# i.e. the states in both sets.
		speakNegatives &= negativeStates
		# #6946: if HALFCHECKED is present but CHECKED isn't, we should make sure we add CHECKED to speakNegatives.
		if (STATE_HALFCHECKED in negativeStates and STATE_CHECKED not in states):
			speakNegatives.add(STATE_CHECKED)
		if STATES_SORTED & negativeStates and not STATES_SORTED & states:
			# If the object has just stopped being sorted, just report not sorted.
			# The user doesn't care how it was sorted before.
			speakNegatives.add(STATE_SORTED)
		return speakNegatives
	else:
		# This is not a state change; only positive states were supplied.
		# Return all negative states which should be spoken, excluding the positive states.
		return speakNegatives - states

def processAndLabelStates(role, states, reason, positiveStates=None, negativeStates=None, positiveStateLabelDict={}, negativeStateLabelDict={}):
	"""Processes the states for an object and returns the appropriate state labels for both positive and negative states.
	@param role: The role of the object to process states for (e.g. C{ROLE_CHECKBOX}.
	@type role: int
	@param states: The raw states for an object to process.
	@type states: set
	@param reason: The reason to process the states (e.g. C{REASON_FOCUS}.
	@type reason: str
	@param positiveStates: Used for C{REASON_CHANGE}, specifies states changed from negative to positive;
	@type positiveStates: set
	@param negativeStates: Used for C{REASON_CHANGE}, specifies states changed from positive to negative;
	@type negativeStates: setpositiveStateLabelDict={}, negativeStateLabelDict
	@param positiveStateLabelDict: Dictionary containing state identifiers as keys and associated positive labels as their values.
	@type positiveStateLabelDict: dict
	@param negativeStateLabelDict: Dictionary containing state identifiers as keys and associated negative labels as their values.
	@type negativeStateLabelDict: dict
	@return: The labels of the relevant positive and negative states.
	@rtype: [str, ...]
	"""
	mergedStateLabels=[]
	positiveStates = processPositiveStates(role, states, reason, positiveStates)
	negativeStates = processNegativeStates(role, states, reason, negativeStates)
	for state in sorted(positiveStates | negativeStates):
		if state in positiveStates:
			mergedStateLabels.append(positiveStateLabelDict.get(state, stateLabels[state]))
		elif state in negativeStates:
			# Translators: Indicates that a particular state of an object is negated.
			# Separate strings have now been defined for commonly negated states (e.g. not selected and not checked),
			# but this still might be used in some other cases.
			# %s will be replaced with the full identifier of the negated state (e.g. selected).
			mergedStateLabels.append(negativeStateLabelDict.get(state, negativeStateLabels.get(state, _("not %s") % stateLabels[state])))
	return mergedStateLabels
'''
