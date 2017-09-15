def verifyValuesExists(input):
        visibilityFlag=True
        err_msg=None
        try:
            if input is not None:
                option_len = ['None ','Screen Reader Optimized ','Standard Accessibility ']
                opt_len = len(option_len)
                inp_val_len = len(input)
                temp = []
                flag = True
                for x in range(0,opt_len):
                    internal_val = option_len[x].strip()
                    temp.append(internal_val)
                count = 0
                for y in range(0,inp_val_len):
                    input_temp = input[y].strip()
                    if (input_temp in temp):
                        count+=1
                    else:
                        flag = False
                if(not(flag == False)):
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
    #dropdown
    def test_values(self):
        input = ['Standard Accessibility']
        assert verifyValuesExists(input) == 'true'

    def test_suffix_with_space(self):
        input = ['Standard Accessibility ']
        assert verifyValuesExists(input) == 'true'

    def test_text_cases(self):
        input = ['standard accessibility']
        assert verifyValuesExists(input) == 'false'

    def test_all_values(self):
        input = ['None ','Screen Reader Optimized ','Standard Accessibility ']
        assert verifyValuesExists(input) == 'true'

    def test_null_input_value(self):
        input = ['']
        assert verifyValuesExists(input) == 'false'

    def test_text_doesnt_exist(self):
        input = ['Insert']
        assert verifyValuesExists(input) == 'false'