# -*- coding:utf-8 -*-
import traceback

from PyQt5.QtCore import *

import time
import os
from gtyTools import gtyLog


class uiEventEngine(QThread):
    signal_every1second = pyqtSignal(int)  # 产生一次整数秒时刻，以系统时间为准
    signal_getEpc = pyqtSignal(list)  # 获得了EPC的事件
    signal_1 = pyqtSignal(str)  # 主页面log输出信号
    signal_2 = pyqtSignal(list)  # 电池百分比信号
    signal_3 = pyqtSignal(str)  # 配置状态信号
    signal_6 = pyqtSignal(str)  # 配置文件内容信号
    signal_7 = pyqtSignal(str)  # 获取当前的赛事配置文件名
    signal_8 = pyqtSignal(str)  # 从服务器下载赛事配置文件
    signal_9 = pyqtSignal(list)  # 获得固件版本号
    # signal_10 = pyqtSignal(list)  # 暂停或停止读取
    signal_11 = pyqtSignal(str)  # 更新读取控制按钮的显示，读写器1
    signal_13 = pyqtSignal(str)  # 电源管理（重启、关机）信号
    signal_21 = pyqtSignal(str)  # 当前能否上网的结果信号
    signal_22 = pyqtSignal(list)  # 上传结果文件成功与否信号
    signal_26 = pyqtSignal(list)  # 获得同步时间信号的结果，[累加器数值，接收还是发送]
    signal_27 = pyqtSignal(str)  # 下载软件包是否成功
    signal_28 = pyqtSignal(list)  # stm32固件升级进度
    signal_29 = pyqtSignal(list)  # stm32固件升级完成
    signal_39 = pyqtSignal(list)  # 测试卡读到的次数
    signal_43 = pyqtSignal(dict)  # 更新主页面的值
    signal_45 = pyqtSignal(list)  # 获得了读卡功率的返回值
    signal_47 = pyqtSignal(int)  # 待上传数据的条数

    signal_54 = pyqtSignal(list)  # 0：国标 920~925Mhz

    signal_updateFieldsFromConfigFile = pyqtSignal(list)
    signal_socketConnectResult = pyqtSignal(bool)
    signal_socketGetDate = pyqtSignal(bool)
    signal_socketGetTime = pyqtSignal(bool)
    signal_socketGetGunTime = pyqtSignal(bool)
    
    signal_powerSaveCount = pyqtSignal(int)
    signal_displayStatus = pyqtSignal(int)
    signal_updateTimeDisplay = pyqtSignal(str)

    def __init__(self, eventQ, parent=None):
        super(uiEventEngine, self).__init__(parent)  # 继承了父类的构造函数
        self.eventQ = eventQ
        self._lastTime_1s = 0
        self.timeStampModifiedBy = 0
        self._lastTimeModified = 0
        self.localRunCounter = 0

        # 事件列表
        self.eventList = {
            'everySecond':self.signal_every1second,
            'ui_getEPC':self.signal_getEpc,
            'ui_loadEventConfigFile':self.signal_3,
            'ui_batteryVoltage':self.signal_2,
            'ui_log':self.signal_1,

            'ui_updateFieldsFromConfigFile':self.signal_updateFieldsFromConfigFile,
            'ui_updateCurrentEventConfigFileName':self.signal_6,
            'ui_updateMainDialogEventInfo':self.signal_7,
            'ui_downloadEventConfigFileFromServer':self.signal_8,
            'ui_getFirmwareVersion':self.signal_9,
            # 'ui_startOrStropReading':self.signal_10,
            'ui_updateOperateDialogReadingLabel':self.signal_11,
            'ui_powerControl':self.signal_13,
            'ui_internetConnectionReport': self.signal_21,
            'ui_uploadResultFileToServer': self.signal_22,
            'ui_getSetTimeInfo':self.signal_26,
            'ui_downloadSoftwarePackResult':self.signal_27,
            'ui_stm32UpdateProgress':self.signal_28,
            'ui_stm32UpdateComplete':self.signal_29,
            'ui_testTagReadTimes':self.signal_39,
            'ui_updateMainDialogValue':self.signal_43,
            'ui_getReaderPower':self.signal_45,
            "ui_getFreqBand": self.signal_54,
            'ui_uploadTagNumInWait':self.signal_47,

            'ui_socketConnectedResult':self.signal_socketConnectResult,
            'ui_socketGetDate':self.signal_socketGetDate,
            'ui_socketGetTime':self.signal_socketGetTime,
            'ui_socketGetGunTime':self.signal_socketGetGunTime,
            
            'ui_powerSaveValueSet':self.signal_powerSaveCount,
            'ui_updateDisplayStatus':self.signal_displayStatus,
            'ui_updateTimeDisplay': self.signal_updateTimeDisplay
        }

    def run(self):
        while True:
            # 延时占用
            time.sleep(0.005)
            # 用来发送整数系统时间数据信号
            timeStamp = time.time()
            try:
                # 每1s发出一个信号
                if int(timeStamp * 100) % 100 < 10 and timeStamp - self._lastTime_1s > 0.5:
                    self._lastTime_1s = time.time()
                    self.eventList['everySecond'].emit(int(timeStamp))
            except Exception as e:
                gtyLog.log.write(__file__,e,traceback.extract_stack())
                
            # 事件队列非空
            if not self.eventQ["UI"].empty():
                # 获取队列中的事件 超时1秒
                resultEvent = self.eventQ["UI"].get(block=True, timeout=1)
                # 这里直接根据不同的事件类型发送不同的信号
                task = resultEvent[0]
                data = resultEvent[1]
                gtyLog.log.write(__file__, resultEvent)
                try:
                    self.eventList[task].emit(data)
                    continue
                except Exception as e:
                    gtyLog.log.write(__file__,e,traceback.extract_stack())
