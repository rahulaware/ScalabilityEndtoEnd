sh createDummyDevicesAndFlowsOnDC.sh 172.16.2.115 root FixStream

python scheduleDiscovery.py 172.16.2.112 US >> discoveryLog.txt

python scheduleServerPerformanceList.py
