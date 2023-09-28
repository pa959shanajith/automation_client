#-------------------------------------------------------------------------------
# Name:        icetoken
# Purpose:
#
# Author:      sushma.p
#
# Created:     05-06-2020
# Copyright:   (c) sushma.p 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import wx
import sys
import json
import codecs
import logging
from uuid import uuid4 as uuid
from core_utils import CoreUtils
import logger
log = logging.getLogger('icetoken.py')

import readconfig
configvalues = readconfig.readConfig().readJson()
ICE_Token = configvalues.get('Ice_Token')

class ICEToken():
    def __init__(self):
        self.token = None
        self.tokenwindow = None
        self.enc_obj = CoreUtils()
        self.check_token()

    """ Check for the Avo Assure Client token. If exists, returns decrypted token """
    def check_token(self):
        self.token_folder=self.get_token_folder()
        self.tokenid_file=os.environ["AVO_ASSURE_HOME"] + os.sep + "lib" + os.sep + "METADATA"
        self.token_file=self.token_folder+os.sep+self.get_token_id()+".enc"
        if os.path.exists(self.token_file):
            log.debug("Token exists")
            """ Decrypt the token with token key """
            token_key = "".join(['a','s','i','d','f','n','H','T','E','o','w','#','D','j',
                        'g','L','I','$','o','K','n','^','8','s','j','p','2','h','9','Y','&','d'])
            with open(self.token_file, "r") as f:
                token=f.read()
            if token != "":
                try:
                    self.token=json.loads(self.enc_obj.unwrap(token,token_key))
                except: pass
        return self.token

    """ Registration window for token """
    def token_window(self,parent,images_path):
        self.tokenwindow=Token_window(parent = parent, id = -1, title="Avo Assure Client Registration",images_path=images_path)

    """ Registration window for token """
    def kill_window(self):
        if self.tokenwindow:
            self.tokenwindow.Destroy()
        self.tokenwindow = None

    """ Save the encrypted token in the localappdata folder """
    def save_token(self, token):
        if not os.path.exists(self.token_folder):
            os.makedirs(self.token_folder)
        """ Encrypt the token with token key"""
        token_key = "".join(['a','s','i','d','f','n','H','T','E','o','w','#','D','j',
                        'g','L','I','$','o','K','n','^','8','s','j','p','2','h','9','Y','&','d'])
        token = self.enc_obj.wrap(json.dumps(token),token_key)
        with open(self.token_file, "w") as f:
            f.write(token.decode("utf-8"))

    """ Deletes the token in the appdatafolder """
    def delete_token(self):
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
        self.token=None

    """ Returns the appdatafolder based on the platform """
    def get_token_folder(self):
        token_folder=None
        if sys.platform=="win32":
            token_folder=os.getenv("LOCALAPPDATA")+os.sep+"AvoAssure"
        elif sys.platform.lower()=="darwin" or sys.platform.lower()=='linux':
            token_folder=os.environ['HOME']+os.sep+".Local"+os.sep+"AvoAssure"
        else:
            print(sys.platform+" platform yet to be supported")
        return token_folder

    """ Returns the tokenid to get token from appdatafolder """
    def get_token_id(self):
        token_id = '-'
        if os.path.exists(self.tokenid_file):
            with open(self.tokenid_file, 'rb') as f:
                try:
                    token_id = codecs.decode(f.read(), 'hex').decode('utf-8')
                except Exception as e:
                    print(e)
                    pass
        if token_id == '-':
            token_id = str(uuid())
            with open(self.tokenid_file, 'wb') as f:
                f.write(codecs.encode(token_id.encode('utf-8'), 'hex'))
                f.close()
        return token_id

class Token_window(wx.Frame):
    """Initialization and defining the wx-components of the pop-up"""
    def __init__(self, parent, id, title,images_path=None):
        try:
            self.parent=parent
            self.ICE_Token = self.parent.Ice_Token

            # SN Adiga 07-Aug-2022: Show both URL and Token during registration window display
            # Name : A Sreenivasulu Date : 05/08/2022 ICE_token frame properties will change depend on token existens,token comes from config.json
            #if self.ICE_Token:
            #    wx.Frame.__init__(self, parent=None, title=title, pos=(300, 150), size=(420,170), style = wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX))
            #else:
            #    wx.Frame.__init__(self, parent=None, title=title, pos=(300, 150), size=(420,210), style = wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX))
            
            wx.Frame.__init__(self, parent=None, title=title, pos=(300, 150), size=(420,210), style = wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX))
            
            # End - SNA

            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = images_path +"avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            self.panel = wx.Panel(self)
            self.host_url_label = wx.StaticText((self.panel), label='Host URL', pos=(35,35), style=0, name='')
            self.url = wx.TextCtrl((self.panel), pos=(108, 30), size=(250, 28))
            
            # SN Adiga 07-Aug-2022: Show both URL and Token during registration window display
            #if self.ICE_Token:
            #    self.submit_btn=wx.Button(self.panel, label="Submit", pos=(200, 70), size=(65,26))
            #else:
            # End SNA

            self.token_label = wx.StaticText((self.panel), label='Token', pos=(40,80), style=0, name='')
            #self.tok_name=wx.StaticText(self.panel, label="Register", pos=(70,10),size=(70,20), style=0, name="")
            self.token_name = wx.TextCtrl((self.panel), pos=(108, 75), size=(250, 28))
            self.submit_btn=wx.Button(self.panel, label="Submit", pos=(200, 115), size=(65,26))
            
            #self.url=wx.TextCtrl(self.panel, pos=(10,35), size=((175,28)))
            #self.token_name=wx.TextCtrl(self.panel, pos=(10,70), size=((175,28)))
            self.submit_btn.Bind(wx.EVT_BUTTON, self.submit_token)
            self.url.SetValue('server-ip:port')
            if self.parent.server_url.strip() != ':':
                self.url.SetValue(self.parent.server_url)
            self.token_name.SetValue(self.ICE_Token)
            self.Centre()
            self.Bind(wx.EVT_CLOSE, self.close)
            wx.Frame(self.panel)
            # SN Adiga 07-Aug-2022: Show registration window if auto registration failure
            # A sreenivasulu , auto registration is required for servicelevel = 2(means trinee registration)
            # licenectype = 1(means trial), 2(means trinee), 3(starter),4(enterprise)
            if configvalues.get('isTrial') or configvalues.get("servicelevel") == 2:
                res = self.auto_registration()
                if (res == False) or (res == None):
                    self.Show()
            else:
                self.Show()

        except Exception as e:
            logger.print_on_console("Error occured in Token Registration")
            log.error("Error occured in Token Registration. Err msg: " + str(e))

    def submit_token(self, event):
        url = self.url.GetValue().strip()
        # A Sreenivasulu Date:03/08/2022 this condistion is adding https protocal to URL if protocal not exit 
        if url[0:7].lower() == 'http://':
            url = url[7:]
        if url[0:8].lower() == 'https://':
            url = url[8:]
        token = self.token_name.GetValue().strip()
        self.parent.server_url = url
        self.parent.register(token)
        self.parent.token_obj.kill_window()

    def close(self, event):
        self.parent.cw.connectbutton.Enable()
        self.parent.token_obj.kill_window()    
        
    # Name:A sreenivasulu Date: 3/08/2022
    # below two functions responsible for auto registration{auto_submit() and auto_registration()} 
    def auto_submit(self,url,token):
        if url[0:7].lower() == 'http://':
            url = url[7:]
        if url[0:8].lower() == 'https://':
            url = url[8:]
        self.parent.server_url = url
        res = self.parent.register(token)
        self.parent.token_obj.kill_window()
        return res

    def auto_registration(self):
        try:
            avo_url = configvalues['server_ip']+':'+configvalues['server_port']
            token = self.ICE_Token
            if avo_url:
                # calling for registration
                res = self.auto_submit(avo_url,token)
                return res
            else:
                logger.print_on_console('file not found')
                return False
        except Exception as ex:
            logger.print_on_console(ex)
            return False


