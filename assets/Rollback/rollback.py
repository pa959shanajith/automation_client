#-------------------------------------------------------------------------------
# Name:        Rollback.py
# Purpose:     Does the following functions
#               1. Close ICE
#               2. Delete Nineteen68 Folder and client manifest
#               3. Unpack Nineteen68_backup.7z in ICE directory
#               4. Delete the rollback
#               5. Update in client manifest
#               6. Restart ICE
#
# Author:      anas.ahmed
#
# Created:     28-08-2019
# Copyright:   (c) anas.ahmed 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import shutil
import tempfile
import subprocess
import sys
import json
import win32gui
import win32con
import wx
import threading
import time
#-------------------------------------------logging
import logging
import datetime
date_obj = datetime.datetime.now()
LOG_FILEPATH = str(os.getcwd()) + '\\assets\\RollBack\\logs\\' + 'Rollback_Logs_' + str(date_obj.year) + '_' + str(date_obj.month) + '_' + str(date_obj.day) + '_' + str(date_obj.hour) +str(date_obj.minute) + '.log'
logging.basicConfig(filename=LOG_FILEPATH,level=logging.DEBUG)
try:
    log = logging.getLogger("rollback.py")
except:
    log = logging.getLogger("rollback.exe")
#-------------------------------------------logging

class Message(wx.Frame):
    """Class to create a progress bar and nothing else!"""
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

class Rollback():
    """Code modifications done here"""

    def __init__(self):
        """Initializing class variables"""
        self.ROLLBACK_LOC = None
        self.NINETEEN68_LOC = None
        self.loc_7z = None
        pass

    def backup_check(self):
        res = False
        try:
            res = os.path.exists(self.ROLLBACK_LOC)
            if ( res == True ):
                print( '=>Nineteen68_backup.7z exists, in location : ' + str(self.ROLLBACK_LOC) )
                log.info( "Nineteen68_backup.7z exists, in location : " + str(self.ROLLBACK_LOC) )
            elif ( res == False ):
                print( '=>Nineteen68_backup.7z does not exist, in location : ' + str(self.ROLLBACK_LOC) )
                log.info( "Nineteen68_backup.7z does not exist, in location : " + str(self.ROLLBACK_LOC) )
        except Exception as e:
            print ( "=>Error occoured in backup_check : ", e )
            log.error( "Error occoured in backup_check : " + str(e) )
            import traceback
            traceback.print_exc()
        return res

    def assignment(self,NINETEEN68_LOC,loc_7z):
        """Assigning value to class variables"""
        self.ROLLBACK_LOC = NINETEEN68_LOC+"\\assets\\Rollback\\Nineteen68_backup.7z"
        log.info( '=>Rollback location : ' + str(self.ROLLBACK_LOC))
        self.NINETEEN68_LOC = NINETEEN68_LOC
        log.info( '=>Nineteen68 location : ' + str(self.NINETEEN68_LOC))
        self.loc_7z = loc_7z
        log.info( '=>7z location : ' + str(self.loc_7z))

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
            print ( "=>Error occoured in close_ICE : ", e )
            log.error( "Error occoured in close_ICE : " + str(e) )
            import traceback
            traceback.print_exc()

    def delete_old_instance(self):
        """Removing old Nineteen68 and client manifest"""
        try:
            log.debug( 'Inside delete_old_instance function' )
            #-----------------------------------------deleting Nineteen68 folder and its contents
            print( '=>Deleting : ',self.NINETEEN68_LOC+"\\plugins" )
            log.info( 'Deleting : ' + str(self.NINETEEN68_LOC+"\\plugins") )
            shutil.rmtree(self.NINETEEN68_LOC+"\\plugins", ignore_errors=False, onerror=None)
            print( '=>Deleted : ',self.NINETEEN68_LOC+"\\plugins" )
            log.info( 'Deleted : ' + str(self.NINETEEN68_LOC+"\\plugins") )
            #-------------------------------------------deleting client manifest
            print( '=>Deleting : ',self.NINETEEN68_LOC+"\\assets\\about_manifest.json" )
            log.info( 'Deleting : ' + str(self.NINETEEN68_LOC+"\\assets\\about_manifest.json") )
            os.remove(self.NINETEEN68_LOC+"\\assets\\about_manifest.json")
            print( '=>Deleted : ',self.NINETEEN68_LOC+"\\assets\\about_manifest.json" )
            log.info( 'Deleted : ' + str(self.NINETEEN68_LOC+"\\assets\\about_manifest.json") )
        except Exception as e:
            print ( "=>Error occoured in delete_old_instance : ", e )
            log.error( "Error occoured in delete_old_instance : " + str(e) )
            import traceback
            traceback.print_exc()

    def rollback_changes(self):
        """get to portable 7z and open the cmd #2.EXTRACT TO DESTINATION"""
        try:
            log.debug( 'Inside rollback_changes function' )
            extract_command = r'"{}" x "{}" -o"{}" -y'.format( self.loc_7z, self.ROLLBACK_LOC, self.NINETEEN68_LOC )
            subprocess.call(extract_command, shell = True )
            print( '=>Completed extraction of package at :', self.NINETEEN68_LOC )
            log.info( 'Completed extraction of package at : ' + str(self.NINETEEN68_LOC) )
        except Exception as e:
            print( '=>Extraction could not complete \n' )
            print ( "=>Error occoured in rollback_changes : ", e )
            log.error( "Error occoured in rollback_changes : " + str(e) )
            import traceback
            traceback.print_exc()

    def delete_rollback(self):
        """Removing old Nineteen68 and client manifest"""
        try:
            log.debug( 'Inside delete_rollback function' )
            #--------------------------------------deleting Nineteen68_backup.7z
            print( '=>Deleting : ',self.ROLLBACK_LOC )
            log.info( 'Deleting : ' + str(self.ROLLBACK_LOC) )
            os.remove(self.ROLLBACK_LOC)
            print( '=>Deleted : ',self.ROLLBACK_LOC )
            log.info( 'Deleted : ' + str(self.ROLLBACK_LOC) )
        except Exception as e:
            print ( "=>Error occoured in delete_rollback : ", e )
            log.error( "Error occoured in delete_rollback : " + str(e) )
            import traceback
            traceback.print_exc()

    def update_client_manifest(self):
        """Modify the client manifest"""
        try:
            log.debug( 'Inside modify_client_manifest function' )
            path= str(self.NINETEEN68_LOC + "/about_manifest.json")
            with open(path) as json_file:
                json_decoded = json.load(json_file)
            json_decoded['rollback'] = 'True'
            json_decoded['rollback_on'] =str(date_obj.day)+'/'+str(date_obj.month)+'/'+str(date_obj.year)+', '+str(date_obj.hour)+':'+str(date_obj.minute)+':'+str(date_obj.second)
            with open(path, 'w') as json_file:
                json.dump(json_decoded, json_file)
        except Exception as e:
            print ( "=>Error occoured in modify_client_manifest : ", e )
            log.error( "Error occoured in modify_client_manifest : " + str(e) )
            import traceback
            traceback.print_exc()

    def restartICE(self):
        """Method to restart ICE"""
        try:
            log.debug( 'Inside restartICE function' )
            loc = self.NINETEEN68_LOC[:self.NINETEEN68_LOC.rindex('\\')] +"\\run.bat"
            subprocess.Popen(loc,cwd=os.path.dirname(loc), creationflags=subprocess.CREATE_NEW_CONSOLE)
            log.debug( 'Restarted ICE.' )
        except Exception as e:
            print ( "=>Error occoured in restartICE : ", e )
            log.error( "Error occoured in restartICE : " + str(e) )
            import traceback
            traceback.print_exc()

    def percentageIncri(self,msg,taskPercent,update_msg):
        msg.StartThread(msg.updateProgress, taskPercent)
        msg.progIncrement(1, taskPercent,update_msg)

def main():
    """Inputs 1.Nineteen68 location  2.7zip location """
    app = wx.App()
    if len(sys.argv) >1:
        print( "=>Retriving arguments :" + str(sys.argv) )
        log.debug( "Retriving arguments : " + str(sys.argv) )
        obj = Rollback()
        msg = Message(None)
        msg.StartThread(msg.showProgress)
        obj.percentageIncri(msg,5,"Rolling back changes...")
        obj.percentageIncri(msg,10,"Assigning values...")
        obj.assignment(sys.argv[1], sys.argv[2])#---------------------------------->Assignment of values
        obj.percentageIncri(msg,15,"Values assigned.")
        obj.percentageIncri(msg,20,"Rolling back changes...")
        res = obj.backup_check()#---------------------------------> Check if backup has been created
        obj.percentageIncri(msg,25,"Closing ICE...")
        obj.close_ICE()#---------------------------------->1.Close ICE
        obj.percentageIncri(msg,30,"ICE Closed.")
        obj.percentageIncri(msg,35,"Rolling back changes...")
        if ( res == True ):
            obj.percentageIncri(msg,40,"Deleting old instance...")
            obj.delete_old_instance()#---------------------------------->2.Delete old instance of Nineteen68 and about_manifest.json
            obj.percentageIncri(msg,45,"Old instance deleted.")
            obj.percentageIncri(msg,50,"Rolling back changes...")
            obj.percentageIncri(msg,55,"Extracting files...")
            obj.rollback_changes()#---------------------------------->3.Rollback contents of Nineteen68_backup.7z
            obj.percentageIncri(msg,60,"Files extracted.")
            obj.percentageIncri(msg,65,"Rolling back changes...")
            obj.percentageIncri(msg,70,"Deleting rollback instance...")
            obj.delete_rollback()#---------------------------------->4.Delete Nineteen68_backup.7z
            obj.percentageIncri(msg,75,"Rollback instance deleted.")
            obj.percentageIncri(msg,80,"Rolling back changes...")
            obj.percentageIncri(msg,85,"Modifying client manifest...")
            obj.update_client_manifest()#---------------------------------->5.Update about_manifest.json with
            obj.percentageIncri(msg,90,"Client manifest modified.")
            obj.percentageIncri(msg,95,"Successfully rolled back changes!")
            obj.percentageIncri(msg,100,"Success!")
            msg.destoryProgress()
            msg.ShowMessage()
        elif ( res == False ):
            i = 35
            while ( i >= 1 ):
                obj.percentageIncri(msg,i,"Backup not found...")
                i = i-5
            msg.destoryProgress()
        obj.restartICE()#---------------------------------->6.Restart ICE
    else:
        log.error( "Wrong values passed" )
    app.MainLoop()

if __name__ == '__main__':
    main()