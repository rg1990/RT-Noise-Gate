# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drum_noise_gate_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1223, 747)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(760, 350, 100, 16))
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(870, 220, 102, 148))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.release_dial_layout = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.release_dial_layout.setContentsMargins(0, 0, 0, 0)
        self.release_dial_layout.setObjectName("release_dial_layout")
        self.release_dial = QtWidgets.QDial(self.layoutWidget_2)
        self.release_dial.setMaximum(1000)
        self.release_dial.setNotchTarget(100.0)
        self.release_dial.setNotchesVisible(True)
        self.release_dial.setObjectName("release_dial")
        self.release_dial_layout.addWidget(self.release_dial)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.release_dial_layout.addLayout(self.horizontalLayout_3)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.release_dial_layout.addWidget(self.label_9)
        self.threshold_slider = QtWidgets.QSlider(self.centralwidget)
        self.threshold_slider.setGeometry(QtCore.QRect(790, 40, 41, 291))
        self.threshold_slider.setMinimum(-60)
        self.threshold_slider.setMaximum(0)
        self.threshold_slider.setPageStep(0)
        self.threshold_slider.setProperty("value", -20)
        self.threshold_slider.setOrientation(QtCore.Qt.Vertical)
        self.threshold_slider.setObjectName("threshold_slider")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 751, 361))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.scrolling_plot_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.scrolling_plot_layout.setContentsMargins(0, 0, 0, 0)
        self.scrolling_plot_layout.setObjectName("scrolling_plot_layout")
        self.layoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(1020, 220, 102, 148))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.lookahead_dial_layout = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.lookahead_dial_layout.setContentsMargins(0, 0, 0, 0)
        self.lookahead_dial_layout.setObjectName("lookahead_dial_layout")
        self.lookahead_dial = QtWidgets.QDial(self.layoutWidget_3)
        self.lookahead_dial.setMaximum(10)
        self.lookahead_dial.setNotchTarget(10.0)
        self.lookahead_dial.setNotchesVisible(True)
        self.lookahead_dial.setObjectName("lookahead_dial")
        self.lookahead_dial_layout.addWidget(self.lookahead_dial)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.lookahead_dial_layout.addLayout(self.horizontalLayout_4)
        self.label_12 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.lookahead_dial_layout.addWidget(self.label_12)
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1020, 40, 102, 148))
        self.layoutWidget.setObjectName("layoutWidget")
        self.hold_dial_layout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.hold_dial_layout.setContentsMargins(0, 0, 0, 0)
        self.hold_dial_layout.setObjectName("hold_dial_layout")
        self.hold_dial = QtWidgets.QDial(self.layoutWidget)
        self.hold_dial.setMaximum(250)
        self.hold_dial.setNotchTarget(25.0)
        self.hold_dial.setNotchesVisible(True)
        self.hold_dial.setObjectName("hold_dial")
        self.hold_dial_layout.addWidget(self.hold_dial)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.hold_dial_layout.addLayout(self.horizontalLayout_2)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.hold_dial_layout.addWidget(self.label_6)
        self.layoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_4.setGeometry(QtCore.QRect(870, 41, 107, 148))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.attack_dial_layout = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.attack_dial_layout.setContentsMargins(0, 0, 0, 0)
        self.attack_dial_layout.setObjectName("attack_dial_layout")
        self.attack_dial = QtWidgets.QDial(self.layoutWidget_4)
        self.attack_dial.setMaximum(200)
        self.attack_dial.setNotchTarget(20.0)
        self.attack_dial.setNotchesVisible(True)
        self.attack_dial.setObjectName("attack_dial")
        self.attack_dial_layout.addWidget(self.attack_dial)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget_4)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_4)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.attack_dial_layout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.layoutWidget_4)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.attack_dial_layout.addWidget(self.label)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 390, 1151, 261))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.waveform_nav_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.waveform_nav_layout.setContentsMargins(0, 0, 0, 0)
        self.waveform_nav_layout.setObjectName("waveform_nav_layout")
        self.on_off_button = QtWidgets.QPushButton(self.centralwidget)
        self.on_off_button.setGeometry(QtCore.QRect(1150, 40, 31, 31))
        self.on_off_button.setStyleSheet("")
        self.on_off_button.setCheckable(False)
        self.on_off_button.setChecked(False)
        self.on_off_button.setObjectName("on_off_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Drum Gate v0.1"))
        self.label_13.setText(_translate("MainWindow", "Threshold (dB)"))
        self.label_7.setText(_translate("MainWindow", "0 ms"))
        self.label_8.setText(_translate("MainWindow", "1000 s"))
        self.label_9.setText(_translate("MainWindow", "Release"))
        self.label_10.setText(_translate("MainWindow", "0 ms"))
        self.label_11.setText(_translate("MainWindow", "10ms"))
        self.label_12.setText(_translate("MainWindow", "Lookahead"))
        self.label_4.setText(_translate("MainWindow", "0 ms"))
        self.label_5.setText(_translate("MainWindow", "250ms"))
        self.label_6.setText(_translate("MainWindow", "Hold"))
        self.label_2.setText(_translate("MainWindow", "0 ms"))
        self.label_3.setText(_translate("MainWindow", "200 ms"))
        self.label.setText(_translate("MainWindow", "Attack"))
        self.on_off_button.setText(_translate("MainWindow", "ON"))
