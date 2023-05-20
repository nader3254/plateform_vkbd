# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QDialog, QApplication

import gtyTools.RF_band
from uiFiles import ui_readerSet
import time
# from gtyConfig import language
import uiTools
from gtyTools import RF_band
from gtyConfig import language, configFileHandler, systemConfig


class ReaderSetDialog(QDialog, ui_readerSet.Ui_readerSetDialog):

    def __init__(self, mainPage, eventQ, readerId=1, parent=None):
        super(ReaderSetDialog, self).__init__(parent)
        self.setupUi(self)
        uiTools.centerAndSetIcon(self)
        self.eventQ = eventQ
        self.mainPage = mainPage
        self.mode = ''
        self.readerId = readerId
        self.power = 31
        self.machineConfig = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)
        self.allowReaderChannelLength = self.machineConfig.read("reader", "allowReaderChannelLength").split(',')

        self.mainPage.eventEngine.eventList["ui_getReaderPower"].connect(self.getReaderPower)

        self.powerAddBtn.clicked.connect(self.powerAdd)
        self.powerMinBtn.clicked.connect(self.powerMin)
        self.setPowerBtn.clicked.connect(self.setPower)
        self.getPowerBtn.clicked.connect(self.getPower)
        self.setFreqBtn.clicked.connect(self.setBand)
        self.getFreqBtn.clicked.connect(self.getBand)
        self.mainPage.eventEngine.eventList["ui_getFreqBand"].connect(self.updateFreqBand)
        
        # 读卡通道选择按钮
        self.checkBox_ch_1.clicked.connect(lambda: self.updateCheckCnannelAllow(1))
        self.checkBox_ch_2.clicked.connect(lambda: self.updateCheckCnannelAllow(2))
        self.checkBox_ch_3.clicked.connect(lambda: self.updateCheckCnannelAllow(3))
        self.checkBox_ch_4.clicked.connect(lambda: self.updateCheckCnannelAllow(4))
        # self.checkBox_ch_1.setChecked(True)
        self.checkBox_ch_1.setChecked("1" in self.allowReaderChannelLength)
        self.checkBox_ch_2.setChecked("2" in self.allowReaderChannelLength)
        self.checkBox_ch_3.setChecked("3" in self.allowReaderChannelLength)
        self.checkBox_ch_4.setChecked("4" in self.allowReaderChannelLength)


        self.setWindowTitle("Reader"+str(readerId)+" Setting")
        # language
        # 处理不同的语言
        self.label.setText(language.readerSetting_reader)
        self.strSetReaderPower = ': Set reader power '
        self.strReadReaderPower = ': Read reader power '
        self.strSetBand = ': Set reader band '
        self.strReadBand = ': Read reader band '
        self.setPowerBtn.setText(language.readerSetting_setPower)
        self.getPowerBtn.setText(language.readerSetting_getPower)
        self.returnBtn.setText(language.readerSetting_back)
        self.label_1.setText(language.readerSetting_band)
        self.setFreqBtn.setText(language.readerSetting_setFreq)
        self.getFreqBtn.setText(language.readerSetting_getFreq)
        self.label_power.setText('30')

        # 频率复选框
        self.rfBand = gtyTools.RF_band.RF_BAND()
        self.FreqComboBox.addItems(self.rfBand.getBandList())

        # 获取读写器功率
        self.getPower()
        time.sleep(0.1)
        self.getBand()

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

    # 获取了读写器的功率
    def getReaderPower(self, d):
        readerId = int(d[0])
        print(__file__, d)
        if int(self.readerId) == readerId:
            self.label_power.setText(str(d[1]))
            self.power = int(d[1])

    # 功率加减
    def powerAdd(self):
        if self.power + 1 <= 33:
            self.power += 1
        self.label_power.setText(str(self.power))

    # 功率加减
    def powerMin(self):
        if self.power - 1 >= 5:
            self.power -= 1
        self.label_power.setText(str(self.power))

    # 设置读写功率
    def setPower(self):
        power = int(self.label_power.text())
        self.sendEvent('UART', 'uart_setReaderPower', [int(self.readerId) + 2, power])  # 设置读卡功率
        self.label_info.setText(time.strftime('%H:%M:%S', time.localtime(time.time())) + self.strReadReaderPower)

    # 读取读写功率
    def getPower(self):
        self.sendEvent('UART', 'uart_getReaderPower', int(self.readerId) + 2)  # 读取读卡功率
        self.label_info.setText(time.strftime('%H:%M:%S', time.localtime(time.time())) + self.strSetReaderPower)

    # 获得读写器频段
    def getBand(self):
        self.sendEvent('UART','uart_freqBand',[0,int(self.readerId)+2])
        self.label_info.setText(time.strftime('%H:%M:%S', time.localtime(time.time())) + self.strReadBand)

    # 设置读写器频段
    def setBand(self):
        bandId = self.FreqComboBox.currentIndex()
        self.sendEvent('UART','uart_freqBand',[1,bandId])
        print(__file__,'set freq band:',bandId)
        self.label_info.setText(time.strftime('%H:%M:%S', time.localtime(time.time())) + self.strSetBand)
        pass

    def updateFreqBand(self,dataList):
        print(__file__,'updateFreqBand:',dataList)
        band = dataList[0]
        self.FreqComboBox.setCurrentText(self.rfBand.bandDict[band])
        
    
    # 更新允许的字节数
    def updateCheckCnannelAllow(self, chAllow):
        # 至少允许一个长度
        if len(self.allowReaderChannelLength) == 1 and str(chAllow) in self.allowReaderChannelLength:
            self.updateCheckBox()
            return

        if str(chAllow) not in self.allowReaderChannelLength:
            self.allowReaderChannelLength.append(str(chAllow))
        else:
            while str(chAllow) in self.allowReaderChannelLength:
                self.allowReaderChannelLength.remove(str(chAllow))
        self.allowReaderChannelLength = [int(x) for x in self.allowReaderChannelLength]
        self.allowReaderChannelLength.sort()
        self.allowReaderChannelLength = [str(x) for x in self.allowReaderChannelLength]
        print(__file__, self.allowReaderChannelLength)
        text = ''
        for i in self.allowReaderChannelLength:
            text += i + ','
        text = text.strip(',')
        self.machineConfig.write('reader', 'allowReaderChannelLength', text)
        self.allowReaderChannelLength = self.machineConfig.read('reader', 'allowReaderChannelLength').split(',')

        # self.sendEvent("UI", "ui_updateFieldsFromConfigFile", [])
        self.updateCheckBox()

    def updateCheckBox(self):
        self.checkBox_ch_1.setChecked("1" in self.allowReaderChannelLength)
        self.checkBox_ch_2.setChecked("2" in self.allowReaderChannelLength)
        self.checkBox_ch_3.setChecked("3" in self.allowReaderChannelLength)
        self.checkBox_ch_4.setChecked("4" in self.allowReaderChannelLength)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ReaderSetDialog(None, None, None, None)
    form.show()
    sys.exit(app.exec_())
