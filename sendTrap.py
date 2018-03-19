import os
def sendtrap(ip,dc_ip):
        os.system("snmptrap -v 2c -c public %s '' .1.3.6.1.6.3.1.1.5.1 ifIndex i 2 ifAdminStatus i 1 ifOperStatus i 2 1.3.6.1.4.1.11307.10.10 a %s"%(dc_ip,ip))
        os.system("snmptrap -v 2c -c public %s '' .1.3.6.1.6.3.1.1.5.2 ifIndex i 2 ifAdminStatus i 1 ifOperStatus i 2 1.3.6.1.4.1.11307.10.10 a %s"%(dc_ip, ip))
        os.system("snmptrap -v 2c -c public %s '' .1.3.6.1.6.3.1.1.5.5 ifIndex i 2 ifAdminStatus i 1 ifOperStatus i 2 1.3.6.1.4.1.11307.10.10 a %s"%(dc_ip, ip))
        os.system("snmptrap -v 2c -c public %s '' .1.3.6.1.6.3.1.1.5.3 ifIndex i 2 ifAdminStatus i 1 ifOperStatus i 2 1.3.6.1.4.1.11307.10.10 a %s"%(dc_ip, ip))
        #os.system("snmptrap -v 2c -c public %s '' .1.3.6.1.6.3.1.1.5.4 ifIndex i 2 ifAdminStatus i 1 ifOperStatus i 2 1.3.6.1.4.1.11307.10.10 a %s"%(dc_ip, ip))


def generateTrapOnDevices(listOfIPs, dc_ip):
    for device in listOfIPs:
        sendtrap(device["ip"], dc_ip)



