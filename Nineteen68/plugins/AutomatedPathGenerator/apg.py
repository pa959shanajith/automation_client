import os
import subprocess
import sys
import zipfile
import tarfile
import dataStruct
import ObjectExtract
import CheckPossibleMethods
import logger
import shutil
import json
import re
import controller
import logging
from datetime import datetime
log = logging.getLogger('apg.py')
Cylomatic_Compelxity={}
prev_classes = []
varstorage = None

class AutomatedPathGenerator:
    def __init__(self,sockeIOobj):
        self.FlowChart = [] #List of all the FlowChart Nodes
        self.PosMethod = [] #List of all the PossibleMethods
        self.Classes = [] #List of all the Classes
        self.PossibleMethods = []
        self.filenames = set()
        self.socketIO = sockeIOobj
        self.ClassVariables= {}
        self.counter = 0

    '''function to open zip file'''
    def open_zip(self, zip_file, java_version):
        fstart = zip_file.rfind("\\")
        fend = zip_file.rfind(".")
        fname = zip_file[fstart:fend]
        try:
            shutil.rmtree("." + fname)
        except Exception as e:
            pass
        zf = zipfile.ZipFile(zip_file, 'r')
        error_flag = True
        try:
            lst = zf.infolist()
            for zi in lst:
                fn = zi.filename
                filename = zf.extract(fn)
                if os.path.isdir(filename):
                    error_flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    error_flag = self.open_file(filename, java_version)
                if(not error_flag):
                    break
        finally:
            zf.close()
        return error_flag

    '''function to open tar file'''
    def open_tar(self, tar_file, java_version):
        tf = tarfile.TarFile(tar_file, 'r')
        error_flag = True
        try:
            lst = tf.getnames()
            for zi in lst:
                filename = tf.extract(zi, path="")
                if os.path.isdir(filename):
                    error_flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    error_flag = self.open_file(filename, java_version)
                if(not error_flag):
                    break
        finally:
            tf.close()
        return error_flag

    '''function to open folder'''
    def open_folder(self, folder, java_version):
        error_flag = True
        try:
            lst = os.listdir(folder)
            for filename in lst:
                filename = folder + "\\" + filename
                if os.path.isdir(filename):
                    error_flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    error_flag = self.open_file(filename, java_version)
                if(not error_flag):
                    break
        except Exception as e:
            pass
        return error_flag

    '''This call will generate the AST Using PMD Parser and store it in ASTTree.txt'''
    def pmdCall(self, version, pathToFile, filename):
        os.chdir(r'./Lib/site-packages')
        subprocess.call(['java',
                         '-classpath',
                         r'.\flowgraph_lib\*;.',
                         r'PMD.DD',
                         str(version),
                         pathToFile,
                         filename
                         ],
                        shell="false")

    '''function to open file'''
    def open_file(self, filename, java_version):
        flag = True
        try:
            global prev_classes, varstorage
            filename = filename.replace("/", "\\")
            name = filename.split('\\')[-1][:-5]
            if filename not in self.filenames:
                if filename.find(".java", len(filename) - 5,
                                 len(filename)) > 0:
                    logger.print_on_console(filename)
                    self.filenames.add(filename)
                    # call to generate ASTTree
                    self.pmdCall(java_version, filename, name)
                # ASTTree 1st node(CompilationUnit) captured in root if no error is present
                root = dataStruct.start(name)
                os.remove(r'./ASTTree' + name + '.txt')
                os.chdir(os.environ["NINETEEN68_HOME"])
                if root:
                    # ObjectExtract.main will generate the FlowChart Nodes, give the Classes and all Possible Methods
                    prev_classes.extend(self.Classes)
                    self.FlowChart, self.Classes, PosMethod, self.ClassVariables, varstorage = ObjectExtract.main(
                        root, self.FlowChart, self.Classes, self.PosMethod)
                    (self.PosMethod).extend(PosMethod)
                    data = [c for c in self.Classes if c not in prev_classes]
                    for cls in data:
                        if(not controller.terminate_flag):
                            d = self.modifyJSON(cls, filename)
                            d['complexity']=self.cyclomatic_Complexity(filename,d['name'])
                            self.socketIO.emit('flowgraph_result',json.dumps(d))
                        else:
                            flag = False
                            break
                else:
                    flag = False
                    print("Java file %s has Errors!!!" % (filename.split('\\')[-1]))
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in open file")
        return flag

    def modifyJSON(self, cls, filename):
        try:
            output = []
            for keys in cls['methods']:
                for meth in cls['methods'][keys]:
                    method = meth['MethodName']+'('+meth['Variables']+'): '+meth['ResultType']
                    if meth['MethodType'][0] == 'package private':
                        output.append('~'+method)
                    elif meth['MethodType'][0] == 'private':
                        output.append('-'+method)
                    elif meth['MethodType'][0] == 'protected':
                        output.append('#'+method)
                    elif meth['MethodType'][0] == 'public':
                        output.append('+'+method)
            cls['abstract'] = False
            cls['classVariables'] = []
            if(cls['name'] in self.ClassVariables.keys()):
                cls['classVariables'] = self.ClassVariables[cls['name']]
            name = cls['name'].split('(',1)
            cls['name'] = name[0]
            if ('abstract' in name[1]):
                cls['abstract'] = True
            acc_mod = name[1].split(')',1)
            if(acc_mod[0] == 'package private'):
                cls['accessModifier'] = 'default'
            else:
                cls['accessModifier'] = acc_mod[0]
            cls['classMethods'] = output
            cls['id'] = self.counter
            self.counter = self.counter + 1
            cls['file'] = filename
        except Exception as e:
            pass
        return cls

    def checkformat(self, version, source):
        flag = True
        try:
            if source.find(".tar") > 0:
                flag = self.open_tar(source, version)
            elif source.find(".zip") > 0:
                flag = self.open_zip(source, version)
            elif source.find(".java") > 0:
                flag = self.open_file(source, version)
            else:
                flag = self.open_folder(source, version)
        except Exception as e:
            pass
        return flag

    def generate_flowgraph(self, version, source, *args):
        try:
            global Cylomatic_Compelxity, prev_classes, varstorage
            currentdate= datetime.now()
            beginingoftime = datetime.utcfromtimestamp(0)
            differencedate= currentdate - beginingoftime
            start_time = long(differencedate.total_seconds() * 1000.0)
            Cylomatic_Compelxity={}
            prev_classes=[]
            varstorage = None
            logger.print_on_console("Graph generation in progress...")
            logger.print_on_console("File name:")
            logger.print_on_console("=============")
            '''This is to check the input is a zip/tar/java file or a folder.'''
            if (self.checkformat(int(version), source) ==
                    True):
                '''After check format, the flow chart would be made completely. So now, we'll check the possible method linking.'''
                self.PossibleMethods = CheckPossibleMethods.main(
                    self.PosMethod, self.Classes, varstorage)
                #print self.PossibleMethods
                for i in range(0,len(self.FlowChart)):
                    self.FlowChart[i]['id']=i
                    if("'" in self.FlowChart[i]['text']):
                        self.FlowChart[i]['text'] = (self.FlowChart[i]['text']).replace("'", '"')
                    if(self.FlowChart[i]['class'] == 'import'):
                        start = i
                        while(self.FlowChart[i]['class'] == 'import'):
                            i = i + 1
                            end = i
                        classname = self.FlowChart[i]['class']
                        for j in range (start, end):
                            self.FlowChart[j]['class'] = classname

                '''jsonString contains the association links for the class diagram'''
                jsonString = []
                c_source=None
                c_target=None
                method_calls_count = {}
                for method in self.PossibleMethods:
                    if(method["MethodOrClassCall"] == "Variable"):
                        c_source = method["PresentClass"].split("(")[0]
                        c_target = method["Class"]
                        if(c_source != None and c_target != None and c_source != c_target):
                            jsonString.append({"source":c_source,"target":c_target})
                    elif(method["ParentNodeNo"] != None):
                        m = method["PosMethod"].split('(')[0]
                        for cls in self.Classes:
                            if (m in cls["methods"].keys()):
                                c_target = cls["name"]
                                break
                            elif (m == cls["name"]):
                                c_target = cls["name"]
                                break
                        if(method.has_key("PresentClass")):
                            c_source = method["PresentClass"].split("(")[0]
                        if(c_source != None and c_target != None):
                            if(c_source != c_target):
                                jsonString.append({"source":c_source,"target":c_target})
                            id = None
                            for fc in self.FlowChart:
                                if((fc['class'].split('(')[0] == c_source) and (m in fc['text']) and ('Method Name:' not in fc['text'])):
                                    for trgt in self.FlowChart:
                                        if((trgt['class'].split('(')[0] == c_target) and (m in trgt['text']) and ('Method Name:' in trgt['text'])):
                                            id = trgt['id']
                                            break
                                    if(not method_calls_count.has_key(fc['method'])):
                                        method_calls_count.update({fc['method']:{'within':0,'outside':0}})
                                    if(isinstance(fc['child'],list)):
                                        fc['child'].append(id)
                                    else:
                                        fc['child'] = [id]
                                    if(c_source == c_target):
                                        fc['within'] = True
                                        method_calls_count[fc['method']]['within'] += 1
                                    else:
                                        fc['outside'] = True
                                        method_calls_count[fc['method']]['outside'] += 1
                                    break
                jsonString = [dict(t) for t in set([tuple(d.items()) for d in jsonString])]

                '''To compress similar nodes in data-flow into one'''
                test = []
                i = 0
                flag = False
                while(i < len(self.FlowChart)):
                    if(self.FlowChart[i]['shape'] == 'Square'):
                        start = i
                        parent = self.FlowChart[i]['id']
                        i = i + 1
                        f = False
                        while(i <len(self.FlowChart) and self.FlowChart[i]['shape'] == 'Square' and self.FlowChart[i-1]['child'] == [self.FlowChart[i]['id']]
                        and self.FlowChart[i]['child'] == [self.FlowChart[i]['id']+1]):
                            id = self.FlowChart[i]['id']
                            parent = id
                            for fc in self.FlowChart:
                                if(fc['child'] != None and (id in fc['child']) and fc['id'] > id):
                                    f = True
                                    break
                            if(not f):
                                self.FlowChart[start]['text'] += '\n' + self.FlowChart[i]['text']
                                self.FlowChart[i]['delete'] = 'true'
                                end = i
                                flag = True
                            i = i + 1
                        if (flag):
                            self.FlowChart[start]['child'] = self.FlowChart[end]['child']
                            self.FlowChart[end+1]['parent'] = [start]
                            flag = False
                    else:
                        i = i + 1
                for fc in self.FlowChart:
                    if not (fc.has_key('delete')):
                        test.append(fc)

                currentdate = datetime.now()
                differencedate= currentdate - beginingoftime
                end_time = long(differencedate.total_seconds() * 1000.0)

                data = {"links":jsonString, "data_flow":test, "result":"success", "starttime":start_time,
                        "endtime":end_time, "method_calls_count":method_calls_count}
                self.socketIO.emit("result_flow_graph_finished", json.dumps(data))
                logger.print_on_console("Graph generation completed")

            else:
                if(controller.terminate_flag == True):
                    logger.print_on_console("---------Termination Completed-------")
                data = {"result":"fail"}
                self.socketIO.emit("result_flow_graph_finished", json.dumps(data))
                logger.print_on_console("Graph generation failed")

            controller.terminate_flag = False
        except Exception as e:
            data = {"result":"fail"}
            self.socketIO.emit("result_flow_graph_finished", json.dumps(data))
            logger.print_on_console("Graph generation failed")
            import traceback
            print (traceback.format_exc())
            log.error(e)
            logger.print_on_console("Error occured while generate graph.")

    def extract_Complexity(self,line):
        name=""
        complexity=""
        name = re.findall(r"['](.*?)[']",line)
        if len(name)!=0:
            name = re.sub(r"\s?\(.*?\)",r"",name[0])
        complexity=re.search("cyclomatic complexity of (\d+)",line,re.IGNORECASE).group(1)
        complexity = "1" if complexity=="0" else complexity
        line_no=re.search(r'.*:([^:]*):',line).group(1)
        return name,complexity,line_no

    def cyclomatic_Complexity(self,filepath,cname):
        try:
             global Cylomatic_Compelxity
             error_flag_cc=False
             cdata={'class':'', 'methods':[],'line_no':''}
             if not filepath in Cylomatic_Compelxity:
                 complexity_data={}
                 subprocess.call(['java','-classpath',r'./Lib/site-packages/flowgraph_lib/Cyclomatic/*','net.sourceforge.pmd.PMD','-d',
                                    str(filepath),'-R','category/java/design.xml/CyclomaticComplexity','-f','text','>','Output.txt'],shell="false")

                 file= open('./Output.txt','r+')
                 flag_name=''
                 for i in file:
                    if 'The class' in i:
                        flag_name=''
                        class_name,complexity,line_no=self.extract_Complexity(i)
                        flag_name=class_name
                        if not (class_name in complexity_data):
                            complexity_data[class_name]=complexity
                            complexity_data[flag_name+'_methods']=[]
                            complexity_data[flag_name+'line_no']=line_no
                        else:
                            error_flag_cc=True
                    elif 'The method' in i:
                            method_name,complexity,line_no=self.extract_Complexity(i)
                            complexity_data[flag_name+'_methods'].append({'methodname':method_name,'complexity':complexity,'line_no':line_no})
                 Cylomatic_Compelxity[filepath]=complexity_data
                 file.close()
                 os.remove('./Output.txt')
                 if cname in complexity_data:
                    cdata['class']=complexity_data[cname]
                    cdata['line_no']=complexity_data[cname+'line_no']
                    cdata['methods']=complexity_data[cname+'_methods']
                 else:
                    cdata="Undefined"
             else:
                if cname in Cylomatic_Compelxity[filepath]:
                    cdata['class'] = Cylomatic_Compelxity[filepath][cname]
                    cdata['line_no'] = Cylomatic_Compelxity[filepath][cname+'line_no']
                    cdata['methods']=Cylomatic_Compelxity[filepath][cname+'_methods'] if cname+'_methods' in Cylomatic_Compelxity[filepath] else []
                else:
                    cdata="Undefined"
             return cdata
        except Exception as e:
            logger.print_on_console("Error occured while calculating complexity")
            log.error(e)

    def open_file_in_editor(self, editor, filepath, linenumber):
        try:
            if os.path.exists(filepath):
                linenumberOption = "-n" + str(linenumber)
                editorOption = "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
                command = editorOption + " " + linenumberOption + " " + filepath
                logger.print_on_console('Opening file %s' % filepath)
                editor_process = subprocess.Popen(command)
                data = {'status' : 'success','message' : 'successfully opened file'}
                self.socketIO.emit('open_file_in_editor_result',json.dumps(data))
            else:
                logger.print_on_console("File ",filepath ," is removed or deleted")
                data = {'status': 'fail','message': "File is removed or deleted"}
                self.socketIO.emit('open_file_in_editor_result', json.dumps(data))
        except Exception as e:
            logger.print_on_console("Error occured while opening file")
            data = {'status': 'fail', 'message': "Notepad++ installation filepath is not correct"}
            self.socketIO.emit('open_file_in_editor_result', json.dumps(data))
            log.error(e)