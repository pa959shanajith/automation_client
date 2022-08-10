import wx
import __main__
import logging
log = logging.getLogger('loadingwindow.py')

class Loading_window(wx.Frame):
    """Initialization and defining the wx-components of the pop-up"""
    def __init__(self, parent):
        try:
            wx.Frame.__init__(self, parent=None, size=(250,100),title = 'Initializing Avo Assure Client', style = wx.CAPTION & ~ (wx.SYSTEM_MENU|wx.FRAME_TOOL_WINDOW))
            self.SetBackgroundColour('#e6e7e8')
            # font.SetPointSize(9)
            panel = wx.Panel(self)
            host_url_label = wx.StaticText(panel,-1, label='Please wait ...',pos =(20, 20))
            self.Centre()
            self.Show()
            self.Update()
        except Exception as e:
            log.error("Error occured in Token Registration. Err msg: " + str(e))




