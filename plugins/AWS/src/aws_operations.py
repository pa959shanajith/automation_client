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

bundle_name='Test_Bundle'
AWS_Path=os.environ['NINETEEN68_HOME']+os.sep+'plugins'+os.sep+'AWS'
AWS_assets=os.environ['NINETEEN68_HOME']+os.sep+'plugins'+os.sep+'AWS'+os.sep+'AWS_assets'
AWS_config_path=AWS_assets+os.sep+'AWS_config.json'
AWS_cred_path=AWS_assets+os.sep+'config'
AWS_output_path=AWS_assets+os.sep+'output'
AWS_tests_path=AWS_assets+os.sep+bundle_name+os.sep+'tests'


os.environ["AWS_SHARED_CREDENTIALS_FILE"]=AWS_cred_path+os.sep+'credentials'
os.environ["AWS_CONFIG_FILE"]=AWS_cred_path+os.sep+'config'


class AWS_Operations:

    def __init__(self,cur_date,profile_name=None):
        if profile_name is None:
            profile_name='default'
        self.session=boto3.Session(profile_name=profile_name)
        self.dc=self.session.client('devicefarm')
        self.cur_date=cur_date
        self.terminateFlag=False



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
            self.test_run_arn = None
            # self.test_spec_path=AWS_assets+os.sep+params['testspec']


        except Exception as e:
            logger.print_on_console('Error while getting Run configurations')
            log.error(e)


    def create_project(self,project_name):
        result = None
        try:
            p_arn=self.dc.create_project(name=project_name,defaultJobTimeoutMinutes=150)
            result = p_arn['project']['arn']
        except Exception as e:
            logger.print_on_console('Error while creating Project')
            log.error(e)
        return result

    def create_upload(self,project_arn, upload_type, name, file_path):
        # name needs to be a file name like app-releaseProduction.apk, not "Android App"
        log.info('Uploading %s %r' % (upload_type, file_path))
        logger.print_on_console("Uploading ",name)
        result = None
        try:
            result = self.dc.create_upload(
                projectArn=project_arn,
                name=name,
                type=upload_type
            )
            upload = result['upload']
            log.debug(upload)
            self._upload_presigned_url(upload['url'], file_path)
            result = upload['arn']
        except Exception as e:
            logger.print_on_console('Error while creating Upload')
            log.error(e)
        return result

    def wait_for_upload(self,arn):
        result = None
        try:
            result = self._poll_until(
                self.dc.get_upload,
                arn,
                get_status_callable=lambda x: x['upload']['status'],
                success_statuses=('SUCCEEDED', ),
                check_every_seconds=10
            )
        except Exception as e:
            logger.print_on_console('Error while waiting for Upload')
            log.error(e)
        return result

    def _upload_presigned_url(self,url, file_path):
        try:
            with open(file_path,"rb") as fp:
                data = fp.read()
                result = requests.put(url, data=data)
                assert result.status_code == 200
        except Exception as e:
            logger.print_on_console('Error while uploading presigned URL')
            log.error(e)

    def _poll_until(self,method, arn, get_status_callable, success_statuses, check_every_seconds=5,timeout_seconds=180):
        # check_every_seconds = 10
        #if timeout_seconds == RUN_TIMEOUT_SECONDS else 1
        result=False
        try:
            start = time.time()
            while True:
                if self.terminateFlag:
                    break
                result = method(arn=arn)
                current_status = get_status_callable(result)
                if current_status in success_statuses:
                    return result
                elif current_status == 'FAILED':
                    raise StopIteration('Upload Failed for %r' % arn)
                log.info('Waiting for %r status %r to be in %r' % (arn, current_status, success_statuses))
                now = time.time()
                if now - start > timeout_seconds:
                    raise StopIteration('Time out waiting for %r to be done' % arn)
                time.sleep(check_every_seconds)
        except Exception as e:
            logger.print_on_console('Error / Time out while polling')
            log.error(e)
        return result

    def get_run_web_url(self,project_arn, test_run_arn):
    # project_arn = arn:aws:devicefarm:us-west-2:foo:project:NEW-ARN-HERE
    # test_run_arn = arn:aws:devicefarm:us-west-2:foo:run:project-arn/NEW-ARN-HERE
        result = None
        try:
            project_arn_id = project_arn.split(':')[6]
            test_run_arid = test_run_arn.split('/')[1]
            result = WEB_URL_TEMPLATE % (
                project_arn_id,
                test_run_arid,
            )
        except Exception as e:
            logger.print_on_console('Error while fetching run web URL')
            log.error(e)
        return result




    def get_device_pool(self,project_arn,pool_name):
        try:
            device_pool_arn = None
            d_list=self.dc.list_device_pools(arn=project_arn)['devicePools']
            for d in d_list:
                if d['name']==pool_name:
                    device_pool_arn=d['arn']
                    break
        except Exception as e:
            logger.print_on_console('Error while fetching device pool')
            log.error(e)
        return device_pool_arn




    def get_project(self,project_name):
        try:
            project_arn=None
            p_list=self.dc.list_projects()['projects']
            for p in p_list:
                if p['name']==project_name:
                    project_arn=p['arn']
                    break
            if project_arn==None:
                project_arn=self.create_project(project_name)
        except Exception as e:
            logger.print_on_console('Error while fetching project')
            log.error(e)
        return project_arn


    def get_app_arn(self,project_arn,upload_type,upload_file_name,*args):
        app_arn=None
        try:
            if not(self.terminateFlag):
                a_list=self.dc.list_uploads(arn=project_arn,type=upload_type)['uploads']
                for a in a_list:
                    if a['name']==upload_file_name and a['status']=='SUCCEEDED':
                        app_arn=a['arn']
                        log.info("Fetching "+str(upload_file_name))
                        logger.print_on_console("Fetching ",upload_file_name)
                        break
                if app_arn==None:
                    app_arn=self.create_upload(project_arn, upload_type, upload_file_name, args[0])
        except Exception as e:
            logger.print_on_console('Error while fetching app arn')
            log.error(e)
        return app_arn

    def get_test_run(self,project_arn,test_name):
        try:
            test_run_arn=None
            run_list=self.dc.list_runs(arn=project_arn)['runs']
            for n in run_list:
                if n['name']==test_name:
                    test_run_arn=n['arn']
        except Exception as e:
            logger.print_on_console('Error while fetching test run')
            log.error(e)
        return test_run_arn


    def schedule_run(self,project_arn, name, device_pool_arn, app_arn, test_package_arn,spec_arn):
        res = None
        try:
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
            res = run['arn']
        except Exception as e:
            logger.print_on_console('Error while Scheduling run')
            log.error(e)
        return res



    def wait_for_run(self,test_run_arn,timeout):
        result = False
        try:
            result = self._poll_until(
                self.dc.get_run,
                test_run_arn,
                get_status_callable=lambda x: x['run']['status'],
                success_statuses=('COMPLETED', ),
                check_every_seconds=60,
                timeout_seconds=timeout,
                
            )
            if result:
                final_run = result['run']
                logger.print_on_console('Final run counts: %(counters)s' % final_run)
                log.info('Final run counts: %(counters)s' % final_run)
                result = (final_run['result'] == 'PASSED')
                logger.print_on_console('Run completed')
                log.info('Run completed')
        except Exception as e:
            logger.print_on_console('Error while waiting for run')
            log.error(e)
        return result



    def run_test(self,project_arn,app_arn,tp_arn,spec_arn,device_pool_arn):
        run_status = False
        # time=str(datetime.now())
        try:
            name='Test_Run_'+self.cur_date

            self.test_run_arn = self.schedule_run(
                    project_arn,
                    name=name,
                    device_pool_arn=device_pool_arn,
                    app_arn=app_arn,
                    test_package_arn=tp_arn,
                    spec_arn=spec_arn
                )
            download_type='FILE'
            run_status=self.wait_for_run(self.test_run_arn,9000)
            
            if not(self.terminateFlag):
                self.download_results(self.test_run_arn,download_type,AWS_output_path)
        except Exception as e:
            logger.print_on_console('Error while performing run')
            log.error(e)
        return run_status

    def configure_run(self,project_name,app_name,package_name,pool_name):
        project_arn=app_arn=tp_arn=spec_arn=device_pool_arn=None
        try:
            if not(self.terminateFlag):
                #get the project Arn
                project_arn=self.get_project(project_name)
                log.debug ('project_arn',str(project_arn))

                #get device pool
                device_pool_arn=self.get_device_pool(project_arn,pool_name)
                log.debug ('device_pool_arn',str(device_pool_arn))

                if self.apk_path[-3:] == 'ipa':
                    app_arn=self.get_app_arn(project_arn,'IOS_APP',app_name,self.apk_path)
                else:
                    app_arn=self.get_app_arn(project_arn,'ANDROID_APP',app_name,self.apk_path)
                status=self.wait_for_upload(app_arn)
                log.debug ('app_arn',str(app_arn))

                #get test package name
                ##tp_arn=get_app_arn(project_arn,upload_type2,'TEST1.zip')
                tp_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_PACKAGE',package_name,self.file_path)
                status=self.wait_for_upload(tp_arn)
                log.debug ('tp_arn',str(tp_arn))

                #get test spec name
                if self.apk_path[-3:] == 'ipa':
                    # spec_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_SPEC','Default TestSpec for iOS Appium 1.9.1 Python (Support for iOS 12)')
                    spec_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_SPEC',self.ios_test_spec,AWS_assets+os.sep+self.ios_test_spec)
                else:
                    # spec_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_SPEC','Default TestSpec for Android Appium Python')
                    spec_arn=self.get_app_arn(project_arn,'APPIUM_PYTHON_TEST_SPEC',self.android_test_spec,AWS_assets+os.sep+self.android_test_spec)
                log.debug ('spec_arn',str(spec_arn))
                info_msg="All details fetched to Schedule Run"
                log.info(info_msg)
                logger.print_on_console(info_msg)
        except Exception as e:
            logger.print_on_console('Error while Configuring run')
            log.error(e)
        return project_arn,app_arn,tp_arn,spec_arn,device_pool_arn


    def run_aws_android_tests(self):
        result = False
        try:
            if not(self.terminateFlag):
                self.get_run_configurations()
                project_arn,app_arn,tp_arn,spec_arn,device_pool_arn=self.configure_run(self.project_name,self.app_name,self.package_name,self.pool_name)
                if(project_arn and app_arn and tp_arn and spec_arn and device_pool_arn) is not None:
                    result = self.run_test(project_arn,app_arn,tp_arn,spec_arn,device_pool_arn)
                else:
                    if not(self.terminateFlag):
                        msg='Error in Configuring AWS run'
                        log.error(msg)
                        logger.print_on_console(msg)
        except Exception as e:
            logger.print_on_console('Error in running aws tests')
            log.error(e)
        return result

    def download_results(self,test_run_arn,download_type,output_dir):
    ##    artifcats=self.dc.list_artifacts(arn='arn:aws:devicefarm:us-west-2:197128414257:run:02a594e3-ea23-48f8-a630-eac93487a7b1/25self.dc69bc-2907-4612-b890-92a66c0377d0',type='FILE')['artifacts']
        try:
            artifcats=self.dc.list_artifacts(arn=test_run_arn,type=download_type)['artifacts']
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            if len(artifcats) > 0:
                logger.print_on_console('Outputs are stored here '+output_dir)
                log.info('Outputs are stored here '+output_dir)
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
                
                msg="Download Successfull"
                logger.print_on_console(msg)
                log.info(msg)
            else:
                logger.print_on_console("No results to fetch")
                log.info("No results to fetch")
        except Exception as e:
            logger.print_on_console('Error while downloading results')
            log.error(e)

    def stop_job(self):
        self.terminateFlag=True
        logger.print_on_console("Termination initiated on current AWS run")
        try:
            if self.test_run_arn is not None:
                self.dc.stop_run(
                    arn=self.test_run_arn
                )
                logger.print_on_console("Stop initiated on current AWS run")
        except Exception as e:
            logger.print_on_console("Error while stopping run")
            log.error(e)



