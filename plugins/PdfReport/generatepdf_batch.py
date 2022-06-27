import os, json, wx, shutil, threading, time
from importlib_metadata import files
from pdfkitlib_override import pdfkit
import reportnfs
import constants
from constants import *
import logger
import logging
log = logging.getLogger('generatepdf_batch.py')
template_path = os.environ["AVO_ASSURE_HOME"] + "/plugins/PdfReport/template.html"
report_path = os.environ["AVO_ASSURE_HOME"] + "/plugins/PdfReport/report.json"
SEP = os.sep

class WatchThread(threading.Thread):
    def __init__(self, wxObj, source, target):
        threading.Thread.__init__(self)
        self.wxObj = wxObj
        self.src = source
        self.tgt = target
        self.keep_running = True
        self.start()

    def run(self):
        source = self.src
        target = os.path.normpath(self.tgt)
        log.debug(str(source)+", "+str(target))
        '''
        with open(source) as f:
            lines = f.readlines()
            log.debug(lines)
            lines = [l for l in lines if "ROW" in l]
            with open(report_path, "w") as f1:
                f1.writelines(lines)
        '''
        log.debug("1"+str(os.listdir(source)))
        path_to_watch = source
        #before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        before = []
        opts = {'quiet': ''}
        if log.getEffectiveLevel() == logging.DEBUG: opts = {}
        while self.keep_running:
            time.sleep(5)
            after = dict ([(f, None) for f in os.listdir (path_to_watch)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]
            if added: log.debug("Added: "+", ".join (added))
            if removed: log.debug("Removed: "+", ".join (removed))
            before = after
            for filename in added:
                extn=filename.split('.')[-1].lower()
                file_name=filename.split('.')[0]
                if(extn != 'json'):
                    continue
                log.debug(">>>>>>>>"+source+SEP+filename)
                try:
                    with open(report_path, 'wb+') as output, open(source+SEP+filename, 'rb') as src_path:
                        emsg = None
                        try:
                            json_data = json.load(src_path)
                            if not (("overallstatus" in json_data) and ("rows" in json_data)):
                                emsg = str(filename)+" is invalid report JSON file."
                        except:
                            emsg = str(filename)+" is not a valid JSON file."
                        finally:
                            src_path.seek(0)
                        if emsg is not None:
                            logger.print_on_console(emsg)
                            log.error(emsg)
                            continue
                        output.write(src_path.read())
                        #output.write(data)
                    #shutil.copyfile(source, os.getcwd())
                    #os.rename(filename, report_path)
                    pdfkit.from_file(template_path, file_name+'.pdf', options=opts, configuration=pdfkit_conf)
                    try:
                        if target != os.environ['AVO_ASSURE_HOME']:
                            try: os.remove(target+SEP+file_name+'.pdf')
                            except: pass
                            shutil.move(os.getcwd()+SEP+file_name+'.pdf', target)
                        logger.print_on_console(file_name+".pdf Created Successfully")
                    except Exception as e:
                        emsg = file_name+".pdf Created Successfully. Fail to move "+os.getcwd()+"\\"+file_name+'.pdf'+" to "+ target
                        logger.print_on_console(emsg)
                        log.error(emsg)
                        log.error(e)
                except Exception as e:
                    log.error(e)
            wx.CallAfter(self.wxObj.l4.SetLabel,"Reports generated successfully")
            wx.CallAfter(self.wxObj.btn.SetLabel,"Start")
            self.wxObj.watchThread.keep_running = False
            self.wxObj.watchThread= None
            self.wxObj.started = False

class GeneratePDFReportBatch(wx.Frame):
    def __init__(self, title, conf):
        wx.Frame.__init__(self, parent=None, id=-1, title = title,size = (350,200),
            style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX) & ~ (wx.RESIZE_BORDER))

        global pdfkit_conf
        pdfkit_conf = conf
        self.SetIcon(wx.Icon(os.environ["IMAGES_PATH"] + "/avo.ico", wx.BITMAP_TYPE_ICO))

        self.watchThread = None
        self.started = False
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(5, 3)

        self.l1=wx.StaticText(self.panel, label="Source json folder", pos=(12,34), style=0, name="")
        self.t1=wx.TextCtrl(self.panel, pos=(120,30), size=(150,-1))
        self.btnsource = wx.Button(self.panel, label="...", pos=(290,30), size=(40,25), name="source")
        self.btnsource.Bind(wx.EVT_BUTTON, self.getFile)

        self.l2=wx.StaticText(self.panel, label="Target pdf folder", pos=(12,74), style=0, name="")
        self.t2=wx.TextCtrl(self.panel, pos=(120,70), size=(150,-1))
        self.btntarget= wx.Button(self.panel, label="...", pos=(290,70), size=(40,25), name="target")
        self.btntarget.Bind(wx.EVT_BUTTON, self.getFile)

        self.l4=wx.StaticText(self.panel, label=" ", pos=(12,100), style=0, name="")

        self.btn = wx.Button(self.panel, label="Start",pos=(135,130), size=(80,30))
        self.btn.Bind(wx.EVT_BUTTON, self.generatePDF)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show()

    def OnClose(self, *event):
        if self.watchThread is not None:
            self.watchThread.keep_running = False
            self.watchThread.join()
        self.Destroy()
        try:
            os.remove(report_path)
        except:
            pass

    def generatePDF(self,*args):
        self.l4.SetLabel(" ")
        source = self.t1.GetValue()
        target = self.t2.GetValue()

        error_flag = False
        if source.strip()=='' or target.strip()=='':
            self.l4.SetLabel("No input field can be left empty!")
            error_flag = True
        elif not (os.path.isdir(target) and os.path.exists(source)):
            self.l4.SetLabel("Either Source or Target path is Invalid!")
            error_flag = True
        try:
            sourceFileName = []
            for root, dirs, files1 in os.walk(source):
                sourceFileName = files1
                break

            for name in sourceFileName:
                name = name[:-4] + 'pdf'
                for root, dirs, files2 in os.walk(target):
                    if name in files2:
                        error_flag = True
                        self.l4.SetLabel(name + " is already present in Target Folder")

                    break
        except:
                if not error_flag:
                    self.l4.SetLabel("Error in Target/Source pdf location")
                    error_flag = True

        if error_flag: return False

        self.btn.SetLabel("Start" if self.started else "Stop")
        self.setEnable(self.started)
        if self.started:
            self.watchThread.keep_running = False
            self.watchThread.join()
            self.watchThread= None
            self.started = False
        else:
            try:
                os.remove(report_path)
            except:
                pass
            self.started = True
            self.l4.SetLabel("Listening...")
            self.watchThread = WatchThread(self,source,target)

    def getFile(self,*args):
        dialog = wx.DirDialog (None, "Choose input directory", "",wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            if(args[0].GetEventObject().GetName() == 'source'):
                self.t1.SetValue(path)
            elif(args[0].GetEventObject().GetName() == 'target'):
                self.t2.SetValue(path)
        dialog.Destroy()

    def setEnable(self, val=True):
        self.t1.Enable(val)
        self.btnsource.Enable(val)
        self.t2.Enable(val)
        self.btntarget.Enable(val)
