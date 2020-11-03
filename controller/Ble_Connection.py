import pygatt
import time
#import binascii
from binascii import hexlify

adapter = pygatt.GATTToolBackend()

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

try:
    adapter.start()
    device = adapter.connect('EE:FD:F4:4E:9D:FB', address_type=pygatt.BLEAddressType.random)
    time.sleep(2)
    print ("subscribing")
    #for uuid in device.discover_characteristics().keys():
        #print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))
    device.subscribe("6e400001-b5a3-f393-e0a9-e50e24dcca9e", callback=handle_data, indication=True)


finally:
    adapter.stop()