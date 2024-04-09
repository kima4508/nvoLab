
from openstack import connection
#security_group_name = 'default'

# Authentication credentials
auth = {
    'auth_url': "http://10.0.0.198/identity",
    'project_name': "demo",
    'username': "admin",
    'password': "password",
    'user_domain_name': "default",
    'project_domain_name': "default"
}

def allowICMP(security_group_name):

    conn = connection.Connection(**auth)
    security_groups = list(conn.network.security_groups(name=security_group_name))
    if not security_groups:
        print(f"Security group '{security_group_name}' not found.")
        exit()

    # Assuming there's only one security group with the given name, taking the first one
    security_group_id = security_groups[0].id

    #Add ICMP for ingress and egress direction for Floating Ips to be reachable
    icmp_rules = [
        {
        'security_group_id': security_group_id,
        'direction': 'ingress',
        'protocol': 'icmp',
        'remote_ip_prefix': '0.0.0.0/0'
        },
        {
        'security_group_id': security_group_id,
        'direction': 'egress',
        'protocol': 'icmp',
        'remote_ip_prefix': '0.0.0.0/0'
        }
    ]

    for icmp_rule in icmp_rules:
        conn.network.create_security_group_rule(**icmp_rule)

def allowAllbetweenVN(security_group_name,network1_cidr,network2_cidr):

    conn = connection.Connection(**auth)
    security_groups = list(conn.network.security_groups(name=security_group_name))
    if not security_groups:
        print(f"Security group '{security_group_name}' not found.")
        exit()

    # Assuming there's only one security group with the given name, taking the first one
    security_group_id = security_groups[0].id

    #Add ICMP for ingress and egress direction for Floating Ips to be reachable
    VN_rules = [
        {
            'security_group_id': security_group_id,
            'direction': 'ingress',
            'protocol': None,  # Allow any protocol
            'remote_ip_prefix': network1_cidr,
        },
        {
            'security_group_id': security_group_id,
            'direction': 'egress',
            'protocol': None,  # Allow any protocol
            'remote_ip_prefix': network1_cidr,
        },
                {
            'security_group_id': security_group_id,
            'direction': 'ingress',
            'protocol': None,  # Allow any protocol
            'remote_ip_prefix': network2_cidr,
        },
        {
            'security_group_id': security_group_id,
            'direction': 'egress',
            'protocol': None,  # Allow any protocol
            'remote_ip_prefix': network2_cidr,
        }
    ]hatg

    for  VN_rule in VN_rules:
        conn.network.create_security_group_rule(**VN_rule)