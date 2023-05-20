# -*- coding:utf-8 -*-

# 升级固件的对象
class FirmwareUpdateManager:

    # gty:构造函数
    def __init__(self):
        self._binFileName = ''  # gty：固件文件名
        self._binFileDataList = []  # gty：固件文件数据字节列表
        self._duringStm32FirmwareUpdate = False
        self._currentSendingPackNumber = -1  # 当前需要传送给stm32的固件包的包号
        self._firmwareLength = -1  # 固件包的总字节数
        self._packAmount = -1  # 固件包的总包数
        self._eachPackLength = 240  # 每一包的字节数
        self.lastCurrentSendingPackNumber = -1  # 上一步的暂存值

    # 重置变量
    def reset(self):
        self._binFileName = ''
        self._binFileDataList = []
        self._duringStm32FirmwareUpdate = False
        self._currentSendingPackNumber = -1
        self._firmwareLength = -1
        self._packAmount = -1
        self._eachPackLength = 240
        self.lastCurrentSendingPackNumber = -1

    # 读取固件文件
    def readBinFile(self, firmwareFileName):
        self._binFileName = firmwareFileName  # 对二进制文件名进行赋值
        fh = open(firmwareFileName, 'rb')
        a = fh.read()

        # 获取固件文件字节列表
        self._binFileDataList = str2list(a)
        print(__file__,"binFileDataList:",self._binFileDataList)
        # 获取固件字节数
        self._firmwareLength = len(self._binFileDataList)

        # 获取固件包个数
        if self._firmwareLength % self._eachPackLength == 0:
            self._packAmount = self._firmwareLength // self._eachPackLength
        else:
            self._packAmount = self._firmwareLength // self._eachPackLength + 1

        print(__file__,"packAmount:",self._packAmount)

    # 构建固件包字符串，包号由自己的变量决定
    def buildPack(self, packNum):
        self._currentSendingPackNumber = packNum
        if self._firmwareLength > 0:  # 固件文件读取完成
            thisPack = [0xfe, self._currentSendingPackNumber % 250, self._currentSendingPackNumber // 250,(self._eachPackLength + 6) % 250]
            for i in range(0, self._eachPackLength):
                position = (self._currentSendingPackNumber - 1) * self._eachPackLength + i
                if position < self._firmwareLength:
                    thisPack.append(self._binFileDataList[position])
                else:
                    thisPack.append(0xff)
            summation = sum(thisPack) % 250
            thisPack.append(summation)
            thisPack.append(0xfc)
            print(__file__,"thisPack:",thisPack)
            return thisPack

    # 解码串口数据包并返回当前stm32正在索要的固件包的包号
    '''
    gty
    # 输入：串口数据包
    # 输出：是否在读取固件，当前需要发送的固件包序号'''

    def decode(self, getDataList):
        if self._duringStm32FirmwareUpdate is True:
            len_list = len(getDataList)
            if len_list >= 6:
                j = 0
                for ele in getDataList:
                    if ele == 0x7e:
                        if len_list - j >= 6:
                            if getDataList[j + 4] == 0x0d and getDataList[j + 5] == 0x0a:
                                everyElementNotLessThan35 = True
                                for i in range(1, 4):
                                    if getDataList[j + i] < 35:
                                        everyElementNotLessThan35 = False
                                        break
                                if everyElementNotLessThan35 is True:
                                    newList = [0x7e]
                                    for i in range(1, 4):
                                        newList.append(getDataList[j + i] - 35)
                                    summation = (sum(newList) - newList[3]) % 91
                                    if summation == newList[3]:
                                        self.lastCurrentSendingPackNumber = self._currentSendingPackNumber
                                        _currentSendingPackNumber = newList[2] * 91 + newList[1]
                                        return True, _currentSendingPackNumber
                    j += 1
        return False, -1

    def updatePercentage(self):
        return self._currentSendingPackNumber * 100.0 / self._packAmount


def str2list(string):
    getList = []
    for i in string:
        getList.append(i)
    return getList


if __name__ == "__main__":
    f = FirmwareUpdateManager()
    f.readBinFile('plateform.bin')
