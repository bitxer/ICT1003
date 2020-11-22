from struct import pack, unpack
from datetime import datetime
from os import path

from requests import post
import pygatt
from picamera import PiCamera

import config

class Data():
    '''Data object to be transmitted and recieved'''
    STRUCT_FORMAT = '>bbI14s'
    def __init__(self, actref, rsp, otp, ver=1, rev=1, data=None):
        try:
            self.len = len(data)
            self.data = data
        except TypeError:
            self.len = 0
            self.data = b''

        if self.len > 14:
            raise ValueError('Length of data is too long')

        if ver > 0xF:
            raise ValueError('Invalid Version Field')

        if rev > 0xF:
            raise ValueError('Invalid Revision Field')

        if actref > 0xFF:
            raise ValueError('Invalid Action Reference Field')

        if rsp > 0x1:
            raise ValueError('Invalid RSP Field')

        if otp > 0xFFFFFF:
            raise ValueError('Invalid OTP Field')

        self.ver = ver
        self.rev = rev
        self.actref = actref
        self.rsp = rsp
        self.otp = otp

    def pack(self):
        '''Pack the object and return a byte stream in big endian format'''
        ver_rev = (self.ver << 4) + self.rev
        rsp_len = (self.rsp << 7) + self.len
        rsp_len_otp = (rsp_len << 24) + self.otp
        if isinstance(self.data, str):
            self.data = self.data.encode()
        return pack(self.STRUCT_FORMAT, ver_rev, self.actref, rsp_len_otp, self.data)

    @classmethod
    def parse(cls, data):
        '''Parse data recieved using big endian'''
        if len(data) < 6:
            raise ValueError("Invalid data")
        ver_rev, actref, rsp_len_otp, data = unpack(cls.STRUCT_FORMAT, data)
        ver = (ver_rev & 0xF0) >> 4
        rev = ver_rev & 0x0F

        rsp = (rsp_len_otp & 0x80000000) >> 31
        clen = (rsp_len_otp & 0x7F000000) >> 24
        otp = rsp_len_otp & 0x00FFFFFF
        data = data.decode()
        cls(actref, rsp, otp, ver=ver, rev=rev, data=data)

    def __str__(self):
        return f"<Data ver={self.ver} ref={self.actref} rsp={self.rsp} len={self.len} otp={self.otp} data={self.data}>"


def detect():
    camera = PiCamera()
    now = str(int(datetime.now().timestamp()))
    filename = path.join(config.CAMERA_FOLDER, now) + '.jpg'
    camera.capture(filename)
    headers = {"X-APIKEY": config.ROOM_KEY}
    with open(filename, 'rb') as f:
        post(config.DETECTION_URL, headers=headers, data={'time': now}, files={'image': f})


def process(_, data):
    """
    _    -- integer, characteristic read handle the data was received on
    data -- bytearray, the data returned in the notification
    """
    data = Data.parse(data)
    print(data)

def main():
    adapter = pygatt.GATTToolBackend()
    try:
        adapter.start()
        device = adapter.connect('c5:2d:cc:32:65:34', address_type=pygatt.BLEAddressType.random, auto_reconnect=True)
        device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=process)
        input("Press enter to continue.....")
    except KeyboardInterrupt:
        pass
    finally:
        adapter.stop()

if __name__ == '__main__':
    main()
