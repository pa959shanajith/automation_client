class Object:
	
	def __init__(self,name,parent,imports,lineNum):
		self.imports = {}
		self.methods = []
		self.variables = {}
		self.objects = []
		self.name=name
		self.line = lineNum
		self.parent = parent
		self.addImport(imports)

	def  addType(self,Type):
		self.Type = Type
	
	def getType(self):
		return self.Type

	def addVariable(self,variable):
		self.variables.update(variable)

	def addImport(self,lst):
		for line in lst.keys():
			actualValue = line
			if line.find("*") == -1:
				while line.find(".") != -1:
					line = line[line.find(".") + 1 :]
				if line.find(":") != -1:
					self.imports[line.strip()] = {"value":actualValue,"used": True,"lineNo":lst[actualValue]}
				else:	
					self.imports[line.strip()] = {"value":actualValue,"used": False,"lineNo":lst[actualValue]}

	def setScope(self,scope):
		self.scope = scope

	def getScope(self):
		return self.scope

	def addMethod(self,method):
		self.methods.insert(len(self.methods),method)

	def getName(self):
		return self.name

	def updateMethod(self,method):
		self.methods.pop()
		self.methods.insert(len(self.methods),method)

	def getCurrentMethod(self):
		if self.methods:
			return self.methods[-1]
		else:
			return None 
		
	