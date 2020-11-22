from os import path
from datetime import datetime
from requests import post
from pygatt import BLEAddressType
from picamera import PiCamera
from picamera.exc import PiCameraMMALError

from definitions import SYNC, OPEN, CLOSE
from data import Data
from config import CAMERA_FOLDER, ROOM_KEY, DETECTION_URL

class Sensor:
    def __init__(self,adapter, mac):
        self.mac = mac
        self.message_id = 0
        self.device = adapter.connect(mac, address_type=BLEAddressType.random, auto_reconnect=True)
        self.device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=self.process)

    def process(self, _, data):
        """
        _    -- integer, characteristic read handle the data was received on
        data -- bytearray, the data returned in the notification
        """
        data = Data.parse(data)
        print(data)
        if data.actref == OPEN:
            self.detect()
        elif data.actref == CLOSE:
            pass
        elif data.actref == SYNC:
            self.sync(data)

    def detect(self):
        now = str(int(datetime.now().timestamp()))
        filename = path.join(CAMERA_FOLDER, now) + '.jpg'
        try:
            camera = PiCamera()
            camera.capture(filename)
        except PiCameraMMALError:
            return
        finally:
            camera.close()
        headers = {"X-APIKEY": ROOM_KEY}
        with open(filename, 'rb') as f:
            post(DETECTION_URL, headers=headers, data={'time': now}, files={'image': f})

    def sync(self, data):
        self.message_id = data.msg_id
