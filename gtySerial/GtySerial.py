# -*- coding:utf-8 -*-
import serial
import sys
import os
import time
import threading
import traceback

for d in ['gtyConfig', 'gtyIO', 'gtySerial', 'gtySocket', 'gtyTools', 'gtyUI']:
    module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), d)
    sys.path.append(module_path)  # 导入的绝对路径

from gtySerial import gtySerialProtocol, firmwareUpdateManager
import gtyTools.gtyTypes
from gtyTools import gtyLog, tools


class GtySerial:
    def __init__(self, eventQ):
        # 配置的控制接口
        self.configHandlers = gtyTools.gtyTypes.ConfigHandlers()

        self.getBuf = []
        self.getBufCopy = []
        self.sendBuf = []
        self.eventQ = eventQ

        self.localEventEngine = None

        # 启动事件引擎
        self.localEventEngine = threading.Thread(target=self.eventEngine)
        self.localEventEngine.start()

        # 一些计数器
        self.receiveHeartBeatCounter = 5  # 接受的串口心跳包计数器，从5开始倒计数

        # 升级固件对象
        self.firmwareUpdater = firmwareUpdateManager.FirmwareUpdateManager()

        self.protocol = gtySerialProtocol.GtySerialProtocol()

        # 指令累加器
        self.btnShortCounter = 0  # 按钮短按累加器
        self.btnLongCounter = 0  # 按钮长按累加器

        # 处理一些初始化的事情
        gtyLog.log.write(__file__, "serial init finish")

    # 主程序
    def startSerial(self):
        try:
            port, baud = self.getSerialPort()
            ser = serial.Serial(port, baud)
            gtyLog.log.write(__file__, "serial port:", port, baud)
        except Exception as e:
            gtyLog.log.write(__file__, e, "open serial port failed")
            return
        # 串口正常后的操作
        frq = 20  # 串口收发的处理频率
        dt = 1.0 / frq  # 串口收发的时间间隔
        localCounter = 1
        lastT = time.time()
        while True:
            T = time.time()
            if T - lastT >= dt:
                try:
                    localCounter += 1

                    # 读取缓冲区全部数据
                    self.getBuf.extend(ser.read(ser.in_waiting))
                    # 清空接收缓冲区
                    ser.flushInput()
                    self.getBufCopy.extend(self.getBuf.copy())
                    del self.getBuf[:]

                    # 处理接收
                    if self.getBufCopy:
                        self.sendEvent('UART', 'uart_dealGetData')

                    # 写入缓冲区数据
                    if self.sendBuf:
                        if self.sendBuf[2] != 1:
                            print(__file__, 'linux send buf:', self.sendBuf)
                        sendBytes = []
                        # 检查发送的范围在0~255
                        for i in self.sendBuf:
                            if 0 <= i <= 255:
                                sendBytes.append(i)
                            else:
                                gtyLog.log.write(__file__,'send byte not in range(0,256):',self.sendBuf)
                                break
                        ser.write(sendBytes)
                        # 清空发送缓冲区
                        del self.sendBuf[:]
                        del sendBytes

                    if T - lastT > dt * 2:
                        gtyLog.log.write(__file__, '串口收发延迟过长，dt = ', str(T - lastT))
                    lastT = T
                    # 记录下循环的进行
                    if localCounter % 2000 == 1:
                        gtyLog.log.write('serial running: ', localCounter)

                except Exception as e:
                    del self.sendBuf[:]
                    del self.getBuf[:]
                    gtyLog.log.write(__file__, '串口异常', e, traceback.extract_stack())

            # 延迟，减少cpu占用
            time.sleep(dt / 4.0)

    # 事件处理引擎
    def eventEngine(self):
        while True:
            time.sleep(0.001)
            if not self.eventQ["UART"].empty():
                try:
                    resultEvent = self.eventQ["UART"].get(block=True, timeout=1)
                    self.handleEventResult(resultEvent)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    gtyLog.log.write(__file__, 'serial event Engine error')

    # 发生事件
    def sendEvent(self, task, eventName, eventData=None):
        if eventData is None:
            eventData = []
        e = [eventName,  eventData]
        try:
            if task.upper() in self.eventQ.keys():
                self.eventQ[task.upper()].put(e)
        except Exception as e:
            print(e)

    # 处理事件
    def handleEventResult(self, event):
        # 这里resultEvent的结构是['eventType',eventId,data]
        # 这里一共有以下一些事件
        task = event[0]
        taskData = event[1]
        if task == 'uart_sendHeartBeatToStm32':
            self.sendHeartBeat()
            return
        if task == 'uart_dealGetData':
            self.handleGetData()
            return
        if task == 'uart_beepHalfSecond':
            self.sendBuf += gtySerialProtocol.buildCmd('beep', [5])
            return
        if task == 'uart_beep':
            self.sendBuf += gtySerialProtocol.buildCmd('beep', [int(float(taskData) * 10)])
            return
        if task == 'uart_stopReadEpc':
            self.sendBuf += gtySerialProtocol.buildCmd('startReadEpc', [3])
            self.sendBuf += gtySerialProtocol.buildCmd('startReadEpc', [3])
            return
        if task == 'uart_setDs3231Time':
            self.sendBuf += gtySerialProtocol.buildCmd('setTime', taskData)
            return
        if task == 'uart_setDs3231Date':
            self.sendBuf += gtySerialProtocol.buildCmd('setDate', taskData)
            return
        if task == 'uart_readControlCh1':  # 通道1读取控制
            if taskData == 1:  # 开始读卡
                self.sendBuf += gtySerialProtocol.buildCmd('startReadEpc', [3])
            if taskData == 0:  # 停止读卡
                self.sendBuf += gtySerialProtocol.buildCmd('stopReadEpc', [3])
            return
        if task == 'uart_readControlCh2':  # 通道2读取控制
            if taskData == 1:  # 开始读卡
                self.sendBuf += gtySerialProtocol.buildCmd('startReadEpc', [4])
            if taskData == 0:  # 停止读卡
                self.sendBuf += gtySerialProtocol.buildCmd('stopReadEpc', [4])
            return
        if task == 'uart_setReaderPower':  # uart_setReaderPower
            self.sendBuf += gtySerialProtocol.buildCmd('setPower', taskData)
            return
        if task == 'uart_getReaderPower':  # 读取读卡功率
            self.sendBuf += gtySerialProtocol.buildCmd('getReaderPower', taskData)
            return
        if task == 'uart_setTimeByAir':
            self.sendBuf += gtySerialProtocol.buildCmd('setTimeByAir', '')
            return
        if task == 'uart_shutDown':
            self.sendBuf += gtySerialProtocol.buildCmd('shutDown', '')
            return
        if task == 'uart_reboot':
            self.sendBuf += gtySerialProtocol.buildCmd('reboot', '')
            return
        if task == 'uart_updateStm32Firmware':
            self.updateStm32Firmware(taskData)
            return
        if task == 'uart_channelOpen':
            self.channelOpen(taskData)
            return
        if task == 'uart_fanControl':
            self.sendBuf += gtySerialProtocol.buildCmd('fanControl', taskData)
            return
        if task == 'uart_reBootReader':
            self.sendBuf += gtySerialProtocol.buildCmd('reBootReader', taskData)
            return
        if task == 'uart_sendReleaseMode':
            self.sendBuf += gtySerialProtocol.buildCmd('releaseMode', taskData)
            return

        if task == 'uart_freqBand':
            self.sendBuf += gtySerialProtocol.buildCmd('FreqBand', taskData)
            return
        if task == 'uart_askFirmwareVersion':
            self.sendBuf += gtySerialProtocol.buildCmd('askFirmwareVersion', taskData)
            return

    def getSerialPort(self):
        port = '/dev/ttyS3'
        baud = 115200
        return port, baud

    '''
    =================================================================================================================
    以下是具体的处理事件的函数
    =================================================================================================================
    '''

    # 发送心跳包
    def sendHeartBeat(self):
        cmd = gtySerialProtocol.buildCmd('heartBeat', [])

        self.receiveHeartBeatCounter -= 1  # 每秒减去一个，减到0串口重启
        self.sendBuf += cmd

    def handleGetData(self):
        getBufList = gtySerialProtocol.str2list(self.getBufCopy)
        del self.getBufCopy[:]
        if not getBufList:
            return
        # 进入固件升级
        self.sendFirmwarePackToStm32(getBufList)
        for c in getBufList:
            v, cmdId, data = self.protocol.decode(c)
            if not v:
                continue
            if cmdId == 'tagFlexible':
                self.sendEvent('UI', 'ui_getEPC', data)
                continue

            # 处理心跳信号
            if cmdId == 'heartBeat':
                self.receiveHeartBeatCounter = 5
                if self.receiveHeartBeatCounter <= 3:
                    print(__file__, 'heart beat:', self.receiveHeartBeatCounter)
                continue

            if cmdId == 'time':
                self.sendEvent('UI', 'ui_Ds3231TimeTick', data)
                continue

            if cmdId == 'bat':
                self.sendEvent('UI', 'ui_batteryVoltage', [data])
                continue

            if cmdId == 'date':
                self.sendEvent('UI', 'ui_Ds3231Date', data)
                continue

            if cmdId == 'setTimeByAir':
                self.sendEvent('UI', 'ui_getSetTimeInfo', data)
                continue

            if cmdId == 'firmwareVersion':
                self.sendEvent('UI', 'ui_getFirmwareVersion', data)
                continue

            if cmdId == 'buttonPressedShort':
                if self.btnShortCounter != data[1]:
                    self.btnShortCounter = data[1]
                    self.sendEvent('UI', 'ui_gunStartButtonPressedShort', data)
                    print(__file__, 'BTN SHORT PRESS')
                continue

            if cmdId == 'buttonPressedLong':
                if self.btnLongCounter != data[1]:
                    self.btnLongCounter = data[1]
                    self.sendEvent('UI', 'ui_gunStartButtonPressedLong', data)
                    # self.sendEvent('UART', 'uart_clockReset', d)
                    print(__file__, 'BTN LONG PRESS')
                continue

            if cmdId == 'chSettingResponse':
                self.sendEvent('UI', 'ui_chSettingResponse', data)
                continue

            if cmdId == 'testTagReadTimes':
                self.sendEvent('UI', 'ui_testTagReadTimes', data)
                continue

            if cmdId == 'stm32Boot':
                self.sendEvent('UI', 'ui_stm32Boot', data)
                continue

            if cmdId == 'stm32Cmd':
                self.sendEvent('UI', 'ui_stm32Cmd', data)
                continue

            if cmdId == 'getReaderPower':
                self.sendEvent('UI', 'ui_getReaderPower', data)
                print(__file__, 'ui_getReaderPower', data)
                continue

            if cmdId == 'getFreqBand':
                self.sendEvent('UI','ui_getFreqBand',data)

                continue

    # 向stm32升级固件
    # alist ： 由stm32发过来的数据包
    def sendFirmwarePackToStm32(self, alist):
        if len(alist) > 0:
            # print 'l ', len(alist)
            firmwareUpdating, packId = self.firmwareUpdater.decode(alist)
            if firmwareUpdating:
                if packId > 0 and packId > self.firmwareUpdater.lastCurrentSendingPackNumber:  # 正在升级
                    self.sendBuf += self.firmwareUpdater.buildPack(packId)
                    percentage = self.firmwareUpdater.updatePercentage()
                    if percentage > 100:  # 升级完成
                        self.firmwareUpdater.reset()
                        print('stm32 update complete')
                        self.sendEvent('UI', 'ui_stm32UpdateComplete', [])
                    else:
                        print(percentage, '%')
                    self.sendEvent('UI', 'ui_stm32UpdateProgress', [round(percentage, 1)])
                elif (packId == 0 and self.firmwareUpdater.lastCurrentSendingPackNumber > 0) or (
                        0 < packId < self.firmwareUpdater.lastCurrentSendingPackNumber):  # 升级完成
                    self.firmwareUpdater.reset()

    # 为stm32升级固件
    def updateStm32Firmware(self,d):
        firmwarePath = d[0]
        cmd = gtySerialProtocol.buildCmd('updateStm32Firmware', [])
        self.sendBuf += cmd
        self.firmwareUpdater.readBinFile(firmwarePath)
        self.firmwareUpdater._duringStm32FirmwareUpdate = True
        print(__file__,'stm32 update begins',firmwarePath)

    # 设置通道开启
    def channelOpen(self, data):
        data1 = data[0:4]
        data2 = data[4:8]
        print('ch cmd data:', data1, data2)
        bitData1 = data1[0] + data1[1] * 2 + data1[2] * 4 + data1[3] * 8
        bitData2 = data2[0] + data2[1] * 2 + data2[2] * 4 + data2[3] * 8
        cmd = gtySerialProtocol.buildCmd('chControl', [1, bitData1, bitData2])
        self.sendBuf += cmd


def main(eventQ):
    while True:
        print("===================UART task started===================")
        try:
            serial1 = GtySerial(eventQ)
            serial1.startSerial()
        except Exception as e:
            gtyLog.log.write(__file__, e, traceback.extract_stack())
        gtyLog.log.write(__file__, '=================serial service restart!=================')
        time.sleep(1)


