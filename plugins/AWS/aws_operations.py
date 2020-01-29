#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import requests
import boto3
import time
import json
import logger
import logging
from datetime import datetime

log = logging.getLogger('aws_operations.py')

RUN_TIMEOUT_SECONDS = 60 * 10
WEB_URL_TEMPLATE = 'https://us-west-2.console.aws.amazon.com/devicefarm/home#/projects/%s/runs/%s'

AWS_Path=os.environ['NINETEEN68_HOME']+os.sep+'plugins'+os.sep+'AWS'
AWS_assets=os.environ['NINETEEN68_HOME']+os.sep+'plugins'+os.sep+'AWS'+os.sep+'AWS_assets'
AWS_config_path=AWS_assets+os.sep+'AWS_config.json'
AWS_cred_path=AWS_assets+os.sep+'config'
AWS_output_path=AWS_assets+os.sep+'output'
bundle_name='Test_Bundle'

os.environ["AWS_SHARED_CREDENTIALS_FILE"]=AWS_cred_path+os.sep+'credentials'
os.environ["AWS_CONFIG_FILE"]=AWS_cred_path+os.sep+'config'


class AWS_Operations:

    def __init__(self,cur_date,profile_name=None):
        if profile_name is None:
            profile_name='default'
        self.session=boto3.Session(profile_name=profile_name)
        self.dc=self.session.client('devicefarm')
        self.cur_date=cur_date



    def get_run_configurations(self):
        try:
            conf = open(AWS_config_path, 'r')
            params = json.load(conf)
            conf.close()
            self.profile_name=None
            if 'profilename' in params:
                self.profile_name=params['profilename']
            self.project_name=params['projectname']
            self.pool_name=params['poolname']
            self.apk_path=params['apkpath']
            self.app_name=params['appname']
            self.package_name=params['packagename']
            self.file_path=params['filepath']
            self.android_test_spec=params['android_testspec']
            self.ios_test_spec=params['ios_testspec']
            # self.test_spec_path=AWS_assets+os.sep+params['testspec']


        except Exception as e:
            logger.print_on_console('Error while getting Run configurations')
            log.error(e)


    def create_project(self,project_name):
        p_arn=self.dc.create_project(name=project_name,defaultJobTimeoutMinutes=150)
        return p_arn['project']['arn']

    def create_upload(self,project_arn, upload_type, name, file_path):
        # name needs to be a file name like app-releaseProduction.apk, not "Android App"
    ##    logger.info('Uploading %s %r' % (upload_type, file_path))
        result = self.dc.create_upload(
            projectArn=project_arn,
            name=name,
            type=upload_type
        )
        upload = result['upload']
        log.debug(upload)
        self._upload_presigned_url(upload['url'], file_path)
        return upload['arn']

    def wait_for_upload(self,arn):
        return self._poll_until(
            self.dc.get_upload,
            arn,
            get_status_callable=lambda x: x['upload']['status'],
            success_statuses=('SUCCEEDED', ),
            check_every_seconds=10
        )

    def _upload_presigned_url(self,url, file_path):
        with open(file_path,"rb") as fp:
            data = fp.read()
            result = requests.put(url, data=data)
            assert result.status_code == 200

    def _poll_until(self,method, arn, get_status_callable, success_statuses, check_every_seconds=10,timeout_seconds=180):
        # check_every_seconds = 10
        #if timeout_seconds == RUN_TIMEOUT_SECONDS else 1
        start = time.time()
        while True:
            result = method(arn=arn)
            current_status = get_status_callable(result)
            if current_status in success_statuses:
                return result
            log.info('Waiting for %r status %r to be in %r' % (arn, current_status, success_statuses))
            now = time.time()
            if now - start > timeout_seconds:
                raise StopIteration('Time out waiting for %r to be done' % arn)
            time.sleep(check_every_seconds)

    def get_run_web_url(self,project_arn, test_run_arn):
    # project_arn = arn:aws:devicefarm:us-west-2:foo:project:NEW-ARN-HERE
    # test_run_arn = arn:aws:devicefarm:us-west-2:foo:run:project-arn/NEW-ARN-HERE
        project_arn_id = project_arn.split(':')[6]
        test_run_arid = test_run_arn.split('/')[1]
        return WEB_URL_TEMPLATE % (
            project_arn_id,
            test_run_arid,
        )



    def get_device_pool(self,project_arn,pool_name):
        d_list=self.dc.list_device_pools(arn=project_arn)['devicePools']
        for d in d_list:
            if d['name']==pool_name:
                device_pool_arn=d['arn']
                break
        return device_pool_arn




    def get_project(self,project_name):
        project_arn=None
        p_list=self.dc.list_projects()['projects']
        for p in p_list:
            if p['name']==project_name:
                project_arn=p['arn']
                break
        if project_arn==None:
            project_arn=self.create_project(project_name)
        return project_arn


    def get_app_arn(self,project_arn,upload_type,upload_file_name,*args):
        app_arn=None
        a_list=self.dc.list_uploads(arn=project_arn,type=upload_type)['uploads']
        for a in a_list:
            if a['name']==upload_file_name and a['status']=='SUCCEEDED':
                app_arn=a['arn']
                break
        if app_arn==None:
            app_arn=self.create_upload(project_arn, upload_type, upload_file_name, args[0])
        return app_arn

    def get_test_run(self,project_arn,test_name):
        test_run_arn=None
        run_list=self.dc.list_runs(arn=project_arn)['runs']
        for n in run_list:
            if n['name']==test_name:
                test_run_arn=n['arn']
        return test_run_arn


    def schedule_run(self,project_arn, name, device_pool_arn, app_arn, test_package_arn,spec_arn):
        logger.print_on_console('Scheduling test run %r' % name)
        result = self.dc.schedule_run(
            projectArn=project_arn,
            appArn=app_arn,
            devicePoolArn=device_pool_arn,
            name=name,
            test={
                'type': 'APPIUM_PYTHON',
                'testPackageArn': test_package_arn,
                'testSpecArn':spec_arn
    ##            'testSpecArn':'arn:aws:devicefarm:us-west-2::upload:4f8bd6b2-7be5-11e8-aself.dc0-fa7ae01bbebc'
            }
        )
        run = result['run']
        logger.print_on_console('Run Scheduled')
        log.info(run)
        return run['arn']



    def wait_for_run(self,test_run_arn,timeout):
        result = self._poll_until(
            self.dc.get_run,
            test_run_arn,
            get_status_callable=lambda x: x['run']['status'],
            success_statuses=('COMPLETED', ),
            check_every_seconds=60,
            timeout_seconds=timeout,
            
        )
        final_run = result['run']
        logger.print_on_console('Final run counts: %(counters)s' % final_run)
        log.info('Final run counts: %(counters)s' % final_run)
        return final_run['result'] == 'PASSED'



    def run_test(self,project_arn,app_arn,tp_arn,spec_arn,device_pool_arn):
        # time=str(datetime.now())
        name='Test_Run_'+self.cur_date

        test_run_arn = self.schedule_run(
                project_arn,
                name=name,
                device_pool_arn=device_pool_arn,
                app_arn=app_arn,
                test_package_arn=tp_arn,
                spec_arn=spec_arn
            )
        download_type='FILE'
        


        # print (self.get_run_web_url(project_arn,test_run_arn))
        run_status=self.wait_for_run(test_run_arn,340)
        logger.print_on_console('Run completed')
        log.info('Run completed')
        self.download_results(test_run_arn,download_type,AWS_output_path)
        return run_status

    def configure_run(self,project_name,app_name,package_name,pool_name):


        #get the project Arn
        project_arn=self.get_project(project_name)
        log.debug ('project_arn',project_arn)

        #get device pool
        device_pool_arn=self.get_device_pool(project_arn,pool_name)
        log.debug ('device_pool_arn',device_pool_arn)

        if self.apk_path[-3:] == 'ipa':
            app_arn=self.get_app_arn(project_arn,'IOS_APP',app_name,self.apk_path)
        else:
            app_arn=self.get_app_arn(project_arn,'ANDROID_APP',app_name,self.apk_path)
        status=self.wait_for_upload(app_arn)
        log.debug ('app_arn',app_arn)

        #get test package name
        ##tp_arn=get_app_arn(project_arn,upload_type2,'TEST1.zip')
        tp_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_PACKAGE',package_name,self.file_path)
        status=self.wait_for_upload(tp_arn)
        log.debug ('tp_arn',tp_arn)

        #get test spec name
        if self.apk_path[-3:] == 'ipa':
            # spec_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_SPEC','Default TestSpec for iOS Appium 1.9.1 Python (Support for iOS 12)')
            spec_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_SPEC',self.ios_test_spec,AWS_assets+os.sep+self.ios_test_spec)
        else:
            # spec_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_SPEC','Default TestSpec for Android Appium Python')
            spec_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_SPEC',self.android_test_spec,AWS_assets+os.sep+self.android_test_spec)
        log.debug ('spec_arn',spec_arn)
        info_msg="All details fetched to Schedule Run"
        log.info(info_msg)
        logger.print_on_console(info_msg)
        return project_arn,app_arn,tp_arn,spec_arn,device_pool_arn


    def run_aws_android_tests(self):
        self.get_run_configurations()
        project_arn,app_arn,tp_arn,spec_arn,device_pool_arn=self.configure_run(self.project_name,self.app_name,self.package_name,self.pool_name)
        return self.run_test(project_arn,app_arn,tp_arn,spec_arn,device_pool_arn)

    def download_results(self,test_run_arn,download_type,output_dir):
    ##    artifcats=self.dc.list_artifacts(arn='arn:aws:devicefarm:us-west-2:197128414257:run:02a594e3-ea23-48f8-a630-eac93487a7b1/25self.dc69bc-2907-4612-b890-92a66c0377d0',type='FILE')['artifacts']
        artifcats=self.dc.list_artifacts(arn=test_run_arn,type=download_type)['artifacts']
        logger.print_on_console('Outputs are stored here '+output_dir)
        log.info('Outputs are stored here '+output_dir)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        for a in artifcats:
            msg='Downloading ',a['type'],a['name']
            if a['type'] in ['CUSTOMER_ARTIFACT','VIDEO','TESTSPEC_OUTPUT']:
                logger.print_on_console(msg)
                log.info(msg)
                output_file=output_dir+"/"+a['name']+'.'+a['extension']
                output_url=a['url']
                r=requests.get(output_url)
                fd=open(output_file,'wb')
                fd.write(r.content)
                fd.close()
                time.sleep(1)
        msg="All files downloaded into"
        logger.print_on_console(msg)
        log.info(msg)





