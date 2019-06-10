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
import desktop_scraping

log = logging.getLogger( 'desktop_custom_object.py' )
class CustomObjectHandler():
    def get_all_custom_children(self, ch, ne, i, path, win):
        """Method to retreve full scraped objects, returns a list ne[]"""
        try:
            for i in range (len(ch)):
                 hiddentag = 'Yes'
                 text = ''
                 parent = ''
                 coordinates = ''
                 tag = ch[i].friendly_class_name()
                 log.info( tag )
##                 if tag == 'Button' or tag =='RadioButton' or tag == 'Edit' or tag == 'ComboBox' or tag == 'Static' or tag == 'GroupBox' or tag == 'CheckBox' or tag== 'ListView' or tag == 'ListBox'or tag == 'TreeView'or tag == 'TabControl' or tag == 'DateTimePicker'  or tag == 'Toolbar':
                 try:
                    coordinates = ch[i].client_rect()
                 except:
                    """ Logic to find height and width for non hwndwrapper elements """
                    coordinates_obj = desktop_scraping.Rectangle()
                    coordinates_obj.set_coordinates(ch[i])
                    pass
                 cor = ch[i].rectangle()
                 properties = ''
                 try:
                     pythoncom.CoInitialize()
                     try:
                        properties = json.loads(json.dumps(ch[i].get_properties(    ), default = lambda x : str(x)))
                     except Exception as e:
                        #----hardcoding only done for 32bit python as its not performing via ch[i].get_properties
                        #----' id {0}'.format(button.idCommand)) or
                        #----RuntimeError: GetButtonInfo failed for "element" with command id XXXX occours when one of the properties not correct
                        #----Please Refer SWAPY application and check the element ,if all the properties are not populating , chances are this
                        #--- error will occour.I have noticed most of the time ch[i].texts() is the problem hence setting it to u''
                        try:
                            getProperties = {'is_enabled' : ch[i].is_enabled(),
                                           'is_visible' : ch[i].is_visible(),
                                           'style' : ch[i].style(),
                                           'fonts' : ch[i].fonts(),
                                           'client_rects' : ch[i].client_rects(),
                                           'texts': '',
                                           'class_name' : ch[i].class_name(),
                                           'is_unicode' : ch[i].is_unicode(),
                                           'control_id' : ch[i].control_id(),
                                           'menu_items' : ch[i].menu_items(),
                                           'user_data' : ch[i].user_data(),
                                           'friendly_class_name' : ch[i].friendly_class_name(),
                                           'control_count' : ch[i].control_count(),
                                           'exstyle' : ch[i].exstyle(),
                                           'context_help_id' : ch[i].context_help_id(),
                                           'rectangle' : ch[i].rectangle()
                                          }
                            properties = json.loads(json.dumps(getProperties, default = lambda x : str(x)))
                        except Exception as e:
                            """Some properties dont exists in ele<uia> when comapred to ele<win32>"""
                            try:
                                getProperties = {'is_enabled' : ch[i].is_enabled(),
                                           'is_visible' : ch[i].is_visible(),
                                           'style' : '',
                                           'fonts' : '',
                                           'client_rects' : '',
                                           'texts' : '',
                                           'class_name' : ch[i].class_name(),
                                           'is_unicode' : '',
                                           'control_id' : '',
                                           'menu_items' : '',
                                           'user_data' : '',
                                           'friendly_class_name' : ch[i].friendly_class_name(),
                                           'control_count' : '',
                                           'exstyle' : '',
                                           'context_help_id' : '',
                                           'rectangle' : ch[i].rectangle()
                                          }
                                properties = json.loads(json.dumps(getProperties, default = lambda x : str(x)))
                            except Exception as e:
                                logger.print_on_console ( e )
                                pass
                     if ( properties['is_visible'] == True ):
                         properties["url"] =  win.texts()[0] if ( len(win.texts()) > 0 ) else ""
                         properties['control_id'] = ch[i].element_info.control_id
                         properties['parent'] = ch[i].element_info.parent.class_name
                         handle = ch[i].handle
                         text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                         if ( text == '' ):
                            t = ch[i].texts()
                            if ( len(t) >= 2 ):
                                text = t[1]
                         if ( text == '' ):
                            text = ch[i].friendly_class_name()
                         text = text.strip()
                         url = properties['url']
                         parent = properties['parent']
                         rectangle = properties['rectangle']
                         path = str (parent) + '[' + str(i) + ']'
                         if ( tag == 'Button' ):
                            tag = 'button'
                            text =  str(text) + '_btn'
                         elif ( tag == 'Edit' ):
                            tag = 'input'
                            text =  str(text) + '_txtbox'
                         elif ( tag == 'RadioButton' ):
                            tag = 'radiobutton'
                            text = str(text) + '_radiobtn'
                         elif ( tag == 'ComboBox' ):
                            tag = 'select'
                            text = str(text) + '_dropdown'
                         elif ( tag == 'CheckBox' ):
                            tag ='checkbox'
                            text = str(text) + '_chkbox'
                         elif ( tag == 'ListView' ):
                            tag = 'list'
                            text = str(text) + '_list'
                         elif ( tag == 'ListBox' ):
                            tag = 'list'
                            text = str(text) + '_list'
                         elif ( tag == 'TabControl' ):
                            tag = 'tab'
                            text = str(text) + '_tab'
                         elif ( tag == 'DateTimePicker' ):
                            tag = 'datepicker'
                            text = str(text) + '_dtp'
                         elif ( tag == 'Table' ):
                            tag = 'table'
                            text = str(text) + '_table'
                         else:
                            tag = 'label'
                            if ( not isinstance(text, str) ):
                                text = str(text) + '_lbl'
                            else:
                                text = text + '_lbl'
                         try:
                            width = coordinates.width()
                            height = coordinates.height()
                         except:
                            width = coordinates_obj.width
                            height = coordinates_obj.height
                            pass
                         x_screen = cor.left
                         y_screen = cor.top
                         left = cor.left
                         top = cor.top
                         control_id = properties['control_id']
                         if ( control_id == None ):
                            control_id = 'null'
                         if ( properties['is_visible'] == True ):
                            hiddentag = 'No'
                            flag = False
                            for k in range(len(ne)):
                                if ( ne[k]['xpath'] == path ):
                                    flag = True
                            new_path = ''
                            className = ch[i].friendly_class_name()
                            new_path = path + ';' + className + ';' + str(control_id)
                            if ( not flag ):
                                ne.append({"custname" : text,
                                        "tag" : tag,
                                        "url" : url,
                                        'control_id' : control_id,
                                        'parent' : parent,
                                        'xpath' : new_path,
                                        'hiddentag' : hiddentag,
                                        'top' : top,
                                        'left' : left,
                                        'height' : height,
                                        'width' : width,
                                        'x_screen' :x_screen,
                                        'y_screen' :y_screen
                                        })
                            else:
                                logger.print_on_console( 'This element is duplicate' )
                     else:
                        text = ''
                        handle = ch[i].handle
                        text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                 except Exception as e:
##                    import traceback
##                    traceback.print_exc()

                    logger.print_on_console( e )
                    log.error ( 'Error occoured in CustomObjectHandler, Error Msg : ', e )
        except Exception as e:
##            import traceback
##            traceback.print_exc()
            logger.print_on_console( e )
            log.error ( 'Error occoured in CustomObjectHandler, Error Msg : ', e )
        return ne

    def for_custom_scrape(self, backendType):
        """Method to perform a  full scrape, returns allobjects"""
        try:
            obj = desktop_launch_keywords.Launch_Keywords()
            obj.set_to_foreground()
            obj.bring_Window_Front()
            if ( backendType == 'A' ):
                win = desktop_launch_keywords.app_win32.top_window()
                ch = win.children()
            elif ( backendType == 'B' ):
                win = desktop_launch_keywords.app_uia.top_window()
##                ch=win.children()[:]
##                for i in range(0,len(ch)):
##                    if len(ch[i].children()):
##                        c=ch[i].children()
##                        for a in c:
##                            ch.append(a)
                ch = []
                def rec_ch(child):
                    ch.append(child)
                    for c in child.children():
                        rec_ch(c)
                rec_ch(win)
            #----------------------Tooltips are treated as children to the top window, they will disappear after 7 seconds
            if ( win.friendly_class_name() == "ToolTips" or win.friendly_class_name() == "SysShadow" ): #---Checking if the win has a friendly class name Tooltips
                time.sleep(7)                                   #---Waiting for 7 seconds so that the Tooltip disappears
                if ( backendType == 'A' ):
                    win = desktop_launch_keywords.app_win32.top_window()
                    ch = win.children()
                elif ( backendType == 'B' ) :
                    win = desktop_launch_keywords.app_uia.top_window()
##                    ch = win.children()[:]
##                    for i in range(0,len(ch)):
##                        if len(ch[i].children()):
##                            c = ch[i].children()
##                            for a in c:
##                                ch.append(a)                     #---trying to get the top window again
                    ch = []
                    def rec_ch(child):
                        ch.append(child)
                        for c in child.children():
                            rec_ch(c)
                    rec_ch(win)
            #---------------------------------------------------
            allobjects = ''
            ne = []
            allobjects =  self.get_all_custom_children(ch, ne, 0, '', win)
        except Exception as e:
##            import traceback
##            traceback.print_exc()
            logger.print_on_console( e )
            log.error( 'Error occoured in fullscrape, warning Msg : ', e )
        return allobjects

    def getobjectforcustom(self, parent_xpath, eleType, eleIndex):
        """Method to retreve Custom elements, returns xpath of the element , after searching for in the list of data recieved from function(for_custom_scrape)"""
        """Note: parent_xpath is the xpath of the element from where custom keyword performs its operation."""
        x_var = parent_xpath.split(';')
        parent_xpath = x_var[0]
        data = []
        newdata = []
        backendType = x_var[4]
        xpath = None
        try:
            #app_uia = desktop_launch_keywords.app_uia
            try:
                data = self.for_custom_scrape(backendType)
            except:
                backendType = 'A'
                data = self.for_custom_scrape(backendType)

            for index, item in enumerate(data):
                i_var = item['xpath'].split(';')
                item_xpath = i_var[0]
                if ( item_xpath == parent_xpath ):
                    newdata = data[index + 1 :]
            for elem in newdata :
                if ( elem['tag'].lower() == eleType.strip().lower() ):
##                    try:
                        eleIndex = int(eleIndex) - 1
                        if ( eleIndex == 0 ):
                            xpath = elem['xpath']
##                        elif ( eleIndex < 0 ):
##                            logger.print_on_console( "Entered index value is 0 or lesser,please provide a correct index value" )
##                    except:
##                        logger.print_on_console( e )
        except Exception as e:
            logger.print_on_console( e )
        if ( xpath == None ):
            logger.print_on_console( 'Warning! : AUT Structure has changed, unable to verify the parent element.' )
            log.error( 'Warning! : AUT Structure has changed, unable to verify the parent element.' )
        return xpath