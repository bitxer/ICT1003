from pygatt import GATTToolBackend

from config import ALLOWED_MAC
from sensor import Sensor

def main():
    connected_sensors = []
    adapter = GATTToolBackend()
    try:
        adapter.start()
        for mac in ALLOWED_MAC:
            connected_sensors.append(Sensor(adapter, mac))
        input("Press enter to continue....\n")
    except KeyboardInterrupt:
        pass
    finally:
        adapter.stop()

if __name__ == '__main__':
    main()
