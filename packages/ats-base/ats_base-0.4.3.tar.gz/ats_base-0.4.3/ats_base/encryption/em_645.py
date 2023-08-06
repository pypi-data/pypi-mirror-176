"""
    645加密机
"""
import socket

from ats_base.base import entrance
from ats_base.common import func
from ats_base.config.configure import CONFIG

em_645 = entrance.api(CONFIG.get(func.ENCRYPTION, '645'))


class Client(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect(func.tcp_extract(em_645))

    def close(self):
        self.s.close()

    def send(self, command):
        self.connect()
        self.s.send(command.encode('utf-8'))
        result = self.s.recv(1024).decode('utf-8')
        self.s.close()
        return result


"""
    DLT645协议客户端调用接口
"""


def identify(meter_no: str):
    command = '301;0;0000{};'.format(meter_no)
    result = Client().send(command)
    ar = result.split(';')[1]
    rn = ar[:16]
    iv = ar[16:]

    return {'rn': rn, 'iv': iv}


"""
    DLT645协议服务端调用接口
"""


def encrypt(di: str, data, rn: str, iv: str):
    command = '306;0;{}{}{}{}{};'.format(rn.upper(), iv.upper(), _apdu(di), di, data.upper())
    result = Client().send(command)
    ar = result.split(';')[1]
    cipher = ar[:len(ar) - 8]
    mac = ar[len(ar) - 8:]

    return {'cipher': cipher, 'mac': mac}


def encrypt_reset(tag: str, data, rn: str, iv: str):
    command = '308;0;{}{}{}{};'.format(rn.upper(), iv.upper(), tag.upper(), data.upper())
    result = Client().send(command)
    ar = result.split(';')[1]
    cipher = ar[:len(ar) - 8]
    mac = ar[len(ar) - 8:]

    return {'cipher': cipher, 'mac': mac}


def _apdu(di: str):
    uch = int(di[2:4]) % 5

    if uch == 0:
        return "04D6880014"
    if uch == 1:
        return "04D6880014"
    if uch == 2:
        return "04D6880014"
    if uch == 3:
        return "04D6880014"
    if uch == 4:
        return "04D6880014"


