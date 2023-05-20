# -*- coding:utf-8 -*-

import psutil

# 启动平台
if __name__ == '__main__':
    count = 0
    # 防止重复启动
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        cmdList = p.cmdline()
        if len(cmdList) > 1 and "platformStart.py" in cmdList[1]:
            count += 1
            print(cmdList,count)
