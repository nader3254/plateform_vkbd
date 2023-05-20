import socket


class Udp:
    def __init__(self, targetIp, targetPort, localPort):
        self.target = (targetIp, int(targetPort))
        self.localPort = int(localPort)
        self.socket_rx = None
        self.socket_tx = None
        self.rxBuf = ''
        self.connectState = False

    def send(self, data):
        if self.connectState:
            try:
                self.socket_tx.sendto(bytes(data, encoding='utf-8'), self.target)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    def receive(self):
        if self.connectState:
            try:
                receive_data, client = self.socket_rx.recvfrom(10240)
                self.rxBuf += str(receive_data, encoding='utf-8')
                return True
            except socket.timeout:  # 如果10秒钟没有接收数据进行提示（打印 "time out"）
                return False
        else:
            return False

    def connect(self):
        try:
            self.socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket_rx.bind(("", self.localPort))
            self.socket_rx.settimeout(0.2)
            self.socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.connectState = True
            return True
        except Exception as e:
            self.connectState = False
            print(e)
            return False

    def disconnect(self):
        try:
            self.socket_rx = None
            self.socket_tx = None
            self.connectState = False
            return True
        except Exception as e:
            print(e)
            return False

    def reconnect(self):
        try:
            self.disconnect()
            self.connect()
            return True
        except Exception as e:
            print(e)
            return False

    def getState(self):
        return True
