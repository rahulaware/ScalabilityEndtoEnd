from Library import RequiredAPI;
import time,logging,sys,csv,os
from Library import UserfulFunction;

#This function is called only once when schedule start
def startDump(deviceIP,fileName):
    try:
        with open(fileName,"a") as fh:
            fh.write("*************************Schedule Discovery with %s*******************\n"%str(deviceIP))
    except Exception as e:
        print "Exception is :"+str(e)

#This funtion dumps parsed command ouput of top command
def dumpOutput(IP,fileName):
    try:
        global NCE_IP,NCE_W1,NCE_W2,DC_IP
        with open(fileName, "a") as fh:
            top_output = UserfulFunction.topCommandOutput(IP,"root","FixStream")
            topParamter =UserfulFunction.parsedCPURAMLOADSWAPFromTopOutput(top_output)
            logging.info("-----------%s-------------", IP)
            logging.info("CPU : %s", topParamter["CpuUsed"])
            logging.info("RAM (MB): %s", topParamter["RamUsed"]/1024/1024)
            logging.info("SwapUsed (MB): %s", topParamter["SwapUsed"]/1024)
            logging.info("LOAD : %s", topParamter["LoadAverage"])
            fh.write(top_output)
            fh.write("----------------------------------------------------------------------------\n")
        data={'CPU': topParamter["CpuUsed"], 'RAM GB': round(topParamter["RamUsed"]/1024/1024,2),'LOAD':topParamter["LoadAverage"],'SWAP MB':topParamter["SwapUsed"]/1024}
        return data
    except Exception as e:
        print "Exception is :" + str(e)


def DumptoCSV(row):
    iscreated = False
    if os.path.isfile(csvfileName):
        iscreated = True
    with open(csvfileName, 'a') as csvfile:
        fieldnames=['Time','deviceIP','CPU MAX', 'CPU MIN', 'CPU AVG','RAM MAX GB', 'RAM MIN GB', 'RAM AVG GB','LOAD MAX', 'LOAD MIN', 'LOAD AVG','SWAP MAX MB', 'SWAP MIN MB', 'SWAP AVG MB' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if iscreated == False:
            writer.writeheader()
        writer.writerow(row)

NCE_IP = "172.16.2.112"
NCE_W1 = "172.16.2.113"
NCE_W2 = "172.16.2.114"
DC_IP = "172.16.2.115"

NCE_IPOutput = "172.16.2.112Output.txt"
NCE_W1Output = "172.16.2.113Output.txt"
NCE_W2Output = "172.16.2.114Output.txt"
DC_IPOutput = "172.16.2.115Output.txt"

SiteName= "US"
outputLogFile="discovery.log"
csvfileName = "finalOutput.csv"
logging.basicConfig(filename=outputLogFile, level=logging.INFO, format='')

Token = RequiredAPI.getToken(NCE_IP)
# print "token created"

Org, Site = RequiredAPI.getOrgAndSite(NCE_IP, Token, SiteName)
# print "ORG and Site ID selected"

deviceIP=sys.argv[1]
deviceCount=1
#Dump top command output
startDump(deviceIP, NCE_IPOutput)
startDump(deviceIP, NCE_W1Output)
startDump(deviceIP, NCE_W2Output)
startDump(deviceIP, DC_IPOutput)


logging.info("*************************Schedule Discovery with %s Result*******************", str(deviceIP))
try:
    rowCSV={}
    rowCSV["Vcenter"]=deviceIP
    DumptoCSV(rowCSV)

    numberofSecond=0;
    num=0
    while True:
        try:
            #Dump top output and take cppu,load,ram,swap
            row={}
            rowCSV={}
            row["NCE"]= dumpOutput(NCE_IP, NCE_IPOutput)
            row["NCE1"]= dumpOutput(NCE_W1, NCE_W1Output)
            row["NCE2"]= dumpOutput(NCE_W2, NCE_W2Output)
            row["DC"] = dumpOutput(DC_IP, DC_IPOutput)
            rowCSV= {'NCE CPU': row["NCE"]["CPU"], 'NCE RAM GB': row["NCE"]["RAM GB"], \
                    'NCE LOAD': row["NCE"]["LOAD"], 'NCE SWAP MB': row["NCE"]["SWAP MB"], \
                    'NCE1 CPU': row["NCE1"]["CPU"], 'NCE1 RAM GB': row["NCE1"]["RAM GB"], \
                    'NCE1 LOAD': row["NCE1"]["LOAD"], 'NCE1 SWAP MB': row["NCE1"]["SWAP MB"], \
                    'NCE2 CPU': row["NCE2"]["CPU"], 'NCE2 RAM GB': row["NCE2"]["RAM GB"], \
                    'NCE2 LOAD': row["NCE2"]["LOAD"], 'NCE2 SWAP MB': row["NCE2"]["SWAP MB"], \
                    'DC CPU': row["DC"]["CPU"], 'DC RAM GB': row["DC"]["RAM GB"], \
                    'DC LOAD': row["DC"]["LOAD"], 'DC SWAP MB': row["DC"]["SWAP MB"]}
            DumptoCSV(rowCSV)

            value,requestId,inprogressPercent = RequiredAPI.get_all_scheduledDiscoveryRequest(NCE_IP,Token,Org,Site,"NETWORK_DISCOVERY")
            #if request not present break the loop
            if value == 0 :
                requestPayload=None
                break;
            #if inprogress percent remain 99 for next 10 min then break
            time.sleep(120)
            numberofSecond = numberofSecond + 120
            if inprogressPercent >= 99:
                if num==5:
                    requestPayload = None
                    try:
                        res= RequiredAPI.deleteRequest(NCE_IP,Token,Org,Site,requestId)
                    except Exception as e:
                        print "Exception is :" + str(e)
                    break;
                else:
                    num = num + 1
            if value == 1 and (numberofSecond/60) > 80 :
                try:
                    res= RequiredAPI.deleteRequest(NCE_IP,Token,Org,Site,requestId)
                except Exception as e:
                    print "Exception is :" + str(e)
                break;
        except Exception as e:
            logging.info("Excpetion :%s",str(e))
    CompletionTime = numberofSecond / 60
    logging.info("Completion Time (min):%s", str(CompletionTime))
    rowCSV={}
    rowCSV["CompletionTime"]=CompletionTime
    DumptoCSV(rowCSV)
except Exception as e:
    logging.info("Exception : %s",str(e))
