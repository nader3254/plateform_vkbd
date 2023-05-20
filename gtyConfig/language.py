# -*- coding:utf-8 -*-


from . import configFileHandler
from . import systemConfig
import os

cf = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)
language = cf.read("language", "displayLanguage", "string", "chinese")

l = configFileHandler.ConfigFileHandler(os.path.join(systemConfig.languageFilePath, language + "Config.ini"))


def lanFromFile():
    if not language:
        return 'chinese'
    else:
        return language


# 主页面：
mainPage_label3 = l.read('mainDialog', 'dataInWait')
mainPage_label = l.read('mainDialog', 'localT')
mainPage_label5 = l.read('mainDialog', 'passedT')
mainPage_label23 = l.read('mainDialog', 'machineId')
mainPage_label9 = l.read('mainDialog', 'tagTotal')
mainPage_label11 = l.read('mainDialog', 'tagDiff')
mainPage_label13 = l.read('mainDialog', 'server')
mainPage_label21 = l.read('mainDialog', 'batLife')
mainPage_configButton = l.read('mainDialog', 'configButton')
mainPage_resetDataButton = l.read('mainDialog', 'resetDataButton')
mainPage_label25_max = l.read('mainDialog', 'max')
mainPage_label25_min = l.read('mainDialog', 'min')
mainPage_label14_connected = l.read('mainDialog', 'connected')
mainPage_label14_connectedWithoutServer = l.read('mainDialog', 'connectedWithoutServer')
mainPage_label14_disconnected = l.read('mainDialog', 'disconnected')
mainPage_reading = l.read('mainDialog', 'reading')
mainPage_stopReading = l.read('mainDialog', 'stopReading')
mainPage_TestMode = l.read('mainDialog', 'testMode')
mainPage_releaseMode = l.read('mainDialog', 'releaseMode')
mainPage_reader = l.read('mainDialog', 'reader')
mainPage_diskSpace1 = l.read('mainDialog', 'diskSpace1')
mainPage_diskSpace2 = l.read('mainDialog', 'diskSpace2')
mainPage_newSoftware = l.read('mainDialog', 'newSoftware')
mainPage_newFirmware = l.read('mainDialog', 'newFirmware')
mainPage_dataFileUploadSuccessful = l.read('mainDialog', 'dataFileUploadSuccessful')
mainPage_dataFileUploadFailed = l.read('mainDialog', 'dataFileUploadFailed')

config_event = l.read('config', 'event')
config_machine = l.read('config', 'machine')
config_functions = l.read('config', 'functions')
config_about = l.read('config', 'about')
config_return = l.read('config', 'return')

eventSetting_eventId = l.read('eventSetting', 'eventId')
eventSetting_eventName = l.read('eventSetting', 'eventName')
eventSetting_machinePosition = l.read('eventSetting', 'machinePosition')
eventSetting_configFile = l.read('eventSetting', 'configFile')
eventSetting_recordFile = l.read('eventSetting', 'recordFile')
eventSetting_readConfigFileFromDisk = l.read('eventSetting', 'readConfigFileFromDisk')
eventSetting_downLoadConfigFile = l.read('eventSetting', 'downLoadConfigFile')
eventSetting_uploadFile = l.read('eventSetting', 'uploadFile')
eventSetting_back = l.read('eventSetting', 'back')
eventSetting_deleteDataFile = l.read('eventSetting', 'deleteDataFile')
eventSetting_readerId = l.read('eventSetting','readerId')
eventSetting_tokenId = l.read('eventSetting','tokenId')
eventSetting_set = l.read('eventSetting','set')

configMachine_operate = l.read('configMachine', 'operate')
configMachine_timeDateSetting = l.read('configMachine', 'timeDateSetting')
configMachine_networkSetting = l.read('configMachine', 'networkSetting')
configMachine_softwareUpdate = l.read('configMachine', 'softwareUpdate')
configMachine_back = l.read('configMachine', 'back')
configMachine_displaySetting = l.read('configMachine','displaySetting')

operate_reader = l.read('operate', 'reader')
operate_start = l.read('operate', 'start')
operate_stop = l.read('operate', 'stop')
operate_reboot = l.read('operate', 'reboot')
operate_setup = l.read('operate', 'setup')
operate_allowEpcBoxTitle = l.read('operate', 'allowEpcBoxTitle')
operate_byte = l.read('operate', 'byte')
operate_fanOn = l.read('operate', 'fanOn')
operate_fanOff = l.read('operate', 'fanOff')
operate_powerOff = l.read('operate', 'powerOff')
operate_back = l.read('operate', 'back')

about_softwareVersion = l.read('about', 'softwareVersion')
about_firmwareVersion = l.read('about', 'firmwareVersion')
about_testMode = l.read('about', 'testMode')
about_normalMode = l.read('about', 'normalMode')
about_back = l.read('about', 'back')

timeSetting_year = l.read('timeSetting', 'year')
timeSetting_month = l.read('timeSetting', 'month')
timeSetting_day = l.read('timeSetting', 'day')
timeSetting_hour = l.read('timeSetting', 'hour')
timeSetting_minute = l.read('timeSetting', 'minute')
timeSetting_second = l.read('timeSetting', 'second')
timeSetting_ntpTime = l.read('timeSetting', 'ntpTime')
timeSetting_setNtpTime = l.read('timeSetting', 'setNtpTime')
timeSetting_wirelessTimeSynch = l.read('timeSetting', 'wirelessTimeSynch')
timeSetting_modifyTime = l.read('timeSetting', 'modifyTime')
timeSetting_setTime = l.read('timeSetting', 'setTime')
timeSetting_setDate = l.read('timeSetting', 'setDate')
timeSetting_back = l.read('timeSetting', 'back')
timeSetting_send = l.read('timeSetting', 'send')
timeSetting_receive = l.read('timeSetting', 'receive')
timeSetting_wirelessTimeSignal = l.read('timeSetting', 'wirelessTimeSignal')
timeSetting_ntpEnable = l.read('timeSetting', 'ntpOn')
timeSetting_ntpDisable = l.read('timeSetting', 'ntpOff')

networkSetting_ipAddress = l.read('networkSetting', 'ipAddress')
networkSetting_udpTarget = l.read('networkSetting', 'udpTarget')
networkSetting_targetIp = l.read('networkSetting', 'targetIp')
networkSetting_targetPort = l.read('networkSetting', 'targetPort')
networkSetting_set = l.read('networkSetting', 'set')
networkSetting_back = l.read('networkSetting', 'back')
networkSetting_connected = l.read('networkSetting', 'connected')
networkSetting_disconnected = l.read('networkSetting', 'disconnected')

softwareUpdate_select = l.read('softwareUpdate', 'select')
softwareUpdate_write = l.read('softwareUpdate', 'write')
softwareUpdate_back = l.read('softwareUpdate', 'back')

shutDown_info = l.read('shutDown', 'info')
shutDown_powerOff = l.read('shutDown', 'powerOff')
shutDown_reboot = l.read('shutDown', 'reboot')
shutDown_back = l.read('shutDown', 'back')

readerSetting_reader = l.read('readerSetting', 'reader')
readerSetting_setPower = l.read('readerSetting', 'setPower')
readerSetting_getPower = l.read('readerSetting', 'getPower')
readerSetting_band = l.read('readerSetting', 'band')
readerSetting_setFreq = l.read('readerSetting', 'setFreq')
readerSetting_getFreq = l.read('readerSetting', 'getFreq')
readerSetting_back = l.read('readerSetting', 'back')

display_brightness = l.read('displaySetting','brightness')
display_powersave = l.read('displaySetting','powersave')
display_back = l.read('displaySetting','back')