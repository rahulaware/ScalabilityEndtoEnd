import API;
import json;
from jsonpath import jsonpath
username = "superadmin"
password = "admin098"
grant_type="password"
client_id="fixstreamapp"
client_secret="fixstream"

org_name = 'FIXSTREAM'
site_name = 'US'
site_name1 = 'IND'

org_id_jsonpath = "$[?(@.orgName=='" + org_name + "')].orgId"

site_id_jsonpath = "$[?(@.orgName=='" + org_name + \
    "')].siteList[?(@.siteName=='" + site_name + "')].siteId"

site_id1_jsonpath = "$[?(@.orgName=='" + org_name + \
    "')].siteList[?(@.siteName=='" + site_name1 + "')].siteId"


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
    if site == 'US':
        siteId = jsonpath(
            site_response, site_id_jsonpath)
    else:
        siteId = jsonpath(
            site_response, site_id1_jsonpath)
    return orgId[0], siteId[0]

get_all_scheduledRequest="/api/v2/scheduler/status/"
def get_all_scheduledDiscoveryRequest(NCE_IP,token, orgId, siteId):
    request_append = "all?page=1&size=25&sort=startDate,DESC&status=IN_PROGRESS&triggerType=NETWORK_DISCOVERY"
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



def get_all_discovered_and_unscheduled_compute_devices(NCE_IP,token,orgId, siteId,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time):
    request_append = '/all?scheduleDate=' + schedule_start_date + '&scheduleTime=' + schedule_start_time + '&scheduleEndDate=' + schedule_end_date + '&scheduleEndTime=' + schedule_end_time + \
                     '&devSubType=FABRIC_INTERCONNECT&devSubType=SWITCH&devSubType=ROUTER&devSubType=LB&devSubType=BARE_METAL&devSubType=VM&devSubType=HYPERVISOR&devSubType=COMPUTE&triggerType=SERVER_MONITORING&reachableList=TELNET&reachableList=SSH&reachableList=WINEXE&reachableList=SNMP&reachableList=WMI_SHELL&reachableList=JUMP_SERVER&reachableList=WMIC&reachableList=PYSPHERE'

    url = "https://"+NCE_IP+getDeviceURL + request_append
    responseindict = json.loads(API.sendGETRequest(url, token, orgId, siteId))
    response = responseindict["data"]
    response = json.dumps(response)
    return response

def schedulePerformance(response,interval,NumberOfDevices,NCE_IP,token,orgId, siteId,schedule_start_date,schedule_start_time,schedule_end_date,schedule_end_time):
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


#getscheduledDevicesURL='/api/v2/scheduler/octet/'
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
