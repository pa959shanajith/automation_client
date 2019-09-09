import re

def DuplicateImports(imports,impDic):
	if list(impDic.keys())[0] in imports:
		return True
	else:
		return False	

def EmptyDoWhileLoop(root):
	return isEmptyStatement(root.child[0])

def EmptyWhileLoop(root):
	return isEmptyStatement(root.child[0])

def EmptyIfStatement(root):
	return isEmptyStatement(root.child[0])

def EmptyForStatement(root):
	return isEmptyStatement(root.child[0])


def EmptyTryCatchBlock(root):
	return isEmptyStatement(root)

def isEmptyStatement(root):
	if not root.has_child():
		return True
	else:
		return False

def isLiteralPresent(Literallst,value):
	presence = False
	key = None
	index = value.find("(String style)")

	if index >0:
		key = value[:index]
		if key in Literallst:
			presence = True
	return presence,key

def isPrivateMethod(objlst,value):
	value = valueExtract(value)
	present = False
	for i in range(0,len(objlst)):
		for method in objlst[i].methods:
			if re.match("private",method.getScope()):
				if re.match(value,method.getName()):
					index = objlst[i].methods.index(method)
					objlst[i].methods[index].isUsed()
					present = True
	return objlst,present

def isStaticImport(value):
	if value and value.find("static"):
		return True
	else:
		return False

def isStringInstantiation(lst):
	if lst[0] == "Sting" and lst[1] == "String":
		return True
	else:
		return False

def JavaLangImport(imports):
	lst = {}
	nimports = {}
	for imp in imports.keys():
		if len(imp)>=len("java.lang"):
			if imp.find("java.lang") == 0:
				lst.update({imp:imports[imp]})
			else:
				nimports.update({imp:imports[imp]})
	return nimports,lst

def UnusedPrivateField(variables):
	lst =[]
	for var in variables.keys():
		if not variables[var].getUsage() and variables[var].getScope().find("private") == 1:
			lst.append([var,variables[var].getType(),variables[var].getLineNum()])
	return lst

def UnusedImports(imports,value):
	var = valueExtract(value)
	present = False
	if var in imports:
		imports[var]["used"] = True
		present = True
	return imports,present


def variableUsage(obj,value):
	present = False
	var = valueExtract(value)
	meth = obj.getCurrentMethod()
	if (meth and (var in meth.localvariables)):
		present =True
		meth.localvariables[var].isUsed()
		obj.updateMethod(meth)
	elif (meth and (var in meth.formalParameter)):
		present = True
		meth.formalParameter[var].isUsed()
		obj.updateMethod(meth)
	elif var in obj.variables:
		present = True
		obj.variables[var].isUsed()

	return obj,present

def privateMethodInBuffer(buff,method):
	count = buff.count(method.getName())
	if count>0:
		method.isUsed()
		while count:
			buff.pop(buff.index(method.getName()))
			count -= 1
	return method,buff

def valueExtract(value):
	prop = []
	while value.find(".") >0:
		word = value[:value.find(".")]
		prop.append(word)
		value = value[value.find(".")+1:]
	if prop:
		var = prop[0]
	else:
		var = value
	
	return var
