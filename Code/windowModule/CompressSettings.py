# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CompressSettingsERpDde.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(487, 492)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_6.addWidget(self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.label_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
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


        self.horizontalLayout_3.addLayout(self.verticalLayout)

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


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

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

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveLocation = QLineEdit(self.groupBox)
        self.saveLocation.setObjectName(u"saveLocation")

        self.horizontalLayout.addWidget(self.saveLocation)

        self.chooseDir = QPushButton(self.groupBox)
        self.chooseDir.setObjectName(u"chooseDir")

        self.horizontalLayout.addWidget(self.chooseDir)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

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


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.resamplingAlgorithm = QComboBox(self.groupBox_2)
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.addItem("")
        self.resamplingAlgorithm.setObjectName(u"resamplingAlgorithm")

        self.verticalLayout_5.addWidget(self.resamplingAlgorithm)

        self.resamplingDesc = QLabel(self.groupBox_2)
        self.resamplingDesc.setObjectName(u"resamplingDesc")
        self.resamplingDesc.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignTop)
        self.resamplingDesc.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.resamplingDesc)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.recommendedSettings = QPushButton(self.centralwidget)
        self.recommendedSettings.setObjectName(u"recommendedSettings")

        self.horizontalLayout_4.addWidget(self.recommendedSettings)

        self.openSamplePhoto = QPushButton(self.centralwidget)
        self.openSamplePhoto.setObjectName(u"openSamplePhoto")

        self.horizontalLayout_4.addWidget(self.openSamplePhoto)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.deleteOriginalFile = QCheckBox(self.centralwidget)
        self.deleteOriginalFile.setObjectName(u"deleteOriginalFile")

        self.verticalLayout_6.addWidget(self.deleteOriginalFile)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.batal = QPushButton(self.centralwidget)
        self.batal.setObjectName(u"batal")

        self.horizontalLayout_2.addWidget(self.batal)

        self.simpanDanTutup = QPushButton(self.centralwidget)
        self.simpanDanTutup.setObjectName(u"simpanDanTutup")

        self.horizontalLayout_2.addWidget(self.simpanDanTutup)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.resamplingAlgorithm.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Pengaturan Kompresi", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Ubah opsi kompresi file foto Anda. Sebagai referensi, Google Foto menetapkan kompresi 12Mp bagi gambar yang Anda unggah untuk menghemat penyimpanan. Anda direkomendasikan untuk memilih pengaturan dengan tingkat Megapiksel <span style=\" font-weight:700;\">12Mp</span> dan kualitas gambar <span style=\" font-weight:700;\">85%</span> agar kualitas gambar yang dikompresi tidak menurun secara drastis.</p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Pengaturan Dasar", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Resolusi (Megapiksel)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Kualitas Dipertahankan", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Lokasi Simpan", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Format Simpan", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.megaPixel.setSuffix(QCoreApplication.translate("MainWindow", u"Mp", None))
#if QT_CONFIG(tooltip)
        self.photoQuality.setToolTip(QCoreApplication.translate("MainWindow", u"Semakin kecil kualitas, semakin blur gambar yang dihasilkan", None))
#endif // QT_CONFIG(tooltip)
        self.photoQuality.setSuffix(QCoreApplication.translate("MainWindow", u"%", None))
#if QT_CONFIG(tooltip)
        self.saveLocation.setToolTip(QCoreApplication.translate("MainWindow", u"Diset secara default. Ubah dengan menekan \"Pilih Folder\" atau drag-n-drop folder ke line edit.", None))
#endif // QT_CONFIG(tooltip)
        self.saveLocation.setInputMask("")
        self.saveLocation.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Mendukung Drag and Drop", None))
        self.chooseDir.setText(QCoreApplication.translate("MainWindow", u"Pilih Folder", None))
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

        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Algoritma Resampling", None))
        self.resamplingAlgorithm.setItemText(0, QCoreApplication.translate("MainWindow", u"NEAREST", None))
        self.resamplingAlgorithm.setItemText(1, QCoreApplication.translate("MainWindow", u"LANCZOS (Direkomendasikan)", None))
        self.resamplingAlgorithm.setItemText(2, QCoreApplication.translate("MainWindow", u"BILINEAR", None))
        self.resamplingAlgorithm.setItemText(3, QCoreApplication.translate("MainWindow", u"BICUBIC", None))
        self.resamplingAlgorithm.setItemText(4, QCoreApplication.translate("MainWindow", u"BOX", None))
        self.resamplingAlgorithm.setItemText(5, QCoreApplication.translate("MainWindow", u"HAMMING", None))
        self.resamplingAlgorithm.setItemText(6, QCoreApplication.translate("MainWindow", u"MKS2013 (Rekomendasi Kedua)", None))
        self.resamplingAlgorithm.setItemText(7, QCoreApplication.translate("MainWindow", u"MKS2021", None))

        self.resamplingDesc.setText(QCoreApplication.translate("MainWindow", u"Pilih algoritma resampling Anda untuk melihat deskripsi.", None))
#if QT_CONFIG(tooltip)
        self.recommendedSettings.setToolTip(QCoreApplication.translate("MainWindow", u"Gunakan pengaturan yang kami rekomendasikan", None))
#endif // QT_CONFIG(tooltip)
        self.recommendedSettings.setText(QCoreApplication.translate("MainWindow", u"Pengaturan Rekomendasi", None))
#if QT_CONFIG(tooltip)
        self.openSamplePhoto.setToolTip(QCoreApplication.translate("MainWindow", u"Buka jendela untuk melihat perbedaan setiap pengaturan terhadap foto (menggunakan ikon aplikasi)", None))
#endif // QT_CONFIG(tooltip)
        self.openSamplePhoto.setText(QCoreApplication.translate("MainWindow", u"Buka Sampel Foto", None))
        self.deleteOriginalFile.setText(QCoreApplication.translate("MainWindow", u"Hapus File Asli (Tidak Direkomendasikan)", None))
        self.batal.setText(QCoreApplication.translate("MainWindow", u"Batal", None))
        self.simpanDanTutup.setText(QCoreApplication.translate("MainWindow", u"Simpan dan Tutup", None))
    # retranslateUi

