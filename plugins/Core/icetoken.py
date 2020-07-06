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
import sys
from core_utils import CoreUtils
import wx
import logging
import logger
import json

log = logging.getLogger('icetoken.py')

class ICEToken():
    def __init__(self):
        self.token = None
        self.tokenwindow = None
        self.enc_obj = CoreUtils()
        self.check_token()

    """ Check for the ICE token. If exists, returns decrypted token """
    def check_token(self):
        self.token_folder=self.get_token_folder()
        self.token_file=self.token_folder+os.sep+"token.enc"
        if os.path.exists(self.token_file):
            log.info("Token exists")
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
        self.tokenwindow=Token_window(parent = parent, id = -1, title="Nineteen68 Registration",images_path=images_path)

    """ Registration window for token """
    def kill_window(self):
        if self.tokenwindow:
            self.tokenwindow.Destroy()

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
            token_folder=os.getenv("LOCALAPPDATA")+os.sep+"Nineteen68"
        elif sys.platform.lower()=="darwin":
            token_folder=os.environ['HOME']+os.sep+".Local"+os.sep+"Nineteen68"
        else:
            print(sys.platform+" platform yet to be supported")
        return token_folder

class Token_window(wx.Frame):
    """Initialization and defining the wx-components of the pop-up"""
    def __init__(self, parent, id, title,images_path=None):
        try:
            wx.Frame.__init__(self, parent=None, title=title, pos=(300, 150), size=(210, 180), style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  |wx.MAXIMIZE_BOX | wx.CLOSE_BOX))
            self.SetBackgroundColour('#e6e7e8')
            self.parent=parent
            self.iconpath = images_path +"slk.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            self.panel = wx.Panel(self)
            self.tok_name=wx.StaticText(self.panel, label="Register", pos=(70,10),size=(70,20), style=0, name="")
            self.url=wx.TextCtrl(self.panel, pos=(10,35), size=((175,28)))
            self.token_name=wx.TextCtrl(self.panel, pos=(10,70), size=((175,28)))
            self.submit_btn=wx.Button(self.panel, label="Submit",pos=(60,110), size=(60,28))
            self.submit_btn.Bind(wx.EVT_BUTTON, self.submit_token)
            self.url.SetValue('server-ip:port')
            if self.parent.server_url.strip() != ':':
                self.url.SetValue(self.parent.server_url)
            self.token_name.SetValue('Token')
            self.Centre()
            wx.Frame(self.panel)
            self.Show()
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.print_on_console("Error occured in Token Registration")
            log.error("Error occured in Token Registration. Err msg: " + str(e))

    def submit_token(self, event):
        url = self.url.GetValue().strip()
        token = self.token_name.GetValue().strip()
        self.parent.server_url = url
        self.parent.register(token)
        self.Destroy()
