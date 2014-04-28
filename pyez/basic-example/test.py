from pprint import pprint
from jnpr.junos import Device

dev = Device(host='10.0.1.161', user='root', password='PiZZ@!@#!@#' )
dev.open()

pprint( dev.facts )

dev.close()
