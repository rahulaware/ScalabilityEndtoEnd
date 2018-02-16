from Library import RequiredAPI;
import sys,time
snmpCommunity="public"
snmpVersion="v2c"
if len(sys.argv) == 3:
    NCE_IP = sys.argv[1]
    siteName = sys.argv[2]

    Token = RequiredAPI.getToken(NCE_IP)

    Org, Site = RequiredAPI.getOrgAndSite(NCE_IP, Token, siteName)

    createTime= str(long(time.time()*1000))
    updateTime=createTime
    print RequiredAPI.acivateEventCenterConfigurationStatus(NCE_IP,Token,Org, Site, createTime, updateTime, snmpCommunity, snmpVersion)
else:
    print "Please provide NCE IP and SiteName "