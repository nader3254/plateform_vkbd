# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QDialog, QApplication

from uiFiles import ui_shutdownDialog

from gtyConfig import language
import uiTools


class ShutdownDialog(QDialog, ui_shutdownDialog.Ui_shutDownDialog):

    def __init__(self, mainPage, eventQ, parent=None):
        super(ShutdownDialog, self).__init__(parent)
        self.setupUi(self)
        uiTools.centerAndSetIcon(self)
        self.eventQ = eventQ
        self.mainPage = mainPage
        self.mode = ''
        self.shutdownBtn.clicked.connect(self.powerOff)
        self.rebootBtn.clicked.connect(self.reboot)
        self.setWindowTitle('Shut Down')
        # 处理不同的语言
        self.label.setText(language.shutDown_info)
        self.shutdownBtn.setText(language.shutDown_powerOff)
        self.rebootBtn.setText(language.shutDown_reboot)
        self.returnBtn.setText(language.shutDown_back)

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

    # 设置为关机
    def powerOff(self):
        self.mode = 'powerOff'
        self.sendEvent('UI', 'ui_powerControl', 'powerOff')
        self.close()

    # 设置为重启
    def reboot(self):
        self.mode = 'reboot'
        self.sendEvent('UI', 'ui_powerControl', 'reboot')
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ShutdownDialog(None, None, None, None)
    form.show()
    sys.exit(app.exec_())
