#  GNU nano 5.4                    platformStart2.py                              
# -*- coding:utf-8 -*-

import platform4
import gtyTools.tools
import threading


# 启动平台
import os



def powerSave():
    os.system("python3 ts.py")

# if __name__ == '__main__':
def main():    
    num = gtyTools.tools.checkAlreadyRun()
    if num > 1:
        print("feibot desktop already running!",num)
        exit()
    p = platform4.platForm()
    p.start()



# thread()

my_thread = threading.Thread(target=main)
my_thread2 = threading.Thread(target=powerSave)
# # Start the thread
my_thread.start()
my_thread2.start()

# # Wait for the thread to complete (optional)
my_thread.join()
my_thread2.join()
        