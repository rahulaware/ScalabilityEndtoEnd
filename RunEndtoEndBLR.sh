sh createDummyDevicesAndFlowsOnDC.sh 172.16.3.60 root FixStream

python scheduleDiscovery.py 172.16.2.112 BLR >> discoveryLog.txt

python scheduleServerPerformanceListBLR.py
