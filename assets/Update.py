#-------------------------------------------------------------------------------
# Name:        Updater/Rollback Module
# Purpose for update:     Does the following functions
#                   1.Create a backup of Avo Assure ICE (plugins folder) and the about manifest
#                   2.Download files from End Point URL location to temp folder.
#                   3.Unpack the files and replace them in AvoAssure directory.
#                   4.Once all files have been replaced, delete the file from temp directory.
#                   5.If minor changes then perform steps 1-3(while sequentially calling the zip files)
#                   6.If major changes take the base package of the major version, then perform minor operations.
#                   7.Once all changes are completed stop and close ICE
#                   8.Close Client_updater module
# Purpose for rollback:     Does the following functions
#               1. Close ICE
#               2. Delete Avo Assure ICE Folder and client manifest
#               3. Unpack AvoAssureICE_backup.7z in ICE directory
#               4. Delete the rollback
#               5. Update in client manifest
#               6. Restart ICE
#
#
# Notes : For more info on 7zip via cmd refer : https://www.dotnetperls.com/7-zip-examples
#
#
#
# Author:      anas.ahmed
#
# Created:     18-02-2019
# Copyright:   (c) anas.ahmed 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import shutil
import tempfile
import subprocess
import sys
import json
import requests
import win32gui
import win32con
import wx
import threading
import time
import hashlib
#-------------------------------------------logging
import logging
import datetime
date_obj = datetime.datetime.now()
conf = open(os.path.normpath(str(os.getcwd())+"/assets/config.json"), 'r')
params = json.load(conf)
conf.close()
log_loc = params['logFile_Path'][:params['logFile_Path'].rindex('\\')]
if not ( os.path.isdir(str(log_loc)) and os.path.exists(str(log_loc)) ):
    os.mkdir(str(log_loc))
LOG_FILEPATH = str(log_loc) + '\\Updater_logs_' + str(date_obj.year) + '_' + str(date_obj.month) + '_' + str(date_obj.day) + '_' + str(date_obj.hour) + str(date_obj.minute) + '.log'
logging.basicConfig(filename = LOG_FILEPATH, level = logging.DEBUG)
try:
    log = logging.getLogger("Updater.py")
except:
    log = logging.getLogger("Updater.exe")
#-------------------------------------------logging

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

    def ShowMessage(self,warning=None):
        if (warning=='rollback'): dlg = wx.MessageBox("Avo Assure ICE rolled back successfully. Click 'OK' start ICE.", 'Info',wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
        elif (warning and 'Error!: unable to add files to backup' in warning) : dlg = wx.MessageBox("Avo Assure ICE failed to update due to files being used by another process. Click 'OK' to start ICE.", 'Error',wx.OK | wx.ICON_EXCLAMATION | wx.CANCEL)
        elif (warning) : dlg = wx.MessageBox("Avo Assure ICE updated with warnings. Click 'OK' to start ICE.", 'Info',wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
        else : dlg = wx.MessageBox("Avo Assure ICE updated successfully. Click 'OK' to start ICE.", 'Info',wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
        if (dlg == 4 or dlg == 16):
            self.Close()
        return dlg

class getProxy():

    def __init__(self):
        self.proxy_path = os.path.normpath(str(os.getcwd())+"/assets/proxy.json")

    def readJson(self):
        if os.path.isfile(self.proxy_path)==True:
            try:
                conf = open(self.proxy_path, 'r')
                proxy = json.load(conf)
                conf.close()
                if 'enabled' in proxy and proxy['enabled'] == 'Enabled':
                    scheme = 'http'
                    if proxy['url'][0:7] == "http://":
                        proxy['url'] = proxy['url'][7:]
                    elif proxy['url'][0:9] == "https://":
                        scheme = 'https'
                        proxy['url'] = proxy['url'][8:]
                    proxy['password'] = self.unwrap(proxy['password'])
                    proxy_url = scheme + "://" + proxy['username']+":"+proxy['password']+"@"+proxy['url']
                    proxies = {
                        "http": proxy_url,
                        "https": proxy_url
                    }
                elif 'enabled' in proxy and proxy['enabled'] == 'Disabled':
                    proxies = {}
                else:
                    proxies = None
            except Exception as e:
                log.error(e,exc_info=True)
        return proxies

    def unwrap(self, enc):
        import base64
        from Crypto.Cipher import AES
        unpad = lambda s : s[0:-ord(s[-1])]
        enc = base64.b64decode(enc)
        cipher = AES.new(b'\x74\x68\x69\x73'+b'\x49\x73\x41\x53\x65'+b'\x63\x72\x65\x74\x4b\x65\x79', AES.MODE_ECB)
        return unpad(cipher.decrypt(enc).decode('utf-8'))

class Updater:
    def __init__(self):
        #------------initialization
        """Initializing class variables"""
        log.info( 'Initializing all class variables.' )
        self.vers_aval= {} #versions avaliable to the client
        self.ver_client = {} #clinet version
        self.loc_7z = None
        self.extraction_loc = None
        self.SERVER_LOC = None
        self.temp_location = None
        log.info( 'All class variables initialized.' )

    def assignment(self,datatags_file_loc,ver_client,SERVER_LOC,extraction_loc,loc_7z):
        """Assigning value to class variables"""
        #-----------------assignment
        with open(datatags_file_loc) as f:
            content = f.read()
        os.remove(datatags_file_loc)
        log.info( 'Assigning all class variables.' )
        self.vers_aval = json.loads(content.replace("'",'"'))
        log.info( '=>Versions avaliable : ' + str(self.vers_aval))
        self.ver_client = ver_client
        log.info( '=>Client Version : ' + str(self.ver_client))
        self.loc_7z = loc_7z
        log.info( '=>7z location : ' + str(self.loc_7z))
        self.extraction_loc = extraction_loc
        log.info( '=>Extraction Location : ' + str(self.extraction_loc))
        self.SERVER_LOC = SERVER_LOC
        log.info( '=>Server Path : ' + str(self.SERVER_LOC))
        log.info( 'All class variables assigned.' )

    def create_backup(self):
        """Purpose: To create a backup of Avo Assure ICE folder and about_manifest"""
        """Input : 1.7-zip location 2.Avo Assure ICE folder location and about_manifest.json location 3.Rollbackfile location"""
        """Functionality: 1.Checks is Update folder is present in ICE directory, if present checks if AvoAssureICE_backup.7z is present
                          2.If AvoAssureICE_backup.7z is present, then delete this instance to create a new once(we do this so as not to keep appending new files to the existing 7zip file)
                          3.If Update folder is not present then creates a new folder by the same name in ICE directory
                          4.Adds Avo Assure (plugins) folder to AvoAssureICE_backup.7z
                          5.Adds about_manifest.json to AvoAssureICE_backup.7z"""
        try:
            err_msg = None
            log.debug( 'Inside create_backup function' )
            #--------------------------------------------check if Update folder exists
            if ( os.path.exists(self.extraction_loc + "\\assets\\AvoAssureICE_backup.7z") ):
                #rename AvoAssureICE_backup.7z -> AvoAssureICE_backup_temp.7z
                os.rename(str(self.extraction_loc + "\\assets\\AvoAssureICE_backup.7z"), str(self.extraction_loc + "\\assets\\AvoAssureICE_backup_temp.7z"))
                log.debug( 'AvoAssureICE_backup.7z already exists, and renaming AvoAssureICE_backup.7z' )
                time.sleep(1)
            print ( '=>Creating new Avo Assure ICE backup instance' )
            store_loc = self.extraction_loc+"\\assets\\AvoAssureICE_backup.7z"
            source_ice = self.extraction_loc +'\\plugins'
            source_client_manifest = self.extraction_loc +'\\assets\\about_manifest.json'

            """Adding plugins folder to archive"""
            log.debug( 'Adding ' + source_ice + " to archive" )
            archive_command = r'"{}" a "{}" "{}"'.format(self.loc_7z, store_loc, source_ice)
            sp1 = subprocess.Popen(archive_command, stderr = subprocess.PIPE, stdout = subprocess.PIPE, stdin=subprocess.PIPE,shell =True)
            out = sp1.communicate()[0].decode('utf-8')
            if ( "The process cannot access the file because it is being used by another process" in out ):
                err_msg = 'Error!: unable to add files to backup. Backup-process failed as it cannot access the files in '+ str(source_ice) + ' as the files are being used by a different process'
                log.error( err_msg )
            else:
                log.debug( 'Success : Added ' + source_ice + " to archive" )

            """Adding about_manifest file to archive"""
            log.debug( 'Adding '+source_client_manifest+ " to archive" )
            archive_command = r'"{}" a "{}" "{}"'.format(self.loc_7z, store_loc, source_client_manifest)
            sp1 = subprocess.Popen(archive_command, stderr = subprocess.PIPE, stdout = subprocess.PIPE, stdin=subprocess.PIPE,shell =True)
            out = sp1.communicate()[0].decode('utf-8')
            if ( "The process cannot access the file because it is being used by another process" in out ):
                err_msg = 'Error!: unable to add files to backup. Backup-process failed as it cannot access '+ str(source_client_manifest) + ' as this file is being used by a different process'
                log.error( err_msg )
            else:
                log.debug( 'Success : Added ' + source_client_manifest + " to archive" )
            if (err_msg):
                #if files are open first remove the current AvoAssureICE_backup
                if ( os.path.exists(self.extraction_loc + "\\assets\\AvoAssureICE_backup.7z") ):
                    log.debug( 'AvoAssureICE_backup.7z already exists, removing AvoAssureICE_backup.7z' )
                    os.remove(self.extraction_loc + "\\assets\\AvoAssureICE_backup.7z")
                    log.debug( 'AvoAssureICE_backup.7z removed succefully' )
                    time.sleep(1)
                #rename AvoAssureICE_backup_temp.7z -> AvoAssureICE_backup.7z
                os.rename(str(self.extraction_loc + "\\assets\\AvoAssureICE_backup_temp.7z"), str(self.extraction_loc + "\\assets\\AvoAssureICE_backup.7z"))
            else:
                if ( os.path.exists(self.extraction_loc + "\\assets\\AvoAssureICE_backup_temp.7z") ):
                    os.remove(self.extraction_loc + "\\assets\\AvoAssureICE_backup_temp.7z")
                log.debug( 'Successfully created backup of Avo Assure ICE' )
        except Exception as e:
            err_msg = "Error!: unable to add files to backup"
            print ( "Error occurred in create_backup : ", e )
            log.error( "Error occurred in create_backup : " + str(e) )
            import traceback
            traceback.print_exc()
        return err_msg

    def end_point_builder(self,new_version_list):
        """Builds the end point url of the file to download"""
        end_points_list = []
        try:
            log.debug( 'Inside end_point_builder function' )
            log.info( "Building the end point URL's" )
            print ( "=>Building the end point URL's" )
            for ver in new_version_list:
                end_points_list.append(str(self.SERVER_LOC) + '.'.join(ver.split('.')[:2]) + '/' + 'AvoAssure_ICE_' + str(ver) +'.zip')
            print ( "=>End Point URL's are built : ", str(end_points_list) )
            log.info( "End Point URL's are built : " + str(end_points_list) )
        except Exception as e:
            print ( "Error occurred in end_point_builder : ", e )
            log.error( "Error occurred in end_point_builder : " + str(e) )
            import traceback
            traceback.print_exc()
        return end_points_list

    def get_update_files(self):
        """Calculating which directory to update from. Based on that navigates to that particular directory
            Any changes made in versioning need no be implemented here"""
        try:
            log.debug( 'Inside get_update_files function' )
            """
            rule:
            1.get both current version list and get newer version versions,
            2.check for the latest baseline avaliable in new_version_list, from baseline True till latest baseline False
            3.if Baseline = Flase throughout newer version/same version , update from current version till the latest
            Note : we assume that the version list has already been checked for min,max server versions in update_module.py/pyd
            Eg: self.vers_aval = {'3.0.2':['3.0','False','<sha256 of file>'], '3.0.11':['3.0','False','<sha256 of file>'], '3.0.1':['3.0','False','<sha256 of file>'], '3.0.0':['3.0','False','<sha256 of file>'], '2.0.123':['2.0','False','<sha256 of file>'], '2.0.124':['2.0','False','<sha256 of file>'], '2.0.125':['2.0','False','<sha256 of file>']}
            Eg: self.ver_client = {'3.0.2':['3.0']}
            """
            NVL = []
            new_dict={}

            def replaceF1(NVL):
                """Replacing '-rc.' with '.' in each list item  - why are we doing this -  packaging(version),distutils.version(LooseVersion and StrictVersion) is inconsistant with python 3.7.X """
                newNVL = []
                for i in NVL:
                    newNVL.append(i.replace("-rc.","."))
                return newNVL

            def replaceF2(NVL):
                """Replacing  the 3rd '.' with '-rc.' in each list item - why are we doing this - to refer to correct downloading package """
                newNVL = []
                for i in NVL:
                    c = i.count('.')
                    if c == 3:
                        newNVL.append(i[0:i.rindex('.')]+'-rc.'+i[i.rindex('.')+1:])
                    else:
                        newNVL.append(i)
                return newNVL

            for i in self.vers_aval:
                #1.get both current version list and newer version list
                if ( float(self.vers_aval[i][0]) >= float(list(self.ver_client.values())[0][0]) ):
                    print('=>newer version/same version')
                    new_dict.update( {str(i) : self.vers_aval[i]} )
                    NVL.append(i)
                else:
                    print ('=>older prod version')

            #check if rc in list
            flg = False
            for i in NVL:
                if 'rc' in str(i):
                    flg = True
                    break
            if (flg):
                NVL = replaceF1(NVL)
                NVL.sort(key=lambda s:list(map(int, s.split('.'))),reverse=True)
                NVL = replaceF2(NVL)
            else: NVL.sort(key=lambda s:list(map(int, s.split('.'))),reverse=True) # sort list in order

            #get from after current client version and excludes older versions
            nNVL=[]
            for i in range(0,len(NVL)):
                if (NVL[i]==list(self.ver_client.keys())[0]):
                    nNVL=NVL[0:i]
                    break

            #2.baseline list
            new_version_list=[]
            for i in range(0,len(nNVL)):
                if (str(new_dict[nNVL[i]][1]).lower()=='true'):
                    new_version_list=nNVL[0:i+1]
                    break

            #3.no new baseline found
            if not (new_version_list):
                new_version_list=nNVL[:]

            if (flg):
                new_version_list = replaceF1(new_version_list)
                new_version_list.sort(key=lambda s:list(map(int, s.split('.')))) # sort list in order
                new_version_list = replaceF2(new_version_list)
            else: new_version_list.sort(key=lambda s:list(map(int, s.split('.')))) # sort list in order
            print ( '=>Number of changes that happened since then ( lastest delta changes ) : ', str(new_version_list)  )
            log.info( 'Number of changes that happened since then ( lastest delta changes ) : ' + str(new_version_list) )
        except Exception as e:
            print ( "Error occurred in get_update_files : ", e )
            log.error( "Error occurred in get_update_files : " + str(e) )
            import traceback
            traceback.print_exc()
        return new_version_list

    def download_files(self,end_point_list):
        """downloads files from the generated endpoints list"""
        warning_msg = None
        proxies_val = getProxy().readJson()
        try:
            log.debug( 'Inside download_files function' )
            self.temp_location = tempfile.gettempdir()
            for url in end_point_list:
                filename = url[url.rindex('/')+1:]
                temp_file_path = os.path.join(self.temp_location, filename)
                fileObj = requests.get(str(url),verify=False,proxies=proxies_val)
                if(fileObj.status_code == 200):
                    open(temp_file_path, 'wb').write(fileObj.content)
                    print ('=>performing sha256 check')
                    if (self.sha256_check(filename,temp_file_path)):
                        print ('=>sha256 check PASS')
                        print ('=>navigating to extract_files')
                        self.extract_files(temp_file_path)
                        print ('=>deleting the extracted file')
                        self.delete_temp_file(temp_file_path)
                        print (str(filename), ' was extracted and deleted')
                    else:
                        warning_msg = "Warning!: attempt to download further has been disabled due to sha256 mismatch of file : " + str(filename)
                        print('=>sha256 check FAIL: attempt to download further has been disabled due to sha256 mismatch.')
                        log.error( warning_msg )
                        print ('=>deleting the extracted file')
                        self.delete_temp_file(temp_file_path)
                        print (str(filename), ' was extracted and deleted')
                        break
                else:
                    warning_msg = "Warning!: attempt to download further has been disabled due to end-point not being found : " + str(filename) + ". Status Code: " + str(fileObj.status_code)
                    print('=>End point check FAIL: attempt to download further has been disabled due to end-point not being found. Status Code: ' + str(fileObj.status_code))
                    log.error( warning_msg )
                    break
        except Exception as e:
            print ( "Error occurred in download_files : ", e )
            log.error( "Error occurred in download_files : " + str(e) )
            import traceback
            traceback.print_exc()
        return warning_msg

    def sha256_check(self,filename,temp_file_path):
        log.debug( 'Inside sha256_check function' )
        """This function should 1.Generate sha256 value of file downloaded
                                2.Should compare this sha256 value to the respective sha256 value in manifest.json
                                3.if matched then should proceed as normal
                                4.if sha256 values dont match then a.generate and log an error message
                                                                    b.Stop the process to download the next patch of end_point_list"""
        def get_live_sha256(temp_file_path):
            log.debug( 'Inside get_live_sha256 function' )
            sha256 = None
            try:
                hashobj = hashlib.sha256()
                with open(temp_file_path,"rb") as f:
                    # Read and update hash string value in blocks of 4K
                    for byte_block in iter(lambda: f.read(4096),b""):
                        hashobj.update(byte_block)
                    sha256 = hashobj.hexdigest()
            except Exception as e:
                print ( "Error occoured in get_live_sha256 : ", e )
                log.error( "Error occoured in get_live_sha256 : " + str(e) )
                import traceback
                traceback.print_exc()
            print( '=>Completed generating sha256 of file :', temp_file_path )
            log.info( 'Completed generating sha256 of file : ' + str(temp_file_path) )
            return sha256
        filename = filename[filename.rindex('_')+1:]#AvoAssure_ICE_X.Y.Z.zip is stripped to X.Y.Z.zip to match in self.vers_aval
        manifest_sha256 = self.vers_aval[filename[:filename.index('.zip')]][2] #get the sha256 value of the file from manifest.json
        live_sha256 = get_live_sha256(temp_file_path)
        if ( manifest_sha256 == live_sha256 ): return True
        else:
            print( '=>Error : sha256 of downloaded file ' + filename + 'does not match the sha256 in manifest.json' )
            log.error( 'Error : sha256 of downloaded file ' + filename + 'does not match the sha256 in manifest.json' )
            return False

    def extract_files(self, temp_file_path):
        """get to portable 7z and open the cmd #2.EXTRACT TO DESTINATION"""
        try:
            log.debug( 'Inside extract_files function' )
            extract_command = r'"{}" x "{}" -o"{}" -y'.format( self.loc_7z, temp_file_path, os.path.dirname(self.extraction_loc) )
            subprocess.call(extract_command, shell = True )
            print( '=>Completed extraction of package at :', self.temp_location )
            log.info( 'Completed extraction of package at : ' + str(self.temp_location) )
        except Exception as e:
            print( '=>Extraction could not complete \n' )
            print ( "Error occurred in extract_files : ", e )
            log.error( "Error occurred in extract_files : " + str(e) )
            import traceback
            traceback.print_exc()

    def delete_temp_file(self,temp_file_path):
        """delete file from temp location"""
        try:
            log.debug( 'Inside delete_temp_file function' )
            print( '=>Deleting file : ', temp_file_path )
            log.info( 'Deleting file : ' + str(temp_file_path) )
            os.remove(temp_file_path)
            print( '=>Temp file deleted' )
            log.info( 'Temp file : ' + str(temp_file_path) + ' deleted.' )
        except Exception as e:
            print ( "Error occurred in delete_temp_file : ", e )
            log.error( "Error occurred in delete_temp_file : " + str(e) )
            import traceback
            traceback.print_exc()

class Rollback():
    """Code modifications done here"""

    def __init__(self):
        """Initializing class variables"""
        self.ROLLBACK_LOC = None
        self.AVOASSUREICE_LOC = None
        self.loc_7z = None
        pass

    def backup_check(self):
        res = False
        try:
            res = os.path.exists(self.ROLLBACK_LOC)
            if ( res == True ):
                print( '=>AvoAssureICE_backup.7z exists, in location : ' + str(self.ROLLBACK_LOC) )
                log.info( "AvoAssureICE_backup.7z exists, in location : " + str(self.ROLLBACK_LOC) )
            elif ( res == False ):
                print( '=>AvoAssureICE_backup.7z does not exist, in location : ' + str(self.ROLLBACK_LOC) )
                log.info( "AvoAssureICE_backup.7z does not exist, in location : " + str(self.ROLLBACK_LOC) )
        except Exception as e:
            print ( "=>Error occurred in backup_check : ", e )
            log.error( "Error occurred in backup_check : " + str(e) )
            import traceback
            traceback.print_exc()
        return res

    def assignment(self,AVOASSUREICE_LOC,loc_7z):
        """Assigning value to class variables"""
        self.ROLLBACK_LOC = AVOASSUREICE_LOC+"\\assets\\AvoAssureICE_backup.7z"
        log.info( '=>Rollback location : ' + str(self.ROLLBACK_LOC))
        self.AVOASSUREICE_LOC = AVOASSUREICE_LOC
        log.info( '=>Avo Assure ICE location : ' + str(self.AVOASSUREICE_LOC))
        self.loc_7z = loc_7z
        log.info( '=>7z location : ' + str(self.loc_7z))

    def delete_old_instance(self):
        """Removing old Avo Assure ICE and client manifest"""
        try:
            log.debug( 'Inside delete_old_instance function' )
            #-----------------------------------------deleting Avo Assure ICE folder and its contents
            print( '=>Deleting : ',self.AVOASSUREICE_LOC+"\\plugins" )
            log.info( 'Deleting : ' + str(self.AVOASSUREICE_LOC+"\\plugins") )
            shutil.rmtree(self.AVOASSUREICE_LOC+"\\plugins", ignore_errors=False, onerror=None)
            print( '=>Deleted : ',self.AVOASSUREICE_LOC+"\\plugins" )
            log.info( 'Deleted : ' + str(self.AVOASSUREICE_LOC+"\\plugins") )
            #-------------------------------------------deleting client manifest
            print( '=>Deleting : ',self.AVOASSUREICE_LOC+"\\assets\\about_manifest.json" )
            log.info( 'Deleting : ' + str(self.AVOASSUREICE_LOC+"\\assets\\about_manifest.json") )
            os.remove(self.AVOASSUREICE_LOC+"\\assets\\about_manifest.json")
            print( '=>Deleted : ',self.AVOASSUREICE_LOC+"\\assets\\about_manifest.json" )
            log.info( 'Deleted : ' + str(self.AVOASSUREICE_LOC+"\\assets\\about_manifest.json") )
        except Exception as e:
            print ( "=>Error occurred in delete_old_instance : ", e )
            log.error( "Error occurred in delete_old_instance : " + str(e) )
            import traceback
            traceback.print_exc()

    def rollback_changes(self):
        """get to portable 7z and open the cmd #2.EXTRACT TO DESTINATION"""
        try:
            log.debug( 'Inside rollback_changes function' )
            extract_command = r'"{}" x "{}" -o"{}" -y'.format( self.loc_7z, self.ROLLBACK_LOC, self.AVOASSUREICE_LOC )
            subprocess.call(extract_command, shell = True )
            print( '=>Completed extraction of package at :', self.AVOASSUREICE_LOC )
            log.info( 'Completed extraction of package at : ' + str(self.AVOASSUREICE_LOC) )
        except Exception as e:
            print( '=>Extraction could not complete \n' )
            print ( "=>Error occurred in rollback_changes : ", e )
            log.error( "Error occurred in rollback_changes : " + str(e) )
            import traceback
            traceback.print_exc()

    def delete_rollback(self):
        """Removing old Avo Assure ICE and client manifest"""
        try:
            log.debug( 'Inside delete_rollback function' )
            #--------------------------------------deleting AvoAssureICE_backup.7z
            print( '=>Deleting : ',self.ROLLBACK_LOC )
            log.info( 'Deleting : ' + str(self.ROLLBACK_LOC) )
            os.remove(self.ROLLBACK_LOC)
            print( '=>Deleted : ',self.ROLLBACK_LOC )
            log.info( 'Deleted : ' + str(self.ROLLBACK_LOC) )
        except Exception as e:
            print ( "=>Error occurred in delete_rollback : ", e )
            log.error( "Error occurred in delete_rollback : " + str(e) )
            import traceback
            traceback.print_exc()


    def update_client_manifest(self):
        """Modify the client manifest"""
        try:
            log.debug( 'Inside modify_client_manifest function' )
            path= str(self.AVOASSUREICE_LOC + "/about_manifest.json")
            with open(path) as json_file:
                json_decoded = json.load(json_file)
            json_decoded['rollback'] = 'True'
            json_decoded['rollback_on'] =str(date_obj.day)+'/'+str(date_obj.month)+'/'+str(date_obj.year)+', '+str(date_obj.hour)+':'+str(date_obj.minute)+':'+str(date_obj.second)
            with open(path, 'w') as json_file:
                json.dump(json_decoded, json_file)
            #---------------------------------------------move about_manifest to assets.
            shutil.move(self.AVOASSUREICE_LOC+"\\about_manifest.json", self.AVOASSUREICE_LOC+"\\assets\\about_manifest.json")
        except Exception as e:
            print ( "=>Error occurred in modify_client_manifest : ", e )
            log.error( "Error occurred in modify_client_manifest : " + str(e) )
            import traceback
            traceback.print_exc()

class common_functions:
    def __init__(self):
        pass

    def close_ICE(self,PID):
        """Killing ICE via PID"""
        try:
            log.debug( 'Inside close_ICE function')
            hwnd = win32gui.FindWindow(None, 'Avo Assure ICE')
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            time.sleep(5)
            print('=>Closing Avo Assure ICE with PID :' + str(PID))
            log.info('Closing Avo Assure ICE with PID :' + str(PID))
            os.system('taskkill /F /PID ' + str(PID))
            #os.system('taskkill /F /FI "WINDOWTITLE eq Avo Assure ICE"')
            print ( '=>closed ICE' )
            log.info( 'ICE was closed' )
        except Exception as e:
            print ( "Error occurred in close_ICE : ", e )
            log.error( "Error occurred in close_ICE : " + str(e) )
            import traceback
            traceback.print_exc()

    def restartICE(self,AVOASSUREICE_LOC):
        """Method to restart ICE"""
        try:
            log.debug( 'Inside restartICE function' )
            #---------------------------------file and folders to delete
            try:
                loc1 = os.path.dirname(AVOASSUREICE_LOC) + os.sep + 'run.bat.lock'
                if os.path.exists(loc1): os.unlink(loc1)
            except Exception as e:
                print ( "=>Error occurred in restartICE unable to delete 'run.bat.lock' ERR_MSG: ", e )
                log.error( "Error occurred in restartICE unable to delete 'run.bat.lock' ERR_MSG: " + str(e) )
            try:
                loc2 = os.path.dirname(AVOASSUREICE_LOC) + os.sep +"releasenotesCore.log"
                if os.path.exists(loc2): os.remove(loc2)
            except Exception as e:
                print ( "=>Error occurred in restartICE unable to delete 'releasenotesCore.log' ERR_MSG: ", e )
                log.error( "Error occurred in restartICE unable to delete 'releasenotesCore.log' ERR_MSG: " + str(e) )
            try:
                loc3 = os.path.dirname(AVOASSUREICE_LOC) + os.sep +"versionnoCore.txt"
                if os.path.exists(loc3): os.remove(loc3)
            except Exception as e:
                print ( "=>Error occurred in restartICE unable to delete 'versionnoCore.txt' ERR_MSG: ", e )
                log.error( "Error occurred in restartICE unable to delete 'versionnoCore.txt' ERR_MSG: " + str(e) )
            #---------------------------------file and folders to delete
            loc = os.path.dirname(AVOASSUREICE_LOC) + os.sep +"run.bat"
            subprocess.Popen(loc,cwd=os.path.dirname(loc), creationflags=subprocess.CREATE_NEW_CONSOLE)
            log.debug( 'Restarted ICE.' )
        except Exception as e:
            print ( "=>Error occurred in restartICE : ", e )
            log.error( "Error occurred in restartICE : " + str(e) )
            import traceback
            traceback.print_exc()

    def percentageIncri(self,msg,taskPercent,update_msg):
        msg.StartThread(msg.updateProgress, taskPercent)
        msg.progIncrement(1, taskPercent,update_msg)

def main():
    app = wx.App()
    """Inputs for Update :
              0.UPDATE
              1.Versions Avaliable<{'Build Number':}>
              2.Client Data
              3.End Point URL
              4.Unpacking Location
              5.7-Zip File location """
    """Inputs for rollback :
              0.ROLLBACK
              1.Unpacking location
              2.7-Zip File location """
    comm_obj = common_functions()
    msg = Message(None)
    if len(sys.argv) >1:
        if (sys.argv[1] == 'UPDATE'):
            print( "=>UPDATE selected" )
            log.debug( "===============================UPDATE selected===============================" )
            print( "=>Retriving arguments : " + str(sys.argv))
            log.debug( "Retriving arguments : " + str(sys.argv) )
            obj = Updater()
            msg.StartThread(msg.showProgress)
            comm_obj.percentageIncri(msg,5,"Updating...")
            comm_obj.percentageIncri(msg,10,"Closing ICE...")
            comm_obj.close_ICE(sys.argv[7])#---------------------------------->1.Close ICE
            comm_obj.percentageIncri(msg,15,"ICE closed.")
            comm_obj.percentageIncri(msg,20,"Updating...")
            obj.assignment(sys.argv[2], json.loads(sys.argv[3].replace("'", '\"')[1:-1]), sys.argv[4], sys.argv[5], sys.argv[6])#---------------------------------->2.Assign Values
            comm_obj.percentageIncri(msg,25,"Updating...")
            comm_obj.percentageIncri(msg,30,"Creating backup.")
            err_msg = obj.create_backup()#---------------------------------->3.Create backup 'AvoAssureICE_backup' into Rollback folder
            dlg_selected = 0
            if( not err_msg ):
                comm_obj.percentageIncri(msg,35,"Backup created.")
                comm_obj.percentageIncri(msg,40,"Updating...")
                comm_obj.percentageIncri(msg,45,"Verifying latest files.")
                new_version_list = obj.get_update_files()#---------------------------------->4.Get latest files to update
                comm_obj.percentageIncri(msg,50,"Latest files verified.")
                comm_obj.percentageIncri(msg,55,"Updating...")
                comm_obj.percentageIncri(msg,60,"Retrieving the latest files.")
                end_point_list = obj.end_point_builder(new_version_list)#---------------------------------->5.Create endpoint url list for the files to download
                comm_obj.percentageIncri(msg,70,"Latest files retrieved.")
                comm_obj.percentageIncri(msg,75,"Updating...")
                comm_obj.percentageIncri(msg,80,"Downloading and extracting files")
                warning_msg = obj.download_files(end_point_list)#---------------------------------->6.From the endpoint url list a.download the file, b.extract file into Avo Assure ICE and c.delete the downloaded  7z file
                if ( warning_msg ):
                    comm_obj.percentageIncri(msg,85,warning_msg)
                    time.sleep(2)
                    comm_obj.percentageIncri(msg,87,"Error occurred while updating to latest patch")
                    comm_obj.percentageIncri(msg,90,"Updating...")
                    comm_obj.percentageIncri(msg,95,"Updated to latest available patch.")
                    comm_obj.percentageIncri(msg,100,"Updated...")
                    msg.destoryProgress()
                    dlg_selected = msg.ShowMessage(warning_msg)
                else:
                    comm_obj.percentageIncri(msg,85,"Files downloaded and extracted")
                    comm_obj.percentageIncri(msg,90,"Updating...")
                    comm_obj.percentageIncri(msg,95,"Successfully Updated!")
                    comm_obj.percentageIncri(msg,100,"Updated...")
                    msg.destoryProgress()
                    dlg_selected = msg.ShowMessage()
            else:
                comm_obj.percentageIncri(msg,50,err_msg)
                time.sleep(2)
                comm_obj.percentageIncri(msg,60,"Error occurred while creating backup")
                comm_obj.percentageIncri(msg,70,"Unable to update to latest available patch.")
                comm_obj.percentageIncri(msg,85,"Please ensure that files in Avo Assure are not being used by another process.")
                comm_obj.percentageIncri(msg,100,"Updated Failed!")
                msg.destoryProgress()
                dlg_selected = msg.ShowMessage(err_msg)

            if dlg_selected == 4:
                comm_obj.restartICE(sys.argv[5])#---------------------------------->7.Restart ICE

        elif ( sys.argv[1] == 'ROLLBACK' ):
            print( "=>ROLLBACK selected" )
            log.debug( "===============================ROLLBACK selected===============================" )
            print( "=>Retriving arguments : " + str(sys.argv) )
            log.debug( "Retriving arguments : " + str(sys.argv) )
            obj = Rollback()
            msg.StartThread(msg.showProgress)
            comm_obj.percentageIncri(msg,5,"Rolling back changes...")
            comm_obj.percentageIncri(msg,10,"Assigning values...")
            obj.assignment(sys.argv[2], sys.argv[3])#---------------------------------->Assignment of values
            comm_obj.percentageIncri(msg,15,"Values assigned.")
            comm_obj.percentageIncri(msg,20,"Rolling back changes...")
            res = obj.backup_check()#---------------------------------> Check if backup has been created
            comm_obj.percentageIncri(msg,25,"Closing ICE...")
            comm_obj.close_ICE(sys.argv[4])#---------------------------------->1.Close ICE
            comm_obj.percentageIncri(msg,30,"ICE Closed.")
            comm_obj.percentageIncri(msg,35,"Rolling back changes...")
            dlg_selected = 0
            if ( res == True ):
                comm_obj.percentageIncri(msg,40,"Deleting old instance...")
                obj.delete_old_instance()#---------------------------------->2.Delete old instance of Avo Assure ICE and about_manifest.json
                comm_obj.percentageIncri(msg,45,"Old instance deleted.")
                comm_obj.percentageIncri(msg,50,"Rolling back changes...")
                comm_obj.percentageIncri(msg,55,"Extracting files...")
                obj.rollback_changes()#---------------------------------->3.Rollback contents of AvoAssureICE_backup.7z
                comm_obj.percentageIncri(msg,60,"Files extracted.")
                comm_obj.percentageIncri(msg,65,"Rolling back changes...")
                comm_obj.percentageIncri(msg,70,"Deleting rollback instance...")
                obj.delete_rollback()#---------------------------------->4.Delete AvoAssureICE_backup.7z
                comm_obj.percentageIncri(msg,75,"Rollback instance deleted.")
                comm_obj.percentageIncri(msg,80,"Rolling back changes...")
                comm_obj.percentageIncri(msg,85,"Modifying client manifest...")
                obj.update_client_manifest()#---------------------------------->5.Update about_manifest.json with
                comm_obj.percentageIncri(msg,90,"Client manifest modified.")
                comm_obj.percentageIncri(msg,95,"Successfully rolled back changes!")
                comm_obj.percentageIncri(msg,100,"Success!")
                msg.destoryProgress()
                dlg_selected = msg.ShowMessage('rollback')
            elif ( res == False ):
                i = 35
                while ( i >= 1 ):
                    comm_obj.percentageIncri(msg,i,"Backup not found...")
                    i = i-5
                msg.destoryProgress()

            if dlg_selected == 4:
                comm_obj.restartICE(sys.argv[2])#---------------------------------->6.Restart ICE
    else:
        log.error( "Wrong values passed" )
    app.MainLoop()

if __name__ == '__main__':
    main()