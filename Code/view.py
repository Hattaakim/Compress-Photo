from PySide6.QtWidgets import QAbstractItemView, QApplication, QComboBox, QFileDialog, QMainWindow, QMessageBox, QStyledItemDelegate, QTableView, QTreeView
from PySide6.QtCore import QEvent, QModelIndex, QObject, QRegularExpression, QSize, QStandardPaths, QTimer, Qt, Signal
from PySide6.QtGui import QIcon, QRegularExpressionValidator, QStandardItem, QStandardItemModel
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtSql import QSqlTableModel
import sys, os, math, shiboken6, gc, subprocess, platform
from datetime import datetime
from dataclasses import dataclass
from typing import Literal, Callable
from multiprocessing import Pool, cpu_count, Queue, Pipe, Process

######### Externally Managed Module #########
from managedModule import backend, compressModule

######### Assets File ############
from assets import resources

######### Window ##########
from windowModule import MainWindow, selectNewFile, PerfSettingCPU, CompressSettings

######### Global Const #########
APPID = "Compress Foto@hattaakim"

######### Custom Class For Struct ########
@dataclass
class allTableModelStruct:
    """Struct dictionary untuk merangkap (nama tabel sql, init delegate, whichButtonEnabled, whichButtonDisabled)"""
    name: str
    init_delegate: Callable
    enabledButton: list
    disabledButton: list

######### Internal Functions ##########
def showInfo(parent, judul:str, 
             pesan:str, 
             ikon:Literal["info", "warning", 
                          "error", "question"]):
    """Fungsi buat memunculkan dialog info pakai Qt"""
    ikonMap = {
        "info": QMessageBox.Icon.Information,
        "warning": QMessageBox.Icon.Warning,
        "error": QMessageBox.Icon.Critical,
        "question": QMessageBox.Icon.Question
    }
    msgBox = QMessageBox(parent)
    msgBox.setWindowTitle(judul)
    msgBox.setText(pesan)
    msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)
    msgBox.setIcon(
        ikonMap.get(ikon, QMessageBox.Icon.Information)
    )
    msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    return msgBox.exec()

def makeStandardItem(text, alignment=Qt.AlignmentFlag.AlignCenter):
    item = QStandardItem(text)
    item.setTextAlignment(alignment)
    return item

def bringQuestion(parent, judul:str,
                  pesan:str, ikon:Literal["info", "warning",
                                          "error", "question"],
                                          tombol1:Literal["yes", "no"],
                                          tombol2:Literal["yes", "no"]):
    """Fungsi buat memunculkan dialog pertanyaan di QT"""
    ikonMap = {
        "info": QMessageBox.Icon.Information,
        "warning": QMessageBox.Icon.Warning,
        "error": QMessageBox.Icon.Critical,
        "question": QMessageBox.Icon.Question
    }
    tombolMap = {
        "yes": QMessageBox.StandardButton.Yes,
        "no": QMessageBox.StandardButton.No,
        "ok": QMessageBox.StandardButton.Ok
    }
    msgBox = QMessageBox(parent)
    msgBox.setWindowTitle(judul)
    msgBox.setText(pesan)
    msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)
    msgBox.setIcon(
        ikonMap.get(ikon, QMessageBox.Icon.Information)
    )
    msgBox.setStandardButtons(
        tombolMap.get(tombol1) | tombolMap.get(tombol2)
    )
    return msgBox.exec()

def chooseFiles(parent, judul:str):
    """Buat memunculkan dialog file choose besar, khusus extension gambar"""
    downloadsPath = QStandardPaths.writableLocation(
        QStandardPaths.DownloadLocation
    )
    validExt = [".jpg", ".jpeg", ".png"]
    fileDlg = QFileDialog(parent)
    fileDlg.setWindowModality(Qt.WindowModality.ApplicationModal)
    selectedFile, _ = fileDlg.getOpenFileNames(
        parent,
        judul,
        downloadsPath,
    )
    if selectedFile:
        validFiles = [f for f in selectedFile
                      if os.path.splitext(f)[1].lower() in validExt]
        if validFiles:
            return validFiles
        return None
    return None

def chooseFolder(parent, judul:str):
    """Buat munculin dialog explorer memilih folder aja (file dihidden)"""
    downloadsPath = QStandardPaths.writableLocation(
        QStandardPaths.DownloadLocation
    )
    fileDlg = QFileDialog(parent)
    fileDlg.setWindowModality(Qt.WindowModality.ApplicationModal)
    fileDlg.getExistingDirectoryUrl
    folderPath = fileDlg.getExistingDirectory(
        parent,
        judul,
        downloadsPath,
        QFileDialog.Option.ShowDirsOnly
    )

    if folderPath:
        return folderPath
    return None

def humanReadableSize(fileSize):
    """Konversi nilai desimal file menjadi readable untuk manusia"""
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    if fileSize == 0:
        return "0 B"

    i = min(int(math.log(abs(fileSize), 1024)), len(units)-1)
    return f"{fileSize / (1024**i):.2f} {units[i]}"

######### Custom Class For Qt6 Apps###########
class TableAlignDelegate(QStyledItemDelegate):
    """Class untuk mengatur alignment tabel QTableView (bukan QSqlTableModel)"""
    def __init__(self, align=Qt.AlignmentFlag.AlignLeft, parent=None):
        super().__init__(parent)
        self.alignment = align

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = self.alignment

class InterpretTableDelegate(QStyledItemDelegate):
    """Menginterpretasikan angka pada tabel SQL agar lebih mudah dipahami oleh manusia"""
    def __init__(self, align=Qt.AlignmentFlag.AlignCenter, parent=None):
        super().__init__(parent)
        self.alignment = align

    def displayText(self, value, locale):
        fileStatusMap = {
            0: "-", 1: "✔", 2: "✘"
        }
        return fileStatusMap.get(value, "Unsigned")

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = self.alignment

class FileSizeTableDelegate(QStyledItemDelegate):
    def __init__(self, align=Qt.AlignmentFlag.AlignCenter, parent=None):
        super().__init__(parent)
        self.alignment = align

    def displayText(self, value, locale):
        return humanReadableSize(value)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = self.alignment

class SingleInstance(QApplication):
    """Buat memastikan hanya satu instance aplikasi yang berjalan dalam satuan waktu, scalable"""
    def __init__(self, argv):
        super().__init__(argv)
        self.server = None
        self.isRunning = False

        socket = QLocalSocket()
        socket.connectToServer(APPID)
        if socket.waitForConnected(100):
            socket.write(b"APP_ALREADY_RUNNING")
            socket.flush()
            socket.waitForBytesWritten(100)
            socket.disconnectFromServer()
            self.isRunning = True
            return

        self.server = QLocalServer()
        if not self.server.listen(APPID):
            self.isRunning = True
            return
        self.server.newConnection.connect(self.onNewInstanceResponse)

    def onNewInstanceResponse(self):
        conn = self.server.nextPendingConnection()
        if not conn:
            return
        conn.waitForReadyRead(100)
        data = bytes(
            conn.readAll()
        ).decode(errors="ignore")
        if data.strip() == "APP_ALREADY_RUNNING":
            WM_.allWindow[WM_.activeWindowKey].showNormal()
            WM_.allWindow[WM_.activeWindowKey].raise_()
            WM_.allWindow[WM_.activeWindowKey].activateWindow()

    def cleanSocket(self):
        if self.server:
            self.server.removeServer(APPID)
            self.server.close()

class TableViewDragnDropFilter(QObject):
    """Filter biar QTableView bisa accept dropEvent File/Folder"""
    def __init__(self, tView:QTableView, 
                 tModel:QSqlTableModel, 
                 dbPassthrought:backend.QNativeFileDatabase, 
                 type:Literal['File', 'Folder'], parent=None):
        super().__init__(parent)
        self.table = tView
        self.model = tModel
        self.sqlDb = dbPassthrought
        self.filterType = type

    def eventFilter(self, watched, event):
        if watched == self.table:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True

            elif event.type() == QEvent.Type.Drop:
                bulkInsertData = []
                if event.mimeData().hasUrls():
                    if self.filterType == 'File':
                        for url in event.mimeData().urls():
                            hasil = self.sqlDb.selectQuery(querySQL="SELECT fileDir from fileJobTable")
                            existsFile = {file[0] for file in hasil}
                            validExt = {".jpg", ".jpeg", ".png"}

                            droppedFile = os.path.normpath(url.toLocalFile())
                            fileExt = os.path.splitext(droppedFile)[1].lower()

                            if droppedFile not in existsFile and fileExt in validExt and os.path.isfile(droppedFile):
                                bulkInsertData.append((os.path.basename(droppedFile), droppedFile, fileExt))

                        if bulkInsertData:
                            self.sqlDb.executeQuery(
                                querySQL="INSERT INTO newFileTable(fileName, fileDir, fileExt) VALUES (?,?,?)",
                                params=bulkInsertData, isMultipleParams=True
                            )

                    elif self.filterType == 'Folder':
                        for url in event.mimeData().urls():
                            hasil = self.sqlDb.selectQuery(querySQL="SELECT folderPath FROM newFolderTable")
                            existsFolder = {folder[0] for folder in hasil}

                            droppedFolder = os.path.normpath(url.toLocalFile())
                            folderName = os.path.basename(droppedFolder)

                            if droppedFolder not in existsFolder and os.path.isdir(droppedFolder):
                                bulkInsertData.append((folderName, droppedFolder))

                        if bulkInsertData:
                            self.sqlDb.executeQuery(
                                querySQL="INSERT INTO newFolderTable(folderName, folderPath) VALUES (?,?)",
                                params=bulkInsertData, isMultipleParams=True
                            )
                    self.model.select()
                    event.acceptProposedAction()
                    return True
        return False

class LineEditDragnDropFilter(QObject):
    def __init__(self, lineEdit, allFilePathCategory, parent=None):
        self.lineEdit = lineEdit
        self.allFilePathCategory = allFilePathCategory

    def eventFilter(self, watched, event):
        if watched == self.lineEdit:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()

            elif event.type() == QEvent.Type.Drop:
                if event.mimeData().hasUrls():
                    lokasiSimpan = os.path.normpath(event.mimeData().urls()[0].toLocalFile())
                    if lokasiSimpan not in self.allFilePathCategory and os.path.isdir(lokasiSimpan):
                        self.lineEdit.setText(f"{lokasiSimpan}")
                    
                    else:
                        showInfo(self, "Ups.. Kesalahan", "Folder yang Anda pilih mungkin mengandung kategori sebagai berikut.\n1. Tujuan simpan sama dengan tujuan datangnya file foto\n2. Tujuan simpan tidak benar-benar ada\nTolong Verifikasi lagi ya. Kami menunggumu dengan santai!",
                                 'info')
                    event.acceptProposedAction()
                    return True
                return False

class SaberButtonFilter(QObject):
    def __init__(self, saberPButton, parent=None):
        super().__init__(parent)
        self.saberPButton = saberPButton
        self.hoverType = {QEvent.Type.HoverEnter: 1,
                          QEvent.Type.HoverLeave: 0}

    def eventFilter(self, watched, event):
        if watched in self.saberPButton:
            if event.type() in list(self.hoverType.keys()):
                watched.setIcon(QIcon(self.saberPButton[watched][self.hoverType[event.type()]]))
                watched.setIconSize(QSize(30,30))
                return True
            return False
        return False

class WindowManager:
    def __init__(self):
        self.allWindow = {}
        self.activeWindowKey = None

    def openWindow(self, wClass, *args, **kwargs):
        self.activeWindowKey = wClass
        if wClass not in self.allWindow:
            self.allWindow[wClass] = wClass(*args, **kwargs)

        window = self.allWindow[wClass]
        return window

    def closeWindow(self, wClass):
        if wClass in self.allWindow:
            self.allWindow[wClass].deleteLater()
            try:
                shiboken6.delete(self.allWindow[wClass])
            except RuntimeError as e:
                showInfo(None, "C++ Object Error", f"{e}", 'error')
                pass
            del self.allWindow[wClass]
            gc.collect()

######## Window Class GUI #########
class HomeScreen(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        """Initialize the Window as QMainWindow"""
        super().__init__()
        self.setupUi(self)
        #### CONST For Icon ####
        self.saberPButton = {self.addJob: [':/hs_addJobIcon0', ':/hs_addJobIcon1'],
                             self.deleteSelected: [':/hs_deleteSelected0', ':/hs_deleteSelected1'],
                             self.cancelDeleteSelected: [':/hs_cancelDeleteSelected0', ':/hs_cancelDeleteSelected1'],
                             self.startVerify: [':/hs_startVerify0', ':/hs_startVerify1'],
                             self.compressSettings: [':/hs_compressSettings0', ':/hs_compressSettings1'],
                             self.startCompress: [':/hs_startCompress0', ':/hs_startCompress1'],
                             self.revealFile: [':/hs_revealFile0', ':/hs_revealFile1'],
                             self.reloadTable: [':/hs_reloadTable0', ":/hs_reloadTable1"]}
        self.appIcon = ':/ai_appDefaultIcon'
        self.treeModelIcon = {
            ":/tvp_daftarUtama": [":/tvp_fotoBaru", ":/tvp_siapDiproses", ":/tvp_selesaiDiproses"],
            ":/tvp_daftarTerhapus": [":/tvp_fotoDitolak", ":/tvp_batalDiproses"]
        }

        #### Global Const - Accessible For Anything ####
        self.appFullPath = sys.executable if getattr(sys, 'frozen', False) else __file__
        self.appPathJustDir = os.path.dirname(self.appFullPath) 

        #### CONST For Tree View Page Navigator ####
        self.treeModelItem = {
            "Daftar Utama": ["Foto Baru", "Siap Diproses", "Selesai Diproses"],
            "Daftar Terhapus": ["Foto Ditolak", "Batal Diproses"]
        }
        self.treeModel = QStandardItemModel(self)
        self.pageNavRoot = self.treeModel.invisibleRootItem()

        #### Const For Table Model ####
        self.currentTableModel = 0
        self.currentRowClicked = None

        #### Const For SQL Database ####
        self.sqlDb = backend.QNativeFileDatabase()

        #### Const For User Personalization .json ####
        self.userPersonalization = backend.UserPersonalization(self.appPathJustDir)

        #### Const For Start On Boot ####
        self.startOnBoot = backend.QNativeBootStart(self.appFullPath)

        #### Const For Parallelism Workers ####
        self.numWorkers = 0

        #### CONST For SQL Table Model ####
        self.sqlTableModel = QSqlTableModel(self, db=self.sqlDb.fileDatabase)
        self.sqlTableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self._reloadTableStatus = 0
        self.allTableModel = {
            0: allTableModelStruct(name="fileJobTable", init_delegate=self.fileJobTableDelegateInit,
                                   enabledButton=[self.addJob, self.deleteSelected, self.startVerify, self.revealFile], 
                                   disabledButton=[self.cancelDeleteSelected, self.startCompress, self.compressSettings]),
            1: allTableModelStruct(name="verifyFileTable", init_delegate=self.verifyFileTableDelegateInit,
                                   enabledButton=[self.deleteSelected, self.startCompress, self.compressSettings, self.revealFile],
                                   disabledButton=[self.addJob, self.cancelDeleteSelected, self.startVerify]),
            2: allTableModelStruct(name="compressedFileTable", init_delegate=self.compressedFileTableDelegateInit,
                                   enabledButton=[self.revealFile, self.deleteSelected],
                                   disabledButton=[self.addJob, self.cancelDeleteSelected, self.startVerify, self.startCompress, self.compressSettings]),
            3: allTableModelStruct(name="photoRejectedTable", init_delegate=self.photoRejectedTableDelegateInit,
                                   enabledButton=[self.deleteSelected, self.revealFile],
                                   disabledButton=[self.addJob, self.cancelDeleteSelected, self.startVerify, self.startCompress, self.compressSettings]),
            4: allTableModelStruct(name="photoCancelledTable", init_delegate=self.photoCancelledTableDelegateInit,
                                   enabledButton=[self.cancelDeleteSelected, self.revealFile, self.deleteSelected],
                                   disabledButton=[self.addJob, self.startVerify, self.startCompress, self.compressSettings])
        }

        #### Const For Table Headers and Delegate ####
        self.fotoBaruTableHeader = {"No.": 30, "Nama File": 90, "Lokasi File": 250, "Ekstensi File": 80}
        self.verifyFileTableHeader = self.fotoBaruTableHeader | {"Format File": 75, "Dukungan File": 85, "Integritas File": 85, "File Aman": 65,"Ukuran Awal": 85}
        self.compressedFileTableHeader = self.verifyFileTableHeader | {"Ukuran Akhir": 75, "Penghematan": 70, "Lokasi Simpan": 250, "Dihapus": 70}
        self.photoRejectedTableHeader = self.fotoBaruTableHeader | {"Format File": 75, "Dukungan File": 85, "Integritas File": 85, "File Aman": 65}
        self.photoCancelledTableHeader = self.fotoBaruTableHeader | {"Tanggal Dihapus": 100}
        self.allTableHeader = [self.fotoBaruTableHeader, self.verifyFileTableHeader, self.compressedFileTableHeader,
                               self.photoRejectedTableHeader, self.photoCancelledTableHeader]

        self.delegateTableLeftAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignLeft, self)
        self.delegateTableCenterAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignCenter, self)
        self.delegateFileSize = FileSizeTableDelegate(Qt.AlignmentFlag.AlignCenter, self)
        self.delegateTableInterpret = InterpretTableDelegate(Qt.AlignmentFlag.AlignCenter, self)

        #### CONST FOR showInfo/bringQuestion Between different currentTableModel ####
        self.msgDeleteSelectedRow = ("Anda yakin ingin menghapus file ini dari daftar file? File asli Anda tidak akan terhapus dan file ini akan masuk ke dalam daftar 'Batal Diproses'", 
                                     "File ini telah diverifikasi dan siap untuk dikompresi. Anda tetap ingin menghapusnya?", 
                                     "Anda ingin menghapus file hasil kompresi ini", 
                                     "Foto ini telah ditolak sistem dan tidak dapat diproses lebih lanjut. Ingin menghapusnya dari daftar file? File asli Anda tidak akan terhapus.", 
                                     "Anda yakin untuk menghapus permanen file ini dari daftar file? File asli Anda tidak akan terpengaruh.")

        #### CONST FOR Verify File Async Process ####
        self.pool = None
        self.verifyFileIPC = Queue()
        self.timerCheckVFIPC = QTimer(self)
        self.timerUpdateVerifyTable = QTimer(self)
        self._bufferVerifikasiFile = []
        self.doneVerifyCount = 0
        self.verifyFileCount = 0
        self.verifyFileThreadStatus = 0

        #### CONST The Table ####
        self.universalTableView.setModel(self.sqlTableModel)
        self.universalTableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.universalTableView.verticalHeader().setVisible(False)

        #### CONST the Window ####
        self.setWindowIcon(QIcon(self.appIcon))
        self.setWindowTitle("Kompresi Gambar")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        #### CONST SaberPushButton ####
        self.saberButtonFiler = SaberButtonFilter(self.saberPButton, self)

        #### CONST Tree Page Navigator ####
        self.pageNavigator.setModel(self.treeModel)
        self.pageNavigator.setExpandsOnDoubleClick(True)
        self.pageNavigator.setItemsExpandable(True)
        self.pageNavigator.setHeaderHidden(True)
        self.pageNavigator.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

        #### CONST For QAction Performa ####
        self.perfSettings = {0: [self.cpuThreadAuto, self.cpuThreadUserSet],
                        1: [self.autoStartOff, self.autoStartOn]}

        #### INIT FIRST START ####
        self.initSaberPushButton()
        self.initTreePageNavigator()
        self.changePage("Foto Baru", 0)
        self.initUserSettings()

        #### SIGNAL AND SLOT for Page Navigator ####
        self.pageNavigator.clicked.connect(self.pageNavigatorClicked)

        #### SIGNAL AND SLOT FOR startVerifyFile
        self.timerUpdateVerifyTable.timeout.connect(self.forceUpdateTable)
        self.timerCheckVFIPC.timeout.connect(self.checkQueueVerifyFile)

        #### SIGNAL AND SLOT for QAction::Performance Settings ####
        self.cpuThreadAuto.triggered.connect(self.cpuSetBySystem)
        self.cpuThreadUserSet.triggered.connect(self.cpuSetByUser)

        #### SIGNAL AND SLOT for QAction::autoStart Settings #####
        self.autoStartOn.triggered.connect(self.enableAutoStart)
        self.autoStartOff.triggered.connect(self.disableAutoStart)

        #### SIGNAL AND SLOTS FOR TOP BAR PushButton ####
        self.addJob.clicked.connect(self.openAddJobWindow)
        self.deleteSelected.clicked.connect(self.deleteSelectedRow)
        self.cancelDeleteSelected.clicked.connect(self.cancelDelete)
        self.revealFile.clicked.connect(self.revealFileOnFE)
        self.reloadTable.clicked.connect(self.forceUpdateTable)
        self.startVerify.clicked.connect(self.startVerifyFile)

        #### SIGNAL & SLOTS FOR UNIVERSALTABLEVIEW ####
        self.universalTableView.clicked.connect(self.universalTableRowClicked)

    ##### INIT CODE - function #####
    def initTreePageNavigator(self):
        """prepare page navigator berbentuk tree view"""
        for (ortu, anakanak), (ikonOrtu, ikonAnakAnak) in zip(
            self.treeModelItem.items(), self.treeModelIcon.items()
        ):
            headTree = QStandardItem(ortu)
            headTree.setIcon(QIcon(ikonOrtu))
            self.pageNavRoot.appendRow([headTree])
            for anak, ikonAnak in zip(anakanak, ikonAnakAnak):
                anakOrtu = QStandardItem(anak)
                anakOrtu.setIcon(QIcon(ikonAnak))
                headTree.appendRow([anakOrtu])

    def initUserSettings(self):
        """Prepare pengaturan pengguna"""
        userThreadPref = self.userPersonalization.getUserConfig("perfSettings",0)
        autoStart = self.userPersonalization.getUserConfig("autoStart", 0)
        for key, qActList in self.perfSettings.items():
            for qAct in qActList:
                qAct.setChecked(False)

            if key == 0:
                qActList[userThreadPref].setChecked(True)
            elif key == 1:
                qActList[autoStart].setChecked(True)

        self.numWorkers = max(1, cpu_count()-2) if self.userPersonalization.getUserConfig("perfSettings",0) == 0 else self.userPersonalization.getUserConfig("perfSettings",1)

    def initSaberPushButton(self):
        """prepare tombol supaya bisa menyala saat dihover"""
        for key, listOfDir in self.saberPButton.items():
            key.installEventFilter(self.saberButtonFiler)
            key.setIcon(QIcon(listOfDir[0]))
            key.setIconSize(QSize(30,30))

    def changePage(self, pageTitle, page:Literal[0,1,2,3,4]):
        """Function for change current page (pageNavigator, tablemodel, and button)"""
        pageNavFocusIndex = self.treeModel.match(self.treeModel.index(0,0), Qt.ItemDataRole.DisplayRole,
                                                 pageTitle, 1, Qt.MatchFlag.MatchRecursive | Qt.MatchFlag.MatchExactly)
        if pageNavFocusIndex:
            targetIndex = pageNavFocusIndex[0]
            parent = targetIndex.parent()
            while parent.isValid():
                self.pageNavigator.expand(parent)
                parent = parent.parent()
            self.pageNavigator.expand(targetIndex)
            self.pageNavigator.setCurrentIndex(targetIndex)

        #### reset the sqlTableModel and universalTableView
        self.currentTableModel = page
        tableStruct = self.allTableModel[self.currentTableModel]
        self.universalTableView.setModel(None)
        self.sqlTableModel.clear()
        self.sqlTableModel.setTable(tableStruct.name)
        self.universalTableView.setModel(self.sqlTableModel)
        tableStruct.init_delegate()
        self.forceUpdateTable()

        for i, (header, colWidth) in enumerate(self.allTableHeader[self.currentTableModel].items()):
            self.sqlTableModel.setHeaderData(i, Qt.Orientation.Horizontal, header)
            self.universalTableView.setColumnWidth(i, colWidth)

        for targetButton, status in [(tableStruct.enabledButton, True), (tableStruct.disabledButton, False)]:
            for button in targetButton:
                button.setEnabled(status)

    def pageNavigatorClicked(self, index:QModelIndex):
        itemText = index.data()
        pageIndexConst = 0
        pageIndex = None
        for _, child in self.treeModelItem.items():
            if itemText in child:
                pageIndex = pageIndexConst + child.index(itemText)
            else:
                pageIndexConst += 3
        if pageIndex != None:
            self.changePage(itemText, pageIndex)

    def universalTableRowClicked(self, index):
        """Respons ketika pengguna menekan pada row spesifik"""
        self.currentRowClicked = index.row()
    
    def forceUpdateTable(self):
        """Paksa update SQLTable apapun yang sedang online"""
        hasil = self.sqlTableModel.select()
        if hasil == True:
            self.reloadTable.setText("Refresh Tabel\nSukses")
        else:
            self.reloadTable.setText("Refresh Tabel\nGagal")
        QTimer.singleShot(1000, self.forceUpdateTableStatusReset)

    def forceUpdateTableStatusReset(self):
        """reset status reload tabel jadi nama tombol itu lagi"""
        self.reloadTable.setText("Refresh\nTabel")

    ##### PRIVATE FUNCTION RELY ON QAction::cpuCore #####
    def cpuSetBySystem(self):
        """Jumlah CPU diset oleh sistem"""
        self.cpuThreadAuto.setChecked(False)
        self.userPersonalization.editUserConfig('perfSettings',0,0)
        self.userPersonalization.editUserConfig('perfSettings',1,0)
        self.initUserSettings()
        
    def cpuSetByUser(self):
        """Ketika pengguna mau set penggunaan CPUnya sendiri"""
        self.cpuThreadUserSet.setChecked(False)
        showInfo(self, "Peringatan Di Awal", "Pengaturan ini berpengaruh terhadap performa aplikasi dan stabilitas sistem Anda. Harap ubah dengan hati-hati!",
                 'info')
        cpuSetWindow = WM_.openWindow(CPUSettings, self.userPersonalization)
        cpuSetWindow.show()
        cpuSetWindow.doneAction.connect(self.initUserSettings)

    ##### PRIVATE FUNCTION RELY ON QAction::autoStart #####
    def enableAutoStart(self):
        """Menjalankan auto start"""
        self.autoStartOn.setChecked(False)
        self.startOnBoot.enableAutoStart()
        self.userPersonalization.editUserConfig('autoStart', 0, 1)
        self.initUserSettings()
    
    def disableAutoStart(self):
        """Matikan auto start"""
        self.autoStartOff.setChecked(False)
        self.startOnBoot.disableAutoStart()
        self.userPersonalization.editUserConfig('autoStart', 0, 0)
        self.initUserSettings()

    ##### PRIVATE FUNCTION RELY ON TOP LEFT QToolButton #####
    def deleteSelectedRow(self):
        """Saat pengguna menekan row dan memencet delete"""
        if self.currentRowClicked != None:
            jawaban = bringQuestion(self, "Konfirmasi", self.msgDeleteSelectedRow[self.currentTableModel],
                                    'question', 'yes', 'no')
            if jawaban == QMessageBox.Yes:
                if self.currentTableModel in (0,1):
                    currentFileDir = self.sqlTableModel.record(self.currentRowClicked).value("fileDir")
                    self.sqlDb.executeQuery(
                        querySQL=f"INSERT INTO photoCancelledTable(fileName, fileDir, fileExt) SELECT fileName, fileDir, fileExt FROM {self.allTableModel[self.currentTableModel].name} WHERE fileDir = ?",
                        params=[currentFileDir]
                    )
                    self.sqlDb.executeQuery(
                        querySQL=f"UPDATE photoCancelledTable SET dateDeleted = ? WHERE fileDir = ?",
                        params=[datetime.now().strftime("%d/%m/%Y %H:%M:%S"), currentFileDir]
                    )
                self.sqlTableModel.removeRow(self.currentRowClicked)
                self.sqlTableModel.submitAll()

            self.currentRowClicked = None
            self.universalTableView.clearSelection()
            self.universalTableView.clearFocus()
            self.sqlTableModel.select()

    def openAddJobWindow(self):
        """Membuka jendela Add Job Window dan menambahkan trigger doneAction"""
        _w = WM_.openWindow(PilihFileAtauFolder, self.sqlDb)
        _w.show()
        _w.doneAction.connect(self.closeAddJobWindow)

    def closeAddJobWindow(self):
        """Trigger doneActionnya untuk memindahkan data dan reset table seamlessly"""
        allQ = ["INSERT INTO fileJobTable(fileName, fileDir, fileExt) SELECT fileName, fileDir, fileExt FROM newFileTable",
                "DELETE FROM newFolderTable", "DELETE FROM newFileTable"]
        for i, query in enumerate(allQ):
            self.sqlDb.executeQuery(query)
            if i == 1:
                self.sqlTableModel.select()

    def cancelDelete(self):
        """Saat pengguna menekan row dan memencet cancel delete (file restored)"""
        if self.currentRowClicked != None:
            currentFileDir = self.sqlTableModel.record(self.currentRowClicked).value("fileDir")

            hasil = self.sqlDb.selectQuery(querySQL="SELECT fileDir FROM fileJobTable")
            allFileDir = {file[0] for file in hasil if os.path.isfile(file[0])}
            if currentFileDir not in allFileDir:
                self.sqlDb.executeQuery(
                    querySQL="INSERT INTO fileJobTable(fileName, fileDir, fileExt) SELECT fileName, fileDir, fileExt FROM photoCancelledTable WHERE fileDir = ?",
                    params=[currentFileDir]
                )
                showInfo(self, "Informasi: File Direstorasi",
                        f"File {os.path.basename(currentFileDir)} telah dipindahkan menuju tabel 'Foto Baru'!", 'info')

            else:
                showInfo(self, "Informasi: File Gagal Direstorasi",
                        f"File {os.path.basename(currentFileDir)} sudah ada pada tabel 'Foto Baru'. Tidak dipindahkan untuk mencegah duplikasi file.", 'warning')
                
            self.sqlDb.executeQuery(querySQL="DELETE FROM photoCancelledTable WHERE fileDir = ?", params=[currentFileDir])
            self.currentRowClicked = None
            self.universalTableView.clearSelection()
            self.universalTableView.clearFocus()
            self.sqlTableModel.select()

    def startVerifyFile(self):
        """Mulai proses verifikasi file secara asinkron"""
        if self.currentTableModel == 0:
            if self.verifyFileThreadStatus == 0:
                self.sqlDb.executeQuery(
                    querySQL="INSERT INTO verifyFileTable(fileName, fileDir, fileExt) SELECT fileName, fileDir, fileExt FROM fileJobTable"
                )
                self.sqlDb.executeQuery(
                    querySQL="DELETE FROM fileJobTable"
                )
                hasil = self.sqlDb.selectQuery(
                    querySQL="SELECT fileDir FROM verifyFileTable WHERE fileFormat = '-'"
                )
                allFileToProcess = [file[0] for file in hasil
                                    if os.path.isfile(file[0])]
                if len(allFileToProcess) > 0:
                    self.verifyFileCount = len(allFileToProcess)
                    self.pool = Pool(processes=self.numWorkers)
                    self.verifyFileThreadStatus = 1
                    for file in allFileToProcess:
                        self.pool.apply_async(backend.verifyImageFile,
                                            args=(file,), callback=self.verifyFileIPC.put)
                    self.timerCheckVFIPC.start(100)
                    self.timerUpdateVerifyTable.start(1000)

                else:
                    showInfo(self, "Oops.. Ada Yang Tidak Beres",
                            "Tidak ada file baru yang harus diverifikasi!", 'info')
            
            else:
                showInfo(self, "Worker Thread Warning",
                         "Verifikasi File Foto sedang berlangsung. Tidak bisa menjalankan proses asinkron lebih dari 2!",
                         'warning')

    def checkQueueVerifyFile(self):
        """Sebuah fungsi untuk mengecek IPC dari hasil Asinkronuous verifyFile"""
        while not self.verifyFileIPC.empty():
            hasil = self.verifyFileIPC.get()
            self._bufferVerifikasiFile.append(hasil)
            self.doneVerifyCount += 1
            if len(self._bufferVerifikasiFile) >= 5:
                self.sqlDb.executeQuery(
                    querySQL="UPDATE verifyFileTable SET fileExt = ?, fileFormat = ?, isSupported = ?, isNotCorrupted = ?, isNotVirus = ?, fileSize0 = ? WHERE fileName = ?",
                    params=self._bufferVerifikasiFile, isMultipleParams=True
                )
                self._bufferVerifikasiFile.clear()

            self.startVerify.setText(f"Memproses:\n{self.doneVerifyCount}/{self.verifyFileCount} File")
            
            if self.doneVerifyCount == self.verifyFileCount:
                self.timerCheckVFIPC.stop()
                self.timerUpdateVerifyTable.stop()
                if len(self._bufferVerifikasiFile) > 0:
                    self.sqlDb.executeQuery(
                    querySQL="UPDATE verifyFileTable SET fileExt = ?, fileFormat = ?, isSupported = ?, isNotCorrupted = ?, isNotVirus = ?, fileSize0 = ? WHERE fileName = ?",
                    params=self._bufferVerifikasiFile, isMultipleParams=True
                    )
                    self._bufferVerifikasiFile.clear()
                self.startVerify.setText("Verifikasi\nFile")
                self.doneVerifyCount = 0
                self.verifyFileThreadStatus = 0 
                self.forceUpdateTable()

    def revealFileOnFE(self):
        """Saat pengguna menekan row dan memencet reveal file 
        'JADI GWEJ LUPA FILE APA SIH YANG GWEH MASUKIN?'"""
        if self.currentRowClicked != None:
            currentRowRecord = self.sqlTableModel.record(self.currentRowClicked)
            fileDir = currentRowRecord.value("fileDir")
            if not os.path.isfile(fileDir):
                showInfo(self, "Terjadi Kesalahan",
                         f"Ooops! file yang kamu pilih:[{fileDir}] tidak ada eksistensinya. Kami membantu Anda menyelesaikannya dengan menghapusnya dari list.",
                         'error')
                self.sqlTableModel.removeRow(self.currentRowClicked)
                self.sqlTableModel.submitAll()

            else:
                if sys.platform == "win32":
                    subprocess.run(["explorer", "/select,", f"{fileDir}"])

                else:
                    try:
                        subprocess.run(["xdg-open", os.path.dirname(fileDir)])

                    except Exception:
                        showInfo(self, "Oops... Ada Yang Tidak Beres",
                                 f"100% BUKAN kesalahan Anda... Tetapi sepertinya platform Anda/API belum mendukung hal ini. Catat detail ini dan hubungi pengembang:\nCommand: 'xdg-open' status FAILED\nOS: 'Unknown' defined as '{sys.platform}'",
                                 'error')
            self.currentRowClicked = None
            self.universalTableView.clearSelection()
            self.universalTableView.clearFocus()

    ##### DELEGATE TABLE INIT (FOR GUI) ######
    ##### PUT AT THE BOTTOM BECAUSE OF IT'S CRITICAL WASN'T VERY MATTER #####
    #####---------------------------------------------------------------#####
    ##### PAGE 1: fileJobTable #####
    def fileJobTableDelegateInit(self):
        """Table Delegate Init untuk halaman 'Foto Baru'"""
        delegateTableLeftAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignLeft, self.universalTableView)
        delegateTableCenterAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignCenter, self.universalTableView)
        for i in range(0, 2):
            self.universalTableView.setItemDelegateForColumn(i, delegateTableCenterAlign)
        self.universalTableView.setItemDelegateForColumn(2, delegateTableLeftAlign)
        self.universalTableView.setItemDelegateForColumn(3, delegateTableCenterAlign)

    ##### PAGE 2: verifyFileTable #####
    def verifyFileTableDelegateInit(self):
        """Table Delegate Init untuk tabel 'Siap Diproses'"""
        for i in range(0,2):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)
        self.universalTableView.setItemDelegateForColumn(2, self.delegateTableLeftAlign)
        for i in range(3,5):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)
        for i in range(5,8):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableInterpret)
        self.universalTableView.setItemDelegateForColumn(8, self.delegateFileSize)

    ##### PAGE 3: compressedFileTable #####
    def compressedFileTableDelegateInit(self):
        """Table Delegate Init untuk tabel 'Selesai Diproses'"""
        for i in range(0, 2):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)
        self.universalTableView.setItemDelegateForColumn(2, self.delegateTableLeftAlign)
        for i in range(3,5):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)
        for i in range(5,8):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableInterpret)
        for i in range(8,11):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateFileSize)  
        for i in range(11,13):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)

    ##### PAGE 4: photoRejectedTable #####
    def photoRejectedTableDelegateInit(self):
        """Table Delegate Init untuk tabel 'Foto Ditolak'"""
        for i in range(0,2):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)
        self.universalTableView.setItemDelegateForColumn(2, self.delegateTableLeftAlign)
        for i in range(3,5):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)
        for i in range(5,8):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableInterpret)
        self.universalTableView.setItemDelegateForColumn(8, self.delegateFileSize)
        self.universalTableView.setItemDelegateForColumn(9, self.delegateTableCenterAlign)

    ##### PAGE 5: photoCancelledTable #####
    def photoCancelledTableDelegateInit(self):
        """Table Delegate Init untuk tabel 'Batal Diproses'"""
        for i in range(0,2):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)
        self.universalTableView.setItemDelegateForColumn(2, self.delegateTableLeftAlign)
        for i in range(3,5):
            self.universalTableView.setItemDelegateForColumn(i, self.delegateTableCenterAlign)

#### <!--------------------------- Dynamic Button Window ------------------------------!>
#### Window buat QToolButton yang kalau tombolnya dihover, tombolnya nyala
class PilihFileAtauFolder(QMainWindow, selectNewFile.Ui_MainWindow):
    """Is accessible from page 0 only"""
    doneAction = Signal()
    def __init__(self, dbPassThrough:backend.QNativeFileDatabase):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Pilih File atau Folder")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        #### CONST FOR Icon ####
        self.fileAndFolderIcon = {":/nf_newFileFolder": [self.newPhotoFile, self.newFolder], 
                                  ":/nf_deleteSelected": [self.deletePhotoFile, self.deleteFolder], 
                                  ":/nf_resetTable": [self.resetFolderTable, self.resetPhotoTable]}
        self.appIcon = ':/ai_appDefaultIcon'

        #### CONST For File Button Navigation
        self.fileButton = {
            0: [self.newPhotoFile, self.deletePhotoFile, self.resetPhotoTable],
            1: [self.newFolder, self.deleteFolder, self.resetFolderTable]
        }

        #### CONST for FileType ####
        self.validExt = {".jpg", ".jpeg", ".png"}

        #### CONST FOR QSqlTableModel ####
        self.sqlDb = dbPassThrough
        self.photoTableModel = QSqlTableModel(self, db=self.sqlDb.fileDatabase)
        self.photoTableModel.setTable("newFileTable")
        self.photoTableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.photoTableHeader = {"No.": 30, "Nama File": 90, "Lokasi Simpan": 250, "Ekstensi File": 80}
        self.photoTableModel.select()
        self.photoTableView.setModel(self.photoTableModel)

        self.folderTableModel = QSqlTableModel(self, db=self.sqlDb.fileDatabase)
        self.folderTableModel.setTable("newFolderTable")
        self.folderTableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.folderTableHeader = {"No.":30, "Nama Folder": 90, "Lokasi Simpan": 250}
        self.folderTableModel.select()
        self.folderTableView.setModel(self.folderTableModel)

        #### CONST for Table View ####
        self.allTableView = {
            self.photoTableView: self.photoTableModel,
            self.folderTableView: self.folderTableModel
        }
        self.photoTableCurrentRowClicked = None
        self.folderTableCurrentRowClicked = None

        #### CONST for Simpan dan Tutup Animation ####
        self.saveCloseTimerAnimation = QTimer(self)
        self.countPoint = 1

        #### CONST untuk secondary thread buat fetch file
        self.pConn, self.cConn = Pipe()
        self.fetchFileMP = None
        self.fetchFileMPTimer = QTimer(self)

        #### Drag And Drop Filter ####
        self.photoTableDropFilter = TableViewDragnDropFilter(self.photoTableView, self.photoTableModel, self.sqlDb, 'File', self)
        self.photoTableView.installEventFilter(self.photoTableDropFilter)
        self.folderTableDropFilter = TableViewDragnDropFilter(self.folderTableView, self.folderTableModel, self.sqlDb, 'Folder', self)
        self.folderTableView.installEventFilter(self.folderTableDropFilter)

        #### Init Window ####
        self.initIcon()
        self.initButton()
        self.initTableView()

        #### SIGNAL & SLOTS FOR PHOTO OPTION ####
        self.photoTableView.clicked.connect(self.photoTableRowClicked)
        self.fileOption.clicked.connect(self.fileOptionTriggered)
        self.newPhotoFile.clicked.connect(self.chooseFileFoto)
        self.deletePhotoFile.clicked.connect(self.deletePhoto)
        self.resetPhotoTable.clicked.connect(self.functResetPhotoTabel)

        #### SIGNAL & SLOTS FOR FOLDER OPTION ####
        self.folderTableView.clicked.connect(self.folderTableRowClicked)
        self.folderOption.clicked.connect(self.folderOptionTriggered)
        self.newFolder.clicked.connect(self.chooseFolder)
        self.deleteFolder.clicked.connect(self.functDeleteFolder)
        self.resetFolderTable.clicked.connect(self.functResetFolderTable)

        #### SIGNAL & SLOTS FOR SECONDARY THREAD, ANIMATION, CLOSE AND SAVE BUTTON ####
        self.fetchFileMPTimer.timeout.connect(self.processFileQueue)
        self.saveCloseTimerAnimation.timeout.connect(self.simpanDanTutupAnim)
        self.simpanDanTutup.clicked.connect(self.functSimpanDanTutup)
        self.batal.clicked.connect(self.tutupJendela)

    def initTableView(self):
        """Persiapkan table view dengan menyetel beberapa hal dan memastikan tabel dalam posisi off"""
        delegateTableCenterAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignCenter, self)
        delegateTableLeftAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignLeft, self)
        for i in range(0,2):
            self.folderTableView.setItemDelegateForColumn(i, delegateTableCenterAlign)
            self.photoTableView.setItemDelegateForColumn(i, delegateTableCenterAlign)
        self.photoTableView.setItemDelegateForColumn(3, delegateTableCenterAlign)

        for tableView, tableModel in self.allTableView.items():
            for i, (colHead, colWidth) in enumerate(self.photoTableHeader.items() 
                                                    if tableView==self.photoTableView 
                                                    else self.folderTableHeader.items()):
                tableModel.setHeaderData(i, Qt.Orientation.Horizontal, colHead)
                tableView.setColumnWidth(i, colWidth)
                tableView.setItemDelegateForColumn(2, delegateTableLeftAlign)
                tableView.verticalHeader().setVisible(False)
                tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
                tableView.setAcceptDrops(True)
                tableView.setDisabled(True)

    def initButton(self):
        """Pastikan semua tombol untuk tabel dalam keadaan mati"""
        for _, toolButtons in self.fileButton.items():
            for toolButton in toolButtons:
                toolButton.setDisabled(True)
        
    def initIcon(self):
        """Initialize the button icon"""
        self.setWindowIcon(QIcon(self.appIcon))
        for file, buttons in self.fileAndFolderIcon.items():
            for button in buttons:
                button.setIcon(QIcon(file))
    
    def fileOptionTriggered(self):
        """Menyalakan tombol spesifik mode foto"""
        if self.fileOption.checkState() == Qt.CheckState.Checked:
            self.fileOption.setCheckState(Qt.CheckState.Checked)
            self.photoTableView.setEnabled(True)

            for identifier, toolButtons in self.fileButton.items():
                if identifier == 0:
                    for button in toolButtons:
                        button.setEnabled(True)
        else:
            self.fileOption.setCheckState(Qt.CheckState.Unchecked)
            self.photoTableView.setEnabled(False)
            for identifier, toolButtons in self.fileButton.items():
                if identifier == 0:
                    for button in toolButtons:
                        button.setEnabled(False)

    def chooseFileFoto(self):
        """Respons ketika pengguna menekan tombol newPhotoFile"""
        hasil1 = self.sqlDb.selectQuery(querySQL="SELECT fileDir FROM newFileTable")
        hasil2 = self.sqlDb.selectQuery(querySQL="SELECT fileDir FROM fileJobTable")

        existingFiles = {file[0] for file in hasil1} | {file[0] for file in hasil2}
        userChoosedFile = chooseFiles(self, judul="Pilih File Foto")

        if userChoosedFile:
            dataToInsert = []
            for file in userChoosedFile:
                fileExt = os.path.splitext(file)[1].lower()
                if fileExt not in self.validExt:
                    continue
                fileNormPath = os.path.normpath(file)
                if fileNormPath in existingFiles:
                    continue
                if not os.path.isfile(file):
                    continue
                dataToInsert.append((os.path.basename(file), fileNormPath, fileExt))
                existingFiles.add(fileNormPath)

            if dataToInsert:
                self.sqlDb.executeQuery(
                    querySQL="INSERT INTO newFileTable(fileName, fileDir, fileExt) VALUES (?,?,?)",
                    params=dataToInsert, isMultipleParams=True
                )
                self.photoTableModel.select()

    def photoTableRowClicked(self, index):
        """Respons ketika pengguna menekan pada isian tabel foto"""
        self.photoTableCurrentRowClicked = index.row()

    def deletePhoto(self):
        """Respons saat pengguna menekan isian tabel foto, dan menekan hapus"""
        if self.photoTableCurrentRowClicked != None:
            jawaban = bringQuestion(self, "Konfirmasi", "Anda yakin untuk menghapus kolom terpilih?",
                                    "question", "yes", "no")
            if jawaban == QMessageBox.Yes:
                self.photoTableModel.removeRow(self.photoTableCurrentRowClicked)
                self.photoTableModel.submitAll()
            
            self.photoTableCurrentRowClicked = None
            self.photoTableView.clearSelection()
            self.photoTableView.clearFocus()

        else:
            showInfo(self, "Uhm... Sepertinya Ada Yang Terlewat", "Anda belum memilih baris apapun!", "info")

    def functResetPhotoTabel(self):
        """Respons saat pengguna menekan tombol reset gambar tabel (danger zone)"""
        if self.photoTableModel.rowCount() > 0:
            jawaban = bringQuestion(self, "AREA BERBAHAYA", "Anda yakin untuk menghapus seluruh kolom terisi?",
                                    "warning", "yes", "no")
            if jawaban == QMessageBox.Yes:
                self.sqlDb.executeQuery(
                    querySQL="DELETE FROM newFileTable"
                )
                self.photoTableModel.select()
    
    def folderOptionTriggered(self):
        """Menyalakan tombol spesifik mode file"""
        if self.folderOption.checkState() == Qt.CheckState.Checked:
            self.folderOption.setCheckState(Qt.CheckState.Checked)
            self.folderTableView.setEnabled(True)

            for identifier, toolButtons in self.fileButton.items():
                if identifier == 1:
                    for button in toolButtons:
                        button.setEnabled(True)

        else:
            self.folderOption.setCheckState(Qt.CheckState.Unchecked)
            self.folderTableView.setEnabled(False)
            for identifier, toolButtons in self.fileButton.items():
                if identifier == 1:
                    for button in toolButtons:
                        button.setEnabled(False)

    def chooseFolder(self):
        """Respons ketika pengguna menekan tombol newFolder"""
        hasil = self.sqlDb.selectQuery(querySQL="SELECT folderPath FROM newFolderTable")
        folderSudahAda = {folder[0] for folder in hasil}
        userChoosedFolder = chooseFolder(self, judul="Pilih Folder Foto")

        if userChoosedFolder:
            userChoosedFolderNormPath = os.path.normpath(userChoosedFolder)
            if userChoosedFolderNormPath not in folderSudahAda and os.path.isdir(userChoosedFolderNormPath):
                self.sqlDb.executeQuery(
                    querySQL="INSERT INTO newFolderTable(folderName, folderPath) VALUES (?,?)",
                    params=[os.path.basename(userChoosedFolderNormPath),userChoosedFolderNormPath]
                )
            self.folderTableModel.select()
    
    def folderTableRowClicked(self, index):
        """Respons ketika pengguna menekan pada isian tabel foto"""
        self.folderTableCurrentRowClicked = index.row()

    def functDeleteFolder(self):
        """Respons saat pengguna menekan tombol hapus folder (folderTableCurrentRow is Exists)"""
        if self.folderTableCurrentRowClicked != None:
            jawaban = bringQuestion(self, "Konfirmasi", "Anda yakin untuk menghapus kolom terpilih?",
                                    "question", "yes", "no")
            if jawaban == QMessageBox.Yes:
                self.folderTableModel.removeRow(self.folderTableCurrentRowClicked)
                self.folderTableModel.submitAll()

            self.folderTableCurrentRowClicked = None
            self.folderTableView.clearSelection()
            self.folderTableView.clearFocus()

        else:
            showInfo(self, "Uhm... Sepertinya Ada Yang Terlewat", "Anda belum memilih baris apapun!", "info")

    def functResetFolderTable(self):
        """Respons saat pengguna menekan tombol reset folder tabel"""
        if self.folderTableModel.rowCount() > 0:
            jawaban = bringQuestion(self, "AREA BERBAHAYA", "Anda yakin untuk menghapus seluruh kolom terisi?",
                                    "warning", "yes", "no")
            if jawaban == QMessageBox.Yes:
                self.sqlDb.executeQuery(
                    querySQL="DELETE FROM newFolderTable"
                )
                self.folderTableModel.select()

    def functSimpanDanTutup(self):
        """Menangani permintaan penyimpanan data pengguna"""
        for _, toolButtons in self.fileButton.items():
            for toolButton in toolButtons:
                toolButton.setDisabled(True)

        self.folderOption.setDisabled(True)
        self.fileOption.setDisabled(True)
        self.batal.setDisabled(True)
        self.simpanDanTutup.setDisabled(True)

        if self.folderTableModel.rowCount() > 0:
            self.saveCloseTimerAnimation.start(250)
            hasil = self.sqlDb.selectQuery(
                querySQL="SELECT folderPath FROM newFolderTable"
            )
            allNeedToProcess = backend.filterRedundantPath([file[0] for (file) in hasil])
            self.fetchFileMP = Process(
                target=backend.returnAllFileFromPath,
                args=(allNeedToProcess, self.cConn)
            )
            self.fetchFileMP.start()
            self.fetchFileMPTimer.start(100)

        elif self.photoTableModel.rowCount() > 0:
            self.closeWindowEmitSignal()

        else:
            showInfo(self, "Tidak Ada Data Baru!", "Anda tidak memasukkan data baru apapun!",
                    'info')
            WM_.closeWindows(PilihFileAtauFolder)

    def processFileQueue(self):
        """Proses Queue yang datang dari subprocess independen"""
        if self.pConn.poll():
            allFiles = self.pConn.recv() 
            self.fetchFileMPTimer.stop()

            if self.fetchFileMP.is_alive():
                self.fetchFileMP.kill()

            if len(allFiles) > 0:
                hasil1 = self.sqlDb.selectQuery(querySQL="SELECT fileDir FROM newFileTable")
                hasil2 = self.sqlDb.selectQuery(querySQL="SELECT fileDir FROM fileJobTable")
                existingFiles = {file[0] for file in hasil1} | {file[0] for file in hasil2}
                dataToInsert = []

                for file in allFiles:
                    fileExt = os.path.splitext(file)[1].lower()
                    if fileExt not in self.validExt:
                        continue
                    fileNormPath = os.path.normpath(file)
                    if fileNormPath in existingFiles:
                        continue
                    if not os.path.isfile(file):
                        continue
                    dataToInsert.append((os.path.basename(file), fileNormPath, fileExt))
                    existingFiles.add(fileNormPath)
                
                if dataToInsert:
                    self.sqlDb.executeQuery(
                        querySQL="INSERT INTO newFileTable(fileName, fileDir, fileExt) VALUES (?,?,?)",
                        params=dataToInsert, isMultipleParams=True
                    )
            self.closeWindowEmitSignal()

    def closeWindowEmitSignal(self):
        """Tutup jendela ini dan diawali dengan mengemit sinyal kepada mainthread"""
        self.saveCloseTimerAnimation.stop()
        self.doneAction.emit()
        WM_.closeWindow(PilihFileAtauFolder)

    def simpanDanTutupAnim(self):
        """Animasi tombol '...' '..' '.' cepat"""
        self.simpanDanTutup.setText("Memuat" + "."*self.countPoint)
        if self.countPoint <= 3:
            self.countPoint += 1
        else:
            self.countPoint = 1

    def tutupJendela(self):
        """Fungsi resmi WindowManager Instance untuk menutup jendela"""
        jawaban = bringQuestion(self, "Konfirmasi Untuk Keluar", "Apakah Anda yakin untuk keluar dari jendela ini? Segala data yang tidak tersimpan akan hilang!",
                                'question', 'yes', 'no')
        if jawaban == QMessageBox.Yes:
            self.sqlDb.executeQuery(
                querySQL="DELETE FROM newFolderTable"
            )
            self.sqlDb.executeQuery(
                querySQL="DELETE FROM newFileTable"
            )
            WM_.closeWindow(PilihFileAtauFolder)

    def closeEvent(self, event):
        """Cegah penutupan aplikasi tanpa WindowManager Instance"""
        event.ignore()
        self.tutupJendela()

class PengaturanKompresi(QMainWindow, CompressSettings.Ui_MainWindow):
    def __init__(self, UPPassThrough:backend.UserPersonalization):
        super().__init__()
        self.setupUi(self)
        self.userPersonalization = UPPassThrough

        #### Window Const
        self.mpRegex = QRegularExpressionValidator(QRegularExpression("^\d+Cm$"))
        self.allFillAble = [self.megaPixel, self.photoQuality]
    
    def initGUI(self):
        self.saveLocation.setReadOnly(True)
        self.megaPixel.setEditable(True)
        self.megaPixel.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.megaPixel.lineEdit().setValidator(self.mpRegex)

#### <!---------------------- MENU BAR WINDOW ---------------------------!> ####
#### Window yang bisa diakses lewat menu bar ####
class CPUSettings(QMainWindow, PerfSettingCPU.Ui_MainWindow):
    doneAction = Signal()
    def __init__(self, uPInstancePassThrought:backend.UserPersonalization):
        super().__init__()
        self.setupUi(self)

        #### CONST for Window
        self.appIcon = ':/ai_appDefaultIcon'
        self.userPersonalization = uPInstancePassThrought
        self.maxCore = cpu_count()

        #### Init the first run
        self.initGUI()

        #### Signal and Slots
        self.userDefiniedCPU.valueChanged.connect(self.onUserChangeCPU)
        self.simpan.clicked.connect(self.onSettingsSaved)
        self.batal.clicked.connect(self.closeWindow)

    def initGUI(self):
        """Mempersiapkan komponen GUI (Max CPU Settings, dll) agar UI Siap Dipakai"""
        self.setWindowTitle("Pengaturan CPU")
        self.setWindowIcon(QIcon(self.appIcon))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.cpuAvailable.setReadOnly(True)
        self.cpuAvailable.setText(f"{self.maxCore} Tersedia")
        self.userDefiniedCPU.setMaximum(self.maxCore)
        self.userDefiniedCPU.setMinimum(1)
        self.userDefiniedCPU.setSingleStep(1)
        self.userDefiniedCPU.setValue(max(1, self.maxCore-2))

    def onUserChangeCPU(self, val):
        """Respons khusus ketika user mengubah jumlah CPU Mutlak yang digunakan di range yang diluar nalar"""
        if val >= self.maxCore:
            showInfo(self, "Pengaturan Tidak Valid",
                     "Maaf, kami tidak diizinkan untuk memakai seluruh Core CPU perangkat Anda untuk mencegah instabilitas sistem! Perangkat Anda membutuhkan minimal 1 Core untuk tetap berfungsi secara stabil.",
                     'warning')
            self.userDefiniedCPU.setValue(max(1, self.maxCore-1))

        elif val <= 2:
            jawaban = bringQuestion(self, "Menggunakan CPU Minimum",
                                    f"Anda yakin untuk memakai hanya {val} dari {self.maxCore} jumlah CPU yang tersedia? Performa aplikasi (seperti ketika melakukan verifikasi file/kompresi) mungkin menurun. Jika perangkat Anda memiliki core yang terbatas, maka ini bukan masalah.",
                                    'question', 'yes', 'no')
            if jawaban != QMessageBox.Yes:
                self.userDefiniedCPU.setValue(max(1, val+1))

    def onSettingsSaved(self):
        """Simpan pengaturan yang dibuat oleh pengguna"""
        self.userDefiniedCPU.setReadOnly(True)
        self.userPersonalization.editUserConfig('perfSettings', 0, 1)
        self.userPersonalization.editUserConfig('perfSettings', 1, self.userDefiniedCPU.value())
        self.doneAction.emit()
        self.closeWindow(True)

    def closeWindow(self, withOutQuestioning=False):
        """Tutup jendela, dengan flag withOutQuestioning buat (ignore question)"""
        if withOutQuestioning:
            self.closeWindowAction()

        else:
            jawaban = bringQuestion(self, "Konfirmasi Tutup Jendela",
                                    "Anda yakin ingin menutup jendela ini? Segala data yang tidak tersimpan akan hilang.",
                                    'question', 'yes', 'no')
            if jawaban == QMessageBox.Yes:
                self.closeWindowAction()

    def closeWindowAction(self):
        """Fungsi untuk menutup jendela CPUSettings melalui WindowManager"""
        WM_.closeWindow(CPUSettings)

    def closeEvent(self, event):
        """Mencegah penutupan tidak disengaja melalui tombol silang jendela"""
        self.closeWindow()
        event.ignore()

######### Window Class GUI #########
class JendelaUtama(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kompres Gambar")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.stackedWidget.setCurrentIndex(0)

        ######### Const Global ##########
        self.allPages = {0: [self.stepOneNumber, self.stepOneTitle],
                         1: [self.stepTwoNumber, self.stepTwoTitle],
                         2: [self.stepThreeNumber, self.stepThreeTitle],
                         3: [self.stepFourNumber, self.stepFourTitle]}
        appMainDir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        self.assetFolder = os.path.join(appMainDir, "Assets")
        self.sqlDatabase = backend.QNativeFileDatabase()
        self.nowExitAble = True
        self.numWorkers = max(1, cpu_count()-2)

        ######### INIT Code ##########
        self.initGUI()

        ######### Signal & Slots #########
        allPageSwitcher = list(self.allPages.keys())
        for key in allPageSwitcher:
            for n in range(len(self.allPages[key])):
                button = self.allPages[key][n]
                button.clicked.connect(self.pageSwitcher)

        ######### Variabel Halaman Pertama #########
        self.fileMode = 0 #### 1 = folder | 2 = file ####
        self.folderPath = None
        """Mode folder 1, Mode file 2"""
        self.pageOneInteractable = {
            1: [self.folderBerisiFile, self.pilihFolderFile],
            2: [self.fileTable, self.tambahFile, self.hapusFile, self.resetTable]
        }
        self.pageOneOpsi = [self.opsiFolder, self.opsiFile]

        self.fileTableModel = QSqlTableModel(self, db=self.sqlDatabase.fileDatabase)
        self.fileTableModel.setTable("fileTable")
        self.fileTableModelHeader = ["id", "Nama File", "Lokasi File"]
        for i, item in enumerate(self.fileTableModelHeader):
            self.fileTableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, item
        )
        self.fileTableModel.setEditStrategy(
            QSqlTableModel.EditStrategy.OnManualSubmit
        )
        self.fileTableModel.select()

        self.currentRowClicked = None
        self.tableDropFilter = NotImplemented
        self.fileTable.installEventFilter(self.tableDropFilter)

        ######## Signal & Slots Halaman Pertama ########
        self.firstPageGUI()
        self.fileTable.clicked.connect(self.onRowClicked)
        self.opsiFolder.clicked.connect(self.firstPageOpsiFolder)
        self.opsiFile.clicked.connect(self.firstPageOpsiFile)
        self.pilihFolderFile.clicked.connect(self.pilihFolderFoto)
        self.tambahFile.clicked.connect(self.pilihFileFoto)
        self.hapusFile.clicked.connect(self.hapusFileFoto)
        self.resetTable.clicked.connect(self.resetTableData)
        self.pageOneLanjut.clicked.connect(self.continuePageOneVerify)

        ######## Variabel Halaman Kedua #########
        self.tabelVerifikasiModel = QSqlTableModel(self, db=self.sqlDatabase.fileDatabase)
        self.tabelVerifikasiModel.setTable("fileVerify")
        self.verifyTableModelHeader = ["id", "Nama", "Ekstensi File", "Format File", "Ukuran File", "File Didukung", "Integritas File", "File Aman", "Path File"]
        for i, item in enumerate(self.verifyTableModelHeader):
            self.tabelVerifikasiModel.setHeaderData(
                i, Qt.Orientation.Horizontal, item
            )
        self.tabelVerifikasiModel.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)

        self._bufferVerifikasiModel = []
        self.pConn = None
        self.cConn = None
        self.p1 = None
        self.t1 = QTimer(self) # read file from folder
        self.t2 = QTimer(self) # verify file
        self.t3 = QTimer(self) # update table auto
        self.verifyFileQueue = None
        self.fileCount = 0
        self.doneVerify = 0
        self.pool = None

        ######## Signal & Slot Halaman Kedua #########
        self.startVerify.clicked.connect(self.verifyFile)
        self.pageTwoLanjut.clicked.connect(self.continuePageTwo)
        self.t1.timeout.connect(self.getAllFile)
        self.t2.timeout.connect(self.checkQueueVerifyFile)
        self.t3.timeout.connect(self.updateVerifyTable)
        self.reloadVerifyTable.clicked.connect(self.updateVerifyTable)

        ######## Variabel Halaman Ketiga ##########
        self.pageThreeInteractable = [self.imgCompress, self.imgMpx,
                                      self.pilihFolder, self.hapusFIleAsli,
                                      self.pageThreeNext]
        self.qualityTip = []
        self.compressSummary = []
        self.allFilePathCategory = []
        self.allFileFormatCategory = []
        self.allVerifiedFilePath = []
        self.saveDir = None

        ######## Signal & SLot Halaman Ketiga #######
        self.imgMpx.currentIndexChanged.connect(self.megaPixelChanged)
        self.imgMpx.currentIndexChanged.connect(self.ringkasanUpdater)
        self.imgCompress.valueChanged.connect(self.qualityChanged)
        self.imgCompress.valueChanged.connect(self.ringkasanUpdater)
        self.pilihFolder.clicked.connect(self.chooseSaveDir)
        self.dirTujuan.textChanged.connect(self.ringkasanUpdater)
        self.hapusFIleAsli.clicked.connect(self.deleteOriginalFile)
        self.hapusFIleAsli.checkStateChanged.connect(self.ringkasanUpdater)
        self.pageThreeNext.clicked.connect(self.continuePageThreeVerify)

        ####### Variabel Halaman Keempat ########
        self._bufferCompressionProgress = []
        self.preferredMaxPix = 0
        self.preferredQuality = 0
        self.compressionPenghematan:float = 0.00
        self.deleteOriFile = False
        self.doneCompress = 0

        self.fileCompressionTableModel = QSqlTableModel(self, db=self.sqlDatabase.fileDatabase)
        self.fileCompressionTableModel.setTable("fileProcess")
        self.compressTableModelHeader = ["id", "Nama File", "Status", "Size Awal", "Size Akhir", "Dihemat", "Simpan Di", "Hapus"]
        for i, item in enumerate(self.compressTableModelHeader):
            self.fileCompressionTableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, item
            )
        self.fileCompressionTableModel.setEditStrategy(
            QSqlTableModel.EditStrategy.OnManualSubmit
        )

        self.t4 = QTimer(self) # check compression progress
        self.t5 = QTimer(self) # update table
        self.compressTask = None
        self.compressTaskComms = Queue()
        self.fileToCompress = None

        ####### Signal & Slot Halaman Keempat ######
        self.t4.timeout.connect(self.checkCompressProgress)
        self.t5.timeout.connect(self.updateTable)
        self.startCompression.clicked.connect(self.compressFotoParalell)
        self.refreshCompressTable.clicked.connect(self.updateTable)

    def initGUI(self):
        """First boot, hanya opsi pertama yang muncul"""
        self.setWindowIcon(
            QIcon(
                os.path.join(self.assetFolder, "icon.png")
            )
        )
        self.stackedWidget.setCurrentIndex(0)
        for key, pushButtonList in self.allPages.items():
            if key > 0:
                for pushButton in pushButtonList:
                    pushButton.setDisabled(True)

    def pageSwitcher(self):
        """Page Switcher supaya opsi di atas (nomor & title) bisa buat geser halaman"""
        senderButton = self.sender()
        for key, pushButtonList in self.allPages.items():
            if senderButton in pushButtonList:
                self.stackedWidget.setCurrentIndex(key)

    ######## First Page Only #########
    def firstPageGUI(self):
        """GUI Halaman pertama ketika dibuka"""
        for _, qtObjectList in self.pageOneInteractable.items():
            for qtObject in qtObjectList:
                qtObject.setDisabled(True)
        self.folderBerisiFile.setReadOnly(True)

    def firstPageOpsiFolder(self):
        """Simplenya ini mode folder"""
        for key, qtObjectList in self.pageOneInteractable.items():
            if key == 1:
                for qtObject in qtObjectList:
                    qtObject.setEnabled(True)

            elif key == 2:
                for qtObject in qtObjectList:
                    qtObject.setDisabled(True)
        self.fileMode = 1

    def pilihFolderFoto(self):
        """User pilih folder yang isinya foto"""
        folderFoto = chooseFolder(self, "Pilih Folder Foto Anda!")
        if folderFoto != None:
            self.folderPath = folderFoto
            self.folderBerisiFile.setText(self.folderPath)

        else:
            showInfo(self, "Perhatian",
                     "Anda belum memilih folder apapun!", "info")

    def firstPageOpsiFile(self):
        """Simplenya ini mode table"""
        for key, qtObjectList in self.pageOneInteractable.items():
            if key == 1:
                for qtObject in qtObjectList:
                    qtObject.setEnabled(False)

            elif key == 2:
                for qtObject in qtObjectList:
                    qtObject.setEnabled(True)

        if not self.fileTable.model():
            self.fileTable.setModel(self.fileTableModel)
            self.fileTable.setItemDelegateForColumn(1, 
                                                    TableAlignDelegate(Qt.AlignmentFlag.AlignCenter, self.fileTable)
                                                    )
            self.fileTable.setItemDelegateForColumn(2, 
                                                    TableAlignDelegate(Qt.AlignmentFlag.AlignLeft, self.fileTable)
                                                    )
            self.fileTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.fileTable.hideColumn(0)
            self.fileTable.setAcceptDrops(True)

        self.fileMode = 2

    def onRowClicked(self, index):
        """Respons ketika user klik pada row table, hendak menghapus"""
        self.currentRowClicked = index.row()

    def pilihFileFoto(self):
        """Ketika user mau pakai fitur pilih foto satu persatu alih-alih drag and drop"""
        hasil = self.sqlDatabase.selectQuery(
            querySQL="SELECT fileDir FROM fileTable"
        )
        fileSudahAda = [fDir[0] for (fDir) in hasil]
        files = chooseFiles(self, judul="Test")
        if files:
            for file in files:
                if file not in fileSudahAda and os.path.isfile(file):
                    self.sqlDatabase.executeQuery(
                        querySQL="INSERT INTO fileTable(fileName, fileDir) VALUES (?,?)",
                        params=[os.path.basename(file), file]
                    )
            self.fileTableModel.select()

    def hapusFileFoto(self):
        """Supaya user bisa hapus data yang dia pilih di kolom"""
        if self.currentRowClicked != None:
            jawaban = bringQuestion(self, "Konfirmasi", "Yakin untuk menghapus kolom yang Anda pilih?",
                                    "question", "yes", "no")
            if jawaban == QMessageBox.Yes:
                self.fileTableModel.removeRow(self.currentRowClicked)
                self.fileTableModel.submitAll()
                self.currentRowClicked = None

            else:
                self.currentRowClicked = None
                self.fileTable.clearSelection()
                self.fileTable.clearFocus()
                pass
        else:
            showInfo(self, "Tidak Dipilih", "Anda belum memilih kolom data apapun untuk dihapus!",
                     "info")

    def resetTableData(self):
        """For reset table data function"""
        if self.fileTableModel.rowCount() > 0:
            jawaban = bringQuestion(self, "Area Berbahaya", "Yakin untuk menghapus seluruh kolom terisi?",
                                    "warning", "yes", "no")
            if jawaban == QMessageBox.Yes:
                self.sqlDatabase.executeQuery(
                    querySQL="DELETE FROM fileTable"
                )
                self.fileTableModel.select()

            else:
                pass

    def continuePageOneVerify(self):
        """verifikasi sebelum lanjut"""
        if self.fileMode != 0:
            if self.fileMode == 1:
                if self.folderPath != None and os.path.isdir(self.folderPath):
                    konfirmasi = bringQuestion(self, "Konfirmasi", 
                                               "Siap untuk melanjutkan? Data pada halaman sebelumnya akan menjadi baca-saja (tidak dapat diedit)",
                                               'question','yes','no')
                    if konfirmasi == QMessageBox.Yes:
                        self.continuePageOne()

                else:
                    showInfo(self, "Mode Folder: Kesalahan", 
                             "Jalur folder yang dituju belum dipilih atau tidak ada sama sekali. Silahkan lakukan verifikasi mandiri!",
                             'error')

            elif self.fileMode == 2:
                if self.fileTableModel.rowCount() > 0:
                    konfirmasi = bringQuestion(self, "Konfirmasi", 
                                               "Siap untuk melanjutkan? Data pada halaman sebelumnya akan menjadi baca-saja (tidak dapat diedit)",
                                               'question','yes','no')
                    if konfirmasi == QMessageBox.Yes:
                        self.continuePageOne()

                else:
                    showInfo(self, "Mode File: Kesalahan",
                             "Anda belum memasukkan file apapun ke dalam tabel file. Silahkan lakukan verifikasi mandiri!",
                             'error')

        else:
            showInfo(self, "Belum Dipilih",
                     "Anda belum memilih mode apapun. Silahkan pilih salah satu diantaranya!",
                     'info')

    def continuePageOne(self):
        for _, qtObjectList in self.pageOneInteractable.items():
            for qtObject in qtObjectList:
                qtObject.setDisabled(True)

        for chooseAble in self.pageOneOpsi:
            chooseAble.setDisabled(True)

        for key, buttonList in self.allPages.items():
            if key == 1:
                for button in buttonList:
                    button.setEnabled(True)
        self.pageOneLanjut.setDisabled(True)
        self.stackedWidget.setCurrentIndex(1)
        self.pageTwoInit()

    ###### Second Page Only #######
    def pageTwoInit(self):
        """Initialize Page Two so it's ready to use"""
        self.fileVerifyProgress.setFormat("Belum Dimulai!")
        self.pageTwoLanjut.setDisabled(True)
        if not self.tabelVerifikasi.model():
            self.tabelVerifikasi.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tabelVerifikasi.setModel(self.tabelVerifikasiModel)
            self.tabelVerifikasi.hideColumn(0)

            delegateTableCenterAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignCenter, self.tabelVerifikasi)
            delegateTableLeftAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignLeft, self.tabelVerifikasi)
            delegateTableInterpret = InterpretTableDelegate(Qt.AlignmentFlag.AlignCenter, self.tabelVerifikasi)
            delegateFileSizeReadable = FileSizeTableDelegate(Qt.AlignmentFlag.AlignCenter, self.tabelVerifikasi)
            for i in range(1, 4):
                self.tabelVerifikasi.setItemDelegateForColumn(i, delegateTableCenterAlign)
            self.tabelVerifikasi.setItemDelegateForColumn(4, delegateFileSizeReadable)
            for i in range(5,8):
                self.tabelVerifikasi.setItemDelegateForColumn(i, delegateTableInterpret)
            self.tabelVerifikasi.setItemDelegateForColumn(8, delegateTableLeftAlign)

        self.tabelVerifikasiModel.select()
        if self.fileMode == 1:
            self.startVerify.setDisabled(True)
            self.pConn, self.cConn = Pipe()
            self.p1 = Process(
                target=backend.returnAllFileFromPath,
                args=(self.folderPath, self.cConn)
            )
            self.p1.start()
            self.t1.start(500)
        
        elif self.fileMode == 2:
            self.startVerify.setEnabled(True)

    def getAllFile(self):
        """Subprocess for secondary thread check, comms, and terminate"""
        if self.pConn.poll():
            allFile = self.pConn.recv()
            self.t1.stop()
            self.pConn.close()
            if self.p1.is_alive():
                self.p1.kill()

            if len(allFile) > 0:
                for pFile in allFile:
                    self.sqlDatabase.executeQuery(
                        querySQL="INSERT INTO fileVerify(fileName, filePath) VALUES (?,?)",
                        params=[os.path.basename(pFile), pFile]
                    )
                self.tabelVerifikasiModel.select()
                self.startVerify.setEnabled(True)

            else:
                for chooseAble in self.pageOneOpsi:
                    chooseAble.setEnabled(True)
                self.stackedWidget.setCurrentIndex(0)
                showInfo(self, "Kesalahan: Folder Kosong",
                         "Folder yang Anda pilih pada halaman sebelumnya merupakan folder kosong dan tidak mengandung file foto apapun. Silahkan verifikasi ulang sebelum lanjut menuju halaman verifikasi!", 'error')
                for key, buttonList in self.allPages.items():
                    if key == 0:
                        for button in buttonList:
                            button.setEnabled(True)
                    elif key == 1:
                        for button in buttonList:
                            button.setDisabled(True)
                self.pageOneLanjut.setEnabled(True)
                self.firstPageGUI()
                for key, qtObjectList in self.pageOneInteractable.items():
                    if key == 1:
                        for qtObj in qtObjectList:
                            qtObj.setEnabled(True)

    def verifyFile(self):
        """Lakukan verifikasi secara async menggunakan multiprocessing pool"""
        self.startVerify.setDisabled(True)
        allFDir = self.sqlDatabase.selectQuery(
            querySQL="SELECT filePath from fileVerify WHERE isSupported = 0 AND isNotCorrupted = 0 AND isNotVirus = 0"
        )
        allNeedVerifyFile = [fDir[0] for fDir in allFDir]
        self.fileCount = len(allNeedVerifyFile)
        self.fileVerifyProgress.setRange(0, self.fileCount)
        self.fileVerifyProgress.setFormat("%v/%m File Diproses")
        self.doneVerify = 0
        self.verifyFileQueue = Queue()

        self.pool = Pool(processes=self.numWorkers)
        for file in allNeedVerifyFile:
            self.pool.apply_async(backend.verifyImageFile, 
                                  args=(file,), 
                                  callback=self.verifyFileQueue.put)
        self.pool.close()
        self.t2.start(100)
        self.t3.start(500)

    def updateVerifyTable(self):
        self.tabelVerifikasiModel.select()

    def checkQueueVerifyFile(self):
        """Timer untuk mengecek proses verifikasi"""
        while not self.verifyFileQueue.empty():
            ### ekstensiFile, formatFile, ukuranAwal, dukunganFile, tidakCorrupt, bukanVirus, namaFile
            hasil = self.verifyFileQueue.get()
            self._bufferVerifikasiModel.append(hasil)
            self.doneVerify += 1
            
            if len(self._bufferVerifikasiModel) >= 5:
                self.sqlDatabase.executeQuery(
                    querySQL="UPDATE fileVerify SET fileExt = ?, fileFormat = ?, fileSize = ?, isSupported = ?, isNotCorrupted = ?, isNotVirus = ? WHERE fileName = ?",
                    params=self._bufferVerifikasiModel, isMultipleParams=True
                )
                self._bufferVerifikasiModel.clear()

            else:
                self._bufferVerifikasiModel.append(hasil)

            self.fileVerifyProgress.setValue(self.doneVerify)
            if self.doneVerify == self.fileCount:
                if len(self._bufferVerifikasiModel) > 0:
                    self.sqlDatabase.executeQuery(
                    querySQL="UPDATE fileVerify SET fileExt = ?, fileFormat = ?, fileSize = ?, isSupported = ?, isNotCorrupted = ?, isNotVirus = ? WHERE fileName = ?",
                    params=self._bufferVerifikasiModel, isMultipleParams=True
                )
                    self._bufferVerifikasiModel.clear()
                self.fileVerifyProgress.setFormat("Proses Selesai!")
                self.t2.stop()
                self.t3.stop()
                self.pageTwoLanjut.setEnabled(True)
    
    def continuePageTwo(self):
        """Lanjut menuju halaman selanjutnya (halaman 3)"""
        jawaban = bringQuestion(self, "Konfirmasi Untuk Melanjutkan",
                                "Apakah hasil verifikasi yang ditunjukkan oleh halaman ini sudah memenuhi ekspektasi Anda?\nFile tidak didukung, corrupt dan berpotensi mengandung virus tidak akan diikutsertakan untuk proses kompresi.",
                                "question", "yes", "no")
        if jawaban == QMessageBox.Yes:
            for key, pushButtonList in self.allPages.items():
                if key == 2:
                    for pushButton in pushButtonList:
                        pushButton.setEnabled(True)
            self.pageTwoLanjut.setDisabled(True)
            self.stackedWidget.setCurrentIndex(2)
            self.pageThreeInit()

    ###### Third Page Only #######
    def pageThreeInit(self):
        """Initialize page three supaya siap pakai"""
        allVerifiedFilePath = self.sqlDatabase.selectQuery(
            querySQL="SELECT filePath from fileVerify WHERE isSupported = 1 AND isNotCorrupted = 1 AND isNotVirus = 1"
        )
        allVerifiedFileFormat = self.sqlDatabase.selectQuery(
            querySQL="SELECT fileFormat FROM fileVerify WHERE isSupported = 1 AND isNotCorrupted = 1 AND isNotVirus = 1"
        )
        self.allVerifiedFilePath = [os.path.dirname(fDir[0]) for fDir in allVerifiedFilePath]
        self.allFilePathCategory = sorted(set(self.allVerifiedFilePath))
        self.allFileFormatCategory = sorted(set(
            [fCategory[0] for fCategory in allVerifiedFileFormat]
        ))
        self.pageThreeNext.setDisabled(True)
        self.dirTujuan.setReadOnly(True)
        self.ringkasanUpdater()

    def megaPixelChanged(self, index):
        """Respons on mpx changed below 18mp (index 1)"""
        tips = "Resolusi dibawah 12mp mungkin menghasilkan gambar yang blur"
        if index > 1:
            if tips not in self.qualityTip:
                self.qualityTip.append(tips)
            self.qualityTipsUpdater()

        elif index <=1:
            if tips in self.qualityTip:
                self.qualityTip.remove(tips)
            self.qualityTipsUpdater()

    def qualityChanged(self, value):
        """Respons on quality changed below 70%"""
        tips = r"Kualitas dibawah 70% berdampak pada kualitas secara langsung"
        if value < 70:
            if tips not in self.qualityTip:
                self.qualityTip.append(tips)
            self.qualityTipsUpdater()

        elif value >= 70:
            if tips in self.qualityTip:
                self.qualityTip.remove(tips)
            self.qualityTipsUpdater()

    def qualityTipsUpdater(self):
        """Updating the tips below the settings"""
        baseText = "Saran:" if len(self.qualityTip) > 0 else "Saran: Semua terlihat baik!"
        for number, tip in enumerate(self.qualityTip, start=1):
            baseText += f"\n{number}. {tip}"
        self.compressionTips.setText(baseText)

    def chooseSaveDir(self):
        """Memilih folder tujuan dengan syarat folder tujuan tidak boleh sama dengan folder asal foto"""
        folderTujuan = chooseFolder(self, "Pilih Folder untuk menyimpan hasil")
        if folderTujuan:
            if folderTujuan not in self.allFilePathCategory:
                self.saveDir = folderTujuan
                self.dirTujuan.setText(self.saveDir)

            else:
                showInfo(self, "Kesalahan: Folder Sama",
                         "Maaf, Anda tidak diizinkan untuk menyimpan gambar hasil kompresi pada folder yang sama dengan gambar aslinya. Silahkan pilih folder yang lain!", 
                         "info")

    def deleteOriginalFile(self):
        """BERBAHAYA: Sistem menghapus file asli (original) setelah kompresi selesai"""
        if self.hapusFIleAsli.checkState() == Qt.CheckState.Checked:
            jawaban = bringQuestion(self, "Area Berbahaya", 
                                    "Apakah Anda yakin untuk menghapus file asli Anda setelah proses kompresi selesai (tidak direkomendasikan?\nFile asli yang akan dihapus adalah file yang telah diverifikasi.",
                                    "warning", "yes", "no")
            if jawaban == QMessageBox.Yes:
                showInfo(self, "Area Berbahaya", "File terverifikasi akan dihapus setelah proses kompresi selesai!", 'warning')
                self.hapusFIleAsli.setCheckState(Qt.CheckState.Checked)

            else:
                self.hapusFIleAsli.setCheckState(Qt.CheckState.Unchecked)

        else:
            self.hapusFIleAsli.setCheckState(Qt.CheckState.Unchecked)

    def ringkasanUpdater(self):
        """Fungsi untuk memperbarui ringkasan"""
        headerText = ""

        strukturSummary = [
            f"{len(self.allVerifiedFilePath)} dari {self.tabelVerifikasiModel.rowCount()} foto akan diproses",
            f"Foto yang diproses memiliki ekstensi {",".join(self.allFileFormatCategory[:-1]) + " dan " + self.allFileFormatCategory[-1] if len(self.allFileFormatCategory) > 1 else self.allFileFormatCategory[0]}",
            f"Hasil kompresi beresolusi {self.imgMpx.currentText()} dan mempertahankan {self.imgCompress.value()}% kualitas aslinya",
        ]
        if len(self.dirTujuan.text()) > 0:
            self.pageThreeInteractable[-1].setEnabled(True)
            strukturSummary.append(f"Hasil disimpan pada folder {self.dirTujuan.text()}")

        if self.hapusFIleAsli.checkState() == Qt.CheckState.Checked:
            strukturSummary.append("Foto asli akan dihapus setelah diproses untuk kompresi")

        for number, summaryCategory in enumerate(strukturSummary, 1):
            headerText += f"{number}. {summaryCategory}\n"
        self.dataSummary.setText(headerText)

    def continuePageThreeVerify(self):
        """Lanjut menuju halaman terakhir (halaman 4)"""
        if len(self.dirTujuan.text()) > 0:
            if not os.path.isdir(self.dirTujuan.text()):
                os.makedirs(self.dirTujuan.text(), exist_ok=True)
            for qObject in self.pageThreeInteractable:
                qObject.setDisabled(True)
            self.continuePageThree()

        else:
            showInfo(self, "Ups! Ada yang Dilupakan", 
                     "Anda belum memilih lokasi penyimpanan (folder) untuk menyimpan file hasil kompresi. Silahkan pilih lokasinya terlebih dahulu!",
                     'error')

    def continuePageThree(self):
        """Trigger untuk menuju halaman terakhir"""
        for key, pushButtonList in self.allPages.items():
            if key == 3:
                for pushButton in pushButtonList:
                    pushButton.setEnabled(True)
        self.stackedWidget.setCurrentIndex(3)
        self.pageForthInit()

    ##### Forth (Last) Page Only #####
    def pageForthInit(self):
        """Fungsi untuk mempersiapkan halaman terakhir"""
        if not self.fileCompressionTable.model():
            self.fileCompressionTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.fileCompressionTable.setModel(self.fileCompressionTableModel)
            self.fileCompressionTableModel.select()
            self.fileCompressionTable.hideColumn(0)

            delegateTableCenterAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignCenter, self.fileCompressionTable)
            delegateTableLeftAlign = TableAlignDelegate(Qt.AlignmentFlag.AlignLeft, self.fileCompressionTable)
            delegateTableInterpret = InterpretTableDelegate(Qt.AlignmentFlag.AlignCenter, self.fileCompressionTable)
            delegateFileSizeReadable = FileSizeTableDelegate(Qt.AlignmentFlag.AlignCenter, self.fileCompressionTable)
            self.fileCompressionTable.setItemDelegateForColumn(1, delegateTableCenterAlign)
            self.fileCompressionTable.setItemDelegateForColumn(2, delegateTableInterpret)
            for i in range(3,6):
                self.fileCompressionTable.setItemDelegateForColumn(i, delegateFileSizeReadable)
            self.fileCompressionTable.setItemDelegateForColumn(6, delegateTableLeftAlign)
            self.fileCompressionTable.setItemDelegateForColumn(7, delegateTableInterpret)

        allVerifiedFilePath = self.sqlDatabase.selectQuery(
            querySQL="SELECT filePath from fileVerify WHERE isSupported = 1 AND isNotCorrupted = 1 AND isNotVirus = 1"
        )
        self.fileToCompress = [fPath[0] for fPath in allVerifiedFilePath]
        self.preferredMaxPix = int("".join([char for char in self.imgMpx.currentText() if char.isdigit()]))*100000
        self.preferredQuality = self.imgCompress.value()
        self.deleteOriFile = True if self.hapusFIleAsli.checkState() == Qt.CheckState.Checked else False
        self.fileCompressionProgress.setFormat("Belum Dimulai!")

    def compressFotoParalell(self):
        """Proses parallel untuk kompres gambar"""
        jawaban = bringQuestion(self, "Konfirmasi: Proses Kompresi",
                                "Apakah Anda yakin ingin memulai proses kompresi? Proses tidak dapat dihentikan, sehingga Anda tidak dapat menutup aplikasi ini demi mencegah kegagalan sistem.",
                                "question", 'yes', 'no')
        if jawaban == QMessageBox.Yes:
            self.nowExitAble = False
            self.startCompression.setDisabled(True)
            self.compressTask = Pool(processes=self.numWorkers)
            self.fileCompressionProgress.setRange(0, len(self.fileToCompress))
            self.fileCompressionProgress.setFormat("%v/%m File Dikompresi")
            for fDir in self.fileToCompress:
                self.compressTask.apply_async(compressModule.compressImage,
                                        args=(fDir, self.saveDir, self.preferredMaxPix, self.preferredQuality, self.deleteOriFile),
                                        callback=self.compressTaskComms.put)
            self.compressTask.close()
            self.t4.start(100)
            self.t5.start(500)

    def updateTable(self):
        self.fileCompressionTableModel.select()

    def checkCompressProgress(self):
        """Fungsi untuk mengecek proses verifikasi"""
        while not self.compressTaskComms.empty():
            hasil = self.compressTaskComms.get()
            self._bufferCompressionProgress.append(hasil)
            self.doneCompress +=1
            if len(self._bufferCompressionProgress) >= 5:
                self.sqlDatabase.executeQuery(
                    querySQL="UPDATE fileProcess SET fileStatus = ?, fileSize1 = ?, sizeReduced = ?, fileSavePath = ?, fileDeleted = ? WHERE fileName = ?",
                    params=self._bufferCompressionProgress, isMultipleParams=True
                )
                self._bufferCompressionProgress.clear()
            
            self.fileCompressionProgress.setValue(self.doneCompress)
            if self.doneCompress == len(self.fileToCompress):
                if len(self._bufferCompressionProgress) > 0:
                    self.sqlDatabase.executeQuery(
                    querySQL="UPDATE fileProcess SET fileStatus = ?, fileSize1 = ?, sizeReduced = ?, fileSavePath = ?, fileDeleted = ? WHERE fileName = ?",
                    params=self._bufferCompressionProgress, isMultipleParams=True
                )
                    self._bufferCompressionProgress.clear()
                self.t4.stop()
                self.t5.stop()
                self.nowExitAble = True

                totalPenghematan = self.sqlDatabase.selectQuery(
                    querySQL="SELECT SUM(sizeReduced) FROM fileProcess WHERE fileStatus = 1"
                )
                self.fileCompressionProgress.setFormat(f"Proses Selesai. Anda menghemat {humanReadableSize(totalPenghematan[0][0])}")

    def closeEvent(self, event):
        """Preventing user for accidently closing application"""
        if self.nowExitAble:
            jawaban = bringQuestion(self, "Keluar Aplikasi?", "Apakah Anda yakin ingin keluar dari aplikasi?",
                                    ikon="question", tombol1="yes", tombol2="no")
            if jawaban == QMessageBox.StandardButton.Yes:
                app.cleanSocket()
                event.accept()

            else:
                event.ignore()

        else:
            showInfo(self, "Penutupan Aplikasi: Ditolak!",
                     "Sistem sedang menolak penutupan aplikasi secara keseluruhan karena ada proses berat yang sedang berjalan. Harap coba lagi ketika proses sudah selesai!",
                     'error')
            event.ignore()

if __name__ == "__main__":
    app = SingleInstance(sys.argv)
    if app.isRunning:
        showInfo(None, "Informasi", 
                "Aplikasi sudah berjalan di perangkat Anda. Silahkan cek kembali!", 'info')
        sys.exit(0)

    else:
        WM_ = WindowManager()
        firstPage = WM_.openWindow(HomeScreen)
        firstPage.show()
        app.exec()