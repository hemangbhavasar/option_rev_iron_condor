# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_file.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from yahoo_fin.options import *
from yahoo_fin.stock_info import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView
import numpy as np
import requests


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(630, 432)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 70, 331, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
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
        self.stock_status = QtWidgets.QCheckBox(Form)
        self.stock_status.setGeometry(QtCore.QRect(490, 90, 81, 20))
        # self.stock_status.setCheckable(False)
        self.stock_status.setChecked(False)
        self.stock_status.setObjectName("stock_status")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 190, 389, 161))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.list_exp = QtWidgets.QListView(self.horizontalLayoutWidget_2)
        self.list_exp.setObjectName("list_exp")

        self.horizontalLayout_2.addWidget(self.list_exp)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.exp_add_pb = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.exp_add_pb.setObjectName("exp_add_pb")
        self.verticalLayout.addWidget(self.exp_add_pb)
        self.exp_remove_pb = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.exp_remove_pb.setObjectName("exp_remove_pb")
        self.verticalLayout.addWidget(self.exp_remove_pb)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.list_exp_select = QtWidgets.QListView(self.horizontalLayoutWidget_2)
        self.list_exp_select.setObjectName("list_exp_select")
        self.horizontalLayout_2.addWidget(self.list_exp_select)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 160, 321, 16))
        self.label_3.setObjectName("label_3")
        self.exp_status = QtWidgets.QCheckBox(Form)
        self.exp_status.setGeometry(QtCore.QRect(490, 260, 81, 20))
        self.exp_status.setCheckable(False)
        self.exp_status.setChecked(False)
        self.exp_status.setObjectName("exp_status")
        self.label_2.setBuddy(self.label_2)
        self.label_3.setBuddy(self.label_2)

# -------------------------------------------->
        self.retranslateUi(Form)
        self.get_stock_pb.clicked.connect(self.on_click)
        self.list_exp.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QtCore.QMetaObject.connectSlotsByName(Form)
# --------------------------------------------<

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.get_stock_pb.setText(_translate("Form", "Get stock"))
        self.stock_label.setText(_translate("Form", "No stock selected"))
        self.label_2.setText(_translate("Form", "Select your underlying stock :"))
        self.stock_status.setText(_translate("Form", "Status"))
        self.exp_add_pb.setText(_translate("Form", "Add date ->"))
        self.exp_remove_pb.setText(_translate("Form", "<- Remove date"))
        self.label_3.setText(_translate("Form", "Select the experation dates you want to track"))
        self.exp_status.setText(_translate("Form", "Status"))

# -------------------------------------------->
    def on_click(self):
        stock_value = self.stock_line.text()
        try:
            label_value = get_live_price(stock_value)
            exp_date_list = get_expiration_dates(stock_value)
            self.stock_label.setText(str(np.around(label_value, decimals=2)))
            self.stock_status.setChecked(True)

            model = QtGui.QStandardItemModel()
            self.list_exp.setModel(model)
            for i in exp_date_list:
                item = QtGui.QStandardItem(i)
                model.appendRow(item)

        except requests.ConnectionError:
            self.stock_label.setText("Connection Error")
        except AssertionError:
            self.stock_label.setText("Stock could not be found")

    def add_to_list(self, exp_list):
        pass
# --------------------------------------------<

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
