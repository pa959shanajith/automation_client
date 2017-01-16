#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

a=['1','2','3','backspace','5']
a.reverse()
for x in range(0,3):
    a.pop()
    print a
a.reverse()
print 'FINAL',a
