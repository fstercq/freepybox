#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This example will add and delete DCHP static lease in your box configuration
'''
from freepybox import Freepybox

# Instantiate Freepybox class using default application descriptor 
# and default token_file location
fbx = Freepybox()

# Connect to the freebox with default http protocol
# and default port 80
# Be ready to authorize the application on the Freebox if you use this
# example for the first time
fbx.open('mafreebox.freebox.fr', 80)

# Open backup file
file = open("Freeboxv6-backup.conf","w")

# Set DHCP server config
new_conf = {
        "enabled": True,
        "gateway": "192.168.1.254",
        "sticky_assign": True,
        "ip_range_end": "192.168.1.199",
        "netmask": "255.255.255.0",
        "dns": [
            "9.9.9.9",
            "192.168.1.254",
            "",
            "",
            ""
        ],
        "always_broadcast": False,
        "ip_range_start": "192.168.1.100"
}
fbx.dhcp.set_config(new_conf)

# Get DHCP server config
dhcp_config = fbx.dhcp.get_config()
print(dhcp_config)

# Get the list of DHCP dynamic leases
static_dhcp_leases = fbx.dhcp.get_static_dhcp_lease()
if static_dhcp_leases:
    file.write("static_dhcp_leases:\n")
    print(static_dhcp_leases)
    file.write(static_dhcp_leases)
    file.write("\n")

# Get the list of DHCP dynamic leases
dhcp_leases = fbx.dhcp.get_dynamic_dhcp_lease()
file.write("dhcp_leases:\n")
file.write(str(dhcp_leases))
file.write("\n")
for lease in dhcp_leases:
    print("#####", lease["hostname"], "#####")
    print("mac: ", lease["mac"])
    print("ip: ", lease["ip"])
    print("reachable: ", lease["host"]["reachable"])
    print("vendor_name: ", lease["host"]["vendor_name"])
    print("active: ", lease["host"]["active"])
    print("host_type: ", lease["host"]["host_type"])
    print("persistent: ", lease["host"]["persistent"])
    print()
    
    file.write("#####" + lease["hostname"] + "#####" + "\n")
    file.write("mac: " + lease["mac"] + "\n")
    file.write("ip: " + lease["ip"] + "\n")
    file.write("reachable: " + str(lease["host"]["reachable"]) + "\n")
    file.write("vendor_name: " + lease["host"]["vendor_name"] + "\n")
    file.write("active: " + str(lease["host"]["active"]) + "\n")
    file.write("host_type: " + lease["host"]["host_type"] + "\n")
    file.write("persistent: " + str(lease["host"]["persistent"]) + "\n")

# Add a DHCP static lease
data = {
   "ip": "192.168.1.222",
   "mac": "00:00:00:11:11:11",
   "comment":"comment"
}
fbx.dhcp.set_static_dhcp_lease(data)

# Delete a DHCP static lease with this MAC address
fbx.dhcp.delete_static_dhcp_lease("00:00:00:11:11:11")

# Close the freebox session
fbx.close()

# Close file backup file
file.close() 
