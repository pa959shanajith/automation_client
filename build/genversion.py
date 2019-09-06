#-------------------------------------------------------------------------------
# Name:        Generate Package Build and Release Version
# Purpose:
#
# Author:      ranjan.agrawal
#
# Created:     26-02-2019
# Copyright:   (c) ranjan.agrawal 2019
#-------------------------------------------------------------------------------

import os
import re
import sys
import platform
from subprocess import Popen, PIPE
from datetime import datetime

if platform.system() == "Windows": FILTER_ARG = "find"
else: FILTER_ARG = "grep"
GRAPH_CMD = ["git", "log", "--graph", "--decorate", "--oneline"]
FILTER_CMD = ["origin/master", "origin/production_2.", "production"]
TAG_CMD = ["git", "ls-remote", "--tags", ".git"]
OUT_FILE = './out.txt'
RUNTIME_ERROR = RuntimeError("Error while generating version")

def env(key):
    if key in os.environ:
        #print(key+" is "+os.environ[key])
        return os.environ[key]
    return ""

def process_out(refs):
    file_ref = open(OUT_FILE, 'r')
    chk = Popen(FILTER_ARG + ' "'+refs+'"', stderr=PIPE, stdout=PIPE, stdin=file_ref)
    out, err = chk.communicate()
    file_ref.close()
    if err:
        print(err)
        return "error"
    if sys.version_info.major == 3:
        out = out.decode('utf-8')
    if len(out.strip()) == 0: return ''
    if "master" in refs: return env("MINOR_VERSION")
    matches = re.findall("production_2\.[0-9]+", out)
    if len(matches) == 0: return ''
    return matches[0][13:]

def get_minor_ver():
    global BUILD
    if BRANCH == "master": return env("MINOR_VERSION")
    if BRANCH.startswith("production_2."): return BRANCH[13:]

    file_ref = open(OUT_FILE, 'w+')
    graph_out = Popen(GRAPH_CMD, stderr=PIPE, stdout=file_ref)
    file_ref.close()
    err = graph_out.communicate()[1]
    if err:
        print(err)
        raise RUNTIME_ERROR
    processed = ""
    for c in FILTER_CMD:
        processed = process_out(c)
        if processed == "error":
            raise RUNTIME_ERROR
        elif len(processed) != 0: break
    if len(processed) == 0:
        BUILD = "DEV"
        processed = env("MINOR_VERSION")
        print("Failed to find a parent branch to get minor version.\n"+
            "Assuming 'master' as parent.\n"+
            "Since, branch source is invalid, switching build to DEV mode")
    os.remove(OUT_FILE)
    return processed


def get_patch_ver():
    if BUILD == "DEV": return datetime.now().strftime("%Y%m%d%H%M")
    ver = MAJOR_VERSION+r"\."+MINOR_VERSION+r"\."
    TAG_CMD.append(ver+"[0-9]*")
    tag_out = Popen(TAG_CMD, stderr=PIPE, stdout=PIPE)
    out, err = tag_out.communicate()
    if err:
        print(err)
        raise RUNTIME_ERROR
    if sys.version_info.major == 3:
        out = out.decode('utf-8')
    if len(out) == 0: return "0"
    #matches = re.findall(ver+"([0-9]+)", out)
    matches = re.findall(ver+"([0-9]{0,9})\n", out)
    matches.sort(key=int)
    if len(matches) == 0: return "0"
    return str(int(matches[-1])+1)

BUILD = env("BUILD_ENV")
if BUILD=="": BUILD="PROD"
CBU = env("CBU")
if CBU=="": CBU="RC"
BRANCH = env("BRANCH")
MAJOR_VERSION = env("MAJOR_VERSION")
MINOR_VERSION = get_minor_ver()
PATCH_VERSION = get_patch_ver()

RELEASE_VERSION = MAJOR_VERSION+"."+MINOR_VERSION+"."+PATCH_VERSION
print("Release number for patch is "+RELEASE_VERSION)
os.system("echo "+RELEASE_VERSION+">buildno.txt")
with open("setenv","w") as exportenv:
    exportenv.write("MAJOR_VERSION="+MAJOR_VERSION+"\nMINOR_VERSION="+MINOR_VERSION
    +"\nPATCH_VERSION="+PATCH_VERSION+"\nBUILD_NUMBER="+RELEASE_VERSION+"\nCBU="+CBU)
#with open("env.bat","w+") as exportenv:
#    exportenv.write("SET BUILD="+BUILD+"\nSET MAJOR_VERSION="+MAJOR_VERSION+"\nSET MINOR_VERSION="+MINOR_VERSION+"\nSET PATCH_VERSION="+PATCH_VERSION)
#with open("env","w+") as exportenv:
#    exportenv.write("export BUILD="+BUILD+"\nexport MAJOR_VERSION="+MAJOR_VERSION+"\nexport MINOR_VERSION="+MINOR_VERSION+"\nexport PATCH_VERSION="+PATCH_VERSION)
