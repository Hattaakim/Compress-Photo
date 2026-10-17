# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selectNewFileiNINYf.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(385, 516)
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

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileOption = QCheckBox(self.centralwidget)
        self.fileOption.setObjectName(u"fileOption")

        self.horizontalLayout.addWidget(self.fileOption)

        self.newPhotoFile = QToolButton(self.centralwidget)
        self.newPhotoFile.setObjectName(u"newPhotoFile")
        self.newPhotoFile.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.newPhotoFile)

        self.deletePhotoFile = QToolButton(self.centralwidget)
        self.deletePhotoFile.setObjectName(u"deletePhotoFile")
        self.deletePhotoFile.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.deletePhotoFile)

        self.resetPhotoTable = QToolButton(self.centralwidget)
        self.resetPhotoTable.setObjectName(u"resetPhotoTable")
        self.resetPhotoTable.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.resetPhotoTable)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.photoTableView = QTableView(self.centralwidget)
        self.photoTableView.setObjectName(u"photoTableView")

        self.verticalLayout.addWidget(self.photoTableView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.folderOption = QCheckBox(self.centralwidget)
        self.folderOption.setObjectName(u"folderOption")

        self.horizontalLayout_2.addWidget(self.folderOption)

        self.newFolder = QToolButton(self.centralwidget)
        self.newFolder.setObjectName(u"newFolder")
        self.newFolder.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.newFolder)

        self.deleteFolder = QToolButton(self.centralwidget)
        self.deleteFolder.setObjectName(u"deleteFolder")
        self.deleteFolder.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.deleteFolder)

        self.resetFolderTable = QToolButton(self.centralwidget)
        self.resetFolderTable.setObjectName(u"resetFolderTable")
        self.resetFolderTable.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.resetFolderTable)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.folderTableView = QTableView(self.centralwidget)
        self.folderTableView.setObjectName(u"folderTableView")

        self.verticalLayout.addWidget(self.folderTableView)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.batal = QPushButton(self.centralwidget)
        self.batal.setObjectName(u"batal")

        self.horizontalLayout_3.addWidget(self.batal)

        self.simpanDanTutup = QPushButton(self.centralwidget)
        self.simpanDanTutup.setObjectName(u"simpanDanTutup")

        self.horizontalLayout_3.addWidget(self.simpanDanTutup)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Tambahkan File Foto", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Tambahkan file foto yang ingin Anda kompresi. Pilih satu atau seluruh metode penambahan file.</p></body></html>", None))
        self.fileOption.setText(QCoreApplication.translate("MainWindow", u"File Satuan", None))
        self.newPhotoFile.setText(QCoreApplication.translate("MainWindow", u"File Baru", None))
        self.deletePhotoFile.setText(QCoreApplication.translate("MainWindow", u"Hapus File", None))
        self.resetPhotoTable.setText(QCoreApplication.translate("MainWindow", u"Reset Tabel", None))
        self.folderOption.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.newFolder.setText(QCoreApplication.translate("MainWindow", u"Folder Baru", None))
        self.deleteFolder.setText(QCoreApplication.translate("MainWindow", u"Hapus Folder", None))
        self.resetFolderTable.setText(QCoreApplication.translate("MainWindow", u"Reset Tabel", None))
        self.batal.setText(QCoreApplication.translate("MainWindow", u"Batal", None))
        self.simpanDanTutup.setText(QCoreApplication.translate("MainWindow", u"Simpan dan Tutup", None))
    # retranslateUi

