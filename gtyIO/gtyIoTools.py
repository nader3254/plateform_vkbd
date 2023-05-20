# -*- coding:utf-8 -*-

import hashlib
import os
import random
import signal
import sys
import time
import traceback
import urllib
import urllib.error
import urllib.parse
import urllib.request
from urllib.error import URLError
import ssl

import urllib
from poster3.encode import multipart_encode
from poster3.streaminghttp import register_openers
from gtyConfig import configFileHandler, systemConfig
from gtyTools import gtyLog
from . import OssHandler
import recordFileHandle
import json
ssl._create_default_https_context = ssl._create_unverified_context




machineConfig = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)

serverLocation = machineConfig.read("server", "serverLocation")
print(__file__, "serverlocation", serverLocation)
if serverLocation[-1] != '/':
    serverLocation += "/"

cpDataUploadUrl = machineConfig.read("server", "cpDataUploadUrl")
dataFileDir = machineConfig.read("IO", "dataFileDir")
if dataFileDir[-1] != '/':
    dataFileDir += '/'


# 获取赛事配置文件的下载地址
def obtainUrlOfEventConfigFile(eventId):
    eventUrl = machineConfig.read("server", "eventConfigFileUrl")
    t = urllib.request.urlopen(serverLocation + eventUrl + '?RACEID=' + eventId + '&' + 'TOKEN=' + '000000')
    res = json.loads(t.read().decode('utf-8'))
    return res #res["message"]


# 从指定的地址下载文件到指定目录
def downloadFileFromWeb(fromUrl, toFile="/home/stoperica/plateform/config/filename.txt"):
    try:
        import urllib.request, urllib.error, urllib.parse
        if fromUrl == '':
            fromUrl = serverLocation + machineConfig.read("server", "eventConfigFileUrl")
        f = urllib.request.urlopen(fromUrl)
        data = f.read()
        with open(toFile, "wb") as code:
            code.write(data)
        return 'success'
    except   Exception as e:
        gtyLog.log.write(__file__, e)
        print(e)
        return 'failed'


# TODO ：这里记录的方式就不对，应该改为每n秒记录一次，参数应该改为列表
# 记录EPC信息到文件，默认格式
# 输入应该为
# fileName:文件名
# tagList: 成员为标签对象，
def recordEpcDefaultFormat(fileUrl, tagList):
    if tagList is None or len(tagList) == 0:
        return False
    # 首先打开文件
    try:
        f = open(fileUrl, 'a')
    except Exception as e:
        os.system("touch " + fileUrl)
        gtyLog.log.write(__file__, e)
        return False
    # 对于每一条EPC值记录一行
    for tag in tagList:
        line = tag.epcString + ":" + tag.hardwareDateString + "_" + tag.hardwareTimeString \
               + ",port=" + str(tag.channelId) \
               + ",rssi=" + str(tag.rssi)
        try:
            f.write(line)
            f.write('\n')
        except Exception as e:
            gtyLog.log.write(__file__, 'record epc into file error', e)
    f.flush()
    f.close()


# 从服务器下载配置文件
def downloadFileFromServer(resultQ, eventId, machineId):
    # 1. 获取配置文件的下载地址
    try:
        res = obtainUrlOfEventConfigFile(eventId)
        status = res["status"]
        eventName = res["message"].split('-')[-1].replace('\'','')
        print('status eventName>>>',status,eventName)
        machineConfig.write('event', 'eventName', eventName)
        if status == 200:
            result = 'success'
            res = ['ui_updateCurrentEventConfigFileName', eventId, eventName]
            resultQ.put(res)
            res = ['ui_updateMainDialogEventInfo', eventId, eventName]
            resultQ.put(res)
        else:
            result = 'failed'
        res = ['ui_updateDisplayStatus',status]
        resultQ.put(res)
        return result
    except:
        result = 'failed'
        status = 0
        res = ['ui_updateDisplayStatus',status]
        resultQ.put(res)
        return result


# 测试是否能连上互联网
def pingTest():
    t = 'www.stoperica.live'
    cmd = 'ping -c 1 -w 1 %s' % t
    backInfo = os.system(cmd + "> /dev/null 2>&1")
    if backInfo == 0:
        return True
    return False


# 检测是否能连上服务器


def testWebConnection(eventQ, machineId, batteryPercent, epcTotal, epcDiffent,
                      reader1Working,
                      reader2Working, machineTimeStamp, eventId='unKnown'):
    # 0. 输出自己的pid
    gtyLog.log.write(__file__, 'testWebConnection', os.getpid())
    try:
        try:
            md5String = os.environ.get("platform4_md5String")
            if md5String is None:
                md5String = ""
        except Exception as e:
            md5String = ""
            gtyLog.log.write(__file__, e)
        tocken = str(random.randint(10000000, 99999999))
        url = serverLocation + machineConfig.read("server", "internetConnectionTest") + \
              '?machineId=' + machineId + \
              '&batPercent=' + str(batteryPercent) + \
              '&epcTotal=' + str(epcTotal) + \
              '&epcDiff=' + str(epcDiffent) + \
              '&eventId=' + str(eventId) + \
              '&t=' + str(tocken) + \
              '&sign=' + str(get_token(tocken, md5String)) + \
              '&reader1Working=' + str(reader1Working) + \
              '&reader2Working=' + str(reader2Working) + \
              '&machineTimeStamp=' + str(machineTimeStamp)
        gtyLog.log.write(__file__, url)
        # print(__file__,url)
        t = urllib.request.urlopen(url, timeout=5)
        getData = t.read().decode(encoding='utf-8')
        # print(__file__,getData)
        gtyLog.log.write(__file__, getData)
        if str(getData).upper().startswith('OK'):
            connection = 'connected'
            res = []
            if 'reader1=0' in getData:
                res = ['ui_startOrStropReading', 1, ['1', 'off']]  # 这里的参数是一个数组，['1',cmd]，这里cmd=on，开启，cmd=off，关闭，x不指定
            if 'reader1=1' in getData:
                res = ['ui_startOrStropReading', 1, ['1', 'on']]  # 这里的参数是一个数组，['1',cmd]，这里cmd=on，开启，cmd=off，关闭，x不指定
            if 'reader2=0' in getData:
                res = ['ui_startOrStropReading', 1, ['2', 'off']]  # 这里的参数是一个数组，['1',cmd]，这里cmd=on，开启，cmd=off，关闭，x不指定
            if 'reader2=1' in getData:
                res = ['ui_startOrStropReading', 1, ['2', 'on']]  # 这里的参数是一个数组，['1',cmd]，这里cmd=on，开启，cmd=off，关闭，x不指定
            if len(res) > 0:
                eventQ["UI"].put(res)
        else:
            if pingTest():
                connection = 'wwwConnected'
            else:
                connection = 'disconnected'
    except Exception as e:
        print(__file__, e, "back")
        traceback.extract_stack()
        gtyLog.log.write(__file__, e)
        if pingTest():
            connection = 'wwwConnected'
        else:
            connection = 'disconnected'
    res = ['ui_internetConnectionReport', connection]
    eventQ["UI"].put(res)
    res = ['io_internetConnectionReport', connection]
    eventQ["IO"].put(res)


# 上传结果文件到服务器并向UI线程返回结果信息
# 如果all为true，则上传全部文件
def uploadResultFileToServer(eventQ, recordFileObj,allFiles=False):
    recordFile = recordFileObj
    try:
        gtyLog.log.write(__file__, 'uploadResultFileToServer', os.getpid())

        # 首先判断服务器端是否允许上传
        eventId = recordFileObj.eventId
        t = urllib.request.urlopen(
            serverLocation + machineConfig.read("server", "dataUploadAllowedUrl") + '?eventId=' + eventId, timeout=5)
        getData = t.read().decode('utf-8')
        print(__file__, "getData", getData)
        if 'no' in getData:
            res = ['ui_uploadResultFileToServer', ['failed', 'upload is not allowed by server']]
            eventQ["UI"].put(res)
            return

        # 如果允许，则上传
        # 获取待上传的文件列表
        fileUrlListOld = recordFile.getFileUrlListRecordDone(allFiles)
        fileUrlNow = recordFile.recordFileUrl
        fileUrlTotal = fileUrlListOld + [fileUrlNow]
        totalUrlNum = len(fileUrlTotal)
        successNum = 0
        for fileUrl in fileUrlTotal:
            if uploadFileToServer(fileUrl,recordFileObj.ossObjectPrefix):
                successNum += 1
                if fileUrl != fileUrlNow:
                    print(__file__,fileUrl)
                    eventQ["IO"].put(['io_oldFileUploadSuccessfully',fileUrl])

        if successNum >0:
            res = ['ui_uploadResultFileToServer', ['successful', str(successNum) + "/" + str(totalUrlNum)]]
        else:
            res = ['ui_uploadResultFileToServer', ['failed', "all file upload failed"]]
        eventQ["UI"].put(res)
    except Exception as e:
        gtyLog.log.write(__file__, '上传原始文件进程超时，被杀死1', os.getpid(), e)
    exit()


# 上传一个指定文件到oss
def uploadFileToServer(filePath,objectPrefix=""):
    try:
        # 1.上传之前先压缩
        try:
            os.popen('rm ' + filePath + '.zip')
        except:
            pass
        cmd = 'zip -qj ' + filePath + '.zip ' + filePath
        os.system(cmd)
        filePath += '.zip'
        # 2.通过oss上传文件
        try:
            oss = OssHandler.OssHandler()
            targetFileName = objectPrefix + os.path.basename(filePath)
            if oss.uploadFileToOss(filePath, targetFileName):
                print('oss upload successfully:', targetFileName)
                return True
            else:
                print('oss upload failed:', time.strftime('%H:%M:%S', time.localtime(time.time())))
        except Exception as e:
            gtyLog.log.write(__file__, e)
    except Exception as e:
        gtyLog.log.write(__file__, e, '上传原始文件进程超时，被杀死2')
    # 删除所有zip文件
    try:
        os.popen("rm " + os.path.join(os.path.dirname(filePath), "*.zip"))
    except:
        pass
    return False


# 生成md5字串
def get_token(stra, secret=''):
    md5str = str(stra) + secret
    m1 = hashlib.md5()
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    return token


# 超时异常
def timeOutHandler(signum, frame):
    print('time out, pid:', os.getpid())
    raise Exception("timeout...")


if __name__ == '__main__':
    pass
