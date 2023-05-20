# -*- coding: utf-8 -*-


from gtyConfig import systemConfig, configFileHandler
import os
import oss2

class OssHandler:
    # 0.构造OSS对象,可以手动指定prefix
    def __init__(self):
        self.machine = configFileHandler.ConfigFileHandler(systemConfig.machineConfigFilePath)
        self.ossEnabled = self.machine.read("oss", "enable", "int", 1)
        if self.ossEnabled == 0:
            return

        self.ossConnectedOk = False
        try:
            self.keyId = self.machine.read("oss", "ossAccessKeyId", "string", os.environ.get("platform4_ossKeyId"))
            self.keySecret = self.machine.read("oss", "ossAccessKeySecret", "string",os.environ.get("platform4_ossKeySecret"))
            self.auth = oss2.Auth(self.keyId, self.keySecret)
            self.endPoint = self.machine.read("oss", "endPoint", "string", os.environ.get("platform4_ossEndPoint"))
            self.bucketName = self.machine.read("oss", "bucketName", "string",os.environ.get("platform4_ossBucketName"))
            self.bucket = oss2.Bucket(self.auth, self.endPoint, self.bucketName)
            self.ossConnectedOk = True
        except Exception as e:
            print(e)
            print("oss init failed...")
            self.ossConnectedOk = False

    # 上传一个文件到oss
    def uploadFileToOss(self, fromObj, toObj):
        if self.ossEnabled == 1 and self.ossConnectedOk:
            with open(fromObj, 'rb') as fileObj:
                self.bucket.put_object(toObj, fileObj)
            return True
        else:
            return False


if __name__ == "__main__":
    oss = OssHandler()
    oss.uploadFileToOss("newData", "/home/feibot/data/U001_513/U001_513_00001.csv.zip")
