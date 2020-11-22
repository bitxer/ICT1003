from struct import pack, unpack
from definitions import VERSION, REVISION

class Data():
    '''Data object to be transmitted and recieved'''
    STRUCT_FORMAT = '>bbI'
    def __init__(self, actref, msg_id, ver=VERSION, rev=REVISION):
        if ver > 0xF:
            raise ValueError('Invalid Version Field')

        if rev > 0xF:
            raise ValueError('Invalid Revision Field')

        if actref > 0xFF:
            raise ValueError('Invalid Action Reference Field')

        if msg_id > 0xFFFFFFFF:
            raise ValueError('Invalid OTP Field')

        self.ver = ver
        self.rev = rev
        self.actref = actref
        self.msg_id = msg_id

    def pack(self):
        '''Pack the object and return a byte stream in big endian format'''
        ver_rev = (self.ver << 4) + self.rev
        return pack(self.STRUCT_FORMAT, ver_rev, self.actref, self.msg_id)

    @classmethod
    def parse(cls, data):
        '''Parse data recieved using big endian'''
        header = data[:6]
        ver_rev, actref, msg_id = unpack(cls.STRUCT_FORMAT, header)
        ver = (ver_rev & 0xF0) >> 4
        rev = ver_rev & 0x0F

        try:
            data = data[6:].decode()
        except AttributeError:
            return None

        return cls(actref, msg_id, ver=ver, rev=rev)

    def __str__(self):
        return f"<Data ver={self.ver} rev={self.rev} ref={self.actref} msg_id={self.msg_id}>"
