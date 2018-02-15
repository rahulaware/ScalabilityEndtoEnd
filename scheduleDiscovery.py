from Library import RequiredAPI;
import json,time
import sys;
Arg = len(sys.argv);
NCE_IP=""
Site=""
if Arg == 3:
    NCE_IP=sys.argv[1]
    if sys.argv[2] == "US":
        Site= "US"
        inputs = [{"typeOfDevice": 'linux', "mask": ["10.50.1.1", "10.50.2.1"]},
                  {"typeOfDevice": 'linux', "mask": ["10.50.3.1", "10.50.4.1"]},
                  {"typeOfDevice": 'window', "mask": ["10.50.31.1", "10.50.32.1"]},
                  {"typeOfDevice": 'window', "mask": ["10.50.33.1", "10.50.34.1"]},
                  {"typeOfDevice": 'network', "mask": ["10.50.51.1", "10.50.52.1"]},
                  {"typeOfDevice": 'network', "mask": ["10.50.53.1", "10.50.54.1"]}]
    elif sys.argv[2] == "IND":
        Site= "IND"
        inputs = [{"typeOfDevice": 'linux', "mask": ["10.50.101.1", "10.50.102.1"]},
                  {"typeOfDevice": 'linux', "mask": ["10.50.103.1", "10.50.104.1"]},
                  {"typeOfDevice": 'window', "mask": ["10.50.131.1", "10.50.132.1"]},
                  {"typeOfDevice": 'window', "mask": ["10.50.133.1", "10.50.134.1"]},
                  {"typeOfDevice": 'network', "mask": ["10.50.151.1", "10.50.152.1"]},
                  {"typeOfDevice": 'network', "mask": ["10.50.153.1", "10.50.154.1"]}]
    elif sys.argv[2] == "MUMBAI":
        Site= "MUMBAI"
        inputs = [{"typeOfDevice": 'linux', "mask": ["10.50.71.1", "10.50.72.1"]},
                  {"typeOfDevice": 'linux', "mask": ["10.50.73.1", "10.50.74.1"]},
                  {"typeOfDevice": 'window', "mask": ["10.50.81.1", "10.50.82.1"]},
                  {"typeOfDevice": 'window', "mask": ["10.50.83.1", "10.50.84.1"]},
                  {"typeOfDevice": 'network', "mask": ["10.50.91.1", "10.50.92.1"]},
                  {"typeOfDevice": 'network', "mask": ["10.50.93.1", "10.50.94.1"]}]
    elif sys.argv[2] == "BLR":
        Site= "BLR"
        inputs = [{"typeOfDevice": 'linux', "mask": ["10.50.171.1", "10.50.172.1"]},
                  {"typeOfDevice": 'linux', "mask": ["10.50.173.1", "10.50.174.1"]},
                  {"typeOfDevice": 'window', "mask": ["10.50.181.1", "10.50.182.1"]},
                  {"typeOfDevice": 'window', "mask": ["10.50.183.1", "10.50.184.1"]},
                  {"typeOfDevice": 'network', "mask": ["10.50.191.1", "10.50.192.1"]},
                  {"typeOfDevice": 'network', "mask": ["10.50.193.1", "10.50.194.1"]}]
    else:
        print "Please enter valid Site"
        exit()
else:
    print "Please enter correct parameter"
    exit()

Token= RequiredAPI.getToken(NCE_IP)
print "token created"
Org,Site=RequiredAPI.getOrgAndSite(NCE_IP,Token,Site)
print "ORG and Site ID selected"

for input in inputs:
    try:
        requestPayload = {"scheduleInfo": {"recurrence": "NOW", "recurrenceMin": "", "scheduleDate": "", "scheduleTime": "",
                                           "recurrenceHour": "", "scheduleTimeAMPM": "", "scheduleEndDate": "",
                                           "scheduleEndTime": "", "scheduleEndTimeAMPM": ""}, "resetCredentials": False,
                          "triggerType": "NETWORK_DISCOVERY", "communityStringInfo": [],
                          "ipPool": {"fqdnAddress": [], "ipRange": [{"ipAddressFrom": "", "ipAddressTo": ""}],
                                     "maskRange": []}, "discoveredDeviceType": "True", "dsSelectedOrganization": "#",
                          "requestName": "", "authList": [
                {"username": "root", "api": "", "ssh": "", "jumpServer": "", "windows": "", "jumpServeripAddress": "",
                 "password": "FixStream", "apiType": "", "userProfile": "", "telnet": "", "sshkey": ""}],
                          "enabledPasswordList": [{"enablePassword": ""}],
                          "applicationProperties": {"openstackDetails": []}, "dsSelectedSiteId": "*"}
        typeOfDevice = input["typeOfDevice"]
        subnets=[];
        for mask in input["mask"]:
            subnets.append({"ipAddressMask":mask,"mask":"24"})

        if typeOfDevice == 'linux' or typeOfDevice == 'network':
            requestPayload["authList"][0]["ssh"] = True;

        if typeOfDevice == 'window':
            requestPayload["authList"][0]["windows"] = True;

        if typeOfDevice == 'hypervisor':
            requestPayload["authList"][0]["api"] = True;
            requestPayload["authList"][0]["apiType"] = "PYSPHERE";

        requestPayload["ipPool"]["maskRange"]=subnets
        requestPayload["requestName"]=typeOfDevice
        requestPayload["dsSelectedSiteId"]=Site
        requestPayload["dsSelectedOrganization"]=Org
        requestPayload=json.dumps(requestPayload)
        print "Schedule device discovery Request for " + typeOfDevice + " " + str(input["mask"])
        response= RequiredAPI.schedule_discovery(NCE_IP,Token,Org,Site,requestPayload)
        numberofSecond=0;
        while True:
            time.sleep(120)
            numberofSecond=numberofSecond+120
            value,requestId = RequiredAPI.get_all_scheduledDiscoveryRequest(NCE_IP,Token,Org,Site,"NETWORK_DISCOVERY")
            if value == 0:
                requestPayload=None
                print "Request successful with for "+typeOfDevice+" "+str(input["mask"])
                break;
            if value == 1 and (numberofSecond/60) > 20 :
                res= RequiredAPI.deleteRequest(NCE_IP,Token,Org,Site,requestId)
                print "Request is deleted for "+typeOfDevice+" "+str(input["mask"])
                break;
        isExist = RequiredAPI.get_all_matchingDevices(NCE_IP, Token, Org, Site,typeOfDevice)
        if isExist > 0:
            print "devices are exist in inventory" + typeOfDevice + " " + str(input["mask"])
        else:
            print "devices are not exist in inventory" + typeOfDevice + " " + str(input["mask"])
    except Exception as e:
        print e
