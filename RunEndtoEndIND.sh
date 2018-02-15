sh createDummyDevicesAndFlowsOnDC.sh 172.16.2.116 root FixStream

python scheduleDiscovery.py 172.16.2.112 IND >> discoveryLog.txt

python scheduleServerPerformanceListIND.py
