from time import sleep
from pygatt import GATTToolBackend
from pygatt.exceptions import NotConnectedError

from config import ALLOWED_MAC
from sensor import Sensor

def main():
    available_sensors = []
    connected_sensors = []
    adapter = GATTToolBackend()
    # Scan surroundings
    for device in adapter.scan():
        if device['address'] in ALLOWED_MAC:
            available_sensors.append(device['address'])
    try:
        adapter.start()
        for mac in available_sensors:
            try:
                connected_sensors.append(Sensor(adapter, mac))
            except NotConnectedError:
                continue
        print('Use CTRL-C to stop the current execution')
        while True:
            sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        pass
    finally:
        adapter.stop()

if __name__ == '__main__':
    main()
