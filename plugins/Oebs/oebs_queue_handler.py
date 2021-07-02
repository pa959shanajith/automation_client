#oebs_queue_handler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import types

from queue import Queue # Python 3 import
import oebs_start
import logging
log=logging.getLogger('oebs_queue_handler.py')

eventQueue=Queue()
eventQueue.__name__="eventQueue"
generators={}
lastGeneratorObjID=0

def registerGeneratorObject(generatorObj):
	import oebs_core1
	core=oebs_core1.Core()
	global generators,lastGeneratorObjID
	if not isinstance(generatorObj,types.GeneratorType):
		raise TypeError('Arg 2 must be a generator object, not %s'%type(generatorObj))
	lastGeneratorObjID+=1
	log.info("Adding generator %d"%lastGeneratorObjID)
	generators[lastGeneratorObjID]=generatorObj
	core.requestPump()
	return lastGeneratorObjID

def cancelGeneratorObject(generatorObjID):
	global generators
	try:
		del generators[generatorObjID]
	except KeyError:
		pass

def queueFunction(queue,func,*args,**kwargs):
	import oebs_core1
	core=oebs_core1.Core()
	queue.put_nowait((func,args,kwargs))
	oebs_start.get_core().requestPump()

def isRunningGenerators():
	res=len(generators)>0
	log.info("generators running: %s"%res)

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

def isPendingItems(queue):
	if not queue.empty():
		res=True
	else:
		res=False
	return res

def pumpAll():
	import oebs_core1
	core = oebs_core1.Core()
	# This dict can mutate during iteration, so use keys().
	for ID in generators.keys():
		# KeyError could occur within the generator itself, so retrieve the generator first.
		try:
			gen = generators[ID]
		except KeyError:
			# Generator was cancelled. This is fine.
			continue
		#watchdog.alive()
		try:
			next(gen)
		except StopIteration:
			del generators[ID]
		except:
			del generators[ID]
		# Lose our reference so Python can destroy the generator if appropriate.
		del gen
	if generators:
		oebs_start.core.requestPump()
	flushQueue(eventQueue)
