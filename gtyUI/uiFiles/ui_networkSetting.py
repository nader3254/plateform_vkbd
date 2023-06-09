# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'networkSetting.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_networkSetting(object):
    def setupUi(self, networkSetting):
        networkSetting.setObjectName("networkSetting")
        networkSetting.resize(600, 420)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(networkSetting.sizePolicy().hasHeightForWidth())
        networkSetting.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        networkSetting.setFont(font)
        networkSetting.setStyleSheet("background-color: rgb(32, 30, 41);\n"
"color: rgb(255, 255, 255);")
        self.textEditInfo = QtWidgets.QTextEdit(networkSetting)
        self.textEditInfo.setGeometry(QtCore.QRect(10, 50, 581, 101))
        self.textEditInfo.setObjectName("textEditInfo")
        self.label = QtWidgets.QLabel(networkSetting)
        self.label.setGeometry(QtCore.QRect(10, 20, 181, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(networkSetting)
        self.label_2.setGeometry(QtCore.QRect(10, 220, 81, 41))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.lineEditIp = QtWidgets.QLineEdit(networkSetting)
        self.lineEditIp.setGeometry(QtCore.QRect(100, 220, 211, 41))
        self.lineEditIp.setObjectName("lineEditIp")
        self.lineEditPort = QtWidgets.QLineEdit(networkSetting)
        self.lineEditPort.setGeometry(QtCore.QRect(440, 220, 111, 41))
        self.lineEditPort.setObjectName("lineEditPort")
        self.label_3 = QtWidgets.QLabel(networkSetting)
        self.label_3.setGeometry(QtCore.QRect(350, 220, 81, 41))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(networkSetting)
        self.label_4.setGeometry(QtCore.QRect(10, 170, 201, 21))
        self.label_4.setObjectName("label_4")
        self.btnBack = QtWidgets.QPushButton(networkSetting)
        self.btnBack.setGeometry(QtCore.QRect(490, 350, 101, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnBack.setFont(font)
        self.btnBack.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnBack.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.btnBack.setObjectName("btnBack")
        self.btnSet = QtWidgets.QPushButton(networkSetting)
        self.btnSet.setGeometry(QtCore.QRect(10, 350, 131, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnSet.setFont(font)
        self.btnSet.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnSet.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.btnSet.setObjectName("btnSet")
        self.labelInfo = QtWidgets.QLabel(networkSetting)
        self.labelInfo.setGeometry(QtCore.QRect(10, 300, 581, 31))
        self.labelInfo.setText("")
        self.labelInfo.setObjectName("labelInfo")
        self.btnConnect = QtWidgets.QPushButton(networkSetting)
        self.btnConnect.setGeometry(QtCore.QRect(150, 350, 141, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnConnect.setFont(font)
        self.btnConnect.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnConnect.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.btnConnect.setObjectName("btnConnect")

        self.retranslateUi(networkSetting)
        QtCore.QMetaObject.connectSlotsByName(networkSetting)

    def retranslateUi(self, networkSetting):
        _translate = QtCore.QCoreApplication.translate
        networkSetting.setWindowTitle(_translate("networkSetting", "网络设置"))
        self.label.setText(_translate("networkSetting", "网络状态"))
        self.label_2.setText(_translate("networkSetting", "IP地址"))
        self.label_3.setText(_translate("networkSetting", "端口"))
        self.label_4.setText(_translate("networkSetting", "UDP目标主机配置："))
        self.btnBack.setText(_translate("networkSetting", "返回"))
        self.btnSet.setText(_translate("networkSetting", "设置"))
        self.btnConnect.setText(_translate("networkSetting", "打开"))
