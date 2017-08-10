#-------------------------------------------------------------------------------
# Name:         desktop_custom_object
# Purpose:      This script is created keeping in mind that while performing
#               actions on custom objects a full scrape is required,we will keep
#               the parent element as a reference point. Any object beyond that
#               is treated as its children and likewise, operations are performed.
#
# Author:      anas.ahmed
#
# Created:     12-07-2017
# Copyright:   (c) anas.ahmed 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_launch_keywords
import logger
import logging
import desktop_constants
import json
import pywinauto
import pyHook
import pythoncom
import ctypes
import win32gui
import win32api
import time
from desktop_launch_keywords import Launch_Keywords
from constants import *

log = logging.getLogger('desktop_custom_object.py')
class CustomObjectHandler():
    def get_all_custom_children(self,ch,ne,i,path,win):
        """Method to retreve full scraped objects, returns a list ne[]"""
        try:
            for i in range (len(ch)):
                 hiddentag = 'Yes'
                 text = ''
                 parent = ''
                 coordinates = ''
                 children = ch[i]
                 tag = children.friendly_class_name()
                 log.info(tag)
##                 if tag == 'Button' or tag =='RadioButton' or tag == 'Edit' or tag == 'ComboBox' or tag == 'Static' or tag == 'GroupBox' or tag == 'CheckBox' or tag== 'ListView' or tag == 'ListBox'or tag == 'TreeView'or tag == 'TabControl' or tag == 'DateTimePicker'  or tag == 'Toolbar':
                 coordinates = children.client_rect()
                 cor = children.rectangle()
                 properties = ''
                 try:
                     try:
                        properties = json.loads(json.dumps(children.get_properties(    ), default=lambda x: str(x)))
                     except Exception as e:
                        #----hardcoding only done for 32bit python as its not performing via children.get_properties
                        #----' id {0}'.format(button.idCommand)) or
                        #----RuntimeError: GetButtonInfo failed for "element" with command id XXXX occours when one of the properties not correct
                        #----Please Refer SWAPY application and check the element ,if all the properties are not populating , chances are this
                        #--- error will occour.I have noticed most of the time children.texts() is the problem hence setting it to u''
                        try:
                            getProperties={u'is_enabled': children.is_enabled(),
                                           u'is_visible': children.is_visible(),
                                           u'style': children.style(),
                                           u'fonts': children.fonts(),
                                           u'client_rects': children.client_rects(),
                                           u'texts': u'',
                                           u'class_name': children.class_name(),
                                           u'is_unicode': children.is_unicode(),
                                           u'control_id': children.control_id(),
                                           u'menu_items': children.menu_items(),
                                           u'user_data': children.user_data(),
                                           u'friendly_class_name': children.friendly_class_name(),
                                           u'control_count': children.control_count(),
                                           u'exstyle': children.exstyle(),
                                           u'context_help_id': children.context_help_id(),
                                           u'rectangle': children.rectangle()
                                          }
                            properties = json.loads(json.dumps(getProperties, default=lambda x: str(x)))
                        except Exception as e:
                            logger.print_on_console (e)
                     if properties['is_visible'] == True :
                         properties["url"] =  win.texts()[0] if len(win.texts())>0 else ""
                         properties['control_id'] = children.element_info.control_id
                         properties['parent'] = children.element_info.parent.class_name
                         handle = children.handle
                         text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                         if text =='':
                            t = children.texts()
                            if len(t) >= 2:
                                text = t[1]
                         if text == '':
                            text = children.friendly_class_name()
                         text = text.strip()
                         url = properties['url']
                         parent = properties['parent']
                         rectangle = properties['rectangle']
                         path = str (parent) + '[' + str(i) + ']'
                         if tag == 'Button':
                            tag = 'button'
                            text=  str(text) + '_btn'
                         elif tag == 'Edit':
                            tag = 'input'
                            text=  str(text) + '_txtbox'
                         elif tag == 'RadioButton':
                            tag = 'radiobutton'
                            text= str(text) + '_radiobtn'
                         elif tag == 'ComboBox':
                            tag = 'select'
                            text= str(text) + '_dropdown'
                         elif tag == 'CheckBox':
                            tag ='checkbox'
                            text= str(text) + '_chkbox'
                         elif tag == 'ListView':
                            tag = 'list'
                            text= str(text) + '_list'
                         elif tag == 'ListBox':
                            tag = 'list'
                            text= str(text) + '_list'
                         elif tag == 'TabControl':
                            tag = 'tab'
                            text= str(text) + '_tab'
                         elif tag == 'DateTimePicker':
                            tag = 'datepicker'
                            text= str(text) + '_dtp'
                         else:
                            tag = 'label'
                            text= str(text) + '_lbl'
                         width = coordinates.width()
                         height = coordinates.height()
                         x_screen = cor.left
                         y_screen = cor.top
                         left = cor.left
                         top = cor.top
                         control_id = properties['control_id']
                         if control_id == None:
                            control_id ='null'
                         if properties['is_visible'] == True :
                            hiddentag = 'No'
                            flag = False
                            for k in range(len(ne)):
                                if ne[k]['xpath'] == path:
                                    flag = True
                            if not flag:
                                ne.append({"custname":text,
                                        "tag":tag,
                                        "url":url,
                                        'control_id':control_id,
                                        'parent':parent,
                                        'xpath' : path,
                                        'hiddentag':hiddentag,
                                        'top': top,
                                        'left': left,
                                        'height': height,
                                        'width': width,
                                        'x_screen':x_screen,
                                        'y_screen':y_screen
                                        })
                            else:
                                logger.print_on_console( 'This element is duplicate')
                     else:
                        text = ''
                        handle = children.handle
                        text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                 except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.print_on_console( e)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.print_on_console( e)
        return ne

    def for_custom_scrape(self,app_uia):
        """Method to perform a  full scrape, returns allobjects"""
        try:
            obj = desktop_launch_keywords.Launch_Keywords()
            obj.set_to_foreground()
            obj.bring_Window_Front()
            win = app_uia.top_window()
            #----------------------Tooltips are treated as children to the top window, they will disappear after 7 seconds
            if win.friendly_class_name()=="ToolTips" or win.friendly_class_name()=="SysShadow": #---Checking if the win has a friendly class name Tooltips
                time.sleep(7)                                   #---Waiting for 7 seconds so that the Tooltip disappears
                win = app_uia.top_window()                      #---trying to get the top window again
            #---------------------------------------------------
            ch = win.children()
            allobjects = ''
            ne = []
            allobjects =  self.get_all_custom_children(ch,ne,0,'',win)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.print_on_console(e)
        return allobjects

    def getobjectforcustom(self, parent_xpath, eleType, eleIndex):
        """Method to retreve Custom elements, returns xpath of the element , after searching for in the list of data recieved from function(for_custom_scrape)"""
        """Note: parent_xpath is the xpath of the element from where custom keyword performs its operation."""
        data = []
        newdata=[]
        xpath = None
        try:
            app_uia = desktop_launch_keywords.app_uia
            data = self.for_custom_scrape(app_uia)
            for index, item in enumerate(data):
                if item['xpath']==parent_xpath:
                    newdata =data[index+1:]
            for elem in newdata :
                if elem['tag'].lower() == eleType.strip().lower():
##                    try:
                        eleIndex = int(eleIndex) - 1
                        if(eleIndex == 0):
                            xpath = elem['xpath']
##                        elif(eleIndex<0):
##                            logger.print_on_console("Entered index value is 0 or lesser,please provide a correct index value")
##                    except:
##                        logger.print_on_console( e)
        except Exception as e:
            import traceback
            traceback.print_exc()
        return xpath


