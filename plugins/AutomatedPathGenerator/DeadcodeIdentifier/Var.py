class VarInfo:
	def __init__(self,Type,scope,initialized = False,linenum = -1):
		self.scope = scope
		self.initialized = initialized
		self.Type = Type
		self.used = False
		self.linenum = linenum

	def getLineNum(self):
		return self.linenum

	def getUsage(self):
		return self.used

	def getType(self):
		return str(self.Type)

	def getScope(self):
		return self.scope
		
	def isUsed(self):
		self.used = True
