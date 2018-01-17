from Library import RequiredAPI;
import MySQLdb
import logging
logging.basicConfig(filename='MissingCycleIND.log',level=logging.INFO,format='')

NCE_IP="172.16.2.112"
siteName="IND"
tableName='meridian_data_IND'
Database_IP="172.16.2.49"

def createTable():
    db = MySQLdb.connect(Database_IP, "root", "FixStream", "Test")
    cursor = db.cursor()
    createQuery = "create table " + tableName + " (deviceID varchar(50),metricName varchar(50),instanceType varchar(30),instanceName varchar(50),metricValue float,date_Time Timestamp);"
    cursor.execute(createQuery)
    logging.info(tableName + " is created")
    db.close()

def dropTable():
    db = MySQLdb.connect(Database_IP, "root", "FixStream", "Test")
    cursor = db.cursor()
    Query = "drop table " + tableName+";"
    cursor.execute(Query)
    logging.info(tableName + " is dropped")
    db.close()

def checkTableExistanceAndCreate():
    # Open database connection
    db = MySQLdb.connect(Database_IP, "root", "FixStream", "Test")
    cursor = db.cursor()
    query = "show table status like '"+tableName +"';"
    cursor.execute(query)
    result = cursor.fetchone()
    db.close()
    if result == None:
        createTable()
    else:
        dropTable()
        createTable()

def insertBulkData(data):
    # Open database connection
    db = MySQLdb.connect(Database_IP, "root", "FixStream", "Test")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    query = "insert into meridian_data (deviceID,metricName,instanceType,instanceName,metricValue,date_Time) values (%s, %s, %s, %s,%s, %s)"
    cursor.executemany(query, data)
    db.commit()
    db.close()

def findMissingCycleDevices():
    logging.info("Result ::::::::::::::::::::::::::::::::::::")
    logging.info("Number of Expected Cycle per device: " + str(expectedCyclePerDevice))
    db = MySQLdb.connect(Database_IP, "root", "FixStream", "Test")
    cursor = db.cursor()
    query = "select deviceID,metricName,instanceType,count(*) from meridian_data where date_time between '%s' and '%s' group by deviceID,metricName,instanceType having count(*) != %d" % (
    startDate, endDate, expectedCyclePerDevice)

    cursor.execute(query)
    data = cursor.fetchall()
    logging.info("Number of Devices with Missed Cycle : %s",cursor.rowcount / 2)
    sum = 0;
    logging.info("Devices with missed cycle")
    for r in data:
        cycleCount = r[3]
        sum = sum + (expectedCyclePerDevice - cycleCount)
        logging.info(r[0] + "  " + r[1] + "  " + str(r[3]))
    db.close()
    sum = sum / 2
    logging.info("Number of missed Cycle : %s", sum)
    logging.info("Failed Percent:%s ", (float)(sum * 100) / totalCycleCount)

def generateReport(requestId1,numberOfDevices1,NumberofCyclePerDevice,startDate1,endDate1):
    global requestId, numberOfDevices,startDate, endDate, expectedCyclePerDevice, totalCycleCount
    requestId = requestId1
    numberOfDevices = numberOfDevices1
    startDate = startDate1
    endDate = endDate1
    expectedCyclePerDevice = NumberofCyclePerDevice
    totalCycleCount = numberOfDevices * expectedCyclePerDevice
    Token= RequiredAPI.getToken(NCE_IP)
    Org,Site=RequiredAPI.getOrgAndSite(NCE_IP,Token,siteName)
    checkTableExistanceAndCreate()
    deviceList= RequiredAPI.getscheduledDevicesForPerformance(NCE_IP,Token,Org, Site, requestId)

    DatatoDump=[]
    count=0;
    deviceList1=[x for x in deviceList if x is not None]

    for device in deviceList1:
        outputListCpu= RequiredAPI.getPerformancedatafordevice(NCE_IP, Token, Org, Site, device,"cpuMetrics","default","default")
        outputListMem = RequiredAPI.getPerformancedatafordevice(NCE_IP, Token, Org, Site, device, "memMetrics", "RAM",
                                                              "default")
        if outputListCpu:
            DatatoDump.extend(outputListCpu)
        if outputListMem:
            DatatoDump.extend(outputListMem)

        count = count + 1
        if count%15 == 0:
            insertBulkData(DatatoDump)
            DatatoDump=[];
        if count == numberOfDevices:
            insertBulkData(DatatoDump)
            break;

    findMissingCycleDevices()


