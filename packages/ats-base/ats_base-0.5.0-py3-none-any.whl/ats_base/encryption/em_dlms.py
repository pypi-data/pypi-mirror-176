"""
    DLMS加密机
"""
import socket

from ats_base.base import entrance
from ats_base.common import func
from ats_base.config.configure import CONFIG

em_dlms = entrance.api(CONFIG.get(func.ENCRYPTION, 'dlms'))


class Client(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect(func.tcp_extract(em_dlms))

    def close(self):
        self.s.close()

    def send(self, command):
        self.connect()
        self.s.send(command.encode('utf-8'))
        result = self.s.recv(1024).decode('utf-8')
        self.s.close()
        return result


