import requests;
import logging
logging.getLogger("requests").setLevel(logging.ERROR)

def sendGETRequest(url, auth_token, orgId = "", siteId = ""):
    headers = {'Content-Type': 'application/json', 'Authorization': str(auth_token), 'orgId' : orgId, 'siteId': siteId}
    r = requests.get(url, headers=headers, verify=False , timeout=120)
    #print url + "----------" + str(r.status_code)
    if(r.status_code != 200):
        r.raise_for_status()
    return r.content

def sendPUTRequest(url, bodyParameters, token, orgId = "", siteId = "", sheetId = ""):
    headers = {'Content-Type': 'application/json', 'Authorization': str(token), 'orgId' : orgId, 'siteId': siteId}
    r = requests.put(url, data=bodyParameters, headers=headers, verify=False)
    #print url + "----------" + str(r.status_code)
    if(r.status_code != 201 or r.status_code != 200):
        r.raise_for_status()
    return r.content

def sendPOSTRequest(url, bodyParameters, token, orgId = "", siteId = "", sheetId = ""):
    if (sheetId != ""):
        headers = {'Content-Type': 'application/json', 'Authorization': str(token), 'orgId' : orgId, 'siteId': siteId, 'sheetId': sheetId}
    else:
        headers = {'Content-Type': 'application/json', 'Authorization': str(token), 'orgId' : orgId, 'siteId': siteId}
    r = requests.post(url, data=bodyParameters, headers=headers, verify=False)
    #print url +"----------"+str(r.status_code)
    if(r.status_code != 201 or r.status_code != 200):
        r.raise_for_status()
    return r.content

