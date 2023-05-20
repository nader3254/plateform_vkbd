# -*- coding:utf-8 -*-
import os.path

import sys

if __name__ == "__main__":
    # 模块的导入，参考: https://blog.csdn.net/gvfdbdf/article/details/52084144
    for d in ['gtyConfig', 'gtyIO', 'gtySerial', 'gtySocket', 'gtyTools', 'gtyUI']:
        module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), d)
        sys.path.append(module_path)  # 导入的绝对路径

from gtyTools import gtyTypes, tools


# 记录文件处理类
class RecordFileHandle:

    def __init__(self):
        # 配置的控制接口
        self.configHandlers = gtyTypes.ConfigHandlers()

        try:
            self.machineId = self.configHandlers.machine.read("machine", "machineId")
        except Exception as e:
            self.machineId = "777"

        self.eventId = ''

        # 最大的行数
        self.maxLineNum = self.configHandlers.machine.read("IO", "recordFileMaxLineNum", "int", 5000)
        if self.maxLineNum < 1000:
            self.maxLineNum = 1000

        # oss前缀
        self.ossObjectPrefix = self.configHandlers.machine.read("oss","ossObjectPrefix","string","")

        # 关于存储文件，每一个赛事用一个文件夹，文件名以 设备id_赛事id_record_编号.csv表示
        # 总路径
        self.recordFileRoot = self.configHandlers.machine.read("IO", "dataFileDir")
        # 赛事文件夹
        self.recordFileDirPath = ""
        # 文件序号
        self.fileId = 1
        # 当前文件名
        self.recordFileNameNow = ""
        self.lineNumNow = 0
        # 完整路径
        self.recordFileUrl = ""
        # 生成路径
        self.updateRecordFileUrl()
        # 已经上传过的文件路径列表
        self.fileUrlUploadedList = []

    # 更新一次存储文件位置
    def updateRecordFileUrl(self, newFile=False):
        # 1. 从配置文件中读取赛事名称
        self.eventId = self.configHandlers.machine.read("event", "eventId")
        # 2. 得到此赛事的记录文件夹
        self.recordFileDirPath = os.path.join(self.recordFileRoot, self.machineId + "_" + self.eventId)
        try:
            os.system("mkdir " + self.recordFileDirPath)
        except Exception as e:
            print(e)
        # 3. 列出所有文件名
        files = os.listdir(self.recordFileDirPath)
        resultFiles = []
        for i in files:
            if ".zip" not in str(i) and ".csv" in str(i) and "_" in str(i):
                resultFiles.append(str(i))
                # 多于一个文件的情况
        if len(resultFiles) > 0:
            maxFile = str(max(resultFiles))
            maxFileUrl = os.path.join(self.recordFileDirPath, maxFile)
            try:
                if not newFile:
                    lineNum = getFileLineNum(maxFileUrl)
                    if lineNum < self.maxLineNum:
                        # 沿用原来的文件
                        self.lineNumNow = lineNum
                        self.recordFileNameNow = str(maxFile)
                        self.recordFileUrl = os.path.join(self.recordFileDirPath, self.recordFileNameNow)
                        print(__file__, "use the old file","  lineNum:",lineNum,"  maxLineNum:",self.maxLineNum)
                        print(__file__,"old file:",self.recordFileUrl)
                        return
            except Exception as e:
                print(__file__, e)
            # 创建下一个文件
            self.lineNumNow = 0
            self.recordFileNameNow = fileAddOne(self.machineId, self.eventId, maxFile)
            self.recordFileUrl = os.path.join(self.recordFileDirPath, self.recordFileNameNow)
            os.system("touch " + self.recordFileUrl)
            print(__file__, "create next file")
        else:
            # 创建第一个文件
            self.lineNumNow = 0
            self.recordFileNameNow = self.machineId + "_" + self.eventId + "_" + "00001.csv"
            print(__file__, "create the first file")
            self.recordFileUrl = os.path.join(self.recordFileDirPath, self.recordFileNameNow)
            os.system("touch " + self.recordFileUrl)

    # 获得当前的文件路径
    def getRecordFileUrl(self):
        return self.recordFileUrl

    # 获得已经完成存储的文件列表
    def getFileUrlListRecordDone(self, allFiles=False):
        files = os.listdir(self.recordFileDirPath)
        files.sort()
        res = []
        for f in files:
            if "zip" not in f:
                url = os.path.join(self.recordFileDirPath, f)
                if allFiles:
                    if url != self.recordFileUrl:
                        res.append(url)
                else:
                    if url not in self.fileUrlUploadedList and url != self.recordFileUrl:
                        res.append(url)
        return res

    # 记录已经完整上传的文件路径
    def fileUrlUploadedDone(self, url):
        if url != self.recordFileUrl:
            self.fileUrlUploadedList = self.fileUrlUploadedList + [url]

    # 删除结果文件
    def deleteDataFile(self):
        try:
            print(__file__, "delete eventData")
            os.system("rm -R " + self.recordFileDirPath)
            self.updateRecordFileUrl()
            return True
        except Exception as e:
            print(__file__, e, "delete data file failed", self.recordFileDirPath)
            self.updateRecordFileUrl()
            return False


# 在现有文件名的基础上增加一个
def fileAddOne(machineId, eventId, fileName):
    parts = str.split(fileName, '.')
    parts2 = str.split(parts[-2], '_')
    oldId = int(parts2[-1])
    newFileName = machineId + "_" + eventId + "_" + "%05d" % (oldId + 1) + ".csv"
    return newFileName


# 获得文件的行数
def getFileLineNum(url):
    count = 0
    theFile = open(url, 'r')
    while True:
        buffer = theFile.read(8192 * 1024)
        if not buffer:
            break
        count += buffer.count('\n')
    theFile.close()
    return count


if __name__ == "__main__":
    from gtyTools import gtyLog

    processes = []

    fileAddOne('U001_990_00002.csv')
