#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     15-09-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import unittest
import Webservices

obj=''

class WStestcase(unittest.TestCase):
    global obj
    obj=Webservices.WSkeywords()

    def test_Webservices(self):
        url='hi'
        header=''
        method=''
        operation=''
        body=''

        self.assertTrue(obj.setEndPointURL(url))



if __name__ == '__main__':
    print 'hi'
    unittest.main()
