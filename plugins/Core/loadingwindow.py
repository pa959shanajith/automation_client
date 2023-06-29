import wx
import logging
log = logging.getLogger('loadingwindow.py')

class Loading_window(wx.Frame):
    """Initialization and defining the wx-components of the pop-up"""
    def __init__(self, parent, args):
        try:
            if args.instanceid:
                wx.Frame.__init__(self, parent=None, size=(400,150),title = 'Avo Assure Client', style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX))
            else:    
                wx.Frame.__init__(self, parent=None, size=(400,150),title = 'Initializing Avo Assure Client', style = wx.CAPTION & ~ (wx.SYSTEM_MENU|wx.FRAME_TOOL_WINDOW))
            self.SetBackgroundColour('#e6e7e8')
            # font.SetPointSize(9)
            panel = wx.Panel(self)
            if args.instanceid:
                Running_Instance = args.agentname+'_'+args.instanceid
                host_url_label = wx.StaticText(panel,-1, label = 'Running Instance_:'+ Running_Instance ,pos =(40,40))
            else:
                host_url_label = wx.StaticText(panel,-1, label='Please wait ...',pos =(40,40))
            self.Centre()
            self.Show()
            self.Update()
        except Exception as e:
            log.error("Error occured in Loading_window. Err msg: " + str(e))




