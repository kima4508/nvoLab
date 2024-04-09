from openstack import connection
from createNetwork import createNetwork
from createVM import createVM
from addRules import allowICMP,allowAllbetweenVN
from dockerInstall import install_docker
from configureRouting import *

#Create network1
network1_id = createNetwork("network1","subnet1","10.10.10.0/24","router1")

#Create network2
network2_id = createNetwork("network2","subnet1","20.20.20.0/24","router1")


#Add Rules to allow host reachibility to Floating Ips
allowICMP("default")


#Add Rules to allow any communication between network1 and network2
allowAllbetweenVN("default","10.10.10.0/24","20.20.20.0/24")


#Create Two VM in network1
floatingIP1 = createVM(vm_name="vm1-network1",image_name="mini",flavor_name="m1.small",keypair_name="mykeyPair",network_id=network1_id)
floatingIP2 = createVM(vm_name="vm2-network1",image_name="mini",flavor_name="m1.small",keypair_name="mykeyPair",network_id=network1_id)

#Create one VM in network2
createVM(vm_name="vm1-network2",image_name="mini",flavor_name="m1.small",keypair_name="mykeyPair",network_id=network2_id)

vm2 = {
    'device_type': 'linux',
    'host': floatingIP2,
    'username': 'minine',
    'password': 'mininet'
}

install_docker(vm2)
configFRR(vm2)
configBGP(vm2)


