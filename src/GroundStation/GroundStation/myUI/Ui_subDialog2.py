# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/focal/Desktop/2024_GroundStation/src/GroundStation/GroundStation/myUI/subDialog2.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_carControl(object):
    def setupUi(self, carControl):
        carControl.setObjectName("carControl")
        carControl.resize(676, 439)
        self.gridLayout = QtWidgets.QGridLayout(carControl)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBoxE = QtWidgets.QCheckBox(carControl)
        self.checkBoxE.setObjectName("checkBoxE")
        self.gridLayout_2.addWidget(self.checkBoxE, 1, 1, 1, 1)
        self.checkBoxA = QtWidgets.QCheckBox(carControl)
        self.checkBoxA.setObjectName("checkBoxA")
        self.gridLayout_2.addWidget(self.checkBoxA, 0, 0, 1, 1)
        self.checkBoxF = QtWidgets.QCheckBox(carControl)
        self.checkBoxF.setObjectName("checkBoxF")
        self.gridLayout_2.addWidget(self.checkBoxF, 2, 1, 1, 1)
        self.checkBoxC = QtWidgets.QCheckBox(carControl)
        self.checkBoxC.setObjectName("checkBoxC")
        self.gridLayout_2.addWidget(self.checkBoxC, 2, 0, 1, 1)
        self.checkBoxB = QtWidgets.QCheckBox(carControl)
        self.checkBoxB.setObjectName("checkBoxB")
        self.gridLayout_2.addWidget(self.checkBoxB, 1, 0, 1, 1)
        self.checkBoxD = QtWidgets.QCheckBox(carControl)
        self.checkBoxD.setObjectName("checkBoxD")
        self.gridLayout_2.addWidget(self.checkBoxD, 0, 1, 1, 1)
        self.pushButton_runTask = QtWidgets.QPushButton(carControl)
        self.pushButton_runTask.setObjectName("pushButton_runTask")
        self.gridLayout_2.addWidget(self.pushButton_runTask, 4, 1, 1, 1)
        self.pushButton_setTask = QtWidgets.QPushButton(carControl)
        self.pushButton_setTask.setObjectName("pushButton_setTask")
        self.gridLayout_2.addWidget(self.pushButton_setTask, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_stop = QtWidgets.QPushButton(carControl)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout.addWidget(self.pushButton_stop)
        self.pushButton_unlock = QtWidgets.QPushButton(carControl)
        self.pushButton_unlock.setObjectName("pushButton_unlock")
        self.horizontalLayout.addWidget(self.pushButton_unlock)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(carControl)
        QtCore.QMetaObject.connectSlotsByName(carControl)

    def retranslateUi(self, carControl):
        _translate = QtCore.QCoreApplication.translate
        carControl.setWindowTitle(_translate("carControl", "Form"))
        self.checkBoxE.setText(_translate("carControl", "E"))
        self.checkBoxA.setText(_translate("carControl", "A"))
        self.checkBoxF.setText(_translate("carControl", "F"))
        self.checkBoxC.setText(_translate("carControl", "C"))
        self.checkBoxB.setText(_translate("carControl", "B"))
        self.checkBoxD.setText(_translate("carControl", "D"))
        self.pushButton_runTask.setText(_translate("carControl", "执行任务"))
        self.pushButton_setTask.setText(_translate("carControl", "设置任务"))
        self.pushButton_stop.setText(_translate("carControl", "终止小车/停止"))
        self.pushButton_unlock.setText(_translate("carControl", "解锁小车"))
