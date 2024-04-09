from netmiko import ConnectHandler
# Command to install Docker (for Ubuntu/Debian-based systems)
install_command = 'sudo apt-get update && sudo apt-get install -y docker.io'
# SSH connection and installation
def install_docker(device, install_command):
    try:
        # Connect to the device
        net_connect = ConnectHandler(**device)

        # Send command to install Docker
        output = net_connect.send_command(install_command, expect_string=r'\[sudo\] password')
        
        # Provide password if required
        if 'password' in output.lower():
            net_connect.send_command(device['password'], expect_string=r'#')

        # Print output
        print(output)

        # Disconnect
        net_connect.disconnect()
        print("Docker installed successfully.")
        
    except Exception as e:
        print("An error occurred:", e)

# Call the function to install Docker
install_docker(device, install_command)