import subprocess, os, platform, sys
import shutil
from sys import executable as python
from subprocess import PIPE
from os.path import splitext,join,normpath,isfile,dirname,isdir,basename
py_info = sys.version_info
pythondir = dirname(python) + os.sep
DEVNULL = open(os.devnull, 'w')
errorcount = 0
ext_o_c_py = [".o",".py",".c"]


def del_ignore_folder_list(path="./folderignore.txt"):
    fobj = open(path)
    items = fobj.read().split('\n')
    fobj.close()
    folds = []
    fils = []
    system = platform.system()
    plat_act = False
    for i in items:
        i = i.strip()
        if i == '' or i[0] == '#': continue
        if i[0] == '>':
            plat_act = True if (i[1:].lower() == system.lower()) else False
        if plat_act:
            del_path = normpath(plugins_path+'/'+i[1:])
            try:
                if i[0] == ':':
                    shutil.rmtree(del_path)
                    folds.append(del_path)
                elif i[0] == '?':
                    os.remove(del_path)
                    fils.append(del_path)
            except:
                pass
    return folds, fils

def get_req_plugins_list(path="./pluginrequired.txt"):
    fobj = open(path)
    plugs = fobj.read().split('\n')
    fobj.close()
    fplugs = ["Core", "Generic"]
    for p in plugs:
        p = p.strip()
        if p != '' and p[0] != '#':
            fplugs.append(p)
    return fplugs

def build_pyd(f):
    global errorcount
    try:
        fn = dirname(f)+os.sep+"build_"+basename(f[:-3]) #removing extesnion
        cython_process =subprocess.Popen(python+" -m cython -"+str(py_info.major)+' '+f+" -o "+fn+".c",stdout=PIPE, stderr=PIPE,shell=True)
        out,err = cython_process.communicate()
        if cython_process.returncode != 0:
            errorcount += 1
            msg = f+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n"
            print(msg)
            cython_error.write(msg)
            return

        gcc_process = subprocess.Popen("gcc -c -I"+pythondir+"include -D MS_WIN64 -o "+fn+".o "+fn+".c",stdout=PIPE, stderr=PIPE,shell=True)
        out,err = gcc_process.communicate()
        if gcc_process.returncode != 0:
            errorcount += 1
            print(f+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n")
        gcc_process_pyd = subprocess.Popen("gcc -shared -L"+pythondir+"libs -o "+f[:-3]+".pyd "+fn+".o -lpython"+str(py_info.major)+str(py_info.minor),stdout=PIPE, stderr=PIPE,shell=True)
        out,err = gcc_process_pyd.communicate()
        if gcc_process_pyd.returncode != 0:
            errorcount += 1
            print(f+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n")
        subprocess.call("del /Q /F "+f, stdout=DEVNULL, shell=True)
    except Exception as e:
        errorcount += 1
        print(e)

def build_exe_gcc(f,typ="c"):
    return ""
    global errorcount
    try:
        cython_process = subprocess.Popen(python+" -m cython "+f+" --embed",stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = cython_process.communicate()
        if cython_process.returncode != 0:
            errorcount += 1
            msg = f+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n"
            print(msg)
            cython_error.write(msg)
            return
        f = f[:-3] #removing extesnion

        if typ=="g": typ = "-mwindows"
        else: typ = "-mconsole"
        gcc_process = subprocess.Popen("gcc "+f+".c icon.res -I"+pythondir+"include -D MS_WIN64 -L"+pythondir+"libs -lpython27 "+typ+" -o "+f+".exe",stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell = True)
        out,err = gcc_process.communicate()
        if gcc_process.returncode != 0:
            errorcount += 1
            print(f+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n")
        if os.path.isfile(f+".exe"):
            for ext in ext_o_c_py:
                if os.path.isfile(f + ext):
                    subprocess.check_call("del "+f+ext,shell=True)
    except Exception as e:
        errorcount += 1
        print(e)

def build_exe_pyinstaller(f,typ="c"):
    return ""
    global errorcount
    try:
        if typ=="g": typ = "-mwindows"
        else: typ = "-mconsole"
        gcc_process = subprocess.Popen("gcc "+f+".c icon.res -I"+pythondir+"include -D MS_WIN64 -L"+pythondir+"libs -lpython27 "+typ+" -o "+f+".exe",stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell = True)
        out,err = gcc_process.communicate()
        if gcc_process.returncode != 0:
            errorcount += 1
            print(f+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n")
        f = f.replace("/",os.sep)
        if os.path.isfile(f+".exe"):
            for ext in ext_o_c_py:
                if os.path.isfile(f + ext):
                    subprocess.check_call("del "+f+ext,shell=True)
    except Exception as e:
        errorcount += 1
        print(e)

def build_recursive_dir_tree(path):
    # Removing plugins not needed
    for root, dirs, files in os.walk(path):
        print("\nRemoving unwanted plugins")
        for d in dirs:
            if d not in plugins:
                print(d+" deleted")
                shutil.rmtree(root+os.sep+d)
        break

    for root, dirs, files in os.walk(path):
        print("\nProcessing Directory = "+os.path.basename(root))
        #print("Processing files = "+str(files))
        for f in files:
            full_path = join(root, f)
            if f[-3:] == ".py":
                if f == "__main__.py": build_exe_gcc(full_path, "g")
                else: build_pyd(full_path)
    subprocess.call("del /S /F /Q *.py",stdout=DEVNULL,shell=True)
    subprocess.call("del /S /F /Q build_*",stdout=DEVNULL,shell=True)

print("Building process initiated....")
cwd = os.getcwd()
plugins_path = normpath(cwd + "/Nineteen68/plugins/")
unit_tests_path = normpath(cwd + "/Nineteen68/unit_tests/")
if os.path.isdir(unit_tests_path):
    shutil.rmtree(unit_tests_path)
os.chdir(plugins_path)
print("\nCurrent working location: "+cwd)
plugins = get_req_plugins_list("../../pluginrequired.txt")
print("\nPlugins to build are: " + ", ".join(plugins))
ign_folder, ign_file = del_ignore_folder_list("../../folderignore.txt")
print("\nFolders to remove are: " + ", ".join(ign_folder))
print("\nFiles to remove are: " + ", ".join(ign_file))
cython_error = open('../../cython_error.txt','w+')
build_recursive_dir_tree(plugins_path)
cython_error.close()
if errorcount > 0:
    raise RuntimeError("BUILD FAILED : There are "+ str(errorcount) + " errors")
