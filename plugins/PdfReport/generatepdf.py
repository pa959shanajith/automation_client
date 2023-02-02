import os, json, wx, shutil, threading
from pdfkitlib_override import pdfkit
import logger
import logging
import re
import reportnfs
import constants
from constants import *
import sys

SEP = os.sep
log = logging.getLogger('generatepdf.py')
template_path = os.environ["AVO_ASSURE_HOME"] + "/plugins/PdfReport/template.html"
report_path = os.environ["AVO_ASSURE_HOME"] + "/plugins/PdfReport/report.json"

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
        target = os.path.normpath(self.tgt)
        dest_file = self.dst
        log.debug(str(source)+", "+str(target))
        log.debug(str(source)+", "+os.getcwd())
        filename=source.split(SEP)[-1]
        log.debug("source: "+filename)
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
                output.write(input.read())
                #output.write(data)
            #shutil.copyfile(source, os.getcwd())
            #os.rename(filename, report_path)
            opts = {'quiet': ''}
            if sys.platform=='linux':
                # temporary fix for wkhtmltopdf 0.12.6 which is used in aarm64 ubuntu focal
                # https://github.com/wkhtmltopdf/wkhtmltopdf/issues/4909
                opts['enable-local-file-access']=''
            if log.getEffectiveLevel() == logging.DEBUG: opts = {}
            pdfkit.from_file(template_path, dest_file+'.pdf', options=opts, configuration=pdfkit_conf)
            try:

                # bug 18156: checking this condition to avoid deletion of generated pdf file when target is path equal to AVO_ASSURE_HOME
                if target != os.environ['AVO_ASSURE_HOME']:
                    try: os.remove(target+SEP+dest_file+'.pdf')
                    except: pass
                    shutil.move(os.getcwd()+SEP+dest_file+'.pdf', target)
                logger.print_on_console("PDF Created Successfully")
                if sys.platform=='linux':      
                    wx.CallAfter(wx.MessageBox,'PDF Created Successfully', 'Success', wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)         
                else:
                    wx.CallAfter(wx.MessageBox, 'PDF Created Successfully', 'Success', wx.OK | wx.ICON_INFORMATION)
                    wx.CallAfter(self.wxObj.Raise)
            except Exception as e:
                emsg='PDF Created Successfully! But failed to move pdf. Please collect it from here: '+os.getcwd()
                wx.CallAfter(wx.MessageBox, emsg, 'Access Denied (Requires admin previlege)', wx.OK | wx.ICON_ERROR)
                logger.print_on_console(emsg)
                log.error(emsg)
                log.error(e)
        except Exception as e:
            log.error(e,exc_info=True)
        wx.CallAfter(self.wxObj.l4.SetLabel, " ")
        wx.CallAfter(self.wxObj.setEnable)


class GeneratePDFReport(wx.Frame):
    def __init__(self, title, conf):
        # declare a dict which has the position and size of the field in the frame respective to each platform
        # blank tuple means no size needed for that field
        # list of position size tuple
        if sys.platform == 'linux':
            pdf_gen_tool_config = {
                "frame": [(), (370, 250)],
                "source_json_field": [(12, 34), (), (160, 30), (150, 25), (320, 30), (40, 25)],
                "target_pdf_folder_field": [(12, 74), (), (160, 70), (150, 25), (320, 70), (40, 25)],
                "target_pdf_name_field": [(12, 114), (), (160, 110), (150, 25)],
                "label_field": [(12, 150)],
                "generate_bttn_field": [(185, 180), (80, 30)]
            }
        else:
            pdf_gen_tool_config = {
                "frame": [(), (350, 250)],
                "source_json_field": [(12, 34), (), (120, 30), (150, -1), (290, 30), (40, 25)],
                "target_pdf_folder_field": [(12, 74), (), (120, 70), (150, -1), (290, 70), (40, 25)],
                "target_pdf_name_field": [(12, 114), (), (120, 110), (150, -1)],
                "label_field": [(12, 150)],
                "generate_bttn_field": [(135, 180), (80, 30)]
            }
        if sys.platform == 'linux':
            wx.Frame.__init__(self, parent=None, id=-1, title=title, size=pdf_gen_tool_config["frame"][1], style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX) & ~ (wx.RESIZE_BORDER) | wx.STAY_ON_TOP)
        else:
            wx.Frame.__init__(self, parent=None, id=-1, title = title, size = pdf_gen_tool_config["frame"][1], style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX) & ~ (wx.RESIZE_BORDER))
        global pdfkit_conf
        pdfkit_conf = conf
        self.SetIcon(wx.Icon(os.environ["IMAGES_PATH"] + "/avo.ico", wx.BITMAP_TYPE_ICO))

        self.watchThread = None
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(5, 3)

        self.l1 = wx.StaticText(self.panel, label="Source json file",pos=pdf_gen_tool_config["source_json_field"][0], style=0, name="")
        self.t1 = wx.TextCtrl(self.panel, pos=pdf_gen_tool_config["source_json_field"][2], size=pdf_gen_tool_config["source_json_field"][3])
        self.btnsource = wx.Button(self.panel, label="...", pos=pdf_gen_tool_config["source_json_field"][4], size=pdf_gen_tool_config["source_json_field"][5], name="source")
        self.btnsource.Bind(wx.EVT_BUTTON, self.getFile)

        self.l2 = wx.StaticText(self.panel, label="Target pdf folder",pos=pdf_gen_tool_config["target_pdf_folder_field"][0], style=0, name="")
        self.t2 = wx.TextCtrl(self.panel, pos=pdf_gen_tool_config["target_pdf_folder_field"][2], size=pdf_gen_tool_config["target_pdf_folder_field"][3])
        self.btntarget = wx.Button(self.panel, label="...", pos=pdf_gen_tool_config["target_pdf_folder_field"][4], size=pdf_gen_tool_config["target_pdf_folder_field"][5], name="target")
        self.btntarget.Bind(wx.EVT_BUTTON, self.getFile)

        self.l3 = wx.StaticText(self.panel, label="Target pdf filename",pos=pdf_gen_tool_config["target_pdf_name_field"][0], style=0, name="")
        self.t3 = wx.TextCtrl(self.panel, pos=pdf_gen_tool_config["target_pdf_name_field"][2], size=pdf_gen_tool_config["target_pdf_name_field"][3])

        self.l4 = wx.StaticText(self.panel, label=" ", pos=pdf_gen_tool_config["label_field"][0], style=0, name="")

        self.btn = wx.Button(self.panel, label="Generate",pos=pdf_gen_tool_config["generate_bttn_field"][0], size=pdf_gen_tool_config["generate_bttn_field"][1])
        self.btn.Bind(wx.EVT_BUTTON, self.generatePDF)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show()

    def OnClose(self, *event):
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
        
        error_flag = False
        if source.strip()=='' or target.strip()=='' or dest_file.strip()=='':
            self.l4.SetLabel("No input field can be left empty!")
            error_flag = True
        elif not (os.path.isdir(target) and os.path.exists(source)):
            self.l4.SetLabel("Either Source or Target path is Invalid!") 
            error_flag = True
        elif source.split('.')[-1].lower() != 'json':
            self.l4.SetLabel("Source is not a JSON File")
            error_flag = True
        elif re.search(r'[<>:"/\\|?*]',dest_file) is not None:
            self.l4.SetLabel("File name can't contain following characters: \\ / < | : ? * > \"")
            error_flag=True
        elif re.sub(r'[^a-zA-Z0-9]', '', dest_file) == '':
            self.l4.SetLabel("File name must contain atleast one alphanumeric character!")
            error_flag=True
        try:
            with open(source, 'rb') as read_file:
                json_data = json.load(read_file)
                if not (("overallstatus" in json_data) and ("rows" in json_data)):
                    self.l4.SetLabel("Invalid report JSON File")
                    error_flag = True
        except:
            if not error_flag:
                self.l4.SetLabel("Invalid JSON File")
                error_flag = True
        try:
            newFileName = dest_file+'.pdf'
            # file = files in os.walk(target)
            for root, dirs, files in os.walk(target):
                if newFileName in files:
                    error_flag = True
                    # self.l4.SetLabel("File Name already exists")
                    # logger.print_on_console("PDF Created Successfully")
                    # r = wx.CallAfter(wx.MessageBox, newFileName + ' already exists click on Yes to override','PDF Report Generator', wx.YES | wx.NO | wx.ICON_ERROR)
                    dlg = wx.MessageDialog(self,newFileName + ' already exists.\nDo you want to replace it?','PDF Report Generator', wx.YES| wx.NO |wx.ICON_WARNING)
                    if dlg.ShowModal() == wx.ID_YES:
                        error_flag = False
                    else:
                        self.l4.SetLabel("Please rename Target Pdf filename to proceed")

                    dlg.Destroy()

                
                break
        except:
            if not error_flag:
                self.l4.SetLabel("Error in Target pdf location")
                error_flag = True


        if error_flag: return False
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
