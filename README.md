freepybox
==========

Easily manage your freebox in Python using the Freebox OS API.
Check your calls, manage your contacts, configure your dhcp, disable your wifi, monitor your LAN activity and many others, on LAN or remotely.

freepybox is a python library implementing the freebox OS API. It handles the authentication process and provides a row access to the freebox API.

Install
-------
Use the PIP package manager
```bash
$ pip install freepybox
```

Or manually download and install the last version from github
```bash
$ git clone https://github.com/fstercq/freepybox.git
$ python setup.py install
```

Get started
-----------
```python
# Import the freepybox package.
from freepybox import Freepybox

# Instantiate the Freepybox class using default options.
fbx = Freepybox()

# Connect to the freebox with default options. 
# Be ready to authorize the application on the Freebox.
fbx.open('192.168.0.254')

# Do something usefull, rebooting your freebox for example.
fbx.system.reboot()

# Properly close the session.
fbx.close()
```
Have a look on the example.py for a more complete overview.

Resources
---------
Freebox OS API documentation : http://dev.freebox.fr/sdk/os/

