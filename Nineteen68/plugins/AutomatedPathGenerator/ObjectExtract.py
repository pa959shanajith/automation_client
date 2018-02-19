import re
import sys
sys.setrecursionlimit(15000)

FlowChart = []  # List of Flow Chart Nodes (addNodes)
Classes = []  # List of all the Classes (addClass)
PossibleMethods = []  # List of all PossibleMethods (addPossibleMethod)
VarStorage = {}  # Storing {Variable Name(key),Variable Type(value)}

PresentClass = None  # For Method Linking Purpose

# List of ASTTree data structure's root (structure can be found in
# dataStruct.py)
ASTNode = []
# Handling AnonymousInnerClass (Main use in allocationExpressionExtraction)
AnonymousInnerClass = -1
# Storing AnonymousInnerClass FlowChart Node No (Main use in
# allocationExpressionExtraction)
s = []

# Used for BreakStatement (Use
# in-statementExtraction,forStatementExtraction,switchStatementExtraction,whileStatementExtraction)
Break = False
# Used for ContinueStatement (Use
# in-statementExtraction,forStatementExtraction,whileStatementExtraction)
Continue = False
# Stores BreakStatement FlowChart Node No (Use
# in-statementExtraction,forStatementExtraction,switchStatementExtraction,whileStatementExtraction)
BreakPos = []
# Used for BreakStatement (Use
# in-statementExtraction,forStatementExtraction,switchStatementExtraction,whileStatementExtraction)
ForOrSwitch = None
# Stores ContinueStatement FlowChart Node No (Use
# in-statementExtraction,forStatementExtraction,whileStatementExtraction)
ContinuePos = []
Ternary = False  # for arguments list ternary statement
TernaryPos = []
Label = {}

'''FlowChart Node (Shape,Text,Child Node Nos,Parent Node Nos)'''
def addNodes(shape, text, parent, child):
	if parent is None:
		return {"shape": shape, "text": text, "parent": parent, "child": child}
	else:
		return {"shape": shape, "text": text,
				"parent": [parent], "child": child}


'''Class Node (Name,FlowChart Node No,Methods,Constructors,Extend Name,Implements Name)'''
def addClass(name, position):
	'''Method key has a dictionary value for handling same method with different no. of arguments.'''
	return {"name": name, "position": position, "methods": {},
			"constructors": [], "extends": None, "implements": None}


'''Possible Method Node For Method Linking
(Method call or new Class made(Constructor Call),Possible Method Name,Possible Method FlowChart Node No,Class name from which it is called,No. of Arguments,Type of Arguments,FlowChart Node No after linking)'''
def addPossibleMethod(methodOrClassCall, posMethod, nodeNo):
	return {"MethodOrClassCall": methodOrClassCall, "PosMethod": posMethod, "NodeNo": nodeNo,
			"Class": None, "NoOfArguments": -1, "typeOfArguments": [], "ParentNodeNo": None}


'''Constructor Node (No. Of Arguments,Arguments Name(str),FlowChart Node No)'''
def addConstructor(NodeNo, NoOfFormalParameters, Variables):
	return {"NoOfFormalParameters": NoOfFormalParameters,
			"Variables": Variables, "NodeNo": NodeNo}


'''Method Node
(FlowChart Node No,Return Type,Method Name,No. of Arguments,Arguments Name(str),Access Modifiers)'''
def addMethod(NodeNo, ResultType, MethodName,
			  NoOfFormalParameters, Variables, MethodType):
	return {"NodeNo": NodeNo, "ResultType": ResultType, "MethodName": MethodName,
			"NoOfFormalParameters": NoOfFormalParameters, "Variables": Variables, "MethodType": MethodType}


'''AdditiveExpression (handles +,- operations) '''
def additiveExpressionExtraction(root):
	global Ternary, TernaryPos
	# gives the arithmetic operation sign(+/-)
	AdditiveOperator = ASTNode[root]["value"][1]
	Possibility = 0
	Variable = ""
	I = -1
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]
					   ]["value"][0]  # Label of the child
		if re.match('PrimaryExpression', line):
			Possible, Var = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, Var = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, Var = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, Var = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, Var = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, Var = castExpressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, Var = unaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, Var = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, Var = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, Var = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, Var = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, Var = expressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			Var = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Var = Var[:Var.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, Var = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ShiftExpression', line):
			Possible, Var = shiftExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AndExpression', line):
			Possible, Var = andExpressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('InclusiveOrExpression', line):
			Possible, Var = inclusiveOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		# print Variable
		if I == 1:  # For ConditionalExpression as it gives list
			Ternary = True
			TernaryPos = Var
			Variable = Variable + 'ternaryExpression'
		else:
			Variable = Variable + Var
		'''Add the additive operator in between two variables for display'''
		if i != len(ASTNode[root]["child"]) - 1:
			Variable = Variable + AdditiveOperator
		# if last child,then additive variable will not be concatenated.

		'''Finding the type of variables like n-1,a+b
		E.g: n-1
		if n is of int type then,n-1 will now become of int type and will be added in VarStorage.
		'''
		if i != 0:
			Var1 = Variable[:Variable.rfind(AdditiveOperator)]
			Var2 = Variable[Variable.rfind(AdditiveOperator) + 1:]
			if Var1 in VarStorage and Var2 in VarStorage:
				if VarStorage[Var1] == VarStorage[Var2]:
					VarStorage.update({Variable: VarStorage[Var2]})
	return Possibility, Variable


'''AllocationExpression (handles new keyword)'''
def allocationExpressionExtraction(root):
	# This will link the anonymous inner classes with the respected statement
	global AnonymousInnerClass, s
	Possibility = 0
	Variables = "new "  # new keyword added for display purpose
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("ClassOrInterfaceType", line):
			Variable = Variable + \
				ASTNode[ASTNode[root]["child"][i]]["value"][1]
			if len(ASTNode[ASTNode[root]["child"][i]]["child"]) > 0:
				V = classOrInterfaceTypeExtraction(ASTNode[root]["child"][i])
				Variable = Variable + V
		elif re.match("Arguments", line):
			Possible, V = argumentsExtraction(ASTNode[root]["child"][i])
			Variable = Variable + "(" + V + ")"
			Possibility = Possibility + Possible
		elif re.match("PrimitiveType", line):
			Variable = Variable + \
				ASTNode[ASTNode[root]["child"][i]]["value"][1]  # int,char,etc
		elif re.match("ArrayDimsAndInits", line):
			Possible, V = arrayDimsAndInitsExtraction(
				ASTNode[root]["child"][i])
			Variable = Variable + V
			Possibility = Possibility + Possible
		elif re.match("ClassOrInterfaceBody", line):
			'''Anonymous Inner Class'''
			Variable = Variable + "{}"
			if len(ASTNode[ASTNode[root]["child"][i]]["child"]) > 0:
				s = []  # Initially start with an empty list
				classOrInterfaceBodyExtraction(ASTNode[root]["child"][i])
				# print index
				AnonymousInnerClass = 1  # Anonymous Inner Class Detected.

	'''New Class variable made so its respected constructor needs to be called.'''
	Variables = Variables + Variable
	# 'class' means its possible constructor call type.
	PossibleMethods.append(addPossibleMethod("Class", Variable, -1))
	ArgumentName = Variable[Variable.find(
		"(") + 1:Variable.rfind(")")]  # Arguments
	if ArgumentName == '':  # Empty Argument
		PossibleMethods[len(PossibleMethods) - 1]["NoOfArguments"] = 0
	else:
		k = 0
		NoOfArguments = 0
		while(ArgumentName.find(',', k) != -1):
			x = ArgumentName[:ArgumentName.find(',', k)]
			if x in VarStorage:  # Finding the type of argument in VarStorage
				PossibleMethods[len(PossibleMethods) -
								1]["typeOfArguments"].append(VarStorage[x])
				ArgumentName = ArgumentName.replace(
					ArgumentName[:ArgumentName.find(',', k) + 1], "")
				NoOfArguments = NoOfArguments + 1
			# Handles Cast Arguments Eg.(byte)1 will be handled as 1.
			elif x[x.find(")") + 1:] in VarStorage:
				PossibleMethods[len(
					PossibleMethods) - 1]["typeOfArguments"].append(VarStorage[x[x.find(")") + 1:]])
				ArgumentName = ArgumentName.replace(
					ArgumentName[:ArgumentName.find(',', k) + 1], "")
				NoOfArguments = NoOfArguments + 1
			elif x[:x.find("[")] in VarStorage:  # Handles array elements
				y = VarStorage[x[:x.find("[")]]
				y = y[:y.find("[")]
				noOfBrackets = x.count('[')
				y = y + ("[]" * noOfBrackets)
				PossibleMethods[len(PossibleMethods) -
								1]["typeOfArguments"].append(y)
				ArgumentName = ArgumentName.replace(
					ArgumentName[:ArgumentName.find(',', k) + 1], "")
				NoOfArguments = NoOfArguments + 1
			else:
				k = ArgumentName.find(',', k) + 1

		'''Last Argument Handled similarly like the above.'''
		if ArgumentName in VarStorage:
			PossibleMethods[len(PossibleMethods) -
							1]["typeOfArguments"].append(VarStorage[ArgumentName])
			NoOfArguments = NoOfArguments + 1
		elif ArgumentName[ArgumentName.find(")") + 1:] in VarStorage:
			PossibleMethods[len(PossibleMethods) - 1]["typeOfArguments"].append(
				VarStorage[ArgumentName[ArgumentName.find(")") + 1:]])
			NoOfArguments = NoOfArguments + 1
		elif ArgumentName[:ArgumentName.find("[")] in VarStorage:
			x = ArgumentName
			y = VarStorage[x[:x.find("[")]]
			noOfBrackets1 = y.count('[')
			y = y[:y.find("[")]
			noOfBrackets = x.count('[')
			y = y + ("[]" * (noOfBrackets1 - noOfBrackets))
			PossibleMethods[len(PossibleMethods) -
							1]["typeOfArguments"].append(y)
			NoOfArguments = NoOfArguments + 1
		PossibleMethods[len(PossibleMethods) -
						1]["NoOfArguments"] = NoOfArguments

	Possibility = Possibility + 1  # increase by 1 as new keyword found
	return Possibility, Variables


def andExpressionExtraction(root):
	AndOperator = '&'
	Possibility = 0
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]
					   ]["value"][0]  # Label of the child
		if re.match('PrimaryExpression', line):
			Possible, Var = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
		elif re.match('MultiplicativeExpression', line):
			Possible, Var = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
		'''Add the additive operator in between two variables for display'''
		if i != len(ASTNode[root]["child"]) - 1:
			Variable = Variable + Var + AndOperator
		else:
			# if last child,then additive variable will not be concatenated.
			Variable = Variable + Var
		Possibility = Possibility + Possible

	return Possibility, Variable


'''Arguments (handles part between ())'''
def argumentsExtraction(root):
	global Ternary, TernaryPos
	Possibility = 0
	Variable = ""
	if len(ASTNode[root]["child"]) == 0:
		return 0, ""
	root = ASTNode[root]["child"][0]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possible, Var = expressionExtraction(ASTNode[root]["child"][i])
			'''Separating the arguments with a ,'''
			if isinstance(Var, list):
				Ternary = True
				TernaryPos = Var
				Var = 'ternaryExpression'
			if i != len(ASTNode[root]["child"]) - 1:
				Variable = Variable + Var + ","
			else:
				# after the last child ,separator not required.
				Variable = Variable + Var
			Possibility = Possibility + Possible
	return Possibility, Variable


'''ArrayInitializer (handles part between [])'''
def arrayInitializerExtraction(root):
	Possibility = 0
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('VariableInitializer', line):
			Possible, V = variableInitializerExtraction(
				ASTNode[root]["child"][i])
			'''Separating the array arguments with a ,'''
			if i != len(ASTNode[root]["child"]) - 1:
				Variable = Variable + V + ","
			else:
				# after the last child ,separator not required.
				Variable = Variable + V
			Possibility = Possibility + Possible
	return Possibility, Variable


'''ArrayDimsAndInits (handles array elements)'''
def arrayDimsAndInitsExtraction(root):
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possible, V = expressionExtraction(ASTNode[root]["child"][i])
			Variable = Variable + "[" + V + "]"
		elif re.match('ArrayInitializer', line):
			Possible, V = arrayInitializerExtraction(ASTNode[root]["child"][i])
			Variable = Variable + "[" + V + "]"
		Possibility = Possibility + Possible
	return Possibility, Variable


'''AssertStatement (handles Assert Condition)'''
def assertStatementExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	Variable = ""
	Possibility = 0
	line = ASTNode[ASTNode[root]["child"][0]]["value"][0]
	'''Two ways to use assertion:
	Case 1-assert expression;
	Case 2-assert expression1 : expression2; '''

	if re.match('Expression', line):  # Condition of Assert
		Possible, Variable = expressionExtraction(ASTNode[root]["child"][0])
		Possibility = Possibility + Possible
		'''Making a new node for displaying a condition
		Shape - Assert Diamond as 1st child will occur if condition is false'''
		if isinstance(ASTNode[root]["NodesPosition"], list):
			New_Nodes = addNodes("AssertDiamond", Variable, [], [])
			FlowChart.append(New_Nodes)
			FlowChart[len(FlowChart) - 1]["parent"].pop()
			for i in ASTNode[root]["NodesPosition"]:
				if FlowChart[i]["child"] is not None:
					FlowChart[len(FlowChart) - 1]["parent"].append(i)
					FlowChart[i]["child"].append(len(FlowChart) - 1)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		else:
			if FlowChart[ASTNode[root]["NodesPosition"]]["child"] is not None:
				New_Nodes = addNodes(
					"AssertDiamond",
					Variable,
					ASTNode[root]["NodesPosition"],
					[])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)
				ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		index = ASTNode[root]["NodesPosition"]

	for p in range(0, Possibility):
		PossibleMethods[len(PossibleMethods) - 1 - p]["NodeNo"] = index
		if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["Class"] = PresentClass
	Possibility = 0

	'''Handling the Case 2'''
	if len(ASTNode[root]["child"]) == 2:
		line = ASTNode[ASTNode[root]["child"][1]]["value"][0]
		if re.match('Expression', line):  # if error,it will display this.
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][1])
			Possibility = Possibility + Possible
			'''Shape-Error'''
			New_Nodes = addNodes(
				"Error", Variable, ASTNode[root]["NodesPosition"], [])
			FlowChart.append(New_Nodes)
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

	for p in range(0, Possibility):
		PossibleMethods[len(PossibleMethods) - 1 - p]["NodeNo"] = index
		if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["Class"] = PresentClass
	Possibility = 0

	'''Ending the assert with a error end'''
	if isinstance(ASTNode[root]["NodesPosition"], list):
		New_Nodes = addNodes("Circle", "Error End", [], None)
		FlowChart.append(New_Nodes)
		FlowChart[len(FlowChart) - 1]["parent"].pop()
		for i in ASTNode[root]["NodesPosition"]:
			FlowChart[len(FlowChart) - 1]["parent"].append(i)
			FlowChart[i]["child"].append(len(FlowChart) - 1)
	else:
		New_Nodes = addNodes(
			"Circle",
			"Error End",
			ASTNode[root]["NodesPosition"],
			None)
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

	'''For all the Possible Methods found add NodeNo,Class'''
	for p in range(0, Possibility):
		PossibleMethods[len(PossibleMethods) - 1 - p]["NodeNo"] = index
		if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["Class"] = PresentClass

	Possibility = 0
	return index


'''Block (handles part between {})'''
def blockExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	'''creating a start FlowChart Node for Method Beginning'''
	if re.match('MethodDeclaration',
				ASTNode[ASTNode[root]["parent"]]["value"][0]):
		New_Nodes = addNodes(
			"Circle", "Start", ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
		FlowChart.append(New_Nodes)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
				  ]["child"].append(ASTNode[root]["NodesPosition"])
	index = ASTNode[root]["NodesPosition"]

	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('BlockStatement', line):
			index = blockStatementExtraction(ASTNode[root]["child"][i])
			# print 'be:'+str(index)
			if isinstance(index, list):
				if None in index:
					index.remove(None)
			ASTNode[root]["NodesPosition"] = index
	'''creating an end FlowChart Node for Method Ending'''
	if isinstance(index, list):
		# print index
		if re.match('MethodDeclaration', ASTNode[ASTNode[root]["parent"]]["value"][0]) and (
				FlowChart[index[0]]["shape"] != 'Circle' or FlowChart[index[0]]["child"] is not None):
			New_Nodes = addNodes("Circle", "End", index[0], None)
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			FlowChart[index[0]]["child"].append(ASTNode[root]["NodesPosition"])
			# if FlowChart[index[0]].child!=None:
			# FlowChart[index[0]].child.append(ASTNode[root]["NodesPosition"])

			for i in range(1, len(index)):
				if FlowChart[index[i]]["child"] is not None and FlowChart[index[i]
																		  ]["shape"] != 'Circle':
					FlowChart[index[i]]["child"].append(
						ASTNode[root]["NodesPosition"])
					FlowChart[ASTNode[root]["NodesPosition"]
							  ]["parent"].append(index[i])
	else:
		if re.match('MethodDeclaration', ASTNode[ASTNode[root]["parent"]]["value"][0]) and (
				FlowChart[index]["shape"] != 'Circle' or FlowChart[index]["child"] is not None):
			New_Nodes = addNodes("Circle", "End", index, None)
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			FlowChart[index]["child"].append(ASTNode[root]["NodesPosition"])
	return ASTNode[root]["NodesPosition"]


'''BlockStatement (handles body of Block and handles part between {} of Constructor)'''
def blockStatementExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Statement', line):
			index = statementExtraction(ASTNode[root]["child"][i])
			# print 's:'+str(index)
		elif re.match('LocalVariableDeclaration', line):
			Variable, index = localVariableExtraction(
				ASTNode[root]["child"][i])
			# print 'lv:'+str(index)
		elif re.match('AssertStatement', line):
			index = assertStatementExtraction(ASTNode[root]["child"][i])
			# print 'as:'+str(index)
	return index


'''CastExpression (handles casting Eg-(int)b)'''
def castExpressionExtraction(root):
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Type', line):  # Will Extract Variable Type
			Type = typeVariableExtraction(ASTNode[root]["child"][i])
			Variable = Variable + "(" + Type + ")"
		elif re.match('PrimaryExpression', line):  # Will Extract Variable Name
			Possible, V = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			# add the Variable Name and type in VarStorage
			VarStorage.update({V: Type})
			Variable = Variable + V
			Possibility = Possibility + Possible
	return Possibility, Variable


'''CatchStatement'''
def catchStatementExtraction(no, root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	# cld=(root.get_parent()).total_child()
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('FormalParameter',
					line):  # Argument(Exception) that catch statement will handle
			Condition = formalParametersExtraction(ASTNode[root]["child"][i])
		elif re.match('Block', line):
			index = blockExtraction(ASTNode[root]["child"][i])
			if index == ASTNode[root]["NodesPosition"]:  # Empty Catch Block
				New_Nodes = addNodes(
					"Square",
					"Empty Catch Block",
					ASTNode[root]["NodesPosition"],
					[])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)
				index = len(FlowChart) - 1
			'''Adding the label for the edge between condition and catch body (Text=Label:Text)'''
			FlowChart[FlowChart[ASTNode[root]["NodesPosition"]]["child"][no]]["text"] = Condition + \
				":" + FlowChart[FlowChart[ASTNode[root]
										  ["NodesPosition"]]["child"][no]]["text"]

	return index


'''ClassOrInterfaceBody'''
def classOrInterfaceBodyExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('ClassOrInterfaceBodyDeclaration', line):
			index = classOrInterfaceBodyDeclarationExtraction(
				ASTNode[root]["child"][i])
			# Occurs When ClassOrInterfaceBody is empty(index==None)
			if index is not None:
				# print 'ci:'+str(index)
				ASTNode[root]["NodesPosition"] = index
	return ASTNode[root]["NodesPosition"]


'''ClassOrInterfaceBodyDeclaration (handles ClassOrInterface Body)'''
def classOrInterfaceBodyDeclarationExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	global s  # Used For AnonymousInnerClass
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('MethodDeclaration', line):  # Method in the class
			s.append(methodExtraction(ASTNode[root]["child"][i]))
		# Class Variables(For serializing also updating the
		# ASTNode[root]["NodesPosition"])
		elif re.match('FieldDeclaration', line):
			index = fieldExtraction(ASTNode[root]["child"][i])
			ASTNode[root]["NodesPosition"] = index
		elif re.match('Constructor', line):  # Constructor in the class
			s.append(constructorExtraction(ASTNode[root]["child"][i]))
		# Static Block in class(For serializing also updating the
		# ASTNode[root]["NodesPosition"])
		elif re.match('Initializer', line):
			index = initializerExtraction(ASTNode[root]["child"][i])
			ASTNode[root]["NodesPosition"] = index
		elif re.match('EnumDeclaration', line):  # Enum in the class
			s.append(enumExtraction(ASTNode[root]["child"][i]))
	return ASTNode[root]["NodesPosition"]


'''ClassOrInterface (handles Class OR Interface)'''
def classOrInterfaceExtraction(root):
	global PresentClass  # Used for MethodLinking
	ClassOrInterfaceName = ASTNode[root]["value"][1]
	Property = []  # AccessModifiers For Class(Eg:public)
	while ClassOrInterfaceName.find("(") != -1:
		Property.append(ClassOrInterfaceName[ClassOrInterfaceName.find(
			"(") + 1:ClassOrInterfaceName.find(")")])
		ClassOrInterfaceName = ClassOrInterfaceName.replace(
			ClassOrInterfaceName[ClassOrInterfaceName.find("("):ClassOrInterfaceName.find(")") + 1], "")
	# Last Property will either be class or interface
	ClassOrInterface = Property.pop()
	'''creating a Class Node'''
	if ClassOrInterface == 'class':
		if ASTNode[ASTNode[root]["parent"]]["NodesPosition"] != -1:
			New_Nodes = addNodes("Box",
								 "Class:" + ClassOrInterfaceName,
								 ASTNode[ASTNode[root]["parent"]
										 ]["NodesPosition"],
								 [])
			FlowChart[ASTNode[ASTNode[root]["parent"]]
					  ["NodesPosition"]]["child"].append(len(FlowChart))
		else:
			New_Nodes = addNodes(
				"Box", "Class:" + ClassOrInterfaceName, None, [])
		FlowChart.append(New_Nodes)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		Classes.append(
			addClass(
				ClassOrInterfaceName,
				len(FlowChart) -
				1))  # adding it to Classes
		PresentClass = len(Classes) - 1  # updating Present Class
	else:
		'''creating an Interface Node'''
		if ASTNode[ASTNode[root]["parent"]]["NodesPosition"] != -1:
			New_Nodes = addNodes("Box",
								 "Interface:" + ClassOrInterfaceName,
								 ASTNode[ASTNode[root]["parent"]
										 ]["NodesPosition"],
								 [])
		else:
			New_Nodes = addNodes(
				"Box",
				"Interface:" +
				ClassOrInterfaceName,
				None,
				[])
		FlowChart.append(New_Nodes)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('ClassOrInterfaceBody', line):
			classOrInterfaceBodyExtraction(ASTNode[root]["child"][i])
		elif re.match('ImplementsList', line):  # Implements List
			ImplementName = implementsListExtraction(ASTNode[root]["child"][i])
			FlowChart[ASTNode[root]["NodesPosition"]]["text"] = FlowChart[ASTNode[root]["NodesPosition"]
																		  ]["text"] + "\nImplements:" + ImplementName + " Interface"  # Updating the text to be displayed
			# adding the attribute to Class Variable
			Classes[len(Classes) - 1]["implements"] = ImplementName
		elif re.match('ExtendsList', line):  # Extends List
			ExtendName = extendsListExtraction(ASTNode[root]["child"][i])
			FlowChart[ASTNode[root]["NodesPosition"]]["text"] = FlowChart[ASTNode[root]["NodesPosition"]
																		  ]["text"] + "\nExtends:" + ExtendName + " Class"  # Updating the text to be displayed
			# adding the attribute to Class Variable
			Classes[len(Classes) - 1]["extends"] = ExtendName


'''ClassOrInterfaceType (handles Class type variables)'''
def classOrInterfaceTypeExtraction(root):
	ReferenceType = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("TypeArguments", line):
			ReferenceType = typeArgumentsExtraction(ASTNode[root]["child"][i])
	# print ReferenceType
	return ReferenceType


'''ConditionalAndExpression (handles && operation)'''
def conditionalAndExpressionExtraction(root):
	Possibility = 0
	V = ""
	I = -1  # For ConditionalExpression(Handles Ternary Operation)
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		# print line
		if re.match('PrimaryExpression', line):
			Possible, Variable = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, Variable = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, Variable = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, Variable = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, Variable = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, Variable = castExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, Variable = unaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, Variable = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, Variable = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, Variable = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, Variable = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			Variable = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Variable = Variable[:Variable.find("(")]
		# print Variable
		if I == 1:  # For ConditionalExpression as it gives list
			V = Variable
		else:
			V = V + Variable
		'''Add the && operator in between two variables for display'''
		if i != len(ASTNode[root]["child"]) - 1:
			V = V + " && "

	return Possibility, V


'''ConditionalExpression (handles Ternary Condition)'''
def conditionalExpressionExtraction(root):
	Variable = []
	Possibility = 0
	if ASTNode[root]["value"][1] == '(ternary)':
		'''Case-result = testCondition ? value1 : value2'''
		line = ASTNode[ASTNode[root]["child"][0]]["value"][0]  # testCondition
		i = 0
		if re.match('PrimaryExpression', line):
			Possible, V = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, V = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, V = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, V = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, V = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, V = castExpressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, V = unaryExpressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, V = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, V = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, V = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, V = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, V = expressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			V = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			V = V[:V.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, V = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		Variable.append(V)

		line = ASTNode[ASTNode[root]["child"][1]]["value"][0]  # value1
		i = 1
		if re.match('PrimaryExpression', line):
			Possible, V = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, V = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, V = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, V = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, V = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, V = castExpressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, V = unaryExpressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, V = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, V = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, V = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, V = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, V = expressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			V = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			V = V[:V.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, V = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		Variable.append(V)

		line = ASTNode[ASTNode[root]["child"][2]]["value"][0]  # value2
		i = 2
		if re.match('PrimaryExpression', line):
			Possible, V = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, V = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, V = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, V = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, V = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, V = castExpressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, V = unaryExpressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, V = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, V = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, V = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, V = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, V = expressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			V = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			V = V[:V.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, V = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		Variable.append(V)
	# print 'ce:' + str(len(Variable))
	'''Variable will be alist of type[testCondition,value1,value2]'''
	return Possibility, Variable


'''ConditionalAndExpression (handles || operation)'''
def conditionalOrExpressionExtraction(root):
	Possibility = 0
	V = ""
	I = -1  # For ConditionalExpression(Handles Ternary Operation)
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		# print line
		if re.match('PrimaryExpression', line):
			Possible, Variable = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, Variable = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, Variable = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, Variable = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, Variable = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, Variable = castExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, Variable = unaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, Variable = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, Variable = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, Variable = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, Variable = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			Variable = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Variable = Variable[:Variable.find("(")]
		# print Variable
		if I == 1:
			V = Variable
		else:  # For ConditionalExpression as it gives list
			V = V + Variable
		'''Add the || operator in between two variables for display'''
		if i != len(ASTNode[root]["child"]) - 1:
			V = V + " || "

	return Possibility, V


'''ConstructorDeclaration (handles Constructor)'''
def constructorExtraction(root):
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('FormalParameters',
					line):  # No. of Arguments and name(with type)
			line = ASTNode[ASTNode[root]["child"][i]
						   ]["value"][1]  # line=(No. Of Arguments)
			# NoOfFormalParameters=No. of Arguments
			NoOfFormalParameters = int(line[line.find("(") + 1:line.find(")")])
			Variables = ""
			for j in range(0, len(
					ASTNode[ASTNode[root]["child"][i]]["child"])):
				'''Add , operator in between two variables for display'''
				if j != len(ASTNode[ASTNode[root]["child"][i]]["child"]) - \
						1:  # After the last element no separator is required
					Variables = Variables + \
						formalParametersExtraction(
							ASTNode[ASTNode[root]["child"][i]]["child"][j]) + ","
				else:
					Variables = Variables + \
						formalParametersExtraction(
							ASTNode[ASTNode[root]["child"][i]]["child"][j])

			'''FlowChart Node for Constructors
			(Shape-InnerBox) '''
			New_Nodes = addNodes("InnerBox",
								 constructorToText(NoOfFormalParameters,
												   Variables),
								 ASTNode[ASTNode[root]["parent"]
										 ]["NodesPosition"],
								 [])
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
					  ]["child"].append(ASTNode[root]["NodesPosition"])
			Classes[len(Classes) - 1]["constructors"].append(addConstructor(ASTNode[root]
																			["NodesPosition"], NoOfFormalParameters, Variables))  # adding it to Class variable

			'''creating a start FlowChart Node for Constructor Beginning'''
			New_Nodes = addNodes(
				"Circle", "Start", ASTNode[root]["NodesPosition"], [])
			FlowChart.append(New_Nodes)
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

		elif re.match('ExplicitConstructorInvocation', line):
			Possibility, Variable = explicitConstructorInvocationExtraction(
				ASTNode[root]["child"][i])
			'''FlowChart Node for each explicit constructor invocation(For eg:super,this)'''
			New_Nodes = addNodes(
				"Square",
				Variable,
				ASTNode[root]["NodesPosition"],
				[])
			FlowChart.append(New_Nodes)
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			for p in range(0, Possibility):
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["NodeNo"] = ASTNode[root]["NodesPosition"]
				if PossibleMethods[len(PossibleMethods) -
								   1 - p]["Class"] is None:
					PossibleMethods[len(PossibleMethods) -
									1 - p]["Class"] = PresentClass

			Possibility = 0
		elif re.match('BlockStatement', line):
			index = blockStatementExtraction(ASTNode[root]["child"][i])
			# print 'co:'+str(index)
			ASTNode[root]["NodesPosition"] = index

	'''creating an end FlowChart Node for Constructor Beginning'''
	if isinstance(ASTNode[root]["NodesPosition"], list):
		if FlowChart[ASTNode[root]["NodesPosition"][0]]["child"] is not None:
			New_Nodes = addNodes(
				"Circle", "End", ASTNode[root]["NodesPosition"][0], [])
			FlowChart.append(New_Nodes)
			FlowChart[ASTNode[root]["NodesPosition"][0]
					  ]["child"].append(len(FlowChart) - 1)
			for j in ASTNode[root]["NodesPosition"]:
				if j != ASTNode[root]["NodesPosition"][0] and FlowChart[j]["child"] is not None:
					FlowChart[j]["child"].append(len(FlowChart) - 1)
					FlowChart[len(FlowChart) - 1]["parent"].append(j)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
	else:
		if FlowChart[ASTNode[root]["NodesPosition"]]["child"] is not None:
			New_Nodes = addNodes(
				"Circle", "End", ASTNode[root]["NodesPosition"], [])
			FlowChart.append(New_Nodes)
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
	return ASTNode[root]["NodesPosition"]


'''String that is to be displayed for constructor'''
def constructorToText(NoOfFormalParameters, Variables):
	if NoOfFormalParameters > 0:  # when NoOfFormalParameters==0,no Variables will be there
		return "Constructor\nNo. Of Arguments:" + \
			str(NoOfFormalParameters) + "\nArguments List:" + Variables
	else:
		return "Constructor\nNo. Of Arguments:" + str(NoOfFormalParameters)


'''DoStatement (handles do while condition)'''
def doStatementExtraction(root):
	global ForOrSwitch, Break, BreakPos, Continue, ContinuePos  # for loop breaks,continue
	ForOrSwitch = 'For'
	BreakCheck = True
	ContinueCheck = True
	if Break == True:
		BreakCheck = False
	if Continue == True:
		ContinueCheck = False
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	noChild = len(ASTNode[ASTNode[root]["parent"]]["child"])
	EmptyDoWhile = False  # For Handling Empty Do while cases.
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Statement", line):  # do-while body
			index = statementExtraction(ASTNode[root]["child"][i])
			if index == ASTNode[root]["NodesPosition"]:
				EmptyDoWhile = True
		elif re.match("Expression", line):  # Condition of the do-while loop
			Possibility, Condition = expressionExtraction(
				ASTNode[root]["child"][i])
			if EmptyDoWhile:  # if empty do-while,linking of the do while condition is with itself
				if isinstance(index, list):
					New_Nodes = addNodes(
						"Diamond", Condition, [], [
							len(FlowChart)])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
					for j in index:
						if FlowChart[j]["child"] is not None:
							FlowChart[ASTNode[root]["NodesPosition"]
									  ]["parent"].append(j)
							FlowChart[j]["child"].append(
								ASTNode[root]["NodesPosition"])

				else:
					New_Nodes = addNodes(
						"Diamond", Condition, index, [
							len(FlowChart)])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[index]["child"].append(
						ASTNode[root]["NodesPosition"])

				for p in range(0, Possibility):
					PossibleMethods[len(PossibleMethods) - 1 -
									p]["NodeNo"] = ASTNode[root]["NodesPosition"]
					if PossibleMethods[len(
							PossibleMethods) - 1 - p]["Class"] is None:
						PossibleMethods[len(PossibleMethods) -
										1 - p]["Class"] = PresentClass
				Possibility = 0
			else:
				if isinstance(index, list):
					New_Nodes = addNodes("Diamond", Condition, [], [])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
					for j in index:
						if FlowChart[j]["child"] is not None:
							FlowChart[ASTNode[root]["NodesPosition"]
									  ]["parent"].append(j)
							FlowChart[j]["child"].append(
								ASTNode[root]["NodesPosition"])
				else:
					New_Nodes = addNodes("Diamond", Condition, index, [])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[index]["child"].append(
						ASTNode[root]["NodesPosition"])

				for p in range(0, Possibility):
					PossibleMethods[len(PossibleMethods) - 1 -
									p]["NodeNo"] = ASTNode[root]["NodesPosition"]
					if PossibleMethods[len(
							PossibleMethods) - 1 - p]["Class"] is None:
						PossibleMethods[len(PossibleMethods) -
										1 - p]["Class"] = PresentClass
				Possibility = 0

				'''condition will link to the top of the bosy statement by tracking the parents last child index'''
				if isinstance(ASTNode[ASTNode[root]["parent"]]
							  ["NodesPosition"], list):
					for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
						if FlowChart[j]["child"] is not None:
							child = FlowChart[j]["child"][noChild - 1]
							FlowChart[child]["parent"].append(
								ASTNode[root]["NodesPosition"])
							FlowChart[ASTNode[root]["NodesPosition"]
									  ]["child"].append(child)
				else:
					child = FlowChart[ASTNode[ASTNode[root]["parent"]]
									  ["NodesPosition"]]["child"][noChild - 1]
					FlowChart[child]["parent"].append(
						ASTNode[root]["NodesPosition"])
					FlowChart[ASTNode[root]["NodesPosition"]
							  ]["child"].append(child)
	ForOrSwitch = None
	if ContinueCheck and Continue:
		for j in ContinuePos:
			if isinstance(ASTNode[root]["NodesPosition"], list):
				for k in ASTNode[root]["NodesPosition"]:
					FlowChart[j]["child"].append(k)
			else:
				FlowChart[j]["child"].append(ASTNode[root]["NodesPosition"])
		Continue = False
		ContinuePos = []
	if BreakCheck and Break:
		if isinstance(ASTNode[root]["NodesPosition"], list):
			while None in ASTNode[root]["NodesPosition"]:
				ASTNode[root]["NodesPosition"].remove(None)
			index = []
			for j in ASTNode[root]["NodesPosition"]:
				index.append(j)
			for j in BreakPos:
				index.append(j)
		else:
			index = [ASTNode[root]["NodesPosition"]]
			for j in BreakPos:
				index.append(j)
		ASTNode[root]["NodesPosition"] = index
		Break = False
		BreakPos = []
	return ASTNode[root]["NodesPosition"]


'''EnumBody (handles enum constants)'''
def enumBodyExtraction(root):
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('EnumConstant', line):
			Variable = Variable + \
				ASTNode[ASTNode[root]["child"][i]]["value"][1]
		'''Add , operator in between two variables for display'''
		if i != len(ASTNode[root]["child"]) - 1:
			Variable = Variable + ","
	return Variable


'''EnumExtraction (handles enum)'''
def enumExtraction(root):
	line = ASTNode[root]["value"][1]  # Enum Name and its access modifiers
	EnumType = []
	while line.find("(") != -1:
		EnumType.append(line[line.find("(") + 1:line.find(")")])
		line = line.replace(line[line.find("("):line.find(")") + 1], "")
	EnumName = line
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("EnumBody", line):
			Variable = enumBodyExtraction(ASTNode[root]["child"][i])
			'''FlowChart Node For Enum'''
			New_Nodes = addNodes("InnerBox", enumToText(
				EnumType, EnumName, Variable), ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		if isinstance(ASTNode[ASTNode[root]["parent"]]["NodesPosition"], list):
			FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
			for i in ASTNode[ASTNode[root]["parent"]]:
				FlowChart[i["NodesPosition"]]["child"].append(
					ASTNode[root]["NodesPosition"])
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["parent"].append(i["NodesPosition"])
		else:
			FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
					  ]["child"].append(ASTNode[root]["NodesPosition"])
	return ASTNode[root]["NodesPosition"]


'''String that is to be displayed for enum'''
def enumToText(EnumType, EnumName, Variable):
	AccessModifiers = ""
	for i in range(0, len(EnumType)):
		if i != len(EnumType) - 1:
			AccessModifiers = AccessModifiers + EnumType[i] + ","
		else:
			AccessModifiers = AccessModifiers + EnumType[i]
	return "Enum Name:" + EnumName + "\nAccess Modifiers:" + \
		AccessModifiers + "\nEnum Variables:" + Variable


'''EqualityExpression (handles ==/!= operator)'''
def equalityExpressionExtraction(root):
	EqualityOperator = ASTNode[root]["value"][1]  # (==/!=)
	global Ternary, TernaryPos
	Possibility = 0
	V = ""
	I = -1  # For ConditionalExpression(Handles Ternary Operation)
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		# print line
		if re.match('PrimaryExpression', line):
			Possible, Variable = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, Variable = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, Variable = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, Variable = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, Variable = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, Variable = castExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, Variable = unaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, Variable = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, Variable = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, Variable = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, Variable = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			Variable = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Variable = Variable[:Variable.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, Variable = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ShiftExpression', line):
			Possible, Variable = shiftExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AndExpression', line):
			Possible, Variable = andExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('InclusiveOrExpression', line):
			Possible, Variable = inclusiveOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('PreIncrementExpression', line):
			Possible, Variable = preIncrementExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('PreDecrementExpression', line):
			Possible, Variable = preDecrementExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ExclusiveOrExpression', line):
			Possible, Variable = exclusiveOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		# print Variable
		if I == 1:  # For ConditionalExpression as it gives list
			Ternary = True
			TernaryPos = Variable
			V = V + 'ternaryExpression'
		else:
			V = V + Variable
		if i != len(ASTNode[root]["child"]) - 1:
			V = V + EqualityOperator
	return Possibility, V


def exclusiveOrExpressionExtraction(root):
	OrOperator = '^'
	Possibility = 0
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]
					   ]["value"][0]  # Label of the child
		if re.match('PrimaryExpression', line):
			Possible, Var = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
		elif re.match('MultiplicativeExpression', line):
			Possible, Var = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
		'''Add the additive operator in between two variables for display'''
		if i != len(ASTNode[root]["child"]) - 1:
			Variable = Variable + Var + OrOperator
		else:
			# if last child,then additive variable will not be concatenated.
			Variable = Variable + Var
		Possibility = Possibility + Possible

	return Possibility, Variable


'''ExplicitConstructorInvocation (handles this,super in constructor)'''
def explicitConstructorInvocationExtraction(root):
	Possibility = 0
	line = ASTNode[root]["value"][1]
	while line.find("(") != -1:
		Variable = line[line.find("(") + 1:line.find(")")]
		line = line.replace(line[line.find("("):line.find(")") + 1], "")
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Arguments", line):
			Possible, Var = argumentsExtraction(ASTNode[root]["child"][i])
			Variable = Variable + "(" + Var + ")"

			'''New Constructor variable made so its respected constructor needs to be called.'''
			PossibleMethods.append(addPossibleMethod("Method", Variable, -1))
			Possibility = Possibility + Possible + 1
			ArgumentName = Variable[Variable.find("(") + 1:Variable.rfind(")")]
			if ArgumentName == '':
				PossibleMethods[len(PossibleMethods) - 1]["NoOfArguments"] = 0
			else:
				k = 0
				NoOfArguments = 0
				# print ArgumentName
				while(ArgumentName.find(',', k) != -1):
					x = ArgumentName[:ArgumentName.find(',', k)]
					# print ArgumentName
					if x in VarStorage:
						PossibleMethods[len(
							PossibleMethods) - 1]["typeOfArguments"].append(VarStorage[x])
						ArgumentName = ArgumentName.replace(
							ArgumentName[:ArgumentName.find(',', k) + 1], "")
						NoOfArguments = NoOfArguments + 1
					elif x[x.find(")") + 1:] in VarStorage:
						PossibleMethods[len(
							PossibleMethods) - 1]["typeOfArguments"].append(VarStorage[x[x.find(")") + 1:]])
						ArgumentName = ArgumentName.replace(
							ArgumentName[:ArgumentName.find(',', k) + 1], "")
						NoOfArguments = NoOfArguments + 1
					elif x[:x.find("[")] in VarStorage:
						y = VarStorage[x[:x.find("[")]]
						y = y[:y.find("[")]
						noOfBrackets = x.count('[')
						y = y + ("[]" * noOfBrackets)
						PossibleMethods[len(PossibleMethods) -
										1]["typeOfArguments"].append(y)
						ArgumentName = ArgumentName.replace(
							ArgumentName[:ArgumentName.find(',', k) + 1], "")
						NoOfArguments = NoOfArguments + 1
					else:
						k = ArgumentName.find(',', k) + 1
				if ArgumentName in VarStorage:
					PossibleMethods[len(
						PossibleMethods) - 1]["typeOfArguments"].append(VarStorage[ArgumentName])
					NoOfArguments = NoOfArguments + 1
				elif ArgumentName[ArgumentName.find(")") + 1:] in VarStorage:
					PossibleMethods[len(PossibleMethods) - 1]["typeOfArguments"].append(
						VarStorage[ArgumentName[ArgumentName.find(")") + 1:]])
					NoOfArguments = NoOfArguments + 1
				elif ArgumentName[:ArgumentName.find("[")] in VarStorage:
					x = ArgumentName
					y = VarStorage[x[:x.find("[")]]
					noOfBrackets1 = y.count('[')
					y = y[:y.find("[")]
					noOfBrackets = x.count('[')
					y = y + ("[]" * (noOfBrackets1 - noOfBrackets))
					PossibleMethods[len(PossibleMethods) -
									1]["typeOfArguments"].append(y)
					NoOfArguments = NoOfArguments + 1
				PossibleMethods[len(PossibleMethods) -
								1]["NoOfArguments"] = NoOfArguments
	return Possibility, Variable


'''Expression'''
def expressionExtraction(root):
	global Ternary, TernaryPos
	Possibility = 0
	V = ""
	I = -1  # For ConditionalExpression(Handles Ternary Operation)
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('PrimaryExpression', line):
			Possible, Variable = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, Variable = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, Variable = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, Variable = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, Variable = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, Variable = castExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, Variable = unaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, Variable = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, Variable = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, Variable = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, Variable = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			Variable = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Variable = Variable[:Variable.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, Variable = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ShiftExpression', line):
			Possible, Variable = shiftExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AndExpression', line):
			Possible, Variable = andExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('InclusiveOrExpression', line):
			Possible, Variable = inclusiveOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('PreIncrementExpression', line):
			Possible, Variable = preIncrementExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('PreDecrementExpression', line):
			Possible, Variable = preDecrementExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ExclusiveOrExpression', line):
			Possible, Variable = exclusiveOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		# print Variable
		if I == 1:  # For ConditionalExpression as it gives list
			Ternary = True
			TernaryPos = Variable
			V = V + 'ternaryExpression'
		else:
			V = V + Variable
	# print Possibility
	return Possibility, V


'''Extends List (public a extends *Name*)'''
def extendsListExtraction(root):
	return ASTNode[ASTNode[root]["child"][0]]["value"][1]


'''FieldDeclaration (handles Class Variable)'''
def fieldExtraction(root):
	global AnonymousInnerClass, s
	Prop = ASTNode[root]["value"][1]  # AccessModifiers
	Property = []
	Possibility = 0
	while Prop.find("(") != -1:
		Property.append(Prop[Prop.find("(") + 1:Prop.find(")")])
		Prop = Prop.replace(Prop[Prop.find("("):Prop.find(")") + 1], "")
	LocalVariableName = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Type", line):  # VariableType
			LocalVariableName = typeVariableExtraction(
				ASTNode[root]["child"][i])
		# Variable Name(If VariableDeclaratorId present,it will also contain
		# its value)
		elif re.match('VariableDeclarator', line):
			Possibility, name = variableExtraction(ASTNode[root]["child"][i])
			if isinstance(
					name, list):  # Ternary Condition will be handled here
				Vname = name.pop()  # Variable Name
				# Variable Type and Name stored in VarStorage
				VarStorage.update({Vname: LocalVariableName})
				# print len(name)
				LocalVariableName = LocalVariableName + " " + Vname
				'''Initialize the variable (For eg:int a=(a>10)?2:1) so,initialize int a'''
				New_Nodes = addNodes(
					"Square", LocalVariableName, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
				FlowChart.append(New_Nodes)
				ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
				FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
					ASTNode[root]["NodesPosition"])

				'''Condition Part Eg:a>10'''
				New_Nodes = addNodes(
					"Diamond", name[0], ASTNode[root]["NodesPosition"], [])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)
				ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

				for p in range(0, Possibility):
					PossibleMethods[len(PossibleMethods) - 1 -
									p]["NodeNo"] = ASTNode[root]["NodesPosition"]
					if PossibleMethods[len(
							PossibleMethods) - 1 - p]["Class"] is None:
						PossibleMethods[len(PossibleMethods) -
										1 - p]["Class"] = PresentClass

				Possibility = 0

				'''True Part'''
				New_Nodes = addNodes(
					"Square",
					Vname + "=" + name[1],
					ASTNode[root]["NodesPosition"],
					[])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)

				'''False Part'''
				New_Nodes = addNodes(
					"Square",
					Vname + "=" + name[2],
					ASTNode[root]["NodesPosition"],
					[])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)

				return [len(FlowChart) - 2, len(FlowChart) - 1]
			else:
				if name.rfind("=") != -1:  # Variable initializer id is present
					VarStorage.update(
						{name[:name.rfind("=")]: LocalVariableName})
				else:
					VarStorage.update({name: LocalVariableName})
				LocalVariableName = LocalVariableName + " " + name
				if isinstance(ASTNode[ASTNode[root]["parent"]]
							  ["NodesPosition"], list):
					New_Nodes = addNodes(
						"Square", LocalVariableName, ASTNode[ASTNode[root]["parent"]]["NodesPosition"][0], [])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
						if FlowChart[j]["child"] is not None:
							FlowChart[j]["child"].append(
								ASTNode[root]["NodesPosition"])
							if j != ASTNode[ASTNode[root]
											["parent"]]["NodesPosition"][0]:
								FlowChart[ASTNode[root]
										  ["NodesPosition"]]["parent"].append(j)
				else:
					New_Nodes = addNodes(
						"Square", LocalVariableName, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
						ASTNode[root]["NodesPosition"])

				for p in range(0, Possibility):
					PossibleMethods[len(PossibleMethods) - 1 -
									p]["NodeNo"] = ASTNode[root]["NodesPosition"]
					if PossibleMethods[len(
							PossibleMethods) - 1 - p]["Class"] is None:
						PossibleMethods[len(PossibleMethods) -
										1 - p]["Class"] = PresentClass

				Possibility = 0
				if AnonymousInnerClass != -1:  # Handling Anonymous Inner Class
					# print s
					for j in s:
						while(FlowChart[j]["parent"]):
							FlowChart[j]["parent"].pop()
						if len(FlowChart[j]["child"]) > 0:
							FlowChart[j]["child"].pop(0)
						FlowChart[j]["parent"].append(
							ASTNode[root]["NodesPosition"])
						FlowChart[ASTNode[root]["NodesPosition"]
								  ]["child"].append(j)
					AnonymousInnerClass = -1
					s = []
				return ASTNode[root]["NodesPosition"]


'''FinallyStatement (handles the finally block of try-catch-finally)'''
def finallyStatementExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Block', line):
			index = blockExtraction(ASTNode[root]["child"][i])

	return index


'''FormalParameters (handles Arguments)'''
def formalParametersExtraction(root):
	VariableDescription = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Type', line):  # Variable Type
			Type = typeVariableExtraction(ASTNode[root]["child"][i])
			VariableDescription = VariableDescription + Type
			if ASTNode[ASTNode[root]["parent"]]["value"][0] == 'CatchStatement' and i != len(
					ASTNode[root]["child"]) - 2:  # for handling catch statement condition(Eg:-FileNotFoundException|IOException e)
				VariableDescription = VariableDescription + "|"
		elif re.match('VariableDeclaratorId', line):  # Variable Name
			V = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			VariableDescription = VariableDescription + " " + V
			# Variable Type and Name stored in VarStorage
			VarStorage.update({V: Type})
	return VariableDescription


'''ForInit (handles for initializer part eg:for(a;b;c),it will handle a )'''
def forInitExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('LocalVariableDeclaration', line):
			Variable, Initialization = localVariableExtraction(
				ASTNode[root]["child"][i])
		elif re.match('StatementExpressionList', line):
			Initialization = statementExpressionListExtraction(
				ASTNode[root]["child"][i])
	return Variable, Initialization


'''ForStatement(handles for)'''
def forStatementExtraction(root):
	global ForOrSwitch, Break, BreakPos, Continue, ContinuePos  # for loop breaks,continue
	ForOrSwitch = 'For'
	BreakCheck = True
	ContinueCheck = True
	if Break == True:
		BreakCheck = False
	if Continue == True:
		ContinueCheck = False
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]["parent"]
											 ]["NodesPosition"]  # initializing the root's Flow Chart Node No
	ImplicitIteration = False  # (eg:-for(int a:b))
	'''for(a,b,c)'''
	Initialization = -1  # handles a
	Condition = ""  # handles b
	Updation = -1  # handles c
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("ForInit", line):  # Initialize
			name, Initialization = forInitExtraction(ASTNode[root]["child"][i])
		elif re.match("ForUpdate", line):  # Update
			k = 0
			if isinstance(ASTNode[root]["NodesPosition"], list):
				for k in ASTNode[root]["NodesPosition"]:
					if FlowChart[k]["child"] is not None:
						break
				noChild = len(FlowChart[k]["child"])
			else:
				noChild = len(
					FlowChart[ASTNode[root]["NodesPosition"]]["child"])
			Updation = forUpdateExtraction(ASTNode[root]["child"][i])
			if isinstance(ASTNode[root]["NodesPosition"], list):
				UpdationS = FlowChart[k]["child"][noChild]
			else:
				UpdationS = FlowChart[ASTNode[root]
									  ["NodesPosition"]]["child"][noChild]
		elif re.match("Expression", line):  # Condition
			Possible, Condition = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			if ImplicitIteration:  # Eg :- for(int a:b)
				FlowChart[Initialization]["text"] = FlowChart[Initialization]["text"] + \
					"=" + Condition + ".next()"
				Updation = name + "=" + Condition + ".next()"
				Condition = Condition + ".hasNext()"
		elif re.match("Statement", line):  # For Body
			# print 'st'
			if Initialization == -1:  # if no initialization is given
				Initialization = ASTNode[root]["NodesPosition"]
			if Condition != "":  # Condition=='' only when no condition is given
				New_Nodes = addNodes("Diamond", Condition, Initialization, [])
			else:  # when no condition is given,the condition will become true
				New_Nodes = addNodes("Diamond", "True", Initialization, [])
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

			for p in range(0, Possibility):
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["NodeNo"] = ASTNode[root]["NodesPosition"]
				if PossibleMethods[len(PossibleMethods) -
								   1 - p]["Class"] is None:
					PossibleMethods[len(PossibleMethods) -
									1 - p]["Class"] = PresentClass

			Possibility = 0
			if isinstance(Initialization, list):
				FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
				for j in Initialization:
					FlowChart[ASTNode[root]["NodesPosition"]
							  ]["parent"].append(j)
					FlowChart[j]["child"].append(
						ASTNode[root]["NodesPosition"])
				# print ASTNode[root]["NodesPosition"]
			else:
				FlowChart[Initialization]["child"].append(
					ASTNode[root]["NodesPosition"])
			# last FlowChart No of the for body
			index = statementExtraction(ASTNode[root]["child"][i])
			if ImplicitIteration:
				if isinstance(index, list):
					New_Nodes = addNodes("Square", Updation, index, [])
					FlowChart.append(New_Nodes)
					FlowChart[len(FlowChart) - 1]["parent"].pop()
					for j in range(0, len(index)):
						if FlowChart[index[j]]["child"] is not None:
							FlowChart[index[j]]["child"].append(
								len(FlowChart) - 1)
							FlowChart[len(FlowChart) -
									  1]["parent"].append(index[j])
				else:
					if index is not None:
						New_Nodes = addNodes("Square", Updation, index, [])
						FlowChart.append(New_Nodes)
						FlowChart[index]["child"].append(len(FlowChart) - 1)
				index = len(FlowChart) - 1
				if ContinueCheck and Continue:
					for j in ContinuePos:
						FlowChart[j]["child"].append(index)
					Continue = False
					ContinuePos = []
				# FlowChart[index]["child"].append(ASTNode[root]["NodesPosition"])
			else:
				if Updation != -1:
					while(FlowChart[UpdationS]["parent"]):
						exPar = FlowChart[UpdationS]["parent"].pop()
						if FlowChart[exPar]["child"] is not None and UpdationS in FlowChart[exPar]["child"]:
							FlowChart[exPar]["child"].remove(UpdationS)
						else:
							print UpdationS
					if isinstance(index, list):
						# print index
						for j in range(0, len(index)):
							if j is not None and FlowChart[index[j]
														   ]["child"] is not None:
								FlowChart[index[j]]["child"].append(UpdationS)
								FlowChart[UpdationS]["parent"].append(index[j])
					else:
						if index is not None and FlowChart[index]["child"] is not None:
							FlowChart[index]["child"].append(UpdationS)
							FlowChart[UpdationS]["parent"].append(index)
					index = Updation
					if ContinueCheck and Continue:
						for j in ContinuePos:
							FlowChart[j]["child"].append(index)
						Continue = False
						ContinuePos = []
				else:
					if Continue:
						if isinstance(index, list):
							for j in ContinuePos:
								index.append(j)
						else:
							index = [index]
							for j in ContinuePos:
								index.append(j)
						Continue = False
						ContinuePos = []

			if isinstance(index, list):
				for j in index:
					if j is not None and FlowChart[j]["child"] is not None:
						FlowChart[j]["child"].append(
							ASTNode[root]["NodesPosition"])
			else:
				if FlowChart[index]["child"] is not None:
					FlowChart[index]["child"].append(
						ASTNode[root]["NodesPosition"])
		elif re.match("LocalVariableDeclaration", line):
			name, Initialization = localVariableExtraction(
				ASTNode[root]["child"][i])
			ImplicitIteration = True
	ForOrSwitch = None

	if BreakCheck and Break:
		if isinstance(ASTNode[root]["NodesPosition"], list):
			if None in ASTNode[root]["NodesPosition"]:
				ASTNode[root]["NodesPosition"].remove(None)
			index = []
			for j in ASTNode[root]["NodesPosition"]:
				index.append(j)
			for j in BreakPos:
				index.append(j)
		else:
			index = [ASTNode[root]["NodesPosition"]]
			for j in BreakPos:
				index.append(j)
		ASTNode[root]["NodesPosition"] = index
		Break = False
		BreakPos = []
	return ASTNode[root]["NodesPosition"]


def forUpdateExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("StatementExpressionList", line):
			return statementExpressionListExtraction(ASTNode[root]["child"][i])


def ifStatementExtraction(root):
	Possibility = 0
	Else = False
	line = ASTNode[root]["value"][1]
	if line is not None and line.find('else') != -1:
		Else = True
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	index = []
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Statement", line):
			if i == 1:
				if isinstance(ASTNode[ASTNode[root]["parent"]]
							  ["NodesPosition"], list):
					New_Nodes = addNodes("Diamond", Condition, [], [])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
					for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
						if j is not None and FlowChart[j]["child"] is not None:
							FlowChart[ASTNode[root]["NodesPosition"]
									  ]["parent"].append(j)
							FlowChart[j]["child"].append(
								ASTNode[root]["NodesPosition"])
				else:
					New_Nodes = addNodes(
						"Diamond", Condition, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
						ASTNode[root]["NodesPosition"])

			for p in range(0, Possibility):
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["NodeNo"] = ASTNode[root]["NodesPosition"]
				if PossibleMethods[len(PossibleMethods) -
								   1 - p]["Class"] is None:
					PossibleMethods[len(PossibleMethods) -
									1 - p]["Class"] = PresentClass

			Possibility = 0
			Variable = statementExtraction(ASTNode[root]["child"][i])

			if isinstance(Variable, list):
				for j in Variable:
					index.append(j)
			else:
				index.append(Variable)
		elif re.match("Expression", line):
			Possible, Condition = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
	if not Else:
		index.append(ASTNode[root]["NodesPosition"])
	# print index
	return index


def implementsListExtraction(root):
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		if i != len(ASTNode[root]["child"]) - 1:
			Variable = Variable + \
				ASTNode[ASTNode[root]["child"][i]]["value"][1] + ","
		else:
			Variable = Variable + \
				ASTNode[ASTNode[root]["child"][i]]["value"][1]

	return Variable


def importExtraction(root):
	ImportName = ASTNode[ASTNode[root]["child"][0]]["value"][1]
	if ASTNode[ASTNode[root]["parent"]]["NodesPosition"] == -1:
		New_Nodes = addNodes("Square", "Import: " + ImportName, None, [])
	else:
		New_Nodes = addNodes("Square",
							 "Import: " + ImportName,
							 ASTNode[ASTNode[root]["parent"]]["NodesPosition"],
							 [])
		FlowChart[ASTNode[ASTNode[root]["parent"]]
				  ["NodesPosition"]]["child"].append(len(FlowChart))
	FlowChart.append(New_Nodes)
	ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

	return ASTNode[root]["NodesPosition"]


def inclusiveOrExpressionExtraction(root):
	OrOperator = '|'
	Possibility = 0
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]
					   ]["value"][0]  # Label of the child
		if re.match('PrimaryExpression', line):
			Possible, Var = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
		elif re.match('MultiplicativeExpression', line):
			Possible, Var = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
		'''Add the additive operator in between two variables for display'''
		if i != len(ASTNode[root]["child"]) - 1:
			Variable = Variable + Var + OrOperator
		else:
			# if last child,then additive variable will not be concatenated.
			Variable = Variable + Var
		Possibility = Possibility + Possible

	return Possibility, Variable


def initializerExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Block", line):
			index = blockExtraction(ASTNode[root]["child"][i])
			ASTNode[root]["NodesPosition"] = index

	return ASTNode[root]["NodesPosition"]


def instanceOfExpressionExtraction(root):
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("PrimaryExpression", line):
			Possible, V = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			Variable = Variable + V + " instanceof "
		elif re.match("Type", line):
			V = typeVariableExtraction(ASTNode[root]["child"][i])
			Variable = Variable + V

	return Possibility, Variable


def labeledStatementExtraction(root):
	global Label
	# print ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	LabelName = ASTNode[root]["value"][1]
	New_Nodes = addNodes("Circle", "Label Name:" +
						 LabelName, ASTNode[root]["NodesPosition"], [])
	FlowChart.append(New_Nodes)
	ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
	Label.update({LabelName: ASTNode[root]["NodesPosition"]})
	if isinstance(ASTNode[ASTNode[root]["parent"]]["NodesPosition"], list):
		FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
		for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
			if FlowChart[j]["child"] is not None:
				FlowChart[j]["child"].append(ASTNode[root]["NodesPosition"])
				FlowChart[ASTNode[root]["NodesPosition"]]["parent"].append(j)
	else:
		FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
				  ]["child"].append(ASTNode[root]["NodesPosition"])
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Statement", line):
			index = statementExtraction(ASTNode[root]["child"][i])
			ASTNode[root]["NodesPosition"] = index

	New_Nodes = addNodes(
		"Circle",
		"Label End",
		ASTNode[root]["NodesPosition"],
		[])
	FlowChart.append(New_Nodes)

	if isinstance(ASTNode[root]["NodesPosition"], list):
		FlowChart[len(FlowChart) - 1]["parent"].pop()
		for j in ASTNode[root]["NodesPosition"]:
			if FlowChart[j]["child"] is not None:
				FlowChart[j]["child"].append(len(FlowChart) - 1)
				FlowChart[len(FlowChart) - 1]["parent"].append(j)
	else:
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)
	ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

	return ASTNode[root]["NodesPosition"]


def localVariableExtraction(root):
	global AnonymousInnerClass, s
	Possibility = 0
	Prop = ASTNode[root]["value"][1]
	Property = []
	while Prop.find("(") != -1:
		Property.append(Prop[Prop.find("(") + 1:Prop.find(")")])
		Prop = Prop.replace(Prop[Prop.find("("):Prop.find(")") + 1], "")
	LocalVariableName = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Type", line):
			LocalVariableName = typeVariableExtraction(
				ASTNode[root]["child"][i])
		elif re.match('VariableDeclarator', line):
			Possible, name = variableExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			if isinstance(name, list):
				Vname = name.pop()
				# print len(name)
				VarStorage.update({Vname: LocalVariableName})
				LocalVariableName = LocalVariableName + " " + Vname
				New_Nodes = addNodes(
					"Square", LocalVariableName, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
				FlowChart.append(New_Nodes)
				ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
				if isinstance(ASTNode[ASTNode[root]["parent"]]
							  ["NodesPosition"], list):
					FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
					for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
						FlowChart[j]["child"].append(
							ASTNode[root]["NodesPosition"])
				else:
					FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
						ASTNode[root]["NodesPosition"])

				New_Nodes = addNodes(
					"Diamond", name[0], ASTNode[root]["NodesPosition"], [])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)
				ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

				for p in range(0, Possibility):
					PossibleMethods[len(PossibleMethods) - 1 -
									p]["NodeNo"] = ASTNode[root]["NodesPosition"]
					if PossibleMethods[len(
							PossibleMethods) - 1 - p]["Class"] is None:
						PossibleMethods[len(PossibleMethods) -
										1 - p]["Class"] = PresentClass
				Possibility = 0

				New_Nodes = addNodes(
					"Square",
					Vname + "=" + name[1],
					ASTNode[root]["NodesPosition"],
					[])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)

				New_Nodes = addNodes(
					"Square",
					Vname + "=" + name[2],
					ASTNode[root]["NodesPosition"],
					[])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)

				return Vname, [len(FlowChart) - 2, len(FlowChart) - 1]
			else:
				if name.rfind("=") != -1:
					VarStorage.update(
						{name[:name.rfind("=")]: LocalVariableName})
				else:
					VarStorage.update({name: LocalVariableName})
				LocalVariableName = LocalVariableName + " " + name
				if isinstance(ASTNode[ASTNode[root]["parent"]]
							  ["NodesPosition"], list):
					New_Nodes = addNodes(
						"Square", LocalVariableName, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
					for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
						if j is not None and FlowChart[j]["child"] is not None:
							FlowChart[j]["child"].append(
								ASTNode[root]["NodesPosition"])
							FlowChart[ASTNode[root]["NodesPosition"]
									  ]["parent"].append(j)
				else:
					New_Nodes = addNodes(
						"Square", LocalVariableName, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
					FlowChart.append(New_Nodes)
					ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
					FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
						ASTNode[root]["NodesPosition"])

				for p in range(0, Possibility):
					PossibleMethods[len(PossibleMethods) - 1 -
									p]["NodeNo"] = ASTNode[root]["NodesPosition"]
					if PossibleMethods[len(
							PossibleMethods) - 1 - p]["Class"] is None:
						PossibleMethods[len(PossibleMethods) -
										1 - p]["Class"] = PresentClass
				Possibility = 0

				if AnonymousInnerClass != -1:
					# print s
					for i in s:
						while(FlowChart[i]["parent"]):
							FlowChart[i]["parent"].pop()
						if len(FlowChart[i]["child"]) > 0:
							FlowChart[i]["child"].pop(0)
						FlowChart[i]["parent"].append(
							ASTNode[root]["NodesPosition"])
						FlowChart[ASTNode[root]["NodesPosition"]
								  ]["child"].append(i)
					AnonymousInnerClass = -1
					s = []
				return name, ASTNode[root]["NodesPosition"]


def main(ASTDict, Flow, Class, PosMeth):
	global ASTNode, FlowChart, Classes, PosMethod, PossibleMethods
	ASTNode = ASTDict
	FlowChart = Flow
	Classes = Class
	PosMethod = PosMeth
	PossibleMethods = []
	objectExtract(0)

	return FlowChart, Classes, PossibleMethods


def memberSelectorExtraction(root):
	ClassName = ASTNode[root]["value"][1]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('TypeArguments', line):
			MethodName = typeArgumentsExtraction(ASTNode[root]["child"][i])

	PossibleMethods.append(addPossibleMethod("MemberSelector", MethodName, -1))
	PossibleMethods[len(PossibleMethods) - 1]["Class"] = ClassName

	return 1, ClassName + "::" + MethodName


def methodDeclaratorExtraction(root):
	line = ASTNode[ASTNode[root]["child"][0]]["value"][1]
	NoOfFormalParameters = int(line[line.find("(") + 1:line.find(")")])
	if NoOfFormalParameters == 0:
		return 0, ""
	root = ASTNode[root]["child"][0]
	Variables = ""
	for i in range(0, len(ASTNode[root]["child"])):
		if i != len(ASTNode[root]["child"]) - 1:
			Variables = Variables + \
				formalParametersExtraction(ASTNode[root]["child"][i]) + ","
		else:
			Variables = Variables + \
				formalParametersExtraction(ASTNode[root]["child"][i])
	return NoOfFormalParameters, Variables


def methodExtraction(root):
	line = ASTNode[root]["value"][1]
	MethodType = []
	NameList = False
	Block = False
	while line.find("(") != -1:
		MethodType.append(line[line.find("(") + 1:line.find(")")])
		line = line.replace(line[line.find("("):line.find(")") + 1], "")
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('ResultType', line):
			ResultType = resultTypeExtraction(ASTNode[root]["child"][i])
		elif re.match('MethodDeclarator', line):
			MethodName = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			NoOfFormalParameters, Variables = methodDeclaratorExtraction(
				ASTNode[root]["child"][i])
			New_Nodes = addNodes("InnerBox",
								 methodToText(ResultType,
											  MethodName,
											  NoOfFormalParameters,
											  Variables,
											  MethodType),
								 ASTNode[ASTNode[root]["parent"]
										 ]["NodesPosition"],
								 [])
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			aIC = ASTNode[root]["NodesPosition"]
			if isinstance(ASTNode[ASTNode[root]["parent"]]
						  ["NodesPosition"], list):
				FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
				for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
					FlowChart[j]["child"].append(
						ASTNode[root]["NodesPosition"])
					FlowChart[ASTNode[root]["NodesPosition"]
							  ]["parent"].append(j)
			else:
				FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
					ASTNode[root]["NodesPosition"])
			if MethodName in Classes[len(Classes) - 1]["methods"]:
				Classes[len(Classes) - 1]["methods"][MethodName].append(addMethod(ASTNode[root]
																				  ["NodesPosition"], ResultType, MethodName, NoOfFormalParameters, Variables, MethodType))
			else:
				Classes[len(Classes) - 1]["methods"].update({MethodName: [addMethod(
					ASTNode[root]["NodesPosition"], ResultType, MethodName, NoOfFormalParameters, Variables, MethodType)]})
		elif re.match('NameList', line):
			Names = nameListExtraction(ASTNode[root]["child"][i])
			New_Nodes = addNodes(
				"SwitchDiamond",
				"Error",
				ASTNode[root]["NodesPosition"],
				[])
			FlowChart.append(New_Nodes)
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

			New_Nodes = addNodes(
				"Circle",
				Names + ":return Error",
				ASTNode[root]["NodesPosition"],
				None)
			FlowChart.append(New_Nodes)
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
			NameList = True

		elif re.match('Block', line):
			Block = True
			blockExtraction(ASTNode[root]["child"][i])
	if NameList:
		if not Block:
			New_Nodes = addNodes(
				"Square",
				"Empty Method",
				ASTNode[root]["NodesPosition"],
				[])
			FlowChart.append(New_Nodes)
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
		FlowChart[FlowChart[ASTNode[root]["NodesPosition"]]["child"][1]]["text"] = "False:" + \
			FlowChart[FlowChart[ASTNode[root]["NodesPosition"]]
					  ["child"][1]]["text"]
	return aIC


def methodToText(ResultType, MethodName,
				 NoOfFormalParameters, Variables, MethodType):
	AccessModifiers = ""
	for i in range(0, len(MethodType)):
		if i != len(MethodType) - 1:
			AccessModifiers = AccessModifiers + MethodType[i] + ","
		else:
			AccessModifiers = AccessModifiers + MethodType[i]
	if NoOfFormalParameters > 0:
		return "Method Name:" + MethodName + "\nResultType:" + ResultType + "\nAccess Modifiers:" + \
			AccessModifiers + "\nNo. Of Arguments:" + \
			str(NoOfFormalParameters) + "\nArguments List:" + Variables
	else:
		return "Method Name:" + MethodName + "\nResultType:" + ResultType + \
			"\nAccess Modifiers:" + AccessModifiers + \
			"\nNo. Of Arguments:" + str(NoOfFormalParameters)


def multiplicativeExpressionExtraction(root):
	MultiplicativeOperator = ASTNode[root]["value"][1]
	Variable = ""
	Possibility = 0
	V = ""
	I = -1  # For ConditionalExpression(Handles Ternary Operation)
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		# print line
		if re.match('PrimaryExpression', line):
			Possible, Variable = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, Variable = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, Variable = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, Variable = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, Variable = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, Variable = castExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, Variable = unaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, Variable = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, Variable = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, Variable = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, Variable = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			Variable = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Variable = Variable[:Variable.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, Variable = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		# print Variable
		if I == 1:  # For ConditionalExpression as it gives list
			V = Variable
		else:
			V = V + Variable

		if i != len(ASTNode[root]["child"]) - 1:
			V = V + MultiplicativeOperator
	# print Possibility
	return Possibility, V


def nameListExtraction(root):
	Names = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Name', line):
			if i != len(ASTNode[root]["child"]) - 1:
				Names = Names + ASTNode[ASTNode[root]
										["child"][i]]["value"][1] + ","
			else:
				Names = Names + ASTNode[ASTNode[root]["child"][i]]["value"][1]
	return Names


def objectExtract(root):
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('PackageDeclaration', line):
			index = packageExtraction(ASTNode[root]["child"][i])
			ASTNode[root]["NodesPosition"] = index
		elif re.match('ImportDeclaration', line):
			index = importExtraction(ASTNode[root]["child"][i])
			ASTNode[root]["NodesPosition"] = index
		elif re.match('TypeDeclaration', line):
			typeExtraction(ASTNode[root]["child"][i])


def packageExtraction(root):
	PackageName = ASTNode[ASTNode[root]["child"][0]]["value"][1]
	New_Nodes = addNodes("Square", "Package: " + PackageName, None, [])
	FlowChart.append(New_Nodes)
	ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

	return ASTNode[root]["NodesPosition"]


def postfixExpressionExtraction(root):
	PostfixOperator = ASTNode[root]["value"][1]
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('PrimaryExpression', line):
			Possible, V = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Variable = Variable + V
			Possibility = Possibility + Possible
	# print Variable+PostfixOperator
	return Possibility, Variable + PostfixOperator


def preDecrementExpressionExtraction(root):
	global Ternary, TernaryPos
	Possibility = 0
	V = ""
	I = -1  # For ConditionalExpression(Handles Ternary Operation)
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		# print line
		if re.match('PrimaryExpression', line):
			Possible, Variable = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, Variable = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, Variable = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, Variable = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, Variable = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, Variable = castExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, Variable = unaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, Variable = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, Variable = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, Variable = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, Variable = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			Variable = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Variable = Variable[:Variable.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, Variable = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		# print Variable
		if I == 1:  # For ConditionalExpression as it gives list
			V = 'ternaryExpression'
			Ternary = True
			TernaryPos = []
		else:
			V = V + Variable
	return Possibility, "--" + V


def preIncrementExpressionExtraction(root):
	global Ternary, TernaryPos
	Possibility = 0
	V = ""
	I = -1  # For ConditionalExpression(Handles Ternary Operation)
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		# print line
		if re.match('PrimaryExpression', line):
			Possible, Variable = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('RelationalExpression', line):
			Possible, Variable = relationalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('EqualityExpression', line):
			Possible, Variable = equalityExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AdditiveExpression', line):
			Possible, Variable = additiveExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('MultiplicativeExpression', line):
			Possible, Variable = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('CastExpression', line):
			Possible, Variable = castExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('UnaryExpression', line):
			Possible, Variable = unaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalOrExpression', line):
			Possible, Variable = conditionalOrExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalAndExpression', line):
			Possible, Variable = conditionalAndExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('ConditionalExpression', line):
			Possible, Variable = conditionalExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			I = 1
		elif re.match('InstanceOfExpression', line):
			Possible, Variable = instanceOfExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('AssignmentOperator', line):
			Variable = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Variable = Variable[:Variable.find("(")]
		elif re.match('PostfixExpression', line):
			Possible, Variable = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		# print Variable
		if I == 1:  # For ConditionalExpression as it gives list
			V = 'ternaryExpression'
			Ternary = True
			TernaryPos = []
		else:
			V = V + Variable
	return Possibility, "++" + V


def primaryExpressionExtraction(root):
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('PrimaryPrefix', line):
			Possible, Var = primaryPrefixExtraction(ASTNode[root]["child"][i])
			Variable = Variable + Var
			Possibility = Possibility + Possible
			if re.match('System.out.println', Variable):
				Variable = 'PrintAndGoToNextLine'
			elif re.match('System.out.print', Variable):
				Variable = 'Print'
		elif re.match('PrimarySuffix', line):
			Possible, Var = primarySuffixExtraction(ASTNode[root]["child"][i])
			Variable = Variable + Var
			Possibility = Possibility + Possible
			if Var.find("(") != -1:
				if Variable.rfind(
						".") != -1 and Variable[:Variable.rfind(".")] in VarStorage:
					PossibleMethods.append(addPossibleMethod(
						"Method", Variable[Variable.rfind(".") + 1:], -1))
					PossibleMethods[len(
						PossibleMethods) - 1]["Class"] = (VarStorage[Variable[:Variable.rfind(".")]])
					Var = Variable[Variable.rfind(".") + 1:]
					ArgumentName = Var[Var.find("(") + 1:Var.rfind(")")]
				elif Variable.rfind(".") != -1 and Variable[:Variable.rfind("[")] in VarStorage:
					PossibleMethods.append(addPossibleMethod(
						"Method", Variable[Variable.rfind(".") + 1:], -1))
					y = VarStorage[Variable[:Variable.rfind("[")]]
					PossibleMethods[len(PossibleMethods) -
									1]["Class"] = (y[:y.find("[")])
					Var = Variable[Variable.rfind(".") + 1:]
					ArgumentName = Var[Var.find("(") + 1:Var.rfind(")")]
				else:
					PossibleMethods.append(
						addPossibleMethod(
							"Method", Variable, -1))
					ArgumentName = Variable[Variable.find(
						"(") + 1:Variable.rfind(")")]
				if ArgumentName == '':
					PossibleMethods[len(PossibleMethods) -
									1]["NoOfArguments"] = 0
				else:
					k = 0
					NoOfArguments = 0
					while(ArgumentName.find(',', k) != -1 ):
						x = ArgumentName[:ArgumentName.find(',', k)]
						if x in VarStorage:
							PossibleMethods[len(
								PossibleMethods) - 1]["typeOfArguments"].append(VarStorage[x])
							ArgumentName = ArgumentName.replace(
								ArgumentName[:ArgumentName.find(',', k)], "")
							NoOfArguments = NoOfArguments + 1
						elif x[x.find(")") + 1:] in VarStorage:
							PossibleMethods[len(
								PossibleMethods) - 1]["typeOfArguments"].append(VarStorage[x[x.find(")") + 1:]])
							ArgumentName = ArgumentName.replace(
								ArgumentName[:ArgumentName.find(',', k) + 1], "")
							NoOfArguments = NoOfArguments + 1
						elif x[:x.find("[")] in VarStorage:
							y = VarStorage[x[:x.find("[")]]
							y = y[:y.find("[")]
							noOfBrackets = x.count('[')
							y = y + ("[]" * noOfBrackets)
							PossibleMethods[len(
								PossibleMethods) - 1]["typeOfArguments"].append(y)
							ArgumentName = ArgumentName.replace(
								ArgumentName[:ArgumentName.find(',', k) + 1], "")
							NoOfArguments = NoOfArguments + 1
						else:
							k = ArgumentName.find(',', k) + 1
					if ArgumentName.find(',', k) == -1:
						if ArgumentName[:ArgumentName.find(',', k) + 1] == '':
							ArgumentName = ArgumentName[1:]
					if ArgumentName in VarStorage:
						PossibleMethods[len(
							PossibleMethods) - 1]["typeOfArguments"].append(VarStorage[ArgumentName])
						NoOfArguments = NoOfArguments + 1
					elif ArgumentName[ArgumentName.find(")") + 1:] in VarStorage:
						PossibleMethods[len(PossibleMethods) - 1]["typeOfArguments"].append(
							VarStorage[ArgumentName[ArgumentName.find(")") + 1:]])
						NoOfArguments = NoOfArguments + 1
					elif ArgumentName[:ArgumentName.find("[")] in VarStorage:
						x = ArgumentName
						y = VarStorage[x[:x.find("[")]]
						noOfBrackets1 = y.count('[')
						y = y[:y.find("[")]
						noOfBrackets = x.count('[')
						y = y + ("[]" * (noOfBrackets1 - noOfBrackets))
						PossibleMethods[len(PossibleMethods) -
										1]["typeOfArguments"].append(y)
						NoOfArguments = NoOfArguments + 1
					PossibleMethods[len(PossibleMethods) -
									1]["NoOfArguments"] = NoOfArguments

				Possibility = Possibility + 1
	return Possibility, Variable


def primaryPrefixExtraction(root):
	PrimaryPrefix = ""
	Possibility = 0
	if ASTNode[root]["value"][1] is not None:
		if ASTNode[root]["value"][1] == 'this':
			PrimaryPrefix = PrimaryPrefix + ASTNode[root]["value"][1]
		else:
			PrimaryPrefix = PrimaryPrefix + ASTNode[root]["value"][1] + "."
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			if isinstance(Variable, list):
				PrimaryPrefix = Variable
			else:
				PrimaryPrefix = PrimaryPrefix + Variable
			Possibility = Possibility + Possible
		elif re.match('AllocationExpression', line):
			Possible, Variable = allocationExpressionExtraction(
				ASTNode[root]["child"][i])
			PrimaryPrefix = PrimaryPrefix + Variable
			Possibility = Possibility + Possible
		elif line == 'Literal':
			if len(ASTNode[ASTNode[root]["child"][i]]["child"]) == 0:
				line = ASTNode[ASTNode[root]["child"][i]]["value"][1]
				Type = line[line.rfind("(") + 1:line.find(" ")]
				line = line[0:line.rfind("(")]
				while line.find('"') != -1:
					line = line.replace(
						line[line.find('"'):line.find('"') + 1], "'")
				VarStorage.update({line: Type})
				PrimaryPrefix = PrimaryPrefix + line
			else:
				for j in range(0, len(
						ASTNode[ASTNode[root]["child"][i]]["child"])):
					line = ASTNode[ASTNode[ASTNode[root]
										   ["child"][i]]["child"][j]]["value"][0]
					if re.match('NullLiteral', line):
						PrimaryPrefix = PrimaryPrefix + "Null"
						VarStorage.update({"null": "null"})
					elif re.match('BooleanLiteral', line):
						PrimaryPrefix = PrimaryPrefix + \
							ASTNode[ASTNode[ASTNode[root]["child"][i]]
									["child"][j]]["value"][1]
						VarStorage.update(
							{ASTNode[ASTNode[ASTNode[root]["child"][i]]["child"][j]]["value"][1]: "boolean"})
		elif re.match('ResultType', line):
			Variable = resultTypeExtraction(ASTNode[root]["child"][i])
			PrimaryPrefix = PrimaryPrefix + Variable
		else:
			PrimaryPrefix = PrimaryPrefix + \
				ASTNode[ASTNode[root]["child"][i]]["value"][1]

	return Possibility, PrimaryPrefix


def primarySuffixExtraction(root):
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		# print line
		if re.match('Arguments', line):
			line = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			NoOfSuffixArgument = int(line[line.find("(") + 1:line.find(")")])
			Possible, Var = argumentsExtraction(ASTNode[root]["child"][i])
			PrimarySuffix = Var
		elif re.match('Expression', line):
			Possible, Var = expressionExtraction(ASTNode[root]["child"][i])
			PrimarySuffix = Var
		elif re.match('MemberSelector', line):
			Possible, Var = memberSelectorExtraction(ASTNode[root]["child"][i])
			PrimarySuffix = Var
		Possibility = Possibility + Possible
	if ASTNode[root]["value"][1] is None:
		if len(ASTNode[root]["child"]) == 0:
			return 0, ".this"
		return Possibility, "(" + PrimarySuffix + ")"
	elif ASTNode[root]["value"][1] == '[':
		return Possibility, "[" + PrimarySuffix + "]"
	else:
		return Possibility, "." + ASTNode[root]["value"][1]


def referenceTypeExtraction(root):
	line = ASTNode[root]["value"][1]
	ReferenceType = ""
	if ASTNode[ASTNode[root]["child"][0]]["value"][1] is not None:
		ReferenceType = ReferenceType + \
			ASTNode[ASTNode[root]["child"][0]]["value"][1]
	if line is not None and line.find("array") != -1:
		noOfBrackets = line.count('[')
		ReferenceType = ReferenceType + ("[]" * noOfBrackets)
	if len(ASTNode[ASTNode[root]["child"][0]]["child"]) > 0:
		root = ASTNode[root]["child"][0]
		for i in range(0, len(ASTNode[root]["child"])):
			line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
			if re.match('TypeArguments', line):
				ReferenceType = ReferenceType + \
					typeArgumentsExtraction(ASTNode[root]["child"][i])
			elif re.match('ClassOrInterfaceType', line):
				ReferenceType = ReferenceType + \
					ASTNode[ASTNode[root]["child"][i]]["value"][1]
				ReferenceType = ReferenceType + \
					classOrInterfaceTypeExtraction(ASTNode[root]["child"][i])
	return ReferenceType


def relationalExpressionExtraction(root):
	Possibility = 0
	RelationalOperator = ASTNode[root]["value"][1]
	RelationalExpression = ""
	line = ASTNode[ASTNode[root]["child"][0]]["value"][0]
	if re.match('PrimaryExpression', line):
		Possible, Variable = primaryExpressionExtraction(
			ASTNode[root]["child"][0])
		Possibility = Possibility + Possible
		RelationalExpression = RelationalExpression + Variable
	elif re.match('AdditiveExpression', line):
		Possible, Variable = additiveExpressionExtraction(
			ASTNode[root]["child"][0])
		Possibility = Possibility + Possible
		RelationalExpression = RelationalExpression + Variable
	RelationalExpression = RelationalExpression + RelationalOperator
	line = ASTNode[ASTNode[root]["child"][1]]["value"][0]
	if re.match('PrimaryExpression', line):
		Possible, Variable = primaryExpressionExtraction(
			ASTNode[root]["child"][1])
		Possibility = Possibility + Possible
		RelationalExpression = RelationalExpression + Variable
	elif re.match('AdditiveExpression', line):
		Possible, Variable = additiveExpressionExtraction(
			ASTNode[root]["child"][1])
		Possibility = Possibility + Possible
		RelationalExpression = RelationalExpression + Variable
	return Possibility, RelationalExpression


def resultTypeExtraction(root):
	line = ASTNode[root]["value"][1]
	if len(ASTNode[root]["child"]) == 0:
		return line
	else:
		for i in range(0, len(ASTNode[root]["child"])):
			line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
			if re.match('Type', line):
				return typeVariableExtraction(ASTNode[root]["child"][i])


def returnStatementExtraction(root):
	global Ternary, TernaryPos, AnonymousInnerClass, s
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
	if Ternary:
		name = TernaryPos
		New_Nodes = addNodes(
			"Square",
			"TernaryTemp",
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		if isinstance(ASTNode[root]["NodesPosition"], list):
			FlowChart[len(FlowChart) - 1]["parent"].pop()
			for j in ASTNode[root]["NodesPosition"]:
				if FlowChart[j]["child"] is not None:
					FlowChart[j]["child"].append(len(FlowChart) - 1)
					FlowChart[len(FlowChart) - 1]["parent"].append(j)
		else:
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

		New_Nodes = addNodes(
			"Diamond",
			name[0],
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

		for p in range(0, Possibility):
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["NodeNo"] = ASTNode[root]["NodesPosition"]
			if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["Class"] = PresentClass
		Possibility = 0

		New_Nodes = addNodes(
			"Square",
			"TernaryTemp=" +
			name[1],
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)

		New_Nodes = addNodes(
			"Square",
			"TernaryTemp=" +
			name[2],
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)
		ASTNode[ASTNode[root]["parent"]]["NodesPosition"] = [
			len(FlowChart) - 2, len(FlowChart) - 1]

	if isinstance(Variable, list):
		name = Variable
		New_Nodes = addNodes(
			"Diamond",
			name[0],
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

		for p in range(0, Possibility):
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["NodeNo"] = ASTNode[root]["NodesPosition"]
			if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["Class"] = PresentClass
		Possibility = 0

		New_Nodes = addNodes("Square", "return " +
							 name[1], ASTNode[root]["NodesPosition"], [])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)

		New_Nodes = addNodes("Square", "return " +
							 name[2], ASTNode[root]["NodesPosition"], [])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)

		return [len(FlowChart) - 2, len(FlowChart) - 1]
	else:
		if Ternary:
			Variable = Variable.replace('ternaryExpression', 'TernaryTemp')
			Ternary = False
			TernaryPos = []
		if isinstance(ASTNode[ASTNode[root]["parent"]]["NodesPosition"], list):
			New_Nodes = addNodes(
				"Circle",
				"return " + Variable,
				ASTNode[root]["NodesPosition"],
				None)
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
			for i in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
				if FlowChart[i]["child"] is not None:
					FlowChart[i]["child"].append(
						ASTNode[root]["NodesPosition"])
					FlowChart[ASTNode[root]["NodesPosition"]
							  ]["parent"].append(i)
		else:
			New_Nodes = addNodes("Circle",
								 "return " + Variable,
								 ASTNode[ASTNode[root]["parent"]
										 ]["NodesPosition"],
								 None)
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
					  ]["child"].append(ASTNode[root]["NodesPosition"])

		for p in range(0, Possibility):
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["NodeNo"] = ASTNode[root]["NodesPosition"]
			if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["Class"] = PresentClass

		Possibility = 0

		if AnonymousInnerClass != -1:
			FlowChart[ASTNode[root]["NodesPosition"]]["child"] = []
			# print s
			for i in s:
				while(FlowChart[i]["parent"]):
					FlowChart[i]["parent"].pop()
					if len(FlowChart[i]["child"]) > 0:
						FlowChart[i]["child"].pop(0)
				FlowChart[i]["parent"].append(ASTNode[root]["NodesPosition"])
				FlowChart[ASTNode[root]["NodesPosition"]]["child"].append(i)
				AnonymousInnerClass = -1
				s = []

		return ASTNode[root]["NodesPosition"]


def shiftExpressionExtraction(root):
	ShiftOperator = ""
	if ASTNode[root]["value"][1] is not None:
		# gives the arithmetic operation sign(+/-)
		ShiftOperator = ASTNode[root]["value"][1]
	Possibility = 0
	Variable = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]
					   ]["value"][0]  # Label of the child
		if re.match('PrimaryExpression', line):
			Possible, Var = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
		elif re.match('MultiplicativeExpression', line):
			Possible, Var = multiplicativeExpressionExtraction(
				ASTNode[root]["child"][i])
		elif re.match('RSIGNEDSHIFT', line):
			ShiftOperator = '>>'
			continue
		'''Add the additive operator in between two variables for display'''
		if i != len(ASTNode[root]["child"]) - 1:
			Variable = Variable + Var + ShiftOperator
		else:
			# if last child,then additive variable will not be concatenated.
			Variable = Variable + Var
		Possibility = Possibility + Possible

	return Possibility, Variable


def statementExpressionExtraction(root):
	global AnonymousInnerClass, s, Ternary, TernaryPos
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('PrimaryExpression', line):
			Possible, Primary = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			Variable = Variable + Primary
		elif re.match('AssignmentOperator', line):
			AssignmentOperator = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			Variable = Variable + \
				AssignmentOperator[0:AssignmentOperator.find("(")]
		elif re.match('Expression', line):
			Possible, V = expressionExtraction(ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			Variable = Variable + V
		elif re.match('PostfixExpression', line):
			Possible, V = postfixExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			Variable = Variable + V
		elif re.match('PreIncrementExpression', line):
			Possible, V = preIncrementExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			Variable = Variable + V
		elif re.match('PreDecrementExpression', line):
			Possible, V = preDecrementExpressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			Variable = Variable + V
	# print Variable + '->se:' + str((root.get_parent()).get_NodesPosition())
	if Ternary:
		name = TernaryPos
		New_Nodes = addNodes(
			"Square",
			"TernaryTemp",
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

		New_Nodes = addNodes(
			"Diamond",
			name[0],
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

		for p in range(0, Possibility):
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["NodeNo"] = ASTNode[root]["NodesPosition"]
			if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["Class"] = PresentClass
		Possibility = 0

		New_Nodes = addNodes(
			"Square",
			"TernaryTemp=" +
			name[1],
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)

		New_Nodes = addNodes(
			"Square",
			"TernaryTemp=" +
			name[2],
			ASTNode[root]["NodesPosition"],
			[])
		FlowChart.append(New_Nodes)
		FlowChart[ASTNode[root]["NodesPosition"]
				  ]["child"].append(len(FlowChart) - 1)
		ASTNode[ASTNode[root]["parent"]]["NodesPosition"] = [
			len(FlowChart) - 2, len(FlowChart) - 1]
		Variable = Variable.replace('ternaryExpression', 'TernaryTemp')
		Ternary = False
		TernaryPos = []
	if isinstance(ASTNode[ASTNode[root]["parent"]]["NodesPosition"], list):
		New_Nodes = addNodes(
			"Square", Variable, ASTNode[ASTNode[root]["parent"]]["NodesPosition"][0], [])
		FlowChart.append(New_Nodes)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		for i in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
			if FlowChart[i]["child"] is not None:
				FlowChart[i]["child"].append(ASTNode[root]["NodesPosition"])
				if i != ASTNode[ASTNode[root]["parent"]]["NodesPosition"][0]:
					FlowChart[ASTNode[root]["NodesPosition"]
							  ]["parent"].append(i)
	else:
		New_Nodes = addNodes(
			"Square", Variable, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
		FlowChart.append(New_Nodes)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
				  ]["child"].append(ASTNode[root]["NodesPosition"])

	for p in range(0, Possibility):
		PossibleMethods[len(PossibleMethods) - 1 -
						p]["NodeNo"] = ASTNode[root]["NodesPosition"]
		if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["Class"] = PresentClass
	Possibility = 0

	if AnonymousInnerClass != -1:
		# print s
		for i in s:
			while(FlowChart[i]["parent"]):
				FlowChart[i]["parent"].pop()
			if len(FlowChart[i]["child"]) > 0:
				FlowChart[i]["child"].pop(0)
			FlowChart[i]["parent"].append(ASTNode[root]["NodesPosition"])
			FlowChart[ASTNode[root]["NodesPosition"]]["child"].append(i)
		AnonymousInnerClass = -1
		s = []
	return ASTNode[root]["NodesPosition"]


def statementExpressionListExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('StatementExpression', line):
			Variable = statementExpressionExtraction(ASTNode[root]["child"][i])
			ASTNode[root]["NodesPosition"] = Variable
	return Variable


def statementExtraction(root):
	global Break, BreakPos, ForOrSwitch, Continue, ContinuePos, Label
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('StatementExpression', line):
			index = statementExpressionExtraction(ASTNode[root]["child"][i])
		elif re.match('ForStatement', line):
			index = forStatementExtraction(ASTNode[root]["child"][i])
			# print 'fe:' +str(index)
		elif re.match('ReturnStatement', line):
			index = returnStatementExtraction(ASTNode[root]["child"][i])
		elif re.match("Block", line):
			index = blockExtraction(ASTNode[root]["child"][i])
		elif re.match("IfStatement", line):
			index = ifStatementExtraction(ASTNode[root]["child"][i])
		elif re.match("WhileStatement", line):
			index = whileStatementExtraction(ASTNode[root]["child"][i])
		elif re.match("LabeledStatement", line):
			index = labeledStatementExtraction(ASTNode[root]["child"][i])
		elif re.match("EmptyStatement", line):
			return ASTNode[root]["NodesPosition"]
		elif re.match("TryStatement", line):
			index = tryStatementExtraction(ASTNode[root]["child"][i])
		elif re.match("ThrowStatement", line):
			index = throwStatementExtraction(ASTNode[root]["child"][i])
		elif re.match("SwitchStatement", line):
			index = switchStatementExtraction(ASTNode[root]["child"][i])
		elif re.match("BreakStatement", line):
			Break = True
			BreakValue = ASTNode[ASTNode[root]["child"][i]]["value"][1]
			if BreakValue is not None:
				if BreakValue in Label:
					if isinstance(ASTNode[root]["NodesPosition"], list):
						New_Nodes = addNodes(
							"Square", "Break Statement", [], [])
						FlowChart.append(New_Nodes)
						FlowChart[len(FlowChart) - 1]["parent"].pop()
						for j in ASTNode[root]["NodesPosition"]:
							if FlowChart[j]["child"] is not None:
								FlowChart[j]["child"].append(
									len(FlowChart) - 1)
								FlowChart[len(FlowChart) -
										  1]["parent"].append(j)
					else:
						New_Nodes = addNodes(
							"Square", "Break Statement", ASTNode[root]["NodesPosition"], [])
						FlowChart.append(New_Nodes)
						FlowChart[ASTNode[root]["NodesPosition"]
								  ]["child"].append(len(FlowChart) - 1)
					FlowChart[len(FlowChart) -
							  1]["child"].append(Label[BreakValue])
					FlowChart[Label[BreakValue]]["parent"].append(
						len(FlowChart) - 1)
					Break = False
			if ForOrSwitch == 'For':
				if isinstance(ASTNode[root]["NodesPosition"], list):
					New_Nodes = addNodes("Square", "Break Statement", [], [])
					FlowChart.append(New_Nodes)
					FlowChart[len(FlowChart) - 1]["parent"].pop()
					for j in ASTNode[root]["NodesPosition"]:
						if FlowChart[j]["child"] is not None:
							FlowChart[j]["child"].append(len(FlowChart) - 1)
							FlowChart[len(FlowChart) - 1]["parent"].append(j)
				else:
					New_Nodes = addNodes(
						"Square", "Break Statement", ASTNode[root]["NodesPosition"], [])
					FlowChart.append(New_Nodes)
					FlowChart[ASTNode[root]["NodesPosition"]
							  ]["child"].append(len(FlowChart) - 1)
				BreakPos.append(len(FlowChart) - 1)
				return
			return ASTNode[root]["NodesPosition"]
		elif re.match("DoStatement", line):
			index = doStatementExtraction(ASTNode[root]["child"][i])
		elif re.match("ContinueStatement", line):
			Continue = True
			if isinstance(ASTNode[root]["NodesPosition"], list):
				New_Nodes = addNodes("Square", "Break Statement", [], [])
				FlowChart.append(New_Nodes)
				FlowChart[len(FlowChart) - 1]["parent"].pop()
				for j in ASTNode[root]["NodesPosition"]:
					if FlowChart[j]["child"] is not None:
						FlowChart[j]["child"].append(len(FlowChart) - 1)
						FlowChart[len(FlowChart) - 1]["parent"].append(j)
			else:
				New_Nodes = addNodes(
					"Square",
					"Continue Statement",
					ASTNode[root]["NodesPosition"],
					[])
				FlowChart.append(New_Nodes)
				FlowChart[ASTNode[root]["NodesPosition"]
						  ]["child"].append(len(FlowChart) - 1)
			ContinuePos.append(len(FlowChart) - 1)
			return
		elif re.match("SynchronizedStatement", line):
			index = synchronizedStatementExtraction(ASTNode[root]["child"][i])
	# print index
	return index


def switchLabelExtraction(root):
	Variable = ""
	Possibility = 0
	if len(ASTNode[root]["child"]) == 0:
		line = ASTNode[root]["value"][1]
		return 0, line[line.find("(") + 1:line.rfind(")")]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possibility, Var = expressionExtraction(ASTNode[root]["child"][i])
			Variable = Variable + Var

	return Possibility, Variable


def switchStatementExtraction(root):
	global Break, ForOrSwitch
	ForOrSwitch = 'Switch'
	index = []
	x = -1
	Present = False
	Default = False
	Label = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possibility, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			New_Nodes = addNodes(
				"SwitchDiamond", Variable, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			CondPos = ASTNode[root]["NodesPosition"]
			if isinstance(ASTNode[ASTNode[root]["parent"]]
						  ["NodesPosition"], list):
				FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
				for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
					if FlowChart[j]["child"] is not None:
						FlowChart[j]["child"].append(
							ASTNode[root]["NodesPosition"])
						FlowChart[ASTNode[root]["NodesPosition"]
								  ]["parent"].append(j)
			else:
				FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
					ASTNode[root]["NodesPosition"])

			for p in range(0, Possibility):
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["NodeNo"] = ASTNode[root]["NodesPosition"]
				if PossibleMethods[len(PossibleMethods) -
								   1 - p]["Class"] is None:
					PossibleMethods[len(PossibleMethods) -
									1 - p]["Class"] = PresentClass

			Possibility = 0
		elif re.match('SwitchLabel', line):
			if x != -1 and Present and Break:
				if isinstance(x, list):
					for j in x:
						index.append(j)
				else:
					index.append(x)
				ASTNode[root]["NodesPosition"] = CondPos
				Break = False
				BreakPos = []
			elif x != -1 and Present:
				if isinstance(x, list):
					ASTNode[root]["NodesPosition"] = [CondPos]
					for j in x:
						ASTNode[root]["NodesPosition"].append(j)
				else:
					ASTNode[root]["NodesPosition"] = [CondPos, x]
			Possibility, SwitchLabel = switchLabelExtraction(
				ASTNode[root]["child"][i])
			Label = Label + 1
			Present = False
		elif re.match('BlockStatement', line):
			if SwitchLabel == 'default':
				Default = True
			x = blockStatementExtraction(ASTNode[root]["child"][i])
			if not Present:
				if len(FlowChart[CondPos]["child"]) <= Label - 1:
					if isinstance(ASTNode[root]["NodesPosition"], list):
						New_Nodes = addNodes(
							"Square", "Empty Switch Case", ASTNode[root]["NodesPosition"], [])
						FlowChart.append(New_Nodes)
						FlowChart[len(FlowChart) - 1]["parent"].pop()
						for j in ASTNode[root]["NodesPosition"]:
							if FlowChart[j]["child"] is not None:
								FlowChart[len(FlowChart) -
										  1]["parent"].append(j)
								FlowChart[j]["child"].append(
									len(FlowChart) - 1)

					else:
						if FlowChart[ASTNode[root]
									 ["NodesPosition"]]["child"] is not None:
							New_Nodes = addNodes(
								"Square", "Empty Switch Case", ASTNode[root]["NodesPosition"], [])
							FlowChart.append(New_Nodes)
							FlowChart[ASTNode[root]["NodesPosition"]
									  ]["child"].append(len(FlowChart) - 1)
					x = len(FlowChart) - 1
				if len(FlowChart[CondPos]["child"]) == Label:
					FlowChart[FlowChart[CondPos]["child"][Label - 1]]["text"] = SwitchLabel + \
						":" + FlowChart[FlowChart[CondPos]
										["child"][Label - 1]]["text"]
			for p in range(0, Possibility):
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["NodeNo"] = ASTNode[root]["NodesPosition"]
				if PossibleMethods[len(PossibleMethods) -
								   1 - p]["Class"] is None:
					PossibleMethods[len(PossibleMethods) -
									1 - p]["Class"] = PresentClass

			Possibility = 0

			ASTNode[root]["NodesPosition"] = x
			Present = True

	if Present:
		Break = False
		if isinstance(x, list):
			for j in x:
				index.append(j)
		else:
			index.append(x)
	if not Default:
		New_Nodes = addNodes("Square", "default:Empty Block", CondPos, [])
		FlowChart.append(New_Nodes)
		FlowChart[CondPos]["child"].append(len(FlowChart) - 1)
		index.append(len(FlowChart) - 1)
	ForOrSwitch = None
	return index


def synchronizedStatementExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Block", line):
			index = blockExtraction(ASTNode[root]["child"][i])
			ASTNode[root]["NodesPosition"] = index
		elif re.match("Expression", line):
			Possibility, Condition = expressionExtraction(
				ASTNode[root]["child"][i])
			New_Nodes = addNodes(
				"Circle",
				"synchronized (" + Condition + ")",
				ASTNode[root]["NodesPosition"],
				[])
			FlowChart.append(New_Nodes)
			ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
			if isinstance(ASTNode[ASTNode[root]["parent"]]
						  ["NodesPosition"], list):
				FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
				for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
					if FlowChart[j]["child"] is not None:
						FlowChart[j]["child"].append(
							ASTNode[root]["NodesPosition"])
						FlowChart[ASTNode[root]["NodesPosition"]
								  ]["parent"].append(j)
			else:
				FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
					ASTNode[root]["NodesPosition"])

			for p in range(0, Possibility):
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["NodeNo"] = ASTNode[root]["NodesPosition"]
				if PossibleMethods[len(PossibleMethods) -
								   1 - p]["Class"] is None:
					PossibleMethods[len(PossibleMethods) -
									1 - p]["Class"] = PresentClass

			Possibility = 0

	New_Nodes = addNodes(
		"Circle",
		"Synchronized End",
		ASTNode[root]["NodesPosition"],
		[])
	FlowChart.append(New_Nodes)

	if isinstance(ASTNode[root]["NodesPosition"], list):
		FlowChart[len(FlowChart) - 1]["parent"].pop()
		for j in ASTNode[root]["NodesPosition"]:
			if FlowChart[j]["child"] is not None:
				FlowChart[j]["child"].append(len(FlowChart) - 1)
				FlowChart[len(FlowChart) - 1]["parent"].append(j)
	else:
		if FlowChart[ASTNode[root]["NodesPosition"]]["child"] is not None:
			FlowChart[ASTNode[root]["NodesPosition"]
					  ]["child"].append(len(FlowChart) - 1)
		else:
			FlowChart.pop()

	ASTNode[root]["NodesPosition"] = len(FlowChart) - 1

	return ASTNode[root]["NodesPosition"]


def throwStatementExtraction(root):
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possible, V = expressionExtraction(ASTNode[root]["child"][i])
			Variable = Variable + V
			Possibility = Possibility + Possible

	New_Nodes = addNodes("Circle", "Error:\n" + Variable,
						 ASTNode[ASTNode[root]["parent"]]["NodesPosition"], None)
	FlowChart.append(New_Nodes)
	ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
	if isinstance(ASTNode[ASTNode[root]["parent"]]["NodesPosition"], list):
		FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
		for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
			if FlowChart[j]["child"] is not None:
				FlowChart[j]["child"].append(ASTNode[root]["NodesPosition"])
	else:
		if FlowChart[ASTNode[ASTNode[root]["parent"]]
					 ["NodesPosition"]]["child"] is not None:
			FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
					  ]["child"].append(ASTNode[root]["NodesPosition"])

	for p in range(0, Possibility):
		PossibleMethods[len(PossibleMethods) - 1 -
						p]["NodeNo"] = ASTNode[root]["NodesPosition"]
		if PossibleMethods[len(PossibleMethods) - 1 - p]["Class"] is None:
			PossibleMethods[len(PossibleMethods) - 1 -
							p]["Class"] = PresentClass

	Possibility = 0

	return ASTNode[root]["NodesPosition"]


def typeExtraction(root):
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('ClassOrInterfaceDeclaration', line):
			classOrInterfaceExtraction(ASTNode[root]["child"][i])


def tryStatementExtraction(root):
	if isinstance(ASTNode[ASTNode[root]["parent"]]["NodesPosition"], list):
		if None in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
			ASTNode[ASTNode[root]["parent"]]["NodesPosition"].remove(None)
		New_Nodes = addNodes("SwitchDiamond",
							 "Error",
							 ASTNode[ASTNode[root]["parent"]
									 ]["NodesPosition"][0],
							 [])
		FlowChart.append(New_Nodes)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
			if FlowChart[j]["child"] is not None:
				FlowChart[j]["child"].append(ASTNode[root]["NodesPosition"])
				if j != ASTNode[ASTNode[root]["parent"]]["NodesPosition"][0]:
					FlowChart[ASTNode[root]["NodesPosition"]
							  ]["parent"].append(j)
	else:
		New_Nodes = addNodes("SwitchDiamond",
							 "Error",
							 ASTNode[ASTNode[root]["parent"]]["NodesPosition"],
							 [])
		FlowChart.append(New_Nodes)
		ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
		FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]
				  ]["child"].append(ASTNode[root]["NodesPosition"])
	index = []
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match("Block", line):
			noChild = len(FlowChart[ASTNode[root]["NodesPosition"]]["child"])
			x = blockExtraction(ASTNode[root]["child"][i])
			if isinstance(x, list):
				for j in x:
					index.append(j)
			else:
				index.append(x)
			FlowChart[FlowChart[ASTNode[root]["NodesPosition"]]["child"][noChild]]["text"] = "False:" + \
				FlowChart[FlowChart[ASTNode[root]["NodesPosition"]]
						  ["child"][noChild]]["text"]
		elif re.match("CatchStatement", line):
			noChild = len(FlowChart[ASTNode[root]["NodesPosition"]]["child"])
			x = catchStatementExtraction(noChild, ASTNode[root]["child"][i])
			if isinstance(x, list):
				for j in x:
					index.append(j)
			else:
				index.append(x)
		elif re.match("FinallyStatement", line):
			ASTNode[root]["NodesPosition"] = index
			index = finallyStatementExtraction(ASTNode[root]["child"][i])
			# print index
	return index


def typeArgumentExtraction(root):
	TypeArgument = ""
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('ReferenceType', line):
			TypeArgument = TypeArgument + \
				referenceTypeExtraction(ASTNode[root]["child"][i])

	return TypeArgument


def typeArgumentsExtraction(root):
	TypeArguments = "<"
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('TypeArgument', line):
			TypeArguments = TypeArguments + \
				typeArgumentExtraction(ASTNode[root]["child"][i])
		elif re.match('Type', line):
			ReferenceType = ReferenceType + \
				typeVariableExtraction(ASTNode[root]["child"][i])

		if i != len(ASTNode[root]["child"]) - 1:
			TypeArguments = TypeArguments + ","
	TypeArguments = TypeArguments + ">"
	return TypeArguments


def typeVariableExtraction(root):
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('ReferenceType', line):
			ReferenceType = referenceTypeExtraction(ASTNode[root]["child"][i])
			return ReferenceType
		elif re.match('PrimitiveType', line):
			return ASTNode[ASTNode[root]["child"][i]]["value"][1]
	if len(ASTNode[root]["child"]) == 0:
		return "<?>"


def unaryExpressionExtraction(root):
	UnaryOperator = ASTNode[root]["value"][1]
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('PrimaryExpression', line):
			Possible, V = primaryExpressionExtraction(
				ASTNode[root]["child"][i])
			Variable = Variable + UnaryOperator + V
			Possibility = Possibility + Possible
	return Possibility, Variable


def variableExtraction(root):
	Variable = ""
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('VariableDeclaratorId', line):
			Variable = ASTNode[ASTNode[root]["child"][i]]["value"][1]
		elif re.match('VariableInitializer', line):
			Possibility, index = variableInitializerExtraction(
				ASTNode[root]["child"][i])
			if isinstance(index, list):
				index.append(Variable)
				return Possibility, index
			else:
				Variable = Variable + "=" + index
			# print Variable
	return Possibility, Variable


def variableInitializerExtraction(root):
	Possibility = 0
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possible, Variable = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			return Possible, Variable
		elif re.match('ArrayInitializer', line):
			Possible, Variable = arrayInitializerExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
			return Possible, ("[" + Variable + "]")


def whileStatementExtraction(root):
	global ForOrSwitch, Break, BreakPos, Continue, ContinuePos
	BreakCheck = True
	ContinueCheck = True
	if Break == True:
		BreakCheck = False
	if Continue == True:
		ContinueCheck = False
	ForOrSwitch = 'For'
	Possibility = 0
	ASTNode[root]["NodesPosition"] = ASTNode[ASTNode[root]
											 ["parent"]]["NodesPosition"]
	for i in range(0, len(ASTNode[root]["child"])):
		line = ASTNode[ASTNode[root]["child"][i]]["value"][0]
		if re.match('Expression', line):
			Possible, Condition = expressionExtraction(
				ASTNode[root]["child"][i])
			Possibility = Possibility + Possible
		elif re.match('Statement', line):
			if isinstance(ASTNode[ASTNode[root]["parent"]]
						  ["NodesPosition"], list):
				New_Nodes = addNodes("Diamond", Condition, [], [])
				FlowChart.append(New_Nodes)
				ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
				FlowChart[ASTNode[root]["NodesPosition"]]["parent"].pop()
				for j in ASTNode[ASTNode[root]["parent"]]["NodesPosition"]:
					if FlowChart[j]["child"] is not None:
						FlowChart[j]["child"].append(
							ASTNode[root]["NodesPosition"])
						FlowChart[ASTNode[root]["NodesPosition"]
								  ]["parent"].append(j)
			else:
				New_Nodes = addNodes(
					"Diamond", Condition, ASTNode[ASTNode[root]["parent"]]["NodesPosition"], [])
				FlowChart.append(New_Nodes)
				ASTNode[root]["NodesPosition"] = len(FlowChart) - 1
				FlowChart[ASTNode[ASTNode[root]["parent"]]["NodesPosition"]]["child"].append(
					ASTNode[root]["NodesPosition"])

			for p in range(0, Possibility):
				PossibleMethods[len(PossibleMethods) - 1 -
								p]["NodeNo"] = ASTNode[root]["NodesPosition"]
				if PossibleMethods[len(PossibleMethods) -
								   1 - p]["Class"] is None:
					PossibleMethods[len(PossibleMethods) -
									1 - p]["Class"] = PresentClass

			Possibility = 0
			index = statementExtraction(ASTNode[root]["child"][i])
			# print ASTNode[root]["NodesPosition"]
			if isinstance(index, list):
				if None in index:
					index.remove(None)
				for j in index:
					if FlowChart[j]["child"] is not None:
						FlowChart[j]["child"].append(
							ASTNode[root]["NodesPosition"])
			else:
				if index is not None:
					if FlowChart[index]["child"] is not None:
						FlowChart[index]["child"].append(
							ASTNode[root]["NodesPosition"])

	if ContinueCheck and Continue:
		for j in ContinuePos:
			FlowChart[j]["child"].append(ASTNode[root]["NodesPosition"])
		Continue = False
		ContinuePos = []
	if BreakCheck and Break:
		if isinstance(ASTNode[root]["NodesPosition"], list):
			if None in ASTNode[root]["NodesPosition"]:
				ASTNode[root]["NodesPosition"].remove(None)
			index = []
			for j in ASTNode[root]["NodesPosition"]:
				index.append(j)
			for j in BreakPos:
				index.append(j)
		else:
			index = [ASTNode[root]["NodesPosition"]]
			for j in BreakPos:
				index.append(j)
		ASTNode[root]["NodesPosition"] = index
		Break = False
		BreakPos = []
	ForOrSwitch = None
	return ASTNode[root]["NodesPosition"]