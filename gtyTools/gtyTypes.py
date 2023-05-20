# -*- coding: utf-8 -*-
from gtyConfig import systemConfig, configFileHandler


# 精确到ms的时间父类
class timeInMs:
    def __init__(self, year=1, month=1, day=1, hour=0, minute=0, second=0, ms=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.ms = ms

    def setValues(self, year=1, month=1, day=1, hour=0, minute=0, second=0, ms=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.ms = ms


class hardwareTime(timeInMs):
    def __init__(self):
        super().__init__()


class linuxTime(timeInMs):
    def __init__(self):
        super().__init__()
        self.secondCounter = 0


class Channel:
    def __init__(self):
        self.open = 0
        self.tagReadNum = 0
        self.testTagReadNum = 0
        self.chBtn = None

    def resetNum(self):
        self.tagReadNum = 0
        self.testTagReadNum = 0


class Channels:
    def __init__(self):
        self.ch1 = Channel()
        self.ch2 = Channel()
        self.ch3 = Channel()
        self.ch4 = Channel()
        self.ch5 = Channel()
        self.ch6 = Channel()
        self.ch7 = Channel()
        self.ch8 = Channel()
        self.chs = [self.ch1, self.ch2, self.ch3, self.ch4, self.ch5, self.ch6, self.ch7, self.ch8]
        self.testNumDisplayTilSecond = 0  # 运行的秒数
        self.displayChannelNames = True

    def setBtns(self, btnList):
        self.ch1.chBtn = btnList[0]
        self.ch2.chBtn = btnList[1]
        self.ch3.chBtn = btnList[2]
        self.ch4.chBtn = btnList[3]
        self.ch5.chBtn = btnList[4]
        self.ch6.chBtn = btnList[5]
        self.ch7.chBtn = btnList[6]
        self.ch8.chBtn = btnList[7]

    def resetNum(self):
        for i in range(0, 8):
            self.chs[i].resetNum()
        self.testNumDisplayTilSecond = 0  # linux整数秒计数小于这个时间时，显示测试卡信息
        self.displayChannelNames = True


class ConfigHandlers:
    def __init__(self):
        self.machine = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)
        self.state = configFileHandler.ConfigFileHandler(systemConfig.runStateFilePath)
        self.event = configFileHandler.ConfigFileHandler(systemConfig.getEventConfigFilePath())


class tagDataSummary:
    def __init__(self):
        self.totalCheckedNum = 0
        self.differentCheckedNum = 0
        self.checkedTagDict = {}

    def reset(self):
        self.totalCheckedNum = 0
        self.differentCheckedNum = 0
        self.checkedTagDict = {}


class tag:
    def __init__(self):
        self.epcString = ""
        self.epcByteList = []

        self.epcByteNum = 0

        self.hardwareTime = hardwareTime()
        self.hardwareTimeString = ""
        self.hardwareDateString = ""
        self.timeStamp = 0

        self.channelId = 0
        self.rssi = None

    def buildEpcString(self):
        self.epcString = ""
        for i in self.epcByteList:
            self.epcString += '%02x' % i

    def buildTimeStamp(self):
        self.timeStamp = self.hardwareTime.hour * 3600 + self.hardwareTime.minute * 60 + \
                         self.hardwareTime.second + self.hardwareTime.ms / 1000

    def buildTimeString(self):
        self.hardwareTimeString = '%02d:%02d:%02d.%03d' % \
                                  (self.hardwareTime.hour,
                                   self.hardwareTime.minute,
                                   self.hardwareTime.second,
                                   self.hardwareTime.ms)
        self.hardwareDateString = "%04d-%02d-%02d" % (
            self.hardwareTime.year,
            self.hardwareTime.month,
            self.hardwareTime.day)


class machineState:
    def __init__(self):
        self.machineId = ''
        self.eventId = ''
        self.internetConnectionState = 'disconnected'  # 分为《已联网》和《未联网》两种状态

        self.batteryPercentage = -1  # 为一个整数

        self.gunStartTime = None

        self.readerState1 = 'stopped'  # 读写器1状态，分为《正在读取》和《停止读取》两种状态
        self.readerState2 = 'stopped'  # 读写器2状态，分为《正在读取》和《停止读取》两种状态
        self.readerFreqBand = 0

        self.textBrowserLineNum = 0  # log输出的行数

        # 磁盘可用容量
        self.storageSpace = ''
        self.storageSpaceUnusedG = 0

        # 软件升级提示
        self.updateNotice = ''

        # 提示栏显示
        self.noticeLabelDict = {}

        # 门槛时间
        self.gateTime = 0

        # 允许的epc长度
        self.allowEpcByteNumList = []


class auxiliaryVariables:
    def __init__(self):
        self.gunShowColon = True
        self.counterPer100ms = 0

        self.getFirmwareFlag = 0
        self.rawEpcNum = 0