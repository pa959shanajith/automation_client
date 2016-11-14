
import os
import sys
path= 'D:\Sprint4\Nineteen68\plugins'

for root, dirs, files in os.walk(path):
    for name in files:
        if name.endswith('.py'):
            print 'Filename:',name[0:len(name) - 3] ,'\n'
            sys.path.append(name[0:len(name) - 3])


print sys.