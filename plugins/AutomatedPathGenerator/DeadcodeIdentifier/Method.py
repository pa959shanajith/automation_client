class Method:	
	def __init__(self,name,returntype,Modifiers,linenum):
		self.name = name
		self.returntype = returntype
		self.Modifiers = Modifiers
		self.linenum = linenum
		self.formalParameter = {}
		self.localvariables = {}
		self.used = False

	def isUsed(self):
		self.used = True
	
	def getLineNum(self):
		return self.linenum

	def getScope(self):
		return self.Modifiers[0]

	def addFormalParameter(self,formalParameter):
		self.formalParameter.update(formalParameter)

	def addVariable(self,variable):
		self.localvariables.update(variable)

	def getFormalParameter(self):
		return self.formalParameter

	def getLocalVariables(self):
		return self.localvariables

	def getName(self):
		return self.name
