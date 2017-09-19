def func(file1,file2):
    from PIL import Image
    import numpy as np

    img1 = Image.open(file1)
    img2 = Image.open(file2)
    width1, height1 = img1.size
    width2, height2 = img2.size
    size=(min(width1,width2,1024),min(height1,height2,800))
    if not(file1.split('.')[-1]=='jpg'):
        img1 = img1.convert('RGB')
        #print 'converted img 1'
    if not(file2.split('.')[-1]=='jpg'):
        img2 = img2.convert('RGB')
        #print 'converted img 2'
    img1 = img1.resize(size)
    img2 = img2.resize(size)
    imageA = np.asarray(img1)
    imageB = np.asarray(img2)
    err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)

    err /= float(size[0]*size[1]*3*255*255);
    print 'err %: ',err*100,'%'
    if(err<0.0005):  # err<0.05%
        #info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
        #log.info(info_msg)
        #logger.print_on_console(info_msg)
        #methodoutput=TEST_RESULT_TRUE
        #status=TEST_RESULT_PASS
        status='true'
    else:
        status='false'
        #err_msg=ERROR_CODE_DICT['ERR_IMAGE_COMPARE_FAIL']
    return status


var_name=[]
with open("unit_test_Imageverification_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('$')!=-1):
                path=line[line.find('=')+1:].strip()
#               print path
            elif(line.find('#')==-1):
                eq_index = line.find(',')
                eq_index1 = line.find(' ')
                var_name.append((path+line[:eq_index].strip(),path+line[eq_index+1:eq_index1].strip(),line[eq_index1:].strip()))
#               print(var_name)

# content of test_expectation.py
import pytest
@pytest.mark.parametrize("input1,input2,expected", var_name)
def test_myfunc(input1,input2, expected):
    assert func(input1,input2) == expected