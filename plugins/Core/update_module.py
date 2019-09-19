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
        #version check
        data_L = []
        #data_tags={}
        vers = []
        subvers = []
        try:
            vers=list(data_from_server['version'])
            vers.sort(reverse=True)
            #log.debug (vers)
            #cver=list(client_data['version'])
            #csubvers=list(client_data['version'][list(client_data['version'])[0]]['subversion'])
            cdata=client_data['version'][list(client_data['version'])[0]]['subversion'][list(client_data['version'][list(client_data['version'])[0]]['subversion'])[0]]['Checksum']
            #log.debug (cdata)
            """build arguments for client data"""
            cdata_value = []
            ckey = client_data['version'][list(client_data['version'])[0]]['subversion'][list(client_data['version'][list(client_data['version'])[0]]['subversion'])[0]]['tag']
            cdata_value.append(client_data['version'][list(client_data['version'])[0]]['subversion'][list(client_data['version'][list(client_data['version'])[0]]['subversion'])[0]]['p_tag'])
            cdata_value.append(client_data['version'][list(client_data['version'])[0]]['subversion'][list(client_data['version'][list(client_data['version'])[0]]['subversion'])[0]]['c_tag'])
            self.client_tag.update( {ckey : cdata_value} )

            cdate=client_data['version'][list(client_data['version'])[0]]['subversion'][list(client_data['version'][list(client_data['version'])[0]]['subversion'])[0]]['updated_on']
            #log.debug (cdate)
            for v in vers:
                #subvers=data_from_server['version'][v]['subversion'].keys()
                subvers = list(data_from_server['version'][v]['subversion'])
                subvers.sort(reverse = True)
                #log.debug (subvers)
                for sv in subvers:
                    #log.debug (sv)
                    #log.debug (csubvers)
                    #data=data_from_server['version'][v]['subversion'][sv].keys()  #k
                    #for d in data:
                        #log.debug (d,data_from_server['version'][v]['subversion'][sv][d]) #v
                    if ( data_from_server['version'][v]['subversion'][sv]['Checksum'] != cdata ):
                        data_value=[]
                        data_key = ''
                        data_L.append(data_from_server['version'][v]['subversion'][sv])
                        data_key = data_from_server['version'][v]['subversion'][sv]['tag']
                        data_value.append(data_from_server['version'][v]['subversion'][sv]['p_tag'])
                        data_value.append(data_from_server['version'][v]['subversion'][sv]['c_tag'])
                        data_value.append(data_from_server['version'][v]['subversion'][sv]['fixes'])
                        self.data_tags.update( {data_key : data_value} )
                        #data_tags.append(data_from_server['version'][v]['subversion'][sv]['tag'])
                    elif ( data_from_server['version'][v]['subversion'][sv]['Checksum'] == cdata ):
                        log.debug( 'Found till the original' )
            #log.debug (data_L)
            self.check_flag = True
            self.update_flag = True
        except Exception as e:
            log.error( "Error in check : " + str(e) )
        #data_tags.reverse()
        #return data_tags
        #calling the update msg

    def fetch_current_value(self):
        """Returns the latest production version available"""
        keys = None
        keys = list(self.data_tags.keys())
        keys.sort()
        return keys[len(keys)-1]

    def send_update_message(self):
        """Returns a message """
        update_msg = None
        if ( self.update_flag == True and self.check_flag == True ):
            update_msg = 'Update Available!!! Click on update'
        elif ( self.update_flag == False and self.check_flag == True ):
            update_msg = 'You are running the latest version of Nineteen68'
        elif ( self.check_flag == False ):
            update_msg = 'An Error has occoured while checking for new versions of Nineteen68, kindly contact Support Team'
        return update_msg

    def run_updater(self):
        """function to run Updater.py/Updater.exe ' UPDATE ' feature"""
        try:
            log.debug( 'Sending the following data to Updater : ' + 'python ' + str(self.updater_loc) + ' ' + str(self.option) +  ' """' + str(self.data_tags) + '""" """' + str(self.client_tag) + '""" ' + str(self.SERVER_LOC) + ' ' + str(self.Update_loc) + ' ' + str(self.loc_7z) )
            os.system('python ' + str(self.updater_loc) + ' ' + str(self.option) + ' """' + str(self.data_tags) + '""" """' + str(self.client_tag) + '""" ' + str(self.SERVER_LOC) + ' ' + str(self.Update_loc) + ' ' + str(self.loc_7z))
        except Exception as e:
            log.error( "Error in download_and_run_updater : " + str(e) )

    def run_rollback(self):
        """function to run Updater.py/Updater.exe ' ROLLBACK ' feature"""
        try:
            log.debug( 'Sending the following data to Updater : ' + 'python ' + str(self.updater_loc) + ' ' + self.option + ' ' + str(self.Update_loc) + ' ' + str(self.loc_7z))
            os.system('python ' + str(self.updater_loc) + ' ' + str(self.option) + ' '  ' ' + str(self.Update_loc) + ' ' + str(self.loc_7z))
        except Exception as e:
            log.error( "Error in run_rollback : " + str(e) )