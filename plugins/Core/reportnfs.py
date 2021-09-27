from minio import Minio
import logging
from constants import *
import logger
log = logging.getLogger('screenshot_keywords.py')

class reportNFS():

    def __init__(self):
        self.client = Minio(
            '127.0.0.1:9000', 
            access_key="avoassureadmin",
            secret_key="Welcome@dmin",
            secure=False
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