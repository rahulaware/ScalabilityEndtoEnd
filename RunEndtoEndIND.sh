sh createDummyDevicesAndFlowsOnDC.sh 172.16.2.116 root FixStream

python scheduleDiscovery.py 172.16.2.112 IND >> Discovery.txt

python EventCollectionRequest.py 172.16.2.112 IND >> Event.txt

python scheduleServerPerformanceListIND.py
