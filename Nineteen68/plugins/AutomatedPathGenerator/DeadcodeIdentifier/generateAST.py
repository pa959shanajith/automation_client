import os
import subprocess
import zipfile
import tarfile
import dataStructDeadCode
import ObjectExtraction
import controller
import logging
import logger
log = logging.getLogger('generateAST.py')
from generatePdf import Report
from constants import *

class DeadcodeIdentifier():

	def __init__(self):
		self.showData = {"Unused Local Variable":[["Variable Name",
										   "Variable Type",
										   "Method Name",
										   "Class Name",
										   "File Path",
										   "Line No"
										   ]],

				"Unused Formal Parameter":[["Variable Name",
											"Variable Type",
											"Method Name",
											"Class Name",
											"File Path",
											"Line No"
											]],

				"Unused Imports":[["Import Name",
									"Class Name",
									"File Path",
									"Line No"
									]],

				"Empty If Statement":[["Method Name",
									   "Class Name",
									   "File Path",
										"Line No"
										]],

				"Empty For Loop":[["Method Name",
								   "Class Name",
								   "File Path",
								   "Line No"
								   ]],

				"Empty While Loop":[["Method Name",
									 "Class Name",
									 "File Path",
									 "Line No"
									 ]],

				"Empty Do While Loop":[["Method Name",
										"Class Name",
										"File Path",
										"Line No"
										]],

				"Empty Try/Catch Block":[["Method Name",
										  "Class Name",
										  "File Path",
										  "Line No"
										  ]],

				"Duplicate Imports":[["Import Name",
									  "Line No",
									  "File Path"
									  ]],

				"Unused Private Field":[["Variable Name",
										 "Variable Type",
										 "Class Name",
										 "File Path",
										 "Line No"
										 ]],

				"Java Lang Imports":[["Import Name",
									  "Class Name",
									  "File Path",
									  "Line No"
									  ]],

				"Multiple Return Statement":[["Method Name",
											  "Class Name",
											  "File Path",
											  "Line No"
											  ]],
				"Too Many Static Imports":[["File Path",
											"Line Nos' "
											]],
				"Unused Private Method":[["Method Name",
										  "Line No",
										  "Class Name",
										  "File Path"
										  ]],
				"Avoid Duplicate Literals":[["Literal Value",
											 "Class Name",
											 "Line No",
											 "FilePath"
											 ]]

				}

	#Function to open zip file
	def open_zip(self,jar_file,java_version):
		flag = True
		zf = zipfile.ZipFile(jar_file, 'r')
		try:
			lst = zf.infolist()
			for zi in lst:
				fn = zi.filename
				if fn.endswith('.java'):
					zf.extract(fn)
					flag = self.open_file(fn,java_version)
				if(not flag):
					break
		finally:
			zf.close()
		return flag

	#function to open Tar File
	def open_tar(self,tar_file,java_version):
		flag = True
		tf = tarfile.TarFile(tar_file, 'r')
		try:
			lst = tf.getnames()
			for zi in lst:
				tf.extract(zi, path="")
				flag = self.open_file(zi,java_version)
				if(not flag):
					break
		finally:
			tf.close()
		return flag

	def open_folder(self,folder,java_version):
		flag = True
		lst = os.listdir(folder)
		for filename in lst:
			filename = folder+"/" + filename
			if os.path.isdir(filename):
				flag = self.open_folder(filename,java_version)
			elif os.path.isfile(filename):
				flag = self.open_file(filename,java_version)
			if(not flag):
				break
		return flag

	def pmdCall(self,language,pathToFile):
		if SYSTEM_OS=='Darwin':
			os.chdir(os.environ['NINETEEN68_HOME']+'/lib/python2.7/site-packages/PMD/deadcode_identifier')
			subprocess.call(['java', '-classpath', './lib/*:.' ,'src.DD' ,str(language) , pathToFile],shell=False)
		else:
			os.chdir(r'./Lib/site-packages/PMD/deadcode_identifier')
			subprocess.call(['java', '-classpath', r'.\lib\*;.' ,r'src.DD' ,str(language) , pathToFile],shell="false")

	def open_file(self,filename,java_version):
		try:
			flag = True
			if (not controller.terminate_flag):
				if filename.find(".java")>0:
					self.pmdCall(java_version,filename)
				else:
					flag = False
				root = dataStructDeadCode.start()
				os.remove('./ASTTree.txt')
				os.chdir(os.environ["NINETEEN68_HOME"])
				if root:
					logger.print_on_console(filename)
					filePath = os.path.abspath(filename)
					self.showData = ObjectExtraction.main(root,self.showData,filePath)
					del root
				else:
					logger.print_on_console("Java file %s has Errors" %(filename))
					flag = False
			else:
				flag = False
		except IOError:
			logger.print_on_console('The filepath that is entered does not exist.')
		return flag

	def checkformat(self,source,java_version):
		flag = True
		if source.find(".tar") > 0:
			flag = self.open_tar(source,java_version)
		elif source.find(".zip") > 0:
			flag = self.open_zip(source,java_version)
		elif source.find(".java") > 0:
			flag = self.open_file(source,java_version)
		else:
			flag = self.open_folder(source,java_version)
		return flag

	def start(self,version,path):
		try:
			logger.print_on_console('Starting Deadcode Identifier...')
			flag = self.checkformat(path,version)
			if flag:
				self.reportCreation(self.showData)
				if SYSTEM_OS=='Darwin':
					subprocess.call(['open','Report.pdf'])
				else:
					os.startfile("Report.pdf")
				logger.print_on_console('Deadcode identification completed')
				return True
			else:
				if controller.terminate_flag:
					logger.print_on_console("---------Termination Completed-------")
					controller.terminate_flag = False
				return False
		except Exception as e:
			log.error(e)
			logger.print_on_console("Error occured in deadcode identifier")
			return False

	def reportCreation(self,ShowData):
		r = Report()
		for key in ShowData.keys():
			r.createTable(key,ShowData[key])
		r.save()
		return
