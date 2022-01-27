from minio import Minio
import logging
from constants import *
import logger
import readconfig
import core
import urllib3
import core_utils
from datetime import timedelta
log = logging.getLogger('screenshot_keywords.py')
client = None
cutils = core_utils.CoreUtils()

class reportNFS():

    def __init__(self):
        global client
        k = "".join(['N','i','n','E','t','e','E','n','6','8','d','A','t','a','B','A','s','3','e','N','c','R','y','p','T','1','0','n','k','3','y','S'])
        username = cutils.unwrap('78e14edcbd37e5e43b1fc2a535f41637', k)
        password= cutils.unwrap('da4e266febec8e0b395cebc604966a87', k)
        kw = core.ConnectionThread(None).get_ice_session(no_params=True)
        cert = kw.get('cert', [None,None])
        ca_certs = kw.get('verify', None)
        cert_reqs = None if ca_certs == False else 'CERT_REQUIRED'
        http_client = urllib3.PoolManager(
                        cert_reqs=cert_reqs,
                        headers=kw.get('headers', {}),
                        ca_certs=ca_certs,
                        assert_hostname=kw.get('assert_hostname', True),
                        key_file=cert[1],cert_file=cert[0],
                        _proxy=kw.get('proxy', {'https':None})['https'],
                        retries=urllib3.Retry(
                            total=5,
                            backoff_factor=0.2,
                            status_forcelist=[500, 502, 503, 504]
                        )
                )
        self.client = Minio(
            readconfig.configvalues['server_ip']+":"+readconfig.configvalues['server_port'],
            access_key=username,
            secret_key=password,
            secure=True,
            http_client=http_client
        )
        client = self

    def saveimage(self,*args):
        try:
            result = self.client.fput_object(*args,content_type="image/png")
            return result
        except Exception as exc:
            log.error(exc)
            err_msg = ERROR_CODE_DICT['ERR_SAVE_IMG']
            logger.print_on_console(err_msg)
            return "fail"
            
    def savelogs(self,*args):
        try:
            result = self.client.fput_object(*args,content_type="text/plain")
            return result
        except Exception as exc:
            log.error(exc)
            err_msg = ERROR_CODE_DICT['ERR_SAVE_LOGS']
            logger.print_on_console(err_msg)
            return "fail"

    def getobjectlink(self,*args):
        try:
            result = self.client.presigned_get_object(*args,expires=timedelta(days=1))
            return result
        except Exception as exc:
            log.error(exc)
            err_msg = ERROR_CODE_DICT['ERR_GET_OBJ']
            logger.print_on_console(err_msg)
            return "fail"