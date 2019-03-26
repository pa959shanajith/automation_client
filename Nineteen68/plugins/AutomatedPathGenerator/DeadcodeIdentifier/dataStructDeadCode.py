import re
import sys
import fileinput
from node import Node
sys.setrecursionlimit(15000)

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
	start.f = open(r'./ASTTree.txt','rt')
	level, lineNum,line = next_line()
	if re.match("CompilationUnit",line):
		root = Node(line,level,lineNum)
		level,lineNum ,line = next_line()
		make(level,lineNum,line ,root)
		return root
	else:
		return None

def make(level,lineNum,line,curr_node):
	if line and curr_node:
		if level>curr_node.get_level():
			new = Node(line,level,lineNum)
			new.set_parent(curr_node)
			curr_node.add_child(new)
			level,lineNum,line = next_line()
			make(level,lineNum,line,new)
		elif level<=curr_node.get_level():
			make(level,lineNum,line,curr_node.get_parent())
	return