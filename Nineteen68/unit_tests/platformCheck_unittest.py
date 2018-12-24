#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kavyarathna.s
#
# Created:
# Copyright:   (c) kavyarathna.s
# Licence:     <your licence>
#-------------------------------------------------------------------------------
SYSTEM_OS='windows'
import platform

def platformCheck():
    result='False'
    SYSTEM_OS=platform.system()
    if SYSTEM_OS=='Windows':
        result='True'
    elif SYSTEM_OS=='Darwin':
        result='True'

    return result


var_name=[]
with open("platformCheck_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index1 = line.find('#')
            var_name.append((line[eq_index1+1:].strip()))

import pytest
@pytest.mark.parametrize("expected",var_name)
def test_myfunc(expected):
    assert platformCheck() == expected

