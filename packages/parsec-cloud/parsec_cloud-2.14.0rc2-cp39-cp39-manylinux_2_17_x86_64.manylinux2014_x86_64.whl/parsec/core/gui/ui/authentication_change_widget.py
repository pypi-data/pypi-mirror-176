# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/project/parsec/core/gui/forms/authentication_change_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AuthenticationChangeWidget(object):
    def setupUi(self, AuthenticationChangeWidget):
        AuthenticationChangeWidget.setObjectName("AuthenticationChangeWidget")
        AuthenticationChangeWidget.resize(524, 301)
        self.verticalLayout = QtWidgets.QVBoxLayout(AuthenticationChangeWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.widget_auth = AuthenticationChoiceWidget(AuthenticationChangeWidget)
        self.widget_auth.setObjectName("widget_auth")
        self.main_layout.addWidget(self.widget_auth)
        self.verticalLayout.addLayout(self.main_layout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_validate = QtWidgets.QPushButton(AuthenticationChangeWidget)
        self.button_validate.setObjectName("button_validate")
        self.horizontalLayout.addWidget(self.button_validate)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AuthenticationChangeWidget)
        QtCore.QMetaObject.connectSlotsByName(AuthenticationChangeWidget)

    def retranslateUi(self, AuthenticationChangeWidget):
        _translate = QtCore.QCoreApplication.translate
        AuthenticationChangeWidget.setWindowTitle(_translate("AuthenticationChangeWidget", "Form"))
        self.button_validate.setText(_translate("AuthenticationChangeWidget", "ACTION_NEXT"))
from parsec.core.gui.authentication_choice_widget import AuthenticationChoiceWidget
