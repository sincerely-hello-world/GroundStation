# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/focal/Desktop/2024_GroundStation/src/GroundStation/GroundStation/main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 282)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 40, 301, 126))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_ipG = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_ipG.setObjectName("label_ipG")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_ipG)
        self.label_ipF = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_ipF.setObjectName("label_ipF")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_ipF)
        self.lineEdit_status = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_status.setObjectName("lineEdit_status")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_status)
        self.lineEdit_ipF = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_ipF.setObjectName("lineEdit_ipF")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_ipF)
        self.lineEdit_ipG = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_ipG.setObjectName("lineEdit_ipG")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_ipG)
        self.label_status = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_status.setObjectName("label_status")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_status)
        self.line = QtWidgets.QFrame(self.formLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line)
        self.label_pos = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_pos.setObjectName("label_pos")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_pos)
        self.lineEdit_pos = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_pos.setObjectName("lineEdit_pos")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_pos)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(350, 40, 261, 107))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_land = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_land.setObjectName("pushButton_land")
        self.gridLayout_2.addWidget(self.pushButton_land, 2, 0, 1, 1)
        self.pushButton_takeoff = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_takeoff.setObjectName("pushButton_takeoff")
        self.gridLayout_2.addWidget(self.pushButton_takeoff, 0, 0, 1, 1)
        self.pushButton_runtask = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_runtask.setObjectName("pushButton_runtask")
        self.gridLayout_2.addWidget(self.pushButton_runtask, 1, 0, 1, 1)
        self.pushButton_openDialog1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_openDialog1.setGeometry(QtCore.QRect(40, 190, 151, 41))
        self.pushButton_openDialog1.setObjectName("pushButton_openDialog1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 720, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_ipG.setText(_translate("MainWindow", "地面站ip地址:"))
        self.label_ipF.setText(_translate("MainWindow", "飞行站ip地址:"))
        self.label_status.setText(_translate("MainWindow", "连接情况:"))
        self.label_pos.setText(_translate("MainWindow", "飞机当前位置:"))
        self.pushButton_land.setText(_translate("MainWindow", "降落"))
        self.pushButton_takeoff.setText(_translate("MainWindow", "起飞"))
        self.pushButton_runtask.setText(_translate("MainWindow", "执行任务"))
        self.pushButton_openDialog1.setText(_translate("MainWindow", "打开手动控制页面"))
