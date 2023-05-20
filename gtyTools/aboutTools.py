# Description : This script will monitor the battery voltage and battery level
# Author : Nader Hany

# according to the given data
# Vmin = 4*2.75 v
# Vmax = 4*4.2  v
# according to the voltage divider has r1=68k ,r2=10k Vads=Vbattery*(r2/r1+r2)
# so we calculate Vbattery = 7.8125 * Vads
# Battery level = ((Vbattery - 11) * 17.242)


import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import datetime
import psutil
import subprocess
import Adafruit_DHT as dht
import configparser

# print("Current date and time:", formatted_datetime)


class battery:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.adc0 = AnalogIn(self.ads, ADS.P0)
        self.adc1 = AnalogIn(self.ads, ADS.P1)
        self.adc2 = AnalogIn(self.ads, ADS.P2)
        self.adc3 = AnalogIn(self.ads, ADS.P3)

    # main battery voltage
    def getMainB_v(self):
        # VIN_M
        VOUT = 7.8125*self.adc2.voltage
        # BLEVEL=(VOUT-11)*17.242
        return "{:.2f}v".format(VOUT)

    # main battery level
    def getLMainB_l(self):
        # VIN_M
        VOUT = 7.8125*self.adc2.voltage
        BLEVEL = (VOUT-11)*17.242
        return '{0:0.1f}% '.format(BLEVEL)

    # backup battery voltage
    def getBackupB_v(self):
        VBKB = self.adc1.voltage*5.3
        return "{:.2f}v".format(VBKB)

    # charging voltage

    def getCharging_v(self):
        # VIN_USB
        VUSB = self.adc0.voltage*5.3
        return "{:.2f}v".format(VUSB)

    # pcb  voltage

    def getvPcb_v(self):
        # VIN_PCB
        VPCB = self.adc3.voltage*1.65
        return "{:.2f}v".format(VPCB)


def getDateTime():


    # Specify the file path
    file_path = '../configfiles/machineConfig.ini'
    
    # Read the file content
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Create a ConfigParser object and read the content
    config = configparser.ConfigParser()
    config.read_string(file_content)
    
    # Get the values of timezone and UTC
    timezone = config.get('timezone', 'timezone')
    utc = config.get('timezone', 'UTC')
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%Y %Z %H:%M:%S")
    return formatted_datetime +" UTC "+utc


def getUpTime():
    uptime = psutil.boot_time()
    current_time = psutil.time.time()
    uptime_duration = current_time - uptime
    uptime = str(datetime.timedelta(seconds=int(uptime_duration)))
    return str(uptime)

    # print("System uptime:", uptime_duration, "seconds")


def getCpuUsage():
    # cpu_usage = psutil.cpu_percent(interval=1)
    # print("CPU Usage:", cpu_usage, "%")
    # Execute a command and capture the output
    output = subprocess.check_output(
        "echo \"cpu=$(top -bn1 | grep \"Cpu(s)\" | awk '{print $2}')% \" ", shell=True)
    return str(output.decode())


def getEth0():
    # Get network interfaces
    ipcmd = "ifconfig  eth0 | awk '/inet / {print $2}'"
    maccmd = "ifconfig eth0 | awk '/ether / {print $2}'"
    output1 = subprocess.check_output(ipcmd,  shell=True)
    output2 = subprocess.check_output(maccmd, shell=True)
    return "IP "+str(output1.decode()).replace("\n", "")+" MAC "+str(output2.decode())
    # return "IP "+"192.168.162.150".replace("\n","")+" MAC "+"f6:aa:95:47:69:77"


def getEth1():
    # Get network interfaces
    ipcmd = "ifconfig  eth1 | awk '/inet / {print $2}'"
    maccmd = "ifconfig eth1 | awk '/ether / {print $2}'"
    output1 = subprocess.check_output(ipcmd,  shell=True)
    output2 = subprocess.check_output(maccmd, shell=True)
    return "IP "+str(output1.decode()).replace("\n", "")+" MAC "+str(output2.decode())
    # return "IP:"+"192.168.162.70".replace("\n","")+" MAC:"+"f6:ea:95:75:69:46"


def getWlan0():
    # Get network interfaces
    ipcmd = "ifconfig  wlan0 | awk '/inet / {print $2}'"
    maccmd = "ifconfig wlan0 | awk '/ether / {print $2}'"
    output1 = subprocess.check_output(ipcmd,  shell=True)
    output2 = subprocess.check_output(maccmd, shell=True)
    return "IP "+str(output1.decode()).replace("\n", "")+" MAC "+str(output2.decode())
    # return "IP:"+"192.168.162.76".replace("\n","")+" MAC:"+"f6:ff:ff:75:69:46"


def getCpuTemp():
    temperatures = psutil.sensors_temperatures()
    if 'coretemp' in temperatures:
        cpu_temp = temperatures['coretemp'][0].current
        return str(cpu_temp)+"°C"
    else:
        return "Temp information not available."


def getCpuTemp():
    cmd = "vcgencmd  measure_temp | grep -o -E '[[:digit:]].*'"
    output = subprocess.check_output(cmd,  shell=True)
    return str(output.decode()).replace("\n", "")


def getGpuTemp():
    cmd = "vcgencmd  measure_temp | grep -o -E '[[:digit:]].*'"
    output = subprocess.check_output(cmd,  shell=True)
    return str(output.decode()).replace("\n", "")


def getDHT22():
    pinval = 4
    h, t = dht.read_retry(dht.DHT22, pinval)
    # t=26.565668
    # h=94
    return '{0:0.1f}°C         {1:0.1f}%'.format(t, h)


def getMBattery():
    # Get network interfaces
    batteryScriptPath = "/home/Desktop/file.py"
    cmd = "python3 "+batteryScriptPath
    output1 = subprocess.check_output(cmd,  shell=True)
    return "IP "+str(output1.decode()).replace("\n", "")


if __name__ == '__main__':
    # getMachineId()
    pass
