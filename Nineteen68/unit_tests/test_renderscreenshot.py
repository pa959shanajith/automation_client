#-------------------------------------------------------------------------------
# Name:        test_renderscreenshot
# Purpose:     Unit Test for on_render_screenshot() in client_window.py
#
# Author:      ranjan.agrawal
#
# Created:     22-09-2017
# Copyright:   (c) ranjan.agrawal 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import base64

def on_render_screenshot(self,*args):
    try:
        filepath = args
        data_URIs=[]
        for path in filepath:
            encoded_string = ''
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            base64_data=encoded_string.encode('UTF-8').strip()
            data_URIs.append(base64_data)
        return 'true'
    except Exception as e:
        print 'Error while fetching screenshot data'
        return 'false'


inputs=[]
with open("test_renderscreenshot_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('$')!=-1):
                path=line[line.find('=')+1:].strip()
            elif(line.find('#')==-1):
                i = line.split(';')
                exptd=i[1][:-1]
                filenames = i[0].split(',')
                for i in range(len(filenames)):
                    if filenames[i]!='':
                        filenames[i]=path+filenames[i]
                #inputs.append((path+line[:eq_index].strip(),path+line[eq_index+1:eq_index1].strip(),line[eq_index1:].strip()))
                inputs.append((filenames,exptd))
    print inputs

# content of test_expectation.py
import pytest
@pytest.mark.parametrize("inp,expected", inputs)
def test_myfunc(inp,expected):
    assert on_render_screenshot(inp) == expected
