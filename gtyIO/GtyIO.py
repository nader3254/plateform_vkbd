# -*- coding:utf-8 -*-

"""
    这是IO类

"""

import random
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from multiprocessing import *

from gtyTools import gtyLog, tools, gtyTypes
from . import gtyIoTools
import os
import recordFileHandle
import ssl



ssl._create_default_https_context = ssl._create_unverified_context

class GtyIO:

    def __init__(self, eventQ):

        # 事件队列
        self.eventQ = eventQ
        # 配置的控制接口
        self.configHandlers = gtyTypes.ConfigHandlers()

        # 线程创建时
        self.machineId = self.configHandlers.machine.read("machine", "machineId")

        self.eventId = self.configHandlers.event.read("event", "eventId")

        # 数据文件对象
        self.recordFile = recordFileHandle.RecordFileHandle()

        # # 网络相关
        self.serverLocation = self.configHandlers.machine.read("server", "serverLocation")
        
        if self.serverLocation[-1] != '/':
            self.serverLocation += "/"

        self.cpDataUploadUrl = self.configHandlers.machine.read("server", "cpDataUploadUrl")

        # 从配置文件中读出时间间隔
        self.uploadDataIntervalSecond = max(2, self.configHandlers.machine.read("IO", "uploadDataIntervalSecond", "int", 5))

        self.uploadDataFileIntervalSecond = max(30, self.configHandlers.machine.read("IO", "uploadDataFileIntervalSecond", "int", 180))

        # 每次上传到服务器最多芯片条数
        self.maxTagNumPerWebRequest = self.configHandlers.machine.read("IO", "maxTagNumPerWebRequest", "int", 200)

        # 当前是否能上网
        self.serverConnection = 'disconnected'

        # 启动事件引擎
        self.localEventEngine = threading.Thread(target=self.eventEngine)
        self.localEventEngine.start()

        # 待保存和上传的数据
        self.data2File = []
        self.data2Web = []
        self.data2WebTemp = []  # 上传数据暂存列表

        # 需要上传数据文件的标志
        self.dataFileNeedUploadFlag = True

    # 这里是一些自发的事件
    def start(self):
        localCounter = 0
        while True:
            localCounter += 1
            # 每1秒将数据存入文件
            self.sendEvent('IO', 'file_writeTagsToFile')

            # 刷新待传数据个数
            self.sendEvent('UI', 'ui_uploadTagNumInWait', len(self.data2Web))

            # 联网时工作
            if self.serverConnection == 'connected':
                # 数据上传到服务器
                if localCounter % self.uploadDataIntervalSecond == 1:
                    self.sendEvent('IO', 'web_uploadDataToServer')

                # 文件上传到服务器，第一次上传全部，往后只上传新增
                if localCounter % self.uploadDataFileIntervalSecond == 20 and self.dataFileNeedUploadFlag:
                    self.sendEvent('IO', 'web_uploadFileToServer', [False])
                    self.dataFileNeedUploadFlag = False

            time.sleep(1)

    '''
    以下是事件处理引擎，用来处理事件结果
    '''

    # 事件处理引擎
    def eventEngine(self):
        while True:
            time.sleep(0.001)
            if not self.eventQ["IO"].empty():  # 事件队列非空
                try:
                    self.handleEventResult(self.eventQ["IO"].get(block=True, timeout=1))
                except Exception as e:
                    print(__file__, 'eventEngine error', e, traceback.extract_stack())
            else:
                pass

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

    # 处理事件
    def handleEventResult(self, event):
        try:
            # 这里一共有以下一些事件
            task = event[0]
            if len(event) > 1:
                data = event[1]
            else:
                data = []

            if task == 'io_addTags':
                self.addTags(data)
                return
            if task == 'file_writeTagsToFile':
                self.writeTagsToFile()
                return
            if task == 'web_uploadDataToServer':
                self.uploadDataToServer()
                return
            if task == 'io_uploadToServerSuccess':
                self.uploadDataToServerSuccess()
                return
            if task == 'io_internetConnectionReport':
                self.updateInternetConnection(data)
                return
            if task == 'web_uploadFileToServer':
                self.uploadFileToServer(data[0])
                return
            if task == 'io_checkServerConnection':
                self.testWebConnection(event)
                return
            if task == 'web_downloadEventConfigFileFromServer':
                self.downloadConfigFile(event)
                return
            if task == 'io_deleteDataFile':
                self.deleteDataFile()
                return
            if task == 'io_oldFileUploadSuccessfully':
                self.oldFileUploadSuccessfully(data)
        except Exception as e:
            print(e)
            traceback.print_exc()

    '''
    =======================================================================================================================
    事件处理函数
    =======================================================================================================================
    '''

    def addTags(self, newTags):
        self.data2File.extend(newTags)
        self.data2Web.extend(newTags)
        self.dataFileNeedUploadFlag = True

    def writeTagsToFile(self):
        if len(self.data2File) == 0:
            return
        data2FileCopy = self.data2File.copy()
        localTagList = []
        fileUrl = self.recordFile.getRecordFileUrl()
        # 复制出需要写入文件的数据
        for i in data2FileCopy:
            if self.recordFile.lineNumNow + 1 <= self.recordFile.maxLineNum:
                self.recordFile.lineNumNow += 1
                localTagList.append(i)
                self.data2File.pop(0)
            else:
                # 创建新文件
                self.recordFile.updateRecordFileUrl(True)
                break
        t = Process(target=gtyIoTools.recordEpcDefaultFormat,args=(fileUrl, localTagList))
        t.start()

    def uploadDataToServer(self):
        if len(self.data2WebTemp) == 0:
            self.data2WebTemp = self.data2Web[0:min(len(self.data2Web), self.maxTagNumPerWebRequest)]
        t = Process(target=self.uploadDataToServerGet, args=(self.data2WebTemp,))
        t.start()

    def uploadFileToServer(self,allFiles=False):
        t = Process(target=gtyIoTools.uploadResultFileToServer, args=(self.eventQ, self.recordFile,allFiles))
        t.start()

    def testWebConnection(self, event):
        data = event[1]
        # 再上传数据
        t = Process(target=gtyIoTools.testWebConnection,
                    args=(self.eventQ,
                          data[0]["machineId"],
                          data[0]["batteryPercent"],
                          data[0]["totalEpcRead"],
                          data[0]["differentEpcRead"],
                          data[0]["reader1Working"],
                          data[0]["reader2Working"],
                          data[0]["hardwareTime"],
                          data[0]["eventId"]))
        t.start()
        return

    # 下载配置文件
    def downloadConfigFile(self, event):
        t = Process(target=gtyIoTools.downloadFileFromServer,args=(self.eventQ['UI'], event[1][1],self.machineId))  # 这里最后一个参数是设备代码
        t.start()
        return

    # 删除数据文件
    def deleteDataFile(self):
        self.recordFile.deleteDataFile()

    # 记录已经上传的数据文件
    def oldFileUploadSuccessfully(self,fileUrl):
        self.recordFile.fileUrlUploadedDone(fileUrl)
    '''
    =======================================================================================================================
    此类中的具体的工作函数
    =======================================================================================================================
    '''

    # cp数据上传到服务器，Get请求方式
    def uploadDataToServerGet(self, tagList):
        if len(tagList) == 0:
            return
        url = ''
        try:
            md5String = os.environ.get("platform4_md5String")
            if md5String is None:
                md5String = ""
            token = str(random.randint(10000000, 99999999))
            url = self.serverLocation + self.cpDataUploadUrl + '?machineId=' + self.machineId + '&eventId=' + str(
                self.eventId) + '&epcNum=' + str(len(tagList))
            for i in tagList:
                url += "&" + i.epcString + "=" + i.hardwareDateString + " " + i.hardwareTimeString
            url += '&t=' + str(token) + '&sign=' + gtyIoTools.get_token(token, md5String)
            url = url.replace(' ', '~')
            res = urllib.request.urlopen(url)
            getData = res.read().decode('utf-8')
            gtyLog.log.write(__file__, url, getData)
            if 'ok' in getData:
                self.sendEvent('IO', 'io_uploadToServerSuccess', [])
        except Exception as e:
            gtyLog.log.write(__file__, url, e)

    def uploadDataToServerSuccess(self):
        self.data2Web = self.data2File[len(self.data2WebTemp):]
        self.data2WebTemp = []

    # 更新结果
    def updateInternetConnection(self, data):
        self.serverConnection = data


def main(eventQ):
    while True:
        print("===================IO task started===================")
        try:
            io = GtyIO(eventQ)
            io.start()
        except Exception as e:
            traceback.print_exc()
            gtyLog.log.write(__file__, e, '=================IO service restart!=================')
        time.sleep(1)


if __name__ == '__main__':
    pass
