# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/project/parsec/core/gui/forms/device_recovery_export_page1_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DeviceRecoveryExportPage1Widget(object):
    def setupUi(self, DeviceRecoveryExportPage1Widget):
        DeviceRecoveryExportPage1Widget.setObjectName("DeviceRecoveryExportPage1Widget")
        DeviceRecoveryExportPage1Widget.resize(550, 351)
        self.verticalLayout = QtWidgets.QVBoxLayout(DeviceRecoveryExportPage1Widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(DeviceRecoveryExportPage1Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(DeviceRecoveryExportPage1Widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(20, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.combo_devices = QtWidgets.QComboBox(DeviceRecoveryExportPage1Widget)
        self.combo_devices.setObjectName("combo_devices")
        self.horizontalLayout_3.addWidget(self.combo_devices)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(DeviceRecoveryExportPage1Widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(20, -1, -1, 0)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_select_file = QtWidgets.QPushButton(DeviceRecoveryExportPage1Widget)
        self.button_select_file.setObjectName("button_select_file")
        self.horizontalLayout_2.addWidget(self.button_select_file)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.label_file_path = QtWidgets.QLabel(DeviceRecoveryExportPage1Widget)
        self.label_file_path.setText("")
        self.label_file_path.setObjectName("label_file_path")
        self.verticalLayout_6.addWidget(self.label_file_path)
        self.verticalLayout_4.addLayout(self.verticalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(DeviceRecoveryExportPage1Widget)
        QtCore.QMetaObject.connectSlotsByName(DeviceRecoveryExportPage1Widget)

    def retranslateUi(self, DeviceRecoveryExportPage1Widget):
        _translate = QtCore.QCoreApplication.translate
        DeviceRecoveryExportPage1Widget.setWindowTitle(_translate("DeviceRecoveryExportPage1Widget", "Form"))
        self.label.setText(_translate("DeviceRecoveryExportPage1Widget", "TEXT_DEVICE_RECOVERY_EXPORT_INSTRUCTIONS"))
        self.label_4.setText(_translate("DeviceRecoveryExportPage1Widget", "TEXT_DEVICE_RECOVERY_EXPORT_SELECT_DEVICE_LABEL"))
        self.label_3.setText(_translate("DeviceRecoveryExportPage1Widget", "TEXT_DEVICE_RECOVERY_EXPORT_SELECT_FILE_LABEL"))
        self.button_select_file.setText(_translate("DeviceRecoveryExportPage1Widget", "ACTION_DEVICE_RECOVERY_EXPORT_SELECT_FILE"))
