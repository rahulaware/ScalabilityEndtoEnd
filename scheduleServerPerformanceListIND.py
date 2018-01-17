from Library import RequiredAPI;
from datetime import datetime,timedelta
import CycleCollectionCountForDevicesESIND,ResponseCycleCountForDevicesDCIND
import logging

NCE_IP="172.16.2.112"
siteName="IND"
datefmt = "%Y-%m-%d"
timefmt = "%I:%M:%p"
timefmt1= "%H:%M"
Duration=30

inputs=[[200,3],[500,3],[1000,3],[1200,3],[1500,3],[200,5],[500,5],[1000,5],[1200,5],[1500,5],[200,10],[500,10],[1000,10],[1200,10],[1500,10]]

for input in inputs:
    NumberOfDevices = input[0]
    TimeInterval = input[1]
    NumberofCyclePerDevice= (Duration / int(TimeInterval))+1
    logging.info("------------------------------------------------------------------------------------------------------------------------------------------")
    Token= RequiredAPI.getToken(NCE_IP)

    Org,Site=RequiredAPI.getOrgAndSite(NCE_IP,Token,siteName)

    now_utc = datetime.utcnow()+timedelta(minutes=3)
    end_now_utc = datetime.utcnow()+timedelta(minutes=(3+Duration))
    schedule_start_date = now_utc.strftime(datefmt)
    schedule_end_date = end_now_utc.strftime(datefmt)
    schedule_start_time = now_utc.strftime(timefmt)
    schedule_end_time =end_now_utc.strftime(timefmt)

    schedule_start_time1 = now_utc.strftime(timefmt1)
    schedule_end_time1 = end_now_utc.strftime(timefmt1)

    # Date to send
    ESnewDate = schedule_start_date + " " + schedule_start_time1+":00"
    ESendDate = schedule_end_date + " " + schedule_end_time1+":59"

       #get all devices
    response= RequiredAPI.get_all_discovered_and_unscheduled_compute_devices(NCE_IP,Token,Org,Site,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time)

    #schedule devices for performance
    requestId=RequiredAPI.schedulePerformance(response,TimeInterval,NumberOfDevices,NCE_IP,Token,Org, Site,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time)
    logging.info("Server Performance Schedule with %s requestId %s Devices and %s min interval -----",requestId,NumberOfDevices,TimeInterval)
    import time
    logging.info("Data collection inprogress........Start Date: "+ESnewDate+" End Date: "+ESendDate)
    time.sleep((Duration*60)+600)

    # # import subprocess
    # # #python CycleCollectionCountForDevicesESIND.py requestId,numberofDevices,interval,ESnewDate,EndDate
    # # output = subprocess.call(["python", "CycleCollectionCountForDevicesESIND.py", str(requestId), str(NumberOfDevices),str(TimeInterval),ESnewDate,ESendDate])
    logging.info("DC Report Generation is inprogress........")
    ResponseCycleCountForDevicesDCIND.findMissedCycleInDC(requestId,int(NumberOfDevices), NumberofCyclePerDevice)

    logging.info("NCE Report Generation is inprogress........")
    CycleCollectionCountForDevicesESIND.generateReport(requestId,NumberOfDevices,NumberofCyclePerDevice,ESnewDate,ESendDate)

    time.sleep(60)

    res = RequiredAPI.deleteRequest(NCE_IP, Token, Org, Site, requestId)
    logging.info("Server Performance Scheduled request %s deleted with %s Devices and %s min interval",requestId,NumberOfDevices, TimeInterval)

