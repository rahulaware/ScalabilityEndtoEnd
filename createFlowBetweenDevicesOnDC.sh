
DCIP='172.16.2.115'
DCIP1='172.16.2.116'
username='root'
password='FixStream'

echo "DEVICE Creation on DC1"
sshpass -p $password scp SourceFile/ServerFlow.tar.gz $username@$DCIP:/root
sshpass -p $password ssh $username@$DCIP << EOF
tar -xvf /root/ServerFlow.tar.gz -C /opt/meridian/dc/var/fsdc/data
cd /opt/meridian/dc/var/fsdc/data
chmod 777 create_serverFlow.py
python create_serverFlow.py 10.50.1.1 1000 linux
python create_serverFlow.py 10.50.31.1 1000 window
rm -rf /root/ServerFlow.tar.gz
EOF

echo "DEVICE Creation on DC2"
sshpass -p $password scp SourceFile/ServerFlow.tar.gz $username@$DCIP1:/root
sshpass -p $password ssh $username@$DCIP1 << EOF
tar -xvf /root/ServerFlow.tar.gz -C /opt/meridian/dc/var/fsdc/data
cd /opt/meridian/dc/var/fsdc/data
chmod 777 create_serverFlow.py
python create_serverFlow.py 10.50.101.1 1000 linux
python create_serverFlow.py 10.50.131.1 1000 window
rm -rf /root/ServerFlow.tar.gz
EOF
