from openstack import connection
import os,subprocess,time


router_name = "router1"
# Define network parameters for creating VN
network_name = 'network1'
subnet_name = 'subnet1'
cidr = '10.10.10.0/24'


# Authentication credentials
auth = {
    'auth_url': "http://10.0.0.198/identity",
    'project_name': "demo",
    'username': "admin",
    'password': "password",
    'user_domain_name': "default",
    'project_domain_name': "default"
}

def createNetwork(network_name,subnet_name,cidr,router_name):
    conn = connection.Connection(**auth)
    ip_version = 4
    # Create network
    network = conn.network.create_network(name=network_name, shared= True)

    # Create subnet
    subnet = conn.network.create_subnet(
        name=subnet_name,
        network_id=network.id,
        cidr=cidr,
        ip_version=ip_version
    )

    print("Network and Subnet created successfully:")
    print("Network ID:", network.id)
    print("Subnet ID:", subnet.id)



    # Find existing router
    router = conn.network.find_router(router_name)

    # Attach network subnet to router
    conn.network.add_interface_to_router(router, subnet_id=subnet.id)
    print("Network attached to the existing router successfully.")
    return network.id
