# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'del_point_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 290)
        Dialog.setMinimumSize(QtCore.QSize(350, 219))
        Dialog.setMaximumSize(QtCore.QSize(350, 1000))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_info = QtWidgets.QLabel(Dialog)
        self.label_info.setMinimumSize(QtCore.QSize(0, 40))
        self.label_info.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_info.setFont(font)
        self.label_info.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_info.setStyleSheet("")
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.setObjectName("label_info")
        self.verticalLayout.addWidget(self.label_info)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(328, 120))
        self.groupBox.setMaximumSize(QtCore.QSize(328, 99999))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_z_6 = QtWidgets.QLabel(self.groupBox)
        self.label_z_6.setMinimumSize(QtCore.QSize(50, 0))
        self.label_z_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_z_6.setStyleSheet("")
        self.label_z_6.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_z_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_z_6.setObjectName("label_z_6")
        self.gridLayout.addWidget(self.label_z_6, 0, 0, 1, 1)
        self.lineEdit_select = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_select.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_select.setReadOnly(True)
        self.lineEdit_select.setObjectName("lineEdit_select")
        self.gridLayout.addWidget(self.lineEdit_select, 0, 1, 1, 1)
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
        Dialog.setWindowTitle(_translate("Dialog", "删除点位"))
        self.label_info.setText(_translate("Dialog", "删除NC点"))
        self.groupBox.setTitle(_translate("Dialog", "点位信息"))
        self.label_z_6.setText(_translate("Dialog", "点"))
        self.pushButton_ok.setText(_translate("Dialog", "确定"))
        self.pushButton_reset.setText(_translate("Dialog", "重置"))
        self.pushButton_app.setText(_translate("Dialog", "应用"))
