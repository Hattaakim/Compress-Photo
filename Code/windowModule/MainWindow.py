# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindowvGYaod.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QSpacerItem, QTableView, QToolButton, QTreeView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(910, 600)
        self.actionDiatur_Otomatis = QAction(MainWindow)
        self.actionDiatur_Otomatis.setObjectName(u"actionDiatur_Otomatis")
        self.actionDitentukan_Pengguna = QAction(MainWindow)
        self.actionDitentukan_Pengguna.setObjectName(u"actionDitentukan_Pengguna")
        self.actionJalankan_Aplikasi_Saat_Perangkat_Dimulai = QAction(MainWindow)
        self.actionJalankan_Aplikasi_Saat_Perangkat_Dimulai.setObjectName(u"actionJalankan_Aplikasi_Saat_Perangkat_Dimulai")
        self.actionTidak_Ditentukan = QAction(MainWindow)
        self.actionTidak_Ditentukan.setObjectName(u"actionTidak_Ditentukan")
        self.actionTentang_Aplikasi = QAction(MainWindow)
        self.actionTentang_Aplikasi.setObjectName(u"actionTentang_Aplikasi")
        self.actionHalaman_Github = QAction(MainWindow)
        self.actionHalaman_Github.setObjectName(u"actionHalaman_Github")
        self.actionHalaman_Instagram = QAction(MainWindow)
        self.actionHalaman_Instagram.setObjectName(u"actionHalaman_Instagram")
        self.actionHubungi_Developer_Email = QAction(MainWindow)
        self.actionHubungi_Developer_Email.setObjectName(u"actionHubungi_Developer_Email")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addJob = QToolButton(self.centralwidget)
        self.addJob.setObjectName(u"addJob")
        self.addJob.setMinimumSize(QSize(70, 80))
        self.addJob.setMaximumSize(QSize(70, 80))
        self.addJob.setStyleSheet(u"background-color:transparent")
        self.addJob.setIconSize(QSize(40, 40))
        self.addJob.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.addJob)

        self.deleteSelected = QToolButton(self.centralwidget)
        self.deleteSelected.setObjectName(u"deleteSelected")
        self.deleteSelected.setMinimumSize(QSize(70, 80))
        self.deleteSelected.setMaximumSize(QSize(70, 80))
        self.deleteSelected.setStyleSheet(u"background-color:transparent")
        self.deleteSelected.setIconSize(QSize(40, 40))
        self.deleteSelected.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.deleteSelected)

        self.cancelDeleteSelected = QToolButton(self.centralwidget)
        self.cancelDeleteSelected.setObjectName(u"cancelDeleteSelected")
        self.cancelDeleteSelected.setMinimumSize(QSize(70, 80))
        self.cancelDeleteSelected.setMaximumSize(QSize(70, 80))
        self.cancelDeleteSelected.setStyleSheet(u"background-color:transparent")
        self.cancelDeleteSelected.setIconSize(QSize(40, 40))
        self.cancelDeleteSelected.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.cancelDeleteSelected)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.startVerify = QToolButton(self.centralwidget)
        self.startVerify.setObjectName(u"startVerify")
        self.startVerify.setMinimumSize(QSize(70, 80))
        self.startVerify.setMaximumSize(QSize(70, 80))
        self.startVerify.setStyleSheet(u"background-color:transparent")
        self.startVerify.setIconSize(QSize(40, 40))
        self.startVerify.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.startVerify)

        self.startCompress = QToolButton(self.centralwidget)
        self.startCompress.setObjectName(u"startCompress")
        self.startCompress.setMinimumSize(QSize(70, 80))
        self.startCompress.setMaximumSize(QSize(70, 80))
        self.startCompress.setStyleSheet(u"background-color:transparent")
        self.startCompress.setIconSize(QSize(40, 40))
        self.startCompress.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.startCompress)

        self.compressSettings = QToolButton(self.centralwidget)
        self.compressSettings.setObjectName(u"compressSettings")
        self.compressSettings.setMinimumSize(QSize(70, 80))
        self.compressSettings.setMaximumSize(QSize(70, 80))
        self.compressSettings.setStyleSheet(u"background-color:transparent")
        self.compressSettings.setIconSize(QSize(40, 40))
        self.compressSettings.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.compressSettings)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.revealFile = QToolButton(self.centralwidget)
        self.revealFile.setObjectName(u"revealFile")
        self.revealFile.setMinimumSize(QSize(70, 80))
        self.revealFile.setMaximumSize(QSize(70, 80))
        self.revealFile.setStyleSheet(u"background-color:transparent")
        self.revealFile.setIconSize(QSize(40, 40))
        self.revealFile.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.revealFile)

        self.reloadTable = QToolButton(self.centralwidget)
        self.reloadTable.setObjectName(u"reloadTable")
        self.reloadTable.setMinimumSize(QSize(70, 80))
        self.reloadTable.setMaximumSize(QSize(70, 80))
        self.reloadTable.setStyleSheet(u"background-color:transparent")
        self.reloadTable.setIconSize(QSize(40, 40))
        self.reloadTable.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.reloadTable)

        self.horizontalSpacer = QSpacerItem(869, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pageNavigator = QTreeView(self.centralwidget)
        self.pageNavigator.setObjectName(u"pageNavigator")
        self.pageNavigator.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_2.addWidget(self.pageNavigator)

        self.universalTableView = QTableView(self.centralwidget)
        self.universalTableView.setObjectName(u"universalTableView")

        self.horizontalLayout_2.addWidget(self.universalTableView)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 910, 22))
        self.menuPengaturan = QMenu(self.menubar)
        self.menuPengaturan.setObjectName(u"menuPengaturan")
        self.menuJumlah_CPU_Digunakan = QMenu(self.menuPengaturan)
        self.menuJumlah_CPU_Digunakan.setObjectName(u"menuJumlah_CPU_Digunakan")
        self.menuMulai_Otomatis = QMenu(self.menuPengaturan)
        self.menuMulai_Otomatis.setObjectName(u"menuMulai_Otomatis")
        self.menuTentang = QMenu(self.menubar)
        self.menuTentang.setObjectName(u"menuTentang")
        self.menuDibuat_oleh_Hattaakim = QMenu(self.menuTentang)
        self.menuDibuat_oleh_Hattaakim.setObjectName(u"menuDibuat_oleh_Hattaakim")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuPengaturan.menuAction())
        self.menubar.addAction(self.menuTentang.menuAction())
        self.menuPengaturan.addAction(self.menuJumlah_CPU_Digunakan.menuAction())
        self.menuPengaturan.addSeparator()
        self.menuPengaturan.addAction(self.menuMulai_Otomatis.menuAction())
        self.menuJumlah_CPU_Digunakan.addAction(self.actionDiatur_Otomatis)
        self.menuJumlah_CPU_Digunakan.addAction(self.actionDitentukan_Pengguna)
        self.menuMulai_Otomatis.addAction(self.actionJalankan_Aplikasi_Saat_Perangkat_Dimulai)
        self.menuMulai_Otomatis.addAction(self.actionTidak_Ditentukan)
        self.menuTentang.addAction(self.actionTentang_Aplikasi)
        self.menuTentang.addAction(self.menuDibuat_oleh_Hattaakim.menuAction())
        self.menuDibuat_oleh_Hattaakim.addAction(self.actionHalaman_Github)
        self.menuDibuat_oleh_Hattaakim.addAction(self.actionHalaman_Instagram)
        self.menuDibuat_oleh_Hattaakim.addAction(self.actionHubungi_Developer_Email)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionDiatur_Otomatis.setText(QCoreApplication.translate("MainWindow", u"Ditentukan Otomatis", None))
        self.actionDitentukan_Pengguna.setText(QCoreApplication.translate("MainWindow", u"Ditentukan Pengguna", None))
        self.actionJalankan_Aplikasi_Saat_Perangkat_Dimulai.setText(QCoreApplication.translate("MainWindow", u"Jalankan Aplikasi Saat Perangkat Dimulai", None))
        self.actionTidak_Ditentukan.setText(QCoreApplication.translate("MainWindow", u"Tidak Ditentukan", None))
        self.actionTentang_Aplikasi.setText(QCoreApplication.translate("MainWindow", u"Tentang Aplikasi", None))
        self.actionHalaman_Github.setText(QCoreApplication.translate("MainWindow", u"Halaman Github", None))
        self.actionHalaman_Instagram.setText(QCoreApplication.translate("MainWindow", u"Halaman Instagram", None))
        self.actionHubungi_Developer_Email.setText(QCoreApplication.translate("MainWindow", u"Hubungi Developer (Email)", None))
        self.addJob.setText(QCoreApplication.translate("MainWindow", u"Tambah File\n"
"atau Foto", None))
        self.deleteSelected.setText(QCoreApplication.translate("MainWindow", u"Hapus File\n"
"Terpilih", None))
        self.cancelDeleteSelected.setText(QCoreApplication.translate("MainWindow", u"Batal Hapus\n"
"File Terpilih", None))
        self.startVerify.setText(QCoreApplication.translate("MainWindow", u"Verifikasi\n"
"File", None))
        self.startCompress.setText(QCoreApplication.translate("MainWindow", u"Mulai\n"
"Kompresi", None))
        self.compressSettings.setText(QCoreApplication.translate("MainWindow", u"Pengaturan\n"
"Kompresi", None))
        self.revealFile.setText(QCoreApplication.translate("MainWindow", u"Tunjukkan\n"
"File", None))
        self.reloadTable.setText(QCoreApplication.translate("MainWindow", u"Refresh\n"
"Tabel", None))
        self.menuPengaturan.setTitle(QCoreApplication.translate("MainWindow", u"Performa", None))
        self.menuJumlah_CPU_Digunakan.setTitle(QCoreApplication.translate("MainWindow", u"Jumlah CPU Digunakan", None))
        self.menuMulai_Otomatis.setTitle(QCoreApplication.translate("MainWindow", u"Mulai Otomatis", None))
        self.menuTentang.setTitle(QCoreApplication.translate("MainWindow", u"Informasi Lainnya", None))
        self.menuDibuat_oleh_Hattaakim.setTitle(QCoreApplication.translate("MainWindow", u"Dibuat oleh @Hattaakim", None))
    # retranslateUi

