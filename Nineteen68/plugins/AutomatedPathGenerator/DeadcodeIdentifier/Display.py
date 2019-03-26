from Method import Method
from Var import VarInfo
from Object import Object
import re

def displayDuplicateImports(impDic,filePath):
	impValue = (impDic.keys())[0]
	lineNum = impDic.values()[0]
	return [impValue,lineNum,filePath]

def displayDuplicateLiterals(Literal,classname,filePath):
	lst = []
	for key in Literal.keys():
		if Literal[key]["count"] >= 4:
			lst.append([key,classname,",".join(Literal[key]["lineNum"]),filePath])
	return lst

def displayUnusedPrivateField(ls,classname,filePath):
	lst = []
	for val in ls:
		lst.append([val[0],val[1],classname,filePath,val[2]])
	return lst

def displayJavaLangImport(ls,classname,filePath):
	lst = []
	for val in ls.keys():
		lst.append([val,classname,filePath,ls[val]])
	return lst

def displayUnsedFormalParameters(method,Obj,filePath):
	if Obj.getType() == "interface":
		return []
	else:
		ls = displayUnusedVariables(method.getName(),method.getFormalParameter(),Obj.getName(),filePath)
		return ls

def displayUnusedLocalVariables(method,classname,filePath):
	ls = displayUnusedVariables(method.getName(),method.getLocalVariables(),classname,filePath)
	return ls

def displayUnusedPrivateMethod(objlst,filePath):
	ls = []
	for i in range(0,len(objlst)):
		for method in objlst[i].methods:
			if re.match("private",method.getScope()) and not method.used:
				ls.append([method.getName(),method.getLineNum(),objlst[i].getName(),filePath])
	return ls


def displayUnusedImports(imports,classname,filePath):
	ls = []
	for key in imports.keys():
		if not imports[key]["used"]:
			ls.append([imports[key]["value"],classname,filePath,imports[key]["lineNo"]])
	return ls

def displayUnusedVariables(methodname,variables,classname,filePath):
	ls = []
	for key in variables.keys():
		varinfo = variables[key]
		if not varinfo.getUsage():
			ls.append([key,varinfo.getType(), methodname,classname,filePath,varinfo.getLineNum()])
	return ls    