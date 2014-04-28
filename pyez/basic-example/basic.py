'''
Do selective imports from Python Packages

from x import y #imports only the y package from the greater package set of x
'''
from pprint import pprint
from jnpr.junos import Device

'''
Create a new device object. This represents the SRX we are going to connect to.

The hostname/IP, username, and password are required.
'''
dev = Device(host='172.23.230.204', user='root', password='juniper123' )

'''
Creates a Netconf session to the SRX
'''
dev.open()

'''
Prints out the device facts in a pretty formated way
'''
pprint( dev.facts )

'''
Closes the netconf connection to the SRX
'''
dev.close()