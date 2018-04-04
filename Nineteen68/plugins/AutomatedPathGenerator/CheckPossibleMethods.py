import logging
log = logging.getLogger('CheckPossibleMethods.py')
'''This method will link all the user-defined method call with their method definition.'''
def main(PossibleMethods, Classes):
    try:
        Variables = None
        for i in range(0, len(PossibleMethods)):
            PresentClass = PossibleMethods[i]["Class"]
            PosMethod = PossibleMethods[i]["PosMethod"]
            NoOfArguments = PossibleMethods[i]["NoOfArguments"]
            TypeOfArguments = PossibleMethods[i]["typeOfArguments"]
            MethodOrClassCall = PossibleMethods[i]["MethodOrClassCall"]
            PosMethodName = PosMethod[0:PosMethod.find("(")]
            if isinstance(PresentClass, str):
                for j in Classes:
                    if j["name"] == PresentClass:
                        PresentClass = j
                        break
                if isinstance(PresentClass, str):
                    continue
            else:
                PresentClass = Classes[PresentClass]
            if MethodOrClassCall == 'Method':
                if PosMethodName == 'this':
                    for j in PresentClass["constructors"]:
                        if NoOfArguments == j["NoOfFormalParameters"]:
                            if NoOfArguments > 0:
                                Variables = j["Variables"]
                                y = 0
                                while(Variables.find(",") != -1):
                                    x = Variables[:Variables.find(",")]
                                    if y < len(TypeOfArguments):
                                        if x[:x.find(
                                                " ")] == TypeOfArguments[y]:
                                            y = y + 1
                                            Variables.replace(
                                                Variables[:Variables.find(",") + 1], "")
                                        else:
                                            break
                                    else:
                                        break
                                if y < len(TypeOfArguments):
                                    if Variables[:Variables.find(
                                            " ")] == TypeOfArguments[y]:
                                        y = y + 1
                                if y == NoOfArguments:
                                    PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                            else:
                                PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                elif PosMethodName == 'super':
                    for j in Classes:
                        if j["name"] == PresentClass["extends"]:
                            PresentClass = j
                            if PresentClass["constructors"] is not None:
                                for j in PresentClass["constructors"]:
                                    if NoOfArguments == j["NoOfFormalParameters"]:
                                        if NoOfArguments > 0:
                                            Variables = j["Variables"]
                                            y = 0
                                            while(Variables.find(",") != -1):
                                                x = Variables[:Variables.find(
                                                    ",")]
                                                if y < len(TypeOfArguments):
                                                    if x[:x.find(
                                                            " ")] == TypeOfArguments[y]:
                                                        y = y + 1
                                                        Variables.replace(
                                                            Variables[:Variables.find(",") + 1], "")
                                                    else:
                                                        break
                                                else:
                                                    break
                                            if y < len(TypeOfArguments):
                                                if Variables[:Variables.find(
                                                        " ")] == TypeOfArguments[y]:
                                                    y = y + 1
                                            if y == NoOfArguments:
                                                PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                                        else:
                                            PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                elif PresentClass["methods"] is not None:
                    if PosMethodName in PresentClass["methods"]:
                        for j in (PresentClass["methods"])[PosMethodName]:
                            if NoOfArguments == j["NoOfFormalParameters"]:
                                '''if NoOfArguments > 0:
                                    Variables = j["Variables"]
                                    y = 0
                                    while(Variables.find(",") != -1):
                                        x = Variables[:Variables.find(",")]
                                        if y < len(TypeOfArguments):
                                            if x[:x.find(
                                                    " ")] == TypeOfArguments[y]:
                                                y = y + 1
                                                Variables.replace(
                                                    Variables[:Variables.find(",") + 1], "")
                                            else:
                                                break
                                        else:
                                            break
                                    if y < len(TypeOfArguments):
                                        if Variables[:Variables.find(
                                                " ")] == TypeOfArguments[y]:
                                            y = y + 1

                                    if y == NoOfArguments:
                                        PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                                else:
                                    PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]'''
                                PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                while PossibleMethods[i]["ParentNodeNo"] is None and PresentClass["extends"] is not None:
                    extend = False
                    for k in Classes:
                        if k["name"] == PresentClass["extends"]:
                            PresentClass = k
                            extend = True
                            break
                    if not extend:
                        break
                    if PosMethodName in PresentClass["methods"]:
                        for j in (PresentClass["methods"])[PosMethodName]:
                            if NoOfArguments == j["NoOfFormalParameters"]:
                                if NoOfArguments > 0:
                                    Variables = j["Variables"]
                                    y = 0
                                    while(Variables.find(",") != -1):
                                        x = Variables[:Variables.find(",")]
                                        if y < len(TypeOfArguments):
                                            if x[:x.find(
                                                    " ")] == TypeOfArguments[y]:
                                                y = y + 1
                                                Variables.replace(
                                                    Variables[:Variables.find(",") + 1], "")
                                            else:
                                                break
                                        else:
                                            break
                                    if y < len(TypeOfArguments):
                                        if Variables[:Variables.find(
                                                " ")] == TypeOfArguments[y]:
                                            y = y + 1
                                    if y == NoOfArguments:
                                        PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                                else:
                                    PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
            else:
                for k in Classes:
                    if k["name"] == PosMethodName:
                        if ((k["constructors"] is not None) and (k["constructors"] != [])):
                            for j in k["constructors"]:
                                if NoOfArguments == j["NoOfFormalParameters"]:
                                    if NoOfArguments > 0:
                                        Variables = j["Variables"]
                                        y = 0
                                        while(Variables.find(",") != -1):
                                            x = Variables[:Variables.find(",")]
                                            if y < len(TypeOfArguments):
                                                if x[:x.find(
                                                        " ")] == TypeOfArguments[y]:
                                                    y = y + 1
                                                    Variables.replace(
                                                        Variables[:Variables.find(",") + 1], "")
                                                else:
                                                    break
                                            else:
                                                break
                                        if y < len(TypeOfArguments):
                                            if Variables[:Variables.find(
                                                    " ")] == TypeOfArguments[y]:
                                                y = y + 1
                                        if y == NoOfArguments:
                                            PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                                    else:
                                        PossibleMethods[i]["ParentNodeNo"] = j["NodeNo"]
                        #else:
                         #   PossibleMethods[i]["ParentNodeNo"] = k["position"]
    except Exception as e:
        log.error(e)
    return PossibleMethods
