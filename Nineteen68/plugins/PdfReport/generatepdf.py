import os, json, wx, shutil, threading, pdfkit
import logger
import logging
log = logging.getLogger('generatepdf.py')
template_path = os.environ["NINETEEN68_HOME"] + "/Nineteen68/plugins/PdfReport/template.html"
report_path = os.environ["NINETEEN68_HOME"] + "/Nineteen68/plugins/PdfReport/report.json"

class WatchThread(threading.Thread):
    def __init__(self, wxObj, source, target, dest_file):
        threading.Thread.__init__(self)
        self.wxObj = wxObj
        self.src = source
        self.tgt = target
        self.dst = dest_file
        self.keep_running = True
        self.start()

    def run(self):
        source = self.src
        target = self.tgt
        dest_file = self.dst
        log.debug(source,target)
        log.debug(source, os.getcwd())
        filename = source.split('\\')[-1]
        log.debug("source: " ,filename)
        '''
        with open(source) as f:
            lines = f.readlines()
            print(lines)
            lines = [l for l in lines if "ROW" in l]
            with open(report_path, "w") as f1:
                f1.writelines(lines)
        '''
        try:
            with open(report_path, 'wb+') as output, open(source, 'rb') as input:
                dat = json.loads(input.read())
                filename = filename.replace(".json","")
                dat['overallstatus'][0]['scenarioName'] = filename
                output.write(json.dumps(dat))
                #output.write(data)
            #shutil.copyfile(source, os.getcwd())
            #os.rename(filename, report_path)
            opts = {'quiet': ''}
            if log.getEffectiveLevel() == logging.DEBUG: opts = {}
            pdfkit.from_file(template_path, dest_file+'.pdf', options=opts, configuration=pdfkit_conf)
            try:
                try:
                    os.remove(target+"\\"+dest_file+'.pdf')
                except:
                    pass
                shutil.move(os.getcwd()+"\\"+dest_file+'.pdf', target)
                wx.MessageBox('PDF Created Successfully', 'Success', wx.OK | wx.ICON_INFORMATION)
                logger.print_on_console("PDF Created Successfully")
            except Exception as e:
                emsg='PDF Created Successfully! But failed to move pdf. Please collect it from here: '+os.getcwd()
                wx.MessageBox(emsg, 'Access Denied (Requires admin previlege)', wx.OK | wx.ICON_ERROR)
                logger.print_on_console(emsg)
                log.error(emsg)
                log.error(e)
        except Exception as e:
            log.error(e)
        self.wxObj.l4.SetLabel(" ")
        self.wxObj.setEnable()


class GeneratePDFReport(wx.Frame):
    def __init__(self, title, conf):
        wx.Frame.__init__(self, parent=None, id=-1, title = title, size = (350,250),
            style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX) & ~ (wx.RESIZE_BORDER))

        global pdfkit_conf
        pdfkit_conf = conf
        self.SetIcon(wx.Icon(os.environ["IMAGES_PATH"] + "/slk.ico", wx.BITMAP_TYPE_ICO))

        self.watchThread = None
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(5, 3)

        self.l1=wx.StaticText(self.panel, label="Source JSON", pos=(12,34), style=0, name="")
        self.t1=wx.TextCtrl(self.panel, pos=(120,30), size=(150,-1))
        self.btnsource = wx.Button(self.panel, label="...", pos=(290,30), size=(40,25), name="source")
        self.btnsource.Bind(wx.EVT_BUTTON, self.getFile)

        self.l2=wx.StaticText(self.panel, label="Target PDF Path", pos=(12,74), style=0, name="")
        self.t2=wx.TextCtrl(self.panel, pos=(120,70), size=(150,-1))
        self.btntarget= wx.Button(self.panel, label="...", pos=(290,70), size=(40,25), name="target")
        self.btntarget.Bind(wx.EVT_BUTTON, self.getFile)

        self.l3=wx.StaticText(self.panel, label="Filename", pos=(12,114), style=0, name="")
        self.t3=wx.TextCtrl(self.panel, pos=(120,110), size=(150,-1))

        self.l4=wx.StaticText(self.panel, label=" ", pos=(12,150), style=0, name="")

        self.btn = wx.Button(self.panel, label="Generate",pos=(135,180), size=(80,30))
        self.btn.Bind(wx.EVT_BUTTON, self.generatePDF)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show()

    def OnClose(self, event):
        self.Destroy()
        try:
            os.remove(report_path)
        except:
            pass

    def generatePDF(self,*args):
        self.l4.SetLabel(" ")
        try:
            os.remove(report_path)
        except:
            pass
        source = self.t1.GetValue()
        target = self.t2.GetValue()
        dest_file = self.t3.GetValue()
        if source.strip()=='' or target.strip()=='' or dest_file.strip()=='':
            self.l4.SetLabel("No input feild can be left empty!")
            return
        self.l4.SetLabel("Processing...")
        self.setEnable(False)
        self.watchThread = WatchThread(self,source,target,dest_file)

    def getFile(self,*args):
        dialog = None
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        if(args[0].GetEventObject().GetName() == 'source'):
            dialog = wx.FileDialog(None, 'Open', style=style)
        elif(args[0].GetEventObject().GetName()  == 'target'):
            dialog = wx.DirDialog (None, "Choose input directory", "",wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        else: return

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            if(args[0].GetEventObject().GetName() == 'source'):
                self.t1.SetValue(path)
            elif(args[0].GetEventObject().GetName() == 'target'):
                self.t2.SetValue(path)
        dialog.Destroy()
        self.SetFocus()

    def setEnable(self, val=True):
        self.t1.Enable(val)
        self.btnsource.Enable(val)
        self.t2.Enable(val)
        self.btntarget.Enable(val)
        self.t3.Enable(val)
        self.btn.Enable(val)
