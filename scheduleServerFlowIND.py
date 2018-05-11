from Library import RequiredAPI;
from datetime import datetime,timedelta
import logging

NCE_IP="172.16.2.112"
siteName="IND"
DC_IP = "172.16.2.116"
datefmt = "%Y-%m-%d"
timefmt = "%I:%M:%p"
timefmt1= "%H:%M"
Duration=1440

inputs=[[1500,10]]

outputLogFile='serverFlowIND.log'
logging.basicConfig(filename=outputLogFile, level=logging.INFO, format='')
logging.getLogger("paramiko").setLevel(logging.ERROR)

for input in inputs:
    try:
        NumberOfDevices = input[0]
        server_Flow_Interval = input[1]
        logging.info("------------------------------------------------------------------------------------------------------------------------------------------")
        Token= RequiredAPI.getToken(NCE_IP)
        Org,Site=RequiredAPI.getOrgAndSite(NCE_IP,Token,siteName)

        #Performance Duration
        now_utc = datetime.utcnow()+timedelta(minutes=3)
        end_now_utc = datetime.utcnow()+timedelta(minutes=(3+Duration))
        schedule_start_date = now_utc.strftime(datefmt)
        schedule_end_date = end_now_utc.strftime(datefmt)
        schedule_start_time = now_utc.strftime(timefmt)
        schedule_end_time =end_now_utc.strftime(timefmt)
        schedule_start_time1 = now_utc.strftime(timefmt1)
        schedule_end_time1 = end_now_utc.strftime(timefmt1)

        #get all devices for server flow
        response_serverFlow = RequiredAPI.get_all_discovered_and_unscheduled_compute_devices(NCE_IP, Token, Org, Site,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time,"PCAP_COLLECTION")

        listOfDevices = [];
        listOfDevices = RequiredAPI.selectDevices(response_serverFlow, NumberOfDevices)

        #schedule devices for flow
        requestId_serverFlow = RequiredAPI.scheduleServerFlow(listOfDevices, server_Flow_Interval, NumberOfDevices, NCE_IP, Token, Org, Site,
                                                   schedule_start_date, schedule_start_time, schedule_end_date,
                                                   schedule_end_time)

        logging.info("Server flow Schedule with %s requestId %s Devices and %s min interval -----", requestId_serverFlow,NumberOfDevices, server_Flow_Interval)

    except Exception as e:
        logging.info("scheduleServerPerformance Exception is :" + str(e))
