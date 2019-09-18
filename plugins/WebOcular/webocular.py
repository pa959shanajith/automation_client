#-------------------------------------------------------------------------------
# Name:        webocular.py
# Purpose:      Provides services to the webocular plugin
#
# Author:      nikunj.jain
#
# Created:     08-08-2017
# Copyright:   (c) nikunj.jain 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
from urllib.parse import urljoin, urlparse
import requests
import tldextract
from bs4 import BeautifulSoup
import threading
import json
import logger
import logging
import time
from urllib.parse import quote_plus as encodeURL
from encryption_utility import AESCipher
log = logging.getLogger(__name__)
import controller
import webocular_constants
import os
import platform

# imports for Accessibility
from selenium import webdriver
from axe_selenium_python import Axe
from selenium.webdriver.firefox.options import Options

SYSTEM_OS=platform.system()
NINETEEN68_HOME = os.environ["NINETEEN68_HOME"]
DRIVERS_PATH = NINETEEN68_HOME + "/Lib/Drivers"
GECKODRIVER_PATH = DRIVERS_PATH + "/geckodriver"
if SYSTEM_OS == "Windows":
    GECKODRIVER_PATH += ".exe"

class Webocular():

    def __init__(self):
        self.queue = []
        self.visited = set()
        self.nodedata = {}           #Dictionary of nodes, key is url
        self.edgedata = []           #list of forward nodes (links)
        self.reversedLinks = []         #list of backward nodes(reversedlinks)
        self.subdomains = []
        self.others = []
        self.domain = ""
        self.subdomain = ""
        self.discovered = set()
        self.rooturl=""
        self.start_url=""
        self.crawlStatus = True
        self.notParsedURLs = []
        self.socketIO=None
        self.proxy=None
        self.searchText=None
        self.totalSearchTextCount=0
        self.searchImage=None
        self.accessTest=False
        self.searchData=None
        #self.driver = webdriver.PhantomJS(executable_path="some\\path")

    def get_complete_url(self,url, new_url) :
        try:
            new_url = urljoin(url, new_url)
        except Exception as e:
            return None
        if '#' in new_url :
            pos = new_url.index('#')
            new_url = new_url[:pos]
        elif 'javascript:' in new_url or "mailto:" in new_url or "tel:" in new_url:
            new_url = None
        return new_url

    def get_buttonlinks(self,soup) :
        buttons = soup.find_all('button')
        urlexp = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(urlexp, str(buttons))
        return urls

    def get_imagelinks(self,soup) :
        imglinks = []
        images = soup.find_all('img')
        for image in images:
            if image.get('href') != None :
                imglinks.append(image.get('href'))
        return imglinks

    def crawl(self,start_url, level,agent) :
        self.domain = tldextract.extract(str(start_url)).domain
        #create a start object to initiate the process
        start_obj = {"name" : start_url, "parent" : "None", "level" : 0,"noOfTries" : 0 }
        self.discovered.add(start_url)
        self.queue.append(start_obj)

        i=1
        threads = []
        logger.print_on_console("Request in progress...")
        self.subdomain = tldextract.extract(start_url).subdomain
        while(self.queue and not controller.terminate_flag) :
            obj = self.queue.pop(0)
            url = obj['name']
            t = threading.Thread(target = self.parse, args = (url, obj, level,agent,webocular_constants.REQUEST_URL_TIMEOUT))
            t.start()
            threads.append(t)
            if i == 1 :
                time.sleep(6)
                i += 1
            time.sleep(1)
        for thread in threads :
            thread.join()

    def parse(self,url, obj, lev,agent,timeout):

        if controller.terminate_flag:
            return

        agents = {  "safari" : webocular_constants.SAFARI_AGENT,
                    "firefox" : webocular_constants.FX_AGENT,
                    "chrome" : webocular_constants.CHROME_AGENT,
                    "ie": webocular_constants.IE_AGENT
                }
        try:
            headers = {'User-Agent': agents[agent]}
            #if URL is for file type .pdf, .docx or .zip (mentioned in webocular_constants.py),
            # we will send only header request, will not download entire content

            if not url.endswith(webocular_constants.IGNORE_FILE_EXTENSIONS):
                obj["noOfTries"] = obj["noOfTries"] + 1
                r = requests.get(url, headers = headers,verify = False,timeout = timeout, proxies=self.proxy)
                rurl = r.url

                #Check whether this URL redirects to some other URL
                if rurl == url:
                    obj["redirected"] = "no"
                else:
                    obj["redirected"] = rurl
                status = r.status_code
                obj["status"] = status
                soup = BeautifulSoup(r.text, "lxml")
                if self.searchText=="NA":
                    obj["searchTextCount"]="NA"
                else:
                    pageHTML = BeautifulSoup(r.content)
                    pageText = pageHTML.getText() # get_text() can also be used
                    searchList=re.findall(self.searchText,pageText)
                    obj["searchTextCount"]=str(len(searchList))
                    self.totalSearchTextCount+=int(obj["searchTextCount"])

                if self.accessTest==True:
                    options = Options()
                    options.headless = True
                    driver = webdriver.Firefox(options=options,executable_path=GECKODRIVER_PATH)
                    driver.get(url)
                    axe = Axe(driver)
                    # Inject axe-core javascript into page.
                    axe.inject()
                    results = axe.run()
                    violationCount=dict()
                    for violation in results["violations"]:
                        for tag in violation["tags"]:
                            if tag in violationCount:
                                violationCount[tag]+=1
                            else:
                                violationCount[tag]=1
                    # logger.print_on_console(violationCount)
                    for rule in self.searchData["access-rules"]:
                            if rule["tag"] in violationCount:
                                rule["pass"]=False
                                rule["count"]=violationCount[rule["tag"]]
                            else:
                                rule["pass"]=True
                                rule["count"]=0
                    # axe.write_results(results, 'WebOcular.json')
                    try:
                        driver.close()
                        driver.quit()
                    except:
                        pass
                    obj["accessibility"]=results
                    obj["access-rules"]=self.searchData["access-rules"]
                else:
                    obj["accessibility"]="NA"
                    obj["access-rules"]="NA"

                if soup.title :
                    obj["title"] = soup.title.text
                else :
                    obj["title"] = "None"

                if (tldextract.extract(rurl).subdomain != self.subdomain) or (tldextract.extract(rurl).domain != self.domain) :
                    if (self.domain in urlparse(rurl).netloc) :
                        #it is a subdomain
                         self.subdomains.append(rurl)
                         obj['type'] = "subdomain"
                    else :
                        #it is some other URL
                        self.others.append(rurl)
                        obj['type'] = "subdomain"
                else:
                    obj['type'] = 'page'

                self.nodedata[url] = obj
                self.socketIO.emit('result_web_crawler',json.dumps(obj))
                if obj['level'] < lev :
                    if (tldextract.extract(rurl).domain == self.domain) and (tldextract.extract(rurl).subdomain == self.subdomain):
                        if rurl not in self.visited:
                            self.visited.add(rurl)
                            links = soup.find_all('a')
                            frames = soup.find_all('frame')
                            iframes = soup.find_all('iframe')
                            buttons = self.get_buttonlinks(soup)
                            images = self.get_imagelinks(soup)
                            pagelinks = set()
                            pagelinks.add(rurl)
                            for link in links:
                                new_url = link.get('href')
                                url_text = link.text
                                url_text = url_text.strip()
                                new_url = self.get_complete_url(rurl, new_url)

                                if new_url != None :
                                    if new_url not in self.discovered:
                                        #if new_url not in self.visited:
                                            pagelinks.add(new_url)
                                            self.discovered.add(new_url)
                                            self.queue.append({"name" : new_url, "parent" : rurl, "desc" : url_text, "level" : obj['level']+1,"noOfTries" : 0  })
                                            self.edgedata.append({"source" : rurl, "target" : new_url })
                                            #let's sleep for sometime
                                            time.sleep(0.1)
                                    else :
                                        if new_url not in pagelinks :
                                            self.reversedLinks.append({"name" : new_url, "parent" :rurl, "level" : obj['level']+1 })
##                                             reversedObj = {"type" : "reverse" }
##                                             data = json.dumps(reversedObj)
##                                             self.socketIO.emit('result_web_crawler',data)
                            for frame in frames:
                                new_url = frame.attrs['src']
                                try:
                                    if frame.attrs['name'] is not None:
                                        url_text = frame.attrs['name']
                                        url_text = url_text.strip()
                                    else:
                                        url_text = None
                                except Exception as nameNotPresentInFrame:
                                    url_text = None

                                new_url = self.get_complete_url(rurl, new_url)
                                if new_url != None:
                                    if new_url not in self.discovered:
                                        # if new_url not in self.visited:
                                        pagelinks.add(new_url)
                                        self.discovered.add(new_url)
                                        self.queue.append({"name": new_url, "parent": rurl, "desc": url_text,
                                                           "level": obj['level'] + 1,"noOfTries" : 0 })
                                        self.edgedata.append({"source": rurl, "target": new_url})
                                        #let's sleep for sometime
                                        time.sleep(0.1)
                                    else:
                                        if new_url not in pagelinks:
                                            self.reversedLinks.append(
                                                {"name": new_url, "parent": rurl, "level": obj['level'] + 1})
                            for iframe in iframes:
                                new_url = iframe.attrs['src']
                                try:
                                    if iframe.attrs['name'] is not None:
                                        url_text = iframe.attrs['name']
                                        url_text = url_text.strip()
                                    else:
                                        url_text = None
                                except Exception as nameNotPresentIniFrame:
                                    url_text = None
                                new_url = self.get_complete_url(rurl, new_url)

                                if new_url != None:
                                    if new_url not in self.discovered:
                                        # if new_url not in self.visited:
                                        pagelinks.add(new_url)
                                        self.discovered.add(new_url)
                                        self.queue.append({"name": new_url, "parent": rurl, "desc": url_text,
                                                           "level": obj['level'] + 1,"noOfTries" : 0 })
                                        leveln = obj['level'] + 1
                                        self.edgedata.append({"source": rurl, "target": new_url})
                                        #let's sleep for sometime
                                        time.sleep(0.1)
                                    else:
                                        if new_url not in pagelinks:
                                            self.reversedLinks.append(
                                                {"name": new_url, "parent": rurl, "level": obj['level'] + 1})
            else:
                headerResponse = requests.get(url, headers = headers, verify = False, stream = True, proxies=self.proxy)
                obj["status"] = headerResponse.status_code
                obj['type'] = "others"
                self.nodedata[url] = obj
                self.socketIO.emit('result_web_crawler',json.dumps(obj))
        except requests.exceptions.HTTPError as e:
            if obj["noOfTries"] < 2:
                logger.print_on_console("HTTPError : retrying for url : ",url)
                logger.print_on_console("----------------------------")
                log.info("retrying for url : ")
                log.info(url)
                self.parse(url, obj, lev,agent,webocular_constants.REQUEST_URL_TIMEOUT/2)
            else:
                logger.print_on_console("Max retries exceeded for url : ",url)
                logger.print_on_console("----------------------------")
                obj['error'] = str(e)
                obj['status'] = 400
                self.nodedata[url] = obj
                log.info("Max retries exceeded for url : ")
                log.info(url)
        except requests.exceptions.ConnectTimeout as e:
            if obj["noOfTries"] < 2:
                logger.print_on_console("ConnectTimeout : retrying for url : ",url)
                logger.print_on_console("----------------------------")
                log.info("retrying for url : ")
                log.info(url)
                self.parse(url, obj, lev,agent,webocular_constants.REQUEST_URL_TIMEOUT/2)
            else:
                logger.print_on_console("Max retries exceeded for url : ",url)
                logger.print_on_console("----------------------------")
                obj['error'] = str(e)
                obj['status'] = 400
                self.nodedata[url] = obj
                log.info("Max retries exceeded for url : ")
                log.info(url)
        except requests.exceptions.ReadTimeout as e:
            if obj["noOfTries"] < 2:
                logger.print_on_console("ReadTimeout : retrying for url : ",url)
                logger.print_on_console("----------------------------")
                log.info("retrying for url : ")
                log.info(url)
                self.parse(url, obj, lev,agent,webocular_constants.REQUEST_URL_TIMEOUT/2)
            else:
                logger.print_on_console("Max retries exceeded for url : ",url)
                logger.print_on_console("----------------------------")
                obj['error'] = str(e)
                obj['status'] = 400
                self.nodedata[url] = obj
                log.info("Max retries exceeded for url : ")
                log.info(url)
        except Exception as e:
            obj['error'] = str(e)
            obj['status'] = 400
            self.nodedata[url] = obj
            log.error(e)
            logger.print_on_console("Problem accessing url : ",url)
            logger.print_on_console("----------------------------")
            #import traceback
            #traceback.format_exc()
            self.crawlStatus = False

    def runCrawler(self,socketIO,mainwxobj,url,level,agent,proxy,searchData):
        self.socketIO=socketIO
        log.debug("inside runCrawler method")
        level  = int(level)
        start_url = url
        self.rooturl = start_url
        start = time.clock()
        self.searchData=searchData
        if searchData["accessTest"]==True:
            self.accessTest=True
        else:
            self.accessTest=False
        msg = "New Webocular request has started with following parameters: [URL] : " + start_url  +  " [LEVEL] : "  +  str(level) + " [Agent] : " + str(agent)
        if len(searchData["text"])>0:
            msg += " [SEARCH TEXT] : "+ str(searchData["text"])
            self.searchText=searchData["text"]
        else:
            self.searchText="NA"
            self.totalSearchTextCount=0
        if searchData["image"]!="":
            self.searchImage=searchData["image"]
            msg += " [SEARCH IMAGE] : YES"
        else:
            self.searchImage="NA"
        if self.accessTest==True:
            msg+= "[Accessibility]: True "
        else:
            msg+= "[Accessibility]: False "
        if proxy["enable"]:
            msg += "*(Proxy Enabled)"
            proxy_url = proxy["url"]
            if proxy["username"] and proxy["password"]:
                encryption_obj = AESCipher()
                proxy["password"] = encryption_obj.decrypt(proxy["password"])
                if proxy["password"] is None:
                    raise ValueError("Invalid password")
                proxy_url = encodeURL(proxy["username"])+":"+encodeURL(proxy["password"])+"@"+proxy_url
            self.proxy = {}
            #protocols = ["http", "https", "ftp"]
            protocols = ["http", "https"]
            for protocol in protocols:
                self.proxy[protocol] = protocol+"://"+proxy_url
        log.info(msg)
        logger.print_on_console(msg)
        try:
            #Check if terminate flag is true or not:
            if controller.terminate_flag:
                controller.terminate_flag = False
            if controller.disconnect_flag:
                controller.disconnect_flag=False
            mainwxobj.terminatebutton.Enable()
            t = threading.Thread(target = self.crawl, args = (start_url, level,agent))
            t.start()
            t.join()
            self.crawlStatus = True
        except Exception as e:
            log.info("Something went wrong")

        # Stop everything in the case of disconnection from server
        if controller.disconnect_flag:
            return True

        #process all reverse links
        for reversedLink in self.reversedLinks:
            if reversedLink['name'] in self.nodedata:
                reversedLink['status'] = self.nodedata[reversedLink['name']]['status']
                reversedLink['type'] = "duplicate"
               #TODO:
               #send desc also
                #reversedLink['level'] = self.nodedata[reversedLink['name']]['level']
            else:
                self.reversedLinks.remove(reversedLink)
        sdata = { "nodes" : self.nodedata, "links" : self.reversedLinks }
        time_taken = time.clock() - start

        crawling_status = "succesfully"
        if controller.terminate_flag:
            logger.print_on_console("---------Webocular request Terminated---------")
            log.info("---------Webocular request Terminated---------")
            crawling_status = "partially"

        seconds = 0
        minutes = 0
        time_str = ""

        #Compute time taken string
        if time_taken > 60:
            minutes =  int(time_taken / 60)
            seconds = time_taken % 60
            if seconds != 0:
                time_str = str(minutes) + " mins, " + str("%.2f" % seconds) + " seconds"
            else:
                time_str = str(minutes) + " mins"
        else:
            time_str = str("%.2f" % time_taken) + " seconds"

        log.info("Webocular request completed " + crawling_status +" in " +  time_str)

        #send the completion object to Node
        completetionObj = json.dumps({"progress" : "complete" ,"sdata" : sdata, "status": "success" ,"subdomains":  self.subdomains, "others" : self.others, "notParsedURLs" : self.notParsedURLs, "time_taken" : str(time_taken) +  " seconds","totalSearchTextCount":str(self.totalSearchTextCount),"searchText":str(self.searchText),"accessibility_stats":self.searchData["access-rules"]})
        self.socketIO.emit('result_web_crawler_finished',completetionObj)
        logger.print_on_console("Webocular request completed " + crawling_status +" in " +  time_str)

        #finally reset the controller's terminate flag to False and Disable the terminate button
        controller.terminate_flag = False
        mainwxobj.terminatebutton.Disable()
