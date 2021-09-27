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
import os
import webconstants
import controller
import re
from urllib.parse import urljoin, urlparse
import requests
import tldextract
from bs4 import BeautifulSoup
import core
import logger
import logging
import time
import readconfig
import screenshot_keywords
from webscrape_utils import WebScrape_Utils
import constants
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
        self.subdomains = []
        self.others = []
        self.domain = ""
        self.subdomain = ""
        self.crawlStatus = True
        self.searchData = None
        self.webscrape_utils_obj = WebScrape_Utils()

    def parse(self, obj, driver):
        """
        Parse crawled document and inject axe script to run accessibility testing

        :param obj: final report object
        :param script_info: details about the screen which is being tested
        :param driver: reference of webdriver object
        """
        agent = driver.capabilities['browserName']
        url = driver.current_url
        obj['url'] = url
        if controller.terminate_flag:
            return
        agents = {"safari": webconstants.SAFARI_AGENT,
                  "firefox": webconstants.FX_AGENT,
                  "chrome": webconstants.CHROME_AGENT,
                  "internet explorer": webconstants.IE_AGENT,
                  "default": webconstants.EDGE_AGENT
                  }
        try:
            if agent in agents:
                headers = {'User-Agent': agents[agent]}
            else:
                headers = {'User-Agent': agents["default"]}
            # if URL is for file type .pdf, .docx or .zip (mentioned in webconstants.py),
            # we will send only header request, will not download entire content

            if not url.endswith(webconstants.IGNORE_FILE_EXTENSIONS):
                obj["noOfTries"] = obj["noOfTries"] + 1
                r = requests.get(url, headers=headers, verify=False,timeout=webconstants.REQUEST_URL_TIMEOUT,proxies=readconfig.proxies)
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
                accessOptions = {'runOnly': {'type': "tag", 'values': accessTags}, 'elementRef':"true"}
                axe = Axe(driver)
                # Inject axe-core javascript into page.
                axe.inject()
                results = self.run(options=accessOptions, browsertype = agent, driver = driver)
                #results = axe.run(options=accessOptions, browsertype = agent)
                violationCount = dict()
                report_obj = {"violations":[],"passes":[]}
                for violation in results["violations"]:
                    for tag in violation["tags"]:
                        if tag in violationCount:
                            violationCount[tag] += 1
                        else:
                            violationCount[tag] = 1
                for status in report_obj:
                    for element in results[status]:
                        rep = {}
                        rep["description"] = element['description']
                        rep['help'] = element['help']
                        rep['impact'] = element['impact']
                        rep['tags'] = element['tags']
                        rep['elements'] = []
                        for nodes in element['nodes']:
                            element_details = {}
                            element_details['html'] = nodes['html']
                            element_details['rect'] = nodes['element'].rect
                            if 'failureSummary' in nodes:
                                element_details['solution'] = nodes['failureSummary']
                            else:
                                element_details['solution'] = "N/A"
                            rep['elements'].append(element_details)
                        report_obj[status].append(rep)

                # logger.print_on_console(violationCount)
                for rule in self.searchData:
                    if rule["tag"] in violationCount:
                        rule["pass"] = False
                        rule["count"] = violationCount[rule["tag"]]
                    else:
                        rule["pass"] = True
                        rule["count"] = 0
                obj["accessibility"] = report_obj
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
                obj['error'] = "Invalid URL"
                logger.print_on_console("Invalid URL : ", url)
                return obj
        except Exception as e:
            obj['error'] = str(e)
            log.error(e)
            logger.print_on_console("Error occurred in accessing url : ", url)
            logger.print_on_console("----------------------------")
            self.crawlStatus = False
            return obj


    def run(self, context=None, options=None, browsertype = None, driver = None):
        """
        Run axe against the current page.

        :param context: which page part(s) to analyze and/or what to exclude.
        :param options: dictionary of aXe options.
        """
        template = (
            "var callback = arguments[arguments.length - 1];"
            + "axe.run(%s).then(function(results) { callback(results)})"
        )
        args = ""

        if browsertype is not None and browsertype == "internet explorer":
            ie_script = 'var head = document.getElementsByTagName("head")[0];var script = document.createElement("script");script.src = "https://cdnjs.cloudflare.com/ajax/libs/bluebird/3.3.4/bluebird.min.js";head.appendChild(script);'
            driver.execute_script(ie_script)
        # If context parameter is passed, add to args
        if context is not None:
            args += "%r" % context
        # Add comma delimiter only if both parameters are passed
        if context is not None and options is not None:
            args += ","
        # If options parameter is passed, add to args
        if options is not None:
            args += "%s" % options

        command = template % args
        response = driver.execute_async_script(command)
        return response



    def runCrawler(self, driver, script_info, executionid, index):
        """
        Crawl through the html document at level 0 and test each element in the document.

        :param driver: reference of the webdriver which contains the website to be tested
        :param script_info: details about the screen which is being tested
        :param executionid: unique id of this execution for reference
        """
        result = {} 
        result["status"] = "fail"
        #Add new standards here
        rules_map = {"aria":{'count': 10, 'name': 'Aria', 'pass': True, 'selected': False, 'tag': 'cat.aria'},"AAA":{'count': 10, 'name': 'AAA', 'pass': True, 'selected': False, 'tag': 'wcag2aaa'},"A":{'count': 10, 'name': 'A', 'pass': True, 'selected': False, 'tag': 'wcag2a'},"AA":{'count': 0, 'name': 'AA', 'pass': True, 'selected': False, 'tag': 'wcag2aa'},"508":{'count': 0, 'name': 'Section 508', 'pass': True, 'selected': False, 'tag': 'section508'},"Best Practice":{'count': 0, 'name': 'Best-Practice', 'pass': True, 'selected': False, 'tag': 'best-practice'}}
        #Enable standards to be tested
        for i in script_info["accessibility_parameters"]:
            rules_map[i]["selected"] = True
        self.searchData = list(rules_map.values())
        log.debug("inside runCrawler method")
        mainobj = core.root
        agent = driver.capabilities['browserName']
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
            result = self.parse(start_obj, driver)
            if "error" in result:
                result['status'] = "fail"
                return result
            if agent == 'msedge': agent = "edge chromium"
            elif 'edge' in agent.lower(): agent = "edge legacy"
            result['agent'] = agent
            result['status'] = "success"
            result["screenname"] = script_info['screenname']
            result["screenid"] = script_info['screenid']
            result['executionid'] = executionid
            result['cycleid'] = script_info['cycleid']
            self.crawlStatus = True
        except Exception as e:
            logger.print_on_console('Error in running accessibility testing')
            result['status'] = "fail"
            log.error(e,exc_info=True)
        # Stop everything in the case of disconnection from server
        ######################################## acessbility #########################################
        if controller.disconnect_flag:
            return True
        try:
            logger.print_on_console('Capturing Screenshot for Accessibility Testing')
            temppath = os.getcwd() + os.sep + "output" + os.sep + executionid + os.sep + str(index) +".png"
            screenshot, width, height = self.webscrape_utils_obj.fullpage_screenshot(driver, temppath)
            screen_shot_obj = screenshot_keywords.Screenshot()
            script_info['executionid'] = executionid
            script_info['temppath'] = temppath
            output = screen_shot_obj.captureScreenshot(script_info,accessibility=True)
            result['screenshotpath'] = output[2]
            result['width'] = width
            result['height'] = height
        except Exception as e:
            logger.print_on_console('Error in taking screenshot')
            log.error(e,exc_info=True)

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