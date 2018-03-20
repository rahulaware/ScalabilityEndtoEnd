from Library import RequiredAPI;
import collections,time,json,logging
from Library import UserfulFunction;

#This function is called only once when schedule start
def startDump(IP,deviceCount,fileName):
    try:
        with open(fileName,"a") as fh:
            fh.write("*************************Schedule Discovery with %s*******************\n"%str(deviceCount))
        dumpOutput(IP,fileName)
    except Exception as e:
        print "Exception is :"+str(e)

#This funtion dumps parsed command ouput of top command
def dumpOutput(IP,fileName):
    try:
        global NCETopOutput, NCE1TopOutput, NCE2TopOutput, DCTopOutput,NCE_IP,NCE_W1,NCE_W2,DC_IP
        with open(fileName, "a") as fh:
            top_output = UserfulFunction.topCommandOutput(IP,"root","FixStream")
            topParamter =UserfulFunction.parsedCPURAMLOADSWAPFromTopOutput(top_output)
            if(IP == NCE_IP):
                (NCETopOutput["LoadAverage"]).append(topParamter["LoadAverage"])
                (NCETopOutput["CpuUsed"]).append(topParamter["CpuUsed"])
                (NCETopOutput["RamUsed"]).append(topParamter["RamUsed"])
                (NCETopOutput["SwapUsed"]).append(topParamter["SwapUsed"])
            if (IP == NCE_W1):
                (NCE1TopOutput["LoadAverage"]).append(topParamter["LoadAverage"])
                (NCE1TopOutput["CpuUsed"]).append(topParamter["CpuUsed"])
                (NCE1TopOutput["RamUsed"]).append(topParamter["RamUsed"])
                (NCE1TopOutput["SwapUsed"]).append(topParamter["SwapUsed"])
            if (IP == NCE_W2):
                (NCE2TopOutput["LoadAverage"]).append(topParamter["LoadAverage"])
                (NCE2TopOutput["CpuUsed"]).append(topParamter["CpuUsed"])
                (NCE2TopOutput["RamUsed"]).append(topParamter["RamUsed"])
                (NCE2TopOutput["SwapUsed"]).append(topParamter["SwapUsed"])
            if (IP == DC_IP):
                (DCTopOutput["LoadAverage"]).append(topParamter["LoadAverage"])
                (DCTopOutput["CpuUsed"]).append(topParamter["CpuUsed"])
                (DCTopOutput["RamUsed"]).append(topParamter["RamUsed"])
                (DCTopOutput["SwapUsed"]).append(topParamter["SwapUsed"])
            fh.write(top_output)
            fh.write("----------------------------------------------------------------------------\n")
    except Exception as e:
        print "Exception is :"+str(e)

def outputSaveInLogFile(DeviceType,Data):
    global ScheduleStatus
    maxCPU= round(max(Data["CpuUsed"]),2)
    minCPU= round(min(Data["CpuUsed"]),2)
    avgCPU= round (sum(Data["CpuUsed"]) / len(Data["CpuUsed"]),2)
    maxRAM = round(max(Data["RamUsed"])/1024/1024,2)
    minRAM = round(min(Data["RamUsed"])/1024/1024,2)
    avgRAM = round((sum(Data["RamUsed"]) / len(Data["RamUsed"]))/1024/1024,2)
    maxSWAP = round(max(Data["SwapUsed"]) / 1024,2)
    minSWAP = round(min(Data["SwapUsed"]) / 1024,2)
    avgSWAP = round((sum(Data["SwapUsed"]) / len(Data["SwapUsed"])) / 1024,2)
    maxLOAD = round(max(Data["LoadAverage"]),2)
    minLOAD = round(min(Data["LoadAverage"]),2)
    avgLOAD = round(sum(Data["LoadAverage"]) / len(Data["LoadAverage"]),2)

    logging.info("-----%s-------- ",DeviceType)
    logging.info("CPU : Max: %s  Min : %s  Avg : %s",maxCPU ,minCPU ,avgCPU)
    logging.info("RAM : Max: %s  Min : %s  Avg : %s", maxRAM, minRAM,avgRAM)
    logging.info("SWAP : Max: %s  Min : %s  Avg : %s", maxSWAP,minSWAP,avgSWAP)
    logging.info("LOAD : Max: %s  Min : %s  Avg : %s", maxLOAD,minLOAD,avgLOAD)

    ScheduleStatus[DeviceType + " CPU MIN"]= minCPU
    ScheduleStatus[DeviceType + " CPU MAX"] = maxCPU
    ScheduleStatus[DeviceType + " CPU AVG"] = avgCPU
    ScheduleStatus[DeviceType + " RAM MIN"] = minRAM
    ScheduleStatus[DeviceType + " RAM MAX"] = maxRAM
    ScheduleStatus[DeviceType + " RAM AVG"] = avgRAM
    ScheduleStatus[DeviceType + " SWAP MIN"] = minSWAP
    ScheduleStatus[DeviceType + " SWAP MAX"] = maxSWAP
    ScheduleStatus[DeviceType + " SWAP AVG"] = avgSWAP
    ScheduleStatus[DeviceType + " LOAD MIN"] = minLOAD
    ScheduleStatus[DeviceType + " LOAD MAX"] = maxLOAD
    ScheduleStatus[DeviceType + " LOAD AVG"] = avgLOAD


def devicePresenceInInventory(Token,Org,Site,listOfIPs,NumberOfTime):
    try:
        global NCE_IP,ScheduleStatus
        InventoryData = RequiredAPI.getInventoryTable(NCE_IP, Token, Org, Site)

        NumberofPresentDevices,MissingList = RequiredAPI.check_Device_Existance_In_Inventory(InventoryData, listOfIPs)
        logging.info("==Inventory Status %s==",str(NumberOfTime))
        logging.info("Number of Devices Present Inventory: %s",str(NumberofPresentDevices))
        PassPercent = round((NumberofPresentDevices * 100) / float(len(listOfIPs)),2)
        logging.info("Pass Percent: %s", str(PassPercent))
        logging.info("Fail Percent: %s", str(100-PassPercent))
        ScheduleStatus["NoOfDeviceInventory" + str(NumberOfTime)] = str(NumberofPresentDevices)
        ScheduleStatus["Passed%InventoryStatus"+ str(NumberOfTime)]= str(PassPercent)
        if MissingList:
            logging.info("MissingList Devices: %s", str(MissingList))
        return PassPercent
    except Exception as e:
        print e

NCE_IP = "172.16.2.112"
NCE_W1 = "172.16.2.113"
NCE_W2 = "172.16.2.114"
DC_IP = "172.16.2.115"
NCE_IPOutput = "172.16.2.112Output.txt"
NCE_W1Output = "172.16.2.113Output.txt"
NCE_W2Output = "172.16.2.114Output.txt"
DC_IPOutput = "172.16.2.115Output.txt"

SiteName= "US"
outputFileName="Discovery.xlsx"
outputLogFile="discovery.log"
fieldnames = {'DeviceCount':1, 'DiscoveryCompletionTime':2,'NoOfDeviceInventory0':3,'Passed%InventoryStatus0':4,'NoOfDeviceInventory1':5,\
              'Passed%InventoryStatus1':6,'NoOfDeviceInventory2':7,'Passed%InventoryStatus2':8,'NCE LOAD MIN':9,\
              'NCE LOAD MAX':10,'NCE LOAD AVG':11,'NCE CPU MIN':12,'NCE CPU MAX':13,'NCE CPU AVG':14,'NCE RAM MIN':15,'NCE RAM MAX':16,\
              'NCE RAM AVG':17,'NCE SWAP MIN':18,'NCE SWAP MAX':19,'NCE SWAP AVG':20,'DC LOAD MIN':21,\
              'DC LOAD MAX':22,'DC LOAD AVG':23,'DC CPU MIN':24,'DC CPU MAX':25,\
              'DC CPU AVG':26,'DC RAM MIN':27,'DC RAM MAX':28,'DC RAM AVG':29,'DC SWAP MIN':30,\
              'DC SWAP MAX':31,'DC SWAP AVG':32,'NCEW1 LOAD MIN':33,'NCEW1 LOAD MAX':34,'NCEW1 LOAD AVG':35,'NCEW1 CPU MIN':36,\
              'NCEW1 CPU MAX':37,'NCEW1 CPU AVG':38,'NCEW1 RAM MIN':39,'NCEW1 RAM MAX':40,\
              'NCEW1 RAM AVG':41,'NCEW1 SWAP MIN':42,'NCEW1 SWAP MAX':43,'NCEW1 SWAP AVG':44,\
              'NCEW2 LOAD MIN':45,'NCEW2 LOAD MAX':46,'NCEW2 LOAD AVG':47,'NCEW2 CPU MIN':48,\
              'NCEW2 CPU MAX':49,'NCEW2 CPU AVG':50,'NCEW2 RAM MIN':51,'NCEW2 RAM MAX':52,\
              'NCEW2 RAM AVG':53,'NCEW2 SWAP MIN':54,'NCEW2 SWAP MAX':55,'NCEW2 SWAP AVG':56,'Failure Reason':57}


logging.basicConfig(filename=outputLogFile, level=logging.INFO, format='')

#Generation of Ordered list containing numberof devices and start/end IP
numberofdeviceList=[100,200,300,400,500,750,1000,1200,1500,2000,2500,3000]
discoveryList=collections.OrderedDict()
newStartIP="10.50.1.1"
for deviceCount in numberofdeviceList:
    try:
        startIP=newStartIP;
        discoveryInput,newStartIP=UserfulFunction.returnRangestartEndIP(startIP,deviceCount)
        discoveryList[deviceCount]=discoveryInput;
        logging.info("%s===============================%s", str(deviceCount), startIP)
    except Exception as e:
        print str(e)

# print deviceCount,discoveryInput["startIP"],discoveryInput['endIP'],str(len(discoveryInput["listOfIP"]))
Token = RequiredAPI.getToken(NCE_IP)
# print "token created"
Org, Site = RequiredAPI.getOrgAndSite(NCE_IP, Token, SiteName)
# print "ORG and Site ID selected"

#Scheduling discovery
for deviceCount, discoveryInput in discoveryList.items():
    ScheduleStatus={}
    ScheduleStatus["DeviceCount"]= deviceCount
    NCETopOutput = {"LoadAverage": [], "CpuUsed": [], "RamUsed": [], "SwapUsed": []}
    NCE1TopOutput = {"LoadAverage": [], "CpuUsed": [], "RamUsed": [], "SwapUsed": []}
    NCE2TopOutput = {"LoadAverage": [], "CpuUsed": [], "RamUsed": [], "SwapUsed": []}
    DCTopOutput = {"LoadAverage": [], "CpuUsed": [], "RamUsed": [], "SwapUsed": []}

    #Dump top command output
    startDump(NCE_IP, deviceCount, NCE_IPOutput)
    startDump(NCE_W1, deviceCount, NCE_W1Output)
    startDump(NCE_W2, deviceCount, NCE_W2Output)
    startDump(DC_IP, deviceCount, DC_IPOutput)

    listOfIPs=discoveryInput["listOfIP"]
    logging.info("*************************Schedule Discovery with %s Result*******************", str(deviceCount))
    try:
        requestPayload = {"scheduleInfo": {"recurrence": "NOW", "recurrenceMin": "", "scheduleDate": "", "scheduleTime": "",
                                           "recurrenceHour": "", "scheduleTimeAMPM": "", "scheduleEndDate": "",
                                           "scheduleEndTime": "", "scheduleEndTimeAMPM": ""}, "resetCredentials": False,
                          "triggerType": "NETWORK_DISCOVERY", "communityStringInfo": [],
                          "ipPool": {"fqdnAddress": [], "ipRange": [{"ipAddressFrom": "", "ipAddressTo": ""}],
                                     "maskRange": []}, "discoveredDeviceType": "True", "dsSelectedOrganization": "#",
                          "requestName": "", "authList": [
                {"username": "root", "api": "", "ssh": True, "jumpServer": "", "windows": "", "jumpServeripAddress": "",
                 "password": "FixStream", "apiType": "", "userProfile": "", "telnet": "", "sshkey": ""}],
                          "enabledPasswordList": [{"enablePassword": ""}],
                          "applicationProperties:q"
                          "": {"openstackDetails": []}, "dsSelectedSiteId": "*"}
        requestPayload["ipPool"]["ipRange"][0]["ipAddressFrom"]= discoveryInput["startIP"]
        requestPayload["ipPool"]["ipRange"][0]["ipAddressTo"] =discoveryInput['endIP']
        requestPayload["requestName"]=deviceCount
        requestPayload["dsSelectedSiteId"]=Site
        requestPayload["dsSelectedOrganization"]=Org
        requestPayload=json.dumps(requestPayload)

        response= RequiredAPI.schedule_discovery(NCE_IP,Token,Org,Site,requestPayload)
        logging.info("DeviceCount: %s and RequestID: %s", str(deviceCount),response)
        numberofSecond=0;
        while True:
            try:
                #Dump top output and take cppu,load,ram,swap
                dumpOutput(NCE_IP, NCE_IPOutput)
                dumpOutput(NCE_W1, NCE_W1Output)
                dumpOutput(NCE_W2, NCE_W2Output)
                dumpOutput(DC_IP, DC_IPOutput)
                value,requestId = RequiredAPI.get_all_scheduledDiscoveryRequest(NCE_IP,Token,Org,Site,"NETWORK_DISCOVERY")
                if value == 0:
                    requestPayload=None
                    break;
                time.sleep(120)
                numberofSecond = numberofSecond + 120
                if value == 1 and (numberofSecond/60) > 60 :
                    try:
                        res= RequiredAPI.deleteRequest(NCE_IP,Token,Org,Site,requestId)
                    except Exception as e:
                        print "Exception is :" + str(e)
                    break;
            except Exception as e:
                logging.info("Excpetion :%s",str(e))

        CompletionTime = numberofSecond / 60
        logging.info("Completion Time (min):%s", str(CompletionTime))
        ScheduleStatus["DiscoveryCompletionTime"] = CompletionTime

        outputSaveInLogFile("NCE", NCETopOutput)
        outputSaveInLogFile("NCEW1", NCE1TopOutput)
        outputSaveInLogFile("NCEW2",NCE2TopOutput)
        outputSaveInLogFile("DC", DCTopOutput)

        NumberOfTime=0
        timeWait=600
        logging.info("-----Inventory Status----")
        while True:
            Time= CompletionTime+ (timeWait * NumberOfTime)/60
            PassPercent=devicePresenceInInventory(Token,Org,Site,listOfIPs,NumberOfTime)
            NumberOfTime=NumberOfTime+1
            if PassPercent >= 100:
                break;
            if NumberOfTime==3:
                break
            time.sleep(timeWait)
        #logging.info("Data is ---------")
        logging.info("Data is : %s",ScheduleStatus)
        #UserfulFunction.CreateandStoreOutputCSVFile(outputFileName,fieldnames,ScheduleStatus)
        UserfulFunction.StoreOutputInExcelColumnwise(outputFileName,fieldnames,ScheduleStatus)
    except Exception as e:
        logging.info("Exception : %s",str(e))
