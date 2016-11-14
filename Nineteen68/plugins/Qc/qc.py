import win32com
from win32com.client import Dispatch
import logging
import qcconstants
import Exceptions
import logger




t = None

class Qc():
    def qc_login(self,data):
        logger.log('****QC Login begins****')
        status = qcconstants.TEST_RESULT_FAIL
        try:
            #Get the details (comma separated )- QC url, username and password
            logger.log('Getting the details with comma separated')
            details = data.split(qcconstants.COMMA)
            qcServer = details[0]
            qcUser = details[1]
            qcPassword = details[2]
            #When we install qc client - TDApiOle80.TDConnection(this entry ) will be there in regedit
            logger.log('Creating a dispatch of TDApiOle80.TDConnection (regedit entry)')
            t = Dispatch('TDApiOle80.TDConnection')
            logger.log('Initialising the QC Connection')
            t.InitConnectionEx(qcServer)
            #Below piece of code is to login to the qc
            logger.log('Logging into the Quality Center')
            t.Login(qcUser,qcPassword)
            #since above call does not return a value, hence writing mmidiate line to update the status
            #if t.Login(qcUser,qcPassword) line fails then it will directly go to the except clause there updating the status to Fail
            status = qcconstants.TEST_RESULT_PASS
            logger.log('Valid user, Log in Successful')
            logger.log('****Login Successful****\n\n\n')
            if status == qcconstants.TEST_RESULT_PASS:
                #once the login is completed just log out from the qc and change the status tp Pass
                t.Logout
                t.ReleaseConnection
                status == qcconstants.TEST_RESULT_PASS
            else:
                #else change the status as Fail
                status = qcconstants.TEST_RESULT_FAIL
        except Exception as e:
            #Something went wrong
            logger.log('Something went wrong - Connection not established/ Login unsuccessful')
            status = qcconstants.TEST_RESULT_FAIL
            Exceptions.error(e)
        return status

    def update_qc_details(self,data):
        logger.log('****Updating QCDetails****')
        status = qcconstants.TEST_RESULT_FAIL
        try:
            #Get the details (comma separated )- QC url, username and password
            logger.log('Getting the details with comma separated')
            details = data.split(qcconstants.COMMA)
            qcServer = details[0]
            qcUser = details[1]
            qcPassword = details[2]
            qcDomain = details[3]
            qcProject = details[4]
            tsFolder = details[5]
            tsList = details[6]
            testrunname = details[7]
            result =  details[8]
            #When we install qc client - TDApiOle80.TDConnection(this entry ) will be there in regedit
            logger.log('Creating a dispatch of TDApiOle80.TDConnection (regedit entry)')
            t = Dispatch('TDApiOle80.TDConnection')
            logger.log('Initialising the QC Connection')
            t.InitConnectionEx(qcServer)
            #Below piece of code is to login to the qc
            logger.log('Logging into the Quality Center')
            t.Login(qcUser,qcPassword)
            logger.log('Establishing the connection')
            t.Connect(qcDomain,qcProject)
            #Connection Established
            logger.log('Connection Established')
            TSetFact = t.TestSetFactory
            #Getting the test set factory
            logger.log('Getting the test set factory')
            tsTreeMgr = t.testsettreemanager
            tsFolder = tsTreeMgr.NodeByPath(tsFolder)
            tsList = tsFolder.FindTestSets(tsList)
            #Getting the test lists
            logger.log('Getting the test lists')
            theTestSet = tsList.Item(1)
            #Getting the test set
            logger.log('Getting the test set')
            tsFolder = theTestSet.TestSetFolder
            tsTestFactory = theTestSet.tsTestFactory
            tsTestList = tsTestFactory.NewList("")
            for tsTest in tsTestList:
                #Iterate the Test list
                logger.log('Iterate the Test list')
                if tsTest.Name == testrunname:
                    logger.log('Test runname matched')
                    RunFactory = tsTest.RunFactory
                    #RunFactory object created
                    logger.log('RunFactory object created')
                    obj_theRun = RunFactory.AddItem(testrunname)
                    #Updating the details in QC
                    logger.log('Updating the details in QC')
                    obj_theRun.Status = result
                    #Scenario execution status updated
                    logger.log('Scenario execution status updated')
                    obj_theRun.Post()
                    obj_theRun.Refresh()
                    status = qcconstants.TEST_RESULT_PASS
                    #QC Details updated successfully
                    logger.log('QC Details updated successfully')
                    logger.log('****Updated QCDetails****')
                    if status == qcconstants.TEST_RESULT_PASS:
                        t.Logout
                        t.ReleaseConnection
                        status = qcconstants.TEST_RESULT_PASS
                    else:
                        status = qcconstants.TEST_RESULT_FAIL
        except Exceptions as e:
            logger.log('Something went wrong - Connection not established/ Login unsuccessful/Domain/Project/Folder/Testset/Testrun name wrong')
            status = qcconstants.TEST_RESULT_FAIL
            Exceptions.error(e)
        return status





if __name__ == '__main__':
    qcServer = "http://srv03wap121:8080/qcbin"
    qcUser = 'Gowtham'
    qcPassword = 'Gowtham'
    qcDomain = "ENTERPRISE"
    qcProject = "DimensionLab"
    tsFolder = 'Root\User Login'
    tsList = 'Login'
    testrunname = '[1]Mortgage_Calculator'
    result =  'Passed'
    myqc = Qc()
    login = qcServer + ',' + qcUser + ',' + qcPassword
    myqc.qc_login(login)
    data = qcServer + ',' + qcUser + ',' + qcPassword + ',' + qcDomain + ',' + qcProject + ',' + tsFolder + ',' + tsList + ',' + testrunname + ',' + result
    myqc.update_qc_details(data)




