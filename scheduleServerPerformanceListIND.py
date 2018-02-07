from Library import RequiredAPI;
from datetime import datetime,timedelta
import CycleCollectionCountForDevicesES,ResponseCycleCountForDevicesDC
import logging
import time
from openpyxl import load_workbook
from openpyxl.styles import Font,colors

NCE_IP="172.16.2.112"
siteName="IND"
DC_IP = "172.16.2.116"
port = 22
username = 'root'
password = 'FixStream'
Database_IP="172.16.2.49"
databaseName="Scalability"
tableName='meridian_data_IND'
DBusername="root"
DBpassword="FixStream"
datefmt = "%Y-%m-%d"
timefmt = "%I:%M:%p"
timefmt1= "%H:%M"
ft = Font(color=colors.RED)
Duration=30

inputs=[[200,2],[200,3],[200,5],[200,7],[200,10],[200,15],[500,2],[500,3],[500,5],[500,7],[500,10],[500,15]]
#inputs=[[750,2],[750,3],[750,5],[750,7],[750,10],[750,15],[1000,2],[1000,3],[1000,5],[1000,7],[1000,10],[1000,15],[1500,2],[1500,3],[1500,5],[1500,7],[1500,10],[1500,15]]
#inputs=[[100,2],[100,3],[100,5],[100,7],[100,10],[100,15],[300,2],[300,3],[300,5],[300,7],[300,10],[300,15],[400,2],[400,3],[400,5],[400,7],[400,10],[400,15],[1200,2],[1200,3],[1200,5],[1200,7],[1200,10],[1200,15]]
#inputs=[[100,1],[200,1],[300,1],[400,1],[500,1],[750,1],[1000,1],[1200,1],[1500,1]]


outputLogFile='MissingCycleIND.log'
outputFile="OutputExcel.xlsx"
logging.basicConfig(filename=outputLogFile, level=logging.INFO, format='')
logging.getLogger("paramiko").setLevel(logging.ERROR)

DCoutputExcel={"100_1":"B5","200_1":"D5","300_1":"F5","400_1":"H5","500_1":"J5","750_1":"L5","1000_1":"N5",\
               "1200_1":"P5","1500_1":"R5","2000_1":"T5","2500_1":"V5","3000_1":"X5", \
               "100_2": "B6", "200_2": "D6", "300_2": "F6", "400_2": "H6", "500_2": "J6", "750_2": "L6", "1000_2": "N6", \
               "1200_2": "P6", "1500_2": "R6", "2000_2": "T6", "2500_2": "V6", "3000_2": "X6", \
               "100_3": "B7", "200_3": "D7", "300_3": "F7", "400_3": "H7", "500_3": "J7", "750_3": "L7", "1000_3": "N7", \
               "1200_3": "P7", "1500_3": "R7", "2000_3": "T7", "2500_3": "V7", "3000_3": "X7", \
               "100_5":"B8","200_5":"D8","300_5":"F8","400_5":"H8","500_5":"J8","750_5":"L8","1000_5":"N8",\
               "1200_5":"P8","1500_5":"R8","2000_5":"T8","2500_5":"V8","3000_5":"X8", \
               "100_7": "B9", "200_7": "D9", "300_7": "F9", "400_7": "H9", "500_7": "J9", "750_7": "L9", "1000_7": "N9", \
               "1200_7": "P9", "1500_7": "R9", "2000_7": "T9", "2500_7": "V9", "3000_7": "X9", \
               "100_10": "B10", "200_10": "D10", "300_10": "F10", "400_10": "H10", "500_10": "J10", "750_10": "L10",\
               "1000_10": "N10","1200_10": "P10", "1500_10": "R10", "2000_10": "T10", "2500_10": "V10", "3000_10": "X10", \
               "100_15":"B11","200_15":"D11","300_15":"F11","400_15":"H11","500_15":"J11","750_15":"L11","1000_15":"N11",\
               "1200_15":"P11","1500_15":"R11","2000_15":"T11","2500_15":"V11","3000_15":"X11", \
               }
NCEoutputExcel={"100_1":"C5","200_1":"E5","300_1":"G5","400_1":"I5","500_1":"K5","750_1":"M5","1000_1":"O5",\
               "1200_1":"Q5","1500_1":"S5","2000_1":"U5","2500_1":"W5","3000_1":"Y5", \
               "100_2": "C6", "200_2": "E6", "300_2": "G6", "400_2": "I6", "500_2": "K6", "750_2": "M6", "1000_2": "O6", \
               "1200_2": "Q6", "1500_2": "S6", "2000_2": "U6", "2500_2": "W6", "3000_2": "Y6", \
               "100_3": "C7", "200_3": "E7", "300_3": "G7", "400_3": "I7", "500_3": "K7", "750_3": "M7", "1000_3": "O7", \
               "1200_3": "Q7", "1500_3": "S7", "2000_3": "U7", "2500_3": "W7", "3000_3": "Y7", \
               "100_5":"C8","200_5":"E8","300_5":"G8","400_5":"I8","500_5":"K8","750_5":"M8","1000_5":"O8",\
               "1200_5":"Q8","1500_5":"S8","2000_5":"U8","2500_5":"W8","3000_5":"Y8", \
               "100_7": "C9", "200_7": "E9", "300_7": "G9", "400_7": "I9", "500_7": "K9", "750_7": "M9", "1000_7": "O9", \
               "1200_7": "Q9", "1500_7": "S9", "2000_7": "U9", "2500_7": "W9", "3000_7": "Y9", \
               "100_10": "C10", "200_10": "E10", "300_10": "G10", "400_10": "I10", "500_10": "K10", "750_10": "M10",\
               "1000_10": "O10","1200_10": "Q10", "1500_10": "S10", "2000_10": "U10", "2500_10": "W10", "3000_10": "Y10", \
               "100_15":"C11","200_15":"E11","300_15":"G11","400_15":"I11","500_15":"K11","750_15":"M11","1000_15":"O11",\
               "1200_15":"Q11","1500_15":"S11","2000_15":"U11","2500_15":"W11","3000_15":"Y11", \
               }

for input in inputs:
    try:
        NumberOfDevices = input[0]
        TimeInterval = input[1]
        NumberofCyclePerDevice= (Duration / int(TimeInterval))+1
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
        #Date to send
        ESnewDate = schedule_start_date + " " + schedule_start_time1+":00"
        ESendDate = schedule_end_date + " " + schedule_end_time1+":59"

        #get all devices
        response= RequiredAPI.get_all_discovered_and_unscheduled_compute_devices(NCE_IP,Token,Org,Site,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time)

        #schedule devices for performance
        requestId=RequiredAPI.schedulePerformance(response,TimeInterval,NumberOfDevices,NCE_IP,Token,Org, Site,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time)
        logging.info("Server Performance Schedule with %s requestId %s Devices and %s min interval -----",requestId,NumberOfDevices,TimeInterval)
        logging.info("Data collection inprogress........Start Date: "+ESnewDate+" End Date: "+ESendDate)
        time.sleep((Duration*60)+600)

        # # import subprocess
        # # #python CycleCollectionCountForDevicesES.py requestId,numberofDevices,interval,ESnewDate,EndDate
        # # output = subprocess.call(["python", "CycleCollectionCountForDevicesES.py", str(requestId), str(NumberOfDevices),str(TimeInterval),ESnewDate,ESendDate])
        DCOutput=DCNCEOutput=0

        logging.info("DC Report Generation is inprogress........")
        DCOutput = ResponseCycleCountForDevicesDC.findMissedCycleInDC(requestId,int(NumberOfDevices),NumberofCyclePerDevice,DC_IP,port,username,password)

        logging.info("NCE Report Generation is inprogress........")
        DCNCEOutput = CycleCollectionCountForDevicesES.generateReport(requestId,NumberOfDevices,NumberofCyclePerDevice,ESnewDate,ESendDate,NCE_IP,siteName,Database_IP,databaseName,tableName,DBusername,DBpassword)
        NCEFailure= DCNCEOutput-DCOutput
        logging.info("NCE Failed Percent:%s ", NCEFailure)
        key = str(NumberOfDevices) + "_" + str(TimeInterval)
        if key in DCoutputExcel and key in NCEoutputExcel:
            try:
                Excel = load_workbook(filename=outputFile)
                SiteSheet = Excel['INDSite']
                SiteSheet[DCoutputExcel[key]] = round(DCOutput,2)
                SiteSheet[NCEoutputExcel[key]] = round(NCEFailure,2)
                if DCOutput >= 1:
                    SiteSheet[DCoutputExcel[key]].font=ft
                if NCEFailure >= 1:
                    SiteSheet[NCEoutputExcel[key]].font=ft
                Excel.save(outputFile)
            except Exception as e:
                logging.info("scheduleServerPerformance Exception is :" + str(e))
        else:
            logging.info(key+" key is not present in DC/NCE output Excel")

        time.sleep(60)
        res = RequiredAPI.deleteRequest(NCE_IP, Token, Org, Site, requestId)
        logging.info("Server Performance Scheduled request %s deleted with %s Devices and %s min interval",requestId,NumberOfDevices, TimeInterval)
    except Exception as e:
        logging.info("scheduleServerPerformance Exception is :" + str(e))
