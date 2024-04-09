from netmiko import ConnectHandler

bgp_commands = [
    'vtysh',  # Enter vtysh
    'conf t',  # Enter configuration mode
    'router bgp 20',  # Example BGP AS number
    'neighbor 13.13.13.1 remote-as 20',  # Example neighbor configuration
    'exit',  # Exit BGP configuration
    'exit'  # Exit vtysh
]
def configFRR(vm):
    net_connect = ConnectHandler(**vm)
    # Use SCP to transfer file
            # Construct the SCP command
    scp_command = f'scp Dockerfile sdn@sdn:/hone/sdn/Dockerfile'

    # Execute the SCP command
    output = net_connect.send_command_timing(scp_command)
    print("File uploaded successfully.")
    net_connect.send_command_timing("docker run -it . /bin/bash")
    net_connect.send_command_timing("service frr start")
    net_connect.send_config_set(bgp_commands)
    return

def configBGP(vm):
    #Configure RYU
    net_connect = ConnectHandler(**vm)
    scp_command = f'scp bgp.conf.py sdn@sdn:/hone/sdn/bgp.conf.py'
    net_connect.send_command_timing("sudo ryu-manager --verbose --bgp-app-config-file bgp.conf.py ryu/services/protocols/bngp/application.py ryu/ryu/app/simple_switch_13.py &")
    net_connect.send_command_timing("docker run -it . /bin/bash")
    net_connect.send_command("sudo ovs-vsctl add-br mybridge")                                          # create a bridge 
    net_connect.send_command("sudo ovs-vsctl add-port mybridge eth0")    # add a port to the bridge
    net_connect.send_command("sudo ovs-vsctl set bridge mybridge protocols=OpenFlow13") # set the bridge to use OpenFlow version 13
    net_connect.send_command("sudo ovs-vsctl set-controller mybridge tcp:"+vm["host"]+":6633")
    return


