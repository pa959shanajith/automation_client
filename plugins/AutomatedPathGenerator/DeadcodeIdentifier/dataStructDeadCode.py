import re
from node import Node
import logging
log = logging.getLogger("dataStructDeadCode.py")

def next_line():
	try:
		line = next(start.f)
		level,lineNum,line = divide(line.strip("\n"))
		return level,lineNum,line
	except StopIteration:
		start.f.close()
		return None,None,None

def divide(line):
	space1 = line.find("#")
	space2 = line.find("#",space1+1)
	level = line[0:space1]
	lineNum = line[space1+1:space2]
	return int(level),int(lineNum),line[space2+1:]

def start():
	try:
		root = None
		start.f = open('ASTTree.txt','rt')
		level, lineNum,line = next_line()
		if re.match("CompilationUnit",line):
			root = Node(line,level,lineNum)
			level,lineNum ,line = next_line()
			make(level,lineNum,line ,root)
	except Exception as e:
		log.error(e)
	start.f.close()
	return root

def make(level,lineNum,line,curr_node,depth=0):
	try:
		if depth <= 3000:
			if line and curr_node:
				if level>curr_node.get_level():
					new = Node(line,level,lineNum)
					new.set_parent(curr_node)
					curr_node.add_child(new)
					level,lineNum,line = next_line()
					make(level,lineNum,line,new,depth=depth+1)
				elif level<=curr_node.get_level():
					make(level,lineNum,line,curr_node.get_parent(),depth=depth+1)
	except Exception as e:
		pass
	return