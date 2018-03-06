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
import controller
import logging
log = logging.getLogger('apg.py')
Cylomatic_Compelxity={}
class AutomatedPathGenerator:
    def __init__(self):
        self.FlowChart = [] #List of all the FlowChart Nodes
        self.PosMethod = [] #List of all the PossibleMethods
        self.Classes = [] #List of all the Classes
        self.PossibleMethods = []
        self.filenames = set()
        self.socketIO = None
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
        term_flag = True
        try:
            lst = zf.infolist()
            for zi in lst:
                prev_classes = []
                fn = zi.filename
                filename = zf.extract(fn)
                if os.path.isdir(filename):
                    error_flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    prev_classes.extend(self.Classes)
                    error_flag = self.open_file(filename, java_version, True)
                    data = [c for c in self.Classes if c not in prev_classes]
                    for d in data:
                        if(not controller.terminate_flag):
                            d = self.modifyJSON(d,filename)
                            d['complexity']=self.cyclomatic_Complexity(filename,d['name'])
                            self.socketIO.emit('flowgraph_result',json.dumps(d))
                        else:
                            term_flag = False
                            break
                if((not error_flag) or (not term_flag)):
                    break
        finally:
            zf.close()
        return error_flag

    '''function to open tar file'''
    def open_tar(self, tar_file, java_version):
        tf = tarfile.TarFile(tar_file, 'r')
        error_flag = True
        term_flag = True
        try:
            lst = tf.getnames()
            for zi in lst:
                prev_classes = []
                filename = tf.extract(zi, path="")
                if os.path.isdir(filename):
                    error_flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    prev_classes.extend(self.Classes)
                    error_flag = self.open_file(filename, java_version, True)
                    data = [c for c in self.Classes if c not in prev_classes]
                    for d in data:
                        if(not controller.terminate_flag):
                            d = self.modifyJSON(d,filename)
                            d['complexity']=self.cyclomatic_Complexity(filename,d['name'])
                            self.socketIO.emit('flowgraph_result',json.dumps(d))
                        else:
                            term_flag = False
                            break
                if((not error_flag) or (not term_flag)):
                    break
        finally:
            tf.close()
        return error_flag

    '''function to open folder'''
    def open_folder(self, folder, java_version):
        error_flag = True
        term_flag = True
        try:
            lst = os.listdir(folder)
            for filename in lst:
                prev_classes = []
                filename = folder + "\\" + filename
                if os.path.isdir(filename):
                    error_flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    prev_classes.extend(self.Classes)
                    error_flag = self.open_file(filename, java_version, True)
                    data = [c for c in self.Classes if c not in prev_classes]
                    for d in data:
                        if(not controller.terminate_flag):
                            d = self.modifyJSON(d,filename)
                            d['complexity']=self.cyclomatic_Complexity(filename,d['name'])
                            self.socketIO.emit('flowgraph_result',json.dumps(d))
                        else:
                            term_flag = False
                            break
                if((not error_flag) or (not term_flag)):
                    break
        except Exception as e:
            pass
        return flag

    '''This call will generate the AST Using PMD Parser and store it in ASTTree.txt'''
    def pmdCall(self, version, pathToFile):
        os.chdir(r'./Nineteen68/plugins/AutomatedPathGenerator')
        subprocess.call(['java',
                         '-classpath',
                         r'.\flowgraph_lib\*;.',
                         r'PMD.DD',
                         str(version),
                         pathToFile,
                         ],
                        shell="false")

    '''function to open file'''
    def open_file(self, filename, java_version, folder_flag):
        flag = False
        try:
            filename = filename.replace("/", "\\")
            if filename not in self.filenames:
                if filename.find(".java", len(filename) - 5,
                                 len(filename)) > 0:
                    logger.print_on_console(filename)
                    self.filenames.add(filename)
                    # call to generate ASTTree
                    self.pmdCall(java_version, filename)
                    os.chdir(os.environ["NINETEEN68_HOME"])
                # ASTTree 1st node(CompilationUnit) captured in root if no error is present
                root = dataStruct.start()
                if root:
                    # ObjectExtract.main will generate the FlowChart Nodes, give the Classes and all Possible Methods
                    self.FlowChart, self.Classes, PosMethod, self.ClassVariables = ObjectExtract.main(
                        root, self.FlowChart, self.Classes, self.PosMethod)
                    (self.PosMethod).extend(PosMethod)
                    if(not folder_flag):
                        for cls in self.Classes:
                            if(not controller.terminate_flag):
                                d = self.modifyJSON(cls,filename)
                                d['complexity']=self.cyclomatic_Complexity(filename,d['name'])
                                self.socketIO.emit('flowgraph_result',json.dumps(d))
                            else:
                                break
                    flag = True
                else:
                    print("Java file %s has Errors!!!" % (filename))
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in open file")
        return flag

    def modifyJSON(self, cls, filename):
        try:
            output = []
            for keys in cls['methods']:
                method = cls['methods'][keys][0]['MethodName']+'('+cls['methods'][keys][0]['Variables']+'): '+cls['methods'][keys][0]['ResultType']
                if cls['methods'][keys][0]['MethodType'][0] == 'package private':
                    output.append('~'+method)
                elif cls['methods'][keys][0]['MethodType'][0] == 'private':
                    output.append('-'+method)
                elif cls['methods'][keys][0]['MethodType'][0] == 'protected':
                    output.append('#'+method)
                elif cls['methods'][keys][0]['MethodType'][0] == 'public':
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
                flag = self.open_file(source, version, False)
            else:
                flag = self.open_folder(source, version)
        except Exception as e:
            pass
        return flag

    def generate_flowgraph(self, version, source, socketIO, *args):
        try:
            global Cylomatic_Compelxity
            self.socketIO=socketIO
            logger.print_on_console("Graph generation in progress...")
            logger.print_on_console("File name:")
            logger.print_on_console("=============")
            '''This is to check the input is a zip/tar/java file or a folder.'''
            if (self.checkformat(int(version), source) ==
                    True):
                '''After check format, the flow chart would be made completely. So now, we'll check the possible method linking.'''
                self.PossibleMethods = CheckPossibleMethods.main(
                    self.PosMethod, self.Classes)
                jsonString = []
                c_source=None
                c_target=None
                for method in self.PossibleMethods:
                    if(method["ParentNodeNo"] != None):
                        m = method["PosMethod"].split('(')[0]
                        for cls in self.Classes:
                            if (m in cls["methods"].keys()):
                                c_target = cls["name"]
                                break
                        if(method.has_key("PresentClass")):
                            c_source = method["PresentClass"].split("(")[0]
                        if(c_source != c_target and c_source != None and c_target != None):
                            jsonString.append({"source":c_source,"target":c_target})
                Cylomatic_Compelxity={}
                data = {"classes":self.Classes, "links":jsonString, "result":"success"}
                self.socketIO.emit("result_flow_graph_finished", json.dumps(data))
                if(not controller.terminate_flag):
                    logger.print_on_console("Graph generation completed")
                else:
                    logger.print_on_console("---------Termination Completed-------")
                controller.terminate_flag = False
            else:
                data = {"result":"fail"}
                self.socketIO.emit("result_flow_graph_finished", json.dumps(data))
                logger.print_on_console("Graph generation failed")

        except Exception as e
            log.error(e)
            logger.print_on_console("Error occured while generate graph.")


    def extract_Complexity(self,line):
        name = line[line.find('\'')+1:line.rfind('\'')]
        unqiue_str = 'has a Cyclomatic Complexity of '
        complexity = line[line.find('has a Cyclomatic Complexity of ')+len(unqiue_str):]
        complexity= complexity[:complexity.find(' ')]
        if complexity.find('.')!=-1:
            complexity=complexity[:complexity.find('.')]
        return name,complexity

    def cyclomatic_Complexity(self,filepath,cname):
        try:
             global Cylomatic_Compelxity
             error_flag_cc=False
             if not filepath in Cylomatic_Compelxity:
                 #filepath=os.path.normpath(filepath)
                 pmd_path = os.environ["NINETEEN68_HOME"]
                 pmd_path=pmd_path+'\\Nineteen68\\plugins\\AutomatedPathGenerator\\pmd.bat'
                 command = pmd_path + ' -d '+ filepath +' -R rulesets/java/codesize.xml -f text > Output.txt'
                 complexity_data={}
                 os.system(command)
                 #logger.print_on_console(command)
                 file= open('Output.txt','r+')
                 flag_name='';
                 for i in file:
                    if 'The class' in i and 'has a Cyclomatic Complexity of ' in i:
                        flag_name=''
                        class_name,complexity=self.extract_Complexity(i)
                        flag_name=class_name
                        if not (class_name in complexity_data):
                            complexity_data[class_name]=complexity
                        else:
                            error_flag_cc=true
                           #print 'Error'
                    elif 'The method' in i and 'has a Cyclomatic Complexity of ' in i:
                        method_name,complexity=self.extract_Complexity(i)
                        complexity_data[flag_name+'_'+method_name]=complexity
                 #logger.print_on_console(complexity_data)
                 Cylomatic_Compelxity[filepath]=complexity_data
                 file.close()
                 if cname in complexity_data:
                    return complexity_data[cname]
                 else:
                    return 4
             else:
                if cname in Cylomatic_Compelxity[filepath]:
                    return Cylomatic_Compelxity[filepath][cname]
                else:
                    return 4

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print e