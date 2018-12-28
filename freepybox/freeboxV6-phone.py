#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This example can be run safely as it won't change anything in your box configuration
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

# Extract phone config using connection API
'''
[   {   'gain_rx': 50,
        'gain_tx': 50,
        'hardware_defect': False,
        'id': 1,
        'is_ringing': False,
        'on_hook': True,
        'type': 'fxs',
        'type_id': 1,
        'vendor': 'unknown'},
        
    {   'gain_rx': 0,
        'gain_tx': 0,
        'hardware_defect': False,
        'id': 2,
        'is_ringing': False,
        'on_hook': True,
        'type': 'dect',
        'type_id': 1,
        'vendor': 'siemens_gigaset'}]
'''
fbx_phone_config = fbx.phone.get_config()
for phone in fbx_phone_config:
    print("Phone " + str(phone["id"]) + ", type: " + phone["type"])
    print("\t is_ringing: " + str(phone["is_ringing"]))
    print("\t on_hook: " + str(phone["on_hook"]))
    print("\t vendor: " + phone["vendor"])

# Close the freebox session
fbx.close()

