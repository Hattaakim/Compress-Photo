# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pictureSamplepdlaYP.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1099, 490)
        MainWindow.setMinimumSize(QSize(885, 490))
        MainWindow.setMaximumSize(QSize(16777215, 500))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_12 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_12.addWidget(self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignTop)
        self.label_2.setWordWrap(True)

        self.verticalLayout_12.addWidget(self.label_2)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1063, 392))
        self.horizontalLayout_4 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout = QVBoxLayout(self.groupBox_6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.beforeImage = QGraphicsView(self.groupBox_6)
        self.beforeImage.setObjectName(u"beforeImage")
        self.beforeImage.setMinimumSize(QSize(300, 300))

        self.verticalLayout.addWidget(self.beforeImage)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.samplePhotoDir = QLineEdit(self.groupBox_6)
        self.samplePhotoDir.setObjectName(u"samplePhotoDir")

        self.horizontalLayout_3.addWidget(self.samplePhotoDir)

        self.choosePhotoFile = QPushButton(self.groupBox_6)
        self.choosePhotoFile.setObjectName(u"choosePhotoFile")

        self.horizontalLayout_3.addWidget(self.choosePhotoFile)

        self.beforeScaleUp = QPushButton(self.groupBox_6)
        self.beforeScaleUp.setObjectName(u"beforeScaleUp")
        self.beforeScaleUp.setMinimumSize(QSize(30, 30))
        self.beforeScaleUp.setMaximumSize(QSize(30, 30))

        self.horizontalLayout_3.addWidget(self.beforeScaleUp)

        self.beforeScaleDown = QPushButton(self.groupBox_6)
        self.beforeScaleDown.setObjectName(u"beforeScaleDown")
        self.beforeScaleDown.setMinimumSize(QSize(30, 30))
        self.beforeScaleDown.setMaximumSize(QSize(30, 30))

        self.horizontalLayout_3.addWidget(self.beforeScaleDown)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addWidget(self.groupBox_6)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_3)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(140, 0))
        self.label_3.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(140, 0))
        self.label_4.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(140, 0))
        self.label_8.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_3.addWidget(self.label_8)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(20, 20))
        self.label_5.setMaximumSize(QSize(20, 20))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_5)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(20, 20))
        self.label_6.setMaximumSize(QSize(20, 20))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_6)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(20, 20))
        self.label_7.setMaximumSize(QSize(20, 20))
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_7)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.megaPixel = QSpinBox(self.groupBox)
        self.megaPixel.setObjectName(u"megaPixel")
        self.megaPixel.setMinimum(1)
        self.megaPixel.setMaximum(200)
        self.megaPixel.setValue(12)

        self.verticalLayout_6.addWidget(self.megaPixel)

        self.photoQuality = QSpinBox(self.groupBox)
        self.photoQuality.setObjectName(u"photoQuality")
        self.photoQuality.setMinimum(1)
        self.photoQuality.setMaximum(100)
        self.photoQuality.setValue(85)

        self.verticalLayout_6.addWidget(self.photoQuality)

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

        self.verticalLayout_6.addWidget(self.resamplingAlgorithm)


        self.horizontalLayout.addLayout(self.verticalLayout_6)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.startCompressSimulation = QPushButton(self.groupBox)
        self.startCompressSimulation.setObjectName(u"startCompressSimulation")

        self.verticalLayout_9.addWidget(self.startCompressSimulation)


        self.verticalLayout_11.addWidget(self.groupBox)

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(140, 0))
        self.label_12.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_8.addWidget(self.label_12)

        self.label_19 = QLabel(self.groupBox_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(140, 0))
        self.label_19.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_8.addWidget(self.label_19)

        self.label_14 = QLabel(self.groupBox_5)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(140, 0))
        self.label_14.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_8.addWidget(self.label_14)

        self.label_9 = QLabel(self.groupBox_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(140, 0))
        self.label_9.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_8.addWidget(self.label_9)

        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(140, 0))
        self.label_10.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_8.addWidget(self.label_10)

        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(140, 0))
        self.label_11.setMaximumSize(QSize(140, 16777215))

        self.verticalLayout_8.addWidget(self.label_11)


        self.horizontalLayout_2.addLayout(self.verticalLayout_8)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_15 = QLabel(self.groupBox_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(20, 20))
        self.label_15.setMaximumSize(QSize(20, 20))
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_15)

        self.label_16 = QLabel(self.groupBox_5)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(20, 20))
        self.label_16.setMaximumSize(QSize(20, 20))
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_16)

        self.label_17 = QLabel(self.groupBox_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(20, 20))
        self.label_17.setMaximumSize(QSize(20, 20))
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_17)

        self.label_18 = QLabel(self.groupBox_5)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(20, 20))
        self.label_18.setMaximumSize(QSize(20, 20))
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_18)

        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(20, 20))
        self.label_13.setMaximumSize(QSize(20, 20))
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_13)

        self.label_20 = QLabel(self.groupBox_5)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(20, 20))
        self.label_20.setMaximumSize(QSize(20, 20))
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_20)


        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.fileExt = QLineEdit(self.groupBox_5)
        self.fileExt.setObjectName(u"fileExt")

        self.verticalLayout_10.addWidget(self.fileExt)

        self.fileFormat = QLineEdit(self.groupBox_5)
        self.fileFormat.setObjectName(u"fileFormat")

        self.verticalLayout_10.addWidget(self.fileFormat)

        self.compressStatus = QLineEdit(self.groupBox_5)
        self.compressStatus.setObjectName(u"compressStatus")

        self.verticalLayout_10.addWidget(self.compressStatus)

        self.fileSize0 = QLineEdit(self.groupBox_5)
        self.fileSize0.setObjectName(u"fileSize0")

        self.verticalLayout_10.addWidget(self.fileSize0)

        self.fileSize1 = QLineEdit(self.groupBox_5)
        self.fileSize1.setObjectName(u"fileSize1")

        self.verticalLayout_10.addWidget(self.fileSize1)

        self.sizeReduced = QLineEdit(self.groupBox_5)
        self.sizeReduced.setObjectName(u"sizeReduced")

        self.verticalLayout_10.addWidget(self.sizeReduced)


        self.horizontalLayout_2.addLayout(self.verticalLayout_10)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)


        self.verticalLayout_11.addWidget(self.groupBox_5)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_11)

        self.groupBox_7 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.afterImage = QGraphicsView(self.groupBox_7)
        self.afterImage.setObjectName(u"afterImage")
        self.afterImage.setMinimumSize(QSize(300, 300))

        self.verticalLayout_2.addWidget(self.afterImage)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.afterScaleUp = QPushButton(self.groupBox_7)
        self.afterScaleUp.setObjectName(u"afterScaleUp")
        self.afterScaleUp.setMinimumSize(QSize(30, 30))
        self.afterScaleUp.setMaximumSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.afterScaleUp)

        self.afterScaleDown = QPushButton(self.groupBox_7)
        self.afterScaleDown.setObjectName(u"afterScaleDown")
        self.afterScaleDown.setMinimumSize(QSize(30, 30))
        self.afterScaleDown.setMaximumSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.afterScaleDown)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_4.addWidget(self.groupBox_7)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_12.addWidget(self.scrollArea)

        self.verticalSpacer = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.resamplingAlgorithm.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sampel Foto", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Halaman untuk mencoba kinerja algoritma dan rasio kompresi tertentu menggunakan sampel gambar yang Anda miliki. Hasil simulasi mungkin berbeda-beda tergantung ukuran gambar dan pengaturan kompresi yang Anda terapkan.</p></body></html>", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Sebelum Kompresi", None))
        self.samplePhotoDir.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pilih atau Tarik dan Lepas File Foto Ke Sini", None))
        self.choosePhotoFile.setText(QCoreApplication.translate("MainWindow", u"Pilih File", None))
#if QT_CONFIG(tooltip)
        self.beforeScaleUp.setToolTip(QCoreApplication.translate("MainWindow", u"Perbesar gambar sebelum kompresi", None))
#endif // QT_CONFIG(tooltip)
        self.beforeScaleUp.setText("")
#if QT_CONFIG(tooltip)
        self.beforeScaleDown.setToolTip(QCoreApplication.translate("MainWindow", u"Perkecil gambar sebelum kompresi", None))
#endif // QT_CONFIG(tooltip)
        self.beforeScaleDown.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Pengaturan Kompresi", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Resolusi (Megapiksel)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Kualitas Dipertahankan", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Algoritma Resampling", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.megaPixel.setSuffix(QCoreApplication.translate("MainWindow", u"Mp", None))
#if QT_CONFIG(tooltip)
        self.photoQuality.setToolTip(QCoreApplication.translate("MainWindow", u"Semakin kecil kualitas, semakin blur gambar yang dihasilkan", None))
#endif // QT_CONFIG(tooltip)
        self.photoQuality.setSuffix(QCoreApplication.translate("MainWindow", u"%", None))
        self.resamplingAlgorithm.setItemText(0, QCoreApplication.translate("MainWindow", u"NEAREST", None))
        self.resamplingAlgorithm.setItemText(1, QCoreApplication.translate("MainWindow", u"LANCZOS (Direkomendasikan)", None))
        self.resamplingAlgorithm.setItemText(2, QCoreApplication.translate("MainWindow", u"BILINEAR", None))
        self.resamplingAlgorithm.setItemText(3, QCoreApplication.translate("MainWindow", u"BICUBIC", None))
        self.resamplingAlgorithm.setItemText(4, QCoreApplication.translate("MainWindow", u"BOX", None))
        self.resamplingAlgorithm.setItemText(5, QCoreApplication.translate("MainWindow", u"HAMMING", None))
        self.resamplingAlgorithm.setItemText(6, QCoreApplication.translate("MainWindow", u"MKS2013 (Rekomendasi Kedua)", None))
        self.resamplingAlgorithm.setItemText(7, QCoreApplication.translate("MainWindow", u"MKS2021", None))

        self.startCompressSimulation.setText(QCoreApplication.translate("MainWindow", u"Mulai Kompresi", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Detail File dan Hasil Kompresi", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Ekstensi File", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Format File", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Status Kompresi", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Ukuran File Awal", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Ukuran File Akhir", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Penghematan", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Setelah Kompresi", None))
#if QT_CONFIG(tooltip)
        self.afterScaleUp.setToolTip(QCoreApplication.translate("MainWindow", u"Perbesar gambar setelah kompresi", None))
#endif // QT_CONFIG(tooltip)
        self.afterScaleUp.setText("")
#if QT_CONFIG(tooltip)
        self.afterScaleDown.setToolTip(QCoreApplication.translate("MainWindow", u"Perbesar gambar setelah kompresi", None))
#endif // QT_CONFIG(tooltip)
        self.afterScaleDown.setText("")
    # retranslateUi

