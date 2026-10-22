# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CompressSettingsQKGIUd.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(469, 304)
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

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(140, 0))
        self.label_3.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(140, 0))
        self.label_4.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout.addWidget(self.label_4)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(140, 0))
        self.label_8.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout.addWidget(self.label_8)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(20, 20))
        self.label_5.setMaximumSize(QSize(20, 20))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_5)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(20, 20))
        self.label_6.setMaximumSize(QSize(20, 20))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_6)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(20, 20))
        self.label_7.setMaximumSize(QSize(20, 20))
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_7)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.megaPixel = QComboBox(self.centralwidget)
        self.megaPixel.addItem("")
        self.megaPixel.addItem("")
        self.megaPixel.addItem("")
        self.megaPixel.addItem("")
        self.megaPixel.addItem("")
        self.megaPixel.addItem("")
        self.megaPixel.setObjectName(u"megaPixel")

        self.verticalLayout_3.addWidget(self.megaPixel)

        self.photoQuality = QSpinBox(self.centralwidget)
        self.photoQuality.setObjectName(u"photoQuality")
        self.photoQuality.setMinimum(1)
        self.photoQuality.setMaximum(100)
        self.photoQuality.setValue(85)

        self.verticalLayout_3.addWidget(self.photoQuality)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveLocation = QLineEdit(self.centralwidget)
        self.saveLocation.setObjectName(u"saveLocation")

        self.horizontalLayout.addWidget(self.saveLocation)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_4.addWidget(self.pushButton)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Pengaturan Kompresi", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Ubah opsi kompresi file foto Anda. Sebagai referensi, Google Foto menetapkan kompresi 12Mp bagi gambar yang Anda unggah untuk menghemat penyimpanan. Anda direkomendasikan untuk memilih pengaturan dengan tingkat Megapiksel <span style=\" font-weight:700;\">12Mp</span> dan kualitas gambar <span style=\" font-weight:700;\">85%</span> agar kualitas gambar yang dikompresi tidak menurun secara drastis.</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Resolusi (Megapiksel)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Kualitas Dipertahankan", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Lokasi Simpan", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.megaPixel.setItemText(0, QCoreApplication.translate("MainWindow", u"20Mp", None))
        self.megaPixel.setItemText(1, QCoreApplication.translate("MainWindow", u"18Mp", None))
        self.megaPixel.setItemText(2, QCoreApplication.translate("MainWindow", u"16Mp", None))
        self.megaPixel.setItemText(3, QCoreApplication.translate("MainWindow", u"14Mp", None))
        self.megaPixel.setItemText(4, QCoreApplication.translate("MainWindow", u"12Mp", None))
        self.megaPixel.setItemText(5, QCoreApplication.translate("MainWindow", u"10Mp", None))

        self.photoQuality.setSuffix(QCoreApplication.translate("MainWindow", u"%", None))
        self.saveLocation.setInputMask("")
        self.saveLocation.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Mendukung Drag and Drop", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Pilih Folder", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Gunakan Pengaturan yang Direkomendasikan", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Batal", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Simpan dan Tutup", None))
    # retranslateUi

