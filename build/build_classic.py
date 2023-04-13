import subprocess
import os
import sys
from os import walk
from os.path import splitext, join, dirname, normpath, basename
from sys import executable as python
import py_compile
import shutil
sl = os.sep
pythondir = dirname(sys.executable)+sl #remove python.exe
pymajor = str(sys.version_info.major)
pyminor = str(sys.version_info.minor)
errorcount =0
ext_o_c_py = [".o",".py",".c"]
#cwd = os.getcwd()
f=os.getcwd().split("\\")[-1]
print("hello ")
print(f)
def build_pyd(full_path):
    global errorcount
    try:
        # pending save error and filename to file
        cython_process =subprocess.Popen(python+" -m cython -"+pymajor+' '+full_path,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = cython_process.communicate()
        exitcode = cython_process.returncode
        if not exitcode ==0:
            errorcount = errorcount + 1
            msg = full_path+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n"
            print(msg)
            file_refer.write(msg)
            return
        full_path = full_path[:-3] #removing extesnion
        # file = file[:-3]

        gcc_process = subprocess.Popen("gcc -shared -I"+pythondir+"include -DMS_WIN64 -L"+pythondir+"libs -o "+full_path+".pyd "+full_path+".c -lpython"+pymajor+pyminor,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell = True)
        out,err = gcc_process.communicate()
        exitcode = gcc_process.returncode
        if not exitcode ==0:
            errorcount = errorcount + 1
            msg = full_path+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n"
            print(msg)
        full_path = full_path.replace("/","\\")
        if os.path.isfile(full_path+".pyd"):
            for ext in ext_o_c_py:
                if os.path.isfile(full_path + ext):
                    subprocess.check_call("del "+full_path + ext,shell=True)
    except subprocess.CalledProcessError as e:
        errorcount = errorcount + 1
        print(e)
        return

def build_pyc(full_path):
    global errorcount
    try:
        py_compile.compile(full_path, full_path+'c', doraise=True)
        if os.path.isfile(full_path+'c'):
           subprocess.check_call("del "+full_path, shell = True)
    except py_compile.PyCompileError as e:
        errorcount = errorcount + 1
        msg = full_path+"\nError:"+str(e)+"\n-------\n"
        print(msg)
        file_refer.write(msg)
        return -1

def build_c(full_path, ffile, exe_args=False):
    global errorcount
    try:
        exe_args = " --embed" if exe_args else ''
        cython_process = subprocess.Popen(python+" -m cython -"+pymajor+' -o '+ffile+' '+full_path+exe_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = cython_process.communicate()
        exitcode = cython_process.returncode
        if not exitcode == 0:
            errorcount = errorcount + 1
            msg = full_path+"\nError:"+err.decode('utf-8')+"\nOutput:"+out.decode('utf-8')+"\n-------\n"
            print(msg)
            file_refer.write(msg)
            return -1
        if os.path.isfile(ffile):
           if "__main__" not in full_path:
                subprocess.check_call("del "+full_path, shell = True)
    except subprocess.CalledProcessError as e:
        errorcount = errorcount + 1
        print(e)
        return -1

def build_exe(source, target, gui=False, console=False):
    global errorcount
    try:
        if gui and console:
            raise RuntimeError("BUILD FAILED : gui and console cannot be true both at the same time")
        flags = "-municode"
        if gui: flags += " -mwindows"
        elif console: flags += " -mconsole"
        gcc_process = subprocess.Popen("gcc -I"+pythondir+"include -DMS_WIN64 "+source+" avo_ico.res -o "+target+" "+flags+" -L"+pythondir+"libs -lpython"+pymajor+pyminor, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        out, err = gcc_process.communicate()
        exitcode = gcc_process.returncode
        if not exitcode == 0:
            errorcount = errorcount + 1
            print("Error while generating "+os.path.basename(target)+"\n" + out.decode('utf-8') + '\n' + err.decode('utf-8'))
        if os.path.isfile(target):
           subprocess.check_call("del "+source, shell = True)
    except subprocess.CalledProcessError as e:
        errorcount = errorcount + 1
        print(e)
        return -1

def select_files(root, files, ign, fpyc):
    py_files = []
    print("\n\nDirectory ="+root+"\n")
    for file in files:
        full_path = normpath(join(root, file))
        extsn = splitext(file)[1]
        if extsn==".py":
            if full_path in fpyc:
                py_files.append(full_path)
                build_pyc(full_path)
            elif full_path not in ign:
                py_files.append(full_path)
                build_pyd(full_path)
    return py_files


def build_recursive_dir_tree(path):
    selected_files = []
    ign = "Core/__main__.py"
    # ign = os.getenv("BUILD_IGNORE", [])
    fpyc="AWS/android_operations_keywords.py;AWS/android_spinner_keywords.py;AWS/custom_aws.py;AWS/generic_operations.py;AWS/testmobile_constants.py"
    # fpyc = os.getenv("BUILD_PYC", [])
    if len(ign) > 0:
        b_ign = ign.split(';')
        ign = [normpath(path+line) for line in b_ign]
    if len(fpyc) > 0:
        b_pyc = fpyc.split(';')
        fpyc = [normpath(path+line) for line in b_pyc]
    for root, _, files in walk(path):
        if root not in ign:
            selected_files += select_files(root, files, ign, fpyc)
    return selected_files


def preprocess_deltafiles(path):
    if os.getenv("DELTA_FILES", "").lower() != 'true': return None
    flist = []
    with open('deltafiles.txt') as dfo:
        flist = dfo.read().split('\n')
    folder_to_keep = set([path])
    file_to_keep = []
    prefix = path + sl
    for fi in flist:
        if fi.strip() == '': continue
        if fi.startswith('R'):
            status, _, fpath = fi.split('\t')
            status = status[0]
        else: status, fpath = fi.split('\t')
        if status == 'D': continue
        file_to_keep.append(normpath(prefix+fpath))
        fopath = dirname(fpath)
        while fopath != '':
            folder_to_keep.add(normpath(prefix+fopath))
            fopath = dirname(fopath)
    for d in ['assets', 'plugins']:
        rpath = path+sl+d
        if rpath not in folder_to_keep:
            os.system('rimraf ' + rpath)
            continue
        for root, dirs, files in walk(rpath):
            root = normpath(root)
            # if root not in folder_to_keep:
                # os.system('rimraf ' + root)
            del_list = []
            for di in dirs:
                fpath = root+sl+di
                if fpath not in folder_to_keep:
                    # os.system('rimraf ' + fpath)
                    del_list.append(fpath)
            for fi in files:
                fpath = root+sl+fi
                if fpath not in file_to_keep:
                    # os.system('rimraf ' + fpath)
                    del_list.append(fpath)
            os.system('rimraf ' + ' '.join(del_list))

print("Building process initiated....")
cwd = os.getcwd()
cwd += "" if basename(cwd) == f else (sl + f)
unit_tests_path = cwd + sl + "unit_tests"
if os.path.isdir(unit_tests_path): shutil.rmtree(unit_tests_path)
print(cwd)
try:
    # preprocess_deltafiles(cwd)
    print("here we kept the complete plugins files only")
except Exception as e:
    print("Error occured while processing delta files. Error: ", e)
    raise RuntimeError("BUILD FAILED : There was error during processing delta files")

file_refer = open('../cython_error.txt','a')
try:
    irismt_fileloc = os.path.abspath(cwd + "/assets/IRISMT/IRISMT")
    if os.path.exists(irismt_fileloc+".py"):
        build_c(irismt_fileloc+".py",irismt_fileloc+".c",exe_args=True)
        build_exe(irismt_fileloc+".c",irismt_fileloc+".exe",gui=True)
        if sys.platform == 'win32':
            with open(dirname(irismt_fileloc)+sl+'startIRISMT.bat', 'w') as fo:
                fo.write("@echo off\ncd ../..\nstart assets\IRISMT\IRISMT.exe\nexit")
except Exception as e:
    print("Failed to build IRISMT")
    print("Error: ", e)
try:
    predcmt_fileloc = os.path.abspath(cwd + "/assets/ObjectPredictionMT/ObjectPredictionMT")
    if os.path.exists(predcmt_fileloc+".py"):
        build_c(predcmt_fileloc+".py",predcmt_fileloc+".c",exe_args=True)
        build_exe(predcmt_fileloc+".c",predcmt_fileloc+".exe",gui=True)
        if sys.platform == 'win32':
            with open(dirname(predcmt_fileloc)+sl+'startObjectPredictionMT.bat', 'w') as fo:
                fo.write("@echo off\ncd ../..\nstart assets\ObjectPredictionMT\ObjectPredictionMT.exe\nexit")
except Exception as e:
    print("Failed to build ObjectPredictionMT")
    print("Error: ", e)

try:
    main_fileloc = os.path.abspath(cwd + "/plugins/Core/__main__")
    if os.path.exists(main_fileloc+".py"):
        build_c(main_fileloc+".py",main_fileloc+".c",exe_args=True)
        build_exe(main_fileloc+".c",main_fileloc+".exe",gui=True)
        if os.path.exists(main_fileloc+".exe"):
            exe_fileloc = os.path.abspath(cwd + "/plugins/Core/AvoAssureICE")
            if os.path.exists(exe_fileloc+".exe"):
                subprocess.check_call("del "+exe_fileloc+".exe", shell = True)
            os.rename(main_fileloc+".exe", exe_fileloc+".exe")
except Exception as e:
    print("Failed to build main file")
    print("Error: ", e)
build_recursive_dir_tree(cwd + sl +"plugins" + sl)
file_refer.close()


