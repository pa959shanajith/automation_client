#-------------------------------------------------------------------------------
# Name:        pdflib_custom.py
# Purpose:	   Overwrite wxPython pdfviewer module for PDF plugin support
#
# Author:      ranjan.agrawal
#
# Created:     16-06-2021
# Copyright:   (c) ranjan.agrawal
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx
import fitz
from six import BytesIO, string_types
from wx.lib.pdfviewer import images
import wx.lib.agw.buttonpanel as bp
from wx.lib.pdfviewer import pdfViewer as pdfViewer_main, pdfButtonPanel as pdfButtonPanel_main


class pdfViewer(pdfViewer_main):

    def LoadFile(self, pdf_file):
        """
        Read pdf file. Assume all pages are same size, for now.

        :param `pdf_file`: can be either a string holding
        a filename path or a file-like object.
        """
        def create_fileobject(filename):
            """
            Create and return a file object with the contents of filename,
            only used for testing.
            """
            f = open(filename, 'rb')
            stream = f.read()
            return BytesIO(stream)

        self.pdfpathname = ''
        if isinstance(pdf_file, string_types):
            # a filename/path string, save its name
            self.pdfpathname = pdf_file
            # remove comment from next line to test using a file-like object
            # pdf_file = create_fileobject(pdf_file)
        if wx.lib.pdfviewer.viewer.mupdf:
            self.pdfdoc = mupdfProcessor(self, pdf_file)
        else:
            self.pdfdoc = wx.lib.pdfviewer.viewer.pypdfProcessor(self, pdf_file, self.ShowLoadProgress)

        self.numpages = self.pdfdoc.numpages
        self.pagewidth = self.pdfdoc.pagewidth
        self.pageheight = self.pdfdoc.pageheight
        self.page_buffer_valid = False
        self.Scroll(0, 0)               # in case this is a re-LoadFile
        self.CalculateDimensions()      # to get initial visible page range
        # draw and display the minimal set of pages
        self.pdfdoc.DrawFile(self.frompage, self.topage)
        self.have_file = True
        # now draw full set of pages
        wx.CallAfter(self.pdfdoc.DrawFile, 0, self.numpages-1)

    def RenderPageBoundaries(self, gc):
        """
        Show non-page areas in grey.
        """
        gc.SetBrush(wx.Brush(wx.Colour(230, 230, 255)))        #mid grey
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.Scale(1.0, 1.0)
        extrawidth = self.winwidth - self.Xpagepixels
        if extrawidth > 0:
            gc.DrawRectangle(self.winwidth-extrawidth, 0, extrawidth, self.maxheight)
        extraheight = self.winheight - (self.numpages*self.Ypagepixels - self.y0)
        if extraheight > 0:
            gc.DrawRectangle(0, self.winheight-extraheight, self.maxwidth, extraheight)



class mupdfProcessor(wx.lib.pdfviewer.viewer.mupdfProcessor):

    def RenderPage(self, gc, pageno, scale=1.0):
        " Render the set of pagedrawings into gc for specified page "
        page = self.pdfdoc.loadPage(pageno)
        matrix = fitz.Matrix(scale, scale)
        try:
            pix = page.getPixmap(matrix=matrix)   # MUST be keyword arg(s)
            if [int(v) for v in fitz.version[1].split('.')] >= [1,15,0]:
                # See https://github.com/wxWidgets/Phoenix/issues/1350
                bmp = wx.Bitmap.FromBuffer(pix.width, pix.height, pix.samples)
            else:
                bmp = wx.Bitmap.FromBufferRGBA(pix.width, pix.height, pix.samples)
            gc.DrawBitmap(bmp, 0, 0, pix.width, pix.height)
            self.zoom_error = False
        except (RuntimeError, MemoryError):
            if not self.zoom_error:     # report once only
                self.zoom_error = True
                dlg = wx.MessageDialog(self.parent, 'Out of memory. Zoom level too high?',
                              'pdf viewer' , wx.OK |wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()



class pdfButtonPanel(pdfButtonPanel_main):

    def CreateButtons(self):
        """
        Add the buttons and other controls to the panel.
        """
        self.disabled_controls = []
        self.pagelabel = wx.StaticText(self, -1, 'Page')
        self.pagelabel.SetForegroundColour((255,255,255))   #~#
        self.page = wx.TextCtrl(self, -1, size=(30, -1), style=wx.TE_CENTRE|wx.TE_PROCESS_ENTER)
        self.page.Enable(False)
        self.disabled_controls.append(self.page)
        self.page.Bind(wx.EVT_KILL_FOCUS, self.OnPage)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnPage, self.page)
        self.maxlabel = wx.StaticText(self, -1, '          ')
        self.zoom = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.zoom.Enable(False)
        self.disabled_controls.append(self.zoom)
        self.comboval = (('Actual size', 1.0), ('Fit width', -1), ('Fit page', -2),
                          ('25%', 0.25), ('50%', 0.5), ('75%', 0.75), ('100%', 1.0),
                            ('125%', 1.25), ('150%', 1.5), ('200%', 2.0), ('400%', 4.0),
                            ('800%', 8.0), ('1000%', 10.0))
        for item in self.comboval:
            self.zoom.Append(item[0], item[1])      # string value and client data
        self.Bind(wx.EVT_COMBOBOX, self.OnZoomSet, self.zoom)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnZoomSet, self.zoom)
        panelitems = [
          # ('btn', images.PrintIt.GetBitmap(), wx.ITEM_NORMAL, "Print", self.OnPrint),
          # ('sep',),
          # ('btn', images.SaveIt.GetBitmap(), wx.ITEM_NORMAL, "Save", self.OnSave),
          # ('sep',),
          ('btn', images.First.GetBitmap(), wx.ITEM_NORMAL, "First page", self.OnFirst),
          ('btn', images.Prev.GetBitmap(), wx.ITEM_NORMAL, "Previous page", self.OnPrev),
          ('btn', images.Next.GetBitmap(), wx.ITEM_NORMAL, "Next page", self.OnNext),
          ('btn', images.Last.GetBitmap(), wx.ITEM_NORMAL, "Last page", self.OnLast),
          ('Ctrl', self.pagelabel),
          ('ctrl', self.page),
          ('ctrl', self.maxlabel),
          ('sep',),
          # ('btn', images.ZoomOut.GetBitmap(), wx.ITEM_NORMAL, "Zoom out", self.OnZoomOut),
          # ('btn', images.ZoomIn.GetBitmap(), wx.ITEM_NORMAL, "Zoom in", self.OnZoomIn),
          ('ctrl', self.zoom),
          ('btn', images.Width.GetBitmap(), wx.ITEM_NORMAL, "Fit page width", self.OnWidth),
          ('btn', images.Height.GetBitmap(), wx.ITEM_NORMAL, "Fit page height", self.OnHeight),
          ]

        self.Freeze()
        for item in panelitems:
            if item[0].lower() == 'btn':
                x_type, image, kind, popup, handler = item
                btn = bp.ButtonInfo(self, wx.ID_ANY,image, kind=kind,
                                    shortHelp=popup, longHelp='')
                self.AddButton(btn)
                btn.Enable(False)
                self.disabled_controls.append(btn)
                self.Bind(wx.EVT_BUTTON, handler, id=btn.GetId())
            elif item[0].lower() == 'sep':
                self.AddSeparator()
            elif item[0].lower() == 'space':
                self.AddSpacer(item[1])
            elif item[0].lower() == 'ctrl':
                self.AddControl(item[1])
        self.Thaw()
        self.DoLayout()

    def Update(self, pagenum, numpages, zoomscale):
        """
        Called from viewer to initialize and update controls.

        :param integer `pagenum`: the page to show
        :param integer `numpages`: the total pages
        :param integer `zoomscale`: the zoom factor

        :note:
            In the viewer, page range is from 0 to numpages-1, in button controls it
            is from 1 to numpages.

        """
        if self.disabled_controls:
            for item in self.disabled_controls:
                item.Enable(True)
            self.disabled_controls = []
            self.Refresh()

        self.pageno = pagenum + 1
        self.page.ChangeValue('%d' % self.pageno)
        if numpages != self.numpages:
            self.maxlabel.SetLabel('of %d' % numpages)
            self.maxlabel.SetForegroundColour((255,255,255))
            self.numpages = numpages
        self.percentzoom = zoomscale * 100
        self.zoom.SetValue('%.0f%%' % self.percentzoom)
        self.zoomtext = self.zoom.GetValue()    # save last good value
