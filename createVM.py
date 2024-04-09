from openstack import connection
import time
# Authentication credentials
auth = {
    'auth_url': "http://10.0.0.198/identity",
    'project_name': "demo",
    'username': "admin",
    'password': "password",
    'user_domain_name': "default",
    'project_domain_name': "default"
}


def createVM(vm_name,image_name,flavor_name,keypair_name,network_id):
    conn = connection.Connection(**auth)
    # Find image and flavor
    image = conn.compute.find_image(image_name)
    flavor = conn.compute.find_flavor(flavor_name)

    existing_keypair = conn.compute.find_keypair(name_or_id=keypair_name)

    keypair = None
    if existing_keypair:
        keypair = existing_keypair
        print(f"Key pair '{keypair_name}' already exists.")
    else:
        # Create keypair
        keypair = conn.compute.create_keypair(name=keypair_name)

    # Launch VMs
    vm = conn.compute.create_server(
        name=vm_name,
        image_id=image.id,
        flavor_id=flavor.id,
        networks=[{"uuid": network_id}],
        key_name=keypair.name
    )

    print("VMs created successfully:")
    print("VM1 ID:", vm.id)

    conn.compute.wait_for_server(vm)

    public_network = conn.network.find_network(name_or_id='public')
    public_network_id = public_network.id


    # Allocate floating IPs
    floating_ip = conn.network.create_ip(floating_network_id=public_network_id)
    # Associate floating IPs with VMs
    conn.compute.add_floating_ip_to_server(vm, floating_ip.floating_ip_address)

    # Get IP addresses of VMs
    vm_ip = floating_ip.floating_ip_address
    print("VM1 Floating IP:", vm_ip)
    return vm_ip
