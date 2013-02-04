# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created: Sun Feb 03 16:42:02 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(337, 295)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/client.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(":/net.png")))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setMargin(5)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.username = QtGui.QLineEdit(self.centralwidget)
        self.username.setObjectName(_fromUtf8("username"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.username)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.password = QtGui.QLineEdit(self.centralwidget)
        self.password.setObjectName(_fromUtf8("password"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.password)
        self.savepass = QtGui.QCheckBox(self.centralwidget)
        self.savepass.setObjectName(_fromUtf8("savepass"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.savepass)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(60, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.connect = QtGui.QPushButton(self.centralwidget)
        self.connect.setObjectName(_fromUtf8("connect"))
        self.horizontalLayout_3.addWidget(self.connect)
        self.disconnect = QtGui.QPushButton(self.centralwidget)
        self.disconnect.setObjectName(_fromUtf8("disconnect"))
        self.horizontalLayout_3.addWidget(self.disconnect)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ADSL拨号客户端", None))
        self.label.setText(_translate("MainWindow", "用户名：", None))
        self.label_2.setText(_translate("MainWindow", "密码：", None))
        self.savepass.setText(_translate("MainWindow", "在本机保存密码", None))
        self.connect.setText(_translate("MainWindow", "连接", None))
        self.disconnect.setText(_translate("MainWindow", "断开", None))

import res_rc



