# -*- coding:utf-8 -*-
# 系统配置，用于系统级别的配置，不能被用户轻易更改
import os

from gtyConfig import configFileHandler


# 参数，这里可以修改
class Params:
    def __init__(self):
        self.configFilesPath = "configFiles"
        self.machineConfigFileName = "machineConfig.ini"
        self.runStateFileName = "runState.ini"
        self.languageFileName = "language"
        self.logFilePath = "/home/stoperica/data/log/"
        self.windowLogoPath = "/home/stoperica/platform/resources/feibot_logo_2.jpg"

        # 按钮的颜色
        self.btnEnabledStyle = "background-color:#424f83;"
        self.btnDisabledStyle = "background-color:#333333;"
        self.btnHighLightStyle = "background-color:#ffb579;"


param = Params()

# 版本
softwareVersion = '1.0.0.0513_base'
lowestFirmware = '40.10'
# linux密码
passwd = '100perica!!'
# 方法
parent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
configFilePath = os.path.join(parent_path, param.configFilesPath)
# 设备配置文件位置
machineConfigFilePath = os.path.join(configFilePath, param.machineConfigFileName)
# 运行中状态文件位置
runStateFilePath = os.path.join(configFilePath, param.runStateFileName)
# 语言配置文件位置
languageFilePath = os.path.join(configFilePath, param.languageFileName)


# 获取赛事配置文件地址
# 在指定目录下返回文件名最大的
def getEventConfigFilePath():
    stateConfig = configFileHandler.ConfigFileHandler(runStateFilePath)
    res = stateConfig.read('machine', 'eventConfigFileName')
    if '.ecg' in res:
        return os.path.join(configFilePath, res)
    else:
        files = os.listdir(configFilePath)
        eventConfigFiles = []
        for f in files:
            if 'ec_' in f and '.ecg' in f:
                eventConfigFiles.append(f)
        if len(eventConfigFiles) > 0:
            return os.path.join(configFilePath, max(eventConfigFiles))
        else:
            return ""


# 获取日志文件路径
def getLogFilePath(fileName=""):
    if fileName == "":
        return param.logFilePath
    else:
        return os.path.join(param.logFilePath, fileName)


