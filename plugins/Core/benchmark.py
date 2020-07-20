import time
import os
import random
import sys 
from decimal import Decimal
import math
import logging
import logging.config
import logger
import platform   
import subprocess
import threading
import socket
import datetime
import core
import readconfig

log = logging.getLogger('benchmark.py')
resArray = []
string = ""
configvalues = readconfig.readConfig().readJson()
host = [configvalues["server_ip"], "google.com"]
socketIO = None
bench_thread = []
threadNames = []
terminated = False

def init(times,socket):
    global bench_thread,terminated
    global socketIO
    socketIO = socket
    if len(threadNames) is not 0:
        stop(False)
    times = []
    display_str = "Benchmark Execution Scheduled at "
    for i in range(len(times)):
        timeNow =  datetime.datetime.today()
        display_str = display_str + times[i] + " "
        schedTime = datetime.datetime.strptime(times[i],"%H:%M")
        delta = schedTime - timeNow
        start(delta.seconds + 1,"bench_thread"+str(i),schedTime)
    logger.print_on_console(display_str)


def start(t,name,schedTime):
    global bench_thread,threadNames,terminated
    terminated = False
    for i in range(len(threadNames)):
        if threadNames[i].getName() is name:
            threadNames[i].cancel()
            time.sleep(1)
    bench_thread = threading.Timer(t, execute,[name,schedTime])
    bench_thread.setName(name)
    threadNames.append(bench_thread)
    bench_thread.start()

def stop(terminateExec):
    global terminated,bench_thread,threadNames
    bench_thread = []
    delete_memory_test_file()
    terminated = True
    if terminateExec:
        return
    for i in range(len(threadNames)):
        threadNames[i].cancel()
        time.sleep(1)
    threadNames = []
    return
   
def delete_memory_test_file():
    global terminated
    if os.path.exists('output.txt'):
        try:
            os.unlink('output.txt')
            return True
        except Exception as e:
            log.error(e)
            terminated = True
            logger.print_on_console("Another instance of benchmark running, terminating.")



def cpu():
    global terminated
    logger.print_on_console("Running CPU benchmark")
    for j in range(3):
        beforeCpu = time.time()
        arr = []
        global string
        for i in range(0,350):
            if terminated:
                return -99
            x = random.randint(1,100001)
            arr.append(pow(pow(x, random.randint(1,10)),1/random.randint(1,10))) 
            random.shuffle(arr)
            arr.reverse()
            arr = selectionSort(arr)
            string = string + ''.join(str(e) for e in arr)
            binArr = []
            binArr = arr[:]
            convertToBinary(binArr)
        afterCpu = time.time()
        result = afterCpu - beforeCpu
        resArray.append(result)
    sum = 0
    for i in range(len(resArray)):
        sum += resArray[i]
    return sum/len(resArray)
        
def memory():
    try:
        global terminated
        logger.print_on_console("Running memory benchmark")
        global string
        delete_memory_test_file()
        for x in range(4):
            string = string + string
        for j in range(2): 
            if terminated:
                return -99
            beforeFile = time.time()
            if os.path.exists("output.txt"):
                outputFile = os.stat("output.txt")
                if outputFile.st_size/100000 > 4000:
                    delete_memory_test_file()
            for i in range(30):
                if terminated:
                    return -99
                f = open("output.txt", "a")
                f.write(string)
                f.close()
            for i in range(4):
                if terminated:
                    return -99
                f = open("output.txt", "r")
                f.read()
                f.close()
            delete_memory_test_file()
            afterFile = time.time()
            resArray.append(afterFile - beforeFile)
        sum = 0
        for i in range(len(resArray)):
            sum += resArray[i]
            
        result = sum/len(resArray)
        print("Memory Performance",result)
        return result
    except Exception as e:
        logger.print_on_console("Error in Benchmark Execution")
        return -99

def selectionSort(arr):
    for i in range(len(arr)): 
        min_idx = i 
        for j in range(i+1, len(arr)): 
            if arr[min_idx] > arr[j]: 
                min_idx = j 
                       
        arr[i], arr[min_idx] = arr[min_idx], arr[i] 
    return arr

def dec2bin(dec):
    return bin(math.ceil(dec))

def convertToBinary(rr):
    for i in range(len(rr)):
        rr[i] = dec2bin(rr[i])
  
def ping(host):
    p = subprocess.Popen(["ping.exe",host], stdout = subprocess.PIPE, shell = True)
    result = p.communicate()[0]
    for row in str(result).split("\\r\\n"):
        if 'Average' in row:
            x = row.split("Average = ")[1].split("ms")[0]
            return float(x)
    return -1

def network():
    logger.print_on_console("Running network benchmark")
    global host,terminated
    if terminated:
        return -99,-99
    loss = 0
    sent = 0
    for i in range(2):
        for j in range(len(host)):
            if terminated: 
                return -99,-99
            sent += 1
            p = ping(host[j])
            if p == -1: 
                loss += 1
            else:
                resArray.append(ping(host[j]))
    sum = 0
    for i in range(len(resArray)):
        sum += resArray[i]
    #print("Network Performance",sum/len(resArray))
    logger.print_on_console("Packet Sent ",sent)
    logger.print_on_console("Packet Lost ",loss)
    return sum/len(resArray), ((sent - loss)/sent)

def execute(name,schedTime):
    global string,resArray,terminated,socketIO
    timeNow =  datetime.datetime.today()
    delta = schedTime - timeNow
    
    if core.execution_flag:
        logger.print_on_console("Execution in progress, terminating Benchmark Execution")
        start(delta.seconds,name,schedTime)
        return
    if terminated:
        logger.print_on_console("Benchmark execution terminating.")
        start(delta.seconds,name,schedTime)
        return
    try:
        string = ""
        resArray = []
        logger.print_on_console("Starting Benchmark execution")
        a,percent = network()
        b = cpu()
        c = memory()
        timeNow =  datetime.datetime.today()
        delta = schedTime - timeNow
        if a == -99 or b == -99 or c == -99:
            logger.print_on_console("Terminating Benchmark Execution")
            start(delta.seconds,name,schedTime)
            return
        result = (a+b+c)/3
        logger.print_on_console("Benchmark result: ",result)
        if terminated:
            logger.print_on_console("Terminating Benchmark Execution")
            start(delta.seconds,name,schedTime)
            return 
        socketIO.emit('benchmark_ping',{'cpuscore':b,"memoryscore":c,"networkscore":a,"percent_received":str(percent * 100) + '%',"hostip":socket.gethostbyname(socket.gethostname()),"hostname":os.environ['username'],"systemscore":result,"time":str(datetime.datetime.now())})
        start(delta.seconds,name,schedTime)
        return
    except Exception as e:
        delete_memory_test_file()
        logger.print_on_console("Error in Benchmark Execution, terminating.")
        log.error(e)
        start(delta.seconds,name,schedTime)
        return

