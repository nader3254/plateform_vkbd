# -*- encoding: utf-8 -*-
import threading
import time

import gtyTools.gtyTypes
import gtyTools.gtyLog
import SocketWorker
import traceback

from gtySocket import socketTools


class FeibotSocket:

    def __init__(self, eventQ):
        self.eventQ = eventQ

        # 配置的控制接口
        self.configHandlers = gtyTools.gtyTypes.ConfigHandlers()
        self.socketType = None
        self.targetIp = None
        self.targetPort = None
        self.localPort = None
        self.enRespond = None
        # socketWorker
        self.socketWorker = None

        # 事件驱动引擎
        self.eventEngine = threading.Thread(target=self.eventEngine)
        self.eventEngine.start()

        self.reloadConfigAndConnect()
        # 解包socket指令
        self.parseHandler = socketTools.ParseSocket()
        self.buildHandler = socketTools.SocketBuild()
        # 记录log
        gtyTools.gtyLog.log.write(__file__, 'start: ', self.socketType, self.targetIp, self.targetPort)

    # 重新加载
    def reloadConfigAndConnect(self):
        print(__file__, 'socket reconnect')
        self.configHandlers.machine.openConfigFile()
        self.socketType = self.configHandlers.machine.read('socket', 'type')
        self.targetIp = self.configHandlers.machine.read('socket', 'targetIp')
        self.targetPort = self.configHandlers.machine.read('socket', 'targetPort')
        self.localPort = self.configHandlers.machine.read('socket', 'localPort')
        self.enRespond = self.configHandlers.machine.read('socket', 'enRespond', 'int')

        # socketWorker
        try:
            self.socketWorker.disconnect()
        except:
            pass
        self.socketWorker = SocketWorker.SocketWorker(self.socketType, self.targetIp, self.targetPort, self.localPort)
        connectState = self.socketWorker.connect()
        self.configHandlers.state.write('machine', 'socketConnectState', connectState, 'bool')
        self.sendEvent('UI', 'ui_socketConnectedResult', connectState)

    def work(self):
        while True:
            time.sleep(0.01)
            try:
                if self.socketWorker.receive():
                    self.sendEvent('SOCKET', 'socket_receive', [])
            except Exception as e:
                print(e)
                print(__file__, 'socket run...')

    def eventEngine(self):
        while True:
            time.sleep(0.001)

            if 'SOCKET' not in self.eventQ.keys():
                continue

            if not self.eventQ['SOCKET'].empty():  # 事件队列非空
                try:
                    event = self.eventQ['SOCKET'].get(block=True, timeout=1)  # 获取队列中的事件 超时1秒
                    self.handleEventResult(event)
                except Exception as e:
                    traceback.extract_stack()
                    print(__file__, 'eventEngine error', e)
            else:
                pass

    # 发出事件
    def sendEvent(self, task, eventName, eventData=None):
        if eventData is None:
            eventData = []
        e = [eventName, eventData]
        try:
            if task.upper() in self.eventQ.keys():
                self.eventQ[task.upper()].put(e)
        except Exception as e:
            print(e)

    def handleEventResult(self, event):
        task = event[0]
        data = event[1]
        if task == 'socket_send':
            # if 'heartBeat' not in data:
            #     print(__file__, data)
            self.socketWorker.send(data)
            return
        if task == 'socket_receive':
            self.handleReceive()
            return
        if task == 'socket_connect':
            connectState = self.socketWorker.connect()
            self.configHandlers.state.write('machine', 'socketConnectState', connectState, 'bool')
            self.sendEvent('UI', 'ui_socketConnectedResult', connectState)
            return
        if task == 'socket_disconnect':
            connectState = self.socketWorker.disconnect()
            self.configHandlers.state.write('machine', 'socketConnectState', not connectState, 'bool')
            self.sendEvent('UI', 'ui_socketConnectedResult', not connectState)
            return
        if task == 'socket_reconnect':
            connectState = self.socketWorker.reconnect()
            self.configHandlers.state.write('machine', 'socketConnectState', connectState, 'bool')
            self.sendEvent('UI', 'ui_socketConnectedResult', connectState)
            return
        if task == 'socket_getConnectionState':
            self.socketWorker.getState()
            return
        if task == 'socket_loadConfigAndConnect':
            self.reloadConfigAndConnect()
            return

    # 处理接收
    def handleReceive(self):
        print(__file__, 'socket rx: ' + self.socketWorker.socketObj.rxBuf)
        socketCmds = self.socketWorker.socketObj.rxBuf.split(';')
        for socketCmd in socketCmds:
            res = self.parseHandler.parseSocket(socketCmd)
            if len(res) != 3:
                continue
            cmd = res[0]
            cmdId = res[1]
            data = res[2]
            d = data.split(',')
            if cmd:
                if cmd == 'readerOpen':  # 这里的参数是一个数组，['1',cmd]，这里cmd=on，开启，cmd=off，关闭，x不指定
                    self.sendEvent('UI', 'ui_startOrStropReading', [data, 'on'])
                    continue

                if cmd == 'readerStop': # 这里的参数是一个数组，['1',cmd]，这里cmd=on，开启，cmd=off，关闭，x不指定
                    self.sendEvent('UI', 'ui_startOrStropReading', [data, 'off'])
                    continue

                if cmd == 'setReaderPower':
                    self.sendEvent('UART', 'uart_setReaderPower', [int(d[0]) + 2, int(d[1])])  # 设置读卡功率
                    continue

                if cmd == 'setDate':
                    year = int(d[0]) if int(d[0]) < 2000 else int(d[0]) - 2000
                    self.sendEvent("UART", "uart_setDs3231Date", [year, d[1], d[2]])
                    continue

                if cmd == 'setTime':
                    self.sendEvent("UART", "uart_setDs3231Time", [int(d[0]), int(d[1]), int(d[2]), int(d[3])])
                    continue

                if cmd == 'packData':
                    continue

                if cmd == 'deleteData':
                    continue

                if cmd == 'setGateTime':
                    continue

                if cmd == 'packDataSection':
                    continue

                if cmd == 'getDate':
                    self.sendEvent("UI", "ui_socketGetDate", True)
                    continue

                if cmd == 'getTime':
                    print(__file__, 'get getTime')
                    self.sendEvent("UI", "ui_socketGetTime", True)
                    continue

                if cmd == 'getEpcData':
                    continue

                if cmd == 'getGunTime':
                    self.sendEvent("UI", "ui_socketGetGunTime", True)
                    continue

        if self.enRespond == 1:
            self.socketWorker.send(self.socketWorker.socketObj.rxBuf)
        self.socketWorker.socketObj.rxBuf = ''


def main(eventQ):
    while True:
        print("===================Socket task started===================")
        try:
            so = FeibotSocket(eventQ)
            so.work()
        except Exception as e:
            print(e)
            gtyTools.gtyLog.log.write(__file__, e, traceback.extract_stack())
