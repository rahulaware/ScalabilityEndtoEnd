import subprocess

#Take startIP and deviceCount :-> StartIP,EndIP,List of devices between them and newStartIP
def returnRangestartEndIP(startIP,deviceCount):
    try:
        startIpList= startIP.split(".")
        third_index=int(startIpList[2])
        fourth_index=int(startIpList[3])
        discoveryInput = {}
        listOfIP=[]
        count = 1
        for thirdIndex in range(third_index, 255):
            for fourthIndex in range(fourth_index, 255):
                ip_Address = str(startIpList[0]) + "." + str(startIpList[1]) + "." + str(thirdIndex) + "." + str(fourthIndex);
                if count == 1:
                    discoveryInput["startIP"] = ip_Address
                elif count == deviceCount:
                    discoveryInput["endIP"] = ip_Address
                if count > int(deviceCount):
                    newStartPoint = ip_Address
                    break;
                elif fourthIndex == 254:
                    fourth_index = 1
                listOfIP.append(ip_Address)
                count = count + 1
            if count > int(deviceCount):
                break
        discoveryInput["listOfIP"]=listOfIP
        return discoveryInput,newStartPoint
    except Exception as e:
        print "Exception is:",str(e)
        return False,False;


def topCommandOutput(linuxServer,username,password):
    try:
        direct_output = subprocess.check_output(
            "sshpass -p %s ssh %s@%s 'top -b -n 1| head -n 20'" % (password, username, linuxServer),
            shell=True)
        return direct_output
    except Exception as e:
        print "Exception is :",str(e)
        return False

def parsedCPURAMLOADSWAPFromTopOutput(topOutput):
    topParamter={}
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
        return topParamter
    except Exception as e:
        print "Exception is :",str(e)

#CSV Report Generation ROW By ROW
'''fieldnames = ['DeviceCount', 'DiscoveryCompletionTime','NoOfDeviceInventory0','PassedInventoryStatus0','NoOfDeviceInventory1',\
              'PassedInventoryStatus1','NoOfDeviceInventory2','PassedInventoryStatus2','NCE LOAD MIN',\
              'NCE LOAD MAX','NCE LOAD AVG','NCE CPU MIN','NCE CPU MAX','NCE CPU AVG','NCE RAM MIN','NCE RAM MAX','NCE RAM AVG',\
              'NCE SWAP MIN','NCE SWAP MAX','NCE SWAP AVG','DC LOAD MIN','DC LOAD MAX','DC LOAD AVG','DC CPU MIN','DC CPU MAX',\
              'DC CPU AVG','DC RAM MIN','DC RAM MAX','DC RAM AVG','DC SWAP MIN','DC SWAP MAX','DC SWAP AVG','Failure Reason']
'''
import os
import csv
def CreateandStoreOutputCSVFile(filename,fieldnames,Output):
    if not (os.path.exists(filename)):
        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(Output)

from openpyxl import load_workbook
import string
def StoreOutputInExcelColumnwise(filename,fieldnames,Output):
    try:
        Excel = load_workbook(filename=filename)
        SiteSheet = Excel["Sheet1"]
        for letter in string.ascii_uppercase:
            if (SiteSheet[letter + "1"]).value == None:
                break;
        print letter
        for key in Output:
            SiteSheet[letter + str(fieldnames[key])] = Output[key]
        Excel.save(filename)
    except Exception as e:
        print "Exception is :"+str(e)
