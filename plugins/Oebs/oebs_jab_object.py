import ctypes
import re
import oebs_event_handler
import oebs_api
import oebs_control_types

import logging
log=logging.getLogger('oebs_jab_object.py')

JABRolesToNVDARoles={
	"alert":oebs_control_types.ROLE_DIALOG,
	"column header":oebs_control_types.ROLE_TABLECOLUMNHEADER,
	"canvas":oebs_control_types.ROLE_CANVAS,
	"combo box":oebs_control_types.ROLE_COMBOBOX,
	"desktop icon":oebs_control_types.ROLE_DESKTOPICON,
	"internal frame":oebs_control_types.ROLE_INTERNALFRAME,
	"desktop pane":oebs_control_types.ROLE_DESKTOPPANE,
	"option pane":oebs_control_types.ROLE_OPTIONPANE,
	"window":oebs_control_types.ROLE_WINDOW,
	"frame":oebs_control_types.ROLE_FRAME,
	"dialog":oebs_control_types.ROLE_DIALOG,
	"color chooser":oebs_control_types.ROLE_COLORCHOOSER,
	"directory pane":oebs_control_types.ROLE_DIRECTORYPANE,
	"file chooser":oebs_control_types.ROLE_FILECHOOSER,
	"filler":oebs_control_types.ROLE_FILLER,
	"hyperlink":oebs_control_types.ROLE_LINK,
	"icon":oebs_control_types.ROLE_ICON,
	"label":oebs_control_types.ROLE_LABEL,
	"root pane":oebs_control_types.ROLE_PANEL,
	"glass pane":oebs_control_types.ROLE_PANEL,
	"layered pane":oebs_control_types.ROLE_PANEL,
	"list":oebs_control_types.ROLE_LIST,
	"list item":oebs_control_types.ROLE_LISTITEM,
	"menu bar":oebs_control_types.ROLE_MENUBAR,
	"popup menu":oebs_control_types.ROLE_POPUPMENU,
	"menu":oebs_control_types.ROLE_MENU,
	"menu item":oebs_control_types.ROLE_MENUITEM,
	"separator":oebs_control_types.ROLE_SEPARATOR,
	"page tab list":oebs_control_types.ROLE_TABCONTROL,
	"page tab":oebs_control_types.ROLE_TAB,
	"panel":oebs_control_types.ROLE_PANEL,
	"progress bar":oebs_control_types.ROLE_PROGRESSBAR,
	"password text":oebs_control_types.ROLE_PASSWORDEDIT,
	"push button":oebs_control_types.ROLE_BUTTON,
	"toggle button":oebs_control_types.ROLE_TOGGLEBUTTON,
	"check box":oebs_control_types.ROLE_CHECKBOX,
	"radio button":oebs_control_types.ROLE_RADIOBUTTON,
	"row header":oebs_control_types.ROLE_TABLEROWHEADER,
	"scroll pane":oebs_control_types.ROLE_SCROLLPANE,
	"scroll bar":oebs_control_types.ROLE_SCROLLBAR,
	"view port":oebs_control_types.ROLE_VIEWPORT,
	"slider":oebs_control_types.ROLE_SLIDER,
	"split pane":oebs_control_types.ROLE_SPLITPANE,
	"table":oebs_control_types.ROLE_TABLE,
	"text":oebs_control_types.ROLE_EDITABLETEXT,
	"tree":oebs_control_types.ROLE_TREEVIEW,
	"tool bar":oebs_control_types.ROLE_TOOLBAR,
	"tool tip":oebs_control_types.ROLE_TOOLTIP,
	"status bar":oebs_control_types.ROLE_STATUSBAR,
	"statusbar":oebs_control_types.ROLE_STATUSBAR,
	"date editor":oebs_control_types.ROLE_DATEEDITOR,
	"spin box":oebs_control_types.ROLE_SPINBUTTON,
	"font chooser":oebs_control_types.ROLE_FONTCHOOSER,
	"group box":oebs_control_types.ROLE_GROUPING,
	"header":oebs_control_types.ROLE_HEADER,
	"footer":oebs_control_types.ROLE_FOOTER,
	"paragraph":oebs_control_types.ROLE_PARAGRAPH,
	"ruler":oebs_control_types.ROLE_RULER,
	"edit bar":oebs_control_types.ROLE_EDITBAR,
}

JABStatesToNVDAStates={
	"busy":oebs_control_types.STATE_BUSY,
	"checked":oebs_control_types.STATE_CHECKED,
	"focused":oebs_control_types.STATE_FOCUSED,
	"selected":oebs_control_types.STATE_SELECTED,
	"pressed":oebs_control_types.STATE_PRESSED,
	"expanded":oebs_control_types.STATE_EXPANDED,
	"collapsed":oebs_control_types.STATE_COLLAPSED,
	"iconified":oebs_control_types.STATE_ICONIFIED,
	"modal":oebs_control_types.STATE_MODAL,
	"multi_line":oebs_control_types.STATE_MULTILINE,
	"focusable":oebs_control_types.STATE_FOCUSABLE,
	"editable":oebs_control_types.STATE_EDITABLE,
}

re_simpleXmlTag=re.compile(r"\<[^>]+\>")
'''
class JABTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _getOffsetFromPoint(self,x,y):
		info=self.obj.jabContext.getAccessibleTextInfo(x,y)
		offset=max(min(info.indexAtPoint,info.charCount-1),0)
		return offset

	def _getCaretOffset(self):
		textInfo=self.obj.jabContext.getAccessibleTextInfo(self.obj._JABAccContextInfo.x,self.obj._JABAccContextInfo.y)
		offset=textInfo.caretIndex
		# OpenOffice sometimes returns nonsense, so treat charCount < offset as no caret.
		if offset==-1 or textInfo.charCount<offset:
			raise RuntimeError("no available caret in this object")
		return offset

	def _setCaretOffset(self,offset):
		self.obj.jabContext.setCaretPosition(offset)

	def _getSelectionOffsets(self):
		info=self.obj.jabContext.getAccessibleTextSelectionInfo()
		start=max(info.selectionStartIndex,0)
		end=max(info.selectionEndIndex,0)
		return (start,end)

	def _setSelectionOffsets(self,start,end):
		self.obj.jabContext.selectTextRange(start,end)

	def _getStoryLength(self):
		if not hasattr(self,'_storyLength'):
			textInfo=self.obj.jabContext.getAccessibleTextInfo(self.obj._JABAccContextInfo.x,self.obj._JABAccContextInfo.y)
			self._storyLength=textInfo.charCount
		return self._storyLength

	def _getTextRange(self,start,end):
		#Java needs end of range as last character, not one past the last character
		text=self.obj.jabContext.getAccessibleTextRange(start,end-1)
		return text

	def _getLineNumFromOffset(self,offset):
		return None

	def _getLineOffsets(self,offset):
		(start,end)=self.obj.jabContext.getAccessibleTextLineBounds(offset)
		if end==-1 and offset>0:
			# #1892: JAB returns -1 for the end insertion position
			# instead of returning the offsets for the last line.
			# Try one character back.
			(start,end)=self.obj.jabContext.getAccessibleTextLineBounds(offset-1)
		#Java gives end as the last character, not one past the last character
		end=end+1
		return (start,end)

	def _getParagraphOffsets(self,offset):
		return self._getLineOffsets(offset)

	def _getFormatFieldAndOffsets(self, offset, formatConfig, calculateOffsets=True):
		attribs, length = self.obj.jabContext.getTextAttributesInRange(offset, self._endOffset - 1)
		field = textInfos.FormatField()
		field["font-family"] = attribs.fontFamily
		field["font-size"] = "%dpt" % attribs.fontSize
		field["bold"] = bool(attribs.bold)
		field["italic"] = bool(attribs.italic)
		field["strikethrough"] = bool(attribs.strikethrough)
		field["underline"] = bool(attribs.underline)
		if attribs.superscript:
			field["text-position"] = "super"
		elif attribs.subscript:
			field["text-position"] = "sub"
		# TODO: Not sure how to interpret Java's alignment numbers.
		return field, (offset, offset + length)

	def getEmbeddedObject(self, offset=0):
		offset += self._startOffset

		# We need to count the embedded objects to determine which child to use.
		# This could possibly be optimised by caching.
		text = self._getTextRange(0, offset + 1)
		childIndex = text.count(u"\uFFFC") - 1
		jabContext=self.obj.jabContext.getAccessibleChildFromContext(childIndex)
		if jabContext:
			return JAB(jabContext=jabContext)

		raise LookupError
'''
class JAB(object):
	'''
	def findOverlayClasses(self,clsList):
		role = self.JABRole
		if self._JABAccContextInfo.accessibleText and role in ("text","password text","edit bar","view port","paragraph"):
			clsList.append(EditableTextWithoutAutoSelectDetection)
		elif role in ("dialog", "alert"):
			clsList.append(Dialog)
		elif role=="combo box":
			clsList.append(ComboBox)
		elif role=="table":
			clsList.append(Table)
		elif self.parent and isinstance(self.parent,Table) and self.parent._jabTableInfo:
			clsList.append(TableCell)
		clsList.append(JAB)
	'''
	'''
	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		jabContext=None
		windowHandle=kwargs['windowHandle']
		if relation=="focus":
			vmID=ctypes.c_int()
			accContext=oebs_api.JOBJECT64()
			oebs_api.windowsbridgeDll.getAccessibleContextWithFocus(windowHandle,ctypes.byref(vmID),ctypes.byref(accContext))
			jabContext=oebs_api.JABContext(hwnd=windowHandle,vmID=vmID.value,accContext=accContext.value)
		elif isinstance(relation,tuple):
			jabContext=oebs_api.JABContext(hwnd=windowHandle)
			if jabContext:
				jabContext=jabContext.getAccessibleContextAt(*relation)
		else:
			jabContext=oebs_api.JABContext(hwnd=windowHandle)
		if not jabContext:
			return False
		kwargs['jabContext']=jabContext
		return True
	'''
	def __init__(self,relation=None,windowHandle=None,jabContext=None):
		if not windowHandle:
			windowHandle=jabContext.hwnd
		self.windowHandle=windowHandle
		self.jabContext=jabContext
		#super(JAB,self).__init__(windowHandle=windowHandle)
		self._JABAccContextInfo = self._get__JABAccContextInfo()
		self.role=self._get_role()
		try:
			self._JABAccContextInfo
		except RuntimeError:
			log.error("Could not get accessible context info")
		

	def _get__JABAccContextInfo(self):
		return self.jabContext.getAccessibleContextInfo()
	'''
	def _get_TextInfo(self):
		if self._JABAccContextInfo.accessibleText and self.role not in [oebs_control_types.ROLE_BUTTON,oebs_control_types.ROLE_MENUITEM,oebs_control_types.ROLE_MENU,oebs_control_types.ROLE_LISTITEM]:
			return JABTextInfo
		return super(JAB,self).TextInfo
	'''
	def _isEqual(self,other):
		try:
			return self.jabContext==other.jabContext
		except:
			return False

	def _get_keyboardShortcut(self):
		bindings=self.jabContext.getAccessibleKeyBindings()
		if not bindings or bindings.keyBindingsCount<1: 
			return None
		shortcutsList=[]
		for index in range(bindings.keyBindingsCount):
			binding=bindings.keyBindingInfo[index]
			# We don't support these modifiers
			if binding.modifiers&(oebs_api.ACCESSIBLE_META_KEYSTROKE|oebs_api.ACCESSIBLE_ALT_GRAPH_KEYSTROKE|oebs_api.ACCESSIBLE_BUTTON1_KEYSTROKE|oebs_api.ACCESSIBLE_BUTTON2_KEYSTROKE|oebs_api.ACCESSIBLE_BUTTON3_KEYSTROKE):
				continue
			keyList=[]
			# We assume alt  if there are no modifiers at all and its not a menu item as this is clearly a nmonic
			if (binding.modifiers&oebs_api.ACCESSIBLE_ALT_KEYSTROKE) or (not binding.modifiers and self.role!=oebs_control_types.ROLE_MENUITEM):
				keyList.append(oebs_control_types.localizedKeyLabels['alt'])
			if binding.modifiers&oebs_api.ACCESSIBLE_CONTROL_KEYSTROKE:
				keyList.append(oebs_control_types.localizedKeyLabels['control'])
			if binding.modifiers&oebs_api.ACCESSIBLE_SHIFT_KEYSTROKE:
				keyList.append(oebs_control_types.localizedKeyLabels['shift'])
			keyList.append(binding.character)
		shortcutsList.append("+".join(keyList))
		return ", ".join(shortcutsList)

	def _get_name(self):
		#return re_simpleXmlTag.sub(" ", self._JABAccContextInfo.name)
		return self._JABAccContextInfo.name

	def _get_JABRole(self):
		return self._JABAccContextInfo.role_en_US

	def _get_role(self):
		#role = JABRolesToNVDARoles.get(self.JABRole,oebs_control_types.ROLE_UNKNOWN)
		role = JABRolesToNVDARoles.get(self._get_JABRole(),oebs_control_types.ROLE_UNKNOWN)
		'''
		if role in ( oebs_control_types.ROLE_LABEL, oebs_control_types.ROLE_PANEL) and self.parent:
			parentRole = self.parent.role
			if parentRole == oebs_control_types.ROLE_LIST:
				return oebs_control_types.ROLE_LISTITEM
			elif parentRole in (oebs_control_types.ROLE_TREEVIEW, oebs_control_types.ROLE_TREEVIEWITEM):
				return oebs_control_types.ROLE_TREEVIEWITEM
		if role==oebs_control_types.ROLE_LABEL:
			return oebs_control_types.ROLE_STATICTEXT
		'''
		return role

	def _get_JABStates(self):
		return self._JABAccContextInfo.states_en_US

	def _get_object_depth(self):
		return self.jabContext.getObjectDepth()

	def _get_states(self):
		log.debug("states: %s"%self.JABStates)
		stateSet=set()
		stateString=self.JABStates
		stateStrings=stateString.split(',')
		temp = self.jabContext.getAccessibleContextInfo()
		for state in stateStrings:
			if JABStatesToNVDAStates.has_key(state):
				stateSet.add(JABStatesToNVDAStates[state])
		if "visible" not in stateStrings:
			stateSet.add(oebs_control_types.STATE_INVISIBLE)
		if "showing" not in stateStrings:
			stateSet.add(oebs_control_types.STATE_OFFSCREEN)
		if "expandable" not in stateStrings:
			stateSet.discard(oebs_control_types.STATE_COLLAPSED)
		return stateSet

	def _get_value(self):
		if self.role not in [oebs_control_types.ROLE_CHECKBOX,oebs_control_types.ROLE_MENU,oebs_control_types.ROLE_MENUITEM,oebs_control_types.ROLE_RADIOBUTTON,oebs_control_types.ROLE_BUTTON] and self._JABAccContextInfo.accessibleValue and not self._JABAccContextInfo.accessibleText:
			return self.jabContext.getCurrentAccessibleValueFromContext()

	def _get_description(self):
		return re_simpleXmlTag.sub(" ", self._JABAccContextInfo.description)
	'''
	def _get_location(self):
		return RectLTWH(self._JABAccContextInfo.x,self._JABAccContextInfo.y,self._JABAccContextInfo.width,self._JABAccContextInfo.height)
	'''
	def _get_hasFocus(self):
		if oebs_control_types.STATE_FOCUSED in self.states:
			return True
		else:
			return False

	def _get_positionInfo(self):
		info=super(JAB,self).positionInfo or {}

		# If tree view item, try to retrieve the level via JAB
		if self.role==oebs_control_types.ROLE_TREEVIEWITEM:
			try:
				tree=self.jabContext.getAccessibleParentWithRole("tree")
				if tree:
					treeDepth=tree.getObjectDepth()
					selfDepth=self.jabContext.getObjectDepth()
					if selfDepth > treeDepth:
						info['level']=selfDepth-treeDepth
			except:
				pass

		targets=self._getJABRelationTargets('memberOf')
		for index,target in enumerate(targets):
			if target==self.jabContext:
				info['indexInGroup']=index+1
				info['similarItemsInGroup']=len(targets)
				return info

		parent=self.parent
		if isinstance(parent,JAB) and self.role in (oebs_control_types.ROLE_TREEVIEWITEM,oebs_control_types.ROLE_LISTITEM):
			index=self._JABAccContextInfo.indexInParent+1
			childCount=parent._JABAccContextInfo.childrenCount
			info['indexInGroup']=index
			info['similarItemsInGroup']=childCount
		return info

	def _get_activeChild(self):
		jabContext=self.jabContext.getActiveDescendent()
		if jabContext:
			return JAB(jabContext=jabContext)
		else:
			return None

	def _get_parent(self):
		jabContext=self.jabContext.getAccessibleParentFromContext()
		if jabContext:
			return JAB(jabContext=jabContext)
		return None
		'''
		if not hasattr(self,'_parent'):
			jabContext=self.jabContext.getAccessibleParentFromContext()
			if jabContext:
				self._parent=JAB(jabContext=jabContext)
			else:
				self._parent=super(JAB,self).parent
		return self._parent
		'''
 
	def _get_next(self):
		parent=self.parent
		if not isinstance(parent,JAB):
			return super(JAB,self).next
		if self.indexInParent is None:
			return None
		newIndex=self.indexInParent+1
		if newIndex>=parent._JABAccContextInfo.childrenCount:
			return None
		jabContext=parent.jabContext.getAccessibleChildFromContext(newIndex)
		if not jabContext:
			return None
		obj=JAB(jabContext=jabContext)
		if not isinstance(obj.parent,JAB):
			obj.parent=parent
		if obj.indexInParent is None:
			obj.indexInParent=newIndex
		elif obj.indexInParent<=self.indexInParent: 
			return None
		return obj

	def _get_previous(self):
		parent=self.parent
		if not isinstance(parent,JAB):
			return super(JAB,self).previous
		if self.indexInParent is None:
			return None
		newIndex=self.indexInParent-1
		if newIndex<0:
			return None
		jabContext=parent.jabContext.getAccessibleChildFromContext(newIndex)
		if not jabContext:
			return None
		obj=JAB(jabContext=jabContext)
		log.debug (obj.role)
		if not isinstance(obj.parent,JAB):
			obj.parent=parent
		if obj.indexInParent is None:
			obj.indexInParent=newIndex
		elif obj.indexInParent>=self.indexInParent: 
			return None
		return obj

	def _get_firstChild(self):
		if self._JABAccContextInfo.childrenCount<=0:
			return None
		jabContext=self.jabContext.getAccessibleChildFromContext(0)
		if jabContext:
			obj=JAB(jabContext=jabContext)
			if not isinstance(obj.parent,JAB):
				obj.parent=self
			if obj.indexInParent is None:
				obj.indexInParent=0
			return obj
		else:
			return None

	def _get_lastChild(self):
		if self._JABAccContextInfo.childrenCount<=0:
			return None
		jabContext=self.jabContext.getAccessibleChildFromContext(self.childCount-1)
		if jabContext:
			obj=JAB(jabContext=jabContext)
			if not isinstance(obj.parent,JAB):
				obj.parent=self
			if obj.indexInParent is None:
				obj.indexInParent=self.childCount-1
			return obj
		else:
			return None

	def _get_childCount(self):
		return self._JABAccContextInfo.childrenCount

	def _get_children(self):
		children=[]
		for index in range(self._JABAccContextInfo.childrenCount):
			jabContext=self.jabContext.getAccessibleChildFromContext(index)
			if jabContext:
				obj=JAB(jabContext=jabContext)
				if not isinstance(obj.parent,JAB):
					obj.parent=self
				if obj.indexInParent is None:
					obj.indexInParent=index
				children.append(obj)
		return children

	def _get_indexInParent(self):
		index = self._JABAccContextInfo.indexInParent
		if index == -1:
			return None
		return index

	def _getJABRelationTargets(self, key):
		rs = self.jabContext.getAccessibleRelationSet()
		targets=[]
		for relation in rs.relations[:rs.relationCount]:
			for target in relation.targets[:relation.targetCount]:
				if relation.key == key:
					targets.append(oebs_api.JABContext(self.jabContext.hwnd, self.jabContext.vmID, target))
				else:
					oebs_api.windowsbridgeDll.releaseJavaObject(self.jabContext.vmID,target)
		return targets

	def _get_flowsTo(self):
		targets=self._getJABRelationTargets("flowsTo")
		if targets:
			return targets[0]

	def _get_flowsFrom(self):
		targets=self._getJABRelationTargets("flowsFrom")
		if targets:
			return targets[0]

	def reportFocus(self):
		parent=self.parent
		if self.role in [oebs_control_types.ROLE_LIST] and isinstance(parent,JAB) and parent.role==oebs_control_types.ROLE_COMBOBOX:
			return
		super(JAB,self).reportFocus()

	def _get__actions(self):
		actions = oebs_api.AccessibleActions()
		oebs_api.windowsbridgeDll.getAccessibleActions(self.jabContext.vmID, self.jabContext.accContext, actions)
		return actions.actionInfo[:actions.actionsCount]

	def _get_actionCount(self):
		return len(self._actions)

	def getActionName(self, index=None):
		if index is None:
			index = self.defaultActionIndex
		try:
			return self._actions[index].name
		except IndexError:
			raise NotImplementedError

	def doAction(self, index=None):
		if index is None:
			index = self.defaultActionIndex
		try:
			oebs_api.windowsbridgeDll.doAccessibleActions(self.jabContext.vmID, self.jabContext.accContext,
				oebs_api.AccessibleActionsToDo(actionsCount=1, actions=(self._actions[index],)),
				oebs_api.jint())
		except (IndexError, RuntimeError):
			raise NotImplementedError

	def _get_activeDescendant(self):
		descendantFound=False
		jabContext=self.jabContext
		while jabContext:
			try:
				tempContext=jabContext.getActiveDescendent()
			except:
				break
			if not tempContext:
				break
			try:
				depth=tempContext.getObjectDepth()
			except:
				depth=-1
			if depth<=0 or tempContext==jabContext: 
				break
			jabContext=tempContext
			descendantFound=True
		if descendantFound:
			return JAB(jabContext=jabContext)

	def event_gainFocus(self):
		if oebs_event_handler.isPendingEvents("gainFocus"):
			return
		#super(JAB,self).event_gainFocus()
		if oebs_event_handler.isPendingEvents("gainFocus"):
			return
		'''
		activeDescendant=self.activeDescendant
		if activeDescendant:
			oebs_event_handler.queueEvent("gainFocus",activeDescendant)
		'''
	
	def event_mousePressed(self):
		#log.info("in event mouse Pressed")
		# see if path generator is free
		pass
		'''
		free = oebs_api.path_obj.isFree()
		while not free:
			log.info("waiting to generate xpath")
			free = oebs_api.path_obj.isFree()
		'''
		'''
		oebs_api.path_obj.get_path(oebs_event_handler.lastQueuedMousePressedObject)
		# wait until path generators status changes to free
		free = oebs_api.path_obj.isFree()
		log.info(free)
		while not free:
			log.info("waiting to generate xpath")
			free = oebs_api.path_obj.isFree()
		'''
		

class ComboBox(JAB):

	def _get_states(self):
		states=super(ComboBox,self).states
		if oebs_control_types.STATE_COLLAPSED not in states and oebs_control_types.STATE_EXPANDED not in states:
			if self.childCount==1 and self.firstChild and self.firstChild.role==oebs_control_types.ROLE_POPUPMENU:
				if oebs_control_types.STATE_INVISIBLE in self.firstChild.states:
					states.add(oebs_control_types.STATE_COLLAPSED)
				else:
					states.add(oebs_control_types.STATE_EXPANDED)
		return states

	def _get_activeDescendant(self):
		if oebs_control_types.STATE_COLLAPSED in self.states:
			return None
		return super(ComboBox,self).activeDescendant

	def _get_value(self):
		value=super(ComboBox,self).value
		if not value and not self.activeDescendant: 
			descendant=super(ComboBox,self).activeDescendant
			if descendant:
				value=descendant.name
		return value

class Table(JAB):

	def _get__jabTableInfo(self):
		info=self.jabContext.getAccessibleTableInfo()
		if info:
			self._jabTableInfo=info
			return info

	def _get_rowCount(self):
		if self._jabTableInfo:
			return self._jabTableInfo.rowCount

	def _get_columnCount(self):
		if self._jabTableInfo:
			return self._jabTableInfo.columnCount

	def _get_tableID(self):
		return self._jabTableInfo.jabTable.accContext.value

class TableCell(JAB):

	role=oebs_control_types.ROLE_TABLECELL

	def _get_table(self):
		if self.parent and isinstance(self.parent,Table):
			self.table=self.parent
			return self.table

	def _get_tableID(self):
		return self.table.tableID

	def _get_rowNumber(self):
		return self.table._jabTableInfo.jabTable.getAccessibleTableRow(self.indexInParent)+1

	def _get_columnNumber(self):
		return self.table._jabTableInfo.jabTable.getAccessibleTableColumn(self.indexInParent)+1

	def _get_rowHeaderText(self):
		headerTableInfo=self.table.jabContext.getAccessibleTableRowHeader()
		if headerTableInfo and headerTableInfo.jabTable:
			textList=[]
			row=self.rowNumber-1
			for col in range(headerTableInfo.columnCount):
				cellInfo=headerTableInfo.jabTable.getAccessibleTableCellInfo(row,col)
				if cellInfo and cellInfo.jabContext:
					obj=JAB(jabContext=cellInfo.jabContext)
					if obj.name: textList.append(obj.name)
					if obj.description: textList.append(obj.description)
			jabContext=self.table._jabTableInfo.jabTable.getAccessibleTableRowDescription(row)
			if jabContext:
				obj=JAB(jabContext=jabContext)
				if obj.name: textList.append(obj.name)
				if obj.description: textList.append(obj.description)
			return " ".join(textList)

	def _get_columnHeaderText(self):
		headerTableInfo=self.table.jabContext.getAccessibleTableColumnHeader()
		if headerTableInfo and headerTableInfo.jabTable:
			textList=[]
			col=self.columnNumber-1
			for row in range(headerTableInfo.rowCount):
				cellInfo=headerTableInfo.jabTable.getAccessibleTableCellInfo(row,col)
				if cellInfo and cellInfo.jabContext:
					obj=JAB(jabContext=cellInfo.jabContext)
					if obj.name: textList.append(obj.name)
					if obj.description: textList.append(obj.description)
			jabContext=self.table._jabTableInfo.jabTable.getAccessibleTableColumnDescription(col)
			if jabContext:
				obj=JAB(jabContext=jabContext)
				if obj.name: textList.append(obj.name)
				if obj.description: textList.append(obj.description)
			return " ".join(textList)
