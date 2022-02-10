import json
import datetime
dateobj=datetime.datetime.now()
import os
import sys
import time
import shutil
sl = os.sep

def exe_converter(file_loc):
    """Updater.exe will be created in the python directory in 'dist' folder"""
    """input : assets folder loc"""
    """Warning!!!! pyinstaller must be installed"""

    try:
        #---------------------> will make .py to .exe
        ico_path = os.path.abspath(os.path.join(file_loc,"..","build", "avo.ico"))
        target = file_loc+sl+"Update.py"
        if not os.path.exists(target): return
        os.system(os.path.join(os.path.dirname(sys.executable),"Scripts","pyinstaller") + " -F -w -i "+ico_path+" "+target)
        time.sleep(5)#-------------------------------->wait time for good measures
        #creates 2 folders where the same directory as this pyfile( dist and build)
        #creates 1 folder in Update folder (__pycache__)
        if os.path.exists(str(os.getcwd())+sl+"dist"+sl+"Update.exe"):
            shutil.move(str(os.getcwd())+sl+"dist"+sl+"Update.exe", file_loc+sl+"Update.exe")
        #1.delete Updater.py
        os.remove(file_loc+sl+"Update.py")
        #2.delete dist folder
        shutil.rmtree(str(os.getcwd())+sl+"dist", ignore_errors=False, onerror=None)
        #3.delete build folder
        shutil.rmtree(str(os.getcwd())+sl+"build", ignore_errors=False, onerror=None)
        #4.delete _pycache_ folder
        shutil.rmtree(file_loc+sl+"__pycache__", ignore_errors=False, onerror=None)
        #5.delete spec file
        os.remove(os.getcwd()+sl+"Update.spec")
        os.remove(file_loc+sl+"Update.spec")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print (e)


def create_manifest(tag,updated_on,baseline,mincomp,maxcomp,file_loc):
    """Creates about_manifest.json
    Index: 1.tag - indicates tag of current build. Eg: 3.1.X
           2.p_tag - indicates parent tag(alpha version) of ICE build. Eg: 3.1
           3.updated_on - indicates date-time when the build was created Eg: 8/31/2020, 23:44:41
           4.baseline - indicates the ICE build baseline(full full/delta package). Eg:True for full package, False for delta package
           5.min-compatibility - indicates the minimum server compatibility with ICE. Eg: 3.1.X
           6.max-compatibility - indicates the maximum server compatibility with ICE. Eg: 3.1.X
    """
    ver=tag[:tag.rindex('.')]
    subver=tag[tag.rindex('.')+1:]
    subver_data={}
    subver_data[subver]={"tag":tag,"p_tag":ver,"updated_on":updated_on,"baseline":baseline,"min-compatibility": mincomp, "max-compatibility": maxcomp}
    subver_data2={}
    subver_data2['subversion']=subver_data
    version_data1={}
    version_data1[ver]=subver_data2
    version_data2={}
    version_data2['iceversion']=version_data1
    version_data2['rollback'] = "False"
    version_data2['rollback_on']= ""
    with open(file_loc+sl+"about_manifest.json", 'w') as outfile:
        json.dump(version_data2, outfile)

if __name__ == '__main__':
    if len(sys.argv) != 2: raise RuntimeError("Invalid Arguments. python update.py tagnumber")
    tag = sys.argv[1]
    cwd = os.getcwd()
    path_prefix = "" if os.path.basename(cwd) == "AvoAssure" else "AvoAssure"
    file_loc = os.path.abspath(os.path.join(cwd, path_prefix, "assets"))
    if not os.path.exists(file_loc): os.makedirs(file_loc) 
    updated_on = str(dateobj.month)+'/'+str(dateobj.day)+'/'+str(dateobj.year)+', '+str(dateobj.hour)+":"+str(dateobj.minute)+":"+str(dateobj.second)
    create_manifest(tag,updated_on,"<baseline>","<mincomp>","<maxcomp>",file_loc)
    exe_converter(file_loc)
