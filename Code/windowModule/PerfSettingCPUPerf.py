# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PerfSettingCPUPerffjIAIf.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(350, 200)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.cpuCoreSlider = QSlider(self.centralwidget)
        self.cpuCoreSlider.setObjectName(u"cpuCoreSlider")
        self.cpuCoreSlider.setMinimum(1)
        self.cpuCoreSlider.setMaximum(8)
        self.cpuCoreSlider.setPageStep(1)
        self.cpuCoreSlider.setValue(1)
        self.cpuCoreSlider.setSliderPosition(1)
        self.cpuCoreSlider.setOrientation(Qt.Orientation.Horizontal)
        self.cpuCoreSlider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.verticalLayout.addWidget(self.cpuCoreSlider)

        self.settingsSuggestion = QLabel(self.centralwidget)
        self.settingsSuggestion.setObjectName(u"settingsSuggestion")
        font1 = QFont()
        font1.setFamilies([u"Yu Gothic Light"])
        self.settingsSuggestion.setFont(font1)
        self.settingsSuggestion.setWordWrap(True)

        self.verticalLayout.addWidget(self.settingsSuggestion)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

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


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Performa CPU", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Lebih banyak core yang digunakan akan mempercepat proses kompresi foto, dan sebaliknya. <span style=\" font-weight:700;\">Harap ubah pengaturan ini dengan hati-hati.</span></p></body></html>", None))
        self.settingsSuggestion.setText(QCoreApplication.translate("MainWindow", u"Summary:", None))
        self.batal.setText(QCoreApplication.translate("MainWindow", u"Batal", None))
        self.simpan.setText(QCoreApplication.translate("MainWindow", u"Simpan dan Tutup", None))
    # retranslateUi

