# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './plateform/gtyUI/uiFiles/machineSetting.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_machineSetting(object):
    def setupUi(self, machineSetting):
        machineSetting.setObjectName("machineSetting")
        machineSetting.resize(350, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(machineSetting.sizePolicy().hasHeightForWidth())
        machineSetting.setSizePolicy(sizePolicy)
        machineSetting.setStyleSheet("background-color: rgb(32, 30, 41);\n"
"color: rgb(255, 255, 255);")
        self.timeDateSettingBtn = QtWidgets.QPushButton(machineSetting)
        self.timeDateSettingBtn.setGeometry(QtCore.QRect(10, 60, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.timeDateSettingBtn.setFont(font)
        self.timeDateSettingBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.timeDateSettingBtn.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.timeDateSettingBtn.setObjectName("timeDateSettingBtn")
        self.updateBtn = QtWidgets.QPushButton(machineSetting)
        self.updateBtn.setGeometry(QtCore.QRect(10, 210, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.updateBtn.setFont(font)
        self.updateBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.updateBtn.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.updateBtn.setObjectName("updateBtn")
        self.returnBtn = QtWidgets.QPushButton(machineSetting)
        self.returnBtn.setGeometry(QtCore.QRect(10, 330, 331, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.returnBtn.setFont(font)
        self.returnBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.returnBtn.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.returnBtn.setObjectName("returnBtn")
        self.operateBtn = QtWidgets.QPushButton(machineSetting)
        self.operateBtn.setGeometry(QtCore.QRect(10, 10, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.operateBtn.setFont(font)
        self.operateBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.operateBtn.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.operateBtn.setObjectName("operateBtn")
        self.networkBtn = QtWidgets.QPushButton(machineSetting)
        self.networkBtn.setGeometry(QtCore.QRect(10, 160, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.networkBtn.setFont(font)
        self.networkBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.networkBtn.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.networkBtn.setObjectName("networkBtn")
        self.displayBtn = QtWidgets.QPushButton(machineSetting)
        self.displayBtn.setGeometry(QtCore.QRect(10, 110, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.displayBtn.setFont(font)
        self.displayBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.displayBtn.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.displayBtn.setObjectName("displayBtn")

        self.retranslateUi(machineSetting)
        self.returnBtn.clicked.connect(machineSetting.accept)
        QtCore.QMetaObject.connectSlotsByName(machineSetting)

    def retranslateUi(self, machineSetting):
        _translate = QtCore.QCoreApplication.translate
        machineSetting.setWindowTitle(_translate("machineSetting", "设备设置"))
        self.timeDateSettingBtn.setText(_translate("machineSetting", "日期时间设置"))
        self.updateBtn.setText(_translate("machineSetting", "软件升级"))
        self.returnBtn.setText(_translate("machineSetting", "返回"))
        self.operateBtn.setText(_translate("machineSetting", "操作"))
        self.networkBtn.setText(_translate("machineSetting", "网络设置"))
        self.displayBtn.setText(_translate("machineSetting", "显示设置"))
