#-------------------------------------------------------------------------------
# Name:        Updater Module
# Purpose:     A separate module that runs as an executable, its purpose is to :
#                   1.Create a backup of Nineteen68 (plugins folder) and the about manifest
#                   2.Download files from End Point URL location to temp folder.
#                   3.Unpack the files and replace them in Nineteen68 directory.
#                   4.Once all files have been replaced, delete the file from temp directory.
#                   5.If minor changes then perform steps 1-3(while sequentially calling the zip files)
#                   6.If major changes take the base package of the major version, then perform minor operations.
#                   7.Once all changes are completed stop and close ICE
#                   8.Close Client_updater module
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
#-------------------------------------------logging
import logging
import datetime
date_obj = datetime.datetime.now()
LOG_FILEPATH = str(os.getcwd()) + '\\plugins\\Update\\Logs\\' + 'Updater_Logs_' + str(date_obj.year) + '_' + str(date_obj.month) + '_' + str(date_obj.day) + '_' + str(date_obj.hour) +str(date_obj.minute) + '.log'
logging.basicConfig(filename=LOG_FILEPATH,level=logging.DEBUG)
try:
    log = logging.getLogger("Client_updater.py")
except:
    log = logging.getLogger("Client_updater.exe")
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
        thread = threading.Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def showProgress(self):
        self.progress = wx.ProgressDialog("Progress Window", "Please wait.", maximum=self.maxPercent, parent=self, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)

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

    def ShowMessage(self):
        dlg = wx.MessageBox('Nineteen68 updated successfully. Please start ICE.', 'Info',
            wx.OK | wx.ICON_INFORMATION)
        if (dlg == 4 ):
            self.Close()

class Updater:
    def __init__(self):
        #------------initialization
        """Initializing class variables"""
        log.info( 'Initializing all class variables.' )
        self.vers_aval={} #versions avaliable to the client
        self.ver_client ={} #clinet version
        self.loc_7z=""
        self.extraction_loc=""
        self.SERVER_LOC = None
        self.temp_location = None
        log.info( 'All class variables initialized.' )

    def assignment(self,vers_aval,ver_client,SERVER_LOC,extraction_loc,loc_7z):
        """Assigning value to class variables"""
        #-----------------assignment
        self.vers_aval=vers_aval
        log.info( '=>Versions avaliable : ' + str(self.vers_aval))
        self.ver_client =ver_client
        log.info( '=>Client Version : ' + str(self.ver_client))
        self.loc_7z = loc_7z
        log.info( '=>7z location : ' + str(self.loc_7z))
        self.extraction_loc = extraction_loc
        log.info( '=>Extraction Location : ' + str(self.extraction_loc))
        self.SERVER_LOC = SERVER_LOC
        log.info( '=>Server Path : ' + str(self.SERVER_LOC))

    def close_ICE(self):
        """Killing ICE via window title"""
        try:
            log.debug( 'Inside close_ICE function')
            hwnd = win32gui.FindWindow(None, 'Nineteen68 ICE')
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            os.system('taskkill /F /FI "WINDOWTITLE eq Nineteen68 ICE"')
            print ( '=>closed ICE' )
            log.info( 'ICE was closed' )
        except Exception as e:
            print ( "Error occoured in close_ICE : ", e )
            log.error( "Error occoured in close_ICE : " + str(e) )
            import traceback
            traceback.print_exc()

    def create_backup(self):
        """Purpose: To create a backup of Nineteen68 folder and about_manifest"""
        """Input : 1.7-zip location 2.Nineteen68 folder location and about_manifest.json location 3.Rollbackfile location"""
        """Functionality: 1.Checks is Rollback folder is present in ICE directory, if present checks if Nineteen68_backup.7z is present
                          2.If Nineteen68_backup.7z is present, then delete this instance to create a new once(we do this so as not to keep appending new files to the existing 7zip file)
                          3.If Rollback folder is not present then creates a new folder by the same name in ICE directory
                          4.Adds Nineteen68(plugins) folder to Nineteen68_backup.7z
                          5.Adds about_manifest.json to Nineteen68_backup.7z"""
        flag = False
        try:
            log.debug( 'Inside create_backup function' )
            #--------------------------------------------check if rollback folder exists
            if ( os.path.isdir(self.extraction_loc + "\\assets\\Rollback") and os.path.exists(self.extraction_loc + "\\assets\\Rollback") ):
                log.debug( 'Rollback folder exists' )
                if ( os.path.exists(self.extraction_loc + "\\assets\\Rollback\\Nineteen68_backup.7z") ):
                    log.debug( 'Nineteen68_backup.7z already exists, removing Nineteen68_backup.7z' )
                    os.remove(self.extraction_loc + "\\assets\\Rollback\\Nineteen68_backup.7z")
                    log.debug( 'Nineteen68_backup.7z removed succefully' )
                    time.sleep(1)
                flag = True
            else:
                log.debug( 'Rollback folder does not exist, creating Rollback folder' )
                try:
                    os.mkdir(self.extraction_loc + "\\assets\\Rollback")
                    flag = True
                except OSError:
                    log.error("Creation of the directory " + self.extraction_loc + "\\assets\\Rollback" + " failed.")
                else:
                    log.debug("Successfully created the directory " + self.extraction_loc + "\\assets\\Rollback")
            if ( flag == True ):
                print ( '=>Creating new Nineteen68 backup instance' )
                store_loc = self.extraction_loc+"\\assets\\Rollback\\Nineteen68_backup.7z"
                source_nineteen68 = self.extraction_loc +'\\plugins'
                source_client_manifest = self.extraction_loc +'\\assets\\about_manifest.json'
                log.debug( 'Adding ' + source_nineteen68 + " to archive" )
                archive_command = r'"{}" a "{}" "{}"'.format(self.loc_7z, store_loc, source_nineteen68)
                subprocess.call(archive_command, shell=True)
                log.debug( 'Success : Added ' + source_nineteen68 + " to archive" )
                log.debug( 'Adding '+source_client_manifest+ " to archive" )
                archive_command = r'"{}" a "{}" "{}"'.format(self.loc_7z, store_loc, source_client_manifest)
                subprocess.call(archive_command, shell=True)
                log.debug( 'Success : Added ' + source_client_manifest + " to archive" )
                log.debug( 'Successfully created backup of Nineteen68' )
            else :
                print ( '=>Failed to create Nineteen68 backup' )
                log.error( "Failed to create Nineteen68 backup" )
        except Exception as e:
            print ( "Error occoured in create_backup : ", e )
            log.error( "Error occoured in create_backup : " + str(e) )
            import traceback
            traceback.print_exc()

    def end_point_builder(self,base_folder,new_version_list):
        """Builds the end point url of the file to download"""
        end_points_list = []
        try:
            log.debug( 'Inside end_point_builder function' )
            log.info( "Building the end point URL's" )
            print ( "=>Building the end point URL's" )
            for ver in new_version_list:
                end_points_list.append(str(self.SERVER_LOC) +'/'+ str(base_folder) + '/'+ str(ver) +'.7z')
            print ( "=>End Point URL's are built : ", str(end_points_list) )
            log.info( "End Point URL's are built : " + str(end_points_list) )
        except Exception as e:
            print ( "Error occoured in end_point_builder : ", e )
            log.error( "Error occoured in end_point_builder : " + str(e) )
            import traceback
            traceback.print_exc()
        return end_points_list

    def get_update_files(self):
        """Calculating which directory to update from. Based on that navigates to that particular directory
            Any changes made in versioning need no be implemented here"""
        try:
            log.debug( 'Inside get_update_files function' )
            for k in self.ver_client:
                print(k)
                d = self.ver_client[k][0]
                e = self.ver_client[k][1]
            #find the latest prod version
            new_version_list = []
            temp_variable = None
            number = {}
            for i in self.vers_aval:
                #major/minor version has gone ahead
                if ( float(self.vers_aval[i][0]) > float(d) ):
                    if ( temp_variable == None ):
                        temp_variable = float(self.vers_aval[i][0])
                        number = i
                    else:
                        if ( temp_variable < float(self.vers_aval[i][0]) ):
                            temp_variable = None
                            temp_variable = float(self.vers_aval[i][0])
                            number = i
                else:
                    print ('=>same prod version')
                    pass
            print ( '=>latest production version avaliable : ', temp_variable )
            log.info( 'latest production version avaliable : ' + str(temp_variable)  )
            new_dict={}
            #sorting based on date
            for i in self.vers_aval:
                if ( float(self.vers_aval[i][0]) == temp_variable ):
                    new_dict.update( {str(i) : self.vers_aval[i]} )
                    new_version_list.append(i)

            new_version_list.sort()
            new_dictionary = {}
            new_dictionary = sorted(new_dict.items(), key = lambda x : x[1])
            print ( '=>Number of changes that happened since then ( lastest delta changes ) : ', str(new_version_list)  )
            log.info( 'Number of changes that happened since then ( lastest delta changes ) : ' + str(new_version_list) )
        except Exception as e:
            print ( "Error occoured in get_update_files : ", e )
            log.error( "Error occoured in get_update_files : " + str(e) )
            import traceback
            traceback.print_exc()
        return temp_variable, new_version_list

    def download_files(self,end_point_list):
        """downloads files from the generated endpoints list"""
        try:
            log.debug( 'Inside download_files function' )
            self.temp_location = tempfile.gettempdir()
            for url in end_point_list:
                filename = url[url.rindex('/')+1:]
                temp_file_path = os.path.join(self.temp_location, filename)
                fileObj = requests.get(str(url),verify=False)
                open(temp_file_path, 'wb').write(fileObj.content)
                print ('=>navigating to extract_files')
                #self.extract_files(temp_file_path)
                print ('=>deleting the extracted file')
                #self.delete_temp_file(temp_file_path)
                print (str(filename), ' was extracted and deleted')
            pass
        except Exception as e:
            print ( "Error occoured in download_files : ", e )
            log.error( "Error occoured in download_files : " + str(e) )
            import traceback
            traceback.print_exc()

    def extract_files(self, temp_file_path):
        """get to portable 7z and open the cmd #2.EXTRACT TO DESTINATION"""
        try:
            log.debug( 'Inside extract_files function' )
            extract_command = r'"{}" x "{}" -o"{}" -y'.format( self.loc_7z, temp_file_path, self.extraction_loc )
            subprocess.call(extract_command, shell = True )
            print( '=>Completed extraction of package at :', self.temp_location )
            log.info( 'Completed extraction of package at : ' + str(self.temp_location) )
        except Exception as e:
            print( '=>Extraction could not complete \n' )
            print ( "Error occoured in extract_files : ", e )
            log.error( "Error occoured in extract_files : " + str(e) )
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
            print ( "Error occoured in delete_temp_file : ", e )
            log.error( "Error occoured in delete_temp_file : " + str(e) )
            import traceback
            traceback.print_exc()

    def percentageIncri(self,msg,taskPercent,update_msg):
        msg.StartThread(msg.updateProgress, taskPercent)
        msg.progIncrement(1, taskPercent,update_msg)

    def restartICE(self):
        """Method to restart ICE"""
        try:
            log.debug( 'Inside restartICE function' )
            loc = self.extraction_loc[:self.extraction_loc.rindex('\\')] +"\\run.bat"
            subprocess.Popen(loc,cwd=os.path.dirname(loc), creationflags=subprocess.CREATE_NEW_CONSOLE)
            log.debug( 'Restarted ICE.' )
        except Exception as e:
            print ( "Error occoured in restartICE : ", e )
            log.error( "Error occoured in restartICE : " + str(e) )
            import traceback
            traceback.print_exc()

def main():
    app = wx.App()

    """Inputs 1.Versions Avaliable<{'Build Number':}>  2.Client Data 3.End Point URL 4.Unpacking Location 5.7-Zip File location"""
    if len(sys.argv) >1:
        print( "=>Retriving arguments :" + str(sys.argv))
        log.debug( "Retriving arguments : " + str(sys.argv) )
        msg = Message(None)
        obj = Updater()
        msg.StartThread(msg.showProgress)
        obj.percentageIncri(msg,5,"Updating...")
        obj.percentageIncri(msg,10,"Update : Closing ICE...")
        obj.close_ICE()#---------------------------------->1.Close ICE
        obj.percentageIncri(msg,15,"Update : ICE closed.")
        obj.percentageIncri(msg,20,"Updating...")
        obj.assignment(json.loads(sys.argv[1].replace("'",'\"')[1:-1]), json.loads(sys.argv[2].replace("'", '\"')[1:-1]), sys.argv[3], sys.argv[4], sys.argv[5])#---------------------------------->2.Assign Values
        obj.percentageIncri(msg,25,"Updating...")
        obj.percentageIncri(msg,30,"Update : Creating backup.")
        obj.create_backup()#---------------------------------->3.Create backup 'Nineteen68_backup' into Rollback folder
        obj.percentageIncri(msg,35,"Update : Backup created.")
        obj.percentageIncri(msg,40,"Updating...")
        obj.percentageIncri(msg,45,"Update : Verifying latest files.")
        temp_variable,new_version_list = obj.get_update_files()#---------------------------------->4.Get latest files to update
        obj.percentageIncri(msg,50,"Update : Latest files verified.")
        obj.percentageIncri(msg,55,"Updating...")
        obj.percentageIncri(msg,60,"Update : Retrieving the latest files.")
        end_point_list = obj.end_point_builder(temp_variable, new_version_list)#---------------------------------->5.Create endpoint url list for the files to download
        obj.percentageIncri(msg,70,"Update : Latest files retrieved.")
        obj.percentageIncri(msg,75,"Updating...")
        obj.percentageIncri(msg,80,"Update : Downloading and extracting files")
        obj.download_files(end_point_list)#---------------------------------->6.From the endpoint url list a.download the file, b.extract file into Nineteen68 and c.delete the downloaded  7z file
        obj.percentageIncri(msg,85,"Update : Files Downloaded and extracted")
        obj.percentageIncri(msg,90,"Updating...")
        obj.percentageIncri(msg,95,"Successfully Updated!")
        obj.percentageIncri(msg,100,"Updated...")
        msg.destoryProgress()
        msg.ShowMessage()
        obj.restartICE()
    app.MainLoop()

if __name__ == '__main__':
    main()