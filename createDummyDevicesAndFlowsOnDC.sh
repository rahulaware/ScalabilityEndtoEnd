if [ "$#" == 3 ]
then
  DCIP=$1
  username=$2
  password=$3
  if [ $DCIP == '172.16.2.115' ]
  then
    sshpass -p $password scp SourceFile/DummyDeviceandPerformance.tar.gz $username@$DCIP:/root
    sshpass -p $password scp SourceFile/ServerFlow.tar.gz $username@$DCIP:/root
    sshpass -p $password ssh $username@$DCIP << EOF
    tar -xvf /root/DummyDeviceandPerformance.tar.gz -C /opt/meridian/dc/var/fsdc/data
    tar -xvf /root/ServerFlow.tar.gz -C /opt/meridian/dc/var/fsdc/data
    cd /opt/meridian/dc/var/fsdc/data
    chmod 777 create_dummy_devices.py
    chmod 777 create_serverFlow.py
    python create_dummy_devices.py USlinux 800 linux 10.50.1.1
    python create_dummy_devices.py USwindow 800 window 10.50.31.1
    python create_dummy_devices.py USswitch 400 network 10.50.51.1
    python create_serverFlow.py 10.50.1.1 800 linux
    python create_serverFlow.py 10.50.31.1 800 window
    rm -rf /root/DummyDeviceandPerformance.tar.gz
    rm -rf /root/ServerFlow.tar.gz
EOF
  elif [ $DCIP == '172.16.2.116' ]
    then
    sshpass -p $password scp SourceFile/DummyDeviceandPerformance.tar.gz $username@$DCIP:/root
    sshpass -p $password scp SourceFile/ServerFlow.tar.gz $username@$DCIP:/root
    sshpass -p $password ssh $username@$DCIP << EOF
    tar -xvf /root/DummyDeviceandPerformance.tar.gz -C /opt/meridian/dc/var/fsdc/data
    tar -xvf /root/ServerFlow.tar.gz -C /opt/meridian/dc/var/fsdc/data
    cd /opt/meridian/dc/var/fsdc/data
    chmod 777 create_dummy_devices.py
    chmod 777 create_serverFlow.py
    python create_dummy_devices.py INDlinux 800 linux 10.50.101.1
    python create_dummy_devices.py INDwindow 800 window 10.50.131.1
    python create_dummy_devices.py INDswitch 400 network 10.50.151.1
    python create_serverFlow.py 10.50.101.1 800 linux
    python create_serverFlow.py 10.50.131.1 800 window
    rm -rf /root/DummyDeviceandPerformance.tar.gz
    rm -rf /root/ServerFlow.tar.gz
EOF
elif [ $DCIP == '172.16.3.59' ]
    then
    sshpass -p $password scp SourceFile/DummyDeviceandPerformance.tar.gz $username@$DCIP:/root
    sshpass -p $password scp SourceFile/ServerFlow.tar.gz $username@$DCIP:/root
    sshpass -p $password ssh $username@$DCIP << EOF
    tar -xvf /root/DummyDeviceandPerformance.tar.gz -C /opt/meridian/dc/var/fsdc/data
    tar -xvf /root/ServerFlow.tar.gz -C /opt/meridian/dc/var/fsdc/data
    cd /opt/meridian/dc/var/fsdc/data
    chmod 777 create_dummy_devices.py
    chmod 777 create_serverFlow.py
    python create_dummy_devices.py MUMlinux 800 linux 10.50.71.1
    python create_dummy_devices.py MUMwindow 800 window 10.50.81.1
    python create_dummy_devices.py MUMswitch 400 network 10.50.91.1
    python create_serverFlow.py 10.50.71.1 1000 linux
    python create_serverFlow.py 10.50.81.1 1000 window
    rm -rf /root/DummyDeviceandPerformance.tar.gz
    rm -rf /root/ServerFlow.tar.gz
EOF
elif [ $DCIP == '172.16.3.60' ]
    then
    sshpass -p $password scp SourceFile/DummyDeviceandPerformance.tar.gz $username@$DCIP:/root
    sshpass -p $password scp SourceFile/ServerFlow.tar.gz $username@$DCIP:/root
    sshpass -p $password ssh $username@$DCIP << EOF
    tar -xvf /root/DummyDeviceandPerformance.tar.gz -C /opt/meridian/dc/var/fsdc/data
    tar -xvf /root/ServerFlow.tar.gz -C /opt/meridian/dc/var/fsdc/data
    cd /opt/meridian/dc/var/fsdc/data
    chmod 777 create_dummy_devices.py
    chmod 777 create_serverFlow.py
    python create_dummy_devices.py BLRlinux 800 linux 10.50.171.1
    python create_dummy_devices.py BLRwindow 800 window 10.50.181.1
    python create_dummy_devices.py BLRswitch 400 network 10.50.191.1
    python create_serverFlow.py 10.50.171.1 800 linux
    python create_serverFlow.py 10.50.181.1 800 window
    rm -rf /root/DummyDeviceandPerformance.tar.gz
    rm -rf /root/ServerFlow.tar.gz
EOF
else
   echo "Please enter valid DC _IP"
  fi
else
  echo "please enter DC IP"
fi



