# -*- coding:utf-8 -*-

import sys
import os
import time
import random

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from uiFiles import ui_displaySetting

from gtyTools import gtyLog, gtyTypes
from gtyConfig import language, systemConfig
import uiTools
from gtyTools import tools



class DisplaySetting(QDialog, ui_displaySetting.Ui_displaySetting):
    def __init__(self, mainPage, eventQ, parent=None):
        super(DisplaySetting, self).__init__(parent)
        self.setupUi(self)
        uiTools.centerAndSetIcon(self)
        self.mainPage = mainPage
        self.eventQ = eventQ
        
        self.configHandlers = gtyTypes.ConfigHandlers()
        self.brightnessValue = int(self.configHandlers.machine.read("display", "brightness"))
        self.powersaveValue = int(self.configHandlers.machine.read("display", "powersave"))
        
        self.language = language.lanFromFile()
        self.label.setText(language.display_brightness)
        self.label_2.setText(language.display_powersave)
        self.returnBtn.setText(language.display_back)
        
        self.brightness_horizontalSlider.sliderReleased.connect(self.setBrightnessValue)
        self.brightness_horizontalSlider.setValue(self.brightnessValue)
        if self.powersaveValue == 0:
            self.radioButton.setChecked(True)
        elif self.powersaveValue == 30:
            self.radioButton_2.setChecked(True)
        elif self.powersaveValue == 60:
            self.radioButton_3.setChecked(True)
        elif self.powersaveValue == 90:
            self.radioButton_4.setChecked(True)
        elif self.powersaveValue == 120:
            self.radioButton.setChecked(True)
            
        self.radioButton.toggled.connect(lambda:self.rbt_toggled(self.radioButton))
        self.radioButton_2.toggled.connect(lambda:self.rbt_toggled(self.radioButton_2))
        self.radioButton_3.toggled.connect(lambda:self.rbt_toggled(self.radioButton_3))
        self.radioButton_4.toggled.connect(lambda:self.rbt_toggled(self.radioButton_4))
        self.radioButton_5.toggled.connect(lambda:self.rbt_toggled(self.radioButton_5))

        self.setWindowTitle("Display setting")
        
        
        
    # 发生事件
    def sendEvent(self, task, eventName, eventData=None):
        if eventData is None:
            eventData = []
        e = [eventName, eventData]
        print(__file__, task, e)
        try:
            if task.upper() in self.eventQ.keys():
                print(__file__, "1", e, self.eventQ)
                self.eventQ[task.upper()].put(e)
        except Exception as e:
            print(e)
            
        
    def setBrightnessValue(self):
        self.brightnessValue = self.brightness_horizontalSlider.value()
        if self.brightnessValue <= 25:
            self.brightnessValue = 25
        elif self.brightnessValue >= 250:
            self.brightnessValue = 255
        self.configHandlers.machine.write('display', 'brightness', str(self.brightnessValue))
        if os.path.exists('/sys/class/backlight/10-0045/brightness'):
            os.system('echo '+ str(self.brightnessValue) + ' | sudo tee /sys/class/backlight/10-0045/brightness')
        else:
            self.label_3.setText('set brightness failed')
        
    
    def rbt_toggled(self,button):
        rbtext = button.text()
        if rbtext == 'off':
            self.powersaveValue = 0
        elif rbtext == '30s':
            self.powersaveValue = 30
        elif rbtext == '60s':
            self.powersaveValue = 60
        elif rbtext == '90s':
            self.powersaveValue = 90
        elif rbtext == '120s':
            self.powersaveValue = 120
        self.configHandlers.machine.write('display', 'powersave', self.powersaveValue)
        self.sendEvent('UI', 'ui_powerSaveValueSet', self.powersaveValue)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DisplaySetting(None, None, None, None)
    form.show()
    sys.exit(app.exec_())