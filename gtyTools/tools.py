# -*- coding: utf-8 -*-

import time
import os

import psutil

from gtyConfig import systemConfig


def getTimeStamp(year, month, day, hour, minute, second, centiSecond):
    # dt为字符串
    if int(year) < 2000:
        year = int(year) + 2000
    dt = '%d-%d-%d %d:%d:%d' % (year, month, day, hour, minute, second)
    # 中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    # 将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s) + centiSecond



# 电池曲线
def batteryPercentage(v):
    # print 'battery v:',v,'v'
    if v > 12.3:
        # gtyLog.log.write(__file__, 'battery:', v)
        return 100
    elif v > 11.1:
        # gtyLog.log.write(__file__, 'battery:', v)
        return (v - 11.1) * 20.8 + 75
    elif v > 10.6:
        # gtyLog.log.write(__file__, 'battery:', v)
        return (v - 10.6) * 50 + 50
    elif v > 10.1:
        # gtyLog.log.write(__file__, 'battery:', v)
        return (v - 10.1) * 50 + 25
    elif v > 8.7:
        # gtyLog.log.write(__file__, 'battery:', v)
        return (v - 8.7) * 17.86
    else:
        # gtyLog.log.write(__file__, 'battery:', v)
        return 0


# 获取ip地址
def getIpAddr():
    try:
        cmd = 'ifconfig | grep \"inet \" | awk \'{ print $2}\''
        p = os.popen(cmd)
        res = p.read()
        a = res.split('\n')
        infos = []
        for i in a:
            if len(i) >= 2:
                if '127.0.0.1' not in i:
                    infos.append(i)
        return infos
    except:
        return []



def check_ip(ipaddr):
    addr = str(ipaddr).strip().split('.')  # 切割IP地址为一个列表

    if len(addr) != 4:  # 切割后列表必须有4个参数
        return False

    for i in range(4):
        try:
            addr[i] = int(addr[i])  # 每个参数必须为数字，否则校验失败
        except:
            return False

        if addr[i] <= 255 and addr[i] >= 0:  # 每个参数值必须在0-255之间
            pass
        else:
            return False

    return True


# 检查当前已经运行的进程个数，避免重复启动
def checkAlreadyRun():
    # 防止重复启动
    pids = psutil.pids()
    count = 0
    for pid in pids:
        p = psutil.Process(pid)
        cmdList = p.cmdline()
        if len(cmdList) > 1 and "platformStart.py" in cmdList[1]:
            count += 1
    return count


# 读取本地的ip，mask，gateway
def GetNetworkInfo():
    try:
        import netifaces
        Networkdict = {}

        routingGateway = netifaces.gateways()[2][0][0]  # 网关
        # print __file__,'interface:',netifaces.interfaces()

        interface = getInterfaces()
        # try:
        routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']  # 获取IP
        routingMusk = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
        # except KeyError:
        # pass
        Networkdict['Interface'] = interface
        Networkdict['IP'] = routingIPAddr
        Networkdict['MASK'] = routingMusk
        Networkdict['GATEWAYS'] = routingGateway
        return Networkdict
    except:
        try:
            interface = 'wlan0'
            # try:
            routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']  # 获取IP
            routingMusk = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            # except KeyError:
            # pass
            Networkdict['Interface'] = interface
            Networkdict['IP'] = routingIPAddr
            Networkdict['MASK'] = routingMusk
            Networkdict['GATEWAYS'] = routingGateway
            return Networkdict
        except:
            return 'failed'


# 从列表中获取需要的网卡号，如果有有线链接，那么返回有线链接。如果没有有线链接，返回无线链接。
def getInterfaces():
    try:
        import netifaces
        interfaceList = netifaces.interfaces()
        for i in interfaceList:
            if i != 'wlan0' and len(i) > 8:
                return i
        return 'wlan0'
    except:
        return 'wlan0'


def linuxSudoCmd(cmd):
    password = systemConfig.passwd
    command = cmd
    try:
        os.system('echo %s | sudo -S %s' % (password, command))
    except Exception as e:
        print(e)
        

def autoFan():
    temp = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    # print('temp',temp)
    if int(temp)/1000 < 45:
        os.system('echo %s | sudo -S %s' % ('100perica!!', 'gpio -g pwm 18 0'))
    if 47 < int(temp)/1000 < 50:
        os.system('echo %s | sudo -S %s' % ('100perica!!', 'gpio -g pwm 18 700'))
    elif 50 <= int(temp)/1000 < 60:
        os.system('echo %s | sudo -S %s' % ('100perica!!', 'gpio -g pwm 18 850'))
    elif int(temp)/1000 >= 60:
        os.system('echo %s | sudo -S %s' % ('100perica!!', 'gpio -g pwm 18 1000'))


if __name__ == '__main__':
    # getMachineId()
    pass
