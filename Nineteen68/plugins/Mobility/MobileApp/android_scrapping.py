#-------------------------------------------------------------------------------
# Name:        android_scrapping.py
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from xml.sax.handler import ContentHandler
import xml.sax
import xml.parsers.expat
import ConfigParser
import uuid,json
import os
import subprocess
import time
import platform
from mobile_app_constants import *
import logger
##log = logging.getLogger('android_scrapping.py')

XpathList=[]
resource_id=[]
class_name=[]
enabled=[]
x_coordinate=[]
y_coordinate=[]
width=[]
height=[]
# visible=[]
rectangle=[]
focusable=[]
content_desc=[]
checked=[]
label=[]
name=[]
ScrapeList=[]
counter=0
driver=None

class InstallAndLaunch():
    def start_server(self):
        try:
            ##            maindir = os.getcwd()
            ##            os.chdir('..')
            curdir = os.environ["NINETEEN68_HOME"]

            if (platform.system() != 'Darwin'):
                path = curdir + '/Nineteen68/plugins/Mobility/MobileApp/node_modules/appium/build/lib/main.js'
                nodePath = curdir + "/Drivers/node.exe"
                proc = subprocess.Popen([nodePath, path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            else:
                path = curdir + '/Nineteen68/plugins/Mobility/node_modules/appium/build/lib/main.js'
                proc = subprocess.Popen(path, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
            time.sleep(15)
            logger.print_on_console('Server started')
        except Exception as e:
            err = 'Error while starting server'
            logger.print_on_console(err)
            log.error(err)
            log.error(e)

    def stop_server(self):
        try:
            if platform.system() != 'Darwin':
                import psutil
                processes = psutil.net_connections()
                for line in processes:
                    p = line.laddr
                    if p[1] == 4723:
                        os.system("TASKKILL /F /PID " + str(line.pid))
                        ##logger.print_on_console('Server stopped')
            else:
                os.system("killall -9 node")
        except Exception as e:
            err = 'Error while stopping server'
            logger.print_on_console(err)
            log.error(err)
            log.error(e)

    def installApplication(self, apk_path, platform_version, device_name, udid, *args):
        self.driver=None
        from appium import webdriver
        try:
            if platform.system() == 'Darwin':
                self.start_server()
                desired_caps = {}
                desired_caps['platformName'] = 'iOS'
                desired_caps['appiumVersion'] = '1.6.5'
                desired_caps['platformVersion'] = platform_version
                # desired_caps['platformVersion'] =input_val[3]
                desired_caps['deviceName'] = device_name
                # desired_caps['deviceName']=input_val[2]
                desired_caps['udid'] = udid
                # desired_caps['udid'] =input_val[1]
                desired_caps['fullReset'] = False
                desired_caps['newCommandTimeout'] = 3600
                desired_caps['launchTimeout'] = 180000
                desired_caps['app'] = apk_path
                # desired_caps['app'] =input_val[0]
                self.driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
            else:
                if device_name == 'wifi':
                    device_keywords_object = device_keywords.Device_Keywords()
                    device_keywords_object.wifi_connect()
                else:
                    self.start_server()
                    desired_caps = {}
                    desired_caps['platformName'] = 'Android'
                    ##            desired_caps['platformVersion'] = platform_version
                    desired_caps['deviceName'] = device_name
                    desired_caps['udid'] = device_name
                    desired_caps['noReset'] = True
                    desired_caps['newCommandTimeout'] = 0
                    ##desired_caps['app'] = 'D:\\mobility\\selendroid-test-app-0.17.0.apk'
                    desired_caps['app'] = apk_path
                    desired_caps['sessionOverride'] = True
                    desired_caps['fullReset'] = False
                    ##            desired_caps['logLevel'] = 'info
                    desired_caps['log_level'] = False
                    ##                print 'come in'
                    self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        except Exception as e:
            err = "Not able to install or launch application"
            logger.print_on_console(err)
            log.error(err)
            log.error(e)
        return self.driver

    def scrape(self):
        finalJson=''
        if self.driver != None:
            page_source=self.driver.page_source
            parser = xml.sax.make_parser()
            handler = Exact('/',parser,'')
            parser.setContentHandler(handler)
            ##  string="""<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][480,800]" resource-id="" instance="0"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][480,800]" resource-id="" instance="0"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="" instance="1"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/action_bar_root" instance="1"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="android:id/content" instance="2"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="" instance="2"><android.view.ViewGroup index="0" text="" class="android.view.ViewGroup" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,120]" resource-id="com.slk.tic.bokf.rmb.app:id/toolbar" instance="0"><android.widget.ImageButton index="0" text="" class="android.widget.ImageButton" package="com.slk.tic.bokf.rmb.app" content-desc="BANK OF OKLAHOMA" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][84,120]" resource-id="" instance="0"/><android.widget.TextView index="1" text="Home" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[90,57][170,98]" resource-id="" instance="0"/></android.view.ViewGroup><android.support.v4.widget.DrawerLayout index="1" text="" class="android.support.v4.widget.DrawerLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/drawer_layout" instance="0"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/container" instance="3"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,800]" resource-id="" instance="3"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,168]" resource-id="" instance="4"><android.widget.TextView index="0" text="January  2017" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,125][240,162]" resource-id="com.slk.tic.bokf.rmb.app:id/currentDate" instance="1"/><android.widget.TextView index="1" text="Acc No  ***123" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[240,125][480,162]" resource-id="com.slk.tic.bokf.rmb.app:id/accNmbr" instance="2"/></android.widget.LinearLayout><android.view.View index="1" text="" class="android.view.View" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,168][480,171]" resource-id="" instance="0"/><android.widget.FrameLayout index="2" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,171][480,406]" resource-id="com.slk.tic.bokf.rmb.app:id/chart_container" instance="4"><android.support.v4.view.ViewPager index="0" text="" class="android.support.v4.view.ViewPager" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="true" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[12,174][468,403]" resource-id="com.slk.tic.bokf.rmb.app:id/view_pager" instance="0"><android.widget.RelativeLayout index="0" text="" class="android.widget.RelativeLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[12,174][468,403]" resource-id="" instance="0"><android.view.ViewGroup index="0" text="" class="android.view.ViewGroup" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[27,189][417,388]" resource-id="com.slk.tic.bokf.rmb.app:id/piechart" instance="1"/><android.widget.LinearLayout index="1" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[341,189][453,267]" resource-id="com.slk.tic.bokf.rmb.app:id/legendsView" instance="5"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,198][453,215]" resource-id="" instance="6"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,198][362,210]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img1" instance="0"/><android.widget.TextView index="1" text="Funds Transfer" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[371,198][453,215]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text1" instance="3"/></android.widget.LinearLayout><android.widget.LinearLayout index="1" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,224][448,241]" resource-id="" instance="7"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,224][362,236]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img2" instance="1"/><android.widget.TextView index="1" text="Check Deposit" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[371,224][448,241]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text2" instance="4"/></android.widget.LinearLayout><android.widget.LinearLayout index="2" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,250][443,267]" resource-id="" instance="8"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,252][362,264]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img3" instance="2"/><android.widget.TextView index="1" text="Cash Deposit" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[371,250][443,267]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text3" instance="5"/></android.widget.LinearLayout></android.widget.LinearLayout></android.widget.RelativeLayout></android.support.v4.view.ViewPager></android.widget.FrameLayout><android.widget.LinearLayout index="3" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,406][480,446]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckBtnLayout" instance="9"><android.widget.Button index="0" text="Checking" class="android.widget.Button" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,406][240,446]" resource-id="com.slk.tic.bokf.rmb.app:id/checkingBtn" instance="0"/><android.widget.Button index="1" text="Savings" class="android.widget.Button" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[240,406][480,446]" resource-id="com.slk.tic.bokf.rmb.app:id/savingsBtn" instance="1"/></android.widget.LinearLayout><android.widget.LinearLayout index="4" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,455][480,636]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckInforLayout" instance="10"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,455][480,492]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckTitleLayout" instance="11"><android.widget.TextView index="0" text="Account No" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,455][240,492]" resource-id="" instance="6"/><android.widget.TextView index="1" text="Balance" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[240,455][480,492]" resource-id="" instance="7"/></android.widget.LinearLayout><android.widget.ListView index="1" text="" class="android.widget.ListView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="true" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,492][480,636]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckListView" instance="0"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,492][480,544]" resource-id="" instance="12"><android.widget.TextView index="0" text="***123" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[8,500][232,536]" resource-id="com.slk.tic.bokf.rmb.app:id/accountColumn" instance="8"/><android.widget.TextView index="1" text="$300.00" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[248,500][472,536]" resource-id="com.slk.tic.bokf.rmb.app:id/balanceColumn" instance="9"/></android.widget.LinearLayout><android.widget.LinearLayout index="1" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,546][480,598]" resource-id="" instance="13"><android.widget.TextView index="0" text="***456" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[8,554][232,590]" resource-id="com.slk.tic.bokf.rmb.app:id/accountColumn" instance="10"/><android.widget.TextView index="1" text="$400.00" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[248,554][472,590]" resource-id="com.slk.tic.bokf.rmb.app:id/balanceColumn" instance="11"/></android.widget.LinearLayout></android.widget.ListView></android.widget.LinearLayout><android.widget.LinearLayout index="5" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[9,636][471,792]" resource-id="" instance="14"><android.widget.ImageView NAF="true" index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[9,636][471,792]" resource-id="com.slk.tic.bokf.rmb.app:id/rewardsImage" instance="3"/></android.widget.LinearLayout></android.widget.LinearLayout></android.widget.FrameLayout></android.support.v4.widget.DrawerLayout></android.widget.LinearLayout></android.widget.FrameLayout></android.widget.LinearLayout></android.widget.FrameLayout></android.widget.LinearLayout></android.widget.FrameLayout></hierarchy>"""
            file_path_xml=os.environ["NINETEEN68_HOME"]+'/Scripts'+'/Elements.xml'
            page_source=page_source.encode('utf-8').strip()
            ##  print page_source
            try:
                with open(file_path_xml,'w') as new_file:
                    new_file.write(page_source)
                    new_file.close()

                parser.parse(file_path_xml)
                obj2=BuildJson()
                finalJson=obj2.xmltojson(self.driver)
                with open(file_path_xml,'w') as new_file:
                    new_file.write('')
                    new_file.close()
            except Exception as e:
                err = "Error occured in scraping"
                logger.print_on_console(err)
                log.error(err)
                log.error(e)
            self.stop_server()
            return finalJson


class BuildJson:

    def xmltojson(self,driver):
        import re
        global ScrapeList
        global XpathList
        global label
        global content_desc
        global class_name
        global resource_id
        global enabled
        global rectangle
        # global visible
        global x_coordinate
        global y_coordinate
        global width
        global height

        ScrapeList=[]
        custnamelist=[]
        global counter
        for i in range(len(XpathList)):
            text=''
            # print platform.system()
            if label[i] != '':
                text=label[i]
            elif platform.system()!='Darwin' and content_desc[i]  != '':
                text=content_desc[i]

            if text=='' or text==None:
                 text=class_name[i]
            if text not in custnamelist:
                custnamelist.append(text)
            else:
                text=text+str(counter)
                custnamelist.append(text)
                counter=counter+1

            if platform.system()!='Darwin':
                xpath = resource_id[i] + ';' + XpathList[i]
                ele_bounds=re.findall('\d+',rectangle[i])
    ##            bounds={'x':ele_bounds[0],
    ##            'y':ele_bounds[1],
    ##            'height':ele_bounds[3],
    ##            'width':ele_bounds[2]}
                width=int(ele_bounds[2])-int(ele_bounds[0])
                height=int(ele_bounds[3])-int(ele_bounds[1])

                ScrapeList.append({'xpath': xpath, 'tag': class_name[i],
                    'text': text,
                    'id': resource_id[i], 'custname': text,
                    'reference': str(uuid.uuid4()),'enabled':enabled[i],'left':ele_bounds[0],'top':ele_bounds[1],'width':width,'height':height})
            elif platform.system()=='Darwin':
                xpath =  XpathList[i]
                ScrapeList.append({'xpath': xpath, 'tag': class_name[i],
                   'text': text,
                   'custname': text,
                   'reference': str(uuid.uuid4()),
                   # 'visible': visible[i],
                   'enabled': enabled[i], 'left': x_coordinate[i], 'top': y_coordinate[i],
                   'width': width[i], 'height': height[i]})

        XpathList = []
        label = []
        content_desc = []
        class_name = []
        resource_id = []
        enabled = []
        # visible = []
        rectangle=[]
        x_coordinate = []
        y_coordinate = []
        width = []
        height = []
        # print 'the json is', self.save_json(ScrapeList)
        return self.save_json(ScrapeList, driver)


    def save_json(self,scrape_data,driver):
        from collections import OrderedDict
        jsonArray=OrderedDict()

        jsonArray['view']= scrape_data
##        jsonArray['mirror']='IMAGEEEEE'
        jsonArray['mirror']=driver.get_screenshot_as_base64()
        dimension = driver.get_window_size()
        jsonArray['mirrorwidth'] = dimension['width']
        jsonArray['mirrorheight'] = dimension['height']
        file_path_json=os.environ["NINETEEN68_HOME"]+'/Scripts'+'/domelements_Android.json'
        with open(file_path_json, 'w') as outfile:
            logger.print_on_console('Writing scrape data to domelements.json file')
            json.dump(jsonArray, outfile, indent=4, sort_keys=False)
            outfile.close()
        return jsonArray




class Exact(xml.sax.handler.ContentHandler):

    def __init__(self,xpath,xmlreader,parent):
        self.curpath = []
        self.xPath=xpath
        self.parser=xmlreader
        self.elementNameCount={}
        self.buffer=''
        self.parent=parent


    def startElement(self, qName, attrs):
        count = self.elementNameCount.get(qName)
        if count==None:
            count=1
        else:
            count=count+1
        self.elementNameCount[qName]=count
        childXPath = self.xPath + "/" + qName + "[" + str(count) + "]";
        attsLength = len(attrs)
        if(attsLength>1):
            XpathList.append(childXPath)
        elements_list = attrs.getQNames()
        label_flag = False
        for x in attrs.getQNames():
            if platform.system()=='Darwin':
                value = attrs.getValue(x)
                # if x.lower()=='text':
                if x.lower() == 'label':
                    ##            if(value == ''):
                    ##		      label.append(qName)
                    ##            else:
                    label_flag = True
                    label.append(value)
                    name.append(qName)
                    # elif x.lower()=='bounds':
                # 	rectangle.append(value)

                elif x.lower() == 'enabled':
                    enabled.append(value)

                # elif x.lower() == 'visible':
                #     visible.append(value)

                elif x.lower() == 'x':
                    x_coordinate.append(value)

                elif x.lower() == 'y':
                    y_coordinate.append(value)

                elif x.lower() == 'width':
                    width.append(value)

                elif x.lower() == 'height':
                    height.append(value)

                    # elif x.lower()=='resource-id':
                # 	resource_id.append(value)

                # elif x.lower()=='focusable':
                # 	focusable.append(value)

                elif x.lower() == 'type':
                    class_name.append(value)

                    # elif x.lower()=='content-desc':
                    # 	content_desc.append(value)

                    # elif x.lower()=='checked':
                    # 	checked.append(value)
            elif platform.system()!='Darwin':
                value=attrs.getValue(x)

                if x.lower()=='text':
        ##            if(value == ''):
        ##		      label.append(qName)
        ##            else:
                    label.append(value)

                    name.append(qName)

                elif x.lower()=='bounds':
                        rectangle.append(value)

                elif x.lower()=='enabled':
                        enabled.append(value)

                elif x.lower()=='resource-id':
                        resource_id.append(value)

                elif x.lower()=='focusable':
                        focusable.append(value)

                elif x.lower()=='class':
                        class_name.append(value)

                elif x.lower()=='content-desc':
                        content_desc.append(value)

                elif x.lower()=='checked':
                        checked.append(value)
        if platform.system() == 'Darwin':
            if label_flag == False and len(elements_list) > 0:
                label.append(qName)
        curobj=self
        child = Exact(childXPath,self.parser,curobj)
        self.parser.setContentHandler(child)

    def endElement(self, name):
        value = self.buffer.strip();
        if(value != ''):
                print (self.xPath + "='" + self.buffer.toString() + "'")

        self.parser.setContentHandler(self.parent)

    def characters(self, data):
        self.buffer += data



##if __name__ == '__main__':
##  import sys
##  list_args=sys.argv[1:]
##  apk_path=platform=device_name=None
##  obj=InstallAndLaunch()
##
##  apk_path=raw_input('Enter apk path')
##  platform=raw_input('Enter platform')
##  device_name=raw_input('Enter device_name')
##
####  if len(list_args)== 3:
####    apk_path=list_args[0]
####    platform=list_args[1]
####    device_name=list_args[2]
##  print apk_path,platform,device_name
####  apk_path='D:\\apks\\selendroid-test-app-0.17.0.apk'
####  platform='6.0'
####  device_name='AND6:5554'
##
##  obj.start_server()
##  driver=obj.installApplication(apk_path,platform,device_name)
##  page_source=None
##  if driver != None:
##    page_source=driver.page_source
##  parser = xml.sax.make_parser()
##  handler = Exact('/',parser,'')
##  parser.setContentHandler(handler)
####  string="""<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][480,800]" resource-id="" instance="0"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][480,800]" resource-id="" instance="0"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="" instance="1"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/action_bar_root" instance="1"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="android:id/content" instance="2"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="" instance="2"><android.view.ViewGroup index="0" text="" class="android.view.ViewGroup" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,120]" resource-id="com.slk.tic.bokf.rmb.app:id/toolbar" instance="0"><android.widget.ImageButton index="0" text="" class="android.widget.ImageButton" package="com.slk.tic.bokf.rmb.app" content-desc="BANK OF OKLAHOMA" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][84,120]" resource-id="" instance="0"/><android.widget.TextView index="1" text="Home" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[90,57][170,98]" resource-id="" instance="0"/></android.view.ViewGroup><android.support.v4.widget.DrawerLayout index="1" text="" class="android.support.v4.widget.DrawerLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/drawer_layout" instance="0"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/container" instance="3"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,800]" resource-id="" instance="3"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,168]" resource-id="" instance="4"><android.widget.TextView index="0" text="January  2017" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,125][240,162]" resource-id="com.slk.tic.bokf.rmb.app:id/currentDate" instance="1"/><android.widget.TextView index="1" text="Acc No  ***123" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[240,125][480,162]" resource-id="com.slk.tic.bokf.rmb.app:id/accNmbr" instance="2"/></android.widget.LinearLayout><android.view.View index="1" text="" class="android.view.View" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,168][480,171]" resource-id="" instance="0"/><android.widget.FrameLayout index="2" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,171][480,406]" resource-id="com.slk.tic.bokf.rmb.app:id/chart_container" instance="4"><android.support.v4.view.ViewPager index="0" text="" class="android.support.v4.view.ViewPager" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="true" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[12,174][468,403]" resource-id="com.slk.tic.bokf.rmb.app:id/view_pager" instance="0"><android.widget.RelativeLayout index="0" text="" class="android.widget.RelativeLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[12,174][468,403]" resource-id="" instance="0"><android.view.ViewGroup index="0" text="" class="android.view.ViewGroup" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[27,189][417,388]" resource-id="com.slk.tic.bokf.rmb.app:id/piechart" instance="1"/><android.widget.LinearLayout index="1" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[341,189][453,267]" resource-id="com.slk.tic.bokf.rmb.app:id/legendsView" instance="5"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,198][453,215]" resource-id="" instance="6"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,198][362,210]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img1" instance="0"/><android.widget.TextView index="1" text="Funds Transfer" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[371,198][453,215]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text1" instance="3"/></android.widget.LinearLayout><android.widget.LinearLayout index="1" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,224][448,241]" resource-id="" instance="7"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,224][362,236]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img2" instance="1"/><android.widget.TextView index="1" text="Check Deposit" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[371,224][448,241]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text2" instance="4"/></android.widget.LinearLayout><android.widget.LinearLayout index="2" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,250][443,267]" resource-id="" instance="8"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,252][362,264]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img3" instance="2"/><android.widget.TextView index="1" text="Cash Deposit" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[371,250][443,267]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text3" instance="5"/></android.widget.LinearLayout></android.widget.LinearLayout></android.widget.RelativeLayout></android.support.v4.view.ViewPager></android.widget.FrameLayout><android.widget.LinearLayout index="3" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,406][480,446]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckBtnLayout" instance="9"><android.widget.Button index="0" text="Checking" class="android.widget.Button" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,406][240,446]" resource-id="com.slk.tic.bokf.rmb.app:id/checkingBtn" instance="0"/><android.widget.Button index="1" text="Savings" class="android.widget.Button" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[240,406][480,446]" resource-id="com.slk.tic.bokf.rmb.app:id/savingsBtn" instance="1"/></android.widget.LinearLayout><android.widget.LinearLayout index="4" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,455][480,636]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckInforLayout" instance="10"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,455][480,492]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckTitleLayout" instance="11"><android.widget.TextView index="0" text="Account No" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,455][240,492]" resource-id="" instance="6"/><android.widget.TextView index="1" text="Balance" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[240,455][480,492]" resource-id="" instance="7"/></android.widget.LinearLayout><android.widget.ListView index="1" text="" class="android.widget.ListView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="true" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,492][480,636]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckListView" instance="0"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,492][480,544]" resource-id="" instance="12"><android.widget.TextView index="0" text="***123" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[8,500][232,536]" resource-id="com.slk.tic.bokf.rmb.app:id/accountColumn" instance="8"/><android.widget.TextView index="1" text="$300.00" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[248,500][472,536]" resource-id="com.slk.tic.bokf.rmb.app:id/balanceColumn" instance="9"/></android.widget.LinearLayout><android.widget.LinearLayout index="1" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,546][480,598]" resource-id="" instance="13"><android.widget.TextView index="0" text="***456" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[8,554][232,590]" resource-id="com.slk.tic.bokf.rmb.app:id/accountColumn" instance="10"/><android.widget.TextView index="1" text="$400.00" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[248,554][472,590]" resource-id="com.slk.tic.bokf.rmb.app:id/balanceColumn" instance="11"/></android.widget.LinearLayout></android.widget.ListView></android.widget.LinearLayout><android.widget.LinearLayout index="5" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[9,636][471,792]" resource-id="" instance="14"><android.widget.ImageView NAF="true" index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[9,636][471,792]" resource-id="com.slk.tic.bokf.rmb.app:id/rewardsImage" instance="3"/></android.widget.LinearLayout></android.widget.LinearLayout></android.widget.FrameLayout></android.support.v4.widget.DrawerLayout></android.widget.LinearLayout></android.widget.FrameLayout></android.widget.LinearLayout></android.widget.FrameLayout></android.widget.LinearLayout></android.widget.FrameLayout></hierarchy>"""
##  file_path_xml=os.getcwd()+'//Elements.xml'
##  page_source=page_source.encode('utf-8').strip()
####  print page_source
##  try:
##      with open(file_path_xml,'w') as new_file:
##        new_file.write(page_source)
##        new_file.close()
##
##      parser.parse(file_path_xml)
##      obj2=BuildJson()
##      obj2.xmltojson(driver)
##
##      with open(file_path_xml,'w') as new_file:
##        new_file.write('')
##        new_file.close()
##  except Exception as e:
##    print e
##
##  obj.stop_server()

