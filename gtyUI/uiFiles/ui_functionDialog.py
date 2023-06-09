# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'functionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_functionDialog(object):
    def setupUi(self, functionDialog):
        functionDialog.setObjectName("functionDialog")
        functionDialog.resize(332, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(functionDialog.sizePolicy().hasHeightForWidth())
        functionDialog.setSizePolicy(sizePolicy)
        functionDialog.setStyleSheet("background-color: rgb(32, 30, 41);")
        self.tagCheckBtn = QtWidgets.QPushButton(functionDialog)
        self.tagCheckBtn.setGeometry(QtCore.QRect(0, 0, 331, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tagCheckBtn.setFont(font)
        self.tagCheckBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tagCheckBtn.setStyleSheet("background-color: rgb(66, 79, 131);\n"
"color: rgb(255, 255, 255);")
        self.tagCheckBtn.setObjectName("tagCheckBtn")
        self.testButton = QtWidgets.QPushButton(functionDialog)
        self.testButton.setGeometry(QtCore.QRect(0, 120, 331, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.testButton.setFont(font)
        self.testButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.testButton.setStyleSheet("background-color: rgb(66, 79, 131);\n"
"color: rgb(255, 255, 255);")
        self.testButton.setObjectName("testButton")
        self.backButton = QtWidgets.QPushButton(functionDialog)
        self.backButton.setGeometry(QtCore.QRect(0, 340, 331, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.backButton.setFont(font)
        self.backButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.backButton.setStyleSheet("background-color: rgb(66, 79, 131);\n"
"color: rgb(255, 255, 255);")
        self.backButton.setObjectName("backButton")
        self.timeResultDisplayBtn = QtWidgets.QPushButton(functionDialog)
        self.timeResultDisplayBtn.setGeometry(QtCore.QRect(0, 60, 331, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.timeResultDisplayBtn.setFont(font)
        self.timeResultDisplayBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.timeResultDisplayBtn.setStyleSheet("background-color: rgb(66, 79, 131);\n"
"color: rgb(255, 255, 255);")
        self.timeResultDisplayBtn.setObjectName("timeResultDisplayBtn")
        self.writeEpcButton = QtWidgets.QPushButton(functionDialog)
        self.writeEpcButton.setGeometry(QtCore.QRect(0, 180, 331, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.writeEpcButton.setFont(font)
        self.writeEpcButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.writeEpcButton.setStyleSheet("background-color: rgb(66, 79, 131);\n"
"color: rgb(255, 255, 255);")
        self.writeEpcButton.setObjectName("writeEpcButton")

        self.retranslateUi(functionDialog)
        self.backButton.clicked.connect(functionDialog.accept) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(functionDialog)

    def retranslateUi(self, functionDialog):
        _translate = QtCore.QCoreApplication.translate
        functionDialog.setWindowTitle(_translate("functionDialog", "功能"))
        self.tagCheckBtn.setText(_translate("functionDialog", "芯片检测"))
        self.testButton.setText(_translate("functionDialog", "系统测试"))
        self.backButton.setText(_translate("functionDialog", "返     回"))
        self.timeResultDisplayBtn.setText(_translate("functionDialog", "成绩显示"))
        self.writeEpcButton.setText(_translate("functionDialog", "标签写入"))
