import logging

logging.basicConfig(filename='MissingCycle.log',level=logging.INFO,format='')
logging.getLogger("paramiko").setLevel(logging.ERROR)

def connectToDC():
    try:
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(DC_IP, port, username, password)
        return ssh;
    except Exception as e:
        logging.info("Exception is :",e)
        return False;

def checkReuqestCreatedorNot():
    try:
        import MySQLdb
        db = MySQLdb.connect(DC_IP, "netra", "fixstream", "netra_dc")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # check request id creted in DC
        cursor.execute("select ip_address from dc_job where request_id ='%s'" % request_id)
        data = cursor.fetchall()
        db.close()
        return data
    except Exception as e:
        logging.info("Exception is :", e)
        return False;

def findMissedCycleInDC(request_id1,NumberofDevices,expectedCycleperDevice):
    #Input RequestID and expected Cycle per Device
    global DC_IP,port,username,password,request_id
    DC_IP="172.16.2.115"
    port = 22
    username = 'root'
    password = 'FixStream'
    request_id=request_id1
    TotalCycle=NumberofDevices*expectedCycleperDevice
    ssh =  connectToDC()
    if ssh != False:
        data= checkReuqestCreatedorNot()
        if data:
            logging.info("Result ::::::::::::::::::::::::::::::::::::")
            logging.info("Expected Cycle per device:"+str(expectedCycleperDevice))
            NumberofDevicewithMissedCycle = 0
            NumberofMissedCycle = 0
            logging.info("Devices with Missed Cycle:")
            for ip in data:
                stdin = stdout = stderr = None
                NumberofCycle = 0
                stdin, stdout, stderr = ssh.exec_command(
                    "grep %s /opt/meridian/dc/var/fsdc/logs/_dc_response.json | grep '\"%s\"'" % (request_id, ip[0]))
                NumberofCycle = len(stdout.readlines())
                if NumberofCycle != expectedCycleperDevice:
                    NumberofDevicewithMissedCycle = NumberofDevicewithMissedCycle + 1
                    logging.info(ip[0] + "*********" + str(NumberofCycle))
                    NumberofMissedCycle = NumberofMissedCycle + (expectedCycleperDevice-NumberofCycle)

            logging.info("Number of Devices with Missed Cycle : "+str(NumberofDevicewithMissedCycle))
            logging.info("Number of missed Cycle : "+str(NumberofMissedCycle))
            logging.info("Failed Percent: "+str((float)(NumberofMissedCycle * 100) / TotalCycle))
            ssh.close()
        else:
            logging.info("Request Id not exist:"+request_id)
    else:
        logging.info("Failed")

#findMissedCycleInDC("3c7f7212-420f-4246-8022-39670b280bf5",100,7)