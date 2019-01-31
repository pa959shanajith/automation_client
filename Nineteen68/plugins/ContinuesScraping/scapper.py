import wx
import sys
import os
from selenium import webdriver
import browserops
import clickandadd
import fullscrape



browserobj = browserops.BrowserOperations()
clickandaddoj = clickandadd.Clickandadd()
fullscrapeobj = fullscrape.Fullscrape()
class ScrapeWindow(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(280, 350) ,style = wx.CAPTION|wx.CLIP_CHILDREN )
        self.SetBackgroundColour(   (245,222,179))
        curdir = os.getcwd()
        browser=input("""Enter the browser name to  open : IE - Internet Explorer, CH - Google Chrome, FX - Mozilla Firefox:\n""")
        if browser == 'IE' or browser == 'CH' or browser == 'FX':
            browserobj.openBrowser(browser)
        else:
            log.info('Invalid browser entered')

        driver = browserops.driver
        self.iconpath = curdir + "\\slk.ico"
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 5)
        self.icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap(self.iconpath))
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.sizer.Add(self.icon, pos=(0, 3), flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT,
                       border=5)
        self.screenname = ''
        self.modulename = ''
        self.depscreens = []
        self.depmodules = []
        box = wx.BoxSizer(wx.VERTICAL)
        self.modulenames = ['WebBanking','MobileBanking','PapaerBanking']

        self.modulescreens= {'WebBanking' : ['WebLogin','WebPayment','WebTranzaction','WebLogout'],
                             'MobileBanking' : ['MobileLogin','MobilePayment','MobileTranzaction','MobileLogout'],
                             'PapaerBanking' : ['PaperLogin','PaperPayment','PaperTranzaction','PaperLogout']

                            }

        self.screennames = []
        self.scrapecount = 0

        self.chlbl1 = wx.StaticText(self.panel,label = "Select the module name: ",pos=(12, 8), size=(175, 28))
        self.choice1 = wx.Choice(self.panel,choices = self.modulenames,pos=(12, 38), size=(175, 28))
        box.Add(self.choice1,1,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)
        box.AddStretchSpacer()
        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoiceModule)
        self.choice1.SetToolTip(wx.ToolTip("Select the module name"))



        self.chlbl2 = wx.StaticText(self.panel,label = "Select the screen name: ",pos=(12, 68), size=(175, 28))
        self.choice2 = wx.Choice(self.panel,choices = self.screennames,pos=(12, 98), size=(175, 28))
        box.Add(self.choice2,1,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)
        box.AddStretchSpacer()
        self.choice2.Bind(wx.EVT_CHOICE, self.OnChoiceScreen)
        self.choice2.SetToolTip(wx.ToolTip("Select the screen name"))


        self.startbutton = wx.Button(self.panel, label="Start ClickAndAdd",pos=(12, 128), size=(175, 28))
        self.startbutton.Bind(wx.EVT_BUTTON, self.startcliclandadd)   # need to implement OnExtract()
        self.startbutton.SetToolTip(wx.ToolTip("To START Click and Add Scraping"))
        self.stopbutton = wx.Button(self.panel, label="Stop ClickAndAdd", pos=(12, 158), size=(175, 28))
        self.stopbutton.Bind(wx.EVT_BUTTON, self.stopcliclandadd)   # need to implement OnExtract()
        self.stopbutton.SetToolTip(wx.ToolTip("To STOP Click and Add Scraping"))
        self.stopbutton.Disable()
        self.fullscrapebutton = wx.Button(self.panel, label="Full Scrape",pos=(12, 198), size=(175, 28))
        self.fullscrapebutton.Bind(wx.EVT_BUTTON, self.fullscrape)   # need to implement OnExtract()
        self.fullscrapebutton.SetToolTip(wx.ToolTip("To perform FULLSCRAPE Scraping"))
        self.savescrapebutton = wx.Button(self.panel, label="Save Scrape",pos=(12, 228), size=(175, 28))
        self.savescrapebutton.Bind(wx.EVT_BUTTON, self.savescrape)   # need to implement OnExtract()
        self.savescrapebutton.SetToolTip(wx.ToolTip("To save SCRAPE data"))
        self.savescrapebutton.Disable()
##        self.cancelbutton = wx.Button(self.panel, label="Exit" ,pos=(12, 258), size=(175, 28))
##        self.cancelbutton.Bind(wx.EVT_BUTTON, self.OnExit)   # need to implement OnExit(). Leave notrace
##        self.cancelbutton.SetToolTip(wx.ToolTip("To exit and close the browser"))
        self.label1 = wx.StaticText(self.panel,label = "@ 2016 SLK Software Services Pvt. Ltd.",pos=(12, 268), size=(220, 28))
        self.label1 = wx.StaticText(self.panel,label =" All Rights Reserved. Patent Pending",pos=(12, 298), size=(220, 28))

        self.sizer.AddGrowableCol(2)
        self.panel.SetSizer(self.sizer)
        self.Centre()
        style = self.GetWindowStyle()
        self.SetWindowStyle( style|wx.STAY_ON_TOP )
        wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Show()



    #----------------------------------------------------------------------
    def OnExit(self, event):
        self.Close()
        driver = browserops.driver
        driver.close()

    #----------------------------------------------------------------------
    def stopcliclandadd(self,event):
        self.stopbutton.Disable()
        self.screenname =  self.choice2.GetString(self.choice2.GetSelection())
        self.modulename =  self.choice1.GetString(self.choice1.GetSelection())

        self.screenname = self.modulename + '##' +self.screenname
        self.depscreens.append(self.screenname)
        if self.scrapecount == 0:
            k = []
            fullscrapeobj.stopclickandadd(self.screenname,k)
        else:
            depscreen = self.depscreens[0:(len(self.depscreens) - 1)]
            fullscrapeobj.stopclickandadd(self.screenname,depscreen)
        self.scrapecount = self.scrapecount + 1
        self.startbutton.Enable()
        self.fullscrapebutton.Enable()
        self.savescrapebutton.Enable()
        log.info('Stopped click and add')

    #----------------------------------------------------------------------
    def startcliclandadd(self,event):
        self.startbutton.Disable()
        self.modulename =  self.choice1.GetString(self.choice1.GetSelection())
        if self.modulename == '':
            wx.MessageBox('Please select the module name', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.startbutton.Enable()
            return
        self.screenname =  self.choice2.GetString(self.choice2.GetSelection())
        if self.screenname == '':
            wx.MessageBox('Please select the screen name', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.startbutton.Enable()
            return
        fullscrapeobj.startclickandadd()
        self.stopbutton.Enable()
        self.fullscrapebutton.Disable()
        self.savescrapebutton.Disable()
        log.info('click and add initiated, select the elements from AUT')

    #----------------------------------------------------------------------
    def fullscrape(self,event):
        log.info('Performing full scrape')
        self.startbutton.Disable()
        self.modulename =  self.choice1.GetString(self.choice1.GetSelection())
        self.screenname =  self.choice2.GetString(self.choice2.GetSelection())
        self.screenname = self.modulename + '##' +self.screenname
        self.depscreens.append( self.screenname)
        if self.modulename == '':
            wx.MessageBox('Please select the module name', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.fullscrapebutton.Enable()
            return
        self.screenname =  self.choice2.GetString(self.choice2.GetSelection())
        if self.screenname == '':
            wx.MessageBox('Please select the screen name', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.fullscrapebutton.Enable()
            return
        self.screenname =  self.modulename + '##' + self.screenname
        if self.scrapecount == 0:
            k = []
            fullscrapeobj.fullscrape(self.screenname,k)
        else:
            depscreen = self.depscreens[0:(len(self.depscreens) - 1)]
            fullscrapeobj.fullscrape(self.screenname,depscreen)
        self.scrapecount = self.scrapecount + 1
        self.startbutton.Enable()
        self.savescrapebutton.Enable()
        log.info('Full scrape  completed')

    #----------------------------------------------------------------------
    def savescrape(self,event):
        log.info('Saving scraped data')
        data = clickandadd.vie
        if len(data) > 0:
            fullscrapeobj.save_json_data()
        else:
            fullscrapeobj.save_json_data()
        self.Close()
        driver = browserops.driver
        driver.close()
        log.info('Scrapped data saved successfully in domelements.json file')

    #----------------------------------------------------------------------
    def OnChoiceScreen(self,event):
        self.screenname =  self.choice2.GetString(self.choice2.GetSelection())
        log.info("You selected "+ self.screenname +" from screen selection")

    #----------------------------------------------------------------------
    def OnChoiceModule(self,event):
        self.modulename =  self.choice1.GetString(self.choice1.GetSelection())
        self.screennames = self.modulescreens[self.modulename]
        self.choice2.SetItems(self.screennames)
        log.info("You selected "+ self.modulename +" from module selection")

#----------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App()
    ScrapeWindow(None, title="SLK Nineteen68 - Continues Scrapper")
    app.MainLoop()
