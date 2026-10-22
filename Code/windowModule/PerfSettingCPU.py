# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PerfSettingCPUPerfVbOmIz.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(305, 249)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_4.addWidget(self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(130, 16777215))

        self.verticalLayout_3.addWidget(self.label_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(20, 16777215))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_5)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(20, 16777215))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cpuAvailable = QLineEdit(self.centralwidget)
        self.cpuAvailable.setObjectName(u"cpuAvailable")

        self.verticalLayout_2.addWidget(self.cpuAvailable)

        self.userDefiniedCPU = QSpinBox(self.centralwidget)
        self.userDefiniedCPU.setObjectName(u"userDefiniedCPU")

        self.verticalLayout_2.addWidget(self.userDefiniedCPU)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.batal = QPushButton(self.centralwidget)
        self.batal.setObjectName(u"batal")

        self.horizontalLayout.addWidget(self.batal)

        self.simpan = QPushButton(self.centralwidget)
        self.simpan.setObjectName(u"simpan")

        self.horizontalLayout.addWidget(self.simpan)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Performa CPU", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Lebih banyak core yang digunakan akan mempercepat proses kompresi foto, dan sebaliknya. Secara default, sistem menggunakan core CPU sejumlah (maxCore - 2). <span style=\" font-weight:700;\">Harap ubah pengaturan ini dengan hati-hati.</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"CPU Sistem Tersedia", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"CPU Yang Digunakan", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.userDefiniedCPU.setSuffix(QCoreApplication.translate("MainWindow", u" CPU", None))
        self.userDefiniedCPU.setPrefix("")
        self.batal.setText(QCoreApplication.translate("MainWindow", u"Batal", None))
        self.simpan.setText(QCoreApplication.translate("MainWindow", u"Simpan dan Tutup", None))
    # retranslateUi

