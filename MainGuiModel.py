# -*- coding:utf-8 -*-

from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication

from gtyUI.uiFiles import ui_mainDialog
from gtyUI import config, uiEventEngine
from gtyTools import tools, gtyLog
from gtyConfig import language, systemConfig

import os
import sys
import gtyTools.gtyTypes
import time
import datetime
import traceback

import gtySocket.socketTools


class MainGuiModel(QDialog, ui_mainDialog.Ui_Form):

    def __init__(self, eventQ, parent=None):
        super(MainGuiModel, self).__init__(parent)

        # ==========变量的定义===================
        # 配置的控制接口
        self.configHandlers = gtyTools.gtyTypes.ConfigHandlers()
        # 设备状态
        self.state = gtyTools.gtyTypes.machineState()
        # 通道状态
        self.channels = gtyTools.gtyTypes.Channels()
        # 芯片数据
        self.tagsGot = gtyTools.gtyTypes.tagDataSummary()
        # 硬件（stm32板子）时间，精确到ms
        self.hardwareTime = gtyTools.gtyTypes.hardwareTime()
        # linux系统的时间，用于辅助
        self.linuxTime = gtyTools.gtyTypes.linuxTime()
        

        # 事件处理队列
        self.eventQ = eventQ
        # 事件驱动引擎
        self.eventEngine = uiEventEngine.uiEventEngine(self.eventQ)
        # 辅助变量
        self.var = gtyTools.gtyTypes.auxiliaryVariables()
        self.socketBuilder = gtySocket.socketTools.SocketBuild()
        self.timerIntervalMs = 10
        self.timer = QTimer(self)
        
        # 传递的变量
        self.powerSaveCountValue = 0

        # =========系统的运行====================
        # 建立ui, UI控件的调整和配置
        self.initGui()
        # 变量的初始化
        self.initFields()
        # 更新显示
        self.initStateDisplay()
        # 启动事件驱动引擎
        self.initEventEngine()
        # =======辅助显示========================
        
        print('||||||||||||||||||||||||||||||||||||||')

    '''
    ===============================================================================================================
    二、 工具函数
    ===============================================================================================================
    '''

    # 初始化变量
    def initFields(self):
        # ==========变量的定义===================
        # 设备状态
        self.state.machineId = self.configHandlers.machine.read("machine", "machineId")
        self.getFieldsFromConfigFiles()

        # 初始状态为发布模式
        self.configHandlers.state.write('machine', 'releaseMode', 'release')
        self.updateValuesFromEventConfigFile()

    # 从配置文件更新不影响页面显示的变量
    def getFieldsFromConfigFiles(self):
        self.configHandlers = gtyTools.gtyTypes.ConfigHandlers()
        self.state.gateTime = self.configHandlers.machine.read("machine", "gateTime", "float", 1)
        self.state.allowEpcByteNumList = self.configHandlers.machine.read("reader", "allowEpcByteLength").split(",")
        self.powerSaveCountValue = int(self.configHandlers.machine.read("display", "powersave"))

    # GUI控件建立
    def initGui(self):
        self.setGeometry(0, 0, 800, 480)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.update()
        # 用不同的语言初始化
        self.initInLanguage()
        self.initGuiConnections()
        # 0.05秒的定时器
        
        self.timer.timeout.connect(self.updateHardwareTimePer10ms)
        self.timer.start(self.timerIntervalMs)

        # 设置字体大小
        font = QFont()
        font.setPointSize(18)
        self.resetDataButton.setFont(font)
        
        font.setPointSize(22)
        self.configButton.setFont(font)
        

    # 建立GUI的信号槽连接
    def initGuiConnections(self):
        self.configButton.clicked.connect(self.config)
        self.resetDataButton.clicked.connect(self.resetData)


    # 根据语言初始化文字
    def initInLanguage(self):
        self.label_3.setText(language.mainPage_label3)
        self.label.setText(language.mainPage_label)
        self.label_5.setText(language.mainPage_label5)
        self.label_23.setText(language.mainPage_label23)
        self.label_9.setText(language.mainPage_label9)
        self.label_11.setText(language.mainPage_label11)
        self.label_13.setText(language.mainPage_label13)
        self.label_21.setText(language.mainPage_label21)
        self.configButton.setText(language.mainPage_configButton)
        self.resetDataButton.setText(language.mainPage_resetDataButton)


    # 刷新状态显示
    def initStateDisplay(self):
        self.labelEventName.setText(self.configHandlers.machine.read("event", "eventName"))
        self.label_24.setText(self.state.machineId)
        # 显示ip地址
        ips = tools.getIpAddr()
        if ips is not []:
            ipStr = ''
            for ip in ips:
                ipStr += ip + ','
            ipStr = ipStr[:-1]
            self.textBrowser.append('ip: ' + ipStr)

    # 初始化eventEngine
    def initEventEngine(self):
        # 事件处理引擎处理
        try:
            self.eventEngine.eventList['everySecond'].connect(self.taskPerSecond)  # 完成每秒一次的操作

            self.eventEngine.eventList["ui_getEPC"].connect(self.getEpc)
            self.eventEngine.eventList["ui_log"].connect(self.outputLog)
            self.eventEngine.eventList["ui_batteryVoltage"].connect(self.updateBatteryPercentage)
            self.eventEngine.eventList["ui_loadEventConfigFile"].connect(self.updateValuesFromEventConfigFile)
            self.eventEngine.eventList["ui_updateMainDialogEventInfo"].connect(self.updateValuesFromEventConfigFile)
            self.eventEngine.eventList["ui_powerControl"].connect(self.powerManage)
            self.eventEngine.eventList["ui_internetConnectionReport"].connect(self.updateInternetConnectionState)
            self.eventEngine.eventList["ui_uploadResultFileToServer"].connect(self.handleFileUploadResult)  # 更新上传是否成功
            self.eventEngine.eventList["ui_testTagReadTimes"].connect(self.updateTestTagShow)  # 显示测试卡读到的次数
            self.eventEngine.eventList["ui_updateMainDialogValue"].connect(self.updateValuesFromEventConfigFile)  # 更新主页面里的值
            self.eventEngine.eventList["ui_uploadTagNumInWait"].connect(self.updateCpValueNumLeft)  # 剩余的待上传的cp数据

            self.eventEngine.eventList["ui_updateFieldsFromConfigFile"].connect(self.getFieldsFromConfigFiles)
            self.eventEngine.eventList["ui_socketGetDate"].connect(self.socketGetDate)
            self.eventEngine.eventList["ui_socketGetTime"].connect(self.socketGetTime)
            self.eventEngine.eventList["ui_socketGetGunTime"].connect(self.socketGetGunTime)
            
            self.eventEngine.eventList["ui_powerSaveValueSet"].connect(self.powerSaveCount)
            self.eventEngine.eventList["ui_updateTimeDisplay"].connect(self.updateTimeDisplay)
            
            self.eventEngine.start()
        except Exception as e:
            traceback.print_exc()
            print(e)

    # 发生事件
    def sendEvent(self, task, eventName, eventData=None):
        if eventData is None:
            eventData = []
        e = [eventName, eventData]
        try:
            if task.upper() in self.eventQ.keys():
                self.eventQ[task.upper()].put(e)
        except Exception as e:
            print(e)

    # 日志输出
    def log(self, text):
        self.sendEvent('UI', 'ui_log', eventData=text)

    # 完成每秒一次的任务，这里由linux系统时间控制
    def taskPerSecond(self):
        # 向主进程发送心跳包
        self.linuxTime.secondCounter += 1

        # 比赛历时
        self.showProcessedTime()
        # 刷新通知栏显示
        self.updateNoticeLabel()
        # 刷新主页时间
        now = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d\n%H:%M:%S')
        self.label_2.setText(now)

        if len(self.tagsGot.checkedTagDict) >= 1000:
            self.tagsGot.checkedTagDict = {}

        # 通过IO进程检测网络连接状态
        # if self.linuxTime.secondCounter % 5 == 1:
        #     self.checkServerConnection()

        # if self.linuxTime.secondCounter == 5:
        #     self.sendEvent('UART', 'uart_askFirmwareVersion')
        
        if self.powerSaveCountValue > 0:
            self.powerSaveCountValue -= 1
            if self.powerSaveCountValue == 0:
                # if os.path.exists('/sys/class/backlight/10-0045/bl_power'):
                print('息屏')

        tools.autoFan()

        # 每1秒发送socket心跳包
        # self.socketSendHeartBeat()
        

    '''
    =============================================================================================================
    三、 事件处理函数，包括直接产生的事件和基于信号-槽的函数
    =============================================================================================================
    '''

    def updateValuesFromEventConfigFile(self):
        self.configHandlers = gtyTools.gtyTypes.ConfigHandlers()
        self.state.eventId = self.configHandlers.event.read("event", "eventId")
        self.labelEventName.setText(self.configHandlers.machine.read("event", "eventName"))
        # 输出调试模式标志
        if self.configHandlers.state.read('machine', 'releaseMode') == 'release':
            self.state.noticeLabelDict['releaseMode'] = language.mainPage_releaseMode
        else:
            self.state.noticeLabelDict['releaseMode'] = language.mainPage_TestMode
        self.updateNoticeLabel()

    # 刷新电池电量
    def updateBatteryPercentage(self, data):
        self.state.batteryPercentage = int(tools.batteryPercentage(data[0]))
        self.label_22.setText(str(self.state.batteryPercentage) + '%')

    # 输出log
    def outputLog(self, text):
        if self.state.textBrowserLineNum >= 1000:
            self.textBrowser.setText('')
            self.state.textBrowserLineNum = 0
        self.state.textBrowserLineNum += 1
        self.textBrowser.append(text)

    # 显示当前时刻
    def showTimePer1Second(self, timeList):
        now = datetime.datetime.now() 
        hour = timeList[0]
        minute = timeList[1]
        second = timeList[2]
        if second % 2 == 0:
            dt = '%02d:%02d:%02d' % (hour, minute, second)
        else:
            dt = '%02d %02d %02d' % (hour, minute, second)
        self.label_2.setText(dt)
        # 百分之一秒时间清零
        self.hardwareTime.hour = hour
        self.hardwareTime.minute = minute
        self.hardwareTime.second = second
        self.hardwareTime.ms = 0

    # 更新0.01秒
    def updateHardwareTimePer10ms(self):
        if self.hardwareTime.ms + self.timerIntervalMs < 1000:
            self.hardwareTime.ms += self.timerIntervalMs

    # 显示比赛已进行时间，采用的是linux系统自身的时间
    def showProcessedTime(self):
        if self.state.gunStartTime is not None:
            gunStart = tools.getTimeStamp(self.state.gunStartTime.year,self.state.gunStartTime.month,self.state.gunStartTime.day,
                                          self.state.gunStartTime.hour,self.state.gunStartTime.minute,self.state.gunStartTime.second,0)
            now = tools.getTimeStamp(self.hardwareTime.year,self.hardwareTime.month,self.hardwareTime.day,
                                     self.hardwareTime.hour,self.hardwareTime.minute,self.hardwareTime.second,0)
            m, s = divmod(int(now - gunStart), 60)
            h, m = divmod(m, 60)
            if self.var.gunShowColon:
                text = ("%02d:%02d:%02d" % (h, m, s))
                self.var.gunShowColon = False
            else:
                text = ("%02d %02d %02d" % (h, m, s))
                self.var.gunShowColon = True
            self.label_6.setText(text)

    # 枪响
    def gunStart(self):
        self.state.gunStartTime = gtyTools.gtyTypes.timeInMs(
            self.hardwareTime.year, self.hardwareTime.month, self.hardwareTime.day,
            self.hardwareTime.hour, self.hardwareTime.minute, self.hardwareTime.second,
            self.hardwareTime.ms)
        font = QFont()
        font.setPointSize(13)
        self.sendEvent('UART', "uart_beep", 0.5)
        print('================== GUN START =================')

    # 枪停止
    def gunStop(self):
        self.state.gunStartTime = None
        self.label_6.setText('------')
        self.sendEvent('UART', "uart_beep", 0.5)
        print('================== GUN STOP =================')

    # 分读写器读取控制
    def readControlByReader(self, data):
        reader = data[0]
        cmd = data[1]
        readerState = ''
        cmdBranch = ''
        if reader == '1':
            readerState = self.state.readerState1
        if reader == '2':
            readerState = self.state.readerState2

        if (readerState == 'stopped' and cmd == 'x') or (cmd == 'on'):
            print(__file__, 'reader' + reader + ' start')
            # 发送读取指令
            if reader == '1':
                self.state.readerState1 = 'reading'
            if reader == '2':
                self.state.readerState2 = 'reading'
            for j in range(0, 5):
                self.sendEvent('UART', 'uart_readControlCh' + reader, 1)  # 1表示开始读卡
            self.sendEvent('UI', 'ui_updateOperateDialogReadingLabel', 'stop' + reader)
            cmdBranch = 'start'
        if (readerState == 'reading' and cmd == 'x') or (cmd == 'off'):
            # 发送停止读取指令
            if reader == '1':
                self.state.readerState1 = 'stopped'
            if reader == '2':
                self.state.readerState2 = 'stopped'
            for j in range(0, 5):
                self.sendEvent('UART', 'uart_readControlCh' + reader, 0)  # 0表示停止读卡
            self.sendEvent('UI', 'ui_updateOperateDialogReadingLabel', 'start' + reader)
            cmdBranch = 'stop'

        self.sendEvent('UART', 'uart_beepHalfSecond')
        text = language.mainPage_reader + reader + ': ' + cmdBranch
        self.log(text)

    # 打开配置页面
    def config(self):
        configDialog = config.Config(self, self.eventQ)
        configDialog.exec_()

    # 重置统计量
    def resetData(self):
        try:
            self.tagsGot.reset()
            self.state.textBrowserLineNum = 0
            self.textBrowser.setText('')
            self.label_12.setText(str(0))
            self.label_10.setText(str(0))
            self.channels.resetNum()
            self.var.rawEpcNum = 0
            for ch in range(0, 8):
                if self.channels.chs[ch].open == 1:
                    self.channels.chs[ch].chBtn.setText('0')
            print('reset data display')
            if self.configHandlers.state.read('machine', 'releaseMode') != 'release':
                self.sendEvent('IO', 'io_resetData')
        except Exception as e:
            print(e)

    # 电源管理
    def powerManage(self, mode):
        print(__file__, mode)
        if mode == 'reboot':
            self.sendEvent('UART', 'uart_reboot', [])
            time.sleep(1)
            gtyLog.log.write(__file__, 'sudo reboot')
            gtyTools.tools.linuxSudoCmd('reboot')
        elif mode == 'powerOff':
            self.sendEvent('UART', 'uart_shutDown', [])
            gtyLog.log.write(__file__, 'halt')
            gtyTools.tools.linuxSudoCmd('halt')

    # 获得了EPC码的处理
    # 这里的l数据结构是：[timeList, epcList, ch,antenna,packId]
    def getEpc(self, data):
        newTag = data[0]
        self.var.rawEpcNum += 1
        # 按字节数过滤
        if str(newTag.epcByteNum) not in self.state.allowEpcByteNumList:
            return
        try:
            tagHasKey = newTag.epcString in self.tagsGot.checkedTagDict
            if not tagHasKey or \
                    (tagHasKey and (abs(newTag.timeStamp - self.tagsGot.checkedTagDict[newTag.epcString].timeStamp) >= self.state.gateTime)):
                self.tagsGot.totalCheckedNum += 1
                self.tagsGot.checkedTagDict[newTag.epcString] = newTag
                # 这里判断是否有epc码，如果有，则显示
                newTag.buildTimeString()
                text = newTag.hardwareTimeString + ":" + newTag.epcString
                self.outputLog(text)
                tags = [newTag]
                self.tagsGot.differentCheckedNum = len(self.tagsGot.checkedTagDict)
                # 把数据发送给IO和SOCKET
                self.sendEvent('IO', 'io_addTags', tags)
                # self.socketSendTagInfo(newTag)
                # 把数据发送给SOCKET服务器
                # self.sendEvent('SOCKET_SERVER', 'add_tag', tags)
                # 刷新统计量
                ch = newTag.channelId
                self.label_12.setText((str(self.tagsGot.differentCheckedNum)))
                self.label_10.setText(str(self.tagsGot.totalCheckedNum))
        except Exception as e:
            print(e)

    # 处理当前是否能上网的结果
    def updateInternetConnectionState(self, state):
        self.state.internetConnectionState = state
        if self.state.internetConnectionState == 'disconnected':
            self.label_14.setText(language.mainPage_label14_disconnected)
        elif self.state.internetConnectionState == 'wwwConnected':
            self.label_14.setText(language.mainPage_label14_connectedWithoutServer)
        else:
            self.label_14.setText(language.mainPage_label14_connected)

    # 刷新Ds3231的日期
    def updateDs3231Date(self, dateList):
        if dateList[0] < 2000:
            dateList[0] += 2000
        self.hardwareTime.year = dateList[0]
        self.hardwareTime.month = dateList[1]
        self.hardwareTime.day = dateList[2]

    def checkServerConnection(self):
        timeStamp = tools.getTimeStamp(self.hardwareTime.year, self.hardwareTime.month, self.hardwareTime.day,
                                       self.hardwareTime.hour, self.hardwareTime.minute, self.hardwareTime.second, 0)
        dataList = {
            "machineId": self.state.machineId,
            "batteryPercent": self.state.batteryPercentage,
            "totalEpcRead": self.tagsGot.totalCheckedNum,
            "differentEpcRead": self.tagsGot.differentCheckedNum,
            "reader1Working": self.state.readerState1,
            "reader2Working": self.state.readerState2,
            "hardwareTime": timeStamp,
            "eventId": self.state.eventId
        }
        self.sendEvent("IO", "io_checkServerConnection", [dataList])

    def updateNoticeLabel(self):
        text = ""
        for k, v in self.state.noticeLabelDict.items():
            text = text + v + ","
        text = text[:len(text) - 1]
        self.labelNotice.setText(text)

    def chBtnClicked(self, ch):
        # 按一下就不再显示通道序号
        if self.channels.displayChannelNames:
            self.channels.displayChannelNames = False
            for i in range(0, 8):
                self.channels.chs[i - 1].chBtn.setText(str(self.channels.chs[i - 1].tagReadNum))

        if self.linuxTime.secondCounter > self.channels.testNumDisplayTilSecond:
            self.channels.chs[ch - 1].chBtn.setText(str(self.channels.chs[ch - 1].tagReadNum))
        try:
            # 开启或关闭这个通道；
            if self.channels.chs[ch - 1].open == 0:
                self.channels.chs[ch - 1].open = 1
            else:
                self.channels.chs[ch - 1].open = 0
            # 这里发送一条指令开启或关闭这个通道
            channelState = []
            for i in range(0, 8):
                channelState.append(self.channels.chs[i].open)
            self.sendEvent('UART', 'uart_channelOpen', channelState)  # 参数是一个列表
        except Exception as e:
            print(e)

    def chEnableResponse(self, data):
        # 通道使能命令执行后的答复
        # 使按钮背景色变化，并显示或不显示读取数量；
        ChDataList = [data[1] % 2, (data[1]) // 2 % 2, (data[1]) // 4 % 2, (data[1]) // 8 % 2, data[2] % 2,
                      (data[2]) // 2 % 2, (data[2]) // 4 % 2, (data[2]) // 8 % 2]
        for i in range(0, 8):
            if ChDataList[i] == 1:
                self.channels.chs[i].chBtn.setStyleSheet(systemConfig.param.btnHighLightStyle)
                self.channels.chs[i].chBtn.setText(str(self.channels.chs[i].tagReadNum))
                self.channels.chs[i].open = 1
            else:
                self.channels.chs[i].chBtn.setStyleSheet(systemConfig.param.btnEnabledStyle)
                self.channels.chs[i].chBtn.setText('CH' + str(i + 1))
                self.channels.chs[i].open = 0

    def updateTestTagShow(self, data):
        for i in range(0, 8):
            if data[i] > 0:
                self.channels.chs[i].testTagReadNum += data[i]
                self.channels.chs[i].chBtn.setText('T:' + str(self.channels.chs[i].testTagReadNum))
                self.channels.testNumDisplayTilSecond = self.linuxTime.secondCounter + 10

    def stm32Cmd(self, cmd):
        if self.configHandlers.state.read('machine', 'release') != 'release':
            if cmd[0] == 'shut down':
                self.powerManage('powerOff')
            if cmd[0] == 'reboot':
                self.powerManage('reboot')

    # 刷新页面待上传数据
    def updateCpValueNumLeft(self, dataNum):
        self.label_30.setText(str(dataNum))

    # 提示软件需要升级
    def softwareUpdateNotice(self, data):
        print(__file__, 'softwareUpdateNotice:', data)
        if data[0] == 'software':
            self.state.updateNotice = 'software'
        if data[0] == 'firmware':
            self.state.updateNotice = 'firmware'

    # 更新上传结果文件是否成功
    def handleFileUploadResult(self, res):
        dis = time.strftime('%H:%M:%S ', time.localtime(time.time()))
        if res[0] == 'successful':
            self.outputLog(dis + language.mainPage_dataFileUploadSuccessful + " " + res[1])
        else:
            self.outputLog(dis + language.mainPage_dataFileUploadFailed + " " + res[1])

    def updateFirmwareVersion(self, data):
        if self.var.getFirmwareFlag == 1:
            return
        self.var.getFirmwareFlag = 1
        print(__file__, 'firmware ', data)
        # 判断是否满足最低固件要求
        firmwareString = str(data[0]) + '.' + str(data[1])
        lowest = float(systemConfig.lowestFirmware)
        now = float(firmwareString)
        if now < lowest:
            s = '<'
        elif now == lowest:
            s = '='
        else:
            s = '>'
        self.log('current firmware: ' + firmwareString + s + systemConfig.lowestFirmware + " required lowest.")
        if s == '<':
            self.log('Firmware version is too low to work correctly, please update! ')
        self.configHandlers.state.write('machine', 'firmwareversion', str(data[0]) + '.' + str(data[1]))
        self.updateValuesFromEventConfigFile()

    '''
        响应socket
    '''

    def socketSendHeartBeat(self):
        cmdStr = self.socketBuilder.buildSocket('heartBeat', "")
        self.sendEvent('SOCKET', 'socket_send', cmdStr)

    def socketSendTagInfo(self, tag):
        cmdStr = self.socketBuilder.buildSocket('epc', tag.hardwareDateString + " " + tag.hardwareTimeString + ','+ tag.epcString)
        self.sendEvent('SOCKET', 'socket_send', cmdStr)

    def socketGetDate(self):
        cmdStr = self.socketBuilder.buildSocket('machineDate', str(self.hardwareTime.year) + '-' +
                                                str(self.hardwareTime.month) + '-' + str(self.hardwareTime.day))
        self.sendEvent('SOCKET', 'socket_send', cmdStr)

    def socketGetTime(self):
        print(__file__, 'socket get getTime')
        cmdStr = self.socketBuilder.buildSocket('machineTime', str(self.hardwareTime.hour) + ':' +
                                                str(self.hardwareTime.minute) + ':' + str(self.hardwareTime.second))
        print(__file__, cmdStr)
        self.sendEvent('SOCKET', 'socket_send', cmdStr)

    def socketGetGunTime(self):
        if self.state.gunStartTime is not None:
            s = "%04d-%02d-%02d %02d:%02d:%02d:%02d" % (
                self.state.gunStartTime.year,
                self.state.gunStartTime.month,
                self.state.gunStartTime.day,
                self.state.gunStartTime.hour,
                self.state.gunStartTime.minute,
                self.state.gunStartTime.second,
                self.state.gunStartTime.ms / 10
            )
            cmdStr = self.socketBuilder.buildSocket('gunTime', s)
        else:
            cmdStr = self.socketBuilder.buildSocket('gunTime', 'gunNotStarted')
        self.sendEvent('SOCKET', 'socket_send', cmdStr)
        
    def powerSaveCount(self,data):
        self.powerSaveCountValue = data
        
    def updateTimeDisplay(self):
        timeStamp = tools.getTimeStamp(self.hardwareTime.year, self.hardwareTime.month, self.hardwareTime.day,
                                       self.hardwareTime.hour, self.hardwareTime.minute, self.hardwareTime.second, 0)
        print('update time display',timeStamp)
    
        

def main(eventQ):
    print("===================UI task started===================")
    try:
        gtyLog.log.write(__file__, 'ui process starting ...')
        app = QApplication(sys.argv)
        ex = MainGuiModel(eventQ)
        ex.show()
        app.exec_()
        gtyLog.log.write(__file__, 'ui process ended...')
        sys.exit()
    except Exception as e:
        gtyLog.log.write(__file__, e, traceback.extract_stack())
