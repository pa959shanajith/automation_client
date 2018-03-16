import sys
import re
import os

ASTNode = []

def next_line(line):
    try:
        num, line = divide(line.strip("\n"))
        return num, line
    except Exception as e:
        pass

def divide(line):
    try:
        space = line.find(" ")
        num = line[0:space]
        return int(num), line[space + 1:]
    except Exception as e:
        pass

def start(name):
    global ASTNode
    ASTNode = []
    try:
        with open(r'./ASTTree' + name + '.txt', 'rt') as f:
            line = f.readline()
            level, value = next_line(line)
            if value.find(":") != -1:
                ASTNode.append({"level": level,
                                "value": [value[:value.find(":")],
                                          value[value.find(":") + 1:]],
                                "child": [],
                                "parent": -1,
                                "NodesPosition": -1})
            else:
                ASTNode.append({"level": level, "value": [value, None], "child": [
                ], "parent": -1, "NodesPosition": -1})
            parent = 0
            for line in f:
                level, value = next_line(line)
                while(level <= ASTNode[parent]["level"]):
                    parent = ASTNode[parent]["parent"]
                if level > ASTNode[parent]["level"]:
                    if value.find(":") != -1:
                        ASTNode.append({"level": level,
                                        "value": [value[:value.find(":")],
                                                  value[value.find(":") + 1:]],
                                        "child": [],
                                        "parent": parent,
                                        "NodesPosition": -1})
                    else:
                        ASTNode.append({"level": level, "value": [value, None], "child": [
                        ], "parent": parent, "NodesPosition": -1})
                    ASTNode[parent]["child"].append(len(ASTNode) - 1)
                    parent = len(ASTNode) - 1
            f.close()
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        ASTNode = []
    return ASTNode