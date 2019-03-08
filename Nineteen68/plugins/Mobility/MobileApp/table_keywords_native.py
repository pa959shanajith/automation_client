from constants import *
from mobile_app_constants import *
#from appium.webdriver.common.touch_action import TouchAction
#import install_and_launch
import logging
import logger

log = logging.getLogger('table_keywords_native.py')

class Table_Keywords():
    # def __init__(self):
    #     self.status={'radio':'Selected',
    #                 'checkbox':'Checked'}

    def get_row_count(self, element,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')

                        # for set value
                        cells = element.find_elements_by_class_name('XCUIElementTypeCell')
                        count=len(cells)
                        output=count
                        # print count,'from get count'
                        input_count=input_val[0]
                        status = TEST_RESULT_PASS
                        # print element.text
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        # print 'element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg




    def verify_row_count(self, element,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        # for set value
                        cells = element.find_elements_by_class_name('XCUIElementTypeCell')
                        count=len(cells)
                        input_count = input_val[0]
                        # print count,' fgh ',input_count,'dfghj',str(count) == input_count
                        if str(count) == input_count:
                            status = TEST_RESULT_PASS
                            # print element.text
                            methodoutput = TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        # print 'element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def cell_click(self, element,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        # for set value
                        cells = element.find_elements_by_class_name('XCUIElementTypeCell')
                        count=len(cells)
                        input_count = input_val[0]
                        if (int(input_count) > 0 and int(input_count)<=count):
                            # print 'about to click '
                            cells[int(input_count)].click()
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        # print 'element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def get_cell_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if type(webelement) is list:
                   webelement=webelement[0]
            if webelement is not None:
                    if webelement.is_enabled():
                        cells = webelement.find_elements_by_class_name('XCUIElementTypeCell')
                        # for x in input:
                        #     print x,'wsgfddhgdsughj'
                        # print element_path[3]
                        type_raw_input=str(input[1]).lower()
                        if type_raw_input=='text':
                            object_type = 'XCUIElementTypeStaticText'

                        elif type_raw_input=='slider':
                            object_type = 'XCUIElementTypeSlider'

                        elif type_raw_input=='button':
                            object_type = 'XCUIElementTypeButton'

                        elif type_raw_input=='toggle':
                            object_type = 'XCUIElementTypeSwitch'


                        elif type_raw_input=='textbox':
                            object_type = 'XCUIElementTypeTextField'

                        elif type_raw_input=='picker':
                            object_type = 'XCUIElementTypePickerWheel'

                        elif type_raw_input=='searchbar':
                            object_type = 'XCUIElementTypeSearchField'


                        else:
                            object_type=type_raw_input
                        # print object_type
                        row_num=int(input[0])-1
                        type_index=int(input[2])-1
                        # check the inoput is less than cell count
                        count = len(cells)
                        if (row_num >= 0 and row_num < count):
                            child_object=cells[row_num].find_elements_by_class_name(object_type)
                            log.info(len(child_object))
                            # print len(child_object),'len is',type(len(child_object)),'ghjk',type(child_object)
                            if(type_index>=0 and type_index<=len(child_object)):
                                output=child_object[type_index].text
                                log.info(output,' is the output')
                                logger.print_on_console(output)
                                if type_raw_input=='toggle':
                                    if output == 1:
                                        output='On'
                                    else:
                                        output='Off'
                                # print count, 'from get count',output
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                            else:
                                err_msg='please provide valid input in type'
                        else:
                            err_msg='please provide valid input'
                    else:
                        err_msg='ERR_DISABLED_OBJECT'
                    if err_msg is not None:
                        log.info(err_msg)
                        logger.print_on_console(err_msg)

        except Exception as e:
                log.error(e)
                logger.print_on_console(err_msg)
        return status,result,output,err_msg




    def verify_cell_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if type(webelement) is list:
                   webelement=webelement[0]
            if webelement is not None:
                    if webelement.is_enabled():
                        cells = webelement.find_elements_by_class_name('XCUIElementTypeCell')
                        # for x in input:
                        #     # print x,'wsgfddhgdsughj'
                        element_path=str(input[0]).split(';')
                        # for x in  element_path:
                        #     print x,'sdfghjkl'
                        # print input[0]
                        # print input[1]
                        # print input[2]
                        # print element_path[3]
                        type_raw_input=str(input[1]).lower()
                        if type_raw_input=='text':
                            object_type = 'XCUIElementTypeStaticText'

                        elif type_raw_input=='slider':
                            object_type = 'XCUIElementTypeSlider'

                        elif type_raw_input=='button':
                            object_type = 'XCUIElementTypeButton'

                        elif type_raw_input=='toggle':
                            object_type = 'XCUIElementTypeSwitch'


                        elif type_raw_input=='textbox':
                            object_type = 'XCUIElementTypeTextField'

                        elif type_raw_input=='picker':
                            object_type = 'XCUIElementTypePickerWheel'

                        elif type_raw_input=='searchbar':
                            object_type = 'XCUIElementTypeSearchField'

                        else:
                            object_type=type_raw_input
                        # print object_type
                        row_num=int(input[0])-1
                        type_index=int(input[2])-1
                        row_input=str(input[3])
                        # check the inoput is less than cell count
                        count = len(cells)
                        if (row_num >= 0 and row_num < count):
                            child_object=cells[row_num].find_elements_by_class_name(object_type)
                            # print len(child_object),'len is',type(len(child_object)),'ghjk',type(child_object),'fdsghjkc',type_index
                            if(type_index>=0 and type_index<len(child_object)):
                                output_val=child_object[type_index].text
                                # print count, 'from get count',output
                                if type_raw_input=='toggle':
                                    if output_val == 1:
                                        output_val='On'
                                    else:
                                        output_val='Off'
                                if str(output_val) == row_input:
                                    # print 'pass'
                                    status = TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                                else:
                                    print(' fail ')
                            else:
                                print('please provide valid input')
                        else:
                            print('please provide valid input s')
                    else:
                        err_msg='ERR_DISABLED_OBJECT'
        except Exception as e:
                log.error(e)
                logger.print_on_console(err_msg)
        return status, methodoutput, output, err_msg
