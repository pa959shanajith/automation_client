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
from aws_keywords import *
import logger
import logging
log = logging.getLogger("testcase_compile.py")
from aws_operations import *


class TestcaseCompile():

    def __init__(self,cur_date):
        self.cur_date=cur_date.replace("-","_")
        self.apk_path = None

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
        filename='scenario'+str(scenario_counter)+'_'+scenario_name+'_'+self.cur_date
        pytest_file=filename+'.py'
        f=open(pytest_file,"w")
        code="""import pytest
import time
import logging
import os
import pytz
from generic_operations import GenericOperations
from android_spinner_keywords import Spinner_Keywords
from android_operations_keywords import MobileOpeartions
import datetime as dt
from pytz import timezone
from testmobile_constants import *
logging.basicConfig(filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
log=logging.getLogger('"""+pytest_file+""".py')

def scenario(driver):
\tmob_obj=MobileOpeartions()
\tgen_obj=GenericOperations()
\tspinner_obj=Spinner_Keywords()
\tres={}
\tscenario_exe_time=""
\ttimezone_req = pytz.timezone('Asia/Kolkata')
\tsc_time = dt.datetime.now(timezone_req)
\tscenario_exe_time= str(sc_time.replace(tzinfo=None))
"""
        f.write(code)
        launch_status=False
        # counter=1
        for t in tspList:

            inputs=t.inputval[0].split(';')
            inputs[0]=inputs[0].strip()
            ele_str = "(driver,'"+t.objectname+"')"
            if t.name.lower() in mobile_keywords:
                if t.name.lower()=='launchapplication':
                    self.apk_path = inputs[0]
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

                elif (t.custname not in ["@Android_Custom", "@CustomiOS"]) and (t.name.lower()=='waitforelementexists'):
                    inputs[0]=t.objectname

                elif t.custname in ["@Android_Custom", "@CustomiOS"]:
                    t.objectname = inputs,t.name.lower()
                    if t.name.lower()=='waitforelementexists':
                        inputs = t.objectname
                    elif len(inputs) == 3:
                        inputs = [""]
                    elif len(inputs) > 3:
                        inputs = inputs[3:]
                    ele_str = "(driver,\""+str(t.objectname)+"\")"
                
                
                inp_str = "(driver,mob_ele,*"+str(inputs)+")"
                f.write("\n\ttime.sleep(2)")
                f.write("\n\tmob_ele=mob_obj.getMobileElement"+ele_str)
                f.write("\n\t"+"result="+mobile_keywords[t.name.lower()]+inp_str)
                # if counter==1:
                #     f.write("\n\tif result[0]==TEST_RESULT_FAIL:")
                #     f.write('\n\t\tmob_obj.driver.press_keycode(4)')
                #     f.write('\n\t\tmob_obj.driver.swipe(1,1,2,2, 3000)')
                #     counter+=1
            elif t.name.lower() in generic_keywords:
                f.write("\n\ttime.sleep(2)")
                f.write("\n\t"+"result="+generic_keywords[t.name.lower()]+"(*"+str(t.inputval[0].split(';'))+")")
            else:
                logger.print_on_console (t.name,' is not supported')
                log.error(t.name+' is not supported')
                compile_status=False
                continue
            f.write("\n\tlog.info('Step %s : %s is executed and result is %s' % ('"+str(t.stepnum)+"','"+t.name+"',result[0]))")
            f.write("\n\tlog.info('----------------------------------------------------------------------------------')")
            f.write("\n\tres['"+str(t.stepnum)+"'] = result")
        f.write("\n\tprint('result:')")
        f.write("\n\tprint(res)")
        f.write("\n\treturn scenario_exe_time")
        f.close()
        if compile_status:
            dest_folder=AWS_assets+os.sep+bundle_name+os.sep+'tests'+os.sep+pytest_file
            shutil.move(pytest_file, dest_folder)

            log.info("Compilation Completed "+str(scenario_counter)+':'+scenario_name)
            logger.print_on_console("Compilation Completed "+str(scenario_counter)+':'+scenario_name)
        return compile_status,pytest_file


    def create_test_file(self,pytest_files):
        pytest_file='test_scenario_'+self.cur_date+'.py'
        f=open(pytest_file,"w")
        code="""import pytest
import time
import logging
import os
import pytz
import datetime as dt
from pytz import timezone
from android_operations_keywords import MobileOpeartions
logging.basicConfig(filemode='a',format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',level=logging.INFO)
log=logging.getLogger('test_scenario.py')\n"""
        f.write(code)
        call_scenarios="\n"
        timez_calc="\n"
        last_scenario_time="\n"
        append_time="\n"
        append_last_sctime=""
        s_counter=1
        for scenario in pytest_files:
            f.write("import "+scenario[:-3]+" as s"+str(s_counter)+"\n")
            call_scenarios+="\tt"+str(s_counter)+"="+"s"+str(s_counter)+".scenario(driver)\n"
            append_time+="\ttime_list.append(t"+str(s_counter)+")\n"
            s_counter+=1
        timez_calc="""\ttimezone_req=pytz.timezone('Asia/Kolkata')\n\tsc_time=dt.datetime.now(timezone_req)\n\tscenario_exe_time=str(sc_time.replace(tzinfo=None))\n"""
        last_scenario_time="\tt"+str(s_counter)+"="+"scenario_exe_time\n"
        append_last_sctime="\ttime_list.append(t"+str(s_counter)+")\n"
        print_list="""\n\tprint(time_list)"""
        import platform
        if platform.system() == 'Darwin':
            code="""def test_scenario():\n\tmob_obj=MobileOpeartions()\n\tdriver=mob_obj.start_server()"""
        else:
            package_name, activity_name = self.get_package_activity()
            code="""def test_scenario():\n\tmob_obj=MobileOpeartions()\n\tdriver=mob_obj.start_server('"""+package_name+"""','"""+activity_name+"""')"""
            list_time="""\n\ttime_list=[]"""
        f.write(code)
        f.write(list_time)
        f.write(call_scenarios)
        f.write(timez_calc)
        f.write(last_scenario_time)
        f.write(append_time)
        f.write(append_last_sctime)
        f.write(print_list)
        f.close()
        dest_folder=AWS_assets+os.sep+bundle_name+os.sep+'tests'+os.sep+pytest_file
        shutil.move(pytest_file, dest_folder)
        pytest_files.append(pytest_file)
        




    def make_zip(self,pytest_files):
        """
        Purpose : Converting test_bundle folder  into .zip file
        pytest_files : List of all the pytest file generated from Nineteen68 which is to be
                      sent to AWS

        By-default : Test_Bundle is the folder in which required tests and python wheel
                     dependencies are already present

        """
        logger.print_on_console('Creating Test Bundle...')
        log.info('Creating Test Bundle...')
        self.create_test_file(pytest_files)
        filelist=os.listdir(AWS_Path)
        for f in filelist:
            if f not in ['src','AWS_assets','__pycache__']:
                destination=AWS_tests_path+os.sep+f
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
                if (filename.find('scenario')>-1 and filename not in pytest_files) or (filename.endswith('.zip') and filename != test_bundle):
                    os.remove(filepath)
                    continue
                if test_bundle not in filename:
                    zip_file.write(filepath)

        zip_file.close()

        bundle_path=AWS_assets+os.sep+bundle_name+os.sep+test_bundle
        self.save_config(['packagename','filepath'],[test_bundle,bundle_path])
        os.chdir(cur_dir)



    def get_package_activity(self):
        package_name = activity_name = ""
        if self.apk_path == None:
            return package_name, activity_name
        else:
            try:
                aapt_home=os.environ['AAPT_HOME']
                cur_dir=os.getcwd()
                os.chdir(aapt_home)
                aapt_home = aapt_home + 'aapt.exe'
                import subprocess
                out = subprocess.Popen([aapt_home, 'dump','badging',self.apk_path],stdout= subprocess.PIPE, close_fds=True)
                for line in out.stdout.readlines():
                    curr_line = str(line)[2:-1]
                    if ('package:' in curr_line) and (package_name == ""):
                        curr_line = curr_line.strip().split()
                        package_name = curr_line[1][6:-1]
                        if (package_name != "" and activity_name != ""):
                            break
                    if ('launchable' in curr_line) and (activity_name == ""):
                        curr_line = curr_line.strip().split()
                        activity_name = curr_line[1][6:-1]
                        if (package_name != "" and activity_name != ""):
                            break
                os.chdir(cur_dir)
            except Exception as e:
                log.error(e,exc_info = True)
            return package_name, activity_name