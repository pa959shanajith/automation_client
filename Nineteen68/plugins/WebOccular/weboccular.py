#-------------------------------------------------------------------------------
# Name:        weboccular.py
# Purpose:      Provides serivces to the weboccular plugin
#
# Author:      nikunj.jain
#
# Created:     08-08-2017
# Copyright:   (c) nikunj.jain 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
from urlparse import urljoin, urlparse
import requests
import tldextract
from bs4 import BeautifulSoup
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import json
import html5lib
import logger
import logging.config
import logging
import time
log = logging.getLogger(__name__)
import controller
import weboccular_constants
class Weboccular():

    def __init__(self):
        self.queue = []
        self.visited = set()
        self.nodedata = []           #list of nodes
        self.edgedata = []           #list of forward nodes (links)
        self.extraLinks = []         #list of backward nodes(sublinks)
        self.subdomains = []
        self.others = []
        self.domain = ""
        self.subdomain = ""
        self.discovered = set()
        self.rooturl=""
        self.start_url=""
        self.crawlStatus = True
        self.notParsedURLs = []

    def get_complete_url(self,url, new_url) :
        try:
            new_url = urljoin(url, new_url)
        except Exception as e:

            return None
        if '#' in new_url :
            pos = new_url.index('#')
            new_url = new_url[:pos]
        elif 'javascript' in new_url :
            new_url = None
        elif "mailto" in new_url :
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


    def crawl(self,start_url, level,agent,socketIO) :
        self.domain = tldextract.extract(str(start_url)).domain
        start_obj = {"name" : start_url, "parent" : "None", "level" : 0 }
        self.discovered.add(start_url)
        self.queue.append(start_obj)
        i=1
        threads = []
        logger.print_on_console("crawling in progress...")
        self.subdomain = tldextract.extract(start_url).subdomain
        while(self.queue and not controller.terminate_flag) :
            obj = self.queue.pop(0)
            url = obj['name']
            t = threading.Thread(target = self.parse, args = (url, obj, level,agent,socketIO))
            t.start()
            threads.append(t)
            if i == 1 :
                time.sleep(6)
                i += 1
            time.sleep(1)

        for thread in threads :
            thread.join()

    def parse(self,url, obj, lev,agent,socketIO) :

        if controller.terminate_flag:
            return

        agents = {  "safari" : weboccular_constants.SAFARI_AGENT,
                    "firefox" : weboccular_constants.FX_AGENT,
                    "chrome" : weboccular_constants.CHROME_AGENT,
                    "ie": weboccular_constants.IE_AGENT
                }
        try:
            headers = {'User-Agent': agents[agent]}
            #if URL is for file type .pdf, .docx or .zip we will send only header request, will not download entire content

            #print "processing URL : ", url
            if not url.endswith('.pdf') and not url.endswith('.docx') and not url.endswith('.zip'):
                r = requests.get(url, headers = headers,verify = False)
                rurl = r.url
                if rurl == url :
                    obj["redirected"] = "no"
                else :
                    obj["redirected"] = rurl
                status = r.status_code
                obj["status"] = status
                response = r.text
                soup = BeautifulSoup(response, "html5lib")
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
                self.nodedata.append(obj)
                data = json.dumps(obj)
                socketIO.emit('result_web_crawler',data)
                if obj['level'] < lev :
                    if (tldextract.extract(rurl).domain == self.domain) and (tldextract.extract(rurl).subdomain == self.subdomain):
                        if rurl not in self.visited:
                            self.visited.add(rurl)
                            links = soup.find_all('a')
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
        #                            if new_url not in self.visited:
                                            pagelinks.add(new_url)
                                            self.discovered.add(new_url)
                                            self.queue.append({"name" : new_url, "parent" : rurl, "desc" : url_text, "level" : obj['level']+1  })
                                            leveln = obj['level']+1
                                            self.edgedata.append({"source" : rurl, "target" : new_url })
                                    else :
                                        if new_url not in pagelinks :
                                             self.extraLinks.append({"source" : new_url, "target" :rurl })
##                                             reversedObj = {"type" : "reverse" }
##                                             data = json.dumps(reversedObj)
##                                             socketIO.emit('result_web_crawler',data)

            else:
                headerResponse = requests.get(url,headers = headers,verify = False,stream = True)
                obj["status"] = headerResponse.status_code
                obj['type'] = "others"
                self.nodedata.append(obj)
                data = json.dumps(obj)
                socketIO.emit('result_web_crawler',data)

        except Exception as e:
            obj['error'] = str(e)
            self.nodedata.append(obj)
            #print e
            #print "error url" , url
            self.crawlStatus = False

    def runCrawler(self,url,level,agent,socketIO) :
        log.debug("inside runCrawler method")
        level  = int(level)
        start_url = url
        self.rooturl = start_url
        start = time.clock()
        log.info("starting new crawling request with following parameteres: [URL] : " + start_url  +  " [LEVEL] : "  +  str(level) + " [Agent] : " + str(agent))
        logger.print_on_console("--------------------")
        logger.print_on_console("starting new crawling request with following parameteres: [URL] : " + start_url  +  " [LEVEL] : "  +  str(level) + " [Agent] : " + str(agent))
        logger.print_on_console("--------------------")
        try:
            t = threading.Thread(target = self.crawl, args = (start_url, level,agent,socketIO))
            t.start()
            t.join()
            self.crawlStatus = True
        except Exception as e:
            log.info("Something went wrong")
        sdata = { "nodes" : self.nodedata, "links" : self.extraLinks }

        time_taken = time.clock() - start

        crawling_status = "succesfully"
        if controller.terminate_flag:
            logger.print_on_console("---------crawling request Terminated---------")
            log.info("---------crawling request Terminated---------")
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

        log.info("crawling request completed " + crawling_status +" in " +  time_str)
        completetionObj = json.dumps({"progress" : "complete" , "status": "success" ,"subdomains":  self.subdomains, "others" : self.others, "notParsedURLs" : self.notParsedURLs, "time_taken" : str(time_taken) +  " seconds"})
        socketIO.emit('result_web_crawler_finished',completetionObj)
        logger.print_on_console("--------------------")

        logger.print_on_console("crawling request completed " + crawling_status +" in " +  time_str)
        logger.print_on_console("--------------------")
        controller.terminate_flag = False