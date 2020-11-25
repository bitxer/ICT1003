from pygatt import GATTToolBackend
from pygatt.exceptions import NotConnectedError

from config import ALLOWED_MAC
from sensor import Sensor

def main():
    connected_sensors = []
    adapter = GATTToolBackend()
    try:
        adapter.start()
        for mac in ALLOWED_MAC:
            try:
                connected_sensors.append(Sensor(adapter, mac))
            except NotConnectedError:
                continue
        input("Press enter to continue....\n")
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        adapter.stop()

if __name__ == '__main__':
    main()
