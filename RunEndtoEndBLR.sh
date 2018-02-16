sh createDummyDevicesAndFlowsOnDC.sh 172.16.3.60 root FixStream

python scheduleDiscovery.py 172.16.2.112 BLR >> Discovery.txt

python EventCollectionRequest.py 172.16.2.112 BLR >> Event.txt

python scheduleServerPerformanceListBLR.py
