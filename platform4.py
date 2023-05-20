# -*- coding:utf-8 -*-
import time
from multiprocessing import Process, Queue
import os
import sys



# 模块的导入，参考: https://blog.csdn.net/gvfdbdf/article/details/52084144
for d in ['gtyConfig', 'gtyIO', 'gtySerial', 'gtySocket', 'gtyTools', 'gtyUI']:
    module_path = os.path.join(os.path.dirname(__file__), d)
    sys.path.append(module_path)  # 导入的绝对路径
from gtyTools import gtyLog,gtyTypes

processes = []


class platForm:

    def __init__(self):
        # 事件队列,元素是['eventType',eventId,data]
        queueSize = 10000
        # 配置的控制接口
        self.configHandlers = gtyTypes.ConfigHandlers()
        self.eventQ = {
            'UI': Queue(queueSize),
            'UART': Queue(queueSize),
            'IO': Queue(queueSize),
            'SOCKET': Queue(queueSize),
            'SOCKET_SERVER':Queue(queueSize)
        }
        # 按定义顺序执行
        self.tasks = {
            'UI': self.uiTask,
            'UART': self.uartTask,
            'IO': self.ioTask,
            'SOCKET': self.socketTask,
            'SOCKET_SERVER':self.socketServerTask
        }
    '''
        以下为各进程的函数
    '''

    def uartTask(self):
        import gtySerial.GtySerial
        gtySerial.GtySerial.main(self.eventQ)

    def uiTask(self):
        import MainGuiModel
        MainGuiModel.main(self.eventQ)

    def ioTask(self):
        import gtyIO.GtyIO
        gtyIO.GtyIO.main(self.eventQ)

    def socketTask(self):
        import gtySocket.FeibotSocket
        gtySocket.FeibotSocket.main(self.eventQ)

    def socketServerTask(self):
        import gtySocket.SocketToServer
        gtySocket.SocketToServer.main(self.eventQ)

    # 启动各个进程任务
    def start(self):
        gtyLog.log.write(__file__, 'platform start!')
        # 启动各个进程任务，并放到字典中
        for taskName, task in self.tasks.items():
            if taskName in ["UI","IO"]:
                t = Process(target=task, name=taskName)
                t.start()
                processes.append(t)
                time.sleep(0.2)


