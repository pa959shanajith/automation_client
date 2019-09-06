class Node:
	
	def __init__(self,value,level,lineNum):
		self.level = level
		self.value = self.make_list(value)
		self.lineNum = lineNum
		self.child = []
		self.index = 0

	def set_parent(self,parent):
		self.parent = parent
		return

	def make_list(self,line):
		index = line.find(":")
		if index != -1:
			key = line[0:index]
			value = line[index+1:]
		else:
			key = line
			value = None
		return [key,value]

	def add_child(self,child):
		self.child.append(child)

	def has_child(self):
		if len(self.child) > 0:
			return True
		else:
			return False

	def getLineNum(self):
		return self.lineNum

	def get_level(self):
		return self.level
	
	def get_value(self):
		return(self.value)

	def get_parent(self):
		if self.parent:
			return self.parent
		else:
			raise ValueError("No parent")
			return

	def last_child(self):
		if self.has_child():
			return self.child[-1]
		else:
			return None

	def total_child(self):
		return len(self.child)

	def next_child(self):
		if self.has_child() and self.index <= self.total_child():
			kid = self.child[self.index]
			self.index +=1
			return kid
		else:
			return None

	def set_index(self,index):
		if self.index > index :
			self.index = index
		else:
			raise IndexError("Index out of bound Error")