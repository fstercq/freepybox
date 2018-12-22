#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This example will add and delete a forwarding rule in your box configuration
'''
from freepybox import Freepybox
from freepybox.exceptions import *

# Instantiate Freepybox class using default application descriptor 
# and default token_file location
fbx = Freepybox()

# Connect to the freebox with default http protocol
# and default port 80
# Be ready to authorize the application on the Freebox if you use this
# example for the first time
fbx.open('mafreebox.freebox.fr', 80)

# port forwarding rule settings
new_fwd_rule = {
    "enabled": True,
    "comment": "test rule",
    "lan_port": 4242,
    "wan_port_end": 4242,
    "wan_port_start": 4242,
    "lan_ip": "192.168.1.42",
    "ip_proto": "tcp",
    "src_ip": "0.0.0.0"
}

# Add a port forwarding rule
try:
    fbx.fw.add_forward(new_fwd_rule)
except HttpRequestError as e:
    msg = str(e)
    if msg == ("internal"):
        print("ERROR: internal error")
    else:
        print("ERROR: " + str(e))
except Exception as e:
    print("ERROR: " + str(e))

# Getting the list of port forwarding
fwd_rules = fbx.fw.get_forward()
last_id = 0
if (fwd_rules != None):
    for fwd_rule in fwd_rules:
        last_id = fwd_rule["id"]
        print("############ ", fwd_rule["id"], "############")
        print("Comment: " +  fwd_rule["comment"])
        print("Status: " +  str(fwd_rule["enabled"]))
        print("Protocol: " + fwd_rule["ip_proto"])
        print("Destination IP address: " +  fwd_rule["lan_ip"])
        print("Destination Port: " + str(fwd_rule["lan_port"]))
        print("Allowed source IP addresses: " + fwd_rule["src_ip"])
        print("Allowed source port: " +  str(fwd_rule["wan_port_start"]) +  "-" +  str(fwd_rule["wan_port_end"]))
        print("\n")

try:
    print("trying to delete the last rule id :", last_id)
    fwd_rules = fbx.fw.delete_forward(last_id)

except HttpRequestError as e:
    msg = str(e)
    if msg == ("noent"):
        print("noent: forward rule doen't exist")
    else:
        print("ERROR: " + str(e))
except Exception as e:
    print("ERROR: " + str(e))

# Close the freebox session
fbx.close()
