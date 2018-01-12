
DCIP='172.16.2.115'
DCIP1='172.16.2.116'
username='root'
password='FixStream'

echo "DEVICE Creation on DC1"
sshpass -p $password scp SourceFile/DummyDeviceandPerformance.tar.gz $username@$DCIP:/root
sshpass -p $password ssh $username@$DCIP << EOF
tar -xvf /root/DummyDeviceandPerformance.tar.gz -C /opt/meridian/dc/var/fsdc/data
cd /opt/meridian/dc/var/fsdc/data
chmod 777 create_dummy_devices.py
python create_dummy_devices.py USlinux 1050 linux 10.50.1.1
python create_dummy_devices.py USwindow 1050 window 10.50.31.1
python create_dummy_devices.py USswitch 1050 network 10.50.51.1
python create_dummy_devices.py USHypervisor 1050 hypervisor 10.50.61.1
rm -rf /root/DummyDeviceandPerformance.tar.gz
EOF

echo "DEVICE Creation on DC2"
sshpass -p $password scp SourceFile/DummyDeviceandPerformance.tar.gz $username@$DCIP1:/root
sshpass -p $password ssh $username@$DCIP1 << EOF
tar -xvf /root/DummyDeviceandPerformance.tar.gz -C /opt/meridian/dc/var/fsdc/data
cd /opt/meridian/dc/var/fsdc/data
chmod 777 create_dummy_devices.py
python create_dummy_devices.py INDlinux 1050 linux 10.50.101.1
python create_dummy_devices.py INDwindow 1050 window 10.50.131.1
python create_dummy_devices.py INDswitch 1050 network 10.50.151.1
python create_dummy_devices.py INDHypervisor 1050 hypervisor 10.50.161.1
rm -rf /root/DummyDeviceandPerformance.tar.gz
EOF
