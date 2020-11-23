import pyautogui 
import cv2 
import numpy as np
import threading
from datetime import datetime
import logging
import logger


log = logging.getLogger("controller.py")


class Recorder():

    def __init__(self):
        self.rec_status = False

    # Recording screen while execution(Currently for Web Apptype)
    def record_execution(self):
        try:
            ##start screen recording
            import constants
            if constants.SCREENSHOT_PATH  not in ['screenshot_path', 'Disabled']:
                filename = constants.SCREENSHOT_PATH+"ScreenRecording_"+datetime.now().strftime("%Y%m%d%H%M%S")+".mp4"
            else:
                filename = "output/ScreenRecording_"+datetime.now().strftime("%Y%m%d%H%M%S")+".mp4"
                logger.print_on_console("Screen capturing disabled since user does not have sufficient privileges for screenshot folder. Video saved in 'Avoassure/output' folder\n")
                log.info("Screen capturing disabled since user does not have sufficient privileges for screenshot folder. Video saved in 'Avoassure/output' folder\n")
            resolution = tuple(pyautogui.size())
            codec = cv2.VideoWriter_fourcc(*"MP4V")
            log.info("Screen Recorded here:")
            log.info(filename)
            fps = 10.0
            out = None
            out = cv2.VideoWriter(filename, codec, fps, resolution)
            self.rec_status = True
            rec_th = threading.Thread(target = self.start_recording, name="start_recording", args = (out,))
            rec_th.start()
            
        except Exception as e:
            logger.print_on_console('Error in screen recording')
            log.error(e,exc_info = True)
        return filename

    def start_recording(self,*args):
        try:
            out = args[0]
            while self.rec_status:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
            out.release()
            log.info("Video saved!!!")
        except Exception as e:
            log.error(e,exc_info = True)
