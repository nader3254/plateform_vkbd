# -*- coding:utf-8 -*-

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog

from uiFiles import ui_eventSettingDialog
import os
from gtyTools import gtyLog, gtyTypes,virtualKbd
import time
import random
from gtyConfig import language, systemConfig
import uiTools
from gtyTools import tools




class EventSettingDialog(QDialog, ui_eventSettingDialog.Ui_eventSettingDialog):

    def __init__(self, mainPage, eventQ, parent=None):
        super(EventSettingDialog, self).__init__(parent)

        self.setupUi(self)
        #uiTools.centerAndSetIcon(self)
        self.setWindowIcon(QIcon(systemConfig.param.windowLogoPath))
        self.mainPage = mainPage
        self.eventQ = eventQ

        # 配置文件对象
        self.configHandlers = gtyTypes.ConfigHandlers()
        self.releaseMode = self.configHandlers.state.read("machine", "releaseMode")
        self.machineId = self.configHandlers.machine.read("machine", "machineId")
        self.readerId = self.configHandlers.machine.read("event", "readerId")
        self.tokenId = self.configHandlers.machine.read("event", "tokenId")
        self.eventId = self.configHandlers.machine.read("event", "eventId")
        self.eventName = self.configHandlers.machine.read("event", "eventName")
        self.machinePosition = ""
        self.configFileName = ""
        self.recordFileDir = ""
        self.updateEventConfigInfo()
        self.label_eventName.setText(self.eventName)
        self.lineEditReaderId.setText(self.readerId)
        self.lineEditEventId.setText(self.eventId)
        self.lineEditTokenId.setText(self.tokenId)

        # Virtual Keyboard Registering
        virtualKbd.Registe(self.lineEditReaderId)
        virtualKbd.Registe(self.lineEditEventId)
        virtualKbd.Registe(self.lineEditTokenId)

        # 建立连接
        self.downloadConfigFileButton.clicked.connect(self.downloadConfigFileFromServer)
        self.eraseRecordDataBtn.clicked.connect(self.deleteRecord)
        self.btnSetEventId.clicked.connect(self.setEventId)
        self.btnSetTokenId.clicked.connect(self.setTokenId)
        self.btnSetReaderId.clicked.connect(self.setReaderId)
        
        

        self.mainPage.eventEngine.eventList["ui_updateCurrentEventConfigFileName"].connect(self.updateEventConfigInfo)  # 刷新配置信息
        self.mainPage.eventEngine.eventList["ui_downloadEventConfigFileFromServer"].connect(self.loadConfigFileDownloadedFromServer)
        self.mainPage.eventEngine.eventList["ui_updateDisplayStatus"].connect(self.displayStatus)
        
        
        #
        if self.releaseMode == 'release':
            self.eraseRecordDataBtn.setHidden(True)

        # 处理不同的语言
        self.language = language.lanFromFile()

        self.label_19.setText(language.eventSetting_eventId)
        self.label_17.setText(language.eventSetting_eventName)
        self.label_21.setText(language.eventSetting_recordFile)
        self.eraseRecordDataBtn.setText(language.eventSetting_deleteDataFile)
        self.downloadConfigFileButton.setText(language.eventSetting_downLoadConfigFile)
        self.returnButton.setText(language.eventSetting_back)
        self.label_22.setText(language.eventSetting_readerId)
        self.label_23.setText(language.eventSetting_tokenId)
        self.btnSetEventId.setText(language.eventSetting_set)
        self.btnSetTokenId.setText(language.eventSetting_set)
        self.btnSetReaderId.setText(language.eventSetting_set)
                
        self.setWindowTitle("Race")
        

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

    # 从U盘复制配置文件
    def readConfigFileFromU(self):
        print('readConfigFileFromU')
        # 1. 获取了新的配置文件文件名
        res = QFileDialog.getOpenFileName(self, '选择文件', systemConfig.configFilePath
                                          , 'event config files(*.ecg)')
        eventConfigFileName = res[0]
        if '.ecg' not in eventConfigFileName:
            return
        eventConfigFileNameWithoutPath = eventConfigFileName.split('/')[-1]
        self.label_configFile.setText(eventConfigFileNameWithoutPath)
        print(__file__, eventConfigFileNameWithoutPath)
        # 2. 删除原来的配置文件
        cmd = str('cp ' + eventConfigFileName + ' ' + os.path.join(systemConfig.configFilePath
                                                                   , 'newEventConfigFile'))
        os.system(cmd)
        os.system('rm ' + os.path.join(systemConfig.configFilePath, 'ec_*.ecg'))
        # 3. 将这个文件复制到config目录下
        cmd = str('mv ' + os.path.join(systemConfig.configFilePath, 'newEventConfigFile') + ' ' +
                  os.path.join(systemConfig.configFilePath, eventConfigFileNameWithoutPath))
        os.system(cmd)
        # 4. 加载赛事配置文件的内容
        self.sendEvent('IO', 'file_loadEventConfigFile', eventConfigFileNameWithoutPath)
        self.sendEvent('UI', 'ui_loadEventConfigFile', eventConfigFileNameWithoutPath)
        self.updateEventConfigInfo()
        # 5. 显示读取成功
        dis = time.strftime('%Y-%m-%d %H:%M:%S, read successfully ', time.localtime(time.time()))
        self.label_display.setText(dis + eventConfigFileNameWithoutPath)

    # 更新这个页面的显示
    def updateEventConfigInfo(self):
        try:
            self.configHandlers = gtyTypes.ConfigHandlers()
            self.machineId = self.configHandlers.machine.read("machine", "machineId")
            self.eventId = self.configHandlers.machine.read("event", "eventId")
            self.eventName = self.configHandlers.machine.read("event", "eventName")
            self.readerId = self.configHandlers.machine.read("event", "readerId")
            self.tokenId = self.configHandlers.machine.read("event", "tokenId")
            self.recordFileDir = os.path.join(self.configHandlers.machine.read("IO", "dataFileDir"), self.machineId + "_" + self.eventId)
            self.label_recordFile.setText(self.recordFileDir)
            # 数据库对象
            self.label_eventName.setText(self.eventName)
            self.lineEditEventId.setText(self.eventId)
            self.lineEditTokenId.setText(self.tokenId)
            self.lineEditReaderId.setText(self.readerId)
        except Exception as e:
            gtyLog.log.write(__file__, e)
            pass

    # 从服务器下载配置文件
    def downloadConfigFileFromServer(self):
        # 创建一个下载事件交给IO进程去下载
        self.sendEvent('IO', 'web_downloadEventConfigFileFromServer', [self.machineId,self.eventId])

    # 下载配置文件完成后的处理
    def loadConfigFileDownloadedFromServer(self, configFileName):
        if 'failed' not in configFileName:
            # 1. 加载赛事配置文件的内容
            self.sendEvent('IO', 'file_loadEventConfigFile', configFileName)
            self.label_display.setText(configFileName + '    download config file Successfully！')
        else:
            print('down load config file failed')
            if configFileName == 'failed':
                self.label_display.setText('Download Config File Failed！')
            else:
                self.label_display.setText('failed: machine not in event.')

    # 上传比赛记录到服务器，上传全部文件
    def uploadRecordFileToServer(self):
        self.uploadRecordFileButton.setDisabled(True)
        self.uploadRecordFileButton.setStyleSheet(systemConfig.param.btnDisabledStyle)
        self.sendEvent('IO', 'web_uploadFileToServer', [True])
        self.label_display.setText("Uploading files to server...")
        print(__file__,"uploadRecordFileToServer")

    # 更新上传结果文件是否成功
    def handleFileUploadResult(self, list):
        import time
        dis = time.strftime('%Y-%m-%d %H:%M:%S, ', time.localtime(time.time()))
        if list[0] == 'successful':
            self.label_display.setText(dis + language.mainPage_dataFileUploadSuccessful+". "+list[1]+".")
        else:
            self.label_display.setText(dis + language.mainPage_dataFileUploadFailed)
        self.uploadRecordFileButton.setEnabled(True)
        self.uploadRecordFileButton.setStyleSheet(systemConfig.param.btnEnabledStyle)

    # 删除数据文件
    def deleteRecord(self):
        self.sendEvent("IO", "io_deleteDataFile", [])
        pass
    
    def setEventId(self):
        eventId = self.lineEditEventId.text()
        if 0 <= int(eventId) <= 9999:
            self.configHandlers.machine.write('event', 'eventId', eventId)
            self.eventId = eventId
            self.lineEditEventId.setText(self.eventId)
            self.label_display.setText("Set race id ok!")
        else:
            self.label_display.setText("Set race id wrong!")
            
    def setTokenId(self):
        tokenId = self.lineEditTokenId.text()
        if 0 <= int(tokenId) <= 999999:
            self.configHandlers.machine.write('event', 'tokenId', tokenId)
            self.tokenId = tokenId
            self.lineEditTokenId.setText(self.tokenId)
            self.label_display.setText("Set token id ok!")
        else:
            self.label_display.setText("Set token id wrong!")
            
    def setReaderId(self):
        readerId = self.lineEditReaderId.text()
        if 0 <= int(readerId) <= 100:
            self.configHandlers.machine.write('event', 'readerId', readerId)
            self.readerId = readerId
            self.lineEditReaderId.setText(self.readerId)
            self.label_display.setText("Set reader id ok!")
        else:
            self.label_display.setText("Set reader id wrong!")
            
    def displayStatus(self,status):
        if status == 200:
            self.label_display.setText("check race success!")
        else:
            self.label_display.setText("check race failed!")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = EventSettingDialog(None, None, None, None)
    form.show()
    sys.exit(app.exec_())
