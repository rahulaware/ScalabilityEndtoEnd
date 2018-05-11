from datetime import datetime
datefmt = "%Y%m%d%H%M%S"

def CalculateNumberofCycle(startTime,endTime,totalDevice,interval):

    startDate_dateObject = datetime.strptime(startTime, datefmt)
    endDate_dateObject = datetime.strptime(endTime, datefmt)
    hoursMinuteSeconds=endDate_dateObject-startDate_dateObject
    DaysDuration=0
    if hoursMinuteSeconds.days!=0 and hoursMinuteSeconds.days!=-1 :
        DaysDuration=DaysDuration+(hoursMinuteSeconds.days*24*60)
        print "Number of Days",hoursMinuteSeconds.days
    #print "Number of hours",hoursMinuteSeconds.seconds/60/60
    Duration=(hoursMinuteSeconds.seconds/60)+DaysDuration
    print "Total Duration(min):", Duration
    NumberofCyclePerDevice=Duration/interval;
    totalCycleCount = totalDevice * NumberofCyclePerDevice
    return NumberofCyclePerDevice,totalCycleCount

import MySQLdb
def dc_job_run(Database_IP, username, password, databaseName,tableName,requestID,startDate,endDate):
    db = MySQLdb.connect(Database_IP, username, password, databaseName)
    cursor = db.cursor()
    query = "select ip_address,count(*) from " + tableName + " where request_id= '%s' and _create_time >= '%s' and _create_time <= '%s' group by ip_address" % (requestID,startDate,endDate)
    cursor.execute(query)
    data = cursor.fetchall()
    #print "Number of records in table:",str(cursor.rowcount)
    sum = 0;
    for r in data:
        sum=sum+ int(r[1])
    return sum

import json,requests
def queryExecution(url,query):
    query = json.dumps(query)
    response = requests.post(url, auth=("admin", "FixStream"), data=query)
    results = json.loads(response.text)
    return results

def calculateNumberofRecord(performanceUrl,siteName,startDate,endDate):
    query = {
               "size": 2000,
               "query": {
                  "bool": {
                     "must": [
                        {
                            "wildcard": {
                                "siteId": {
                                    "value": "*:"+siteName
                                }
                            }
                        },
                        {
                           "range": {
                              "dcCreateTime": {
                                 "from": startDate,
                                 "to": endDate
                              }
                           }
                        },
                        {
                           "bool": {
                              "should": [
                                 {
                                    "bool": {
                                       "must": [
                                          {
                                             "term": {
                                                "metricGroupName": {
                                                   "value": "cpuMetrics"
                                                }
                                             }
                                          },
                                          {
                                             "term": {
                                                "instanceType": {
                                                   "value": "default"
                                                }
                                             }
                                          },
                                          {
                                             "term": {
                                                "instanceName": {
                                                   "value": "default"
                                                }
                                             }
                                          },
                                          {
                                             "term": {
                                                "metricName": {
                                                   "value": "pctUtil"
                                                }
                                             }
                                          }
                                       ]
                                    }
                                 },
                                 {
                                    "bool": {
                                       "must": [
                                          {
                                             "term": {
                                                "metricGroupName": {
                                                   "value": "memMetrics"
                                                }
                                             }
                                          },
                                          {
                                             "term": {
                                                "instanceType": {
                                                   "value": "RAM"
                                                }
                                             }
                                          },
                                          {
                                             "term": {
                                                "instanceName": {
                                                   "value": "default"
                                                }
                                             }
                                          },
                                          {
                                             "term": {
                                                "metricName": {
                                                   "value": "memUtil"
                                                }
                                             }
                                          }
                                       ]
                                    }
                                 }
                              ]
                           }
                        }
                     ]
                  }
               },
               "aggs": {
                  "metricGroupName": {
                     "terms": {
                        "field": "metricGroupName"
                     }
                  }
               }
    }

    results= queryExecution(performanceUrl,query)
    return results["aggregations"]["metricGroupName"]["buckets"][0]["doc_count"]

NCE_IP="172.16.2.112"
siteName="US"
performanceUrl='http://'+NCE_IP+':9200/meridian_metrics/_search'
DC_IP="172.16.2.115"
requestID="a67f8406-f6f4-40c7-8230-19ba3fdc57a5"
totalDevice=1500
interval=5

startDate='20180508100217'
#endDate='20180503140711'
now_utc = datetime.utcnow()
endDate = now_utc.strftime(datefmt)

numberofCyclePerDevice,numberofExpectedCycle = CalculateNumberofCycle(startDate,endDate,totalDevice,interval)
print "Start Date-----------",startDate
print "End Date-----------",endDate
print "NumberofCyclePerDevice:", str(numberofCyclePerDevice)
print "Total Cycle Count:",numberofExpectedCycle
#
numberofScheduleProcessed = dc_job_run(DC_IP,"netra","fixstream","netra_dc","dc_job_run",requestID,startDate,endDate)
numberofDevicesProcessed=numberofScheduleProcessed/numberofCyclePerDevice
print "Number of Schedule executed at DC:",numberofScheduleProcessed
print "Number of devices processed at DC:",str(numberofDevicesProcessed)
print "Schedule Passed Percent(based on missed cycle) at DC:",((numberofScheduleProcessed*100)/numberofExpectedCycle)
print "Schedule passed Percent(based on number of devices) at DC:",((numberofDevicesProcessed*100)/totalDevice)
#
#
passRecordinElasticSearch= calculateNumberofRecord(performanceUrl,siteName,startDate,endDate)
numberofDevicesProcessedAtNCE=passRecordinElasticSearch/numberofCyclePerDevice
print "Number of data point at NCE:",passRecordinElasticSearch
print "Number of devices processed at NCE:",str(numberofDevicesProcessedAtNCE)
print "Schedule Passed Percent(based on missed cycle) at NCE:",((passRecordinElasticSearch*100)/numberofScheduleProcessed)
print "Schedule passed Percent(based on number of devices) at NCE:",((numberofDevicesProcessedAtNCE*100)/numberofDevicesProcessed)
