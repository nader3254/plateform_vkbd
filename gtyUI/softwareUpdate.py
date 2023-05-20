# -*- coding:utf-8 -*-

import sys
import time

from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog

from uiFiles import ui_softwareUpdate

from gtyConfig import language
import uiTools


class SoftwareUpdate(QDialog, ui_softwareUpdate.Ui_softWareUpdate):

    def __init__(self, mainPage, eventQ, parent=None):
        super(SoftwareUpdate, self).__init__(parent)
        self.setupUi(self)
        uiTools.centerAndSetIcon(self)

        self.eventQ = eventQ
        self.mainPage = mainPage

        self.setWindowTitle('software update')
        self.selectBtn.setText(language.softwareUpdate_select)
        self.programFirmwareBtn.setText(language.softwareUpdate_write)
        self.returnBtn.setText(language.softwareUpdate_back)
        self.progressBar.setValue(0)

        self.programFirmwareBtn.clicked.connect(self.updateStm32Firmware)
        self.returnBtn.clicked.connect(self.reject)

        self.mainPage.eventEngine.eventList["ui_getFirmwareVersion"].connect(self.showNewFirmwareVersion)
        self.mainPage.eventEngine.eventList["ui_stm32UpdateProgress"].connect(self.refreshStm32UpdateProgress)
        self.mainPage.eventEngine.eventList["ui_stm32UpdateComplete"].connect(self.stm32UpdateComplete)

        self.selectBtn.clicked.connect(self.selectFirmware)

        # 获取网络上的软件版本信息
        self.sendEvent('IO', 'web_getNewestSoftwareVersion')

        # 变量
        self.firmwarePath = ''

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

    # 选择固件文件
    def selectFirmware(self):
        res = QFileDialog.getOpenFileName(self, '选择文件', '/home/feibot/platform/', 'firmware file(*.bin)')
        print(__file__,"firmware",res)
        self.firmwarePath = res[0]
        if 'platform' not in self.firmwarePath or '.bin' not in self.firmwarePath:
            self.label_states.setText("wrong firmware file!")
            self.firmwarePath = ''
        else:
            self.label_states.setText("firmware file selected!")

    # 执行固件升级的命令
    def updateStm32Firmware(self):
        if 'platform' in self.firmwarePath and '.bin' in self.firmwarePath:
            self.label_states.setText("start program firmware!")
            print('updateStm32Firmware clicked')
            self.sendEvent('UART', 'uart_updateStm32Firmware',[self.firmwarePath])
        else:
            self.label_states.setText("firmware file not selected!")

    # 刷新stm32的升级进度
    def refreshStm32UpdateProgress(self, data):
        percentage = data[0]
        if percentage > 99.0:
            percentage = 100.0
        self.progressBar.setValue(percentage)

    # stm32固件升级完成
    def stm32UpdateComplete(self):
        self.label_states.setText('firmware update successfully complete!')
        time.sleep(5)
        self.sendEvent('UART', 'uart_askFirmwareVersion')
        self.sendEvent('UART', 'uart_askFirmwareVersion')
        self.sendEvent('UART', 'uart_askFirmwareVersion')

    # 显示新的固件版本号
    def showNewFirmwareVersion(self,data):
        print(__file__,"show new firmware version",data)
        firmwareString = str(data[0])+'.'+str(data[1])
        info = "\nNew firmware version is " + firmwareString
        if "version" not in self.label_states.text():
            self.label_states.setText(self.label_states.text()+info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SoftwareUpdate(None, None, None, None)
    form.show()
    sys.exit(app.exec_())
