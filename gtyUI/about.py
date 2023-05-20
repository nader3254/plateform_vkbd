# -*- coding:utf-8 -*-

import sys

from PyQt5.QtWidgets import QDialog, QApplication

from PyQt5.QtGui import *

import gtyTools.gtyTypes
from uiFiles import ui_about
from gtyTools import tools ,aboutTools
from gtyConfig import language, systemConfig
import uiTools
from PyQt5.QtWidgets import (
	QApplication,
	QDialog,
	QLabel,
	QPushButton,
	QSizePolicy,
	QWidget,
	QLineEdit
)
from PyQt5.QtCore import (
	QCoreApplication,
	QDate,
	QDateTime,
	QLocale,
	QMetaObject,
	QObject,
	QPoint,
	QRect,
	QSize,
	QTime,
	QUrl,
	Qt,
	QTimer,
)
from PyQt5.QtGui import (
	QBrush,
	QColor,
	QConicalGradient,
	QCursor,
	QFont,
	QFontDatabase,
	QGradient,
	QIcon,
	QImage,
	QKeySequence,
	QLinearGradient,
	QPainter,
	QPalette,
	QPixmap,
	QRadialGradient,
	QTransform,
)


class About(QDialog, ui_about.Ui_AboutDialog):

	def __init__(self, mainPage, eventQ, parent=None):
		super(About, self).__init__(parent)
		self.setupUi(self)
		uiTools.centerAndSetIcon(self)
		# 处理不同的语言
		self.setWindowTitle("About")
		self.l = language.lanFromFile()
		self.backButton.setText(language.about_back)

		self.mainPage = mainPage
		self.eventQ = eventQ

		
  
		if self.l == 'english':
			self.aboutLabel.setPixmap(QPixmap("/home/feibot/platform/resources/pic2.png"))
		else:
			self.aboutLabel.setPixmap(QPixmap("/home/feibot/platform/resources/pic1.png"))

		# 配置的控制接口
		self.configHandlers = gtyTools.gtyTypes.ConfigHandlers()

		self.modeBtn.setText('------')
		self.releaseMode = self.configHandlers.state.read('machine', 'releaseMode')
		if 'release' in self.releaseMode:
			self.modeBtn.setText('release mode')
		if 'debug' in self.releaseMode:
			self.modeBtn.setText('debug mode')
		self.modeBtn.clicked.connect(self.setReleaseMode)

		# 显示ip地址
		ips = tools.getIpAddr()
		if ips is not []:
			ipStr = ''
			for ip in ips:
				ipStr += ip + ','
			ipStr = ipStr[:-1]
			#self.textBrowser.append('ip: ' + ipStr)
		self.textBrowser.append('software version: ' + systemConfig.softwareVersion)
		self.textBrowser.append('firmware version: ' + self.configHandlers.state.read('machine', 'firmwareversion'))
		self.init_details()

		 
	# 发生事件
	def sendEvent(self, task, eventName, eventData=None):
		if eventData is None:
			eventData = []
		e = [eventName,  eventData]
		try:
			if task.upper() in self.eventQ.keys():
				self.eventQ[task.upper()].put(e)
		except Exception as e:
			print(e)
   
		

	# 设置调试模式
	def setReleaseMode(self):
		print(__file__, 'setReleaseMode:', self.releaseMode)
		if self.releaseMode == 'release':
			self.sendEvent('UART', 'uart_sendReleaseMode', ['debug'])
			self.releaseMode = 'debug'
			self.configHandlers.state.write('machine', 'releaseMode', 'debug')
			self.modeBtn.setText('debug mode')
			self.sendEvent('UI', 'ui_updateMainDialogValue', {'releaseMode': 'debug'})
			return
		if self.releaseMode == 'debug':
			self.sendEvent('UART', 'uart_sendReleaseMode', ['release'])
			self.releaseMode = 'release'
			self.configHandlers.state.write('machine', 'releaseMode', 'release')
			self.modeBtn.setText('release mode')
			self.sendEvent('UI', 'ui_updateMainDialogValue', {'releaseMode': 'release'})
			return

	# new labels
	def init_details(self):
		font = QFont()
		font.setPointSize(12)
		value_start_x=105

		# Timer for Long Press  
		
		self.long_press_timer = QTimer()
		self.long_press_timer.timeout.connect(self.updateDetailsValues)
		        

		
		# Current time
		self.curr_time_header = QLabel(self)
		self.curr_time_header.setText("Current Time: ")
		self.curr_time_header.setObjectName("label")
		self.curr_time_header.setGeometry(QRect(5, 35*0+2, 105, 35))
		self.curr_time_header.setFont(font)
		self.curr_time_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)

		# up time
		self.up_time_header = QLabel(self)
		self.up_time_header.setText("up Time ")
		self.up_time_header.setObjectName("label")
		self.up_time_header.setGeometry(QRect(5, 35*1+2, 105, 35))
		self.up_time_header.setFont(font)
		self.up_time_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  
  		# cpu 
		self.cpu_header = QLabel(self)
		self.cpu_header.setText("cpu ")
		self.cpu_header.setObjectName("label")
		self.cpu_header.setGeometry(QRect(5, 35*2+2, 105, 35))
		self.cpu_header.setFont(font)
		self.cpu_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
		# eth0
		self.eth0_header = QLabel(self)
		self.eth0_header.setText("eth0 ")
		self.eth0_header.setObjectName("label")
		self.eth0_header.setGeometry(QRect(5, 35*3+2, 105, 35))
		self.eth0_header.setFont(font)
		self.eth0_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  		# eth1
		self.eth0_header = QLabel(self)
		self.eth0_header.setText("eth1 ")
		self.eth0_header.setObjectName("label")
		self.eth0_header.setGeometry(QRect(5, 35*4+2, 105, 35))
		self.eth0_header.setFont(font)
		self.eth0_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
		# wlan0
		self.wlan_header = QLabel(self)
		self.wlan_header.setText("wlan0 ")
		self.wlan_header.setObjectName("label")
		self.wlan_header.setGeometry(QRect(5, 35*5+2, 105, 35))
		self.wlan_header.setFont(font)
		self.wlan_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  
		# Temprature & humidity
		self.sysTempHum_header = QLabel(self)
		self.sysTempHum_header.setText("Temprature & humidity ")
		self.sysTempHum_header.setObjectName("label")
		self.sysTempHum_header.setGeometry(QRect(5, 35*6+2, 250, 35))
		self.sysTempHum_header.setFont(font)
		self.sysTempHum_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  
  
		# system Temp/humidity
		self.sys_header = QLabel(self)
		self.sys_header.setText("System ")
		self.sys_header.setObjectName("label")
		self.sys_header.setGeometry(QRect(3, 35*7+2, 180, 35))
		self.sys_header.setFont(font)
		self.sys_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  
  
		# CPU
		self.tcpu_header = QLabel(self)
		self.tcpu_header.setText("CPU ")
		self.tcpu_header.setObjectName("label")
		self.tcpu_header.setGeometry(QRect(3, 35*8+2, 105, 35))
		self.tcpu_header.setFont(font)
		self.tcpu_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  		# GPU
		self.gpu_header = QLabel(self)
		self.gpu_header.setText("GPU ")
		self.gpu_header.setObjectName("label")
		self.gpu_header.setGeometry(QRect(200, 35*8+2, 105, 35))
		self.gpu_header.setFont(font)
		self.gpu_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  

        # Battery_main
		self.mbattery_val = QLabel(self)
		self.mbattery_val.setText("Main Battery ")
		self.mbattery_val.setObjectName("label")
		self.mbattery_val.setGeometry(QRect(3, 35*9-5, 110, 35))
		self.mbattery_val.setFont(font)
		self.mbattery_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  
      	# Battery_backup
		self.bbattery_header = QLabel(self)
		self.bbattery_header.setText("Backup Battery ")
		self.bbattery_header.setObjectName("label")
		self.bbattery_header.setGeometry(QRect(200, 35*9-5, 120, 35))
		self.bbattery_header.setFont(font)
		self.bbattery_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
      	# Battery_charge
		self.cbattery_header = QLabel(self)
		self.cbattery_header.setText("Charge ")
		self.cbattery_header.setObjectName("label")
		self.cbattery_header.setGeometry(QRect(3, 35*10-12, 105, 35))
		self.cbattery_header.setFont(font)
		self.cbattery_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  
      	# Battery_system
		self.sbattery_header = QLabel(self)
		self.sbattery_header.setText("System ")
		self.sbattery_header.setObjectName("label")
		self.sbattery_header.setGeometry(QRect(200, 35*10-12, 105, 35))
		self.sbattery_header.setFont(font)
		self.sbattery_header.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(255, 255, 255);"
		)
  
  
		######################### Values #############################
		
		
 		# Current time
   
		font.setPointSize(10)
  
  
		self.curr_time_val = QLabel(self)
		self.curr_time_val.setText("Current Time: ")
		self.curr_time_val.setObjectName("label")
		self.curr_time_val.setGeometry(QRect(value_start_x+4, 35*0+2, 250, 35))
		self.curr_time_val.setFont(font)
		self.curr_time_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)

		# up time
		self.up_time_val = QLabel(self)
		self.up_time_val.setText("up Time: ")
		self.up_time_val.setObjectName("label")
		self.up_time_val.setGeometry(QRect(value_start_x+4, 35*1+2, 250, 35))
		self.up_time_val.setFont(font)
		self.up_time_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
  
  		# cpu 
		self.cpu_val = QLabel(self)
		self.cpu_val.setText("cpu: ")
		self.cpu_val.setObjectName("label")
		self.cpu_val.setGeometry(QRect(value_start_x+4, 35*2+7, 250, 35))
		self.cpu_val.setFont(font)
		self.cpu_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
		# eth0
		self.eth0_val = QLabel(self)
		self.eth0_val.setText("eth0: ")
		self.eth0_val.setObjectName("label")
		self.eth0_val.setGeometry(QRect(value_start_x+4, 35*3+2, 260, 35))
		self.eth0_val.setFont(font)
		self.eth0_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
    	# eth1
		self.eth1_val = QLabel(self)
		self.eth1_val.setText("eth1 ")
		self.eth1_val.setObjectName("label")
		self.eth1_val.setGeometry(QRect(5+100, 35*4+2, 250, 35))
		self.eth1_val.setFont(font)
		self.eth1_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
		# wlan0
		self.wlan_val = QLabel(self)
		self.wlan_val.setText("wlan0: ")
		self.wlan_val.setObjectName("label")
		self.wlan_val.setGeometry(QRect(value_start_x+4, 35*5+2, 250, 35))
		self.wlan_val.setFont(font)
		self.wlan_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
  
  		# system Temp/humidity
		self.sys_val = QLabel(self)
		self.sys_val.setText("System ")
		self.sys_val.setObjectName("label")
		self.sys_val.setGeometry(QRect(110, 35*7+2, 180, 35))
		self.sys_val.setFont(font)
		self.sys_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
    
		# CPU
		self.tcpu_val = QLabel(self)
		self.tcpu_val.setText("CPU ")
		self.tcpu_val.setObjectName("label")
		self.tcpu_val.setGeometry(QRect(3+110, 35*8+2, 80, 35))
		self.tcpu_val.setFont(font)
		self.tcpu_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
  		# GPU
		self.gpu_val = QLabel(self)
		self.gpu_val.setText("GPU ")
		self.gpu_val.setObjectName("label")
		self.gpu_val.setGeometry(QRect(200+130, 35*8+2, 105, 35))
		self.gpu_val.setFont(font)
		self.gpu_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
        # Battery_main
		self.mbattery_val = QLabel(self)
		self.mbattery_val.setText("Main Battery ")
		self.mbattery_val.setObjectName("label")
		self.mbattery_val.setGeometry(QRect(3+110, 35*9-5, 80, 35))
		self.mbattery_val.setFont(font)
		self.mbattery_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
      	# Battery_backup
		self.bbattery_val = QLabel(self)
		self.bbattery_val.setText("Backup Battery ")
		self.bbattery_val.setObjectName("label")
		self.bbattery_val.setGeometry(QRect(200+130, 35*9-5, 80, 35))
		self.bbattery_val.setFont(font)
		self.bbattery_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
      	# Battery_charge
		self.cbattery_Val = QLabel(self)
		self.cbattery_Val.setText("Charge ")
		self.cbattery_Val.setObjectName("label")
		self.cbattery_Val.setGeometry(QRect(3+110, 35*10-12, 80, 35))
		self.cbattery_Val.setFont(font)
		self.cbattery_Val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
  
      	# Battery_system
		self.sbattery_val = QLabel(self)
		self.sbattery_val.setText("System ")
		self.sbattery_val.setObjectName("label")
		self.sbattery_val.setGeometry(QRect(200+130, 35*10-12, 80, 35))
		self.sbattery_val.setFont(font)
		self.sbattery_val.setStyleSheet(
			"background-color: rgb(32, 30, 41);\n" "color: rgb(209, 101, 53);"
		)
  
  

		self.bat=aboutTools.battery()
		# starting our timer
		self.long_press_timer.start(300)  
  
	# update details values
	def updateDetailsValues(self):
		self.curr_time_val.setText(aboutTools.getDateTime())
		self.up_time_val.setText(aboutTools.getUpTime())
		self.cpu_val.setText(aboutTools.getCpuUsage())
		self.eth0_val.setText(aboutTools.getEth0())
		self.eth1_val.setText(aboutTools.getEth1())
		self.wlan_val.setText(aboutTools.getWlan0())
		self.sys_val.setText(aboutTools.getDHT22())
		self.tcpu_val.setText(aboutTools.getCpuTemp())
		self.gpu_val.setText(aboutTools.getGpuTemp())
		self.bbattery_val.setText(self.bat.getBackupB_v())
		self.mbattery_val.setText(self.bat.getMainB_v())
		self.cbattery_Val.setText(self.bat.getCharging_v())
		self.sbattery_val.setText(self.bat.getvPcb_v())

  

  
     
	   
   
  
	   