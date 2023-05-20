# -*- coding:utf-8 -*-


import sys
from PyQt5.QtWidgets import QDialog, QApplication

import gtyTools.tools
from uiFiles import ui_networkSetting
import time
from gtyConfig import language
from gtyTools import tools, gtyTypes
import uiTools


class NetworkSetting(QDialog, ui_networkSetting.Ui_networkSetting):

    def __init__(self, mainPage, eventQ, parent=None):
        super(NetworkSetting, self).__init__(parent)
        self.setupUi(self)
        uiTools.centerAndSetIcon(self)
        self.eventQ = eventQ

        self.mainPage = mainPage
        # 配置的控制接口
        self.configHandlers = gtyTypes.ConfigHandlers()
        self.connectState = self.configHandlers.state.read("machine","socketConnectState","bool")

        # language
        # 处理不同的语言
        self.setWindowTitle('Network Setting')
        self.label.setText(language.networkSetting_ipAddress)
        self.label_4.setText(language.networkSetting_udpTarget)
        self.label_2.setText(language.networkSetting_targetIp)
        self.label_3.setText(language.networkSetting_targetPort)
        self.btnSet.setText(language.networkSetting_set)
        self.btnBack.setText(language.networkSetting_back)
        if self.connectState:
            self.btnConnect.setText(language.networkSetting_connected)
        else:
            self.btnConnect.setText(language.networkSetting_disconnected)

        self.lineEditIp.setText(self.configHandlers.machine.read('socket', 'targetIp'))
        self.lineEditPort.setText(self.configHandlers.machine.read('socket', 'targetPort'))
        self.localPort = self.configHandlers.machine.read('socket', 'localPort')

        self.updateNetworkInfo()

        self.btnBack.clicked.connect(self.close)
        self.btnSet.clicked.connect(self.setTargetIp)
        self.btnConnect.clicked.connect(self.toggleConnect)

        self.mainPage.eventEngine.eventList["ui_socketConnectedResult"].connect(self.updateConnectBtn)

    def sendEvent(self, task, eventName, eventData=None):
        if eventData is None:
            eventData = []
        e = [eventName,  eventData]
        try:
            if task.upper() in self.eventQ.keys():
                self.eventQ[task.upper()].put(e)
        except Exception as e:
            print(e)

    def updateNetworkInfo(self):
        networkInfo = tools.GetNetworkInfo()
        networkState = ''
        networkState += "interface: " + networkInfo['Interface'] + ".   "
        networkState += "IP address: " + networkInfo['IP'] + ".\n"
        networkState += "local listening ip: " + self.localPort + '.   '
        networkState += "mask: " + networkInfo['MASK'] + ". \n"
        networkState += "gate way: " + networkInfo['GATEWAYS']
        self.textEditInfo.setText(networkState)

    def setTargetIp(self):
        ip = self.lineEditIp.text()
        port = self.lineEditPort.text()
        if gtyTools.tools.check_ip(ip) and 0 <= int(port) <= 65535:
            self.configHandlers.machine.write('socket', 'targetIp', ip)
            self.configHandlers.machine.write('socket', 'targetPort', port)
            self.sendEvent('SOCKET', 'socket_loadConfigAndConnect', '')
            self.labelInfo.setText("Set ip and port ok!")
        else:
            self.labelInfo.setText("Set ip or port wrong!")

    # 更新socket连接的结果
    def updateConnectBtn(self,res):
        if res:
            print(__file__,'connect: true')
            self.btnConnect.setText(language.networkSetting_connected)
        else:
            print(__file__,'connect: false')
            self.btnConnect.setText(language.networkSetting_disconnected)
        self.connectState = res

    # 按下连接按钮
    def toggleConnect(self):
        if self.connectState:
            self.sendEvent('SOCKET','socket_disconnect','')
        else:
            self.sendEvent('SOCKET','socket_connect','')
