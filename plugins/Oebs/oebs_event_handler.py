#oebs_event_handler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2017 NV Access Limited, Babbage B.V.

import threading
import oebs_queue_handler
import oebs_api2
import oebs_global_vars
import winuser
import inspect
import logging
from queue import Queue # Python 3 import
import oebs_click_and_add
log=logging.getLogger('oebs_event_handler.py')
eventQueue=Queue()
eventQueue.__name__="eventQueue"



#Some dicts to store event counts by name and or obj
_pendingEventCountsByName={}
_pendingEventCountsByObj={}
_pendingEventCountsByNameAndObj={}
# Needed to ensure updates are atomic, as these might be updated from multiple threads simultaneously.
_pendingEventCountsLock=threading.RLock()

#: the last object queued for a gainFocus event. Useful for code running outside NVDA's core queue 
lastQueuedFocusObject=None
lastQueuedMousePressedObject=None
def queueEvent(eventName,obj,**kwargs):
	"""Queues an NVDA event to be executed.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	"""
	global lastQueuedFocusObject, lastQueuedMousePressedObject, eventQueue
	if eventName=="gainFocus":
		lastQueuedFocusObject=obj
	if eventName=="mousePressed":
		lastQueuedMousePressedObject=obj
	with _pendingEventCountsLock:
		_pendingEventCountsByName[eventName]=_pendingEventCountsByName.get(eventName,0)+1
		_pendingEventCountsByObj[obj]=_pendingEventCountsByObj.get(obj,0)+1
		_pendingEventCountsByNameAndObj[(eventName,obj)]=_pendingEventCountsByNameAndObj.get((eventName,obj),0)+1
	queueFunction(eventQueue,_queueEventCallback,eventName,obj,kwargs)


def queueFunction(queue,func,*args,**kwargs):
	queue.put_nowait((func,args,kwargs))
	oebs_click_and_add.get_core().requestPump()

def flushQueue(queue):
	for count in range(queue.qsize()+1):
		if not queue.empty():
			(func,args,kwargs)=queue.get_nowait()
			#watchdog.alive()
			try:
				func(*args,**kwargs)
			except Exception as e:
				log.debug("Error in func %s from %s"%(func.__name__,queue.__name__))
				log.debug(e)

def _queueEventCallback(eventName,obj,kwargs):
	with _pendingEventCountsLock:
		curCount=_pendingEventCountsByName.get(eventName,0)
		if curCount>1:
			_pendingEventCountsByName[eventName]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByName[eventName]
		curCount=_pendingEventCountsByObj.get(obj,0)
		if curCount>1:
			_pendingEventCountsByObj[obj]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByObj[obj]
		curCount=_pendingEventCountsByNameAndObj.get((eventName,obj),0)
		if curCount>1:
			_pendingEventCountsByNameAndObj[(eventName,obj)]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByNameAndObj[(eventName,obj)]
	executeEvent(eventName,obj,**kwargs)

def isPendingEvents(eventName=None,obj=None):
	"""Are there currently any events queued?
	@param eventName: an optional name of an event type. If given then only if there are events of this type queued will it return True.
	@type eventName: string
	@param obj: the NVDAObject the event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@returns: True if there are events queued, False otherwise.
	@rtype: boolean
	"""
	if not eventName and not obj:
		return bool(len(_pendingEventCountsByName))
	elif not eventName and obj:
		return obj in _pendingEventCountsByObj
	elif eventName and not obj:
		return eventName in _pendingEventCountsByName
	elif eventName and obj:
		return (eventName,obj) in _pendingEventCountsByNameAndObj

class _EventExecuter(object):
	"""Facilitates execution of a chain of event functions.
	L{gen} generates the event functions and positional arguments.
	L{next} calls the next function in the chain.
	"""

	def __init__(self, eventName, obj, kwargs):
		self.kwargs = kwargs
		self._gen = self.gen(eventName, obj)
		try:
			self.next()
		except StopIteration:
			pass
		del self._gen

	def next(self):
		#logger.info("next")
		func, args = next(self._gen)
		try:
			return func(*args, **self.kwargs)
		except TypeError:
			log.warning("Could not execute function {func} defined in {module} module; kwargs: {kwargs}".format(
				func=func.__name__,
				module=func.__module__ or "unknown",
				kwargs=self.kwargs
			), exc_info=True) 
			return callWithSupportedKwargs(func, *args, **self.kwargs)

	def gen(self, eventName, obj):
		funcName = "event_%s" % eventName
		keyboard = False
		if eventName == 'typedCharacter':
			import keyboardHandler
			func = keyboardHandler.event_typedCharacter
			keyboard = True
			if func:
				yield func, ()
		# NVDAObject level.
		if not keyboard:
			func = getattr(obj, funcName, None)
			if func:
				yield func, ()

def executeEvent(eventName,obj,**kwargs):
	"""Executes an NVDA event.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	@param obj: the object the event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@param kwargs: Additional event parameters as keyword arguments.
	"""

	try:
		oebs_api2.setFocusObject(obj)
		_EventExecuter(eventName,obj,kwargs)
	except:
		log.error("error executing event: %s on %s with extra args of %s"%(eventName,obj,kwargs))

def doPreGainFocus(obj,sleepMode=False):
	oldForeground=oebs_api2.getForegroundObject()
	oldFocus=oebs_api2.getFocusObject()
	oldTreeInterceptor=oldFocus.treeInterceptor if oldFocus else None
	oebs_api2.setFocusObject(obj)
	if oebs_global_vars.focusDifferenceLevel<=1:
		newForeground=oebs_api2.getDesktopObject().objectInForeground()
		if not newForeground:
			log.debug("Can not get real foreground, resorting to focus ancestors")
			ancestors=oebs_api2.getFocusAncestors()
			if len(ancestors)>1:
				newForeground=ancestors[1]
			else:
				newForeground=obj
		oebs_api2.setForegroundObject(newForeground)
		executeEvent('foreground',newForeground)
	if sleepMode: return True
	#Fire focus entered events for all new ancestors of the focus if this is a gainFocus event
	for parent in oebs_global_vars.focusAncestors[oebs_global_vars.focusDifferenceLevel:]:
		executeEvent("focusEntered",parent)
	if obj.treeInterceptor is not oldTreeInterceptor:
		if hasattr(oldTreeInterceptor,"event_treeInterceptor_loseFocus"):
			oldTreeInterceptor.event_treeInterceptor_loseFocus()
		if obj.treeInterceptor and obj.treeInterceptor.isReady and hasattr(obj.treeInterceptor,"event_treeInterceptor_gainFocus"):
			obj.treeInterceptor.event_treeInterceptor_gainFocus()
	return True

def doPreDocumentLoadComplete(obj):
	focusObject=oebs_api2.getFocusObject()
	return True

#: set of (eventName, processId, windowClassName) of events to accept.
_acceptEvents = set()
#: Maps process IDs to sets of events so they can be cleaned up when the process exits.
_acceptEventsByProcess = {}

def requestEvents(eventName=None, processId=None, windowClassName=None):
	"""Request that particular events be accepted from a platform API.
	Normally, L{shouldAcceptEvent} rejects certain events, including
	most show events, events indicating changes in background processes, etc.
	This function allows plugins to override this for specific cases;
	e.g. to receive show events from a specific control or
	to receive certain events even when in the background.
	Note that NVDA may block some events at a lower level and doesn't listen for some event types at all.
	In these cases, you will not be able to override this.
	This should generally be called when a plugin is instantiated.
	All arguments must be provided.
	"""
	if not eventName or not processId or not windowClassName:
		raise ValueError("eventName, processId or windowClassName not specified")
	entry = (eventName, processId, windowClassName)
	procEvents = _acceptEventsByProcess.get(processId)
	if not procEvents:
		procEvents = _acceptEventsByProcess[processId] = set()
	procEvents.add(entry)
	_acceptEvents.add(entry)

def handleAppTerminate(appModule):
	global _acceptEvents
	events = _acceptEventsByProcess.pop(appModule.processID, None)
	if not events:
		return
	_acceptEvents -= events

def shouldAcceptEvent(eventName, windowHandle=None):
	"""Check whether an event should be accepted from a platform API.
	Creating NVDAObjects and executing events can be expensive
	and might block the main thread noticeably if the object is slow to respond.
	Therefore, this should be used before NVDAObject creation to filter out any unnecessary events.
	A platform API handler may do its own filtering before this.
	"""
	if not windowHandle:
		# We can't filter without a window handle.
		return True
	wClass = winuser.getClassName(windowHandle)
	key = (eventName,
		winuser.getWindowThreadProcessID(windowHandle)[0],
		wClass)
	if key in _acceptEvents:
		return True
	'''
	if eventName == "valueChange" and config.conf["presentation"]["progressBarUpdates"]["reportBackgroundProgressBars"]:
		return True
	'''
	if eventName == "valueChange":
		return True
	if eventName == "show":
		# Only accept 'show' events for specific cases, as otherwise we get flooded.
		return wClass in (
			"Frame Notification Bar", # notification bars
			"tooltips_class32", # tooltips
			"mscandui21.candidate", "mscandui40.candidate", "MSCandUIWindow_Candidate", # IMM candidates
			"TTrayAlert", # 5405: Skype
		)
	if eventName == "reorder":
		# Prevent another flood risk.
		return wClass == "TTrayAlert" # #4841: Skype
	if eventName == "alert" and winuser.getClassName(winuser.getAncestor(windowHandle, winuser.GA_PARENT)) == "ToastChildWindowClass":
		# Toast notifications.
		return True
	if eventName in ("menuEnd", "switchEnd", "desktopSwitch"):
		# #5302, #5462: These events can be fired on the desktop window
		# or windows that would otherwise be blocked.
		# Platform API handlers will translate these events to focus events anyway,
		# so we must allow them here.
		return True
	if windowHandle == winuser.getDesktopWindow():
		# #5595: Events for the cursor get mapped to the desktop window.
		return True

	# #6713: Edge (and soon all UWP apps) will no longer have windows as descendants of the foreground window.
	# However, it does look like they are always  equal to or descendants of the "active" window of the input thread. 
	if wClass.startswith('Windows.UI.Core'):
		gi=winuser.getGUIThreadInfo(0)
		if winuser.isDescendantWindow(gi.hwndActive,windowHandle):
			return True

	fg = winuser.getForegroundWindow()
	fgClassName=winuser.getClassName(fg)
	if wClass == "NetUIHWND" and fgClassName in ("Net UI Tool Window Layered","Net UI Tool Window"):
		# #5504: In Office >= 2013 with the ribbon showing only tabs,
		# when a tab is expanded, the window we get from the focus object is incorrect.
		# This window isn't beneath the foreground window,
		# so our foreground application checks fail.
		# Just compare the root owners.
		if winuser.getAncestor(windowHandle, winuser.GA_ROOTOWNER) == winuser.getAncestor(fg, winuser.GA_ROOTOWNER):
			return True
	if (winuser.isDescendantWindow(fg, windowHandle)
			# #3899, #3905: Covers cases such as the Firefox Page Bookmarked window and OpenOffice/LibreOffice context menus.
			or winuser.isDescendantWindow(fg, winuser.getAncestor(windowHandle, winuser.GA_ROOTOWNER))):
		# This is for the foreground application.
		return True
	if (winuser.user32.GetWindowLongW(windowHandle, winuser.GWL_EXSTYLE) & winuser.WS_EX_TOPMOST
			or winuser.user32.GetWindowLongW(winuser.getAncestor(windowHandle, winuser.GA_ROOT), winuser.GWL_EXSTYLE) & winuser.WS_EX_TOPMOST):
		# This window or its root is a topmost window.
		# This includes menus, combo box pop-ups and the task switching list.
		return True
	return False


def callWithSupportedKwargs(func, *args, **kwargs):
	"""Call a function with only the keyword arguments it supports.
	For example, if myFunc is defined as:
	C{def myFunc(a=None, b=None):}
	and you call:
	C{callWithSupportedKwargs(myFunc, a=1, b=2, c=3)}
	Instead of raising a TypeError, myFunc will simply be called like this:
	C{myFunc(a=1, b=2)}

	While C{callWithSupportedKwargs} does support positional arguments (C{*args}), usage is strongly discouraged due to the
	risk of parameter order differences causing bugs.

	@param func: can be any callable that is not an unbound method. EG:
		- Bound instance methods
		- class methods
		- static methods
		- functions
		- lambdas

		The arguments for the supplied callable, C{func}, do not need to have default values, and can take C{**kwargs} to
		capture all arguments.
		See C{tests/unit/test_extensionPoints.py:TestCallWithSupportedKwargs} for examples.

		An exception is raised if:
			- the number of positional arguments given can not be received by C{func}.
			- parameters required (parameters declared with no default value) by C{func} are not supplied.
	"""
	spec = inspect.getargspec(func)

	# some handlers are instance/class methods, discard "self"/"cls" because it is typically passed implicitly.
	if inspect.ismethod(func):
		spec.args.pop(0)  # remove "self"/"cls" for instance methods
		if not hasattr(func, "__self__"):
			raise TypeError("Unbound instance methods are not handled.")

	# Ensure that the positional args provided by the caller of `callWithSupportedKwargs` actually have a place to go.
	# Unfortunately, positional args can not be matched on name (keyword) to the names of the params in the handler,
	# and so calling `callWithSupportedKwargs` is at risk of causing bugs if parameter order differs.
	numExpectedArgs = len(spec.args)
	numGivenPositionalArgs = len(args)
	if numGivenPositionalArgs > numExpectedArgs:
		raise TypeError("Expected to be able to pass {} positional arguments.".format(numGivenPositionalArgs))

	# Ensure that all arguments without defaults which are expected by the handler were provided.
	# `defaults` is a tuple of default argument values or None if there are no default arguments;
	# if this tuple has N elements, they correspond to the last N elements listed in args.
	numExpectedArgsWithDefaults = len(spec.defaults) if spec.defaults else 0
	if not spec.defaults or numExpectedArgsWithDefaults != numExpectedArgs:
		# get the names of the args without defaults, skipping the N positional args given to `callWithSupportedKwargs`
		# positionals are required for the Filter extension point.
		givenKwargsKeys = set(kwargs.keys())
		firstArgWithDefault = numExpectedArgs - numExpectedArgsWithDefaults
		specArgs = set(spec.args[numGivenPositionalArgs:firstArgWithDefault])
		for arg in specArgs:
			# and ensure they are in the kwargs list
			if arg not in givenKwargsKeys:
				raise TypeError("Parameter required for handler not provided: {}".format(arg))

	if spec.keywords:
		# func has a catch-all for kwargs (**kwargs) so we do not need to filter to just the supported args.
		return func(*args, **kwargs)

	supportedKwargs = set(spec.args)
	for kwarg in kwargs.keys():
		if kwarg not in supportedKwargs:
			del kwargs[kwarg]
	return func(*args, **kwargs)
