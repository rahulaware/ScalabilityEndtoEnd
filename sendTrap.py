import os
def sendtrap(status, ip,dc_ip):
        if status == "up":
                os.system("snmptrap -v 2c -c public %s '' .1.3.6.1.6.3.1.1.5.4 ifIndex i 2 ifAdminStatus i 1 ifOperStatus i 1 1.3.6.1.4.1.11307.10.10 a %s"%(dc_ip,ip))
        if status == "down":
                os.system("snmptrap -v 2c -c public %s '' .1.3.6.1.6.3.1.1.5.3 ifIndex i 2 ifAdminStatus i 1 ifOperStatus i 2 1.3.6.1.4.1.11307.10.10 a %s"%(dc_ip,ip))

def generateTrapOnDevices(listOfIPs,dc_ip):
        for device in listOfIPs:
            ip_Address=device["ip"]
            sendtrap("down", ip_Address,dc_ip)
            sendtrap("up", ip_Address,dc_ip)


