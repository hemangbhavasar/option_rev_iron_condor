# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_file.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from yahoo_fin.options import *
from yahoo_fin.stock_info import *
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import requests


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(630, 430)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 70, 331, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stock_line = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.stock_line.setObjectName("stock_line")
        self.horizontalLayout.addWidget(self.stock_line)
        self.get_stock_pb = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.get_stock_pb.setObjectName("get_stock_pb")
        self.horizontalLayout.addWidget(self.get_stock_pb)
        self.stock_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.stock_label.setObjectName("stock_label")
        self.horizontalLayout.addWidget(self.stock_label)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 321, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setBuddy(self.label_2)

        self.retranslateUi(Form)
        self.get_stock_pb.clicked.connect(self.on_click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.get_stock_pb.setText(_translate("Form", "Get stock"))
        self.stock_label.setText(_translate("Form", "No stock selected"))
        self.label_2.setText(_translate("Form",  "Select your underlying "
                                                 "stock :"))

    def on_click(self):
        stock_value = self.stock_line.text()
        try:
            label_value = get_live_price(stock_value)
            exp_date_list = get_expiration_dates(stock_value)
            self.stock_label.setText(str(np.around(label_value, decimals=2)))

        except requests.ConnectionError:
            self.stock_label.setText("Connection Error")
        except AssertionError:
            self.stock_label.setText("Stock could not be found")

    def add_to_list(self, exp_list):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
