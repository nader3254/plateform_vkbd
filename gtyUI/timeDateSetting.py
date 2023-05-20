# -*- coding:utf-8 -*-
import datetime
import sys
import os
import time
from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import QDialog, QApplication

from uiFiles import ui_setTime
from gtyConfig import language, systemConfig, configFileHandler
import uiTools
from gtyTools import gtyLog, gtyTypes, selection
import threading


class TimeDateSetting(QDialog, ui_setTime.Ui_timeSetting):

    def __init__(self, mainPage, eventQ, parent=None):
        super(TimeDateSetting, self).__init__(parent)
        self.setupUi(self)
        uiTools.centerAndSetIcon(self)
        self.eventQ = eventQ
        self.mainPage = mainPage

        # 当前DS3231里记录的时间变量，这个由DS3231整数秒事件驱动每秒刷新一次
        self.hardwareTime = gtyTypes.hardwareTime()

        # 网络时间的毫秒位
        self.ntpTimeMs = 0

        # 连接
        self.clockModifyState = False
        self.ntpEnableState = False
        self.modifyClockBtn.clicked.connect(self.changeModifyState)
        self.setTimeBtn.clicked.connect(lambda: self.setHardwareDateTime('time'))
        self.setDateBtn.clicked.connect(lambda: self.setHardwareDateTime('date'))
        self.writeInNtpBtn.clicked.connect(self.getNtpThread)
        self.ntpEnableBtn.clicked.connect(self.ntpEnableDisable)
        self.setTimeZoneBtn.clicked.connect(self.setTimeZone)
        # 获得数据链同步时间的结果指令
        self.mainPage.eventEngine.eventList["ui_getSetTimeInfo"].connect(self.getSetTimeByAirResult)


        # 各种连接
        self.yearP1Btn.clicked.connect(lambda: self.modifyBtnAction('year', 1))
        self.yearM1Btn.clicked.connect(lambda: self.modifyBtnAction('year', -1))
        self.monthP1Btn.clicked.connect(lambda: self.modifyBtnAction('month', 1))
        self.monthM1Btn.clicked.connect(lambda: self.modifyBtnAction('month', -1))
        self.dayP1Btn.clicked.connect(lambda: self.modifyBtnAction('day', 1))
        self.dayM1Btn.clicked.connect(lambda: self.modifyBtnAction('day', -1))
        self.hourP1Btn.clicked.connect(lambda: self.modifyBtnAction('hour', 1))
        self.hourM1Btn.clicked.connect(lambda: self.modifyBtnAction('hour', -1))
        self.minP1Btn.clicked.connect(lambda: self.modifyBtnAction('minute', 1))
        self.minM1Btn.clicked.connect(lambda: self.modifyBtnAction('minute', -1))
        self.secP1Btn.clicked.connect(lambda: self.modifyBtnAction('second', 1))
        self.secM1Btn.clicked.connect(lambda: self.modifyBtnAction('second', -1))
        self.secP01Btn.clicked.connect(lambda: self.modifyBtnAction('second', 0.1))
        self.secM01Btn.clicked.connect(lambda: self.modifyBtnAction('second', -0.1))

        # language
        # 处理不同的语言
        self.setWindowTitle("Time and Date Setting")
        self.label.setText(language.timeSetting_year)
        self.label_2.setText(language.timeSetting_month)
        self.label_7.setText(language.timeSetting_day)
        self.label_4.setText(language.timeSetting_hour)
        self.label_5.setText(language.timeSetting_minute)
        self.label_6.setText(language.timeSetting_second)
        self.writeInNtpBtn.setText(language.timeSetting_setNtpTime)
        self.modifyClockBtn.setText(language.timeSetting_modifyTime)
        self.setTimeBtn.setText(language.timeSetting_setTime)
        self.setDateBtn.setText(language.timeSetting_setDate)
        self.returnBtn.setText(language.timeSetting_back)
        self.strSend = language.timeSetting_send
        self.strReceive = language.timeSetting_receive
        self.strS1 = language.timeSetting_wirelessTimeSignal

        self.mainPage.eventEngine.eventList["everySecond"].connect(self.clearNtpMs)
        
        self.machineConfig = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)
        # 0.05秒的定时器
        self.timerIntervalMs = self.mainPage.timerIntervalMs
        self.mainPage.timer.timeout.connect(self.timerWork)

        self.setModifyBtnStyle('disable')
        
        # ntp初始化状态显示
        self.getNtpFlag=0
        self.ntpServer = self.machineConfig.read('ntp', 'ntpServer')
        self.ntpTimeout = self.machineConfig.read('ntp', 'ntpTimeout','int')
        ntpEnableStatus = self.machineConfig.read('ntp', 'ntpEnable')
        if ntpEnableStatus == 'off':
            self.setNtpEnableBtnStyle('disable')
        else:
            self.setNtpEnableBtnStyle('enable')
        
        # 时区复选框
        self.timezone = selection.TIMEZONE()
        self.timezoneComboBox.addItems(self.timezone.getTZList())
        TZName = self.machineConfig.read('timezone', 'timezone')
        self.timezoneComboBox.setCurrentText(TZName)
        
        
        

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

    # 刷新时间显示，函数的输入是DS3231的日期,
    def updateDs3231Date(self, dateList=None):
        if not self.clockModifyState:
            self.hardwareTime.year = dateList[0] + 2000
            self.hardwareTime.month = dateList[1]
            self.hardwareTime.day = dateList[2]
            self.lcdNumber_year.display(str(self.hardwareTime.year))
            self.lcdNumber_month.display(str(self.hardwareTime.month))
            self.lcdNumber_day.display(str(self.hardwareTime.day))

    # 刷新DS3231的显示时间，函数的输入是DS3231的时间
    def updateDs3231Time(self, timeList=None):
        if not self.clockModifyState:
            self.hardwareTime.hour = timeList[0]
            self.hardwareTime.minute = timeList[1]
            self.hardwareTime.second = timeList[2]
            self.hardwareTime.ms = 0
            self.lcdNumber_hour.display(str(self.hardwareTime.hour))
            self.lcdNumber_min.display(str(self.hardwareTime.minute))
            self.lcdNumber_sec.display(str(self.hardwareTime.second))
            self.lcdNumber_ms.display('%03d' % 0)

    def modifyBtnAction(self, section, direction):
        if not self.clockModifyState:
            return
        if not (direction in [-1, 1] or ((direction in [-0.1, 0.1]) and (section == 'second'))):
            return
        if section == 'year' and 2000 <= self.hardwareTime.year + direction <= 2100:
            self.hardwareTime.year += direction
            self.lcdNumber_year.display(str(self.hardwareTime.year))
        if section == 'month' and 1 <= self.hardwareTime.month + direction <= 12:
            self.hardwareTime.month += direction
            self.lcdNumber_month.display(str(self.hardwareTime.month))
        if section == 'day' and 1 <= self.hardwareTime.day + direction <= 31:
            self.hardwareTime.day += direction
            self.lcdNumber_day.display(str(self.hardwareTime.day))
        if section == 'hour' and 0 <= self.hardwareTime.hour + direction <= 23:
            self.hardwareTime.hour += direction
            self.lcdNumber_hour.display(str(self.hardwareTime.hour))
        if section == 'minute' and 0 <= self.hardwareTime.minute + direction <= 59:
            self.hardwareTime.minute += direction
            self.lcdNumber_min.display(str(self.hardwareTime.minute))
        if section == 'second' and 0 <= self.hardwareTime.second + direction <= 59 and direction in [-1, 1]:
            self.hardwareTime.second += direction
            self.lcdNumber_sec.display(str(self.hardwareTime.second))
        if section == 'second' and 0 <= self.hardwareTime.ms + direction * 1000 <= 999 and direction in [-0.1, 0.1]:
            self.hardwareTime.ms += int(direction * 1000)
            self.lcdNumber_ms.display('%03d' % self.hardwareTime.ms)

    def timerWork(self):
        if not self.clockModifyState and 0 <= self.hardwareTime.ms + self.timerIntervalMs <= 999:
            self.hardwareTime.ms += self.timerIntervalMs
            self.lcdNumber_ms.display(str(self.hardwareTime.ms))
        if 0 <= self.ntpTimeMs + self.timerIntervalMs <= 999:
            self.ntpTimeMs += self.timerIntervalMs
            now = datetime.datetime.now()
            self.label_systemTime.setText(language.timeSetting_ntpTime + ":\n " + datetime.datetime.strftime(now,'%Y-%m-%d %H:%M:%S') + ".%03d" % self.ntpTimeMs)

    def clearNtpMs(self):
        self.ntpTimeMs = 0

    def changeModifyState(self):
        if self.clockModifyState:
            self.clockModifyState = False
            self.modifyClockBtn.setStyleSheet(systemConfig.param.btnEnabledStyle)
            self.setModifyBtnStyle('disable')
        else:
            self.clockModifyState = True
            self.modifyClockBtn.setStyleSheet(systemConfig.param.btnHighLightStyle)
            self.setModifyBtnStyle('enable')


    def getNtpThread(self):
        self.getNtp = threading.Thread(target=self.getNtpTime)
        self.getNtp.start()    
        
         
    def getNtpTime(self):
        self.label_display.setText('Getting ntp time...')
        try:
            status = os.system('echo %s | sudo -S %s' %('100perica!!','ntpdate -u '+ str(self.ntpServer)))
            if status == 0:
                self.setNtpTime()
                self.label_display.setText('Get ntp time success!')
            else:
                self.label_display.setText('Get ntp time failed!')
        except Exception as e:
            print('get ntp time failed ',e)   
        return
        
        
    def setNtpTime(self):
        self.ntpTimeout = self.machineConfig.read('ntp', 'ntpTimeout','int')
        now = datetime.datetime.now()
        print('now----',now)
        # self.sendEvent("UART", "uart_setDs3231Time",[now.hour, now.minute, now.second, self.ntpTimeMs // 10])
        

    def setHardwareDateTime(self, target):
        if target == 'time':
            back = 30
            second = self.hardwareTime.second
            centiSecond = self.hardwareTime.ms // 10
            if centiSecond >= back:
                centiSecond -= back
            elif second >= 1:
                second -= 1
                centiSecond = centiSecond + 100 - back
            self.sendEvent("UART", "uart_setDs3231Time",[self.hardwareTime.hour, self.hardwareTime.minute, second, centiSecond])
        if target == 'date':
            if self.hardwareTime.year > 2000:
                year = self.hardwareTime.year - 2000
            else:
                year = self.hardwareTime.year
            self.sendEvent("UART", "uart_setDs3231Date",[year, self.hardwareTime.month, self.hardwareTime.day])

    # 通过数据链同步时间
    def setTimeInAir(self):
        self.sendEvent('UART', 'uart_setTimeByAir', '')

    # 获得数据链同步时间的指令
    def getSetTimeByAirResult(self, resList):
        id = resList[0]
        direction = resList[1]
        res = u''
        if str(direction) == '1':
            res += self.strSend
        else:
            res += self.strReceive
        res += self.strS1
        res += str(id)
        self.label_display.setText(res)

    # 更新调整按钮的颜色样式
    def setModifyBtnStyle(self, style):
        buttons = [self.yearP1Btn, self.yearM1Btn, self.monthP1Btn, self.monthM1Btn, self.dayP1Btn, self.dayM1Btn,
                   self.hourP1Btn, self.hourM1Btn, self.minP1Btn, self.minM1Btn, self.secP1Btn, self.secM1Btn,
                   self.secP01Btn, self.secM01Btn]
        for btn in buttons:
            if style == 'disable':
                btn.setStyleSheet(systemConfig.param.btnDisabledStyle)
            if style == 'enable':
                btn.setStyleSheet(systemConfig.param.btnEnabledStyle)
    
    # 设置时区
    def setTimeZone(self):
        TZid = self.timezoneComboBox.currentIndex()
        TZName = self.timezoneComboBox.currentText()
        
        os.system('echo %s | sudo -S %s' %('100perica!!','rm /etc/localtime'))
        os.system('echo %s | sudo -S %s' %('100perica!!','ln -sf /usr/share/zoneinfo/'+str(TZName) + ' /etc/localtime'))
        os.system('echo '+str(TZName) +' | sudo tee /etc/timezone')

        cmd = 'date "+ %z"'
        res = os.popen(cmd)
        UTC = res.read().replace(')', '')
        
        self.label_display.setText('set timezone: '+ TZName + '\n' + 'UTC: ' + UTC)
        self.machineConfig.write('timezone', 'timezone', TZName)
        self.machineConfig.write('timezone', 'UTC', UTC)
        self.timezoneComboBox.setCurrentText(TZName)
        self.sendEvent('UI', 'ui_updateTimeDisplay','')
        
    
    def ntpEnableDisable(self):
        if self.ntpEnableState:
            self.ntpEnableState = False
            self.setNtpEnableBtnStyle('disable')
            self.ntpEnableBtn.setStyleSheet(systemConfig.param.btnDisabledStyle)
            self.machineConfig.write('ntp', 'ntpEnable', 'off')
            self.label_display.setText('Successfully closed ntp')
        else:
            self.ntpEnableState = True
            self.setNtpEnableBtnStyle('enable')
            self.ntpEnableBtn.setStyleSheet(systemConfig.param.btnEnabledStyle)
            self.machineConfig.write('ntp', 'ntpEnable', 'on')
            self.label_display.setText('Successfully opened ntp')
            
            
    def setNtpEnableBtnStyle(self,style):
        if style == 'disable':
            os.system('echo %s | sudo -S %s' %('100perica!!','timedatectl set-ntp false &'))
            self.ntpEnableBtn.setStyleSheet(systemConfig.param.btnDisabledStyle)
            self.ntpEnableBtn.setText(language.timeSetting_ntpDisable)
        elif style == 'enable':
            os.system('echo %s | sudo -S %s' %('100perica!!','timedatectl set-ntp true &'))
            self.ntpEnableBtn.setStyleSheet(systemConfig.param.btnEnabledStyle)
            self.ntpEnableBtn.setText(language.timeSetting_ntpEnable)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = TimeDateSetting(None, None, None, None)
    form.show()
    sys.exit(app.exec_())
