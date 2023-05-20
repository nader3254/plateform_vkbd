# -*- coding:utf-8 -*-


import sys
import time
import os

from PyQt5.QtWidgets import QDialog, QApplication

from gtyUI import shutDown

sys.path.append('..')

from uiFiles import ui_operate
from gtyTools import tools
import readerSet
from gtyConfig import language, configFileHandler, systemConfig
import uiTools


class Operate(QDialog, ui_operate.Ui_operateDialog):

    def __init__(self, mainPage, eventQ, parent=None):
        super(Operate, self).__init__(parent)

        self.machineConfig = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)
        self.allowEpcByteLength = self.machineConfig.read("reader", "allowEpcByteLength").split(',')
        self.machineId = self.machineConfig.read("machine", "machineId")

        self.setupUi(self)
        uiTools.centerAndSetIcon(self)
        self.eventQ = eventQ
        self.mainPage = mainPage

        self.readControlBtn1Start.clicked.connect(lambda: self.startOrStopReading(1,'on'))
        self.readControlBtn1Stop.clicked.connect(lambda: self.startOrStopReading(1,'off'))
        self.readControlBtn2Start.clicked.connect(lambda: self.startOrStopReading(2,'on'))
        self.readControlBtn2Stop.clicked.connect(lambda: self.startOrStopReading(2,'off'))

        self.mainPage.eventEngine.eventList["ui_updateOperateDialogReadingLabel"].connect(self.updateReadingBtn)
        self.shutdownBtn.clicked.connect(self.shutdown)
        self.fanControlBtn_on.clicked.connect(lambda: self.fanControl('on'))
        self.fanControlBtn_off.clicked.connect(lambda: self.fanControl('off'))
        self.readerRebootBtn1.clicked.connect(lambda: self.rebootReader(1))
        self.readerRebootBtn2.clicked.connect(lambda: self.rebootReader(2))
        self.readerSetBtn1.clicked.connect(lambda: self.readerSet(1))
        self.readerSetBtn2.clicked.connect(lambda: self.readerSet(2))

        # 读卡长度选择按钮
        self.checkBox_2Byte.clicked.connect(lambda: self.updateCheckByteAllow(2))
        self.checkBox_4Byte.clicked.connect(lambda: self.updateCheckByteAllow(4))
        self.checkBox_6Byte.clicked.connect(lambda: self.updateCheckByteAllow(6))
        self.checkBox_8Byte.clicked.connect(lambda: self.updateCheckByteAllow(8))
        self.checkBox_12Byte.clicked.connect(lambda: self.updateCheckByteAllow(12))
        self.checkBox_16Byte.clicked.connect(lambda: self.updateCheckByteAllow(16))

        self.checkBox_4Byte.setChecked(True)

        self.label.setText(language.operate_reader + "1")
        self.label_2.setText(language.operate_reader + "2")
        self.readerRebootBtn1.setText(language.operate_reboot)
        self.readerRebootBtn2.setText(language.operate_reboot)
        self.readerSetBtn1.setText(language.operate_setup)
        self.readerSetBtn2.setText(language.operate_setup)
        self.fanControlBtn_on.setText(language.operate_fanOn)
        self.fanControlBtn_off.setText(language.operate_fanOff)
        self.shutdownBtn.setText(language.operate_powerOff)
        self.returnBtn.setText(language.operate_back)
        self.stringStartReading = language.operate_start
        self.stringStopReading = language.operate_stop
        self.setWindowTitle('Operate')
        self.groupBox.setWindowTitle(language.operate_allowEpcBoxTitle)
        self.checkBox_2Byte.setText('2' + language.operate_byte)
        self.checkBox_4Byte.setText('4' + language.operate_byte)
        self.checkBox_6Byte.setText('6' + language.operate_byte)
        self.checkBox_8Byte.setText('8' + language.operate_byte)
        self.checkBox_12Byte.setText('12' + language.operate_byte)
        self.checkBox_16Byte.setText('16' + language.operate_byte)


        # 初始化按钮
        self.readControlBtn1Start.setText(self.stringStartReading)
        self.readControlBtn1Stop.setText(self.stringStopReading)
        self.readControlBtn2Start.setText(self.stringStartReading)
        self.readControlBtn2Stop.setText(self.stringStopReading)

        # 初始化选择
        self.checkBox_2Byte.setChecked("2" in self.allowEpcByteLength)
        self.checkBox_4Byte.setChecked("4" in self.allowEpcByteLength)
        self.checkBox_6Byte.setChecked("6" in self.allowEpcByteLength)
        self.checkBox_8Byte.setChecked("8" in self.allowEpcByteLength)
        self.checkBox_12Byte.setChecked("12" in self.allowEpcByteLength)
        self.checkBox_16Byte.setChecked("16" in self.allowEpcByteLength)

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

    # 开始/暂停读取
    def startOrStopReading(self, readerId,cmd):
        self.sendEvent('UI', 'ui_startOrStropReading',
                       [str(readerId), cmd])  # 这里的参数是一个数组，['1',cmd]，这里cmd=on，开启，cmd=off，关闭，x不指定

    # 更新读取控制按钮的显示
    def updateReadingBtn(self, string):
        print(__file__, string)

    # 关机
    def shutdown(self):
        s = shutDown.ShutdownDialog(self.mainPage, self.eventQ)
        s.exec_()

    def fanControl(self, cmd):
        self.sendEvent('UART','uart_beep',0.1)
        time.sleep(0.1)
        self.sendEvent('UART', 'uart_fanControl', cmd)
        
        if cmd == 'on':
            os.system('echo %s | sudo -S %s' % ('100perica!!', 'gpio -g mode 18 pwm'))
        elif cmd == 'off':
            os.system('echo %s | sudo -S %s' % ('100perica!!', 'gpio -g mode 18 in'))

    # 重启读卡器1
    def rebootReader(self, readerId):
        if readerId == 1:
            self.sendEvent('UART', 'uart_reBootReader', [1])
        if readerId == 2:
            self.sendEvent('UART', 'uart_reBootReader', [2])

    # 启动设置读写器1
    def readerSet(self, readerId):
        s = readerSet.ReaderSetDialog(self.mainPage, self.eventQ, readerId)
        s.exec_()

    # 更新允许的字节数
    def updateCheckByteAllow(self, byteAllow):
        # 至少允许一个长度
        if len(self.allowEpcByteLength) == 1 and str(byteAllow) in self.allowEpcByteLength:
            self.updateCheckBox()
            return

        if str(byteAllow) not in self.allowEpcByteLength:
            self.allowEpcByteLength.append(str(byteAllow))
        else:
            while str(byteAllow) in self.allowEpcByteLength:
                self.allowEpcByteLength.remove(str(byteAllow))
        self.allowEpcByteLength = [int(x) for x in self.allowEpcByteLength]
        self.allowEpcByteLength.sort()
        self.allowEpcByteLength = [str(x) for x in self.allowEpcByteLength]
        print(__file__, self.allowEpcByteLength)
        text = ''
        for i in self.allowEpcByteLength:
            text += i + ','
        text = text.strip(',')
        self.machineConfig.write('reader', 'allowEpcByteLength', text)
        self.allowEpcByteLength = self.machineConfig.read('reader', 'allowEpcByteLength').split(',')

        self.sendEvent("UI", "ui_updateFieldsFromConfigFile", [])
        self.updateCheckBox()

    def updateCheckBox(self):
        self.checkBox_2Byte.setChecked("2" in self.allowEpcByteLength)
        self.checkBox_4Byte.setChecked("4" in self.allowEpcByteLength)
        self.checkBox_6Byte.setChecked("6" in self.allowEpcByteLength)
        self.checkBox_8Byte.setChecked("8" in self.allowEpcByteLength)
        self.checkBox_12Byte.setChecked("12" in self.allowEpcByteLength)
        self.checkBox_16Byte.setChecked("16" in self.allowEpcByteLength)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Operate(None, None, None, None)
    form.show()
    sys.exit(app.exec_())
