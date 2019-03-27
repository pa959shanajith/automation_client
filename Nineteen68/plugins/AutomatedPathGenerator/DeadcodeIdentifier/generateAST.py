import os
import subprocess
import sys
import zipfile
import tarfile
import dataStructDeadCode
import ObjectExtraction
import controller
import logging
import logger
log = logging.getLogger('generateAST.py')
from generatePdf import Report

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
		zf = zipfile.ZipFile(jar_file, 'r')
		try:
			lst = zf.infolist()
			for zi in lst:
				fn = zi.filename
				if fn.endswith('.java'):
					zf.extract(fn)
					self.open_file(fn,java_version)
		finally:
			zf.close()

	#function to open Tar File
	def open_tar(self,tar_file,java_version):
		tf = tarfile.TarFile(tar_file, 'r')
		try:
			lst = tf.getnames()
			for zi in lst:
				tf.extract(zi, path="")
				self.open_file(zi,java_version)
		finally:
			tf.close()

	def open_folder(self,folder,java_version):
		lst = os.listdir(folder)
		for filename in lst:
			filename = folder+"/" + filename
			if os.path.isdir(filename):
				self.open_folder(filename,java_version)
			elif os.path.isfile(filename):
				self.open_file(filename,java_version)

	def pmdCall(self,language,pathToFile):
		os.chdir(r'./Lib/site-packages/PMD/deadcode_identifier')
		subprocess.call(['java', '-classpath', r'.\lib\*;.' ,r'src.DD' ,str(language) , pathToFile],shell="false")

	def open_file(self,filename,java_version):
		try:
			filename = filename.replace("/", "\\")
			name = filename.split('\\')[-1][:-5]
			if filename.find(".java")>0:
				self.pmdCall(java_version,filename)
			else:
				return
			root = dataStructDeadCode.start()
			os.remove(r'./ASTTree.txt')
			os.chdir(os.environ["NINETEEN68_HOME"])
			if root:
				logger.print_on_console(filename)
				filePath = os.path.abspath(filename)
				self.showData = ObjectExtraction.main(root,self.showData,filePath)
				del root
			else:
				logger.print_on_console("Java file %s has Errors" %(filename))
		except IOError:
			logger.print_on_console('The filepath that is entered does not exist.')

	def checkformat(self,source,java_version):
		if source.find(".tar") > 0:
			self.open_tar(source,java_version)
		elif source.find(".zip") > 0:
			self.open_zip(source,java_version)
		elif source.find(".java") > 0:
			self.open_file(source,java_version)
		else:
			self.open_folder(source,java_version)
		self.reportCreation(self.showData)

	def start(self,version,path):
		try:
			logger.print_on_console('Starting Deadcode Identifier...')
			self.checkformat(path,version)
			os.startfile("Report.pdf")
			return True
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
