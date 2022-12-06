import requests
import logging
import time
import logger
from datetime import datetime,timedelta
log = logging.getLogger('retryapis_cicd.py')

class Retryrequests:

    """
    This class is supposed to retry requests.

    """
    def __init__(self) -> None:
        pass
    def retry_cicd_apis(self,server_url,data_dict):
        loop_timelimit = datetime.now() + timedelta(minutes=30)
        retry_flag = 1
        while retry_flag:
            current_time = datetime.now()
            try:
                if current_time >= loop_timelimit:
                    retry_flag = 0 
                    log.info("Maximum retries and Time limit exceeded")
                res = requests.post(server_url, json = data_dict, verify = False, timeout=160)
                if res.status_code != 200:
                    log.error("Unable to connect to server retrying after 10 seconds. Status code is: %s",
                        res.status_code)
                    time.sleep(10)
                else:
                    retry_flag = 0
            except Exception as e:
                res = None
                log.error(e)
                time.sleep(30)
        return res