import subprocess
import os
import sys
import json
from datetime import datetime
from os import walk
from os.path import splitext, join
import py_compile
cwd = os.getcwd()
#https://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html
#https://stackoverflow.com/questions/9875772/linux-c-linker-usr-bin-ld?lq=1
#https://www.linuxtopia.org/online_books/an_introduction_to_gcc/gccintro_14.html
#apt-get install libgtk2.0-0  for this error: ImportError: libgtk-x11-2.0.so.0: cannot open shared object file: No such file or directory
pythondir = os.path.dirname(sys.executable)
PY_MJR = str(sys.version_info.major)
PY_MIN = str(sys.version_info.minor)
LIB_FILE = PY_MJR+'.'+PY_MIN
INCLUDE_DIR = LIB_FILE + ('m' if PY_MJR == '3' else '')
errorcount = 0
ext_o_c_py = [".py", ".c"]
print(pythondir,PY_MJR,PY_MIN,LIB_FILE,INCLUDE_DIR)

# def  generate_manifest(semi_version):
#     try:
#         f=open("version.json","r")
#         ver=json.load(f)
#         f.close()
#         min_comp = max_comp = ver["version"]
#         updated_on = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
#         last_ice_patch_list = list(ver["iceversion"][semi_version].keys())
#         if len(last_ice_patch_list) > 0:
#             last_ice = ver["iceversion"][semi_version][last_ice_patch_list[-1]]
#             version = last_ice['tag']
#             min_comp = last_ice["min-compatibility"]
#             baseline=last_ice['baseline']
#             min_comp = last_ice["min-compatibility"]
#             max_comp = last_ice["max-compatibility"]
#         ice_ver = {
#             "version": version,
#             "p_tag": semi_version,
#             "updated_on": updated_on,
#             "baseline": baseline,
#             "min-compatibility": min_comp,
#             "max-compatibility": max_comp,
#             "rollback": False,
#             "rollback_on": "",
#             "isWebPackage": "True"
#         }
#         with open(cwd+os.sep+"assets"+os.sep+"about_manifest.json", "w") as f:
#            json.dump(ice_ver, f, indent="  ")
#         print("Generated Manifest for ICE version " + version)
#     except Exception as e:
#         print(e)


def build(full_path, file, file_refer):
    global errorcount
    try:
        # pending save error and filename to file
        full_path_c = os.path.splitext(full_path)[0]+".c"
        cython_process = subprocess.Popen(sys.executable + " -m cython -"+PY_MJR + " -o " +
                                          full_path_c+" " + full_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = cython_process.communicate()
        exitcode = cython_process.returncode
        if not exitcode == 0:
            errorcount = errorcount + 1
            file_refer.write(str(full_path) + "\nError:" +
                             str(err) + "\nOutput:" + str(out) + "\n------- \n")
            return
        full_path = full_path[:-3]  # removing extesnion
        file = file[:-3]
        gcc_cmd = "gcc -shared -I"+pythondir+"/include/python"+INCLUDE_DIR+" -L" + pythondir + \
            "/lib -Wl,-rpath="+pythondir+"/lib -Wall -o " + \
            full_path+".so "+full_path+".c -lpython3.7m -fPIC"
        #print(cmd)
        gcc_process_so = subprocess.Popen(
            gcc_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        out, err = gcc_process_so.communicate()
        exitcode = gcc_process_so.returncode
        if not exitcode == 0:
            errorcount = errorcount + 1
        #full_path = full_path.replace("/", "\\")
        if os.path.isfile(full_path + ".so"):
            for ext in ext_o_c_py:
                if os.path.isfile(full_path + ext):
                    subprocess.check_call("rm " + full_path + ext, shell=True)
    except subprocess.CalledProcessError as e:
        errorcount = errorcount + 1
        print(e)
        return


def select_files(ign, root, files):
    py_files = []
    ##print "\n\nDirectory =" + root + "\n"
    file_refer = open('../cython_error.txt', 'a')
    for file in files:
        full_path = os.path.normpath(join(root, file))
        extsn = splitext(file)[1]
        if extsn == ".py" and (full_path not in ign):
            py_files.append(full_path)
            build(full_path, file, file_refer)
    file_refer.close()
    return py_files


def build_recursive_dir_tree(path):
    selected_files = []
    ign = []
    # ign = [path + line.rstrip('\n') for line in open("./buildignore.txt")]
    # for i, ignv in enumerate(ign):
    #     ign[i] = os.path.normpath(ignv)
    #print (ign)
    for root, dirs, files in walk(path):
        root = os.path.normpath(root)
        if (root not in ign):
            selected_files += select_files(ign, root, files)
    return selected_files


def build_pyc(path):
    for i in os.listdir(path):
        if i.endswith("py"):
            fp = path+i
            py_compile.compile(fp, fp+"c")
            os.remove(fp)
    new_path = os.path.dirname(
        os.path.dirname(os.path.dirname(path)))+"/assets"
    py_compile.compile(new_path+"/Update.py", new_path+"/Update.pyc")
    os.remove(new_path+"/Update.py")
    py_compile.compile(new_path+"/IRISMT/IRISMT.py",
                       new_path+"/IRISMT/IRISMT.pyc")
    os.remove(new_path+"/IRISMT/IRISMT.py")
    py_compile.compile(new_path+"/ObjectPredictionMT/ObjectPredictionMT.py",
                       new_path+"/ObjectPredictionMT/ObjectPredictionMT.pyc")
    os.remove(new_path+"/ObjectPredictionMT/ObjectPredictionMT.py")


print("Building process initiated....")
print('Current directory ', cwd)

build_recursive_dir_tree(cwd + "/plugins/AWS")

# build_pyc(cwd+"/plugins/AWS/")

# generate_manifest("22.2")


if errorcount > 0:
    print("raise error")
    raise RuntimeError("BUILD FAILED : There are " +
                       str(errorcount) + " no of errors")
