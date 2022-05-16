
import re
from oebs_jab_object import JAB
import json
import logging
import time
import ast
import win32gui
import win32api
from oebs_constants import *
import logger
import oebs_click_and_add
import os
log=logging.getLogger('oebs_xpath_generator.py')


class PathGenerator():
    def __init__(self,window_name=''):
        self.path = ''
        self.activeframename = ''
        self.store_object = []
        self.previous_path = ''
        self.path_generator_free = True
        self.window_name = window_name

    def postfixCustname(self,role,custname):
        if(role in ['push button','toggle button']):
            custname = custname + "_btn"
        elif(role in ['edit','Edit Box','text','password text']):
            custname = custname + "_txtbox"
        elif(role == 'combo box'):
            custname = custname +"_select"
        elif(role == 'radio button'):
            custname = custname + "_radiobtn"
        elif(role == 'check box'):
            custname = custname + "_chkbox"
        elif(role == 'table'):
            custname = custname + "_table"
        elif(role in ['list item','list']):
            custname = custname + "_lst"
        elif(role == 'internal frame'):
            custname = custname + "_internalframe"
        elif(role == "scroll bar"):
            custname = custname + "_scroll"
        elif(role in ['hyperlink','Static']):
            custname = custname + "_link"
        else:
            custname = custname + "_elmnt"
        return custname


    def match(self,objectInfo,point):
        expectedx=int(objectInfo[0])+int(objectInfo[2])
        expectedy=int(objectInfo[1])+int(objectInfo[3])
        if((point[0] >= int(objectInfo[0]) and point[0]<=expectedx) and (point[1] >= int(objectInfo[1]) and point[1]<=expectedy)):
            return 1
        else:
            return 0

    def get_path(self,obj,eventName='',window_name=''):
        current_acc_info = obj._get__JABAccContextInfo()
        parent_acc = obj._get_parent()

        if eventName == 'stateChange' and current_acc_info.role not in ('page tab','list'):
            return

        if eventName == 'caret' and current_acc_info.role != 'text' and len(self.store_object) > 0:
            return
        
        #added me "label"
        if eventName == 'mousePressed' and current_acc_info.role not in ('text','combo box','push button','check box','radio button', 'label','page tab list', 'tool bar', 'menu', 'scroll bar'):
            return

        if -1 in (current_acc_info.x,current_acc_info.y,current_acc_info.width,current_acc_info.height):
            return
        


        #(To Check the Co-ordination)
        #--------------------------
        hwnd = win32gui.FindWindow(None, oebs_click_and_add.core.window_name)
        win_rect= win32gui.GetWindowRect(hwnd)

        #coordinates Calculation
        x1_win = win_rect[0]
        y1_win = win_rect[1]
        x2_win = win_rect[2]
        y2_win = win_rect[3]
        width_win = x2_win - x1_win
        height_win = y2_win - y1_win
        #width=current_acc_info.width
        #height=current_acc_info.height
        left_need = current_acc_info.x
        top_need =  current_acc_info.y 
        point=win32gui.GetCursorPos()
        #-----------------------

        if current_acc_info.role == 'page tab list':
            try:
                # path for page tab returns a new jabContext 
                # check the logic
                tempJabContext = self.path_for_page_tab(obj)
                obj = JAB(jabContext=tempJabContext)
                current_acc_info = obj._get__JABAccContextInfo()
                parent_acc = obj._get_parent()
            except Exception as e:
                log.debug(e)

        
        if current_acc_info.role == 'tool bar':
            try:
                tempJabContext = self.path_for_tool_bar(obj)
                for key in tempJabContext:
                    arr=key.split(',')
                    data = self.match(arr,point)
                    if data == 1:
                        break
                obj = JAB(jabContext=tempJabContext[key])
                current_acc_info = obj._get__JABAccContextInfo()
                parent_acc = obj._get_parent()
            except Exception as e:
                log.debug(e)
        
        
        self.path_generator_free = False
        xpath = self.generate_xpath(obj)
        if xpath == 'fail':
            return
        # get the value selected in combo box - not implemented yet
        # traverse throught the childern of the obj (combo box) and check the status of all childern if selected 
        # get the name and index of parent of the child
        keyboard_shortcut = obj._get_keyboardShortcut()

        try:
            name = obj._get_name()
            if name is None or name == '':
                name = current_acc_info.name
        except Exception as e:
            log.debug(e)

        parent_xpath = xpath.rsplit('//',1)[0]
        parent_xpath = parent_xpath.replace('//','/')
        xpath = xpath.replace('//','/')

        path = xpath + ';' +  str(name) + ';' + str(obj._get_indexInParent()) + ';' + str(obj._get_childCount()) + ';' + str(parent_acc._get_name()).strip() + ';' + str(parent_xpath) + ';' + str(parent_acc._get_childCount()) + ';' + str(parent_acc._get_indexInParent()) + ';' + str(parent_acc.role) + ';' + str(current_acc_info.role) + ';' + str(obj._get_description())

        path_to_check = xpath + ';' +  str(name) + ';' + str(obj._get_indexInParent()) + ';' + str(current_acc_info.role)

        if path_to_check == self.previous_path:
            self.path = ''
            if eventName == 'caret':
                self.edit_text_value(obj)

            if current_acc_info.role == 'combo box' or current_acc_info.role == 'list':
                self.edit_combo_text(obj)
            
            self.path_generator_free = True
            return
        
        if eventName not in ('mousePressed','stateChange'):
            self.path = ''
            self.path_generator_free = True
            return
        
        if len(current_acc_info.name) == 0 :
            if current_acc_info.description is not None:
                description = current_acc_info.description
            else:
                description = ''
        if current_acc_info.accessibleText == 1:
            charinfo = obj.jabContext.getAccessibleTextInfo(0,1)
            text = obj.jabContext.getAccessibleTextRange(0,charinfo.charCount - 1)
            text = text.strip()
            text = str(text)
            text = text.strip()
            text = text.replace('<','')
            text = text.replace('>','')

        else:
            text = ''

        if current_acc_info.role == 'combo box' or current_acc_info.role == 'list':
            text = self.get_combo_box_text(obj)
        
        log.info("Element ' %s ' of role ' %s ' recorded"%(str(name),str(current_acc_info.role)))

        #custname
        if text.strip() == '':
            text = name.strip().replace('<','').replace('>','')
        custname = self.postfixCustname(str(current_acc_info.role),text.strip())
        #custname


        self.store_object.append({
            "custname": custname,
            "tag":current_acc_info.role,
	        "xpath":path,
	        "hiddentag":str(False),
	        "id":'null',
	        "text":str(text),
	        "url":oebs_click_and_add.core.window_name,
	        "x_coor":current_acc_info.x,
	        "y_coor":current_acc_info.y,
            "left":left_need,
            "top":top_need,
	        "width":current_acc_info.width,
	        "height":current_acc_info.height,
            "keyboardshortcut":str(keyboard_shortcut),
            "value":''
        })

        self.previous_path , self.path  = path_to_check , ''
        self.path_generator_free = True
    
    def generate_xpath(self,obj):
        current_acc_info = obj._get__JABAccContextInfo()
        tagrole = current_acc_info.role
        tagname = current_acc_info.name
        text = current_acc_info.name
        j = current_acc_info.indexInParent
        queue = []
        p = ''
        loop = True
        while loop:
            current_acc_info = obj._get__JABAccContextInfo()
            tagname = current_acc_info.name
            text = current_acc_info.name
            j = current_acc_info.indexInParent
            if j == 2 and current_acc_info.role == "panel" and tagrole == "combo box":
                j = 1
            if j == -1 and current_acc_info.role == "frame":
                j = 0

            if self.path == '':
                if len(current_acc_info.description.strip()) == 0:
                    self.path = current_acc_info.role + '[' + str(j) + ']' 
                else:
                    if 'panel' in current_acc_info.role:
                        self.path = current_acc_info.role  + '[' + str(j) + ']'
                    else:
                        self.path = current_acc_info.role + '[' + str(current_acc_info.description.strip()) + ']' 
            else:
                if len(current_acc_info.description.strip()) == 0:
                    self.path = current_acc_info.role  + '[' + str(j) + ']' + '//' + self.path
                else:
                    if 'panel' in current_acc_info.role:
                        self.path = current_acc_info.role  + '[' + str(j) + ']' + '//' + self.path
                    else:
                        self.path = current_acc_info.role  + '[' + str(current_acc_info.description.strip()) + ']' + '//' + self.path
            if obj._get_object_depth() > 0:
                obj = obj._get_parent()
                parent = obj._get__JABAccContextInfo()
                if current_acc_info.role == 'push button' and parent.role == 'scroll bar':
                    err_msg = ERROR_CODE_DICT['err_push_btn_scroll_bar']
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
                    self.path = ''
                    return 'fail'
                if current_acc_info.role == 'scroll bar' and parent.role == 'scroll pane':
                    err_msg = ERROR_CODE_DICT['err_scroll_in_list']
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
                    self.path = ''
                    return 'fail'
            else:
                loop = False

        return self.path

    def isFree(self):
        return self.path_generator_free

    def create_file(self,window_name=''):
        data = {'view':self.store_object}
        data = json.dumps(data)
        data_out = ast.literal_eval(data)

        with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json',"w") as f:
            json.dump(data_out, f, indent=4, sort_keys=False)
        self.reset_variables()
        return data

    def reset_variables(self):
        self.path = ''
        self.activeframename = ''
        self.store_object = []
        self.previous_path = ''
        self.path_generator_free = True

    def keyboard_event(self,ch):
        if len(self.store_object) == 0:
            return 
        value = self.store_object[-1]['value']
        if str(ch) != '\b':
            value = value + str(ch)
        else:
            if len(value) > 0:
                value = value[:-1]
        self.store_object[-1]['value'] = value

    def edit_text_value(self,obj):
        current_acc_info = obj._get__JABAccContextInfo()
        if current_acc_info.accessibleText == 1:
            charinfo = obj.jabContext.getAccessibleTextInfo(0,1)
            text = obj.jabContext.getAccessibleTextRange(0,charinfo.charCount - 1)
            text = text.strip()
            text = str(text)
            text = text.strip()
            text = text.replace('<','')
            text = text.replace('>','')
        else:
            text = ''
        if len(self.store_object) > 0 and text != self.store_object[-1]['text']:
            self.store_object[-1]['text'] = text 

    def set_window_name(self,window_name=''):
        self.window_name = window_name 

    def path_for_page_tab(self,obj):
        """
            This method will iterate through the children of page tab list. If status is
            focused and selected,object of jabContext (page tab) is returned.
        """
        try:
            parent_obj = obj._get_parent()
            child_count = parent_obj._get_childCount()
            found , index = False , 0
            while not found and index < child_count:
                child = parent_obj.jabContext.getAccessibleChildFromContext(index)
                child_info = child.getAccessibleContextInfo()
                if "selected" in child_info.states:
                    found = True
                index += 1
        except Exception as e:
            log.debug(e)
        return child


    def path_for_tool_bar(self,obj):
        try:
            parent_obj = obj._get_parent()
            child_count = obj._get_childCount()
            found , index = False , 0
            all_child = {}
            while index < child_count:
                child = obj.jabContext.getAccessibleChildFromContext(index)
                child_info = child.getAccessibleContextInfo()
                x=child_info.x
                y=child_info.y
                w=child_info.width
                h=child_info.height
                size = str(x)+','+str(y)+','+str(w)+','+str(h)
                all_child[size]=child
                index += 1
        except Exception as e:
            log.debug(e)
        return all_child

    def get_combo_box_text(self,obj,delay=2):
        '''
            input_args : obj -> accessible context of combo box , delay (default 2s) -> wait for 2s before getting the selection item in the combo box.
            returns : This method returns the selected items name of the combo box. If nothing is selected it returns ''. 
        '''
        try:
            time.sleep(delay)
            index = 0
            child_name = '' 
            list_jabContext = self.looptolist(obj.jabContext)
            if list_jabContext:
                list_acc_info = list_jabContext.getAccessibleContextInfo()
                child_count = list_acc_info.childrenCount
                while index < child_count:
                    child = list_jabContext.getAccessibleChildFromContext(index)
                    child_info = child.getAccessibleContextInfo()
                    child_name = child_info.name
                    if "selected" in child_info.states:
                        break
                    index += 1
        except Exception as e:
            log.debug(e)
        return child_name

    def looptolist(self,acc):
        charinfo = acc.getAccessibleContextInfo()
        if charinfo.role == 'list':
            return acc
        for i in range(charinfo.childrenCount):
            childacc = acc.getAccessibleChildFromContext(i)
            return self.looptolist(childacc)
        return ''

    def edit_combo_text(self,obj):
        try:
            text = self.get_combo_box_text(obj)
            if len(self.store_object) > 0 and text != self.store_object[-1]['text']:
                self.store_object[-1]['text'] = text
        except Exception as e:
            log.debug(e)
        




