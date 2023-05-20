import datetime
import psutil
import subprocess
import Adafruit_DHT as dht


#print("Current date and time:", formatted_datetime)

def getDateTime():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%Y %Z %H:%M:%S UTC +02:00")  
    return formatted_datetime 


def getUpTime():
    uptime = psutil.boot_time()
    current_time = psutil.time.time()
    uptime_duration = current_time - uptime
    uptime = str(datetime.timedelta(seconds=int(uptime_duration)))
    return str(uptime)

    #print("System uptime:", uptime_duration, "seconds")


def getCpuUsage():
    #cpu_usage = psutil.cpu_percent(interval=1)
    #print("CPU Usage:", cpu_usage, "%")
    # Execute a command and capture the output
    output = subprocess.check_output("echo \"cpu=$(top -bn1 | grep \"Cpu(s)\" | awk '{print $2}')% \" ", shell=True)
    return str(output.decode())


def getEth0():
    # Get network interfaces
    ipcmd="ifconfig  eth0 | awk '/inet / {print $2}'"
    maccmd="ifconfig eth0 | awk '/ether / {print $2}'"
    output1 = subprocess.check_output(ipcmd,  shell=True)
    output2 = subprocess.check_output(maccmd, shell=True)
    return "IP "+str(output1.decode()).replace("\n","")+" MAC "+str(output2.decode())
    #return "IP "+"192.168.162.150".replace("\n","")+" MAC "+"f6:aa:95:47:69:77"

def getEth1():
    # Get network interfaces
    ipcmd="ifconfig  eth1 | awk '/inet / {print $2}'"
    maccmd="ifconfig eth1 | awk '/ether / {print $2}'"
    output1 = subprocess.check_output(ipcmd,  shell=True)
    output2 = subprocess.check_output(maccmd, shell=True)
    return "IP "+str(output1.decode()).replace("\n","")+" MAC "+str(output2.decode())
    #return "IP:"+"192.168.162.70".replace("\n","")+" MAC:"+"f6:ea:95:75:69:46"


def getWlan0():
    # Get network interfaces
    ipcmd="ifconfig  wlan0 | awk '/inet / {print $2}'"
    maccmd="ifconfig wlan0 | awk '/ether / {print $2}'"
    output1 = subprocess.check_output(ipcmd,  shell=True)
    output2 = subprocess.check_output(maccmd, shell=True)
    return "IP "+str(output1.decode()).replace("\n","")+" MAC "+str(output2.decode())
    #return "IP:"+"192.168.162.76".replace("\n","")+" MAC:"+"f6:ff:ff:75:69:46"

def getCpuTemp():
    temperatures = psutil.sensors_temperatures()
    if 'coretemp' in temperatures:
        cpu_temp = temperatures['coretemp'][0].current
        return str(cpu_temp)+"°C"
    else:
        return "Temp information not available."


def getCpuTemp():
    cmd="vcgencmd  measure_temp | grep -o -E '[[:digit:]].*'"
    output = subprocess.check_output(cmd,  shell=True)
    return str(output.decode()).replace("\n","")

def getGpuTemp():
    cmd="vcgencmd  measure_temp | grep -o -E '[[:digit:]].*'"
    output = subprocess.check_output(cmd,  shell=True)
    return str(output.decode()).replace("\n","")

def getDHT22():
    pinval=4
    h,t=dht.read_retry(dht.DHT22,pinval)
    #t=26.565668
    #h=94    
    return '{0:0.1f}°C         {1:0.1f}%'.format(t,h)
 
def getMBattery():
    # Get network interfaces
    batteryScriptPath="/home/Desktop/file.py"
    cmd="python3 "+batteryScriptPath
    output1 = subprocess.check_output(cmd,  shell=True)
    return "IP "+str(output1.decode()).replace("\n","")
    
    
if __name__ == '__main__':
    # getMachineId()
    pass