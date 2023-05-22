import evdev
import time
import configparser
import os
import datetime
import threading

Touch_deviceName = "ft5x06"

#Touch_deviceName="vc4-hdmi"
#Touch_deviceName="Mouse"
device_path = ""
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    #print(device.path, device.name, device.phys)
    if Touch_deviceName in device.name:
        print("found mouse at :"+device.path)
        device_path = device.path


start=""
end=""
ctr=0
device = evdev.InputDevice(device_path)
print(device)
# device /dev/input/event1, name "USB Keyboard", phys "usb-0000:00:12.1-2/input0"


def TeventThread():
    global start, end, ctr  # Add 'global' declaration for start, end, and ctr variables
    print("inside eventThread")
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            ctr = + 1
            current_datetime = datetime.datetime.now()
            start = str(current_datetime)
            # #print("mouse click")
            # if ctr < 3:
            #     start = str(current_datetime)
            # else:
            #     ctr = 0
            #     end = str(current_datetime)
            print("Click:: start="+start+" end= "+end+"\n")	
            
        

def setBrightness(val):
    if os.path.exists('/sys/class/backlight/10-0045/brightness'):
            os.system('echo ' + str(val) +' | sudo tee /sys/class/backlight/10-0045/brightness')


        
def thread():
    global start, end, ctr  # Add 'global' declaration for start, end, and ctr variables
    #initial value
    print("inside Main Thread")
    current_datetime = datetime.datetime.now()
    start = str(current_datetime)
    end   = str(current_datetime)    
    while True: 
        current_datetime = datetime.datetime.now()
        end   = str(current_datetime) 
        # Specify the file path
        file_path = 'configFiles/machineConfig.ini'
        #file_path = '/home/nader/Desktop/work/machineConfig.ini'
        # Read the file content
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Create a ConfigParser object and read the content
        config = configparser.ConfigParser()
        config.read_string(file_content)

        # Get the values of timezone and UTC
        powersave = config.get('display', 'powersave')
        curr_brt = config.get('display', 'brightness')
        #print(str(powersave)+" ## "+str(curr_brt))
        time.sleep(int(powersave))
        #print(start+" ##### "+end)
        tstart=start
        tend=end
        datetime_obj1 = datetime.datetime.strptime(tstart, "%Y-%m-%d %H:%M:%S.%f")
        datetime_obj2 = datetime.datetime.strptime(tend, "%Y-%m-%d %H:%M:%S.%f")
        deltaTime = datetime_obj2 - datetime_obj1
        time_difference_seconds = deltaTime.total_seconds()
        print("delta time : "+str(int(time_difference_seconds))+" powesave: "+str(int(powersave))+"\n")
        if int(time_difference_seconds) > int(powersave):
            print("display off")
            #turn display off
            setBrightness(0)
        else:
            print("display on")
            #turn display on with curr_brt
            setBrightness(int(curr_brt))


# thread()

my_thread = threading.Thread(target=TeventThread)
my_thread2 = threading.Thread(target=thread)
# # Start the thread
my_thread.start()
my_thread2.start()

# # Wait for the thread to complete (optional)
my_thread.join()
my_thread2.join()
        
