sh createDummyDevicesAndFlowsOnDC.sh 172.16.3.59 root FixStream

python scheduleDiscovery.py 172.16.2.112 MUMBAI >> Discovery.txt

python EventCollectionRequest.py 172.16.2.112 MUMBAI >> Event.txt

python scheduleServerPerformanceListMUMBAI.py
