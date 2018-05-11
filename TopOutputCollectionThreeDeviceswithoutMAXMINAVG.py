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
                topParamter["LOAD"] = float(str(value.split("load average:")[1]).split(",")[0])
            if "Cpu(s):" in value:
                topParamter["CPU"] = float((value.split("%us")[0]).split(":")[1])
            if "Mem:" in value:
                topParamter["RAM GB"] = round(float((value.split("k used")[0]).split(",")[1])/1024/1024,2)
            if "Swap:" in value:
                topParamter["SWAP MB"] = round(float((value.split("k used")[0]).split(",")[1])/1024,2)
        print  topParamter
        return topParamter
    except Exception as e:
        print "Exception is :", str(e)


#Do Avarage for list RAM,LOAD,CPU and SWAP
def DumpToLogFile(Top):
    try:
        logging.info("MIN : %s  CPU :  %s   RAM GB :  %s   SWAP : %s  LOAD : %s",Top["Time min"],Top["CPU"],Top["RAM GB"],Top["SWAP MB"],Top["LOAD"])
    except Exception as e:
        print "Exception is :", str(e)

def DumptoCSV(csvfileName,row):
    import csv,os
    iscreated = False
    if os.path.isfile(csvfileName):
        iscreated = True
    with open(csvfileName, 'a') as csvfile:
        fieldnames=['Time min','deviceIP','CPU','RAM GB','LOAD','SWAP MB']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if iscreated == False:
            writer.writeheader()
        writer.writerow(row)

import sys
if len(sys.argv) < 4:
    print "Please run : scriptName deviceIP interval(min) Duration(min)"
    exit()

deviceIP=sys.argv[1]
interval=int(sys.argv[2])
totalDurationmin=int(sys.argv[3])

outputLogFile=deviceIP+".log"
logging.basicConfig(filename=outputLogFile, level=logging.INFO, format='')
csvfileName=deviceIP+".csv"

countTime=0
while True:
    topOuput = topCommandOutputRemoteorLocal(deviceIP,"root","FixStream",isLocal=False)
    topParamter = parsedCPURAMLOADSWAPFromTopOutputRemoteorLocal(topOuput)
    topParamter["Time min"]=countTime
    topParamter["deviceIP"]=deviceIP
    DumpToLogFile(topParamter)
    DumptoCSV(csvfileName, topParamter)
    time.sleep(interval*60)
    countTime=countTime+interval
    if countTime > totalDurationmin:
        break;
