
username='root'
password='FixStream'

if [ "$#" == 1 ]
then
  DCIP=$1
  echo "$DCIP"
  if [ $DCIP == '172.16.2.115' ]
  then
    sshpass -p $password scp SourceFile/DummyDeviceandPerformance.tar.gz $username@$DCIP:/root
    sshpass -p $password ssh $username@$DCIP << EOF
    tar -xvf /root/DummyDeviceandPerformance.tar.gz -C /opt/meridian/dc/var/fsdc/data
    cd /opt/meridian/dc/var/fsdc/data
    chmod 777 create_dummy_devices.py
    python create_dummy_devices.py USlinux 1022 linux 10.50.1.1
    python create_dummy_devices.py USwindow 1022 window 10.50.31.1
    python create_dummy_devices.py USswitch 1022 network 10.50.51.1
    python create_dummy_devices.py USHypervisor 1022 hypervisor 10.50.61.1
    rm -rf /root/DummyDeviceandPerformance.tar.gz
EOF
    python scheduleDiscoveryUS.py

  else
    sshpass -p $password scp SourceFile/DummyDeviceandPerformance.tar.gz $username@$DCIP:/root
    sshpass -p $password ssh $username@$DCIP << EOF
    tar -xvf /root/DummyDeviceandPerformance.tar.gz -C /opt/meridian/dc/var/fsdc/data
    cd /opt/meridian/dc/var/fsdc/data
    chmod 777 create_dummy_devices.py
    python create_dummy_devices.py INDlinux 1022 linux 10.50.101.1
    python create_dummy_devices.py INDwindow 1022 window 10.50.131.1
    python create_dummy_devices.py INDswitch 1022 network 10.50.151.1
    python create_dummy_devices.py INDHypervisor 1022 hypervisor 10.50.161.1
    rm -rf /root/DummyDeviceandPerformance.tar.gz
EOF
    python scheduleDiscoveryIND.py
  fi
else
  echo "please enter DC IP"
fi


