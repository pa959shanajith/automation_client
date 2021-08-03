#-------------------------------------------------------------------------------
# Name:        pdf
# Purpose:	   PDF utility to perform actions on PDF files
#
# Author:      shree.p
#
# Created:
# Copyright:   (c) shree.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import logging

import sys
import os
import fitz
import wx
import wx.lib.sized_controls as sc
from pdflib_custom import pdfViewer, pdfButtonPanel
import wx.lib.buttons as btn
from constants import IMAGES_PATH, TEMP_PATH
from PIL import ImageGrab
import win32gui

pageToFind = ''
hopIndex = 1
siblingElementArr = []
eleList = []
counter = 0
founf = ''
log = logging.getLogger("pdf_main.py")
class PDF():
    def OnInit(self):
        pdfV = PDFViewer(None, title="PDF Window", size=(615,850))
        pdfV.Show()

class Rect():
    def __init__(self, *args):
        if not args:
            self.x0 = self.y0 = self.x1 = self.y1 = self.width= self.height =0.0
            return None

        if len(args) == 4:
            self.x0 = args[0]
            self.y0 = args[1]
            self.x1 = args[2]
            self.y1 = args[3]
            self.width = args[4]
            self.height = args[5]
            return None


class PDFViewer(sc.SizedFrame):
    def __init__(self, parent, **kwds):
        try:
            super(PDFViewer, self).__init__(parent, **kwds)
            global eleList
            eleList = []
            # Adding avo icon to window
            self.iconpath = IMAGES_PATH+"avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)

            paneCont = self.GetContentsPane()
            paneCont.SetSizerType("vertical")
            paneCont.SetBackgroundColour("#350066")
            hsizer = wx.BoxSizer( wx.HORIZONTAL)
            vsizer = wx.BoxSizer( wx.VERTICAL)
            self.loadbutton = wx.Button(paneCont, wx.ID_ANY, "Load PDF file", wx.DefaultPosition, wx.DefaultSize, 0 )
            operations = ['Sibling Element', 'PDF Image']
            self.combobox = wx.ComboBox(paneCont,wx.ID_ANY,"Select Action",wx.DefaultPosition,wx.DefaultSize,operations ,0)
            size = '4'
##            self.startbutton = btn.GenBitmapButton(paneCont,wx.ID_ANY,bitmap=wx.Bitmap("./images/toolbarButton-actionStart.png"),style=wx.NO_BORDER|wx.BU_EXACTFIT)
##            self.stopbutton = btn.GenBitmapButton(paneCont,wx.ID_ANY,bitmap=wx.Bitmap("./images/toolbarButton-actionStop.png"),style=wx.NO_BORDER|wx.BU_EXACTFIT)
            self.findbar_right = btn.GenBitmapButton(paneCont,wx.ID_ANY,bitmap=wx.Bitmap(IMAGES_PATH+"findbarButton-nextSibling.png"),style=wx.NO_BORDER|wx.BU_EXACTFIT)
            self.findbar_left = btn.GenBitmapButton(paneCont,wx.ID_ANY,bitmap=wx.Bitmap(IMAGES_PATH+"findbarButton-nextSibling-rtl.png"),style=wx.NO_BORDER|wx.BU_EXACTFIT)
            self.forwardbutton = btn.GenBitmapButton(paneCont,wx.ID_ANY,bitmap=wx.Bitmap(IMAGES_PATH+"findbarButton-next.png"),style=wx.NO_BORDER|wx.BU_EXACTFIT)
            self.backwardbutton = btn.GenBitmapButton(paneCont,wx.ID_ANY,bitmap=wx.Bitmap(IMAGES_PATH+"findbarButton-next-rtl.png"),style=wx.NO_BORDER|wx.BU_EXACTFIT)
            self.search = wx.SearchCtrl(paneCont, size=(150,-1), style=wx.TE_PROCESS_ENTER)

##            self.startbutton.SetToolTip(wx.ToolTip("Action Start"))
##            self.startbutton.SetForegroundColour(wx.RED)
##            self.startbutton.Disable()
##            self.stopbutton.SetToolTip(wx.ToolTip("Action Stop"))
##            self.stopbutton.Disable()
            self.search.SetToolTip(wx.ToolTip("Find in document"))
            self.search.Disable()
            self.combobox.SetToolTip(wx.ToolTip("Action"))
            self.combobox.Disable()
            self.findbar_right.SetToolTip(wx.ToolTip("Find the next sibling"))
            self.findbar_right.Disable()
            self.findbar_left.SetToolTip(wx.ToolTip("Find the previous sibling"))
            self.findbar_left.Disable()
            self.forwardbutton.SetToolTip(wx.ToolTip("Find the next occurrence"))
            self.forwardbutton.Disable()
            self.backwardbutton.SetToolTip(wx.ToolTip("Find the previuos occurrence"))
            self.backwardbutton.Disable()


            # Setup the layout
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(self.search, 0, wx.ALL, 15)

##            self.startbutton.SetInitialSize
            hsizer.Add(self.loadbutton, 0, wx.ALIGN_CENTER|wx.ALL, 2)
            hsizer.Add(self.combobox, 0, wx.ALIGN_CENTER|wx.ALL, 2)
##            hsizer.Add(self.startbutton, 0, wx.ALIGN_CENTER|wx.ALL, 2)
##            hsizer.Add(self.stopbutton, 0, wx.ALIGN_CENTER|wx.ALL, 2)
            hsizer.Add(self.search, 0, wx.ALIGN_CENTER|wx.ALL, 2)
            hsizer.Add(self.findbar_right, 0 , wx.ALIGN_CENTER | wx.ALL, 2)
            hsizer.Add(self.findbar_left, 0 , wx.ALIGN_CENTER | wx.ALL, 2)
            hsizer.Add(self.forwardbutton, 0 , wx.ALIGN_CENTER | wx.ALL, 2)
            hsizer.Add(self.backwardbutton, 0 , wx.ALIGN_CENTER | wx.ALL, 2)

            vsizer.Add(hsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
            paneCont.SetSizer(vsizer)

            paneCont.Bind(wx.EVT_BUTTON, self.OnLoadButton, self.loadbutton)
            paneCont.Bind(wx.EVT_COMBOBOX, self.OnSelect,self.combobox)
##            paneCont.Bind(wx.EVT_BUTTON, self.OnStart,self.startbutton)
##            paneCont.Bind(wx.EVT_BUTTON, self.OnStop,self.stopbutton)
            paneCont.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch,self.search)
            paneCont.Bind(wx.EVT_BUTTON, self.OnHopRight,self.findbar_right)
            paneCont.Bind(wx.EVT_BUTTON, self.OnHopLeft,self.findbar_left)
            paneCont.Bind(wx.EVT_BUTTON, self.OnForward,self.forwardbutton)
            paneCont.Bind(wx.EVT_BUTTON, self.OnBackward,self.backwardbutton)

            self.buttonpanel = pdfButtonPanel(paneCont, wx.ID_ANY,
                                    wx.DefaultPosition, wx.DefaultSize, 0)
            self.buttonpanel.SetSizerProps(expand=True)
            self.viewer = pdfViewer(paneCont, wx.ID_ANY, wx.DefaultPosition,
                                    wx.DefaultSize,
                                    wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)

            self.viewer.SetSizerProps(expand=True, proportion=1)

            # introduce buttonpanel and viewer to each other
            self.buttonpanel.viewer = self.viewer
            self.viewer.buttonpanel = self.buttonpanel
            siblingElementArr = []
        except Exception as e :
            logger.print_on_console('Error at pdf viewer')
            log.error(e)

    def OnLoadButton(self,event):
        global eleList
        global siblingElementArr
        siblingElementArr = []
        eleList = []

        dlg = wx.FileDialog(self.loadbutton,wildcard="*.pdf")
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            pdfFilePath = dlg.GetPath()
            self.viewer.LoadFile(dlg.GetPath())
            self.OpenDoc(dlg.GetPath())
            self.combobox.Enable()
            self.viewer.SetZoom(-2)
            wx.EndBusyCursor()
        dlg.Destroy()

    def OpenDoc(self,pdfFilePath):
        if pdfFilePath != None and pdfFilePath != '':
            global doc
            doc = fitz.open(pdfFilePath)

    def OnSelect(self,event):
        selectop = self.combobox.Value

        if selectop == 'Sibling Element':
    ##        self.startbutton.Enable()
    ##        self.stopbutton.Enable()
            self.search.Enable()
            currentpage = self.viewer.buttonpanel
            self.OnResize()
        elif selectop == 'PDF Image':
##            self.Freeze()
##            self.Thaw()
            import time
            time.sleep(0.5)
            self.c1 = None
            self.c2 = None
            try:
                self.viewer.Bind(wx.EVT_MOTION, self.OnMouseMove)
                self.viewer.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
                self.viewer.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
                self.viewer.Bind(wx.EVT_PAINT, self.OnPaint)
                self.viewer.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
            except Exception as e :
                logger.print_on_console('Error at pdf image in onselect')
                log.error(e)


    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.c2 = event.GetPosition()
            self.Refresh()

    def OnMouseDown(self, event):
        self.c1 = event.GetPosition()

    def OnMouseUp(self, event):
        self.viewer.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.viewer.Unbind(wx.EVT_MOTION)
        self.viewer.Unbind(wx.EVT_LEFT_DOWN)
        self.viewer.Unbind(wx.EVT_LEFT_UP)
        self.viewer.Unbind(wx.EVT_PAINT)
        global pageToFind
        global siblingElementArr
        try:
            currentpage = self.viewer.buttonpanel.pageno
            pageToFind =  doc[currentpage-1]

            parentwindow_w = self.viewer.Xpagepixels
            parentwindow_h = self.viewer.GetSize().Height
            page_w = pageToFind.bound().width
            page_h = pageToFind.bound().height

            perct_x = parentwindow_w/page_w
            perct_y = parentwindow_h/page_h

            x1 = self.c1.x/perct_x
            y1 = self.c1.y/perct_y
            x2 = self.c2.x/perct_x
            y2 = self.c2.y/perct_y
            pagewords = pageToFind.getTextWords()
            for i in pagewords:
                t1 = list(i)
                t1.append(pageToFind.number)
                i = tuple(t1)
                a1 = i[0]
                a2 = i[2]
                b1 = i[1]
                b2 = i[3]
                if pageToFind.number > 0:
                    y1 = (self.c1.y + self.viewer.nom_page_gap)/perct_y
                    y2 = (self.c2.y + self.viewer.nom_page_gap)/perct_y
                if ((a1 > x1 and a1 < x2) and (y2 > b2 and b2 > y1)) and ((a2 > x1 and a2 < x2) and (b1 < y2 and b1 > y1)):
                    siblingElementArr.append(i)

            tagV = ''
            imageStartText = ''
            if len(siblingElementArr) > 0:
                if self.combobox.Value == 'Sibling Element':
                    tagV = 'siblingElement'
                elif self.combobox.Value == 'Between Elements':
                    tagV = 'betweenElements'
                elif self.combobox.Value == 'PDF Image':
                    tagV = 'pdfImage'
                    imageStartText = (siblingElementArr[0])[4]
                lis = {"custname": '@PDF_'+tagV+'_'+str(imageStartText)+str(counter),
                    "tag":'@PDF_'+tagV,
                    "xpath":str(siblingElementArr) ,
                    "hiddentag":'No',
                    "id":'null',
                    "text":'',
                    "url":'',
                    "left":'',
                    "top":'',
                    "width":'',
                    "height":''}
                eleList.append(lis)
            siblingElementArr = []
        except Exception as e:
            logger.print_on_console('Error at pdf image in onmouseup')
            log.error(e)

##        self.viewer.U.StopPropagation()


    def OnPaint(self, event):
        if self.c1 is None or self.c2 is None: return
##        dc = wx.PaintDC(self.viewer)
        dc = wx.WindowDC(self.viewer)
        dc.SetPen(wx.Pen('black', 0.5))
##        dc.SetBrush(wx.TRANSPARENT_BRUSH)
##        dc.SetBrush(wx.Brush(wx.TRANSPARENT_BRUSH))
        dc.DrawRectangle(self.c1.x, self.c1.y, self.c2.x - self.c1.x, self.c2.y - self.c1.y)

    def OnStart(self,event):
        currentpage = self.viewer.buttonpanel
        self.search.Enable()

    def OnStop(self,event):
        self.findbar_right.Disable()
        self.findbar_left.Disable()
        self.forwardbutton.Disable()
        self.backwardbutton.Disable()
        global siblingElementArr
        if self.viewer.page_buffer_valid:
            self.viewer.SetZoom(-2)
##        if len(eleList) < 1 and len(siblingElementArr) > 0:
        tagV = ''
        if self.combobox.Value == 'Sibling Element':
            tagV = 'siblingElement'
        if self.combobox.Value == 'Between Elements':
            tagV = 'betweenElements'
        if len(siblingElementArr) > 0 :
            lis = {"custname": '@PDF_'+tagV+'_'+self.search.Value+str(counter),
                "tag":'@PDF_'+tagV,
                "xpath":str(siblingElementArr) ,
                "hiddentag":'No',
                "id":'null',
                "text":'',
                "url":'',
                "left":'',
                "top":'',
                "width":'',
                "height":''}
            eleList.append(lis)
        siblingElementArr = []
        return eleList

    def OnResize(self):
        self.viewer.SetZoom(-2)

    def OnSearch(self,event):
        global hopIndex
        global counter
        hopIndex = 1
        counter = 0
        siblingElementArr=[]
        searchtext = self.search.Value
        self.findbar_right.Enable()
        self.findbar_left.Enable()
        self.forwardbutton.Enable()
        self.backwardbutton.Enable()
        if searchtext != None and searchtext != '':
            currentpage = self.viewer.buttonpanel.pageno
            global pageToFind
            pageToFind =  doc[currentpage-1]
            global found
            found = self.searchFor(pageToFind, searchtext)

##        if (found != None and len(found) != 0):
##            mapOfTextWords = pageToFind.getTextWords()
##            stringCount = len(found)
##            firstStringToFind = found[0]
##            for i in mapOfTextWords:
##                if (i[0] == firstStringToFind.x0 and i[2] == firstStringToFind.x1 and i[1] == firstStringToFind.y0 and i[3] == firstStringToFind.y1):
##                    print (' Element found')
##      print (viewer.pagebuffer)
        wxBitmap = self.viewer.pagebuffer
        maxWidth = wxBitmap.GetWidth
        maxHeight = wxBitmap.GetHeight

        #buffer1 = wx.EmptyBitmap(maxWidth, maxHeight)

        GraphicsContext = wx.GraphicsContext
        dc1= wx.MemoryDC(wxBitmap)
        gc = GraphicsContext.Create(dc1)

        for j,i in enumerate(found):
            self.highlightCordinate(i,pageToFind)

    def searchFor(self,page,searchtext):
        if searchtext != None and searchtext != '':
             return page.searchFor(searchtext)

    def highlightCordinate(self,i,pageToFind):
        parentwindow_w = self.viewer.Xpagepixels
        parentwindow_h = self.viewer.GetSize().Height
        page_w = pageToFind.bound().width
        page_h = pageToFind.bound().height
        if(parentwindow_w > page_w) or (parentwindow_w < page_w):

            perct_x = parentwindow_w/page_w
            window_h = self.viewer.pagebufferheight
            perct_y = parentwindow_h/page_h
            page_gap = self.viewer.Ypagepixels/perct_y - page_h
            dc = wx.WindowDC(self.viewer)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            mid_y = (i.y0+i.y1)/2
            w = (i.width * perct_x)
            h = (i.height * perct_y)
            if pageToFind.number > 0:
                dc.DrawRectangle((i.x0*perct_x), (i.y0 - self.viewer.nom_page_gap)*perct_y, w*perct_x , h)
            else:
                dc.DrawRectangle((i.x0*perct_x), (i.y0*perct_y), w*perct_x , h)

    def OnHopRight(self,event):
        global counter
        if (found != None and len(found) != 0):
            mapOfTextWords = pageToFind.getTextWords()
            stringCount = len(found)
            firstStringToFind = found[counter]
            status= False
            for index , i in enumerate(mapOfTextWords):
                if (i[0] == firstStringToFind.x0 and i[2] == firstStringToFind.x1 and
                i[1] == firstStringToFind.y0 and i[3] == firstStringToFind.y1):

                    status = True
                    c = index
                    rect_obj = []
                    global hopIndex
                    global siblingElementArr
                    t = mapOfTextWords[index+hopIndex]
                    t1 = list(t)
                    t1.append(pageToFind.number)
                    t = tuple(t1)
                    if (index+hopIndex > index):
                        siblingElementArr.append(t)
                    else:
                        siblingElementArr.remove(t)
                    rect_obj.append(t[0])
                    rect_obj.append(t[2])
                    rect_obj.append(t[1])
                    rect_obj.append(t[3])

                    width = t[2] - t[0]
                    height = t[3] - t[1]
                    a = Rect()
                    a.x0 = t[0]
                    a.x1 = t[2]
                    a.y0 = t[1]
                    a.y1 = t[3]
                    a.width = width
                    a.height = height
                    self.highlightCordinate(a,pageToFind)
                    break
            if status:
                hopIndex += 1

    def OnHopLeft(self,event):
        global counter
        global hopIndex
        global siblingElementArr
        hopIndex -= 1
        if (found != None and len(found) != 0):
            mapOfTextWords = pageToFind.getTextWords()
            stringCount = len(found)

            firstStringToFind = found[counter]
            status= False
            for index , i in enumerate(mapOfTextWords):
                if (i[0] == firstStringToFind.x0 and i[2] == firstStringToFind.x1 and
                i[1] == firstStringToFind.y0 and i[3] == firstStringToFind.y1):

                    status = True
    ##                counter = index
                    rect_obj = []

                    t = mapOfTextWords[index+hopIndex]
                    t1 = list(t)
                    t1.append(pageToFind.number)
                    t = tuple(t1)
                    rect_obj.append(t[0])
                    rect_obj.append(t[2])
                    rect_obj.append(t[1])
                    rect_obj.append(t[3])

                    width = t[2] - t[0]
                    height = t[3] - t[1]
                    a = Rect()
                    a.x0 = t[0]
                    a.x1 = t[2]
                    a.y0 = t[1]
                    a.y1 = t[3]
                    a.width = width
                    a.height = height
                    self.highlightCordinate(a,pageToFind)
                    if (index+hopIndex > index):
                        siblingElementArr.remove(t)
##                        removeHighlightCordinate(a,pageToFind)
                    else:
                        siblingElementArr.append(t)
                    break


    def OnForward(self,event):
        global counter
        global hopIndex
        global siblingElementArr
        global eleList
        hopIndex = 1
        tagV = ''
        if len(siblingElementArr) > 0:
            if self.combobox.Value == 'Sibling Element':
                tagV = 'siblingElement'
            if self.combobox.Value == 'Between Elements':
                tagV = 'betweenElements'
            lis = {"custname": '@PDF_'+tagV+'_'+self.search.Value+str(counter),
                "tag":'@PDF_'+tagV,
                "xpath":str(siblingElementArr) ,
                "hiddentag":'No',
                "id":'null',
                "text":'',
                "url":'',
                "left":'',
                "top":'',
                "width":'',
                "height":''}
            eleList.append(lis)
        if counter < len(found) and counter >= 0 and len(found) >1:
            counter += 1
        increment = 0

        siblingElementArr = []

    def OnBackward(self,event):
        global hopIndex
        global siblingElementArr
        global eleList
        hopIndex = 1
        global counter

        if counter <= len(found) and counter >= 0 and len(found) >1:
            counter -= 1

        decrement = 0
        tagV = ''
        if len(siblingElementArr) > 0:
            if self.combobox.Value == 'Sibling Element':
                tagV = 'siblingElement'
            if self.combobox.Value == 'Between Elements':
                tagV = 'betweenElements'
            lis = {"custname": '@PDF_'+tagV+'_'+self.search.Value+str(counter),
                "tag":'@PDF_'+tagV,
                "xpath":str(siblingElementArr) ,
                "hiddentag":'No',
                "id":'null',
                "text":'',
                "url":'',
                "left":'',
                "top":'',
                "width":'',
                "height":''}
            eleList.append(lis)
        siblingElementArr = []

    def capture_window(self):
        handle = self.viewer.GetHandle()

        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)
        hwnd=win32gui.GetForegroundWindow()
##        win32gui.SetForegroundWindow(handle)
        bbox = win32gui.GetWindowRect(handle)
        img = ImageGrab.grab(bbox)
        img.save(TEMP_PATH + os.sep + 'test.png')
        return img
