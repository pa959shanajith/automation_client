#-------------------------------------------------------------------------------
# Name:        testcase_compile.py
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import json
import shutil
import os
from zipfile import ZipFile
from datetime import datetime
keywords_list=[]
keywords_dict={}
from generic_operations import GenericOperations
from android_spinner_keywords import Spinner_Keywords
from android_operations_keywords import MobileOpeartions
import aws_operations
from aws_operations import *


class TestcaseCompile():

    def __init__(self,cur_date):
        self.mob_actions=MobileOpeartions()
        self.gen_actions=GenericOperations()
        self.spinner_actions=Spinner_Keywords()
        mobile_keywords=dir(self.mob_actions)
        generic_keywords=dir(self.gen_actions)
        spinner_keywords=dir(self.spinner_actions)
        self.cur_date=cur_date

        self.mobile_keywords_dict = { i.replace('_','').lower():i for i in mobile_keywords}
        self.generic_keywords_dict = { i.replace('_','').lower():i for i in generic_keywords}
        self.spinner_keywords_dict = { i.replace('_','').lower():i for i in spinner_keywords}

    def save_config(self,keys,values):
        status=True
        try:
            f=open(AWS_config_path,'r+')
            config_data=json.loads(f.read())
            for k,v in zip(keys,values):
                config_data[k]=v
            f.seek(0)
            f.truncate()
            f.write(json.dumps(config_data,indent=4, sort_keys=False))
            f.close()
        except Exception as e:
            status=False
            log.error(e)
        return status




    def compile_tc(self,tspList,scenario_counter,scenario_name):
        compile_status=True
        # cur_date=str(datetime.now()).replace(' ','_').replace('.','_').replace(':','_')
        launch_status=False
        log.info("Compiling Scenario "+str(scenario_counter)+':'+scenario_name)
        logger.print_on_console("Compiling Scenario "+str(scenario_counter)+':'+scenario_name)
        filename='test_scenario'+str(scenario_counter)+'_'+scenario_name+'_'+self.cur_date
        pytest_file=filename+'.py'
        f=open(pytest_file,"w")
        code="""import pytest
import time
import logging
import os
from generic_operations import GenericOperations
from android_spinner_keywords import Spinner_Keywords
from android_operations_keywords import MobileOpeartions
from test_constants import *
logging.basicConfig(filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
log=logging.getLogger('test.py')

def test_scenario():
\tmob_obj=MobileOpeartions()
\tgen_obj=GenericOperations()
\tspinner_obj=Spinner_Keywords()
\ttime.sleep(5)
\tmob_obj.start_server()"""
        f.write(code)
        launch_status=False
        # counter=1
        for t in tspList:

            inputs=t.inputval[0].split(';')
            inputs[0]=inputs[0].strip()
            if t.name.lower() in self.mobile_keywords_dict:
                if t.name.lower()=='launchapplication':
                    
                    if inputs[0]!='':
                        inputs[1]=inputs[0].split(os.sep)[-1]
                        launch_status=self.save_config(['apkpath','appname'],[inputs[0],inputs[1]])

                        continue
                    if not launch_status:
                        compile_status=False
                        err_msg='Invalid Input for Launch Application : Execution stopped'
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                        break
                elif t.name.lower()=='waitforelementexists':
                    inputs[0]=t.objectname
                               
                f.write("\n\ttime.sleep(2)")
                f.write("\n\tmob_ele=mob_obj.getMobileElement"+"('"+t.objectname+"')")
                f.write("\n\t"+"result=mob_obj."+self.mobile_keywords_dict[t.name.lower()]+"(mob_ele,*"+str(inputs)+")")
                # if counter==1:
                #     f.write("\n\tif result[0]==TEST_RESULT_FAIL:")
                #     f.write('\n\t\tmob_obj.driver.press_keycode(4)')
                #     f.write('\n\t\tmob_obj.driver.swipe(1,1,2,2, 3000)')
                #     counter+=1
            elif t.name.lower() in self.spinner_keywords_dict:
                f.write("\n\ttime.sleep(2)")
                f.write("\n\tmob_ele=mob_obj.getMobileElement"+"('"+t.objectname+"')")
                f.write("\n\t"+"result=spinner_obj."+self.spinner_keywords_dict[t.name.lower()]+"(mob_obj.driver,mob_ele,*"+str(t.inputval[0].split(';'))+")")
            elif t.name.lower() in self.generic_keywords_dict:
                f.write("\n\ttime.sleep(2)")
                f.write("\n\t"+"result=gen_obj."+self.generic_keywords_dict[t.name.lower()]+"(*"+str(t.inputval[0].split(';'))+")")
            else:
                logger.print_on_console (t.name,' is not supported')
                log.error(t.name+' is not supported')
                continue
            f.write("\n\tlog.info('Step %s : %s is executed and result is %s' % ('"+str(t.stepnum)+"','"+t.name+"',result[0]))")
            f.write("\n\tlog.info('----------------------------------------------------------------------------------')")


        f.close()
        dest_folder=AWS_assets+os.sep+bundle_name+os.sep+'tests'+os.sep+pytest_file
        shutil.move(pytest_file, dest_folder)
        # if launch_status:
        #     self.make_zip(pytest_file)

        log.info("Completed Compiling Scenario "+str(scenario_counter)+':'+scenario_name)
        logger.print_on_console("Completed Compiling Scenario "+str(scenario_counter)+':'+scenario_name)
        return compile_status,pytest_file

    def make_zip(self,pytest_files):
        """
        Purpose : Converting test_bundle folder  into .zip file
        pytest_files : List of all the pytest file generated from Nineteen68 which is to be
                      sent to AWS

        By-default : Test_Bundle is the folder in which required tests and python wheel
                     dependencies are already present

        """
        # dest_folder=AWS_assets+os.sep+bundle_name+os.sep+'tests'+os.sep+pytest_file
        # shutil.move(pytest_file, dest_folder)
        filelist=os.listdir(AWS_Path)
        for f in filelist:
            if f not in ['testcase_compile.py','aws_operations.py','AWS_assets','__pycache__']:
                destination=AWS_assets+os.sep+bundle_name+os.sep+'tests'+os.sep+f
                shutil.copy(AWS_Path+os.sep+f,destination)
        cur_dir=os.getcwd()
        os.chdir(AWS_assets+os.sep+bundle_name+os.sep)
        test_bundle=bundle_name+self.cur_date+'.zip'
        zip_file=ZipFile(test_bundle,'w')

	    # crawling through directory and subdirectories
        for root, directories, files in os.walk('./'):
            for filename in files:
                # join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                if (filename.startswith('test_scenario') and filename not in pytest_files) or ((filename.endswith('.zip') and filename != test_bundle)):
                    os.remove(filepath)
                    continue
                if test_bundle not in filename:
                    zip_file.write(filepath)

        zip_file.close()
        bundle_path=AWS_assets+os.sep+bundle_name+os.sep+test_bundle
        self.save_config(['packagename','filepath'],[test_bundle,bundle_path])
        os.chdir(cur_dir)



