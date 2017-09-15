# content of test_class.py
from selenium import webdriver

'''def selectByAbsoluteValue(input):
        visibilityFlag=True
        err_msg=None
        if (input is not None) :
            if len(input)==5:
                dropVal=input[2]
                row_num=int(input[0])-1
                col_num=int(input[1])-1
                inp_val = input[4]
                if dropVal.lower()=='dropdown':
                    visibleFlag=True
                    if visibleFlag==True:
                        iList = ['All','Active','Discontinued','Obsolete']
            elif (len(input) == 1):
                if input[0] != '':
                    inp_val = input[0]
                    if len(inp_val.strip()) != 0:
                        iList = ['All','Active','Discontinued','Obsolete']
            try:
                if inp_val !='':
                    temp=[]
                    for i in range (0,len(iList)):
                        internal_val = iList[i]
                        temp.append(internal_val)
                    if (inp_val in temp):
                        status='true'
                    else:
                        status='false'
                else:
                    status='false'
            except Exception as e:
                err_msg=e
                status='false'
        return status'''

def selectByAbsoluteValue(input):
    visibilityFlag=True
    err_msg=None
    driver = webdriver.Firefox()
    driver.get('https://www.ahridirectory.org/ahridirectory/pages/rfr/defaultSearch.aspx')
    webelement = driver.find_element_by_id('cp1_search1_dl1_modelStatus')
    if webelement is not None:
        if (input is not None) :
            if len(input)==5:
                if webelement.tag_name=='table':
                    dropVal=input[2]
                    row_num=int(input[0])-1
                    col_num=int(input[1])-1
                    inp_val = input[4]
                    try:
                        if dropVal.lower()=='dropdown':
                            driver=browser_Keywords.driver_obj
                            visibleFlag=True
                            if visibleFlag==True:
                                from table_keywords import TableOperationKeywords
                                tableops = TableOperationKeywords()
                                cell=tableops.javascriptExecutor(webelement,row_num,col_num)
                                element_list=cell.find_elements_by_xpath('.//*')
                                if len(list(element_list))>0:
                                    xpath=tableops.getElemntXpath(element_list[0])
                                    cell=browser_Keywords.driver_obj.find_elemenst_by_xpath(xpath)
                                    if(cell!=None):
                                        log.debug('checking for element enabled')
                                        if cell.is_enabled():
                                            if len(inp_val.strip()) != 0:
                                                select = Select(cell)
                                                iList = select.options
                                            else:
                                                status='false'
                                else:
                                    status='false'
                    except Exception as e:
                        err_msg=e
                        status='false'
            elif (len(input) == 1):
                if input[0] != '':
                    try:
                        inp_val = input[0]
                        log.info('Input value obtained')
                        log.info(inp_val)
                        coreutilsobj=core_utils.CoreUtils()
                        inp_val=coreutilsobj.get_UTF_8(inp_val)
                        if len(inp_val.strip()) != 0:
                            select = Select(webelement)
                            iList = select.options
                        else:
                            status='false'
                    except Exception as e:
                        status='false'
                        err_msg=e
                else:
                    status='false'
            else:
                status='false'
            try:
                if inp_val !='':
                    temp=[]
                    for i in range (0,len(iList)):
                        internal_val = iList[i].text
                        temp.append(internal_val)
                    if (inp_val in temp):
                        status='true'
                    else:
                        status='false'
                else:
                    status='false'

            except Exception as e:
                err_msg=e
                status='false'
    return status

class TestClass(object):
    #table with dropdown

    def test_same(self):
        input = ['3', '2', 'dropdown', '1', 'All']
        assert selectByAbsoluteValue(input) == 'true'

    def test_differnt_value_with_space(self):
        input = ['3', '2', 'dropdown', '1', 'All ']
        assert selectByAbsoluteValue(input) == 'false'

    def test_differnt_text_cases(self):
        input = ['3', '2', 'dropdown', '1', 'all ']
        assert selectByAbsoluteValue(input) == 'false'

    def test_handling_null_exception(self):
        input = ['3', '2', 'dropdown', '1', ' ']
        assert selectByAbsoluteValue(input) == 'false'

    def test_check_inputlength(self):
        input = ['3', '2', 'dropdown']
        assert selectByAbsoluteValue(input) == 'false'

    def test_check_input_value(self):
        input = ['3', '2', 'ddown','1','All']
        assert selectByAbsoluteValue(input) == 'false'

    def test_text_doesnt_exist(self):
        input = ['3', '2', 'dropdown', '1', 'Insert']
        assert selectByAbsoluteValue(input) == 'false'
    # dropdown
    def test_values(self):
        input = ['Active']
        assert selectByAbsoluteValue(input) == 'true'

    def test_value_with_space(self):
        input = [' Active ']
        assert selectByAbsoluteValue(input) == 'false'

    def test_text_cases(self):
        input = ['active ']
        assert selectByAbsoluteValue(input) == 'false'

    def test_handling_exception(self):
        input = [' ']
        assert selectByAbsoluteValue(input) == 'false'

    def test_inputlength(self):
        input = ['bc','dropdown']
        assert selectByAbsoluteValue(input) == 'false'

    def test_doesnt_exist(self):
        input = ['Insert']
        assert selectByAbsoluteValue(input) == 'false'










