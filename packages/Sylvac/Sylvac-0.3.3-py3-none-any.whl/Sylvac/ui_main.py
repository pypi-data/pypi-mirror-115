# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainLfBomj.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import Sylvac.icons_rc

class Ui_MainDis(object):
    def setupUi(self, MainDis):
        if not MainDis.objectName():
            MainDis.setObjectName(u"MainDis")
        MainDis.resize(449, 244)
        MainDis.setStyleSheet(u"font: 12pt \"Tahoma\";\n"
"border-color: rgb(85, 255, 0);\n"
"\n"
"background-color: rgb(9,5,13);\n"
"color: rgb(255,255,255);")
        self.centralwidget = QWidget(MainDis)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"\n"
"QToolBox{\n"
"	\n"
"	background-color: rgb(24,24,36);\n"
"	text-align: left;\n"
"\n"
"}\n"
"\n"
"QToolBox::tab{\n"
"	\n"
"	border-radius: 5px;\n"
"	background-color: rgb(17,16,26);\n"
"	text-align: left;\n"
"\n"
"}\n"
"")
        self.FrameMain = QFrame(self.centralwidget)
        self.FrameMain.setObjectName(u"FrameMain")
        self.FrameMain.setGeometry(QRect(1, 3, 451, 241))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FrameMain.sizePolicy().hasHeightForWidth())
        self.FrameMain.setSizePolicy(sizePolicy)
        self.FrameMain.setFrameShape(QFrame.Box)
        self.FrameMain.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.FrameMain)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.FrameMain)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 16))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lbTime = QLabel(self.frame)
        self.lbTime.setObjectName(u"lbTime")

        self.verticalLayout_5.addWidget(self.lbTime, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.verticalLayout_9.addWidget(self.frame, 0, Qt.AlignTop)

        self.fr_Measure = QFrame(self.FrameMain)
        self.fr_Measure.setObjectName(u"fr_Measure")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fr_Measure.sizePolicy().hasHeightForWidth())
        self.fr_Measure.setSizePolicy(sizePolicy1)
        self.fr_Measure.setMinimumSize(QSize(0, 0))
        self.fr_Measure.setMaximumSize(QSize(16777215, 16777215))
        self.fr_Measure.setFrameShape(QFrame.StyledPanel)
        self.fr_Measure.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.fr_Measure)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_9.addWidget(self.fr_Measure, 0, Qt.AlignTop)

        self.stackedWidget = QStackedWidget(self.FrameMain)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.stackedWidget.setFrameShadow(QFrame.Raised)
        self.Page_misure = QWidget()
        self.Page_misure.setObjectName(u"Page_misure")
        self.verticalLayout = QVBoxLayout(self.Page_misure)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.Page_misure)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_3)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.Thuoc1 = QFrame(self.frame_3)
        self.Thuoc1.setObjectName(u"Thuoc1")
        self.Thuoc1.setFrameShape(QFrame.StyledPanel)
        self.Thuoc1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.Thuoc1)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(self.Thuoc1)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.lbuplimit1 = QLabel(self.Thuoc1)
        self.lbuplimit1.setObjectName(u"lbuplimit1")

        self.horizontalLayout.addWidget(self.lbuplimit1)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.lbvalue = QLabel(self.Thuoc1)
        self.lbvalue.setObjectName(u"lbvalue")
        font = QFont()
        font.setFamily(u"Tahoma")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbvalue.setFont(font)
        self.lbvalue.setStyleSheet(u"color: rgb(115, 185, 255); \n"
"padding: 0px;\n"
"background-color: none;\n"
"border: 3px solid rgb(230,5,64);\n"
"border-radius: 10px;")
        self.lbvalue.setAlignment(Qt.AlignCenter)
        self.lbvalue.setIndent(-1)

        self.verticalLayout_4.addWidget(self.lbvalue)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetMinimumSize)
        self.lbDlimit1 = QLabel(self.Thuoc1)
        self.lbDlimit1.setObjectName(u"lbDlimit1")

        self.horizontalLayout_7.addWidget(self.lbDlimit1)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btnKetNoi = QPushButton(self.Thuoc1)
        self.btnKetNoi.setObjectName(u"btnKetNoi")
        self.btnKetNoi.setMinimumSize(QSize(0, 32))
        self.btnKetNoi.setMaximumSize(QSize(16777215, 32))
        self.btnKetNoi.setStyleSheet(u"border: 1px solid rgb(230,5,64);\n"
"border-radius: 5px;")
        icon = QIcon()
        icon.addFile(u":/icons/check-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnKetNoi.setIcon(icon)
        self.btnKetNoi.setIconSize(QSize(16, 22))

        self.horizontalLayout_3.addWidget(self.btnKetNoi)

        self.btnThoat = QPushButton(self.Thuoc1)
        self.btnThoat.setObjectName(u"btnThoat")
        self.btnThoat.setMinimumSize(QSize(32, 32))
        self.btnThoat.setStyleSheet(u"border: 1px solid rgb(230,5,64);\n"
"border-radius: 5px;")
        icon1 = QIcon()
        icon1.addFile(u":/icons/wifi-off.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnThoat.setIcon(icon1)
        self.btnThoat.setIconSize(QSize(16, 22))

        self.horizontalLayout_3.addWidget(self.btnThoat)

        self.cb1 = QComboBox(self.Thuoc1)
        self.cb1.setObjectName(u"cb1")
        self.cb1.setMinimumSize(QSize(0, 32))
        font1 = QFont()
        font1.setFamily(u"Tahoma")
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setWeight(50)
        font1.setKerning(False)
        self.cb1.setFont(font1)
        self.cb1.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.cb1)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)


        self.verticalLayout_8.addWidget(self.Thuoc1)


        self.horizontalLayout_10.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_4)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.Thuoc2 = QFrame(self.frame_4)
        self.Thuoc2.setObjectName(u"Thuoc2")
        self.Thuoc2.setStyleSheet(u"background-color: rgb(9,5,13);\n"
"color: rgb(255, 255, 255);")
        self.Thuoc2.setFrameShape(QFrame.StyledPanel)
        self.Thuoc2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.Thuoc2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.label_7 = QLabel(self.Thuoc2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_6.addWidget(self.label_7)

        self.lbuplimit2 = QLabel(self.Thuoc2)
        self.lbuplimit2.setObjectName(u"lbuplimit2")

        self.horizontalLayout_6.addWidget(self.lbuplimit2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.lbvalue_2 = QLabel(self.Thuoc2)
        self.lbvalue_2.setObjectName(u"lbvalue_2")
        self.lbvalue_2.setFont(font)
        self.lbvalue_2.setStyleSheet(u"color: rgb(115, 185, 255); \n"
"padding: 0px;\n"
"background-color: none;\n"
"border: 3px solid rgb(230,5,64);\n"
"border-radius: 10px;")
        self.lbvalue_2.setAlignment(Qt.AlignCenter)
        self.lbvalue_2.setIndent(-1)

        self.verticalLayout_3.addWidget(self.lbvalue_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.lbDlimit2 = QLabel(self.Thuoc2)
        self.lbDlimit2.setObjectName(u"lbDlimit2")

        self.horizontalLayout_8.addWidget(self.lbDlimit2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btnKetNoi_2 = QPushButton(self.Thuoc2)
        self.btnKetNoi_2.setObjectName(u"btnKetNoi_2")
        self.btnKetNoi_2.setMinimumSize(QSize(0, 32))
        self.btnKetNoi_2.setStyleSheet(u"border: 1px solid rgb(230,5,64);\n"
"border-radius: 5px;")
        self.btnKetNoi_2.setIcon(icon)
        self.btnKetNoi_2.setIconSize(QSize(16, 22))

        self.horizontalLayout_4.addWidget(self.btnKetNoi_2)

        self.btnThoat_2 = QPushButton(self.Thuoc2)
        self.btnThoat_2.setObjectName(u"btnThoat_2")
        self.btnThoat_2.setMinimumSize(QSize(0, 32))
        self.btnThoat_2.setStyleSheet(u"border: 1px solid rgb(230,5,64);\n"
"border-radius: 5px;")
        self.btnThoat_2.setIcon(icon1)
        self.btnThoat_2.setIconSize(QSize(16, 22))

        self.horizontalLayout_4.addWidget(self.btnThoat_2)

        self.cb2 = QComboBox(self.Thuoc2)
        self.cb2.setObjectName(u"cb2")
        self.cb2.setMinimumSize(QSize(0, 32))
        self.cb2.setFont(font1)
        self.cb2.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.cb2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_7.addLayout(self.verticalLayout_3)


        self.verticalLayout_10.addWidget(self.Thuoc2)


        self.horizontalLayout_10.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.frame_2)

        self.stackedWidget.addWidget(self.Page_misure)
        self.Page_chart = QWidget()
        self.Page_chart.setObjectName(u"Page_chart")
        sizePolicy1.setHeightForWidth(self.Page_chart.sizePolicy().hasHeightForWidth())
        self.Page_chart.setSizePolicy(sizePolicy1)
        self.verticalLayout_13 = QVBoxLayout(self.Page_chart)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.LayoutChart = QVBoxLayout()
        self.LayoutChart.setSpacing(0)
        self.LayoutChart.setObjectName(u"LayoutChart")
        self.LayoutChart.setSizeConstraint(QLayout.SetMaximumSize)

        self.verticalLayout_13.addLayout(self.LayoutChart)

        self.stackedWidget.addWidget(self.Page_chart)

        self.verticalLayout_9.addWidget(self.stackedWidget)

        self.Fr_button = QFrame(self.FrameMain)
        self.Fr_button.setObjectName(u"Fr_button")
        self.Fr_button.setFrameShape(QFrame.StyledPanel)
        self.Fr_button.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.Fr_button)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.btnMain = QPushButton(self.Fr_button)
        self.btnMain.setObjectName(u"btnMain")
        self.btnMain.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/smartphone.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnMain.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.btnMain)

        self.btnUpdate = QPushButton(self.Fr_button)
        self.btnUpdate.setObjectName(u"btnUpdate")
        icon3 = QIcon()
        icon3.addFile(u":/icons/chrome.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnUpdate.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.btnUpdate)

        self.btnChart = QPushButton(self.Fr_button)
        self.btnChart.setObjectName(u"btnChart")
        icon4 = QIcon()
        icon4.addFile(u":/icons/activity.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnChart.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.btnChart)

        self.btnExit = QPushButton(self.Fr_button)
        self.btnExit.setObjectName(u"btnExit")
        icon5 = QIcon()
        icon5.addFile(u":/icons/power.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnExit.setIcon(icon5)

        self.horizontalLayout_2.addWidget(self.btnExit)

        self.lbsoluong = QLabel(self.Fr_button)
        self.lbsoluong.setObjectName(u"lbsoluong")
        self.lbsoluong.setMinimumSize(QSize(90, 25))
        self.lbsoluong.setMaximumSize(QSize(90, 25))
        self.lbsoluong.setSizeIncrement(QSize(90, 25))
        self.lbsoluong.setStyleSheet(u"color:rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.lbsoluong)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_9.addWidget(self.Fr_button, 0, Qt.AlignBottom)

        MainDis.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainDis)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainDis)
    # setupUi

    def retranslateUi(self, MainDis):
        MainDis.setWindowTitle(QCoreApplication.translate("MainDis", u"MainWindow", None))
        self.lbTime.setText(QCoreApplication.translate("MainDis", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("MainDis", u"Device 1", None))
        self.lbuplimit1.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#55ff00;\">+0.000</span></p></body></html>", None))
        self.lbvalue.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#55ff00;\">00.000</span></p></body></html>", None))
        self.lbDlimit1.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffaa7f;\">-0.000</span></p></body></html>", None))
        self.btnKetNoi.setText("")
        self.btnThoat.setText("")
        self.cb1.setCurrentText("")
        self.label_7.setText(QCoreApplication.translate("MainDis", u"Device 2", None))
        self.lbuplimit2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#55ff00;\">+0.000</span></p></body></html>", None))
        self.lbvalue_2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#55ff00;\">00.000</span></p></body></html>", None))
        self.lbDlimit2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffaa7f;\">-0.000</span></p></body></html>", None))
        self.btnKetNoi_2.setText("")
        self.btnThoat_2.setText("")
        self.cb2.setCurrentText("")
        self.btnMain.setText(QCoreApplication.translate("MainDis", u"Main", None))
        self.btnUpdate.setText(QCoreApplication.translate("MainDis", u"Update", None))
        self.btnChart.setText(QCoreApplication.translate("MainDis", u"Chart", None))
        self.btnExit.setText(QCoreApplication.translate("MainDis", u"Exit", None))
        self.lbsoluong.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" color:#0000ff;\">...</span></p></body></html>", None))
    # retranslateUi

