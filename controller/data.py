from struct import pack, unpack
from definitions import VERSION, REVISION

class Data():
    '''Data object to be transmitted and recieved'''
    STRUCT_FORMAT = '>bbI14s'
    HEADER_FORMAT = '>bbI'
    def __init__(self, actref, rsp, otp, ver=VERSION, rev=REVISION, data=None):
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
        header = data[:6]
        ver_rev, actref, rsp_len_otp = unpack(cls.HEADER_FORMAT, header)
        ver = (ver_rev & 0xF0) >> 4
        rev = ver_rev & 0x0F

        rsp = (rsp_len_otp & 0x80000000) >> 31
        clen = (rsp_len_otp & 0x7F000000) >> 24
        otp = rsp_len_otp & 0x00FFFFFF
        try:
            data = data[6:].decode()
        except AttributeError:
            return None

        if len(data) != clen:
            return None

        return cls(actref, rsp, otp, ver=ver, rev=rev, data=data)

    def __str__(self):
        return f"<Data ver={self.ver} rev={self.rev} ref={self.actref} rsp={self.rsp} len={self.len} otp={self.otp} data={self.data}>"
