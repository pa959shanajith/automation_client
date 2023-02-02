#-------------------------------------------------------------------------------
# Name:        Update_module
# Purpose:     1.Checks if Avo Assure Client requires an update, and calls required updaters if necessary
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
import subprocess
from distutils.version import LooseVersion, StrictVersion
log = logging.getLogger('update_module.py')

class Update_Rollback:
    def __init__(self):
        """Initializing variables"""
        self.update_flag = False
        self.check_flag = False
        self.MAX_FLAG = False
        self.MIN_FLAG = False
        self.server_version =None
        self.data_tags = {}
        self.client_tag = {}
        self.SERVER_LOC = None
        #-----------------------------------------------Required only for Update
        self.Update_loc = None
        self.loc_7z = None
        self.updater_loc = None
        self.option = None
        self.datatags_file_loc = None
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
        """Filters till the point where it find the current Avo Assure Client version in the server manifest, omits lower versions"""
        """Input 1.Client Manifest Data
                 2.Server Manifest Data"""
        """Output 1.Sets the latest data tags
                  2.Sets the update flag and the check flag"""
        #iceversion check
        data_L = []
        vers = []
        subvers = []
        try:
            vers=list(data_from_server['iceversion'])
            vers.sort(reverse=True)
            self.server_version = data_from_server['version']
            """build arguments for client data"""
            cdata_value = []
            ckey = client_data['version']
            cdata_value.append(client_data['p_tag'])
            #------------Server-Client min/max check
            cmin_svr_val = client_data['min-compatibility']
            cmax_svr_val = client_data['max-compatibility']
            self.MIN_FLAG = LooseVersion(str(cmin_svr_val)) <= LooseVersion(str(self.server_version))# min server version has to be lesser than or equal to the Current Sever Version
            self.MAX_FLAG = LooseVersion(str(cmax_svr_val)) == LooseVersion(str(self.server_version))# max server version has to be equal to the Current Server Version
            self.client_tag.update( {ckey : cdata_value} )
            cdate = client_data['updated_on']

            for v in vers:
                subvers = list(data_from_server['iceversion'][v])
                subvers.sort(reverse = True)
                for sv in subvers:
                    data_value=[]
                    data_key = ''
                    data_L.append(data_from_server['iceversion'][v][sv])
                    data_key = data_from_server['iceversion'][v][sv]['tag']
                    data_value.append(data_from_server['iceversion'][v][sv]['p_tag'])
                    data_value.append(str(data_from_server['iceversion'][v][sv]['baseline']))
                    data_value.append(data_from_server['iceversion'][v][sv]['sha256'])
                    self.data_tags.update( {data_key : data_value} )
            self.check_flag = True

            #client version from clinet manifest
            client_version = list(self.client_tag.keys())[0]
            if 'rc' in str(client_version):
                client_version = client_version.replace("-rc.",".") # converting '-rc.' ->'.' for easier comparison

            #latest client version from server manifest
            server_version = self.fetch_current_value()
            if 'rc' in str(server_version):
                server_version = server_version.replace("-rc.",".") # converting '-rc.' ->'.' for easier comparison

            def compare(v1,v2):
                v1 = [int(v) for v in v1.split(".")]
                v2 = [int(v) for v in v2.split(".")]
                for i in range(max(len(v1),len(v2))):
                    vs1 = v1[i] if i< len(v1) else 0
                    vs2 = v2[i] if i< len(v2) else 0
                    if vs1 > vs2:
                        return 1
                    elif vs1 < vs2:
                        return -1
                return 0
            #compare the current client version with the version avaliable in server
            compare_res = compare(client_version,server_version)
            if ( compare_res == 1 or compare_res == 0 ):self.update_flag = False
            else:self.update_flag = True
        except Exception as e:
            log.error( "Error in update_check : " + str(e),exc_info=True)

    def fetch_current_value(self):
        """Returns the latest production version available"""
        flg = False
        keys = list(self.data_tags.keys())
        #check if any of the keys has rc in the value
        for k in keys:
            if 'rc' in k :
                flg = True
                break
        if (flg):
            """For Release Candidate(rc) package expression, Eg : 3.3.0-rc.1[first integer - major version, second integer - minor version, third integer - delta package, fourth part - release candidate number]"""
            newkeys = []
            for i in keys:
                newkeys.append(i.replace("-rc.","."))
            keys = newkeys

            keys.sort(key=lambda s:list(map(int, s.split('.'))))

            newkeys = []
            for i in keys:
                c = i.count('.')
                if c == 3:
                    newkeys.append(i[0:i.rindex('.')]+'-rc.'+i[i.rindex('.')+1:])
                else:
                    newkeys.append(i)
            keys = newkeys
            del newkeys
        else:
            """For regular package expression, Eg : 3.3.0[first integer - major version, second integer - minor version, third integer - delta package]"""
            keys.sort(key=lambda s:list(map(int, s.split('.'))))
        if (len(keys)>0):return keys[-1]
        else: return 'N/A'

    def send_update_message(self):
        """Returns a message """
        update_msg = None
        if ( self.update_flag == True and self.check_flag == True ):
            update_msg = 'Update Available!!! Click on update'
        elif ( self.update_flag == False and self.check_flag == True ):
            update_msg = 'You are running the latest version of Avo Assure Client'
        elif ( self.check_flag == False ):
            update_msg = 'An Error has occured while checking for new versions of Avo Assure Client, kindly contact Support Team'
        return update_msg

    def server_check_message(self):
        """Returns a message if there in incompatibility between Avo Assure Client and Server"""
        update_msg = None
        if ( self.MIN_FLAG and self.MAX_FLAG ):
                log.info( "SERVER_COMPATIBILITY_CHECK: PASS; Avo Assure Client is compatible with current server version : " + str(self.server_version) + "." )
                self.server_check_flag = True
        elif( self.server_version is None ):
            log.info( 'SERVER_COMPATIBILITY_CHECK: FAIL; Unable to get severversion' )
            self.server_check_flag = False
        else:
            log.info( 'SERVER_COMPATIBILITY_CHECK: FAIL; Avo Assure Client is incompatible with current server version : ' + str(self.server_version) + '. Please update to the latest Avo Assure Client' )
            update_msg = 'Warning!: Avo Assure Client is incompatible with current server version : ' + str(self.server_version) + '; Please update to the latest Avo Assure Client'
            self.server_check_flag = False
        return update_msg

    def run_updater(self,l_ver):
        """Function to run Updater.py/Updater.exe ' UPDATE ' feature"""
        try:
            #write datatags to datatags_file
            self.datatags_file_loc = str(self.Update_loc)+"\\datatags_file.txt"
            f = open(self.datatags_file_loc, "w")
            f.write(str(self.data_tags))
            f.close()
            #Command to send to the updater file
            update_cmd = str(self.updater_loc) + ' ' + str(self.option) + ' ' + str(self.datatags_file_loc) + ' """' + str(self.client_tag) + '""" ' + str(self.SERVER_LOC) + ' ' + str(self.Update_loc) + ' ' + str(self.loc_7z) + ' ' + str(os.getpid()) + ' '+str(l_ver)
            msg = "Sending the following data to Updater."
            if (self.updater_loc.endswith(".py")):
                update_cmd = 'python ' + update_cmd
                msg += "py"
            else: msg += "exe"
            log.debug(msg + ' : ' + update_cmd)
            #os.system(update_cmd)
            subprocess.run(update_cmd, shell = True)
        except Exception as e:
            log.error( "Error in run_updater : " + str(e) )

    def run_rollback(self):
        """Function to run Updater.py/Updater.exe ' ROLLBACK ' feature"""
        try:
            update_cmd = str(self.updater_loc) + ' ' + str(self.option) + ' ' + str(self.Update_loc) + ' ' + str(self.loc_7z) + ' ' + str(os.getpid())
            msg = "Sending the following data to Updater."
            if (self.updater_loc.endswith(".py")):
                update_cmd = 'python ' + update_cmd
                msg += "py"
            else: msg += "exe"
            log.debug(msg + ' : ' + update_cmd)
            #os.system(update_cmd)
            subprocess.run(update_cmd, shell = True)
        except Exception as e:
            log.error( "Error in run_rollback : " + str(e) )