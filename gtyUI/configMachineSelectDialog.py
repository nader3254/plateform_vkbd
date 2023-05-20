# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QDialog, QApplication

from uiFiles import ui_machineSetting

import operate
import timeDateSetting
import softwareUpdate
from gtyConfig import language
import networkSetting
import uiTools
import displaySetting


class ConfigMachineSelectDialog(QDialog, ui_machineSetting.Ui_machineSetting):

    def __init__(self, mainPage, eventQ, parent=None):
        super(ConfigMachineSelectDialog, self).__init__(parent)
        self.setupUi(self)
        uiTools.centerAndSetIcon(self)
        self.mainPage = mainPage
        self.eventQ = eventQ


        # 建立链接
        self.operateBtn.clicked.connect(self.operate)
        self.timeDateSettingBtn.clicked.connect(self.timeAndDateSetting)
        self.updateBtn.clicked.connect(self.softwareUpdateDialog)
        self.networkBtn.clicked.connect(self.networkSetting)
        self.displayBtn.clicked.connect(self.displaySetting)

        # 处理不同的语言
        self.operateBtn.setText(language.configMachine_operate)
        self.timeDateSettingBtn.setText(language.configMachine_timeDateSetting)
        self.updateBtn.setText(language.configMachine_softwareUpdate)
        self.networkBtn.setText(language.configMachine_networkSetting)
        self.returnBtn.setText(language.configMachine_back)
        self.displayBtn.setText(language.configMachine_displaySetting)
        self.setWindowTitle("Machine Config")

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

    # 操作
    def operate(self):
        e = operate.Operate(self.mainPage, self.eventQ)
        if e.exec_():
            pass

    # 时间日期设置
    def timeAndDateSetting(self):
        e = timeDateSetting.TimeDateSetting(self.mainPage, self.eventQ)
        if e.exec_():
            pass

    # 软件升级
    def softwareUpdateDialog(self):
        e = softwareUpdate.SoftwareUpdate(self.mainPage, self.eventQ)
        if e.exec_():
            pass

    # 网络设置
    def networkSetting(self):
        e = networkSetting.NetworkSetting(self.mainPage, self.eventQ)
        if e.exec_():
            pass
        
    # 屏幕设置
    def displaySetting(self):
        e = displaySetting.DisplaySetting(self.mainPage, self.eventQ)
        if e.exec_():
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ConfigMachineSelectDialog(None, None, None, None)
    form.show()
    sys.exit(app.exec_())
