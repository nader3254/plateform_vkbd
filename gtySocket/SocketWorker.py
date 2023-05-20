import socket
import time

import udp
from gtyTools import gtyLog


class SocketWorker:
    def __init__(self, socketType, targetIp, targetPort, localPort):
        self.socketObj = None
        if str(socketType).lower() == 'udp':
            gtyLog.log.write(__file__, 'socket start with udp')
            self.socketObj = udp.Udp(targetIp, targetPort, localPort)

    def send(self, data):
        return self.socketObj.send(data)

    def receive(self):
        return self.socketObj.receive()

    def connect(self):
        return self.socketObj.connect()

    def disconnect(self):
        return self.socketObj.disconnect()

    def reconnect(self):
        return self.socketObj.reconnect()

    def getState(self):
        return self.socketObj.getState()
