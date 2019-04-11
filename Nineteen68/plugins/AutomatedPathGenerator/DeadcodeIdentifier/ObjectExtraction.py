import re
import sys
from Object import Object
from Method import Method
import Display
from Var import VarInfo
import Check
import logging
log = logging.getLogger('ObjectExtraction.py')
sys.setrecursionlimit(15000)

def main(root,data,filePath):
	try:
		main.nested = -1
		main.obj = []
		main.imports = {}
		main.buffer = []
		main.StaticImports = []
		main.showData = data
		main.filePath = filePath
		main.Literal = {}
		objectExtract(root)
	except Exception as e:
		log.error(e)
	sys.setrecursionlimit(1000)
	return main.showData

def additiveExpressionExtraction(root):

	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('PrimaryExpression',line):
			primaryExpressionExtraction(root.child[i])
	return

def AllocationExpressionExtraction(root):
	for i in range(0,root.total_child()):
		line = (root.child[i]).get_value()[0]
		if re.match("ClassOrInterfaceType",line):
			AllocatorClass = classOrInterfaceTypeExtraction(root.child[i])
		elif re.match("Arguments",line):
			argumentsExtraction(root.child[i])
		elif re.match("PrimitiveType",line):
			initializerClassName = root.child[i].get_value()[1]
		elif re.match("ArrayDimsAndInits",line):
			ArrayDimsAndInitsExtraction(root.child[i])
		elif re.match("ClassOrInterfaceBody",line):
			classOrInterfaceBodyExtraction(root.child[i])
	return

def annotationExtraction(root):
	line = root.child[0].get_value()[0]
	if re.match("MarkerAnnotation",line):
		markerAnnotationExtraction(root.child[0])
	elif re.match("SingleMemberAnnotation",line):
		singleMemberAnnotationExtraction(root.child[0])


def ArrayDimsAndInitsExtraction(root):
	value = ""
	for i in range(0,root.total_child()):
		line = (root.child[i]).get_value()[0]
		if re.match("Exression",line):
			value = "[" + expressionExtraction(root.child[i]) + "]" + value
	return 
def argumentsExtraction(root):
	Variable=""
	if root.has_child() is False:
		return 
	root=root.child[0]
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('Expression',line):
			expressionExtraction(root.child[i])
	return

def blockExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('BlockStatement',line):
			blockStatementExtraction(root.child[i])
	return

def blockStatementExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('Statement',line):
			statementExtraction(root.child[i])
		elif re.match('LocalVariableDeclaration',line):
			Variables = localVariableExtraction(root.child[i])
			(main.obj[main.nested].getCurrentMethod()).addVariable(Variables)
	return

def castExpressionExtraction(root):
	Variable=""
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('Type',line):
			typeVariableExtraction(root.child[i])
		elif re.match('PrimaryExpression',line):
			primaryExpressionExtraction(root.child[i])
	return

def catchStatementExtraction(root):
	for i in range(0,root.total_child()):
		line = (root.child[i]).get_value()[0]
		if re.match("FormalParameter",line):
			formalParameterExtraction(root.child[i])
		elif re.match("Block",line):
			if Check.EmptyTryCatchBlock(root.child[i]):
				main.showData["Empty Try/Catch Block"].append([main.obj[main.nested].getCurrentMethod().getName(),
															  main.obj[main.nested].getName(),
															  main.filePath,root.getLineNum()]
															  )
			else:
				blockExtraction(root.child[i])
	return

def classOrInterfaceBodyExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('ClassOrInterfaceBodyDeclaration',line):
			classOrInterfaceBodyDeclaration_OnlyField_Extraction(root.child[i])

	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('ClassOrInterfaceBodyDeclaration',line):
			classOrInterfaceBodyDeclarationExtraction(root.child[i])
	return

def classOrInterfaceBodyDeclaration_OnlyField_Extraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("FieldDeclaration",line):
			Variables = FieldDeclarationExtraction(root.child[i])
			main.obj[main.nested].addVariable(Variables)

def classOrInterfaceBodyDeclarationExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('MethodDeclaration',line):
			methodExtraction(root.child[i])
		elif re.match('ClassOrInterfaceDeclaration',line):
			main.nested +=1
			classOrInterfaceExtraction(root.child[i])
			main.nested -= 1
		elif re.match("FieldDeclaration",line):
			FieldDeclarationExtraction(root.child[i])
		elif re.match("Annotation",line):
			annotationExtraction(root.child[i])
		elif re.match("ConstructorDeclaration",line):
			constructorDeclarationExtraction(root.child[i])
	return

def classOrInterfaceExtraction(root):
	ClassOrInterfaceName=(root.get_value())[1]
	className = ClassOrInterfaceName[0:ClassOrInterfaceName.find("(")]
	if main.nested==0:
		main.imports,dic = Check.JavaLangImport(main.imports)
		main.showData["Java Lang Imports"].extend(Display.displayJavaLangImport(dic,className,main.filePath))
		
	main.obj.insert(main.nested,Object(className,None,main.imports,root.getLineNum()))
	Property=[]
	while ClassOrInterfaceName.find("(")!=-1:
		Property.append(ClassOrInterfaceName[ClassOrInterfaceName.find("(")+1:ClassOrInterfaceName.find(")")])
		ClassOrInterfaceName=ClassOrInterfaceName.replace(ClassOrInterfaceName[ClassOrInterfaceName.find("("):ClassOrInterfaceName.find(")")+1],"")
	ClassOrInterface=Property.pop()
	
	if ClassOrInterface=='class':
		main.obj[main.nested].addType("class")
	elif ClassOrInterface=='nested':
		main.obj[main.nested].addType(Property.pop())
	elif ClassOrInterface =="interface":
		main.obj[main.nested].addType("interface")
	
	main.obj[main.nested].setScope(Property.pop())

	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('ClassOrInterfaceBody',line):
			classOrInterfaceBodyExtraction(root.child[i])
		elif re.match("ImplementsList",line):
			implementsListExtraction(root.child[i])
		elif re.match("ExtendsList",line):
			extendsListExtraction(root.child[i])
	return

def classOrInterfaceTypeExtraction(root):
	value = root.get_value()[1]
	main.obj[0].imports ,present= Check.UnusedImports(main.obj[0].imports,value)
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("TypeArguments",line):
			value = value + "<" + typeArgumentsExtraction(root.child[i]) + ">"
	return value



def constructorDeclarationExtraction(root):
	line=(root.get_value())[1]
	Modifiers = []
	while line.find("(")!=-1:
		Modifiers.append(line[line.find("(")+1:line.find(")")])
		line=line.replace(line[line.find("("):line.find(")")+1],"")
	constructor = Method(main.obj[main.nested].getName()+"(Constructor)",
					None,
					Modifiers,
					root.getLineNum()
					)

	for i in range(0,root.total_child()):
		line=(root.child[i]).get_value()[0]
		if re.match("BlockStatement",line):
			blockStatementExtraction(root.child[i])
		elif re.match('FormalParameters',line):
			constructor.addFormalParameter(formalParametersExtraction(root.child[i]))
			main.obj[main.nested].addMethod(constructor)
		
	main.showData["Unused Local Variable"].extend(Display.displayUnusedLocalVariables(main.obj[main.nested].getCurrentMethod(),
																						main.obj[main.nested].getName(),
																						main.filePath
																						))
	main.showData["Unused Formal Parameter"].extend(Display.displayUnsedFormalParameters(main.obj[main.nested].getCurrentMethod(),
																						main.obj[main.nested],
																						main.filePath
																						))
	return


def conditionalExpressionExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("InstanceOfExpression",line):
			instanceOfExpressionExtraction(root.child[i])
		elif re.match("Expression",line):
			expressionExtraction(root.child[i])
		elif re.match("PrimaryExpression",line):
			primaryExpressionExtraction(root.child[i])
def conditionalAndExpressionExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("EqualityExpression",line):
			equalityExpressionExtraction(root.child[i])
		elif re.match("PrimaryExpression",line):
			primaryExpressionExtraction(root.child[i])

def conditionalOrExpressionExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("EqualityExpression",line):
			equalityExpressionExtraction(root.child[i])
		elif re.match("UnaryExpressionNotPlusMinus",line):
			unaryExpressionNotPlusMinusExtraction(root.child[i])
	
def doStatementExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("Statement",line):
			if Check.EmptyDoWhileLoop(root.child[i]):
				main.showData["Empty Do While Loop"].append([main.obj[main.nested].getCurrentMethod().getName(),
															main.obj[main.nested].getName(),
															main.filePath,
															root.getLineNum()
															])
			else:
				statementExtraction(root.child[i])
		elif re.match("Expression",line):
			expressionExtraction(root.child[i])

def equalityExpressionExtraction(root):
	for i in range(0,root.total_child()):		
		line=(root.child[i].get_value())[0]
		if re.match('PrimaryExpression',line):

			primaryExpressionExtraction(root.child[i])
	return
			
def expressionExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('PrimaryExpression',line):
			primaryExpressionExtraction(root.child[i])	
		elif re.match('RelationalExpression',line):
			relationalExpressionExtraction(root.child[i])
		elif re.match('EqualityExpression',line):
			equalityExpressionExtraction(root.child[i])
		elif re.match('AdditiveExpression',line):
			additiveExpressionExtraction(root.child[i])
		elif re.match('CastExpression',line):		
			castExpressionExtraction(root.child[i])
		elif re.match("ConditionalAndExpression",line):
			conditionalAndExpressionExtraction(root.child[i])
		elif re.match("ConditionalOrExpression",line):
			conditionalOrExpressionExtraction(root.child[i])
		elif re.match("ConditionalExpression",line):
			conditionalExpressionExtraction(root.child[i])
		elif re.match("InstanceOfExpression",line):
			instanceOfExpressionExtraction(root.child[i])
	return

def extendsListExtraction(root):
	line = root.child[0].get_value()[0]
	if re.match("ClassOrInterfaceType",line):
		classOrInterfaceTypeExtraction(root.child[0])

def FieldDeclarationExtraction(root):
	Variables = {}
	scope = root.get_value()[1]
	for i in range(0,root.total_child()):
		line = (root.child[i]).get_value()[0]
		if re.match("Type",line):
			VariableType = typeVariableExtraction(root.child[i])
		elif re.match("VariableDeclarator",line):
			VariableName,VariableInitialized = variableExtraction(root.child[i])
			Variables.update({VariableName:VarInfo(VariableType,scope,VariableInitialized,root.getLineNum())})
	return Variables

def formalParametersExtraction(root):
	line=(root.get_value())[1]
	Variables = {}
	NoOfFormalParameters=int(line[line.find("(")+1:line.find(")")])
	if NoOfFormalParameters>0:
		for i in range(0,root.total_child()):
			Variables.update(formalParameterExtraction(root.child[i]))
	return Variables

def formalParameterExtraction(root):
	line = root.get_value()[1]
	scope = line[line.find("(")+1:line.find(")")]
	VariableName=''
	VariableType=''
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('Type',line):
			VariableType=typeVariableExtraction(root.child[i])
		elif re.match('VariableDeclaratorId',line):
			VariableName=(root.child[i].get_value())[1]	
		elif re.match("Annotation",line):
			annotationExtraction(root.child[i])
	return {VariableName:VarInfo(VariableType,scope,linenum=root.getLineNum())}

def forInitExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('LocalVariableDeclaration',line):
			main.obj[main.nested].getCurrentMethod().addVariable(localVariableExtraction(root.child[i]))
	return

def forStatementExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]	
		if re.match("ForInit",line):
			forInitExtraction(root.child[i])
		elif re.match("ForUpdate",line):
			forUpdateExtraction(root.child[i])
		elif re.match("Expression",line):
			expressionExtraction(root.child[i])
		elif re.match("Statement",line):
			if Check.EmptyForStatement(root.child[i]):
				main.showData["Empty For Loop"].append([main.obj[main.nested].getCurrentMethod().getName(),
														main.obj[main.nested].getName(),
														main.filePath,
														root.getLineNum()
														])
			else:
				statementExtraction(root.child[i])
		elif re.match("LocalVariableDeclaration",line):
			localVariableExtraction(root.child[i])
	return
			
def forUpdateExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]	
		if re.match("StatementExpressionList",line):
			statementExpressionListExtraction(root.child[i])
	return

def ifStatementExtraction(root):
	for i in range(0,root.total_child()):
		line = (root.child[i].get_value())[0]
		if re.match("Statement",line):
			if Check.EmptyIfStatement(root.child[i]):
				main.showData["Empty If Statement"].append([main.obj[main.nested].getCurrentMethod().getName(),
															main.obj[main.nested].getName(),
															main.filePath,
															root.getLineNum()
															])
			else:
				statementExtraction(root.child[i])
		elif re.match("Expression",line):
			expressionExtraction(root.child[i])
	return

def instanceOfExpressionExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("PrimaryExpression",line):
			primaryExpressionExtraction(root.child[i])
		elif re.match("Type",line):
			typeVariableExtraction(root.child[i])
	return

def implementsListExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("ClassOrInterfaceType",line):
			classOrInterfaceTypeExtraction(root.child[i])
	return

def importExtraction(root):
	return {(root.child[0]).get_value()[1]:(root.child[0]).getLineNum()}
	
def localVariableExtraction(root):
	Prop=(root.get_value())[1]
	Property=[]
	Variables = {}
	while Prop.find("(")!=-1:
		Property.append(Prop[Prop.find("(")+1:Prop.find(")")])
		Prop=Prop.replace(Prop[Prop.find("("):Prop.find(")")+1],"")
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]	
		if re.match("Type",line):
			VariableType=typeVariableExtraction(root.child[i])
		elif re.match('VariableDeclarator',line):
			VariableName,VariableInitialized = variableExtraction(root.child[i])
			Variables.update({VariableName:VarInfo(VariableType,
													Property,
													VariableInitialized,
													root.getLineNum()
													)})
	

	return Variables

def memberValueArrayInitializer(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("MemberValue",line):
			memberValueExtraction(root.child[i])
	return

def memberValueExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("PrimaryExpression",line):
			primaryExpressionExtraction(root.child[i])
		elif re.match("MemberValueArrayInitializer",line):
			memberValueArrayInitializer(root.child[i])
	return

def markerAnnotationExtraction(root):
	line = root.child[0].get_value()[0]
	if re.match("Name",line):
		nameExtraction(root.child[0])
	return


def methodDeclaratorExtraction(root):
	Variables = {}
	if(len(root.child)>0):
		Variables = formalParametersExtraction(root.child[0])
	return Variables


def methodExtraction(root):
	line=(root.get_value())[1]
	Modifiers = []
	while line.find("(")!=-1:
		Modifiers.append(line[line.find("(")+1:line.find(")")])
		line=line.replace(line[line.find("("):line.find(")")+1],"")
	for i in range(0,root.total_child()):
		line=(root.child[i]).get_value()[0]
		if re.match('ResultType',line):
			ResultType=resultTypeExtraction(root.child[i])
		elif re.match('NameList',line):
			nameListExtraction(root.child[i])	
		elif re.match('MethodDeclarator',line):
			MethodName=(root.child[i].get_value())[1]
			method = Method(MethodName,ResultType,Modifiers,(root.child[i]).getLineNum()) ##name,returntype,scope,Modifiers
			if re.match("private", Modifiers[0]): 
				method,main.buffer = Check.privateMethodInBuffer(main.buffer,method)
			method.addFormalParameter(methodDeclaratorExtraction(root.child[i]))
			main.obj[main.nested].addMethod(method)
		elif re.match('Block',line):
			methodExtraction.NumOfReturnStatements = 0
			blockExtraction(root.child[i])
			if methodExtraction.NumOfReturnStatements >1:
				main.showData["Multiple Return Statement"].append([MethodName,
																main.obj[main.nested].getName(),
																main.filePath,root.getLineNum()
																])
				methodExtraction.NumOfReturnStatements = 0
	main.showData["Unused Local Variable"].extend(Display.displayUnusedLocalVariables(main.obj[main.nested].getCurrentMethod(),
																						main.obj[main.nested].getName(),
																						main.filePath
																						))
	main.showData["Unused Formal Parameter"].extend(Display.displayUnsedFormalParameters(main.obj[main.nested].getCurrentMethod(),
																						main.obj[main.nested],
																						main.filePath
																						))
	return

def nameExtraction(root):
	value = root.get_value()[1]
	value =value.strip()
	if len(main.obj) ==0:
		for imp in (main.imports).keys():
			if imp.find(value,len(imp) - len(value),len(imp)) > 0:
				main.imports.update({imp+ ":" : (main.imports).pop(imp)})

	elif len(main.obj)>0:
		main.obj[main.nested],present1 = Check.variableUsage(main.obj[main.nested],value)
		main.obj[0].imports ,present2= Check.UnusedImports(main.obj[0].imports,value)
		main.obj,present3 = Check.isPrivateMethod(main.obj,value)
		if (not present2) or (not present1) or (not present3):
			main.buffer.append(value)
	return

def nameListExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("Name",line):
			nameExtraction(root.child[i])
	return

def objectExtract(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('PackageDeclaration',line):
			pass
		elif re.match('ImportDeclaration',line):
			if Check.isStaticImport((root.child[i]).get_value()[1]):
				main.StaticImports.append((root.child[i]).getLineNum())

			impDic = importExtraction(root.child[i])
			if Check.DuplicateImports(main.imports,impDic):
				main.showData["Duplicate Imports"].extend(Display.displayDuplicateImports(impDic,main.filePath))
			else:
				main.imports.update(impDic)
		elif re.match('TypeDeclaration',line):
			if len(main.StaticImports) >= 4:
					main.showData["Too Many Static Imports"].extend([main.filePath,",".join(main.StaticImports)])
			typeExtraction(root.child[i])
	for i in range(0,len(main.obj)):
		ls = Check.UnusedPrivateField(main.obj[i].variables)
		main.showData["Unused Private Field"].extend(Display.displayUnusedPrivateField(ls,main.obj[i].getName(),main.filePath))
	return
	
def postfixExpressionExtraction(root):
	PostfixOperator=(root.get_value())[1]
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('PrimaryExpression',line):
			primaryExpressionExtraction(root.child[i])
	return 
	
def preDecrementExpressionExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]

		if re.match('PrimaryExpression',line):
			primaryExpressionExtraction(root.child[i])
	
	return 
	
def preIncrementExpressionExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('PrimaryExpression',line):
			primaryExpressionExtraction(root.child[i])
	return 
	
def primaryExpressionExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('PrimaryPrefix',line):
			primaryPrefixExtraction(root.child[i])
		elif re.match('PrimarySuffix',line):
			primarySuffixExtraction(root.child[i])
	return

def primaryPrefixExtraction(root):
	if root.has_child():
		line = (root.child[0]).get_value()[0]
		if re.match('Literal',line):
			value = root.child[0].get_value()[1]
			if(value != None):
				presence,key = Check.isLiteralPresent(main.Literal,value)
			else:
				presence = False
				key = None
			if presence:
				main.Literal[key]["count"] += 1
				main.Literal[key]["lineNum"].append(str(root.child[0].getLineNum()))
			elif not presence and key:
				main.Literal.update({key:{"count":1,"lineNum":[str(root.child[0].getLineNum())]}})
								
		elif re.match("AllocationExpression",line):
			AllocationExpressionExtraction(root.child[0])
		
		elif re.match("Name",line):
			nameExtraction(root.child[0])
	return 	

def primarySuffixExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('Arguments',line):
			argumentsExtraction(root.child[i])
	return
	

def referenceTypeExtraction(root):
	line = root.get_value()[1]
	count = ""
	ReferenceType = ""
	if line:
		while(line.find("[")) != -1:
			count = count + "[]"
			line = line[line.find("[")+1 : ]
	if(len(root.child)>0):
		line = (root.child[0].get_value())[0]
		if re.match("ClassOrInterfaceType",line):
			ReferenceType = classOrInterfaceTypeExtraction(root.child[0])
		elif re.match("PrimitiveType",line):
			ReferenceType = root.child[0].get_value()[1]
	return {ReferenceType:count}
	
def relationalExpressionExtraction(root):
	RelationalOperator=(root.get_value())[1]
	RelationalExpression=""
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('PrimaryExpression',line):
			primaryExpressionExtraction(root.child[i])
		
def resultTypeExtraction(root):
	resultType = root.get_value()[1]
	if root.has_child():
		for i in range(0,root.total_child()):
			line=(root.child[i].get_value())[0]
			if re.match('Type',line):
				resultType = typeVariableExtraction(root.child[i])

	return resultType
				
def returnStatementExtraction(root):
	Variable=""
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('Expression',line):
			expressionExtraction(root.child[i])
	return

def singleMemberAnnotationExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("Name",line):
			nameExtraction(root.child[i])
		elif re.match("MemberValue",line):
			memberValueExtraction(root.child[i])
	return

def statementExpressionExtraction(root):
	Variable=""
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('PrimaryExpression',line):
			primaryExpressionExtraction(root.child[i])
		
		elif re.match('AssignmentOperator',line):
			statementExpressionExtraction.AssignmentOperator= True
			
		elif re.match('Expression',line):
			expressionExtraction(root.child[i])
			statementExpressionExtraction.AssignmentOperator= False
	
		elif re.match('PostfixExpression',line):
			postfixExpressionExtraction(root.child[i])
		
		elif re.match('PreIncrementExpression',line):
			preIncrementExpressionExtraction(root.child[i])

		elif re.match('PreDecrementExpression',line):
			preDecrementExpressionExtraction(root.child[i])

	return 
	
def statementExpressionListExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('StatementExpression',line):
		
			statementExpressionExtraction(root.child[i])
	return 
	
def statementExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		
		if re.match('StatementExpression',line):
			statementExpressionExtraction(root.child[i])
		
		elif re.match('ForStatement',line):
			forStatementExtraction(root.child[i])
		
		elif re.match('ReturnStatement',line):
			methodExtraction.NumOfReturnStatements += 1
			returnStatementExtraction(root.child[i])
		
		elif re.match("Block",line): 
			blockExtraction(root.child[i])
		
		elif re.match("IfStatement",line): 
			ifStatementExtraction(root.child[i])
		
		elif re.match("WhileStatement",line): 
			whileStatementExtraction(root.child[i])
		
		elif re.match("EmptyStatement",line): 
			return
		
		elif re.match("BreakStatement",line):
			pass
		
		elif re.match("SwitchStatement",line):
			switchStatementExtraction(root.child[i])
		
		elif re.match("TryStatement",line):  ## Added by nikita
			tryStatementExtraction(root.child[i])
		
		elif re.match("DoStatement",line):
			doStatementExtraction(root.child[i])
		
		elif re.match("SynchronizedStatement",line):
			synchronizedStatementExtraction(root.child[i])
	return

def switchLabelExtraction(root):
	if root.get_value()[1]:
		root.get_value()[1]
	elif re.match("Expression",root.get_value()[0]):
		expressionExtraction(root.child[0])
	return

def switchStatementExtraction(root):
	labels = []
	for i in range(0,root.total_child()):
		child = root.child[i]
		line = child.get_value()[0]
		if re.match("Expression",line):
			expressionExtraction(child)
		elif re.match("SwitchLabel",line):
			labels.append(switchLabelExtraction(child))
		elif re.match("BlockStatement",line):
			blockStatementExtraction(child)
	return

def synchronizedStatementExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("Exrepession",line):
			expressionExtraction(root.child[i])
		elif re.match("Block",line):
			blockExtraction(root.child[i])
	return

def tryStatementExtraction(root):
	for i in range(0,root.total_child()):
		line = (root.child[i]).get_value()[0]
		if re.match("Block",line):
			if Check.EmptyTryCatchBlock(root.child[i]):
				main.showData["Empty Try/Catch Block"].append([main.obj[main.nested].getCurrentMethod().getName(),
															  main.obj[main.nested].getName(),
															  main.filePath
															  ])
			else:
				blockExtraction(root.child[i])
		elif re.match("CatchStatement",line):
			catchStatementExtraction(root.child[i])
	return

def typeArgumentExtraction(root):
	value = ""
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("ReferenceType",line):
			value = referenceTypeExtraction(root.child[i])
			value = list(value.keys())[0]
	return value

def typeArgumentsExtraction(root):
	value = ""
	if root.total_child() >1:
		var = []
		for i in range(0,root.total_child()):
			line = root.child[i].get_value()[0]
			if re.match("TypeArgument",line):
				var.append(typeArgumentExtraction(root.child[i]))
		value = ",".join(var) 
	elif root.total_child() == 1:
		line = root.child[0].get_value()[0]
		if re.match("TypeArgument",line):
			value = typeArgumentExtraction(root.child[0]) 
	return value

def typeExtraction(root):
	ls = []
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('ClassOrInterfaceDeclaration',line):
			main.nested += 1
			classOrInterfaceExtraction(root.child[i])
			main.nested -= 1
		elif re.match('Annotation',line):
			annotationExtraction(root.child[i])

	ls = Display.displayUnusedImports(main.obj[0].imports,main.obj[0].getName(),main.filePath)
	main.showData["Unused Imports"].extend(ls)
	
	ls = Display.displayUnusedPrivateMethod(main.obj,main.filePath)
	main.showData["Unused Private Method"].extend(ls)
	
	ls = Display.displayDuplicateLiterals(main.Literal,main.obj[0].getName(),main.filePath)
	main.showData["Avoid Duplicate Literals"].extend(ls)
	
	return
	
def typeVariableExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('ReferenceType',line):
			ReferenceType=referenceTypeExtraction(root.child[i])
			return ReferenceType
		elif re.match('PrimitiveType',line):
			return {(root.child[i].get_value())[1]:""}

def unaryExpressionNotPlusMinusExtraction(root):
	for i in range(0,root.total_child()):
		line = root.child[i].get_value()[0]
		if re.match("PrimaryExpression",line):
			primaryExpressionExtraction(root.child[i])
	return
			
def variableExtraction(root):
	VariableName = None
	VariableInitialized = False
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('VariableDeclaratorId',line):
			Variable=(root.child[i].get_value())[1]
			VariableName = Variable
		elif re.match('VariableInitializer',line):
			variableInitializerExtraction(root.child[i])
			VariableInitialized = True
	return VariableName,VariableInitialized
	
def variableInitializerExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('Expression',line):
			expressionExtraction(root.child[i])
	return
			
def whileStatementExtraction(root):
	for i in range(0,root.total_child()):
		line=(root.child[i].get_value())[0]
		if re.match('Expression',line):
			Condition=expressionExtraction(root.child[i])	
		elif re.match('Statement',line):
			if Check.EmptyWhileLoop(root.child[i]):
				main.showData["Empty While Loop"].append([main.obj[main.nested].getCurrentMethod().getName(),
														  main.obj[main.nested].getName(),
														  main.filePath,
										    			  root.getLineNum()])
			else:
				statementExtraction(root.child[i])
	return