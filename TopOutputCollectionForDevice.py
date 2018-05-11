import logging
import time

#This is code to make subprocess.check_output function compatible to python 2.6
try:
    from subprocess import check_output
except ImportError:
    # Python 2.6
    def check_output(*popenargs, **kwargs):
        """Run command with arguments and return its output as a byte string.
        Backported from Python 2.7 as it's implemented as pure python on stdlib.
        """
        import subprocess
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            error = subprocess.CalledProcessError(retcode, cmd)
            error.output = output
            raise error
        return output



#This function will give you Top command output
def topCommandOutputRemoteorLocal(linuxServer=None, username=None, password=None,isLocal=None):
    try:

        if isLocal == True:
            direct_output = check_output(
                "top -b -n 1| head -n 20", shell=True)
        else:
            direct_output = check_output(
                "sshpass -p %s ssh %s@%s 'top -b -n 1| head -n 20'" % (password, username, linuxServer),
                shell=True)
        return direct_output
    except Exception as e:
        print "Exception is :", str(e)
        return False

#This function will give you RAM,LOAD,CPU and SWAP from TopOutput
def parsedCPURAMLOADSWAPFromTopOutputRemoteorLocal(topOutput):
    topParamter = {}
    try:
        for value in topOutput.splitlines():
            if "load average:" in value:
                topParamter["LoadAverage"] = float(str(value.split("load average:")[1]).split(",")[0])
            if "Cpu(s):" in value:
                topParamter["CpuUsed"] = float((value.split("%us")[0]).split(":")[1])
            if "Mem:" in value:
                topParamter["RamUsed"] = float((value.split("k used")[0]).split(",")[1])
            if "Swap:" in value:
                topParamter["SwapUsed"] = float((value.split("k used")[0]).split(",")[1])
        print  topParamter
        return topParamter
    except Exception as e:
        print "Exception is :", str(e)

#This function will append parseOuput to respective list RAM,LOAD,CPU and SWAP
def appendValueToList(deviceData,topParamter):
    try:
        (deviceData["LoadAverage"]).append(topParamter["LoadAverage"])
        (deviceData["CpuUsed"]).append(topParamter["CpuUsed"])
        (deviceData["RamUsed"]).append(topParamter["RamUsed"])
        (deviceData["SwapUsed"]).append(topParamter["SwapUsed"])
    except Exception as e:
        print "Exception is :", str(e)


#Do Avarage for list RAM,LOAD,CPU and SWAP
def calculateAverage(Data,Min,deviceIP):
    try:
        MinMaxAvgResult["Time min"]= Min
        MinMaxAvgResult["deviceIP"] = deviceIP
        logging.info("Length of sample :%s",len(Data["CpuUsed"]))
        MinMaxAvgResult["CPU MAX"] = round(max(Data["CpuUsed"]), 2)
        MinMaxAvgResult["CPU MIN"] = round(min(Data["CpuUsed"]), 2)
        MinMaxAvgResult["CPU AVG"] = round(sum(Data["CpuUsed"]) / len(Data["CpuUsed"]), 2)
        MinMaxAvgResult["RAM MAX GB"] = round(max(Data["RamUsed"]) / 1024 / 1024, 2)
        MinMaxAvgResult["RAM MIN GB"] = round(min(Data["RamUsed"]) / 1024 / 1024, 2)
        MinMaxAvgResult["RAM AVG GB"] = round((sum(Data["RamUsed"]) / len(Data["RamUsed"])) / 1024 / 1024, 2)
        MinMaxAvgResult["SWAP MAX MB"] = round(max(Data["SwapUsed"]) / 1024, 2)
        MinMaxAvgResult["SWAP MIN MB"] = round(min(Data["SwapUsed"]) / 1024, 2)
        MinMaxAvgResult["SWAP AVG MB"] = round((sum(Data["SwapUsed"]) / len(Data["SwapUsed"])) / 1024, 2)
        MinMaxAvgResult["LOAD MAX"] = round(max(Data["LoadAverage"]), 2)
        MinMaxAvgResult["LOAD MIN"] = round(min(Data["LoadAverage"]), 2)
        MinMaxAvgResult["LOAD AVG"] = round(sum(Data["LoadAverage"]) / len(Data["LoadAverage"]), 2)
        return MinMaxAvgResult
    except Exception as e:
        print "Exception is :", str(e)

#Do Avarage for list RAM,LOAD,CPU and SWAP
def DumpToLogFile(MinMaxAvgResult):
    try:
        logging.info("%s-----%s min-------- ",MinMaxAvgResult["deviceIP"],MinMaxAvgResult["Time min"])
        logging.info("CPU : Max: %s  Min : %s  Avg : %s",MinMaxAvgResult["CPU MAX"],MinMaxAvgResult["CPU MIN"],MinMaxAvgResult["CPU AVG"])
        logging.info("RAM : Max: %s  Min : %s  Avg : %s",MinMaxAvgResult["RAM MAX GB"],MinMaxAvgResult["RAM MIN GB"],MinMaxAvgResult["RAM AVG GB"])
        logging.info("SWAP : Max: %s  Min : %s  Avg : %s",MinMaxAvgResult["SWAP MAX MB"],MinMaxAvgResult["SWAP MIN MB"],MinMaxAvgResult["SWAP AVG MB"])
        logging.info("LOAD : Max: %s  Min : %s  Avg : %s",MinMaxAvgResult["LOAD MAX"],MinMaxAvgResult["LOAD MIN"],MinMaxAvgResult["LOAD AVG"])
    except Exception as e:
        print "Exception is :", str(e)

def DumptoCSV(csvfileName,row):
    import csv,os
    iscreated = False
    if os.path.isfile(csvfileName):
        iscreated = True
    with open(csvfileName, 'a') as csvfile:
        fieldnames=['Time min','deviceIP','CPU MAX', 'CPU MIN', 'CPU AVG','RAM MAX GB', 'RAM MIN GB', 'RAM AVG GB','LOAD MAX', 'LOAD MIN', 'LOAD AVG','SWAP MAX MB', 'SWAP MIN MB','SWAP AVG MB']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if iscreated == False:
            writer.writeheader()
        writer.writerow(row)

import sys
if len(sys.argv) < 6:
    print "Run File :python Scriptname deviceIP intervalmin totalDurationmin averageDurationmin isScriptRunnningLocally(YES/NO)"
    exit()

deviceIP=sys.argv[1]
interval=int(sys.argv[2])
totalDurationmin=int(sys.argv[3])
averageDuration=int(sys.argv[4])
isScriptRunnningLocally=sys.argv[5]

if isScriptRunnningLocally.lower() == "yes":
    isScriptRunnningLocally = True
else:
    isScriptRunnningLocally = False

outputLogFile=deviceIP+".log"
csvfileName=deviceIP+".csv"
logging.basicConfig(filename=outputLogFile, level=logging.INFO, format='')
DeviceTopCommandCollectedSample = {"LoadAverage": [], "CpuUsed": [], "RamUsed": [], "SwapUsed": []}

countTime=0
while True:
    MinMaxAvgResult = {}
    topOuput = topCommandOutputRemoteorLocal(deviceIP,"root","FixStream",isLocal=isScriptRunnningLocally)
    topParamter = parsedCPURAMLOADSWAPFromTopOutputRemoteorLocal(topOuput)
    appendValueToList(DeviceTopCommandCollectedSample,topParamter)
    time.sleep(interval*60)
    countTime = countTime + interval
    if countTime%averageDuration == 0:
        MinMaxAvgResult=calculateAverage(DeviceTopCommandCollectedSample,countTime,deviceIP)
        DumpToLogFile(MinMaxAvgResult)
        DumptoCSV(csvfileName,MinMaxAvgResult)
    if countTime > totalDurationmin:
        break;

MinMaxAvgResult= calculateAverage(DeviceTopCommandCollectedSample,countTime,deviceIP)
DumpToLogFile(MinMaxAvgResult)
DumptoCSV(csvfileName,MinMaxAvgResult)

