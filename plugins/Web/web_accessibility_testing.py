# -------------------------------------------------------------------------------
# Name:        web_accessibility_testing
# Purpose:     Provides services to accessibility testing
#
# Author:      divyansh.singh
#
# Created:     07-01-2021
# Copyright:   (c) divyansh.singh 2021
# Licence:     <your licence>
# -------------------------------------------------------------------------------

from selenium.webdriver.firefox.options import Options
from axe_selenium_python import Axe
from selenium import webdriver
import platform
import readconfig
import os
import webconstants
import controller
import re
from urllib.parse import urljoin, urlparse
import requests
import tldextract
from bs4 import BeautifulSoup
import threading
import core
import json
import logger
import logging
import time
log = logging.getLogger(__name__)

# imports for Accessibility

SYSTEM_OS = platform.system()
AVO_ASSURE_HOME = os.environ["AVO_ASSURE_HOME"]
DRIVERS_PATH = AVO_ASSURE_HOME + "/Lib/Drivers"
GECKODRIVER_PATH = DRIVERS_PATH + "/geckodriver"
if SYSTEM_OS == "Windows":
    GECKODRIVER_PATH += ".exe"


class Web_Accessibility_Testing:

    def __init__(self):
        self.queue = []
        self.visited = set()
        self.edgedata = []  # list of forward nodes (links)
        self.reversedLinks = []  # list of backward nodes(reversedlinks)
        self.subdomains = []
        self.others = []
        self.domain = ""
        self.subdomain = ""
        self.discovered = set()
        self.rooturl = ""
        self.start_url = ""
        self.crawlStatus = True
        self.notParsedURLs = []
        self.socketIO = None
        self.totalSearchTextCount = 0
        self.accessTest = False
        self.searchData = None

    def parse(self, obj, lev, driver):

        agent = driver.capabilities['browserName']
        url = driver.current_url
        obj['url'] = url
        if controller.terminate_flag:
            return
        agents = {"safari": webconstants.SAFARI_AGENT,
                  "firefox": webconstants.FX_AGENT,
                  "chrome": webconstants.CHROME_AGENT,
                  "ie": webconstants.IE_AGENT
                  }
        try:
            headers = {'User-Agent': agents[agent]}
            # if URL is for file type .pdf, .docx or .zip (mentioned in webconstants.py),
            # we will send only header request, will not download entire content

            if not url.endswith(webconstants.IGNORE_FILE_EXTENSIONS):
                obj["noOfTries"] = obj["noOfTries"] + 1
                r = requests.get(url, headers=headers, verify=False,timeout=webconstants.REQUEST_URL_TIMEOUT)
                rurl = r.url

                # Check whether this URL redirects to some other URL
                if rurl == url:
                    obj["redirected"] = "no"
                else:
                    obj["redirected"] = rurl
                status = r.status_code
                obj["status"] = status
                soup = BeautifulSoup(r.text, "lxml")
                accessTags = []
                for rule in self.searchData:
                    if rule["selected"]:
                        accessTags.append(rule["tag"])
                accessOptions = {'runOnly': {
                    'type': "tag", 'values': accessTags}}
                axe = Axe(driver)
                # Inject axe-core javascript into page.
                axe.inject()
                results = axe.run(options=accessOptions)
                violationCount = dict()
                for violation in results["violations"]:
                    for tag in violation["tags"]:
                        if tag in violationCount:
                            violationCount[tag] += 1
                        else:
                            violationCount[tag] = 1
                # logger.print_on_console(violationCount)
                for rule in self.searchData:
                    if rule["tag"] in violationCount:
                        rule["pass"] = False
                        rule["count"] = violationCount[rule["tag"]]
                    else:
                        rule["pass"] = True
                        rule["count"] = 0
                obj["accessibility"] = results
                obj["access-rules"] = self.searchData

                if soup.title:
                    obj["title"] = soup.title.text
                else:
                    obj["title"] = "None"

                if (tldextract.extract(rurl).subdomain != self.subdomain) or (tldextract.extract(rurl).domain != self.domain):
                    if (self.domain in urlparse(rurl).netloc):
                        # it is a subdomain
                        self.subdomains.append(rurl)
                        obj['type'] = "subdomain"
                    else:
                        # it is some other URL
                        self.others.append(rurl)
                        obj['type'] = "subdomain"
                else:
                    obj['type'] = 'page'
                return obj
            else:
                headerResponse = requests.get(url, headers=headers, verify=False, stream=True)
                obj["status"] = headerResponse.status_code
                obj['type'] = "others"
                self.socketIO.emit('result_web_crawler', json.dumps(obj))
        except Exception as e:
            obj['error'] = str(e)
            obj['status'] = 400
            log.error(e)
            logger.print_on_console("Problem accessing url : ", url)
            logger.print_on_console("----------------------------")
            self.crawlStatus = False


    def runCrawler(self, driver, script_info, executionid):
        result = {} 
        result["status"] = "fail"
        rules_map = {"A":{'count': 10, 'name': 'A', 'pass': True, 'selected': False, 'tag': 'wcag2a'},"AA":{'count': 0, 'name': 'AA', 'pass': True, 'selected': False, 'tag': 'wcag2aa'},"508":{'count': 0, 'name': 'Section 508', 'pass': True, 'selected': False, 'tag': 'section508'},"Best Practice":{'count': 0, 'name': 'Best-Practice', 'pass': True, 'selected': False, 'tag': 'best-practice'}}
        for i in script_info["accessibility_parameters"]:
            rules_map[i]["selected"] = True
        self.searchData = list(rules_map.values())
        self.socketIO = core.socketIO
        log.debug("inside runCrawler method")
        mainobj = core.root
        agent = driver.capabilities['browserName']
        level = 0
        self.accessTest = True
        start = time.clock()
        msg = "Accessibility Testing started"
        log.info(msg)
        logger.print_on_console(msg)
        try:
            # Check if terminate flag is true or not:
            if controller.terminate_flag:
                controller.terminate_flag = False
            if controller.disconnect_flag:
                controller.disconnect_flag = False
            if mainobj.gui:
                mainobj.cw.terminatebutton.Enable()
            start_obj = {"name": "", "parent": "None", "level": 0, "noOfTries": 0}
            result = self.parse(start_obj, level, driver)
            result['agent'] = agent
            result["screenname"] = script_info['screenname']
            result["screenid"] = script_info['screenid']
            result['executionid'] = executionid
            result['cycleid'] = script_info['cycleid']
            self.crawlStatus = True
        except Exception as e:
            log.info("Something went wrong")
        # Stop everything in the case of disconnection from server
        if controller.disconnect_flag:
            return True
        time_taken = time.clock() - start
        crawling_status = "succesfully"
        if controller.terminate_flag:
            logger.print_on_console("---------Accessibility Testing Terminated---------")
            log.info("---------Accessibility Testing Terminated---------")
            crawling_status = "partially"
        seconds = 0
        minutes = 0
        time_str = ""
        # Compute time taken string
        if time_taken > 60:
            minutes = int(time_taken / 60)
            seconds = time_taken % 60
            if seconds != 0:
                time_str = str(minutes) + " mins, " + \
                    str("%.2f" % seconds) + " seconds"
            else:
                time_str = str(minutes) + " mins"
        else:
            time_str = str("%.2f" % time_taken) + " seconds"

        log.info("Accessibility Testing completed " + crawling_status + " in " + time_str)
        logger.print_on_console("Accessibility Testing completed " + crawling_status + " in " + time_str)
        return result