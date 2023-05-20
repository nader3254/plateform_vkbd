# -*- coding:utf-8 -*-
import traceback

from gtyConfig import configFileHandler, systemConfig
from gtyTools import gtyTypes, gtyLog


# 协议
class GtySerialProtocol:
    def __init__(self):
        # 这里的内部缓冲区是数字列表
        self.buf = []
        self.getEndFlag = False
        self.bufLen = 0
        self.packLen = 0
        self.lastEpcPack = []  # 上一次收到的epc码数据包
        self.epcPackNum = 0
        self.epcNum = 0  # 收到的epc码的个数
        self.epcFirstPackUsedNum = 0  # 从第二个包获取EPC码的包数

        self.machineConfig = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)
        self.allowEpcByteLength = self.machineConfig.read("reader", "allowEpcByteLength")

        self.unpackBuf = []

    # 用于解数据包到标准格式
    # 返回值：指令编码，数据长度，数据包
    def unpack(self, c):
        self.unpackBuf.append(c)
        for head in range(0, len(self.unpackBuf)):
            try:
                if not self.unpackBuf[head] == 0xfe:
                    continue
                packLen = self.unpackBuf[head + 1]
                cmdId = self.unpackBuf[head + 2]
                checkSumH = self.unpackBuf[head + packLen - 1 - 1]
                checkSumL = self.unpackBuf[head + packLen - 1]
                checkSum = sum(self.unpackBuf[head:head + packLen - 1 - 1])
                if checkSum // 250 == checkSumH and checkSum % 250 == checkSumL:
                    data = self.unpackBuf[head + 3:head + packLen - 2]
                    del self.unpackBuf[:]
                    return cmdId, packLen, data
                else:
                    if len(self.unpackBuf) > 200:
                        gtyLog.log.write(__file__, "uart buf > 200", self.unpackBuf)
                        del self.unpackBuf[:]
                        break
            except:
                continue
        return -1, 0, []

    # 解析从stm32发送到linux的协议包
    # 返回：flag，dataId，data
    def decode(self, c):
        try:
            dataId, dataLen, data = self.unpack(c)
        except Exception as e:
            gtyLog.log.write(__file__, "decode uart data wrong...", e, traceback.extract_stack())
            return False, '', []
        if dataId == -1:
            return False, '', []
        if dataId == 0x0:
            return False, '', []
        # 新的可变长度的EPC数据
        if dataId == 0x27:
            return True,'tagFlexible', unpackEpc(data)
        if dataId == 0x1:
            return True, 'heartBeat', data
        if dataId == 0x3:
            return True, 'date', data
        if dataId == 0x4:
            return True, 'time', data
        if dataId == 0x5:
            return True, 'bat', (data[0] * 250 + data[1]) / 100.0
        if dataId == 0x6:
            return True, 'channelState', data
        if dataId == 0x09:
            return True, 'firmwareVersion', data
        if dataId == 0x0b:
            return True, 'setTimeByAir', data  # self.buf[3]累加器数值，self.buf[4]收发：1发送，0接收
        if dataId == 0x0c:
            return True, 'buttonPressed', ''  # 按钮按下
        if dataId == 0x0d:
            return True, 'buttonPressedShort', data  # 按钮短按
        if dataId == 0x0e:
            return True, 'buttonPressedLong', data  # 按钮长按
        if dataId == 0x13:
            return True, 'chSettingResponse', data  # 通道设置状态
        if dataId == 0x14:  # 测试卡读到的次数
            return True, 'testTagReadTimes', data
        if dataId == 0x15:
            return True, 'stm32Boot', 'boot'
        if dataId == 0x18:
            if data == [0xde, 0xad, 0xbe, 0xef]:
                return True, 'stm32Cmd', ['shut down']
            if data == [0xa1, 0xb2, 0xc3, 0xd4]:
                return True, 'stm32Cmd', ['reboot']
        if dataId == 0x1a:
            return True, 'getReaderPower', data
        if dataId == 0x1e:
            print(__file__,'get band',data)
            return True,'getFreqBand',data
        return False, '', []


# 按可变长度的方式解包EPC数据，并以标签
def unpackEpc(data):
    try:
        # 获取标签时间
        t = gtyTypes.hardwareTime()
        t.setValues(data[0]+2000, data[1], data[2], data[3], data[4], data[5], data[6] * 250 + data[7])
        # 获取标签EPC列表
        tagLen = data[8]*256 + data[9]
        # 读出芯片数据
        tagList = []
        tag = gtyTypes.tag()
        tag.hardwareTime = t
        tag.epcByteNum = tagLen
        tag.epcByteList = data[10:10 + tagLen]
        tag.channelId = data[10+tagLen]
        tag.rssi = data[11+tagLen]

        tag.buildTimeStamp()
        tag.buildEpcString()

        tagList.append(tag)
        return tagList
    except Exception as e:
        print(e)
        return []


# 构建命令函数
# cmdType 字符串，指令类型
# cmdData 列表，指令参数数组
def buildCmd(cmdType, cmdData=None):
    # print(__file__, 'get stm32 cmd: ',cmdType, cmdData)
    rawPackList = [0xfe]
    if cmdType == 'heartBeat':
        rawPackList = [0xfe, 0x05, 0x01]
        return calCheckSum(rawPackList)
    if cmdType == 'startReadEpc':
        rawPackList = [0xfe, 0x06, 0x02, cmdData[0]]
        return calCheckSum(rawPackList)
    if cmdType == 'stopReadEpc':
        rawPackList = [0xfe, 0x06, 0x03, cmdData[0]]
        return calCheckSum(rawPackList)
    if cmdType == 'setPower':
        rawPackList = [0xfe, 0x08, 0x04, 1, cmdData[0], cmdData[1]]
        return calCheckSum(rawPackList)
    if cmdType == 'getReaderPower':
        rawPackList = [0xfe, 0x08, 0x04, 0, cmdData, 0]  #
        return calCheckSum(rawPackList)
    if cmdType == 'beep':
        rawPackList = [0xfe, 0x06, 0x05, cmdData[0]]
        return calCheckSum(rawPackList)
    if cmdType == 'setTime':
        rawPackList = [0xfe, 0x09, 0x06, cmdData[0], cmdData[1], cmdData[2], cmdData[3]]
        return calCheckSum(rawPackList)
    if cmdType == 'setDate':
        rawPackList = [0xfe, 0x08, 0x07, cmdData[0], cmdData[1], cmdData[2]]
        return calCheckSum(rawPackList)
    if cmdType == 'askFirmwareVersion':  # 询问固件版本号
        rawPackList = [0xfe, 0x05, 0x09]
        return calCheckSum(rawPackList)
    if cmdType == 'shutDown':  # 关闭继电器
        rawPackList = [0xfe, 0x05, 0x0b]
        return calCheckSum(rawPackList)
    if cmdType == 'setTimeByAir':  # 通过数据链设置系统时间
        rawPackList = [0xfe, 0x05, 0x0c]
        return calCheckSum(rawPackList)
    if cmdType == 'reboot':  # 重启时静止蜂鸣器长鸣
        rawPackList = [0xfe, 0x05, 0x0d]
        return calCheckSum(rawPackList)
    if cmdType == 'updateStm32Firmware':  # stm32固件升级
        rawPackList = [0xfe, 0x05, 0x0e]
        return calCheckSum(rawPackList)
    if cmdType == 'chControl':  # 通道设置
        rawPackList = [0xfe, 0x08, 0x10, cmdData[0], cmdData[1], cmdData[2]]
        return calCheckSum(rawPackList)
    if cmdType == 'fanControl':  # 设置风扇开关
        if cmdData == 'on':
            rawPackList = [0xfe, 0x06, 0x12, 0]
        if cmdData == 'off':
            rawPackList = [0xfe, 0x06, 0x12, 1]
        return calCheckSum(rawPackList)
    if cmdType == 'reBootReader':  # 重启读卡器
        rawPackList = [0xfe, 0x06, 0x13, cmdData[0] + 2]
        return calCheckSum(rawPackList)
    if cmdType == 'releaseMode':  # 设置启动模式
        print(cmdData)
        if 'debug' in cmdData:
            rawPackList = [0xfe, 0x06, 0x15, 1]
        if 'release' in cmdData:
            rawPackList = [0xfe, 0x06, 0x15, 0]
        return calCheckSum(rawPackList)
    if cmdType == 'FreqBand':  # 设置读卡频率
        print(__file__,'freq band',cmdData)
        rawPackList = [0xfe, 0x07, 0x19, cmdData[0],cmdData[1]]
        return calCheckSum(rawPackList)
    return []


# 计算和校验值并转字符串
def calCheckSum(data):
    try:
        if max(data) > 255:
            gtyLog.log.write(__file__,'uart send byte error, larger than 255')
            return []
        s = sum(data)
        res = data
        res.append(int(s / 250 % 250))
        res.append(int(s % 250))
        return res
    except Exception as e:
        print(e)
        print("serial calCheckSumAndTurnString failed...")
        return []


# 字节转16进制数字
def getHex(i):
    if i in '1234567890':
        return int(i)
    if i in 'aA':
        return 10
    if i in 'bB':
        return 11
    if i in 'cC':
        return 12
    if i in 'dD':
        return 13
    if i in 'eE':
        return 14
    if i in 'fF':
        return 15


# 按16进制打印缓冲区
def printInHex(buf):
    text = ""
    for i in list(buf):
        text += "%02X " % i
    print(text)
    pass


# 一些工具方法
def str2list(string):
    getList = []
    for i in string:
        getList.append(i)
    return getList
