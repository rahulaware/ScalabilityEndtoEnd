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
        global NCE_IP,ScheduleStatus,ScheduleInventoryStatus
        InventoryData = RequiredAPI.getInventoryTable(NCE_IP, Token, Org, Site)

        NumberofPresentDevices,MissingList = RequiredAPI.check_Device_Existance_In_Inventory(InventoryData, listOfIPs)
        logging.info("==Inventory Status after %s min ==",str(NumberOfTime*2))
        logging.info("Number of Devices Present Inventory: %s",str(NumberofPresentDevices))
        PassPercent = round((NumberofPresentDevices * 100) / float(len(listOfIPs)),2)
        logging.info("Pass Percent: %s", str(PassPercent))
        logging.info("Fail Percent: %s", str(100-PassPercent))
        ScheduleStatus["NoOfDeviceInventory" + str(NumberOfTime-1)] = str(NumberofPresentDevices)
        ScheduleStatus["Passed%InventoryStatus"+ str(NumberOfTime-1)]= str(PassPercent)
        ScheduleStatus["NoOfDeviceInventory" + str(NumberOfTime-1)] = str(NumberofPresentDevices)
        ScheduleStatus["Passed%InventoryStatus" + str(NumberOfTime-1)] = str(PassPercent)
        ScheduleStatus["NoOfDeviceInventory" + str(NumberOfTime-1)] = str(NumberofPresentDevices)
        ScheduleStatus["Passed%InventoryStatus" + str(NumberOfTime-1)] = str(PassPercent)
        if MissingList:
            logging.info("MissingList Devices: %s", str(MissingList))
        return PassPercent
    except Exception as e:
        print e

NCE_IP = "172.16.2.112"
NCE_W1 = "172.16.2.113"
NCE_W2 = "172.16.2.114"
DC_IP = "172.16.2.116"

NCE_IPOutput = "172.16.2.112INDOutput.txt"
NCE_W1Output = "172.16.2.113INDOutput.txt"
NCE_W2Output = "172.16.2.114INDOutput.txt"
DC_IPOutput = "172.16.2.116INDOutput.txt"

SiteName= "IND"
outputLogFile="discoveryIND.log"
logging.basicConfig(filename=outputLogFile, level=logging.INFO, format='')
outputFileName="DiscoveryIND.xlsx"

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

fieldNamesCSV={'DeviceCount':1,'InventoryStatus 2 min':2,'InventoryStatus 4 min':3,
               'InventoryStatus 6 min':4,'InventoryStatus 8 min':5,'InventoryStatus 10 min':6,'InventoryStatus 12 min':7,
               'InventoryStatus 14 min':8,'InventoryStatus 16 min':9,'InventoryStatus 18 min':10,'InventoryStatus 20 min':11,
               'InventoryStatus 22 min':12, 'InventoryStatus 24 min':13, 'InventoryStatus 26 min':14, 'InventoryStatus 28 min':15,
               'InventoryStatus 30 min':16, 'InventoryStatus 32 min':17,'InventoryStatus 34 min':18,'InventoryStatus 36 min':19,
               'InventoryStatus 38 min':20,'InventoryStatus 40 min':21, 'InventoryStatus 42 min':22,
               'InventoryStatus 44 min':23, 'InventoryStatus 46 min':24, 'InventoryStatus 48 min':25, 'InventoryStatus 50 min':26,
               'InventoryStatus 52 min':27, 'InventoryStatus 54 min':28, 'InventoryStatus 56 min':29, 'InventoryStatus 58 min':30,
               'InventoryStatus 60 min':31}

#Generation of Ordered list containing numberof devices and start/end IP
numberofdeviceList=[100,200,300,400,500,750,1000,1200,1500,2000,2500,3000]
discoveryList=collections.OrderedDict()
newStartIP="10.50.101.1"
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

    NumberOfTime=1
    totalTime=0
    passpercentList = []
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

        while True:
            # Dump top output and take cppu,load,ram,swap
            dumpOutput(NCE_IP, NCE_IPOutput)
            dumpOutput(NCE_W1, NCE_W1Output)
            dumpOutput(NCE_W2, NCE_W2Output)
            dumpOutput(DC_IP, DC_IPOutput)
            time.sleep(120)
            totalTime=totalTime+120
            PassPercent = devicePresenceInInventory(Token, Org, Site, listOfIPs, NumberOfTime)
            ScheduleStatus["InventoryStatus %s min"%str(NumberOfTime * 2)] = str(PassPercent)
            passpercentList.append(PassPercent)
            NumberOfTime = NumberOfTime + 1
            if PassPercent >= 100:
                break;
            if len(passpercentList) >=3 and (passpercentList[-1]==passpercentList[-2]==passpercentList[-3]!=0):
                break
            if NumberOfTime==31:
                break

        outputSaveInLogFile("NCE", NCETopOutput)
        outputSaveInLogFile("NCEW1", NCE1TopOutput)
        outputSaveInLogFile("NCEW2",NCE2TopOutput)
        outputSaveInLogFile("DC", DCTopOutput)
        logging.info("Data is ---------")
        logging.info("Data is : %s",ScheduleStatus)

        num=0
        discoveryCompletionStatus=""
        while True:
            try:
                value,requestId,inprogressPercent = RequiredAPI.get_all_scheduledDiscoveryRequest(NCE_IP,Token,Org,Site,"NETWORK_DISCOVERY")
                #if request not present breal the loop
                if value == 0 :
                    discoveryCompletionStatus="Completed"
                    requestPayload=None
                    break;
                #if inprogress percent remain 99 for next 10 min then break
                time.sleep(120)
                totalTime = totalTime + 120
                if inprogressPercent >= 98.50:
                    if num==5:
                        discoveryCompletionStatus = "Inprogess-98.50Above"
                        requestPayload = None
                        try:
                            res= RequiredAPI.deleteRequest(NCE_IP,Token,Org,Site,requestId)
                        except Exception as e:
                            print "Exception is :" + str(e)
                        break;
                    else:
                        num = num + 1
                if value == 1 and (totalTime)/60 > 80 :
                    discoveryCompletionStatus = "ForceDeleteAfter80min"
                    try:
                        res= RequiredAPI.deleteRequest(NCE_IP,Token,Org,Site,requestId)
                    except Exception as e:
                        print "Exception is :" + str(e)
                    break;
            except Exception as e:
                logging.info("Excpetion :%s",str(e))

        logging.info("Completion Time :%s", str(totalTime/60))
        logging.info("Completion Status :%s", discoveryCompletionStatus)
        ScheduleStatus["DiscoveryCompletionTime"] = str(totalTime/60)
        #UserfulFunction.CreateandStoreOutputCSVFile(outputFileName,fieldNamesCSV,ScheduleStatus)
        UserfulFunction.StoreOutputInExcelColumnwise(outputFileName,fieldnames,ScheduleStatus,"Sheet1")
        UserfulFunction.StoreOutputInExcelColumnwise(outputFileName, fieldNamesCSV, ScheduleStatus,"Sheet2")
    except Exception as e:
        logging.info("Exception : %s",str(e))
