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
log = logging.getLogger('bench_mark.py')
resArray = []
string = ""
host = ["10.41.31.99", "google.com"]
socketIO = None
bench_thread = None

def init(*args, **kw):
    global bench_thread
    global socketIO
    socketIO = args[0]
    stop()
    start(10)

def start(t=1800):
    global bench_thread
    bench_thread = threading.Timer(t, execute)
    bench_thread.start()

def stop():
    if (bench_thread is not  None) and bench_thread.isAlive():
        bench_thread.cancel()

def cpu():
    logger.print_on_console("Running CPU benchmark")
    for j in range(3):
        beforeCpu = time.time()
        arr = []
        global string
        for i in range(0,300):
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
    logger.print_on_console("Running memory benchmark")
    global string
    try:
        os.unlink("output.txt")
    except Exception as e:
        log.error(e)
    for x in range(4):
        string = string + string
    for j in range(2): 
        beforeFile = time.time()
        for i in range(40):
            f = open("output.txt", "a")
            f.write(string)
            f.close()
        for i in range(4):
            f = open("output.txt", "r")
            f.read()
            f.close()
        os.unlink("output.txt")
        afterFile = time.time()
        resArray.append(afterFile - beforeFile)
    sum = 0
    for i in range(len(resArray)):
        sum += resArray[i]
        
    result = sum/len(resArray)
    print("Memory Performance",result)
    return result

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
	p = subprocess.Popen(["ping.exe",host], stdout = subprocess.PIPE)
	result = p.communicate()[0]
	for row in str(result).split("\\r\\n"):
		if 'Average' in row:
			x = row.split("Average = ")[1].split("ms")[0]
			return float(x)
	return -1

def network():
    logger.print_on_console("Running network benchmark")
    global host
    loss = 0
    sent = 0
    for i in range(2):
        for j in range(len(host)):
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

def execute():
    global string,resArray
    string = ""
    resArray = []
    logger.print_on_console("Starting Benchmark execution")
    logger.print_on_console("Executing system benchmark")
    a,percent = network()
    b = cpu()
    c = memory()
    #a = b = c = 452
    result = (a+b+c)/3
    logger.print_on_console("Benchmark result: ",result)
    socketIO.emit('benchmark_ping',{'cpuscore':b,"time":time.ctime(),"memoryscore":c,"networkscore":a,"percent_received":str(percent * 100) + '%',"hostip":socket.gethostbyname(socket.gethostname()),"hostname":os.environ['username'],"systemscore":result})
    start(300)

