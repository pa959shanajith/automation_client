from minio import Minio
import logging
from constants import *
import logger
import readconfig
import core
server_ip = readconfig.configvalues['server_ip']
log = logging.getLogger('screenshot_keywords.py')

import urllib3

class reportNFS():

    def __init__(self):
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
            server_ip, 
            access_key="avoassureadmin",
            secret_key="Welcome@dmin",
            # secure=False,
            secure=True,
            http_client=http_client
        )

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