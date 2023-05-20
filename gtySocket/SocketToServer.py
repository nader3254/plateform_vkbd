# -*- encoding: utf-8 -*-
import random
import threading
import time

import gtyTools.gtyTypes
import gtyTools.gtyLog
import SocketWorker
import traceback
import os

from gtyIO import gtyIoTools
import json
from gtyTools import tools


class SocketToServer:

    def __init__(self, eventQ):
        self.eventQ = eventQ

        # 配置的控制接口
        self.configHandlers = gtyTools.gtyTypes.ConfigHandlers()
        self.socketType = None
        self.targetIp = None
        self.targetPort = None
        self.localPort = None
        self.enRespond = None
        self.socketWorker = None

        # 看是否需要运行
        self.en = self.configHandlers.machine.read("socketToServer","enable")

        if self.en == "1":
            # self.machineId = tools.getMachineId(self.configHandlers.mmc.read("machine", "machineId"))
            self.machineId = self.configHandlers.machine.read("machine", "machineId")
            self.md5String = os.environ.get("platform4_md5String")
            # 事件驱动引擎
            self.eventEngine = threading.Thread(target=self.eventEngine)
            self.eventEngine.start()

            self.reloadConfigAndConnect()
            # 待传发送的tag数据列表
            self.tagList = []
            # 记录log
            gtyTools.gtyLog.log.write(__file__, 'start: ', self.socketType, self.targetIp, self.targetPort)
        else:
            print(__file__,"socket to server is not enabled!")

    # 重新加载
    def reloadConfigAndConnect(self):
        print(__file__, 'socket server reconnect')
        self.configHandlers.machine.openConfigFile()
        self.socketType = self.configHandlers.machine.read('socketToServer', 'type', "string",os.environ.get("platform4_socketServerType"))
        self.targetIp = self.configHandlers.machine.read('socketToServer', 'targetIp', "string",os.environ.get("platform4_socketServerIp"))
        self.targetPort = self.configHandlers.machine.read('socketToServer', 'targetPort', "string",os.environ.get("platform4_socketServerPort"))
        self.localPort = self.configHandlers.machine.read('socketToServer', 'localPort')
        print(__file__,self.socketType,self.targetIp,self.targetPort,self.localPort)
        try:
            self.socketWorker.disconnect()
        except Exception as e:
            print(e)
        self.socketWorker = SocketWorker.SocketWorker(self.socketType, self.targetIp, self.targetPort, self.localPort)
        connectState = self.socketWorker.connect()
        self.configHandlers.state.write('machine', 'socketServerConnectState', connectState, 'bool')

    def work(self):
        while True:
            time.sleep(0.005)
            if self.en == "1":
                try:
                    if len(self.tagList) > 0:
                        tag = self.tagList.pop()
                        self.socketWorker.send(self.buildTagJson(tag))
                except Exception as e:
                    print(__file__,e)

    def eventEngine(self):
        while True:
            time.sleep(0.001)
            if 'SOCKET_SERVER' not in self.eventQ.keys():
                continue
            if not self.eventQ['SOCKET_SERVER'].empty():  # 事件队列非空
                try:
                    event = self.eventQ['SOCKET_SERVER'].get(block=True, timeout=1)  # 获取队列中的事件 超时1秒
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
        e = [eventName,  eventData]
        try:
            if task.upper() in self.eventQ.keys():
                self.eventQ[task.upper()].put(e)
        except Exception as e:
            print(e)

    def handleEventResult(self, event):
        task = event[0]
        data = event[1]
        if task == 'add_tag':
            self.tagList.extend(data)
            return
        if task == 'socket_send':
            self.socketWorker.send(data)
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

    def buildTagJson(self, tag):
        t = self.md5String + str(random.randint(10000000, 99999999))
        info = {
            "epc": tag.epcString,
            "time": tag.hardwareTimeString,
            "date":tag.hardwareDateString,
            "mId": self.machineId,
            "t": str(random.randint(10000000, 99999999)),
            "sign": gtyIoTools.get_token(t,self.md5String)[0:10]
        }
        res = json.dumps(info)
        return res


def main(eventQ):
    while True:
        print("===================Socket to Server task started===================")
        try:
            so = SocketToServer(eventQ)
            so.work()
        except Exception as e:
            print(e)
            gtyTools.gtyLog.log.write(__file__, e, traceback.extract_stack())
