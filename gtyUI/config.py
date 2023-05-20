# -*- coding:utf-8 -*-

import sys
import traceback

from PyQt5.Qt import *
from PyQt5.QtCore import *

from gtyTools import gtyLog
from uiFiles import ui_config
import eventSettingDialog
import configMachineSelectDialog
import about
from gtyConfig import language, systemConfig

import uiTools


class Config(QDialog, ui_config.Ui_config):

    def __init__(self, mainPage, eventQ, parent=None):
        super(Config, self).__init__(parent)
        self.setupUi(self)
        uiTools.centerAndSetIcon(self)
        self.mainPage = mainPage
        self.eventQ = eventQ
        self.configEventButton.clicked.connect(self.configEvent)
        self.configMachineButton.clicked.connect(self.configMachine)
        self.aboutBtn.clicked.connect(self.about)

        self.configEventButton.setText(language.config_event)
        self.configMachineButton.setText(language.config_machine)
        self.functionBtn.setText(language.config_functions)
        self.aboutBtn.setText(language.config_about)
        self.backButton.setText(language.config_return)
        self.setWindowTitle("Config")

        # 处理不同的语言
        self.functionBtn.hide()
        

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

    # 配置赛事
    def configEvent(self):
        try:
            e = eventSettingDialog.EventSettingDialog(self.mainPage, self.eventQ)
            e.exec_()
        except Exception as ex:
            traceback.print_exc()
            gtyLog.log.write(__file__, ex)

    # 配置设备
    def configMachine(self):
        try:
            e = configMachineSelectDialog.ConfigMachineSelectDialog(self.mainPage, self.eventQ)
            if e.exec_():
                pass
        except Exception as ex:
            traceback.print_exc()
            gtyLog.log.write(__file__, ex)

    # 关于页面
    def about(self):
        try:
            e = about.About(self.mainPage, self.eventQ)
            if e.exec_():
                pass
        except Exception as ex:
            traceback.print_exc()
            gtyLog.log.write(__file__, ex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Config(None, None)
    form.show()
    sys.exit(app.exec_())
