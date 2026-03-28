# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/focal/Desktop/2024_GroundStation/src/GroundStation/GroundStation/myUI/show.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_showDialog(object):
    def setupUi(self, showDialog):
        showDialog.setObjectName("showDialog")
        showDialog.resize(762, 436)
        self.gridLayout = QtWidgets.QGridLayout(showDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(showDialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(showDialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.pushButton_ok = QtWidgets.QPushButton(showDialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pushButton_ok.setFont(font)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.gridLayout.addWidget(self.pushButton_ok, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(showDialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(showDialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.pushButton_cannel = QtWidgets.QPushButton(showDialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pushButton_cannel.setFont(font)
        self.pushButton_cannel.setObjectName("pushButton_cannel")
        self.gridLayout.addWidget(self.pushButton_cannel, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(showDialog)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.gridLayout.setColumnMinimumWidth(0, 1)
        self.gridLayout.setColumnMinimumWidth(1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(showDialog)
        QtCore.QMetaObject.connectSlotsByName(showDialog)

    def retranslateUi(self, showDialog):
        _translate = QtCore.QCoreApplication.translate
        showDialog.setWindowTitle(_translate("showDialog", "Dialog"))
        self.label.setText(_translate("showDialog", "距离货架距离:"))
        self.pushButton_ok.setText(_translate("showDialog", "参数确认"))
        self.label_2.setText(_translate("showDialog", "货架高度:"))
        self.pushButton_cannel.setText(_translate("showDialog", "取消设置"))
        self.label_3.setText(_translate("showDialog", "参数设置"))
