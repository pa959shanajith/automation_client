#-------------------------------------------------------------------------------
# Name:        utilweb_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_constants
import win32com.client
from constants import *
from sap_scraping import Scrape
import logger
import logging
import sap_highlight
log = logging.getLogger('saputil_operations.py')
class SapUtilKeywords:


    def getSapObject(self):
        self.SapGui = None
        try:
            import pythoncom
            pythoncom.CoInitialize()
            self.SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
        except Exception as e:
            logger.print_on_console( 'Not able to find SAPGUI object' )
            log.error(e)
        return self.SapGui

    def getSapElement(self,sap_id,*args):
        id = None
        ses = None
        try:
            SapGui = self.getSapObject()
            scrapingObj = Scrape()                                   #calling scrape class
            wnd = scrapingObj.getWindow(SapGui)                      #calling window method
            wndId =  wnd.__getattr__('id')                         # windowid from name
            j = wndId.index('ses')
            sesId = wndId[0:j+6]
            ses = SapGui.FindByid(str(sesId))
            #-----------------------------------------------------Checking if there is a "/" in the sap_id, if exists take the index(i) after the "/"'s in title to append to id
            title = ses.ActiveWindow.Text
            if("/" in title):
                i = sap_id.index("/",len(title))
            else:
                i = sap_id.index("/")
                #-----------------------------------------------------
            id = wndId + sap_id[i:]
        except Exception as e:
            logger.print_on_console( 'No instance open error :',e)
        except AttributeError as e1:
            logger.print_on_console( ' Attribute  error :',e1)
        return id,ses


    def verifyEnabled(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg  = None
        value = OUTPUT_CONSTANT
        try:
            id, ses = self.getSapElement(sap_id)
            if ( id and ses ):
                if( ses.FindById(id).type == "GuiLabel" or ses.FindById(id).Changeable == True ):
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is disabled'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Enabled" )
        return status,result,value,err_msg

    def verifyDisabled(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            id, ses = self.getSapElement(sap_id)
            if ( id and ses ):
                if ( ses.FindById(id).Changeable == False and ses.FindById(id).type != "GuiLabel" ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is enabled.'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Disabled" )
        return status, result, value, err_msg

    def verifyExists(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            id, ses = self.getSapElement(sap_id)
            if ( id and ses ):
                highligh_obj = sap_highlight.highLight()
                elem = ses.FindById(id)
                if ( elem ):
                    highligh_obj.draw_outline(elem)
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.ELELMENT_NOT_FOUND + ", Unable to highlight"
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Exists" )
        return status, result, value, err_msg

    def verifyHidden(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            id, ses = self.getSapElement(sap_id)
            if ( id and ses ):
                try:
                    ses.FindById(id)
                    err_msg = 'Element is visible'
                except Exception as e:
                    logger.print_on_console( "Element is hidden" )
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Hidden" )
        return status, result, value, err_msg

    def verifyVisible(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            id, ses = self.getSapElement(sap_id)
            if ( id and ses ):
                try:
                    ses.FindById(id)
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    logger.print_on_console( "Element is visible" )
                except Exception as e:
                    err_msg = "Element is hidden"
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Visible" )
        return status, result, value, err_msg

    def getobjectforcustom(self, sap_id, eleType, visible_text, eleIndex):
        data = []
        xpath = None
        err_msg = None
        try:
            id, ses = self.getSapElement(sap_id)
            if ( id and ses ):
                reference_elem = ses.FindById(id)
                wnd_id = id[:26]
                wnd = ses.FindById(wnd_id)
                wnd_title = wnd.__getattr__("Text")
                scrapingObj = Scrape()
                data = scrapingObj.full_scrape(reference_elem, wnd_title)
                elemList = []
                vTextList = []
                for elem in data:
                    if ( elem['tag'].lower() == eleType.strip().lower() ):
                        elemList.append(elem)#make list of elements with same tags
                if( visible_text ):
                    log.info('Identifying element with visible text and index')
                    for elem in elemList:
                        if (elem['text'] == visible_text):
                            vTextList.append(elem)
                    #to get element of  index when visible text is given
                    xpath = vTextList[int(eleIndex)]['xpath']
                else:
                    log.info('Identifying element with only index')
                    #get element with element index
                    xpath = elemList[int(eleIndex)]['xpath']
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console (err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Get Object For Custom" )
        return xpath