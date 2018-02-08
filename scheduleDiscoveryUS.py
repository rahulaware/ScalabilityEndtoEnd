from Library import RequiredAPI;
import json,time

NCE_IP="172.16.2.112"
Site="US"
inputs=[{"typeOfDevice":'linux',"mask":["10.50.1.1","10.50.2.1"]},{"typeOfDevice":'linux',"mask":["10.50.3.1","10.50.4.1"]},\
       {"typeOfDevice":'window',"mask":["10.50.31.1","10.50.32.1"]},{"typeOfDevice":'window',"mask":["10.50.33.1","10.50.34.1"]}, \
       {"typeOfDevice": 'network', "mask": ["10.50.51.1", "10.50.52.1"]},{"typeOfDevice":'network',"mask":["10.50.53.1","10.50.54.1"]}]

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
