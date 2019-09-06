import subprocess, os, sys
from sys import executable as python
from subprocess import PIPE
errorcount = 0

def test_cython(f):
    global errorcount
    try:
        cython_process = subprocess.Popen(python+" -m cython -"+str(sys.version_info.major)+' '+f,stdout=PIPE, stderr=PIPE,shell=True)
        out, err = cython_process.communicate()
        if cython_process.returncode != 0:
            errorcount += 1
            msg = f+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n--------------\n\n"
            print(msg)
            cython_error.write(msg)
    except Exception as e:
        errorcount += 1
        print(e)

print("Cython test initiated....")
cwd = os.getcwd() + os.sep + "Nineteen68" + os.sep
print("\nCurrent working location: "+cwd)
cython_error = open('../cython_error.txt','w+')
for root, dirs, files in os.walk(cwd):
    for f in files:
        if f[-3:] == ".py": test_cython(root + os.sep + f)
cython_error.close()
if errorcount > 0:
    raise RuntimeError("Review Failed: There are "+ str(errorcount) + " errors")
