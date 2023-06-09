# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'operate.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_operateDialog(object):
    def setupUi(self, operateDialog):
        operateDialog.setObjectName("operateDialog")
        operateDialog.resize(700, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(operateDialog.sizePolicy().hasHeightForWidth())
        operateDialog.setSizePolicy(sizePolicy)
        operateDialog.setMinimumSize(QtCore.QSize(30, 30))
        operateDialog.setStyleSheet("background-color: rgb(32, 30, 41);\n"
"color: rgb(255, 255, 255);")
        self.readControlBtn1Start = QtWidgets.QPushButton(operateDialog)
        self.readControlBtn1Start.setGeometry(QtCore.QRect(180, 10, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.readControlBtn1Start.setFont(font)
        self.readControlBtn1Start.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.readControlBtn1Start.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.readControlBtn1Start.setObjectName("readControlBtn1Start")
        self.readControlBtn2Start = QtWidgets.QPushButton(operateDialog)
        self.readControlBtn2Start.setGeometry(QtCore.QRect(180, 80, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.readControlBtn2Start.setFont(font)
        self.readControlBtn2Start.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.readControlBtn2Start.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.readControlBtn2Start.setObjectName("readControlBtn2Start")
        self.returnBtn = QtWidgets.QPushButton(operateDialog)
        self.returnBtn.setGeometry(QtCore.QRect(560, 390, 130, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.returnBtn.setFont(font)
        self.returnBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.returnBtn.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.returnBtn.setObjectName("returnBtn")
        self.shutdownBtn = QtWidgets.QPushButton(operateDialog)
        self.shutdownBtn.setGeometry(QtCore.QRect(420, 390, 130, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.shutdownBtn.setFont(font)
        self.shutdownBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.shutdownBtn.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.shutdownBtn.setObjectName("shutdownBtn")
        self.fanControlBtn_on = QtWidgets.QPushButton(operateDialog)
        self.fanControlBtn_on.setGeometry(QtCore.QRect(0, 390, 130, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.fanControlBtn_on.setFont(font)
        self.fanControlBtn_on.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.fanControlBtn_on.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.fanControlBtn_on.setObjectName("fanControlBtn_on")
        self.fanControlBtn_off = QtWidgets.QPushButton(operateDialog)
        self.fanControlBtn_off.setGeometry(QtCore.QRect(140, 390, 130, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.fanControlBtn_off.setFont(font)
        self.fanControlBtn_off.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.fanControlBtn_off.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.fanControlBtn_off.setObjectName("fanControlBtn_off")
        self.readerRebootBtn1 = QtWidgets.QPushButton(operateDialog)
        self.readerRebootBtn1.setGeometry(QtCore.QRect(440, 10, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.readerRebootBtn1.setFont(font)
        self.readerRebootBtn1.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.readerRebootBtn1.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.readerRebootBtn1.setObjectName("readerRebootBtn1")
        self.readerRebootBtn2 = QtWidgets.QPushButton(operateDialog)
        self.readerRebootBtn2.setGeometry(QtCore.QRect(440, 80, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.readerRebootBtn2.setFont(font)
        self.readerRebootBtn2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.readerRebootBtn2.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.readerRebootBtn2.setObjectName("readerRebootBtn2")
        self.label = QtWidgets.QLabel(operateDialog)
        self.label.setGeometry(QtCore.QRect(20, 15, 116, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(operateDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 116, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_info = QtWidgets.QLabel(operateDialog)
        self.label_info.setGeometry(QtCore.QRect(330, 165, 311, 21))
        self.label_info.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_info.setText("")
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.setObjectName("label_info")
        self.readerSetBtn2 = QtWidgets.QPushButton(operateDialog)
        self.readerSetBtn2.setGeometry(QtCore.QRect(570, 80, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.readerSetBtn2.setFont(font)
        self.readerSetBtn2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.readerSetBtn2.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.readerSetBtn2.setObjectName("readerSetBtn2")
        self.readerSetBtn1 = QtWidgets.QPushButton(operateDialog)
        self.readerSetBtn1.setGeometry(QtCore.QRect(570, 10, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.readerSetBtn1.setFont(font)
        self.readerSetBtn1.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.readerSetBtn1.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.readerSetBtn1.setObjectName("readerSetBtn1")
        self.groupBox = QtWidgets.QGroupBox(operateDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 180, 241, 191))
        self.groupBox.setObjectName("groupBox")
        self.checkBox_2Byte = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2Byte.setGeometry(QtCore.QRect(20, 40, 78, 30))
        self.checkBox_2Byte.setIconSize(QtCore.QSize(50, 40))
        self.checkBox_2Byte.setObjectName("checkBox_2Byte")
        self.checkBox_12Byte = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_12Byte.setGeometry(QtCore.QRect(20, 140, 87, 30))
        self.checkBox_12Byte.setIconSize(QtCore.QSize(50, 40))
        self.checkBox_12Byte.setObjectName("checkBox_12Byte")
        self.checkBox_16Byte = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_16Byte.setGeometry(QtCore.QRect(130, 140, 87, 30))
        self.checkBox_16Byte.setIconSize(QtCore.QSize(50, 40))
        self.checkBox_16Byte.setObjectName("checkBox_16Byte")
        self.checkBox_6Byte = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_6Byte.setGeometry(QtCore.QRect(20, 90, 78, 30))
        self.checkBox_6Byte.setIconSize(QtCore.QSize(50, 40))
        self.checkBox_6Byte.setObjectName("checkBox_6Byte")
        self.checkBox_8Byte = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_8Byte.setGeometry(QtCore.QRect(130, 90, 78, 30))
        self.checkBox_8Byte.setIconSize(QtCore.QSize(50, 40))
        self.checkBox_8Byte.setObjectName("checkBox_8Byte")
        self.checkBox_4Byte = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_4Byte.setGeometry(QtCore.QRect(130, 40, 78, 30))
        self.checkBox_4Byte.setIconSize(QtCore.QSize(50, 40))
        self.checkBox_4Byte.setObjectName("checkBox_4Byte")
        self.readControlBtn1Stop = QtWidgets.QPushButton(operateDialog)
        self.readControlBtn1Stop.setGeometry(QtCore.QRect(310, 10, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.readControlBtn1Stop.setFont(font)
        self.readControlBtn1Stop.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.readControlBtn1Stop.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.readControlBtn1Stop.setObjectName("readControlBtn1Stop")
        self.readControlBtn2Stop = QtWidgets.QPushButton(operateDialog)
        self.readControlBtn2Stop.setGeometry(QtCore.QRect(310, 80, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.readControlBtn2Stop.setFont(font)
        self.readControlBtn2Stop.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.readControlBtn2Stop.setStyleSheet("background-color: rgb(66, 79, 131);")
        self.readControlBtn2Stop.setObjectName("readControlBtn2Stop")

        self.retranslateUi(operateDialog)
        self.returnBtn.clicked.connect(operateDialog.accept) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(operateDialog)

    def retranslateUi(self, operateDialog):
        _translate = QtCore.QCoreApplication.translate
        operateDialog.setWindowTitle(_translate("operateDialog", "操作"))
        self.readControlBtn1Start.setText(_translate("operateDialog", "开始读取"))
        self.readControlBtn2Start.setText(_translate("operateDialog", "开始读取"))
        self.returnBtn.setText(_translate("operateDialog", "返回"))
        self.shutdownBtn.setText(_translate("operateDialog", "关机"))
        self.fanControlBtn_on.setText(_translate("operateDialog", "风扇开"))
        self.fanControlBtn_off.setText(_translate("operateDialog", "风扇关"))
        self.readerRebootBtn1.setText(_translate("operateDialog", "重启"))
        self.readerRebootBtn2.setText(_translate("operateDialog", "重启"))
        self.label.setText(_translate("operateDialog", "读写器1："))
        self.label_2.setText(_translate("operateDialog", "读写器2："))
        self.readerSetBtn2.setText(_translate("operateDialog", "设置"))
        self.readerSetBtn1.setText(_translate("operateDialog", "设置"))
        self.groupBox.setTitle(_translate("operateDialog", "允许的EPC字节数"))
        self.checkBox_2Byte.setText(_translate("operateDialog", "2字节"))
        self.checkBox_12Byte.setText(_translate("operateDialog", "12字节"))
        self.checkBox_16Byte.setText(_translate("operateDialog", "16字节"))
        self.checkBox_6Byte.setText(_translate("operateDialog", "6字节"))
        self.checkBox_8Byte.setText(_translate("operateDialog", "8字节"))
        self.checkBox_4Byte.setText(_translate("operateDialog", "4字节"))
        self.readControlBtn1Stop.setText(_translate("operateDialog", "开始读取"))
        self.readControlBtn2Stop.setText(_translate("operateDialog", "开始读取"))
