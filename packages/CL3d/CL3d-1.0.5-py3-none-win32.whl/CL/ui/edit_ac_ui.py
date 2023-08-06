# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_ac_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 267)
        Dialog.setMinimumSize(QtCore.QSize(350, 219))
        Dialog.setMaximumSize(QtCore.QSize(350, 1000))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(328, 160))
        self.groupBox.setMaximumSize(QtCore.QSize(328, 99999))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_a = QtWidgets.QLabel(self.groupBox)
        self.label_a.setStyleSheet("")
        self.label_a.setObjectName("label_a")
        self.gridLayout.addWidget(self.label_a, 0, 0, 1, 1)
        self.doubleSpinBox_a = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_a.setDecimals(3)
        self.doubleSpinBox_a.setMinimum(-999999.0)
        self.doubleSpinBox_a.setMaximum(999999.0)
        self.doubleSpinBox_a.setSingleStep(1.0)
        self.doubleSpinBox_a.setObjectName("doubleSpinBox_a")
        self.gridLayout.addWidget(self.doubleSpinBox_a, 0, 1, 1, 1)
        self.doubleSpinBox_c = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_c.setDecimals(3)
        self.doubleSpinBox_c.setMinimum(-999999.0)
        self.doubleSpinBox_c.setMaximum(999999.0)
        self.doubleSpinBox_c.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.doubleSpinBox_c.setObjectName("doubleSpinBox_c")
        self.gridLayout.addWidget(self.doubleSpinBox_c, 1, 1, 1, 1)
        self.label_c = QtWidgets.QLabel(self.groupBox)
        self.label_c.setStyleSheet("")
        self.label_c.setObjectName("label_c")
        self.gridLayout.addWidget(self.label_c, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_ok = QtWidgets.QPushButton(self.frame)
        self.pushButton_ok.setAutoDefault(False)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_reset = QtWidgets.QPushButton(self.frame)
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.horizontalLayout.addWidget(self.pushButton_reset)
        self.pushButton_app = QtWidgets.QPushButton(self.frame)
        self.pushButton_app.setAutoDefault(False)
        self.pushButton_app.setObjectName("pushButton_app")
        self.horizontalLayout.addWidget(self.pushButton_app)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "角度编辑"))
        self.groupBox.setTitle(_translate("Dialog", "位置坐标"))
        self.label_a.setText(_translate("Dialog", "A:"))
        self.label_c.setText(_translate("Dialog", "C:"))
        self.pushButton_ok.setText(_translate("Dialog", "确定"))
        self.pushButton_reset.setText(_translate("Dialog", "重置"))
        self.pushButton_app.setText(_translate("Dialog", "应用"))
