import wx
import os
import json
from fontTools import ttLib
import re
import shutil
import logging
import subprocess
import time
import threading
import datetime


date_obj = datetime.datetime.now()

'''
    Home Directory and Zip file location are initialized here
'''
AVO_ASSURE_HOME = os.path.normpath(str(os.getcwd())) + '/'
LOC_7z = AVO_ASSURE_HOME + "Lib/7zip/7z.exe"

'''
    Setting Tesseract-OCR to environment
'''
try:
    os.environ['PATH'] = AVO_ASSURE_HOME + '/Lib/Tesseract-OCR/tesseract.exe'
    os.environ['PATH'] = AVO_ASSURE_HOME + '/Lib/Tesseract-OCR'
except Exception as e:
    print('ERROR occurred while setting path, please set path manually, paths to set in user env-variable :[AVO_ASSURE_HOME + /Lib/Tesseract-OCR/tesseract.exe, AVO_ASSURE_HOME + /Lib/Tesseract-OCR]')

'''
    Config.json is accessed and stored in a variable to later access all the configuration values
'''
config_path = AVO_ASSURE_HOME + "assets/IRISMT/config.json"
config_file = open(config_path, "r")
configs = json.load(config_file)
config_file.close()


'''
    Log location is configured here to save all the logs generated and make log directory if not exist
'''
log_loc = AVO_ASSURE_HOME + configs['logFile_Path'][:configs['logFile_Path'].rindex('/')]
if not ( os.path.isdir(str(log_loc)) and os.path.exists(str(log_loc)) ):
    os.mkdir(str(log_loc))


log = logging.getLogger("IRISMT.py")
log.setLevel(logging.DEBUG)
log_filepath = str(log_loc) + '/Training_logs_' + str(date_obj.year) + '_' + str(date_obj.month) + '_' + str(date_obj.day) + '_' + str(date_obj.hour) + str(date_obj.minute) + '.log'
file_handler = logging.FileHandler(log_filepath)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

class IRISMT(wx.Frame):
    '''
        inputs: common object and message object for progress bar
    '''
    def __init__(self, comm_obj, msg):

        '''
            All the paths are stored in a dictionary after retrieving from config json file
        '''
        self.FONTS_DIR = None
        self.TRAININGTOOL_DIR = AVO_ASSURE_HOME + configs["trainingtool_dir"]
        self.LANG = configs["lang"]
        self.LANGDATA_DIR = AVO_ASSURE_HOME + configs["langdata_dir"]
        self.TESSDATA_DIR = AVO_ASSURE_HOME + configs["tessdata_dir"]
        self.TRAININGFILES_DIR = AVO_ASSURE_HOME + configs["trainingfiles_dir"]
        self.TRAINEDDATA_DIR = AVO_ASSURE_HOME + configs["traineddata_dir"]
        self.CHECKPOINT_DIR = AVO_ASSURE_HOME + configs["checkpoint_dir"]
        self.ITERATIONS = configs["iterations"]
        self.TRAINED_RESULT = AVO_ASSURE_HOME + configs["trained_result"]
        self.all_versions = configs["all_versions"]
        self.current_version = configs["current_version"]
        self.active_model = AVO_ASSURE_HOME + configs["active_model"]
        self.rollback_dir = AVO_ASSURE_HOME + configs["rollback_dir"]

        log.debug("All value initialized")

        if not os.path.exists(self.CHECKPOINT_DIR):
            log.debug("Creating Checkpoint folder")
            os.mkdir(self.CHECKPOINT_DIR)               # if checkpoingt folder doesn't exist then it is created
            log.debug("Checkpoint folder created")

        self.flow_flag = 1              # flow flag switches to 0 if any error occurs
        self.comm_obj = comm_obj        # assigning shared objects to self to access it globally
        self.msg = msg

        '''
            All the widget elements are defined and initialized here
        '''
        wx.Frame.__init__(self, parent=None, title="IRIS MT", pos=(300, 150),  size=(500, 300),style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX))
        self.SetBackgroundColour('#e6e7e8')

        self.panel = wx.Panel(self)

        # training data select label
        self.fontselect_label = wx.StaticText(self.panel, -1,  "Training Data:", pos=(20, 32), size=(100, 20), style=1)
        self.fontselect_txtfield = wx.TextCtrl(self.panel, pos=(120, 30), size=(260, 25), style=wx.FLP_DEFAULT_STYLE|wx.TE_READONLY)

        # training data select button
        self.fontselect_btn = wx.Button(self.panel, label="Select", pos=(390, 28), size=(80, 28))
        self.fontselect_btn.Bind(wx.EVT_BUTTON, self.selectFonts)

        # train button
        self.train_btn = wx.Button(self.panel, label="Train", pos=(135, 80), size=(100, 25))
        self.train_btn.Bind(wx.EVT_BUTTON, self.start_training)

        # revert button to hide/unhide rollback and version list
        self.revert_btn = wx.Button(self.panel, label="Revert", pos=(245, 80), size=(100, 25))
        self.revert_btn.Bind(wx.EVT_BUTTON, self.show_rollback)

        # rollback button to rollback to a previous version
        self.rollback_btn = wx.Button(self.panel, label="Rollback", pos=(355, 80), size=(100, 25))
        self.rollback_btn.Bind(wx.EVT_BUTTON, self.rollback)
        self.rollback_btn.Hide()        # initialized as hidden

        # version list combobox
        choices = self.all_versions
        if len(choices) == 1 and str(choices[0]) == str(self.current_version):
            self.revert_btn.Disable()
        else:
            self.revert_btn.Enable()
        self.version_list = wx.ComboBox(self.panel, pos = (245, 81), size = (100, 25), choices=choices, style=wx.CB_READONLY | wx.CB_DROPDOWN)
        self.version_list.SetSelection(self.all_versions.index(self.current_version))
        self.version_list.Bind(wx.EVT_COMBOBOX, self.combo_opt)
        self.version_list.Hide()    # initialized as hidden same as rollback


        # log message box
        self.log = wx.TextCtrl(self.panel, pos=(20, 130), size=(450, 110) , style=wx.TE_MULTILINE|wx.TE_READONLY)
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,  False, 'Consolas')
        self.log.SetForegroundColour((0,50,250))
        self.log.SetFont(font1)
        self.log.AppendText("-"*28 +"Logs"+"-"*28)
        self.log.AppendText("\n"+"-"*60)
        self.print_log("Current Version: "+str(self.current_version))
        self.Center()
        self.Show()

        # binding the close button to onClose method to destroy progress bar only when exiting
        self.Bind(wx.EVT_CLOSE, self.onClose)


    '''
        Definition: this method gets called when user presses the close button of the window
        input: event object from the close button
        reference: inside __init__ method
    '''
    def onClose(self, event):
        log.info("Deleting msg object")
        self.msg.destroyObject()        # destroys the msg object which is for progress bar
        log.info("Deleting current window object")
        self.Destroy()                  # destroys the current window

    # def revert_model(self, event):
    #     prev_ver = self.get_previous_version()
    #     if prev_ver is None:
    #         print("Revert Model Fail")
    #         return
    #     if self.backup_current_model():
    #         try:
    #             extract_model = r'{loc_7z} x {zipfile} -o{outputdir} {file} -r -y'.format(loc_7z=LOC_7z, zipfile=self.rollback_dir, outputdir=os.path.dirname(self.active_model), file="eng.traineddata_"+prev_ver)
    #             subprocess.call(extract_model, shell=True)
    #             if os.path.exists(self.active_model):
    #                 os.remove(self.active_model)
    #             os.rename(self.active_model+'_'+prev_ver, self.active_model)
    #             self.downgrade_version(prev_ver)
    #         except Exception as err:
    #             print("error in getting previous model")
    #     else:
    #         print("Backup failed. Cannot proceed to revert back")



    '''
        Definition: During rollback, deletes all the versions newer than the selected version
        input: takes the index of version that is being rolled backed
        reference: rollback() method
    '''
    def delete_backups(self, index):
        if not os.path.exists(self.rollback_dir):
            log.info("Rollback file doesn't exist, cannot delete backups")
            return
        try:
            versions = "eng.traineddata_"+" eng.traineddata_".join(self.all_versions[index+1:])
            log.info("Deleting backups")
            delete_cmd = r'{loc_7z} d {zipfile} {files} -r'.format(loc_7z=LOC_7z, zipfile=self.rollback_dir, files=versions)
            subprocess.call(delete_cmd, shell=True)
            log.info("Backups Deleted")
        except Exception as err:
            log.error("Error occured while deleting backups: "+str(err))
            self.print_log("Error Occured in deleting backups")


    '''
        Definition: Rollback method is triggered when pressing the "Rollback" button, rolls back to the selected version
        It rolls back the eng.traineddata to any version selected by user from the dropdown menu
        Input: Event object from the button
    '''
    def rollback(self, event):
        self.print_log("Extracting Model...")
        log.info("Extracting Model...")
        rollback_index = self.version_list.GetCurrentSelection()
        rollback_ver = self.version_list.GetStringSelection()
        log.info("Rollback versions selected")
        self.msg.StartThread(self.msg.showProgress)
        self.comm_obj.percentageIncri(self.msg,10,"Rolling Back...")

        if self.backup_current_model():
            self.comm_obj.percentageIncri(self.msg,30,"Rolling Back...")
            try:
                extract_model = r'{loc_7z} x {zipfile} -o{outputdir} {file} -r -y'.format(loc_7z=LOC_7z, zipfile=self.rollback_dir, outputdir=os.path.dirname(self.active_model), file=str("eng.traineddata_"+rollback_ver))
                subprocess.call(extract_model, shell=True)
                self.comm_obj.percentageIncri(self.msg,70,"Rolling Back...")
                if os.path.exists(self.active_model) and os.path.exists(self.active_model+'_'+rollback_ver):
                    log.info("Deleting current model")
                    os.remove(self.active_model)
                self.comm_obj.percentageIncri(self.msg,80,"Rolling Back...")
                log.info("Renaming the extracted model")
                os.rename(self.active_model+'_'+rollback_ver, self.active_model)
                self.comm_obj.percentageIncri(self.msg,90,"Rolling Back...")
                log.info("Updating config file")
                self.downgrade_version(rollback_ver, rollback_index)
                log.info("Updating combo box")
                self.reset_dropdown()
                self.comm_obj.percentageIncri(self.msg,100,"Rolling Back...")
                self.delete_backups(rollback_index)
                # self.msg.ShowMessage("Rolled back successfully.")
                self.print_log("Model Extracted")
                log.info("Model Extracted. Rollback successful")
                self.print_log("------Rollback Successful------")
                if len(self.all_versions) == 1 and str(self.all_versions[0]) == str(self.current_version):
                    if self.rollback_btn.IsShown():
                        log.debug("Hiding rollback options")
                        self.train_btn.SetPosition((135, 80))
                        self.revert_btn.SetPosition((245, 80))
                        self.version_list.Hide()
                        self.rollback_btn.Hide()
                        self.revert_btn.Disable()
            except Exception as err:
                self.comm_obj.percentageIncri(self.msg,100,"Rollback Failed")

                # self.msg.ShowMessage("Rolled back Failed!")
                self.print_log("Error In Extracting Desired Model")
        else:
            self.comm_obj.percentageIncri(self.msg,100,"Rollback Failed")
            log.error("Rollback Failed")
            # self.msg.ShowMessage("Rolled back Failed!")
            self.print_log("Create Backup Failed. Cannot proceed to Rollback")

        # self.msg.destoryProgress()

    '''
        Definition: reset_dropdown is being called inside start_training
                    It re-initializes the dropdown menu after a new model is trained
                    else the dropdown will not show the latest changes
        Inputs: None
        References: train_font and rollback methods
    '''
    def reset_dropdown(self):
        choices = self.all_versions
        curr = self.current_version
        self.version_list.Clear()
        self.version_list.AppendItems(choices)
        self.version_list.SetSelection(choices.index(curr))
        log.debug("Redrawing version list box")
        # if self.version_list.IsShown():
        #     self.version_list = wx.ComboBox(self.panel, pos = (245, 81), size = (100, 25), choices=choices, style=wx.CB_READONLY | wx.CB_DROPDOWN)
        # else:
        #     self.version_list = wx.ComboBox(self.panel, pos = (245, 81), size = (100, 25), choices=choices, style=wx.CB_READONLY | wx.CB_DROPDOWN)
        #     self.version_list.Hide()

    '''
        Definition : Triggers when pressing "revert" button
                    It displays rollback options on the screen that were initially hidden
        inputs: event object when revert button is pressed
    '''
    def show_rollback(self, event):
        if self.rollback_btn.IsShown():
            log.debug("Revert Pressed. Hiding rollback options")
            self.train_btn.SetPosition((135, 80))
            self.revert_btn.SetPosition((245, 80))
            self.version_list.Hide()
            self.rollback_btn.Hide()
        else:
            log.debug("Revert Pressed. Rollback options shown")
            self.train_btn.SetPosition((25, 80))
            self.revert_btn.SetPosition((135, 80))
            self.version_list.Show()
            self.rollback_btn.Show()
            self.rollback_btn.Disable()

    def combo_opt(self, event):
        """
        Definition : Enables/Disables Rollback button on option selection in the combo_box.
                     Rollback button is disabled when combo_box value is the same as current version
        Inputs: event object when when combo_box items are selected
        """
        combo_box_item_index = self.version_list.GetSelection()
        combo_box_item_value=self.version_list.GetString(combo_box_item_index)
        if (str(self.current_version) != str(combo_box_item_value)):
            self.rollback_btn.Enable()
        else:
            self.rollback_btn.Disable()

    """
        Definition: Converts the line endings of auto generated training_file.txt's
                    line endings from Windows Line (CRLF) to Unix Line (LF)
        Inputs: None
        References: Train_font method
    """
    def convert_line_endings(self):
        log.debug("Converting Lines for eng.training_files.txt from CRLF to LF")
        windows_line_endings = b'\r\n'
        unix_line_endings = b'\n'
        filePath = self.TRAININGFILES_DIR + "/eng.training_files.txt"

        with open(filePath, "rb") as file:
            content = file.read()

        content = content.replace(windows_line_endings, unix_line_endings)

        with open(filePath, "wb") as file:
            file.write(content)

        log.debug("Lines Converted Successfully from CRLF to LF")


    """
        Definition: Returns the actual font name of given input font
        input: font file
        output: name string
        references: selectFont method
    """
    def getName(self, font):
        log.debug("Getting name of selected font(s)")
        name = ""
        # print(font['name'].columns)
        for record in font['name'].names:
            if record.nameID == 4 and not name:
                if b'\000' in record.string:
                    name = str(record.string, "utf-16-be").encode("utf-8").decode("utf-8")
                else:
                    name = record.string.decode("utf-8")
                if name:
                    break

        return name


    '''
        Definition: Training Data input dialog, gets called when pressing "Select" button
        input: event object when pressing select button
    '''
    def selectFonts(self, event):
        self.print_log("Selecting Training Data...")
        log.debug("Selecting Training Data")
        dialog = wx.FileDialog(self, message="Choose font(s) ...", wildcard="FontFile (*.ttf)|*ttf", style=wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPaths()
            # NEED TO ADD VALIDATOR
            fontlist = ""
            for path in paths:
                if not self.FONTS_DIR:
                    self.FONTS_DIR = os.path.dirname(path)
                elif self.FONTS_DIR != os.path.dirname(path):
                    self.FONTS_DIR = os.path.dirname(path)
                try:
                    fontname = None
                    fontname = self.getName(ttLib.TTFont(path))
                except Exception as e:
                    self.print_log("File '" + str(path[path.rindex('\\')+1:]) + "' is an invalid font file.")
                    log.debug("File '" + str(path[path.rindex('\\')+1:]) + "' is an invalid font file, ERR_MSG: " +str(e))
                if(fontname) : fontlist += fontname+";"
            self.fontlist = fontlist.strip(";")
            # self.FONTS = '"'+self.fontlist.replace(';', '" "')+'"'
            self.FONTS = self.fontlist.split(";")
            self.fontselect_txtfield.SetValue(self.fontlist)
            if (len(self.FONTS)>0 and self.FONTS[0]!= ''):
                self.print_log("Data Selected: " + str(self.FONTS))
                log.debug("Data Selected: "+ str(self.FONTS))
            else:
                self.print_log("Unable to select data.")
                log.debug("Unable to select data.")
        dialog.Destroy()

    '''
        Definition : saves changes to the config json file after any rollback operation is performed
        input: receives the version and the index value of version in the list
        references: inside rollback method
    '''
    def downgrade_version(self, version, index):
        try:
            log.debug("Writing changes in config.json")
            with open(config_path, "w") as outfile:
                configs['current_version'] = version
                configs["all_versions"] = configs["all_versions"][:index+1]
                str_ = json.dumps(configs, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
                outfile.write(str(str_))

                self.current_version = version
                self.all_versions = configs["all_versions"]
                self.print_log("Downgraded to version: "+str(self.current_version))
                log.debug("Current Version downgraded to: "+self.current_version)
        except Exception as err:
            self.print_log("Failed to write changes to config.json")
            log.error("Failed to write changes to config.json"+str(err))


    '''
        Definition : Upgrades the version info in the config.json file
        Inputs: None
        References: inside start_training method
    '''
    def upgrade_version(self):
        try:
            log.debug("Writing changes to config.json")
            with open(config_path, "w") as outfile:
                # here the version is upgraded from 5.0.x to 5.0.x+1
                all_ver = configs['all_versions']
                temp_list = all_ver[len(all_ver)-1].split(".")
                temp_list[len(temp_list)-1] = str(int(temp_list[len(temp_list)-1]) + 1)
                curr_version = ".".join(temp_list)
                configs['current_version'] = curr_version   # new version is now assigned as current version
                configs['all_versions'].append(str(curr_version)) # new version is appened to all version list

                # new data is saved to config file
                str_ = json.dumps(configs, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
                outfile.write(str(str_))

                # current version of IRISMT is updated
                self.current_version = curr_version
                self.all_versions = configs["all_versions"]
                self.print_log("Upgraded to version: "+str(self.current_version))
                log.debug("Current Version upgraded to: "+self.current_version)
        except Exception as err:
            self.print_log("Failed to write changes in config.json")
            log.error("Failed to write changes in config.json")



    # def get_previous_version(self):
    #     try:
    #         curr_ver = self.current_version
    #         temp_list = curr_ver.split(".")
    #         temp_list[len(temp_list)-1] = str(int(temp_list[len(temp_list)-1]) - 1)
    #         prev_version = ".".join(temp_list)
    #         if prev_version in self.all_versions:
    #             return prev_version
    #         else:
    #             self.print_log("Previous Version not found")
    #             return None
    #     except Exception as err:
    #         print(err, "FAILED TO GET PREVIOUS VERSION")

    '''
        definition: backs up the current eng.traineddata into the model_backup.7z archive along with its version info
        input: none
        references: called during rollback and start_training
    '''
    def backup_current_model(self):
        try:
            log.debug("Backing up current model")
            if os.path.exists(self.active_model):
                log.debug("Renaming current with version to archive")
                os.rename(self.active_model, self.active_model+'_'+self.current_version)
                archive_command = r'{loc_7z} a {store_loc} {source_file}'.format(loc_7z=LOC_7z, store_loc = self.rollback_dir, source_file=self.active_model+'_'+self.current_version)
                subprocess.call(archive_command, shell=True)
                log.debug("Model Backed Up!")
                os.rename(self.active_model+'_'+self.current_version, self.active_model)
                log.debug("Renaming back to original name")
                return 1
            else:
                self.print_log("Recognition model not found in tessdata")
                log.error("Recognition Model not found in tessdata")
                raise Exception
        except Exception as err:
            self.flow_flag = 0
            if os.path.exists(self.active_model+'_'+self.current_version):
                os.rename(self.active_model+'_'+self.current_version, self.active_model)
                log.debug("Exception Occured , renaming back to original")
            self.print_log("Failed to backup current recognition model")
            log.error("Failed to backup current recognition model")
            return 0



    '''
        Definition: this method gets called by "TRAIN" button and internally calls every method to train the tesseract
        Input: event object from the train button
    '''
    def start_training(self, event):
        if self.current_version == "5.0.0":
            # if current version is 5.0.0, tesseract contains int model in the tessdata but we need float model so we fetchit from tessdata/best
            self.TRAINEDDATA_DIR = AVO_ASSURE_HOME + configs["traineddata_dir"]
        else:
            # all the other versions are built upon the float model so they are fetch from tessdata only
            self.TRAINEDDATA_DIR = AVO_ASSURE_HOME + configs["trained_result"]

        if not os.path.exists(self.CHECKPOINT_DIR):
            log.debug("Creating Checkpoint folder")
            os.mkdir(self.CHECKPOINT_DIR)   # checkpoint files are generated after training and thus stored here
            log.debug("Checkpoint folder created")
        if self.fontselect_txtfield.GetValue() in ["", None]:
            # if the font field is non ie no font is selected. do not proceed
            self.print_log("Training data cannot be empty!")
            log.error("Training data cannot be empty.")
            return

        log.debug("----Training Started----")

        self.msg.StartThread(self.msg.showProgress)
        self.comm_obj.percentageIncri(self.msg,5,"Backing Up Current Data...")
        self.backup_current_model()

        failed_fonts = []
        for font in self.FONTS:
            self.comm_obj.percentageIncri(self.msg,10,"Generating Training Files for "+str(font)+"...")
            failed_flag, failed_font = self.generate_training_files(str("\""+font+"\""))
            if failed_flag:
                failed_fonts.append(failed_font)

        if len(failed_fonts) == len(self.FONTS):
            self.flow_flag = 0


        self.comm_obj.percentageIncri(self.msg,20,"Extracting Old Model...")
        self.extract_old_model()
        self.comm_obj.percentageIncri(self.msg,30,"Training the Data...")
        self.train_font()
        self.comm_obj.percentageIncri(self.msg,80,"Combining Checkpoint Files...")
        self.combine_checkpoint_files()
        if not self.flow_flag:
            self.comm_obj.percentageIncri(self.msg,100,"Training Failed for"+str(font)+"... ")
            # self.msg.ShowMessage("Training Failed!")
            self.remove_temporary_files()
            self.flow_flag = 1
            self.print_log("-"*20+"Training Failed"+"-"*20)
            return
        self.comm_obj.percentageIncri(self.msg,90,"Saving Changes in Config Files...")
        self.upgrade_version()
        self.reset_dropdown()
        self.comm_obj.percentageIncri(self.msg,95,"Removing Temporary Files...")
        self.remove_temporary_files()
        self.comm_obj.percentageIncri(self.msg,100,"Finished Training!")
        self.flow_flag = 1
        # self.msg.ShowMessage("Data Trained Successfully!")
        self.print_log("-----Data Trained Successfully-----")
        #clearing the traning-data selection textbox
        self.fontselect_txtfield.Clear()
        self.revert_btn.Enable()

    '''
        Definition : this method generates the required .lstmf files / training files
        input: None
        Reference: inside start_training method
    '''
    def generate_training_files(self, FONT):
        if not self.flow_flag:
            log.error("Error occured, cannot generate training files")
            return
        try:
            log.debug("----Generating Training Files----")
            failed_flag = 0
            failed_font = None
            BASE_CMD_TRAIN = 'python {TRAININGTOOL_DIR}/tesstrain.py \
                        --fonts_dir {FONTS_DIR} \
                        --lang {LANG} \
                        --linedata_only \
                        --noextract_font_properties \
                        --langdata_dir {LANGDATA_DIR} \
                        --tessdata_dir {TESSDATA_DIR} \
                        --output_dir {TRAININGFILE_DIR} \
                        --fontlist {FONTS}'

            F_DIR = self.FONTS_DIR
            if ' ' in F_DIR:
                F_DIR = '"'+F_DIR+'"'
            CMD_TRAIN = BASE_CMD_TRAIN.format(TRAININGTOOL_DIR = self.TRAININGTOOL_DIR,
                                    FONTS_DIR = F_DIR,
                                    LANG = self.LANG,
                                    LANGDATA_DIR = self.LANGDATA_DIR,
                                    TESSDATA_DIR = self.TESSDATA_DIR,
                                    TRAININGFILE_DIR = self.TRAININGFILES_DIR,
                                    FONTS = FONT)

            self.print_log("Generating Training Files...")
            err = os.system(CMD_TRAIN)
            if err:
                log.error("Error Occured in Training Files Command Line")
                raise Exception
            self.convert_line_endings() # converts the windows line endings to unix line endings
            # conversion is necessary for training files to work
            self.print_log("Training Files Generated for "+FONT)
            log.debug("Training files generate for "+FONT)
        except Exception as err:
            failed_flag = 1
            failed_font = FONT
            log.error("Failed to generate Training Files for "+FONT)
            self.print_log("Failed to generated Training Files for " +FONT)

        return failed_flag, FONT


    '''
        Definition: This method extracts the .lstm model file from the current eng.traineddata
                    Doing this helps us to resume the training from the old model and
                    build up our new data onto the old data
        Inputs: None
        References: start_training method
    '''
    def extract_old_model(self):
        if not self.flow_flag:
            log.error("Error Occured, Cannot Extract LSTM Model")
            return
        try:
            log.debug("----Extracting old Model form traineddata----")
            BASE_CMD_EXTRACT_MODEL = 'combine_tessdata -e {TRAINEDDATA_DIR} {MODEL}'
            CMD_EXTRACT_MODEL = BASE_CMD_EXTRACT_MODEL.format(TRAINEDDATA_DIR = self.TRAINEDDATA_DIR, MODEL = self.CHECKPOINT_DIR+"/eng.lstm")
            self.print_log("Extracting old recognition model from traineddata")
            err = os.system(CMD_EXTRACT_MODEL)
            if err:
                log.error("Error occured in extraction command line")
                raise Exception
            self.print_log("Old recognition model Extracted")
            log.debug("Old recognition model extracted.")
        except Exception as err:
            self.flow_flag = 0
            log.error("Failed in extracting model from traineddata")
            self.print_log("Failed in extracting model from traineddata")


    '''
        Definition : this method performs the training operation.
                    It generates the checkpoint files which is trained model for our new data
        Input: None
        Reference: start_training method
    '''
    def train_font(self):
        if not self.flow_flag:
            log.error("Error Occured, Cannot Train Font")
            return
        try:
            log.debug("----TRAINING FONT----")
            BASE_CMD_TRAIN_FONT = 'lstmtraining \
                                    --model_output {CHECKPOINT_FILE} \
                                    --continue_from {EXTRACTED_MODEL} \
                                    --traineddata {TRAINEDDATA_DIR} \
                                    --train_listfile {TRAINING_FILE} \
                                    --max_iterations {ITERATIONS}'

            CMD_TRAIN_FONT = BASE_CMD_TRAIN_FONT.format(CHECKPOINT_FILE = self.CHECKPOINT_DIR + "/base",
                                                EXTRACTED_MODEL = self.CHECKPOINT_DIR + "/eng.lstm",
                                                TRAINEDDATA_DIR = self.TRAINEDDATA_DIR,
                                                TRAINING_FILE = self.TRAININGFILES_DIR + "/eng.training_files.txt",
                                                ITERATIONS = self.ITERATIONS
                                                )

            self.print_log("Training with new Data...")
            err = os.system(CMD_TRAIN_FONT)
            if err:
                log.error("Error Occured in Training Command Line")
                raise Exception
            self.print_log("Data Trained")
            log.debug("Data Trained Successfully")
        except Exception as err:
            self.flow_flag = 0
            log.error("Failed to Train new Model")
            self.print_log("Failed in Training new Model")


    '''
        Definition: This method combines the checkpoint files into a trained data file : eng.traineddata
        Input: None
        Reference: start_training method
    '''
    def combine_checkpoint_files(self):
        if not self.flow_flag:
            log.error("Error Occured, Cannot Combine checkpoint files")
            return
        try:
            log.debug("----Combining Checkpoint Files----")
            BASE_CMD_COMBINE = 'lstmtraining \
                                --stop_training \
                                --continue_from {CHECKPOINT_FILE} \
                                --traineddata {TRAINEDDATA_DIR} \
                                --model_output {RESULT_DATA}'

            CMD_COMBINE = BASE_CMD_COMBINE.format(CHECKPOINT_FILE = self.CHECKPOINT_DIR + "/base_checkpoint",
                                            TRAINEDDATA_DIR = self.TRAINEDDATA_DIR,
                                            RESULT_DATA = self.TRAINED_RESULT)

            self.print_log("Finalizing process. Combining checkpoint files.")
            err = os.system(CMD_COMBINE)
            if err:
                log.error("Error occured in combining command line")
                raise Exception
            self.print_log("Checkpoint files combined.")
            log.debug("Checkpoint files combined successfully")
        except Exception as err:
            self.flow_flag = 0
            log.error("Failed in combining checkpoint files")
            self.print_log("Failed in Combining checkpoint files.")


    '''
        Definition: This method deletes the files generated throughtout the process which are now of no use to us
        Input: None
        Reference: start_training method
    '''
    def remove_temporary_files(self):
        self.print_log("Cleaning Temporary Files.")
        log.debug("Cleaning Temporary Files.")
        if os.path.exists(self.CHECKPOINT_DIR):
            shutil.rmtree(self.CHECKPOINT_DIR)
        if os.path.exists(self.TRAININGFILES_DIR):
            shutil.rmtree(self.TRAININGFILES_DIR)
        self.print_log("Temporary Files Cleaned.")
        log.debug("Temporary Files Cleaned.")

    def print_log(self, msg):
        self.log.AppendText(str(msg)+"\n")


class Message(wx.Frame):
    """Class for progress window"""
    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        self.InitUI()
        self.maxPercent = 100
        self.percent = 0

    def InitUI(self):
        self.SetSize((300, 200))
        self.SetTitle('Updating')
        self.Centre()

    def StartThread(self, func, *args):
        thread = threading.Thread(target = func, args = args)
        thread.setDaemon(True)
        thread.start()

    def showProgress(self):
        self.progress = wx.ProgressDialog("Progress Window", "Please wait.", maximum = self.maxPercent, parent = self, style = wx.PD_SMOOTH|wx.PD_AUTO_HIDE)

    def destoryProgress(self):
        self.progress.Destroy()

    def updateProgress(self, percent):
        keepGoing = True
        time.sleep(1)
        while keepGoing and self.percent < percent:
            self.percent += 1
            (keepGoing, skip) = self.progress.Update(self.percent)
            time.sleep(0.1)

    def progIncrement(self, take_time, taskPercent,update_msg):
        time.sleep(take_time)
        (keepGoing, skip) = self.progress.Update(taskPercent, update_msg)

    def ShowMessage(self, msg):
        dlg = wx.MessageBox(msg, 'Info',
            wx.OK | wx.ICON_INFORMATION)
        if (dlg == 4 ):
            self.Close()

    def destroyObject(self):
        self.Close()

class common_functions:
    def __init__(self):
        pass

    def percentageIncri(self,msg,taskPercent,update_msg):
        msg.StartThread(msg.updateProgress, taskPercent)
        msg.progIncrement(1, taskPercent,update_msg)





def main():
    '''
        The Training Procedure:
        1. The current data file is backed up so that it can be recovered later.
        2. The Training files are generated by tesseract tool tesstrain.py
            It generates the tif-box pair files and the serialized document .lstmf file
            These are required by tesseract to train the new data
            The files it generates sometimes can have windows line endings so it is important to convert all line endings to unix format
        3. Old Recognition model (.lstm) is extracted from the compressed data file (.traineddata)
            It is important because our new data training will be resumed from this old model
        4. The Training of our data:
            train_fonts method performs the main training procedure. It is also the most time taking task
            It take the generated files from step 2 and goes through a number of iterations to train our new data.
            The optimal iterations is 400 but we can increase or decrease the iterations based on requirements
            -> Generates the checkpoint files.
                Checkpoint files are our newly trained data but it has to be combined into a one single compressed data file before use
        5. Combine checkpoint files is then performed to combine the files generated in our previous step.
            It generates the data file to the result directory
        6. All the final steps are then executed such as updating combobox, config.json file, and
                temporary files are deleted such as checkpoint files and files from step 2.
    '''


    '''
        Rollback:
        1. The current data file is renamed to include the version in its name
        2. Then It is added to mode_backup.7z
        3. Required data file is extracted from the 7z file
        4. The extracted file will have the version info in its name which will be renamed back to original
        5. Now All the version files newer than the version file to which we rolled back will be deleted and combobox is updated
    '''
    app = wx.App()
    comm_obj = common_functions()
    msg = Message(None)
    f = IRISMT(comm_obj, msg)
    app.MainLoop()




if __name__ == '__main__':
    main()