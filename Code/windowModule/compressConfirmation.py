# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'compressConfirmationGdnOSr.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTableView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(442, 517)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_10 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_10.addWidget(self.label)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setWordWrap(True)

        self.verticalLayout_10.addWidget(self.label_13)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_10.addWidget(self.line)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(140, 0))
        self.label_14.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_6.addWidget(self.label_14)

        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(140, 0))
        self.label_15.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_6.addWidget(self.label_15)

        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(140, 0))
        self.label_16.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_6.addWidget(self.label_16)

        self.label_20 = QLabel(self.groupBox_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(140, 0))
        self.label_20.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_6.addWidget(self.label_20)


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(20, 20))
        self.label_17.setMaximumSize(QSize(20, 20))
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_17)

        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(20, 20))
        self.label_19.setMaximumSize(QSize(20, 20))
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_19)

        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(20, 20))
        self.label_18.setMaximumSize(QSize(20, 20))
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_18)

        self.label_21 = QLabel(self.groupBox_2)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(20, 20))
        self.label_21.setMaximumSize(QSize(20, 20))
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_21)


        self.horizontalLayout_3.addLayout(self.verticalLayout_7)


        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_8)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.readyCompress = QLineEdit(self.groupBox_2)
        self.readyCompress.setObjectName(u"readyCompress")

        self.verticalLayout_5.addWidget(self.readyCompress)

        self.cancelledPhoto = QLineEdit(self.groupBox_2)
        self.cancelledPhoto.setObjectName(u"cancelledPhoto")

        self.verticalLayout_5.addWidget(self.cancelledPhoto)

        self.rejectedPhoto = QLineEdit(self.groupBox_2)
        self.rejectedPhoto.setObjectName(u"rejectedPhoto")

        self.verticalLayout_5.addWidget(self.rejectedPhoto)

        self.photoCategory = QTableView(self.groupBox_2)
        self.photoCategory.setObjectName(u"photoCategory")

        self.verticalLayout_5.addWidget(self.photoCategory)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)


        self.verticalLayout_9.addLayout(self.horizontalLayout_4)


        self.verticalLayout_10.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(140, 0))
        self.label_3.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(140, 0))
        self.label_4.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout.addWidget(self.label_4)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(140, 0))
        self.label_8.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout.addWidget(self.label_8)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(140, 0))
        self.label_9.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout.addWidget(self.label_9)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(140, 0))
        self.label_11.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout.addWidget(self.label_11)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(20, 20))
        self.label_5.setMaximumSize(QSize(20, 20))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_5)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(20, 20))
        self.label_6.setMaximumSize(QSize(20, 20))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_6)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(20, 20))
        self.label_7.setMaximumSize(QSize(20, 20))
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_7)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(20, 20))
        self.label_10.setMaximumSize(QSize(20, 20))
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_10)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(20, 20))
        self.label_12.setMaximumSize(QSize(20, 20))
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_12)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.megaPixel = QSpinBox(self.groupBox)
        self.megaPixel.setObjectName(u"megaPixel")
        self.megaPixel.setMinimum(1)
        self.megaPixel.setMaximum(200)
        self.megaPixel.setValue(12)

        self.verticalLayout_3.addWidget(self.megaPixel)

        self.photoQuality = QSpinBox(self.groupBox)
        self.photoQuality.setObjectName(u"photoQuality")
        self.photoQuality.setMinimum(1)
        self.photoQuality.setMaximum(100)
        self.photoQuality.setValue(85)

        self.verticalLayout_3.addWidget(self.photoQuality)

        self.saveLocation = QLineEdit(self.groupBox)
        self.saveLocation.setObjectName(u"saveLocation")

        self.verticalLayout_3.addWidget(self.saveLocation)

        self.saveFormat = QComboBox(self.groupBox)
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.addItem("")
        self.saveFormat.setObjectName(u"saveFormat")

        self.verticalLayout_3.addWidget(self.saveFormat)

        self.resamplingAlgorithm = QComboBox(self.groupBox)
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.setObjectName(u"resamplingAlgorithm")

        self.verticalLayout_3.addWidget(self.resamplingAlgorithm)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout_10.addWidget(self.groupBox)

        self.deleteOriginalFile = QCheckBox(self.centralwidget)
        self.deleteOriginalFile.setObjectName(u"deleteOriginalFile")

        self.verticalLayout_10.addWidget(self.deleteOriginalFile)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.changeSettings = QPushButton(self.centralwidget)
        self.changeSettings.setObjectName(u"changeSettings")

        self.horizontalLayout_2.addWidget(self.changeSettings)

        self.continueCompression = QPushButton(self.centralwidget)
        self.continueCompression.setObjectName(u"continueCompression")

        self.horizontalLayout_2.addWidget(self.continueCompression)


        self.verticalLayout_10.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.resamplingAlgorithm.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Rincian Kompresi", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Silahkan menyimak rincian berikut ini sebelum memulai proses kompresi.</p></body></html>", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Foto yang Dikompresi", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Siap Dikompresi", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Dibatalkan", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Ditolak", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Jenis Foto", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"=", None))
#if QT_CONFIG(tooltip)
        self.readyCompress.setToolTip(QCoreApplication.translate("MainWindow", u"Diset secara default. Ubah dengan menekan \"Pilih Folder\" atau drag-n-drop folder ke line edit.", None))
#endif // QT_CONFIG(tooltip)
        self.readyCompress.setInputMask("")
        self.readyCompress.setPlaceholderText("")
#if QT_CONFIG(tooltip)
        self.cancelledPhoto.setToolTip(QCoreApplication.translate("MainWindow", u"Diset secara default. Ubah dengan menekan \"Pilih Folder\" atau drag-n-drop folder ke line edit.", None))
#endif // QT_CONFIG(tooltip)
        self.cancelledPhoto.setInputMask("")
        self.cancelledPhoto.setPlaceholderText("")
#if QT_CONFIG(tooltip)
        self.rejectedPhoto.setToolTip(QCoreApplication.translate("MainWindow", u"Diset secara default. Ubah dengan menekan \"Pilih Folder\" atau drag-n-drop folder ke line edit.", None))
#endif // QT_CONFIG(tooltip)
        self.rejectedPhoto.setInputMask("")
        self.rejectedPhoto.setPlaceholderText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Pengaturan yang Digunakan", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Resolusi (Megapiksel)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Kualitas Dipertahankan", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Lokasi Simpan", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Format Simpan", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Algoritma Resampling", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.megaPixel.setSuffix(QCoreApplication.translate("MainWindow", u"Mp", None))
#if QT_CONFIG(tooltip)
        self.photoQuality.setToolTip(QCoreApplication.translate("MainWindow", u"Semakin kecil kualitas, semakin blur gambar yang dihasilkan", None))
#endif // QT_CONFIG(tooltip)
        self.photoQuality.setSuffix(QCoreApplication.translate("MainWindow", u"%", None))
#if QT_CONFIG(tooltip)
        self.saveLocation.setToolTip(QCoreApplication.translate("MainWindow", u"Diset secara default. Ubah dengan menekan \"Pilih Folder\" atau drag-n-drop folder ke line edit.", None))
#endif // QT_CONFIG(tooltip)
        self.saveLocation.setInputMask("")
        self.saveLocation.setPlaceholderText("")
        self.saveFormat.setItemText(0, QCoreApplication.translate("MainWindow", u"JPEG", None))
        self.saveFormat.setItemText(1, QCoreApplication.translate("MainWindow", u"JPG", None))
        self.saveFormat.setItemText(2, QCoreApplication.translate("MainWindow", u"JPEG2000", None))
        self.saveFormat.setItemText(3, QCoreApplication.translate("MainWindow", u"PNG", None))
        self.saveFormat.setItemText(4, QCoreApplication.translate("MainWindow", u"HEIF", None))
        self.saveFormat.setItemText(5, QCoreApplication.translate("MainWindow", u"HEIC", None))
        self.saveFormat.setItemText(6, QCoreApplication.translate("MainWindow", u"WEBP", None))
        self.saveFormat.setItemText(7, QCoreApplication.translate("MainWindow", u"BMP", None))
        self.saveFormat.setItemText(8, QCoreApplication.translate("MainWindow", u"TIFF", None))
        self.saveFormat.setItemText(9, QCoreApplication.translate("MainWindow", u"ICO", None))
        self.saveFormat.setItemText(10, QCoreApplication.translate("MainWindow", u"AVIF", None))

        self.resamplingAlgorithm.setItemText(0, QCoreApplication.translate("MainWindow", u"NEAREST", None))
        self.resamplingAlgorithm.setItemText(1, QCoreApplication.translate("MainWindow", u"LANCZOS (Direkomendasikan)", None))
        self.resamplingAlgorithm.setItemText(2, QCoreApplication.translate("MainWindow", u"BILINEAR", None))
        self.resamplingAlgorithm.setItemText(3, QCoreApplication.translate("MainWindow", u"BICUBIC", None))
        self.resamplingAlgorithm.setItemText(4, QCoreApplication.translate("MainWindow", u"BOX", None))
        self.resamplingAlgorithm.setItemText(5, QCoreApplication.translate("MainWindow", u"HAMMING", None))
        self.resamplingAlgorithm.setItemText(6, QCoreApplication.translate("MainWindow", u"MKS2013 (Rekomendasi Kedua)", None))
        self.resamplingAlgorithm.setItemText(7, QCoreApplication.translate("MainWindow", u"MKS2021", None))

        self.deleteOriginalFile.setText(QCoreApplication.translate("MainWindow", u"Hapus File Asli", None))
        self.changeSettings.setText(QCoreApplication.translate("MainWindow", u"Ubah Pengaturan", None))
        self.continueCompression.setText(QCoreApplication.translate("MainWindow", u"Semuanya Beres, Lanjutkan!", None))
    # retranslateUi

