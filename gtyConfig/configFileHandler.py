# -*- coding:utf-8 -*-

import systemConfig
import configparser
import re
import os
import shutil

newLine = re.compile(r'\\n')


# 重载配置接口类，解决：1. 不区分大小写，2. 写入时配置文件中的注释丢失
class gtyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None, dict_type=dict, allow_no_value=True):
        configparser.ConfigParser.__init__(self, defaults, dict_type, allow_no_value)

    def optionxform(self, optionStr):
        return optionStr


def replaceText(path, aim, replace):
    lines = open(path).readlines()
    fp = open(path, 'w')
    for s in lines:
        fp.write(s.replace(aim, replace))
    fp.close()


g_aim = "#"
g_replace = "@"


# 对于配置文件的操作
class ConfigFileHandler:

    def __init__(self, fileName=systemConfig.machineConfigFilePath):
        self.config = gtyConfigParser()
        self.configFileName = fileName
        self.data = None
        self.openConfigFile(fileName)

    def openConfigFile(self, fileName=None):
        if fileName is None:
            fileName = self.configFileName
        try:
            self.config.read(fileName, encoding="utf-8")
        except Exception as e:
            print(e)
            print("open config file failed :" + fileName)

    # 读取数据
    def read(self, section, option, returnType="string", defaultValue=None):
        if defaultValue is None:
            if returnType == "string":
                defaultValue = ""
            if returnType == "int" or returnType == "float":
                defaultValue = 0
            if returnType == "bool":
                defaultValue = False
        try:
            if returnType == "string":
                s = self.config.get(section, option)
                if s == "":
                    return defaultValue
                return newLine.sub('\n', s)
            if returnType == "int":
                s = self.config.get(section, option)
                if s == "":
                    return defaultValue
                return int(s)
            if returnType == "float":
                s = self.config.get(section, option)
                if s == "":
                    return defaultValue
                return float(s)
            if returnType == "bool":
                s = self.config.get(section, option)
                if s in ['0', '']:
                    return False
                else:
                    return True

        except Exception as e:
            print(e)
            return defaultValue

    # 写入数据
    def write(self, section, option, value, valueType="string"):
        # 对于布尔型，转字符串
        if valueType == 'bool':
            if value:
                value = '1'
            else:
                value = '0'
                # 生成备用配置文件
        configPath = self.configFileName
        if '.ecg' not in self.configFileName:
            # 生成备用配置文件
            backConfigPath = self.configFileName + ".bak"
            shutil.copyfile(configPath, backConfigPath)
            # 替换注释
            replaceText(backConfigPath, g_aim, g_replace)
        else:
            backConfigPath = self.configFileName
        # 读取备用配置文件
        self.config.read(backConfigPath, encoding="utf-8")
        self.config.set(section, option, str(value))
        # 写入配置文件
        self.config.write(open(self.configFileName, 'w'))
        replaceText(self.configFileName, g_replace, g_aim)
        # 删除备用配置文件
        if '.ecg' not in self.configFileName:
            try:
                os.system("rm " + backConfigPath)
            except Exception as e:
                print(e)
                pass
        # 重新打开配置文件
        self.openConfigFile(self.configFileName)


if __name__ == "__main__":
    c = ConfigFileHandler(systemConfig.machineConfigFilePath)
    print(c.read("machine", "onlyOneLogFile"))
    c.write("machine", "onlyOneLogFile", 1)
