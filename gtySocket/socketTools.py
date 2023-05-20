# -*- encoding: utf-8 -*-
import traceback

import gtyConfig.systemConfig
from gtyTools import tools


# 读取本地的ip，mask，gateway
def GetNetworkInfo():
    NetworkDict = {'IP': '', 'MASK': '', 'GATEWAYS': ''}
    try:
        import netifaces
        routingGateway = netifaces.gateways()[2][0][0]  # 网关
        # print __file__,'interface:',netifaces.interfaces()

        interface = getInterfaces()
        # try:
        routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']  # 获取IP
        routingMusk = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
        # except KeyError:
        # pass

        NetworkDict['IP'] = routingIPAddr
        NetworkDict['MASK'] = routingMusk
        NetworkDict['GATEWAYS'] = routingGateway
        return NetworkDict
    except Exception as e:
        print(e)
        import netifaces
        routingGateway = netifaces.gateways()[2][0][0]  # 网关
        try:

            interface = 'wlan0'
            # try:
            routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']  # 获取IP
            routingMusk = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            # except KeyError:
            # pass

            NetworkDict['IP'] = routingIPAddr
            NetworkDict['MASK'] = routingMusk
            NetworkDict['GATEWAYS'] = routingGateway
            return NetworkDict
        except:
            return 'failed'


# 从列表中获取需要的网卡号，如果有有线链接，那么返回有线链接。如果没有有线链接，返回无线链接。
def getInterfaces():
    try:
        import netifaces
        interfaceList = netifaces.interfaces()
        for i in interfaceList:
            if i != 'wlan0' and len(i) > 8:
                return i
        return 'wlan0'
    except:
        return 'wlan0'


# F800->PC的数据包构建
from gtyConfig import configFileHandler


# 打包socket指令
class SocketBuild:
    def __init__(self):
        # self.machineConfig = configFileHandler.ConfigFileHandler(gtyConfig.systemConfig.configFileEmmc)
        self.machineConfig = configFileHandler.ConfigFileHandler(gtyConfig.systemConfig.machineConfigFilePath)
        # self.machineId = tools.getMachineId(self.machineConfig.read('machine', 'machineId'))
        self.machineId = self.machineConfig.read('machine', 'machineId')
        self.cmdId = 0

    def buildSocket(self, cmd, data):
        res = self.machineId + '@' + cmd + '@' + str(self.cmdId) + '@' + data + ';'
        self.cmdId += 1
        if self.cmdId >= 10000:
            self.cmdId = 0
        return res


# 解析socket指令
class ParseSocket:
    def __init__(self):
        self.machineConfig = configFileHandler.ConfigFileHandler(gtyConfig.systemConfig.configFileEmmc)
        # self.machineId = tools.getMachineId(self.machineConfig.read('machine', 'machineId'))
        self.machineId = self.machineConfig.read('machine', 'machineId')

    def parseSocket(self, data):
        try:
            if "@" not in data:
                return [False,"",""]
            data = data.replace(';', '')
            if data[-1] == "@":
                data += "x"
            dataList = str(data).split('@')
            machineId = dataList[0]
            cmd = dataList[1]
            cmdId = dataList[2]
            d = dataList[3]
            if machineId.upper() == self.machineId.upper():
                return [cmd, cmdId, d]
            else:
                return [False, '', '']
        except Exception as e:
            traceback.extract_stack()
            print(e)
            return [False, '', '']
