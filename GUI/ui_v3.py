# -*- coding: utf-8 -*-

"""
Main GUI Window for Iron condor price tracker
Written by: Peter Agalakov
version: v0.1(04-April-2020)

V0.1
*Initial release for main window
"""


from yahoo_fin.options import *
from yahoo_fin.stock_info import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QFileDialog
import numpy as np
import requests


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(560, 660)
        self.stock_string = QtWidgets.QLabel()
        self.stock_string.setVisible(False)
        self.gb_stocks = QtWidgets.QGroupBox(Form)
        self.gb_stocks.setGeometry(QtCore.QRect(20, 40, 521, 101))
        self.gb_stocks.setObjectName("gb_stocks")
        self.gb_exp_dates = QtWidgets.QGroupBox(Form)
        self.gb_exp_dates.setGeometry(QtCore.QRect(20, 150, 521, 201))
        self.gb_exp_dates.setObjectName("gb_exp_dates")
        self.gb_strategy = QtWidgets.QGroupBox(Form)
        self.gb_strategy.setGeometry(QtCore.QRect(20, 350, 521, 181))
        self.gb_strategy.setObjectName("gb_strategy")
        self.gridLayoutWidget = QtWidgets.QWidget(self.gb_strategy)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(19, 20, 471, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 70, 352, 61))
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

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 170, 389, 161))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.list_exp = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
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
        self.list_exp_select = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        self.list_exp_select.setObjectName("list_exp_select")
        self.horizontalLayout_2.addWidget(self.list_exp_select)

        self.label_leg2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_leg2.setObjectName("label_leg2")
        self.gridLayout.addWidget(self.label_leg2, 0, 1, 1, 1)
        self.label_leg1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_leg1.setObjectName("label_leg1")
        self.gridLayout.addWidget(self.label_leg1, 0, 0, 1, 1)
        self.label_leg4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_leg4.setObjectName("label_leg4")
        self.gridLayout.addWidget(self.label_leg4, 0, 3, 1, 1)
        self.cb_leg1_sell_buy = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_leg1_sell_buy.setObjectName("cb_leg1_sell_buy")
        self.cb_leg1_sell_buy.addItem("")
        self.cb_leg1_sell_buy.addItem("")
        self.gridLayout.addWidget(self.cb_leg1_sell_buy, 1, 0, 1, 1)
        self.label_leg3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_leg3.setObjectName("label_leg3")
        self.gridLayout.addWidget(self.label_leg3, 0, 2, 1, 1)
        self.cb_leg1_put_call = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_leg1_put_call.setObjectName("cb_leg1_put_call")
        self.cb_leg1_put_call.addItem("")
        self.cb_leg1_put_call.addItem("")
        self.gridLayout.addWidget(self.cb_leg1_put_call, 2, 0, 1, 1)
        self.cb_leg2_sell_buy = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_leg2_sell_buy.setObjectName("cb_leg2_sell_buy")
        self.cb_leg2_sell_buy.addItem("")
        self.cb_leg2_sell_buy.addItem("")
        self.gridLayout.addWidget(self.cb_leg2_sell_buy, 1, 1, 1, 1)
        self.cb_leg3_sell_buy = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_leg3_sell_buy.setObjectName("cb_leg3_sell_buy")
        self.cb_leg3_sell_buy.addItem("")
        self.cb_leg3_sell_buy.addItem("")
        self.gridLayout.addWidget(self.cb_leg3_sell_buy, 1, 2, 1, 1)
        self.cb_leg4_sell_buy = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_leg4_sell_buy.setObjectName("cb_leg4_sell_buy")
        self.cb_leg4_sell_buy.addItem("")
        self.cb_leg4_sell_buy.addItem("")
        self.gridLayout.addWidget(self.cb_leg4_sell_buy, 1, 3, 1, 1)
        self.cb_leg2_put_call = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_leg2_put_call.setObjectName("cb_leg2_put_call")
        self.cb_leg2_put_call.addItem("")
        self.cb_leg2_put_call.addItem("")
        self.gridLayout.addWidget(self.cb_leg2_put_call, 2, 1, 1, 1)
        self.cb_leg3_put_call = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_leg3_put_call.setObjectName("cb_leg3_put_call")
        self.cb_leg3_put_call.addItem("")
        self.cb_leg3_put_call.addItem("")
        self.gridLayout.addWidget(self.cb_leg3_put_call, 2, 2, 1, 1)
        self.cb_leg4_put_call = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_leg4_put_call.setObjectName("cb_leg4_put_call")
        self.cb_leg4_put_call.addItem("")
        self.cb_leg4_put_call.addItem("")
        self.gridLayout.addWidget(self.cb_leg4_put_call, 2, 3, 1, 1)
        self.line = QtWidgets.QFrame(self.gb_strategy)
        self.line.setGeometry(QtCore.QRect(70, 110, 21, 31))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(4)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.gb_strategy)
        self.line_2.setGeometry(QtCore.QRect(170, 110, 21, 31))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(4)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.gb_strategy)
        self.line_3.setGeometry(QtCore.QRect(320, 110, 21, 31))
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(4)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.gb_strategy)
        self.line_4.setGeometry(QtCore.QRect(475, 110, 21, 31))
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setLineWidth(4)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.gb_strategy)
        self.line_5.setGeometry(QtCore.QRect(10, 110, 21, 31))
        self.line_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_5.setLineWidth(4)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.gb_strategy)
        self.line_6.setGeometry(QtCore.QRect(20, 123, 60, 3))
        self.line_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_6.setLineWidth(4)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self.gb_strategy)
        self.line_7.setGeometry(QtCore.QRect(424, 123, 60, 3))
        self.line_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_7.setLineWidth(4)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self.gb_strategy)
        self.line_8.setGeometry(QtCore.QRect(415, 110, 21, 31))
        self.line_8.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_8.setLineWidth(4)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setObjectName("line_8")
        self.spin_leg1_2 = QtWidgets.QSpinBox(self.gb_strategy)
        self.spin_leg1_2.setGeometry(QtCore.QRect(110, 115, 42, 22))
        self.spin_leg1_2.setProperty("value", 10)
        self.spin_leg1_2.setObjectName("spin_leg1_2")
        self.spin_leg2_3 = QtWidgets.QSpinBox(self.gb_strategy)
        self.spin_leg2_3.setGeometry(QtCore.QRect(235, 115, 42, 22))
        self.spin_leg2_3.setProperty("value", 20)
        self.spin_leg2_3.setObjectName("spin_leg2_3")
        self.spin_leg3_4 = QtWidgets.QSpinBox(self.gb_strategy)
        self.spin_leg3_4.setGeometry(QtCore.QRect(360, 115, 42, 22))
        self.spin_leg3_4.setProperty("value", 10)
        self.spin_leg3_4.setObjectName("spin_leg3_4")
        self.label_strike_price_diff = QtWidgets.QLabel(self.gb_strategy)
        self.label_strike_price_diff.setGeometry(QtCore.QRect(20, 150, 461, 16))
        self.label_strike_price_diff.setObjectName("label_strike_price_diff")
        self.gb_output = QtWidgets.QGroupBox(Form)
        self.gb_output.setGeometry(QtCore.QRect(20, 540, 241, 101))
        self.gb_output.setObjectName("gb_output")
        self.load_path_label = QtWidgets.QLabel(self.gb_output)
        self.load_path_label.setGeometry(QtCore.QRect(10, 50, 240, 40))
        self.load_path_label.setObjectName("load_path_label")
        self.load_path_label.setWordWrap(True)
        self.pb_load = QtWidgets.QPushButton(self.gb_output)
        self.pb_load.setGeometry(QtCore.QRect(10, 20, 93, 28))
        self.pb_load.setObjectName("pb_load")
        self.gb_start = QtWidgets.QGroupBox(Form)
        self.gb_start.setGeometry(QtCore.QRect(280, 540, 261, 101))
        self.gb_start.setObjectName("gb_start")
        self.label_data = QtWidgets.QLabel(self.gb_start)
        self.label_data.setGeometry(QtCore.QRect(20, 30, 161, 16))
        self.label_data.setObjectName("label_data")
        self.spin_ever_min = QtWidgets.QSpinBox(self.gb_start)
        self.spin_ever_min.setGeometry(QtCore.QRect(190, 28, 42, 22))
        self.spin_ever_min.setProperty("value", 15)
        self.spin_ever_min.setObjectName("spin_ever_min")
        self.label_min = QtWidgets.QLabel(self.gb_start)
        self.label_min.setGeometry(QtCore.QRect(235, 30, 55, 16))
        self.label_min.setObjectName("label_min")
        self.pb_start = QtWidgets.QPushButton(self.gb_start)
        self.pb_start.setGeometry(QtCore.QRect(160, 60, 93, 28))
        self.pb_start.setObjectName("pb_start")
        self.label_start_info = QtWidgets.QLabel(self.gb_start)
        self.label_start_info.setGeometry(QtCore.QRect(20, 50, 131, 31))
        self.label_start_info.setObjectName("label_start_info")
        self.label_start_info2 = QtWidgets.QLabel(self.gb_start)
        self.label_start_info2.setGeometry(QtCore.QRect(20, 80, 55, 16))
        self.label_start_info2.setObjectName("label_start_info2")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(370, 0, 171, 41))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(370, 30, 81, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(460, 30, 61, 16))
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Form)
        self.list_exp.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.get_stock_pb.clicked.connect(self.on_click_get_stock)
        self.exp_add_pb.clicked.connect(self.on_click_add_item)
        self.exp_remove_pb.clicked.connect(self.on_click_remove_item)
        self.pb_load.clicked.connect(self.set_path_label)
        self.pb_start.clicked.connect(self.on_click_start)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Iron Condor Tracker"))
        self.get_stock_pb.setText(_translate("Form", "Get stock"))
        self.stock_label.setText("No Stock Selected")

        self.exp_add_pb.setText(_translate("Form", "Add date ->"))
        self.exp_remove_pb.setText(_translate("Form", "<- Remove date"))

        self.gb_stocks.setTitle(_translate("Form", "Select the underlying  "
                                                   "stock"))
        self.gb_exp_dates.setTitle(_translate("Form",  "Select the "
                                    "Expiration dates you want to track :"))
        self.gb_strategy.setTitle(_translate("Form", "Strategy:"))
        self.label_leg2.setText(_translate("Form", "Leg 2:"))
        self.label_leg1.setText(_translate("Form", "Leg 1:"))
        self.label_leg4.setText(_translate("Form", "Leg 4:"))
        self.cb_leg1_sell_buy.setItemText(0, _translate("Form", "Sell"))
        self.cb_leg1_sell_buy.setItemText(1, _translate("Form", "Buy"))
        self.label_leg3.setText(_translate("Form", "Leg 3"))
        self.cb_leg1_put_call.setItemText(0, _translate("Form", "Put"))
        self.cb_leg1_put_call.setItemText(1, _translate("Form", "Call"))
        self.cb_leg2_sell_buy.setItemText(0, _translate("Form", "Sell"))
        self.cb_leg2_sell_buy.setItemText(1, _translate("Form", "Buy"))
        self.cb_leg3_sell_buy.setItemText(0, _translate("Form", "Sell"))
        self.cb_leg3_sell_buy.setItemText(1, _translate("Form", "Buy"))
        self.cb_leg4_sell_buy.setItemText(0, _translate("Form", "Sell"))
        self.cb_leg4_sell_buy.setItemText(1, _translate("Form", "Buy"))
        self.cb_leg2_put_call.setItemText(0, _translate("Form", "Put"))
        self.cb_leg2_put_call.setItemText(1, _translate("Form", "Call"))
        self.cb_leg3_put_call.setItemText(0, _translate("Form", "Put"))
        self.cb_leg3_put_call.setItemText(1, _translate("Form", "Call"))
        self.cb_leg4_put_call.setItemText(0, _translate("Form", "Put"))
        self.cb_leg4_put_call.setItemText(1, _translate("Form", "Call"))
        self.label_strike_price_diff.setText(_translate("Form",
                    "Strike Price Difference between each leg"))

        self.gb_output.setTitle(_translate("Form", "Output File selection :"))
        self.pb_load.setText(_translate("Form", "Load"))
        self.load_path_label.setText(_translate("Form", "No Path selected"))
        self.gb_start.setTitle(_translate("Form", "Start Data Collection"))
        self.label_data.setText(_translate("Form",  "Data will be collected "
                                                    "every"))

        self.label_min.setText(_translate("Form", "min"))
        self.pb_start.setText(_translate("Form", "Start"))
        self.label_start_info.setText(_translate("Form", "You can start  "
                                                         "multiple"))

        self.label_start_info2.setText(_translate("Form", "trackers."))
        self.label_6.setText(_translate("Form", "Iron Condor price tracker."))
        self.label_7.setText(_translate("Form", "By: Peter AK "))
        self.label_8.setText(_translate("Form", "V0.4"))

    def on_click_get_stock(self):
        """Get the stock value and fill the exipration dates """
        stock_value = self.stock_line.text()
        self.stock_string.setText(stock_value)
        try:
            label_value = get_live_price(stock_value)
            exp_date_list = get_expiration_dates(stock_value)
            self.stock_label.setText(str(np.around(label_value, decimals=2)))
            self.list_exp.addItems(exp_date_list)

        except requests.ConnectionError:
            self.stock_label.setText("Connection Error")
        except AssertionError:
            self.stock_label.setText("Stock could not be found")

    def on_click_add_item(self):
        """Add one selected item to the selected expiration list"""
        selected_index = [x.row() for x in self.list_exp.selectedIndexes()]
        selected_index = selected_index[0]
        self.list_exp_select.addItem(self.list_exp.takeItem(selected_index))

    def on_click_remove_item(self):
        """Remove one selected item from the selected expiration list"""
        selected_index = [x.row() for x in
                          self.list_exp_select.selectedIndexes()]
        selected_index = selected_index[0]
        self.list_exp.addItem(self.list_exp_select.takeItem(selected_index))

    def set_path_label(self):
        """Lets the user select the output files (as an excel file only (
        xlsx) and then sets this path to the label"""
        qfd = QFileDialog()
        fileName = QFileDialog().getOpenFileName(qfd, "Select a file", '',
                                                 "xlsx(*.xlsx)")
        filePath = str(fileName[0])
        self.load_path_label.setText(filePath)

    def on_click_start(self):
        """Loads all the necessary parameters into the main backend function"""
        stock = self.stock_string.text()
        exp_date_list = [self.list_exp_select.item(i).text() for i in
                         range(self.list_exp_select.count())]
        leg1 = [self.cb_leg1_put_call.currentText(),
               self.cb_leg1_sell_buy.currentText()]
        leg2 = [self.cb_leg2_put_call.currentText(),
                self.cb_leg2_sell_buy.currentText()]
        leg3 = [self.cb_leg3_put_call.currentText(),
                self.cb_leg3_sell_buy.currentText()]
        leg4 = [self.cb_leg4_put_call.currentText(),
                self.cb_leg4_sell_buy.currentText()]
        leg1_2_strat = self.spin_leg1_2.value()
        leg2_3_strat = self.spin_leg2_3.value()
        leg3_4_strat = self.spin_leg3_4.value()
        file_path = self.load_path_label.text()
        print(stock)
        print(exp_date_list)
        print(leg1, leg2, leg3, leg4)
        print(leg1_2_strat, leg2_3_strat, leg3_4_strat)
        print(file_path)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
