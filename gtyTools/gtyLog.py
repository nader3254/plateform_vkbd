# -*- coding:utf-8 -*-

import os
import time
from gtyConfig import systemConfig, configFileHandler


class GtyLog:

    def __init__(self):
        self.logFile = None
        # 生成文件路径
        dateString = time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime(time.time()))
        fileName = 'log_' + dateString + '.txt'
        self.logFilePath = systemConfig.getLogFilePath(fileName)
        self.fileOpenSuccessful = False
        self.machineConfig = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)
        self.onlyOneLogFile = self.machineConfig.read('machine', 'onlyOneLogFile', 'int', 0)
        self.logEnable = self.machineConfig.read('machine', 'logEnable', 'int', 1)

    def openFile(self):
        # 是否使能了日志
        if self.logEnable == 0:
            return
        # 创建日志文件
        if not os.path.exists(self.logFilePath):
            # 如果只保留一个文件那么首先删除其他日志文件
            if self.onlyOneLogFile == 1:
                for file in os.listdir(systemConfig.getLogFilePath()):
                    if "log" in file and ".txt" in file:
                        os.remove(os.path.join(systemConfig.getLogFilePath(), file))
            # 创建文件
            try:
                with open(self.logFilePath, 'w', encoding='utf-8') as f:
                    pass
            except Exception as e:
                print(e)
        # 不存在就打开文件
        try:
            self.logFile = open(self.logFilePath, 'a')
            self.fileOpenSuccessful = True
            return True
        except Exception as e:
            print('create log error')
            print(e)
            return False

    # 写入日志
    def write(self, fName, msg1, msg2='', msg3='', msg4='', msg5='', msg6='', msg7='', msg8='', msg9='', msg10=''):
        # 是否使能了日志
        if self.logEnable == 0:
            return
        try:
            self.openFile()
            t = time.strftime('%m-%d %H:%M:%S ', time.localtime(time.time()))
            print(t, fName, msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9, msg10, file=self.logFile)
            # print(t, fName, msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9, msg10)
        except Exception as e:
            print(e)
            print('write log error')
        try:
            self.logFile.close()
        except Exception as e:
            print(e)


log = GtyLog()

if __name__ == '__main__':
    log.write(__file__, 'test')
