import os
import subprocess
import sys
import zipfile
import tarfile
import dataStruct
import ObjectExtract
#import OE
import CheckPossibleMethods
#import Visualization
import logger
import shutil
import json
import controller

class Flowgraph:
    def __init__(self):
        self.FlowChart = [] #List of all the FlowChart Nodes
        self.PosMethod = [] #List of all the PossibleMethods
        self.Classes = [] #List of all the Classes
        self.PossibleMethods = []
        self.filenames = set()
        self.socketIO = None

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
        flag = True
        try:
            lst = zf.infolist()
            for zi in lst:
                prev_classes = []
                fn = zi.filename
                filename = zf.extract(fn)
                if os.path.isdir(filename):
                    flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    prev_classes.extend(self.Classes)
                    flag = self.open_file(filename, java_version, True)
                    data = [c for c in self.Classes if c not in prev_classes]
                    for d in data:
                        self.socketIO.emit('flowgraph_result',json.dumps(d))
                if(not flag):
                    break
        finally:
            zf.close()
        return flag

    '''function to open tar file'''
    def open_tar(self, tar_file, java_version):
        tf = tarfile.TarFile(tar_file, 'r')
        flag = True
        try:
            lst = tf.getnames()
            for zi in lst:
                prev_classes = []
                filename = tf.extract(zi, path="")
                if os.path.isdir(filename):
                    flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    prev_classes.extend(self.Classes)
                    flag = self.open_file(filename, java_version, True)
                    data = [c for c in self.Classes if c not in prev_classes]
                    for d in data:
                        self.socketIO.emit('flowgraph_result',json.dumps(d))
                if(not flag):
                    break
        finally:
            tf.close()
        return flag

    '''function to open folder'''
    def open_folder(self, folder, java_version):
        flag = True
        try:
            lst = os.listdir(folder)
            for filename in lst:
                prev_classes = []
                filename = folder + "/" + filename
                if os.path.isdir(filename):
                    flag = self.open_folder(filename, java_version)
                elif (os.path.isfile(filename) and filename.endswith('.java')):
                    prev_classes.extend(self.Classes)
                    flag = self.open_file(filename, java_version, True)
                    data = [c for c in self.Classes if c not in prev_classes]
                    for d in data:
                        self.socketIO.emit('flowgraph_result',json.dumps(d))
                if(not flag):
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
                    self.FlowChart, self.Classes, self.PosMethod = ObjectExtract.main(
                        root, self.FlowChart, self.Classes, self.PosMethod)
                    if(not folder_flag):
                        for cls in self.Classes:
                            self.socketIO.emit("flowgraph_result",json.dumps(cls))
                    flag = True
                    del root
                else:
                    print("Java file %s has Errors!!!" % (filename))
        except Exception as e:
            print "open file",e
            import traceback
            print(traceback.format_exc())
        return flag

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
            import traceback
            traceback.print_exc()
        return flag

    def generate_flowgraph(self, version, source, socketIO, *args):
        try:
##            s = sys.stdout
##            p = sys.path
##            reload(sys)
##            sys.setdefaultencoding('Cp1252')
##            sys.setrecursionlimit(15000)
##            sys.stdout = s
##            sys.path = p
            self.socketIO=socketIO
            logger.print_on_console("Flowgraph generation in progress...")
            logger.print_on_console("File name:")
            logger.print_on_console("=============")
            '''This is to check the input is a zip/tar/java file or a folder.'''
            if (self.checkformat(int(version), source) ==
                    True):
                '''After check format, the flow chart would be made completely. So now, we'll check the possible method linking.'''
                self.PossibleMethods = CheckPossibleMethods.main(
                    self.PosMethod, self.Classes)

                JsonString = '{"MethodLink":['
                for i in range(0, len(self.PossibleMethods)):
                    if (self.PossibleMethods[i]["ParentNodeNo"]) is not None:
                        JsonString = JsonString + '{"NodeNo":"' + str(self.PossibleMethods[i]["NodeNo"]) + '","ParentNodeNo":"' + str(
                            self.PossibleMethods[i]["ParentNodeNo"]) + '","PosMethod":"' + self.PossibleMethods[i]["PosMethod"] + '"},'
                if JsonString[len(JsonString) - 1] == ',':
                    JsonString = JsonString[0:len(JsonString) - 1] + ']}'
                else:
                    JsonString = JsonString + ']}'

                data = {"classes":self.Classes,"method":self.PosMethod}
                with open("flowgraphdata.json", 'w') as outfile:
                    json.dump(data, outfile, indent=4, sort_keys=False)

##                '''OE.main will generate FlowChart.svg'''
##                Filename = OE.main(self.FlowChart)
##                '''Visualization.main will generate index.html, link it with js file and open it in the default browser.'''
##                logger.print_on_console("Visualizing graph...")
##                Visualization.main(Filename, JsonString)
                Filename = None
                JsonString = None
                data = {"classes":self.Classes, "result":"success"}
                self.socketIO.emit("result_flow_graph_finished", json.dumps(data))
                logger.print_on_console("Flowgraph generation completed")

            else:
                data = {"result":"fail"}
                self.socketIO.emit("result_flow_graph_finished", json.dumps(data))
                logger.print_on_console("Flowgraph generation failed")
##            s = sys.stdout
##            p = sys.path
##            reload(sys)
##            sys.setdefaultencoding('ascii')
##            sys.stdout = s
##            sys.path = p

        except Exception as e:
            print "generate flowgraph",e
            import traceback
            print (traceback.format_exc())