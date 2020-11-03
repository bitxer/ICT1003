import pygatt
import time
#import binascii
from binascii import hexlify
Ble_Mac = "EE:FD:F4:4E:9D:FB"

adapter = pygatt.GATTToolBackend()

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))
    print(value)

try:
    adapter.start()
    try:
        device = adapter.connect(Ble_Mac,address_type=pygatt.BLEAddressType.random, timeout=20)
    except:
        print("Couldn't connect to the device, retrying...")
        device = adapter.connect(Ble_Mac,address_type=pygatt.BLEAddressType.random, timeout=20)
    print("Pairing with the device...")
    print("Connected with the device.")
    time.sleep(2)
    try:
        device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=handle_data)
    except Exception as e:
        try:
            device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=handle_data)
        except:
            pass

    input("Press Enter to continue...\n")


finally:
    adapter.stop()
