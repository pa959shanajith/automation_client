#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     17-02-2017
# Copyright:   (c) rakesh.v 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_scraping
import wx
##import clientwindow
from socketIO_client import SocketIO,BaseNamespace
import launch_keywords
desktop_scraping_obj = desktop_scraping.Scrape()
import os
from constants import *
import logger

obj=None
class ScrapeWindow(wx.Frame):
    def __init__(self, parent,id, title,filePath,socketIO):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 150) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour(   (245,222,179))
        curdir = os.getcwd()
        global obj
        obj = launch_keywords.Launch_Keywords()
        self.socketIO = socketIO
        fileLoc=filePath.split(';')[0]
        windowname=filePath.split(';')[1]
        input_val=[]
        input_val.append(fileLoc)
        input_val.append(windowname)
        input_val.append(5)
        status = obj.launch_application(input_val)
        print status
        if status!=TERMINATE:
            self.panel = wx.Panel(self)
    ##            self.sizer = wx.GridBagSizer(6, 5)
    ##            self.icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap(self.iconpath))
    ##            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
    ##            self.SetIcon(self.wicon)
    ##            self.sizer.Add(self.icon, pos=(0, 3), flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT,border=5)

    ##            self.tbtn = wx.ToggleButton(panel , -1, "click to on")
    ##            vbox.Add(self.tbtn,0,wx.EXPAND|wx.ALIGN_CENTER)
    ##            self.tbtn.Bind(wx.EVT_TOGGLEBUTTON,self.OnToggle)

            self.startbutton = wx.ToggleButton(self.panel, label="Start ClickAndAdd",pos=(12,8 ), size=(175, 28))
            self.startbutton.Bind(wx.EVT_TOGGLEBUTTON, self.clickandadd)   # need to implement OnExtract()
    ##            self.startbutton.SetToolTip(wx.ToolTip("To START Click and Add Scraping"))
    ##            self.startbutton.Show()
    ##            self.stopbutton = wx.Button(self.panel, label="Stop ClickAndAdd", pos=(12,8 ), size=(175, 28))
    ##            self.stopbutton.Bind(wx.EVT_BUTTON, self.stopcliclandadd)   # need to implement OnExtract()
    ##            self.stopbutton.SetToolTip(wx.ToolTip("To STOP Click and Add Scraping"))
    ##            self.stopbutton.Hide()
            self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12,38 ), size=(175, 28))
            self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()

    ##            self.fullscrapebutton.SetToolTip(wx.ToolTip("To perform FULLSCRAPE Scraping"))
    ##        self.comparebutton = wx.ToggleButton(self.panel, label="Compare",pos=(12,68 ), size=(175, 28))
    ##        self.comparebutton.Bind(wx.EVT_TOGGLEBUTTON, self.compare)   # need to implement OnExtract()
    ##            self.savescrapebutton.SetToolTip(wx.ToolTip("To save SCRAPE data"))
    ##            self.savescrapebutton.Disable()
    ##            self.label1 = wx.StaticText(self.panel,label = "@ 2017 SLK Software Services Pvt. Ltd.",pos=(12,128 ), size=(220, 28))
    ##            self.label1 = wx.StaticText(self.panel,label =" All Rights Reserved. Patent Pending",pos=(12,158 ), size=(220, 28))

    ##            self.sizer.AddGrowableCol(2)
    ##            self.panel.SetSizer(self.sizer)
            self.Centre()
    ##        status = obj.launch_application(input_val)
    ##        print 'After call'

            self.Centre()
            style = self.GetWindowStyle()
            self.SetWindowStyle( style|wx.STAY_ON_TOP )
            wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            self.Show()
        else:

            self.socketIO.emit('scrape','Fail')


     #----------------------------------------------------------------------
##    def OnExit(self, event):
##        self.Close()
##        driver = browserops.driver
##        driver.close()

    #----------------------------------------------------------------------
    def clickandadd(self,event):
        state = event.GetEventObject().GetValue()
        if state == True:
            self.fullscrapebutton.Disable()
##        self.comparebutton.Disable()
            desktop_scraping_obj.clickandadd('STARTCLICKANDADD')
            event.GetEventObject().SetLabel("Stop ClickAndAdd")
##            wx.MessageBox('CLICKANDADD: Select the elements using Mouse - Left Click', 'Info',wx.OK | wx.ICON_INFORMATION)
            logger.print_on_console( 'click and add initiated, select the elements from AUT')

        else:
            d = desktop_scraping_obj.clickandadd('STOPCLICKANDADD')
            event.GetEventObject().SetLabel("Start ClickAndAdd")


##            print desktop_scraping.finalJson
            logger.print_on_console('Stopped click and add')
            logger.print_on_console( 'Scrapped data saved successfully in domelements.json file')
            self.socketIO.emit('scrape',d)
##            wx.MessageBox('CLICKANDADD: Scrape completed', 'Info',wx.OK | wx.ICON_INFORMATION)
            self.Close()
##            event.GetEventObject().SetLabel("Start ClickAndAdd")
            logger.print_on_console('Click and add scrape  completed')


##    def compare(self,event):
##        state = event.GetEventObject().GetValue()
##        if state == True:
##            self.fullscrapebutton.Disable()
##            self.startbutton.Disable()
##            obj = objectspy.Object_Mapper()
##            obj.compare()
##            event.GetEventObject().SetLabel("Update")
##        else:
##            obj = objectspy.Object_Mapper()
##            d = obj.update()
##            self.socketIO.send(d)
##            self.Close()


    #----------------------------------------------------------------------
    def fullscrape(self,event):
        logger.print_on_console('Performing full scrape')
        self.startbutton.Disable()
##        print 'desktop_scraping_obj:',desktop_scraping_obj
####        self.comparebutton.Disable()
        d = desktop_scraping_obj.full_scrape()
        self.socketIO.emit('scrape',d)
        self.Close()
        logger.print_on_console('Full scrape  completed')



