#-------------------------------------------------------------------------------
# Name:        Update_module
# Purpose:     1.Checks if ICE requires an update, and calls required updaters if necessary
#              2.Calls Update.py/Update.exe to rollback changes
#
# Author:      anas.ahmed
#
# Created:     06-02-2019
# Copyright:   (c) anas.ahmed 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import json
import os
import logger
import logging
log = logging.getLogger('update_module.py')

class Update_Rollback:
    def __init__(self):
        """Initializing variables"""
        self.update_flag = False
        self.check_flag = False
        self.data_tags = {}
        self.client_tag = {}
        self.SERVER_LOC = None
        #-----------------------------------------------Required only for Update
        self.Update_loc = None
        self.loc_7z = None
        self.updater_loc = None
        self.option = None
        #----------------------------------Required for both Update and Rollback

    def update(self, data_from_server, path, SERVER_LOC, UNPAC_LOC, LOC_7Z, UPDATER_LOC, OPTION):
        """Assigning values to variables"""
        try:
            self.Update_loc = UNPAC_LOC
            self.loc_7z = LOC_7Z
            self.updater_loc = UPDATER_LOC
            self.option = OPTION
            self.SERVER_LOC = SERVER_LOC
            if ( self.option == 'UPDATE' ):
                client_data = self.get_client_manifest(path)
                self.check(client_data, data_from_server)
        except Exception as e:
            log.error( "Error in update : " + str(e) )
        pass

    def get_client_manifest(self, path):
        data = None
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:
            log.error( "Error in get_client_manifest : " + str(e) )
        return data

    def check(self,client_data,data_from_server):
        """Filters till the point where it find the current ICE version in the server manifest, omits lower versions"""
        """Input 1.Client Manifest Data
                 2.Server Manifest Data"""
        """Output 1.Sets the latest data tags
                  2.Sets the update flag and the check flag"""
        #iceversion check
        data_L = []
        #data_tags={}
        vers = []
        subvers = []
        try:
            vers=list(data_from_server['iceversion'])
            vers.sort(reverse=True)
            #log.debug (vers)
            #cver=list(client_data['version'])
            #csubvers=list(client_data['version'][list(client_data['version'])[0]]['subversion'])
            #cdata=client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'][list(client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'])[0]]['sha256']
            #log.debug (cdata)
            """build arguments for client data"""
            cdata_value = []
            ckey = client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'][list(client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'])[0]]['tag']
            cdata_value.append(client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'][list(client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'])[0]]['p_tag'])
##            cdata_value.append(client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'][list(client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'])[0]]['c_tag'])
            self.client_tag.update( {ckey : cdata_value} )

            cdate=client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'][list(client_data['iceversion'][list(client_data['iceversion'])[0]]['subversion'])[0]]['updated_on']
            #log.debug (cdate)
            for v in vers:
                #subvers=data_from_server['version'][v]['subversion'].keys()
                subvers = list(data_from_server['iceversion'][v]['subversion'])
                subvers.sort(reverse = True)
                #log.debug (subvers)
                for sv in subvers:
                    #log.debug (sv)
                    #log.debug (csubvers)
                    #data=data_from_server['version'][v]['subversion'][sv].keys()  #k
                    #for d in data:
                        #log.debug (d,data_from_server['version'][v]['subversion'][sv][d]) #v
##                    if ( data_from_server['iceversion'][v]['subversion'][sv]['sha256'] != cdata ):
                    data_value=[]
                    data_key = ''
                    data_L.append(data_from_server['iceversion'][v]['subversion'][sv])
                    data_key = data_from_server['iceversion'][v]['subversion'][sv]['tag']
                    data_value.append(data_from_server['iceversion'][v]['subversion'][sv]['p_tag'])
                    data_value.append(data_from_server['iceversion'][v]['subversion'][sv]['baseline'])
                    data_value.append(data_from_server['iceversion'][v]['subversion'][sv]['sha256'])
                    self.data_tags.update( {data_key : data_value} )
                        #data_tags.append(data_from_server['version'][v]['subversion'][sv]['tag'])
##                    elif ( data_from_server['iceversion'][v]['subversion'][sv]['sha256'] == cdata ):
##                        log.debug( 'Found till the original' )
            #log.debug (data_L)
            self.check_flag = True
            if (list(self.client_tag.keys())[0] >= self.fetch_current_value()):self.update_flag = False
            else:self.update_flag = True
        except Exception as e:
            log.error( "Error in update_check : " + str(e),exc_info=True)
        #data_tags.reverse()
        #return data_tags
        #calling the update msg

    def fetch_current_value(self):
        """Returns the latest production version available"""
        keys = list(self.data_tags.keys())
        keys.sort(key=lambda s:list(map(int, s.split('.'))))
        if (len(keys)>0):return keys[-1]
        else: return 'N/A'

    def send_update_message(self):
        """Returns a message """
        update_msg = None
        if ( self.update_flag == True and self.check_flag == True ):
            update_msg = 'Update Available!!! Click on update'
        elif ( self.update_flag == False and self.check_flag == True ):
            update_msg = 'You are running the latest version of Avo Assure ICE'
        elif ( self.check_flag == False ):
            update_msg = 'An Error has occured while checking for new versions of Avo Assure ICE, kindly contact Support Team'
        return update_msg

    def run_updater(self):
        """function to run Updater.py/Updater.exe ' UPDATE ' feature"""
        try:
            update_cmd = str(self.updater_loc) + ' ' + str(self.option) + ' """' + str(self.data_tags) + '""" """' + str(self.client_tag) + '""" ' + str(self.SERVER_LOC) + ' ' + str(self.Update_loc) + ' ' + str(self.loc_7z)
            msg = "Sending the following data to Updater."
            if (self.updater_loc.endswith(".py")):
                update_cmd = 'python ' + update_cmd
                msg += "py"
            else: msg += "exe"
            log.debug(msg + ' : ' + update_cmd)
            os.system(update_cmd)
        except Exception as e:
            log.error( "Error in download_and_run_updater : " + str(e) )

    def run_rollback(self):
        """function to run Updater.py/Updater.exe ' ROLLBACK ' feature"""
        try:
            update_cmd = str(self.updater_loc) + ' ' + str(self.option) + ' ' + str(self.Update_loc) + ' ' + str(self.loc_7z)
            msg = "Sending the following data to Updater."
            if (self.updater_loc.endswith(".py")):
                update_cmd = 'python ' + update_cmd
                msg += "py"
            else: msg += "exe"
            log.debug(msg + ' : ' + update_cmd)
            os.system(update_cmd)
        except Exception as e:
            log.error( "Error in run_rollback : " + str(e) )