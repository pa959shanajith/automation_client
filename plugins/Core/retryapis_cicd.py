import requests
import logging
import time
import logger
from datetime import datetime,timedelta
import controller
import readconfig
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
        if readconfig.proxies:
            verify_flag = True
        else:
            verify_flag = False
        while retry_flag:
            current_time = datetime.now()
            try:
                if current_time >= loop_timelimit or controller.terminate_flag:
                    controller.terminate_flag = True
                    log.info("Maximum retries and Time limit exceeded")
                    log.info("Something went wrong. Sorry, we're unable to reach the server right now")
                    res = None
                    break
                res = requests.post(server_url, json = data_dict, verify = verify_flag,  proxies = readconfig.proxies, timeout = 120)
                if res.status_code != 200:
                    log.info("Unable to connect to server retrying after 10 seconds. Status code is: %s",
                        res.status_code)
                    logger.print_on_console("Connection error occurred with:"+ server_url)
                    time.sleep(10)
                else:
                    retry_flag = 0
            except Exception as e:
                res = None
                log.error(e)
                logger.print_on_console("Unable to connect to server retrying after 30 seconds.")
                time.sleep(30)
        return res