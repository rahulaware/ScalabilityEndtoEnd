import API;
import json;
from jsonpath import jsonpath
username = "superadmin"
password = "admin098"
grant_type="password"
client_id="fixstreamapp"
client_secret="fixstream"

org_name = 'FIXSTREAM'
org_id_jsonpath = "$[?(@.orgName=='" + org_name + "')].orgId"


auth_Token="/oauth/token"
siteURL ='/api/v2/sites'
getDeviceURL = '/api/v2/devices'

def getToken(NCE_IP):
    Token_URL="https://"+NCE_IP+auth_Token
    request_params = '?grant_type=' + grant_type + '&client_id=' + client_id + \
                     '&client_secret=' + client_secret + '&username=' + \
                     username + '&password=' + password + '&scope=read%2Cwrite%2Ctrust'
    headers = {"Content-Type": "application/json", "Authorization": "", "orgId": "", "siteId": ""}
    authResponse = API.sendPOSTRequest(Token_URL + request_params, '', '')
    authResponse = json.loads(authResponse)
    return authResponse["token_type"] + " " + authResponse["access_token"]

def getOrgAndSite(NCE_IP,token,site):
    Site_URL = "https://"+NCE_IP+siteURL
    data = json.loads(API.sendGETRequest(Site_URL, token));
    response = data["data"]
    count = 0
    while (count < len(response[0]['siteList'])):
        response[0]['siteList'][count]['address'] = None
        count = count + 1
    response = json.dumps(response)
    site_response = json.loads(response)
    orgId = jsonpath(
        site_response, org_id_jsonpath)
    site_id_jsonpath = "$[?(@.orgName=='" + org_name + \
                       "')].siteList[?(@.siteName=='" + site + "')].siteId"
    siteId = jsonpath(
         site_response, site_id_jsonpath)
    return orgId[0], siteId[0]

def acivateEventCenterConfigurationStatus (NCE_IP,token,orgId, siteId, createTime, updateTime, snmpCommunity, snmpVersion) :
    body_param = '{"header":{"orgId":"' + orgId + '","siteId":"' + siteId + '","dcId":"DATA_COLLECTOR_ID","dcTriggerType":"SNMP_TRAP_CONFIG_CHANGE","msgType":"SNMP/FCA_CONFIG/SNMP_TRAP","dcCreateTime":' + createTime + ',"dcUpdateTime":' + updateTime + '},"properties":{"snmpCommunity":"' + snmpCommunity + '","snmpVersion":"' + snmpVersion + '","snmpV3Username":null,"snmpV3AuthPassphrase":null,"snmpV3AuthProtocol":null,"snmpV3PrivacyPassphrase":null,"snmpV3PrivacyProtocol":null,"siteFaultCollectionStatus":"true","siteV3FaultCollectionStatus":null}}'
    acivateEventCenterConfigurationStatus_url = "https://"+NCE_IP+'/api/v2/ec/configure'
    responseindict = json.loads(API.sendPOSTRequest(acivateEventCenterConfigurationStatus_url, body_param, token, orgId, siteId))
    response = responseindict["data"]
    response= json.dumps(response)
    return response



get_all_scheduledRequest="/api/v2/scheduler/status/"
def get_all_scheduledDiscoveryRequest(NCE_IP,token, orgId, siteId,typeOfRequest):
    if typeOfRequest == "SERVER_MONITORING":
        request_append='all?page=1&size=25&sort=status,DESC&triggerType ='+typeOfRequest
    if typeOfRequest == "NETWORK_DISCOVERY":
        request_append = "all?page=1&size=25&sort=startDate,DESC&status=IN_PROGRESS&triggerType="+typeOfRequest
    if typeOfRequest == "PCAP_COLLECTION":
        request_append = "all?page=1&size=25&sort=status,DESC&triggerType=" + typeOfRequest

    url="https://"+NCE_IP+get_all_scheduledRequest+request_append
    responseindict = json.loads(API.sendGETRequest(url, token, orgId, siteId))
    response = int(responseindict["data"]["pageInfo"]["totalRecords"])
    if response == 0:
        return response,None
    else:
        return response,responseindict["data"]["pageData"][0]["requestId"]

deleteRequestURL="/api/v2/dataCollector/schedule/"
def deleteRequest(NCE_IP,token, orgId, siteId,requestID):
    url="https://"+NCE_IP+deleteRequestURL+requestID
    requestPayload = '{"ipPool":{"ipaddressfrom":"","ipaddressto":"","ipaddressmask":"","fqdnaddress":[],"mask":""},"requestId":"%","dsSelectedSiteId":"*","dsSelectedOrganization":"#","action":"DELETED","status":"CREATED","triggerType":"JOB_ACTION"}'
    requestPayload = requestPayload.replace("*", siteId);
    requestPayload = requestPayload.replace("#", orgId);
    requestPayload = requestPayload.replace("%", requestID);
    responseindict = json.loads(API.sendPUTRequest(url, requestPayload, token, orgId,siteId))
    return responseindict

check_all_device="/api/v2/devices/tableView"
def get_all_matchingDevices(NCE_IP,token, orgId, siteId,typeofDevice):
    request_append = "?page=1&size=25&sort=lastUpdateTime,DESC"
    url="https://"+NCE_IP+check_all_device+request_append
    requestPayload='{"filterClassList":[{"columnName":"hostName","searchOperator1":"CONTAINS","searchValue1":"'+typeofDevice+'","searchLogicalOperator":null,"searchOperator2":null,"searchValue2":null}]}'
    responseindict = json.loads(API.sendPOSTRequest(url, requestPayload, token, orgId,siteId))
    response = int(responseindict["data"]["pageInfo"]["totalRecords"])
    return response



def get_all_discovered_and_unscheduled_compute_devices(NCE_IP,token,orgId, siteId,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time,typeOfRequest):
    if typeOfRequest == 'SERVER_MONITORING':
        request_append = '/all?scheduleDate=' + schedule_start_date + '&scheduleTime=' + schedule_start_time + '&scheduleEndDate=' + schedule_end_date + '&scheduleEndTime=' + schedule_end_time + \
                     '&devSubType=FABRIC_INTERCONNECT&devSubType=SWITCH&devSubType=ROUTER&devSubType=LB&devSubType=BARE_METAL&devSubType=VM&devSubType=HYPERVISOR&devSubType=COMPUTE&triggerType='+typeOfRequest+'&reachableList=TELNET&reachableList=SSH&reachableList=WINEXE&reachableList=SNMP&reachableList=WMI_SHELL&reachableList=JUMP_SERVER&reachableList=WMIC&reachableList=PYSPHERE'

    if typeOfRequest == 'PCAP_COLLECTION':
        request_append = '/all?scheduleDate=' + schedule_start_date + '&scheduleTime=' + schedule_start_time + '&scheduleEndDate=' + schedule_end_date + '&scheduleEndTime=' + schedule_end_time + \
                     '&triggerType='+typeOfRequest

    url = "https://"+NCE_IP+getDeviceURL + request_append
    responseindict = json.loads(API.sendGETRequest(url, token, orgId, siteId))
    response = responseindict["data"]
    response = json.dumps(response)
    return response

def scheduleServerFlow(response,interval,NumberOfDevices,NCE_IP,token,orgId, siteId,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time):
    import json
    devices = json.loads(response);
    requiredList = [];
    count=0;
    for device in devices:
        temp = {};
        temp["deviceId"] = device["deviceId"];
        temp["ip"] = device["discoveredIpAddr"];
        temp["fqdn"] = device["fqdn"];
        requiredList.append(temp);
        count = count+1;
        if count == int(NumberOfDevices):
            break;
    #print len(requiredList),requiredList

    requestPayload = {
        "ipPool": {
            "fqdnAddress": [],
            "maskRange": [],
            "ipRange": []
        },
        "dsSelectedSiteId": siteId,
        "dsSelectedOrganization": orgId,
        "scheduleInfo": {
            "recurrence": "MINUTE",
            "recurrenceMin": interval,
            "recurrenceHour": "",
            "scheduleDate": schedule_start_date,
            "scheduleTime": schedule_start_time,
            "scheduleEndDate": schedule_end_date,
            "scheduleEndTime": schedule_end_time
        },
        "triggerType": "PCAP_COLLECTION",
        "createdBy": "Admin",
        "discoveredDeviceType": "true",
        "requestName": str(NumberOfDevices) + " devices and interval "+str(interval)
    }
    requestPayload["ipPool"]["fqdnAddress"] = requiredList;
    requestPayload= json.dumps(requestPayload)
    serverperformancescheduleURL_v2='/api/v2/dataCollector/schedule/'
    schedule_server_performance_URL = "https://"+NCE_IP + serverperformancescheduleURL_v2
    responseindict = json.loads(API.sendPOSTRequest(schedule_server_performance_URL, requestPayload, token, orgId,siteId))
    response = responseindict["data"]
    import re
    m = re.search(r"\[([A-Za-z0-9_-]+)\]", response)
    return m.group(1)


def selectDevices(response,NumberOfDevices):
    import json
    devices = json.loads(response);
    requiredList = [];
    count = 0;
    for device in devices:
        temp = {};
        temp["deviceId"] = device["deviceId"];
        temp["ip"] = device["discoveredIpAddr"];
        temp["fqdn"] = device["fqdn"];
        requiredList.append(temp);
        count = count + 1;
        if count == int(NumberOfDevices):
            break;
    return requiredList;


def schedulePerformance(requiredList,interval,NumberOfDevices,NCE_IP,token,orgId, siteId,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time):
    #print len(requiredList),requiredList
    requestPayload = {
        "ipPool": {
            "fqdnAddress": [],
            "maskRange": [],
            "ipRange": []
        },
        "dsSelectedSiteId": siteId,
        "dsSelectedOrganization": orgId,
        "scheduleInfo": {
            "recurrence": "MINUTE",
            "recurrenceMin": interval,
            "recurrenceHour": "",
            "scheduleDate": schedule_start_date,
            "scheduleTime": schedule_start_time,
            "scheduleEndDate": schedule_end_date,
            "scheduleEndTime": schedule_end_time
        },
        "triggerType": "SERVER_MONITORING",
        "createdBy": "Admin",
        "discoveredDeviceType": "true",
        "requestName": str(NumberOfDevices) + " devices and interval "+str(interval)
    }
    requestPayload["ipPool"]["fqdnAddress"] = requiredList;
    requestPayload= json.dumps(requestPayload)
    serverperformancescheduleURL_v2='/api/v2/dataCollector/schedule/'
    schedule_server_performance_URL = "https://"+NCE_IP + serverperformancescheduleURL_v2
    responseindict = json.loads(API.sendPOSTRequest(schedule_server_performance_URL, requestPayload, token, orgId,siteId))
    response = responseindict["data"]
    import re
    m = re.search(r"\[([A-Za-z0-9_-]+)\]", response)
    return m.group(1)

discoveryURL='/api/v2/dataCollector/schedule/'
def schedule_discovery(NCE_IP,token,orgId, siteId, discovery_body_param):
    discovery_url = "https://"+NCE_IP+ discoveryURL
    discovery_response = json.loads(API.sendPOSTRequest(discovery_url, discovery_body_param, token, orgId, siteId))
    discovery_response=  discovery_response["data"]
    return discovery_response

deviceIdHostName=[];
#getscheduledDevicesURL='/api/v2/metrics/ipAddress/octet/1
getDeviceIdURL ='/api/v2/metrics/ipAddress/octet/1'
def getscheduledDeviceswithdeviceId(NCE_IP,token,orgId, siteId):
    getscheduledDeviceswithDeviceIdURL = "https://"+NCE_IP + getDeviceIdURL
    discovery_response = json.loads(API.sendGETRequest(getscheduledDeviceswithDeviceIdURL,token, orgId, siteId))
    discovery_response=  discovery_response["data"]
    return discovery_response


getscheduledDevicesURL='/api/v2/scheduler/octet/'
def getscheduledDevicesForPerformance(NCE_IP,token,orgId, siteId, requestID):
    getscheduledDevicesURL1 = "https://"+NCE_IP + getscheduledDevicesURL + requestID
    discovery_response = json.loads(API.sendGETRequest(getscheduledDevicesURL1,token, orgId, siteId))
    discovery_response=  discovery_response["data"]
    from jsonpath import jsonpath
    deviceList= jsonpath(discovery_response, "$..fqdn")
    deviceNameList=[];
    for device in deviceList:
        deviceNameList.append(str(device).split(".")[0])
    discovery_response = getscheduledDeviceswithdeviceId(NCE_IP, token, orgId, siteId)
    deviceIdList=[]
    for key in discovery_response:
        for device in discovery_response[key]:
            if device["hostName"] in deviceNameList:
                deviceIdList.append(device["deviceId"])
    return deviceIdList
#print getscheduledDevicesForPerformance("172.16.2.112","Bearer 06ab96f8-bcc1-4725-b076-19b66ac0c689","5829fbce-2580-46f0-8194-0950fee12b77:FIXSTREAM","9e7c11c8-28fd-44a9-9b54-37efe8668d2c:IND","52bdcb17-6d23-4219-b3e4-f9a327f6d90b")

# getscheduledDevicesIdURL='/api/v2/scheduler/devices/'
# def getscheduledDevicesIDForPerformance(NCE_IP,token,orgId, siteId, requestID):
#      getscheduledDevicesIdURL1 = "https://"+NCE_IP + getscheduledDevicesIdURL + requestID
#      discovery_response = json.loads(API.sendGETRequest(getscheduledDevicesIdURL1,token, orgId, siteId))
#      discovery_response=  discovery_response["data"]
#      from jsonpath import jsonpath
#      deviceIdList= jsonpath(discovery_response, "$..deviceId")
#      return deviceIdList
#print getscheduledDevicesIDForPerformance("172.16.2.112","Bearer c8a4f457-c19b-427d-b5f1-c06a45a32add","5829fbce-2580-46f0-8194-0950fee12b77:FIXSTREAM","9ca0574f-e9d4-4270-b771-d30cd6fd2a91:US","dfba8633-d1fc-45cf-8916-40fb768720e")

getPerformancedatafordeviceURL='/api/v2/metrics/server/timeSeries'
def getPerformancedatafordevice(NCE_IP,token,orgId, siteId, deviceID,metricName,instanceType,instanceName):
    appendString='?days=3&deviceId='+deviceID+'&instanceName='+instanceName+'&instanceType='+instanceType+'&metricGroup='+metricName+'&rollup=1&type=server'
    getscheduledDevicesURL1 = "https://"+NCE_IP + getPerformancedatafordeviceURL + appendString
    discovery_response = json.loads(API.sendGETRequest(getscheduledDevicesURL1,token, orgId, siteId))
    discovery_response=  discovery_response["data"]
    from jsonpath import jsonpath
    datapoint= jsonpath(discovery_response, "$..dataSet")
    if datapoint == False:
        return False
    else:
        outputList = []
        L = datapoint[0]
        for l2 in L:
                date_time = l2["timeStamp"]
                Data = (date_time.split(".")[0]).split("T")
                t1 = (deviceID,metricName,instanceType,instanceName,l2["metricValue"], Data[0] + " " + Data[1])
                outputList.append(t1)
                t1 = None
        return outputList
