# -*- coding:utf-8 -*-

import platform4
import gtyTools.tools
# 启动平台
if __name__ == '__main__':
    num = gtyTools.tools.checkAlreadyRun()
    if num > 1:
        print("feibot desktop already running!",num)
        exit()
    p = platform4.platForm()
    p.start()


