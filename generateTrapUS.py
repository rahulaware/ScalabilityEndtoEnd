from datetime import datetime,timedelta
from Library import RequiredAPI
import sendTrap
import time,sys

NCE_IP="172.16.2.112"
siteName="US"
DC_IP = "172.16.2.115"
datefmt = "%Y-%m-%d"
timefmt = "%I:%M:%p"
timefmt1= "%H:%M"

inputs=[[1500,5]]
totalDurationmin=1440
snmpCommunity="public"
snmpVersion="v2c"

for input in inputs:
    try:
        NumberOfDevices = input[0]
        intervalmin = input[1]

        Token= RequiredAPI.getToken(NCE_IP)
        Org,Site=RequiredAPI.getOrgAndSite(NCE_IP,Token,siteName)

        createTime = str(long(time.time() * 1000))
        updateTime = createTime

        print RequiredAPI.acivateEventCenterConfigurationStatus(NCE_IP, Token, Org, Site, createTime, updateTime,
                                                                snmpCommunity, snmpVersion)
        #Performance Duration
        now_utc = datetime.utcnow()+timedelta(minutes=3)
        end_now_utc = datetime.utcnow()+timedelta(minutes=(3+totalDurationmin))
        schedule_start_date = now_utc.strftime(datefmt)
        schedule_end_date = end_now_utc.strftime(datefmt)
        schedule_start_time = now_utc.strftime(timefmt)
        schedule_end_time =end_now_utc.strftime(timefmt)
        schedule_start_time1 = now_utc.strftime(timefmt1)
        schedule_end_time1 = end_now_utc.strftime(timefmt1)
        #Date to send
        ESnewDate = schedule_start_date + " " + schedule_start_time1+":00"
        ESendDate = schedule_end_date + " " + schedule_end_time1+":59"

        # get all devices for server flow
        response_serverFlow = RequiredAPI.get_all_discovered_and_unscheduled_compute_devices(NCE_IP, Token, Org, Site,
                                                                                             schedule_start_date,
                                                                                             schedule_start_time,
                                                                                             schedule_end_date,
                                                                                             schedule_end_time,
                                                                                             "PCAP_COLLECTION")


        listOfDevices=[];
        totalTime=0
        listOfDevices= RequiredAPI.selectDevices(response_serverFlow,NumberOfDevices)
        while True:
            sendTrap.generateTrapOnDevices(listOfDevices,DC_IP)
            time.sleep(intervalmin*60)
            totalTime=totalTime+intervalmin
            if totalTime > totalDurationmin:
                break;

    except Exception as e:
        print "Trap generation Script",str(e)

