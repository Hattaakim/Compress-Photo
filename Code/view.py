from PySide6.QtWidgets import QAbstractItemView, QApplication, QComboBox, QFileDialog, QGraphicsScene, QGraphicsView, QMainWindow, QMessageBox, QStyledItemDelegate, QTableView, QTreeView
from PySide6.QtCore import QEvent, QFile, QIODevice, QModelIndex, QObject, QRegularExpression, QSize, QStandardPaths, QThread, QTimer, Qt, Signal
from PySide6.QtGui import QIcon, QImage, QPainter, QPixmap, QRegularExpressionValidator, QStandardItem, QStandardItemModel
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtSql import QSqlTableModel
import sys, os, math, shiboken6, gc, subprocess, pillow_heif, io, tempfile
from datetime import datetime
from dataclasses import dataclass
from typing import Literal, Callable
from multiprocessing import Pool, cpu_count, Queue, Pipe, Process
from PIL import Image
from PIL.ImageQt import ImageQt
from collections import Counter

######### Externally Managed Module #########
from managedModule import backend, compressModule

######### Assets File ############
from assets import resources

######### Window ##########
from windowModule import MainWindow, selectNewFile, PerfSettingCPU, CompressSettings, pictureSample, compressConfirmation

######### Global Const #########
APPID = "Compress Foto@hattaakim"
pillow_heif.register_heif_opener()

######### Custom Class For Struct ########
@dataclass
class allTableModelStruct:
    """Struct dictionary untuk merangkap (nama tabel sql, init delegate, whichButtonEnabled, whichButtonDisabled)"""
    name: str
    init_delegate: Callable
    enabledButton: list
    disabledButton: list

@dataclass
class saveFormatDictStruct:
    """Struct dictionary untuk merangkap (index, format di QComboBox, format System)"""
    formatComboBox: str
    formatSystem: str

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
    validExt = ['.jpg', '.jpeg', '.png', '.webp', 'mpo', '.heic', '.heif']
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
class ImgVerifyWorker(QThread):
    """Worker class async untuk memverifikasi file foto pada halaman sample foto"""
    imgSuccess = Signal(QImage, str, str, float)
    imgError = Signal(str)

    def __init__(self, imgPath):
        super().__init__()
        self.imgPath = imgPath
        self.qtSupportedFormat = ['JPG', 'JPEG', 'PNG', 'WEBP']
        self.qtSupportedExt = ['.jpg', '.jpeg', '.png', '.webp']

    def run(self):
        """Fungsi utama buat memverifikasi file foto"""
        try:
            fileExt = None
            fileFormat = None
            imgSize = 0.00
            qImage = None

            qFile = QFile(self.imgPath)
            if not qFile.open(QIODevice.OpenModeFlag.ReadOnly):
                self.imgError.emit(f"Gagal membuka file: {self.imgPath}")
            imByteArray = qFile.readAll()
            qFile.close()
            qFile.deleteLater()
            imPtr = imByteArray.data()

            imgSize = os.path.getsize(self.imgPath)
            fileExt = os.path.splitext(self.imgPath)[1].lower()
            bufferIm = io.BytesIO(imPtr)

            imgPtr = Image.open(bufferIm)
            fileFormat = imgPtr.format
            imgPtr.verify()
            imgPtr.close()

            if fileExt not in self.qtSupportedExt and fileFormat not in self.qtSupportedFormat:
                imgPtr = Image.open(self.imgPath)
                qImage = ImageQt(imgPtr)

            else:
                qImage = QImage(self.imgPath)

            if qImage.isNull():
                self.imgError.emit("Qt Gagal Memuat Gambar (format file tidak didukung)")

            self.imgSuccess.emit(qImage, fileExt, fileFormat, imgSize)

        except (Image.DecompressionBombWarning, Image.DecompressionBombError) as e:
            self.imgError.emit(f"File gambar ditolak karena merupakan virus Decompression Bomb. [Kode Error: {e}]")
        
        except Exception as e:
            self.imgError.emit(f"File rusak atau bukan file gambar yang valid. [Kode Error: {e}]")

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
            0: "?", 1: "✔", 2: "✘"
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
        self.validExt = {'.jpg', '.jpeg', '.png', '.webp', 'mpo', '.heic', '.heif'}

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

                            droppedFile = os.path.normpath(url.toLocalFile())
                            fileExt = os.path.splitext(droppedFile)[1].lower()

                            if droppedFile not in existsFile and fileExt in self.validExt and os.path.isfile(droppedFile):
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

class LineEditDragnDropFolder(QObject):
    """Filter supaya user bisa drag and drop folder ke line edit"""
    def __init__(self, lineEdit, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.lineEdit = lineEdit
        self.defaultSavePath = os.path.join(os.environ["USERPROFILE"], "Downloads")

    def eventFilter(self, watched, event):
        if watched == self.lineEdit:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True

            elif event.type() == QEvent.Type.Drop:
                if event.mimeData().hasUrls():
                    lokasiSimpan = os.path.normpath(event.mimeData().urls()[0].toLocalFile())
                    if os.path.isdir(lokasiSimpan):
                        self.lineEdit.setText(f"{lokasiSimpan}")
                        if lokasiSimpan != self.defaultSavePath:
                            self.lineEdit.setToolTip("")

                    else:
                        showInfo(self.parent, "Ups, ada kesalahan", "Folder yang kamu pilih harus merupakan folder (bukan file). Silahkan dicoba lagi!",
                                 'info')
                    event.acceptProposedAction()
                    return True
        return False

class SaberButtonFilter(QObject):
    """Filter khusus untuk pushbutton agar ikonnya bisa berubah jadi ikon gradien saat dihover"""
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

class LineEditDragnDropFile(QObject):
    """Filter khusus untuk PCompressSampleTest supaya QLineEdit bisa
    menerima drop berupa file gambar"""
    def __init__(self, lineEdit, mainApp):
        super().__init__(mainApp)
        self.mainApp = mainApp
        self.watchedLineEdit = lineEdit
        self.validExt = {'.jpg', '.jpeg', '.png', '.webp', 'mpo', '.heic', '.heif'}

    def eventFilter(self, watched, event):
        if watched == self.watchedLineEdit:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True

            elif event.type() == QEvent.Type.Drop:
                if event.mimeData().hasUrls():
                    filePath = os.path.normpath(event.mimeData().urls()[0].toLocalFile())
                    currentFilePath = self.watchedLineEdit.text()
                    if filePath != currentFilePath and os.path.splitext(filePath)[1].lower() in self.validExt and os.path.isfile(filePath):
                        self.watchedLineEdit.setText(filePath)
                        self.mainApp.processBeforeImage()

                    else:
                        showInfo(self.mainApp, "Oops... Ada Kesalahan", "Ada beberapa potensi kesalahan:\n1. File yang Anda pilih sama dengan file sebelumnya\n2. Ekstensi file tidak didukung\n3. File tidak ada\nSilahkan verifikasi ulang ya!",
                                 'info')
                    event.acceptProposedAction()
                    return True
        return super().eventFilter(watched, event)

class GraphicsViewScale(QObject):
    """Filter supaya Graphics View yang berisi objek apapun bisa diresize pakai mouse"""
    def __init__(self, graphicsView, parent=None):
        super().__init__(parent)
        self.currentGraphicsView = graphicsView
        self.minScale = 0.01
        self.maxScale = 100.0 

    def manualZoomIn(self):
        """Fungsi untuk melakukan zoom in pada graphics view menggunakan tombol"""
        zoomFactor = 1.1
        currentScale = self.currentGraphicsView.transform().m11()

        if currentScale * zoomFactor > self.maxScale:
            zoomFactor = self.maxScale / currentScale
        self.currentGraphicsView.scale(zoomFactor, zoomFactor)

    def manualZoomOut(self):
        """Fungsi untuk melakukan zoom out pada graphics view menggunakan tombol"""
        zoomFactor = 1/1.1
        currentScale = self.currentGraphicsView.transform().m11()

        if currentScale * zoomFactor < self.minScale:
            zoomFactor = self.minScale / currentScale
        self.currentGraphicsView.scale(zoomFactor, zoomFactor)

    def eventFilter(self, watched, event):
        if watched == self.currentGraphicsView:
            if event.type() == QEvent.Type.Wheel:
                delta = event.angleDelta().y()
                if delta == 0:
                    return False
                
                zoomFactor = math.pow(1.2, delta/120.0)
                currentScale = self.currentGraphicsView.transform().m11()
                newScale = currentScale*zoomFactor

                if newScale < self.minScale:
                    zoomFactor = self.minScale / currentScale
                elif newScale > self.maxScale:
                    zoomFactor = self.maxScale / currentScale
                self.currentGraphicsView.scale(zoomFactor, zoomFactor)
                return True
            return False
        return super().eventFilter(watched, event)

class WindowManager:
    """Window Manager Instance"""
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
        self.compressedFileTableHeader = self.verifyFileTableHeader | {"Ukuran Akhir": 75, "Penghematan": 85, "Status":70, "Lokasi Simpan": 250, "Dihapus": 70}
        self.photoRejectedTableHeader = self.fotoBaruTableHeader | {"Format File": 75, "Dukungan File": 85, "Integritas File": 85, "File Aman": 65, "Tanggal Ditolak": 100}
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

        #### CONST FOR Universal Async Process ####
        self.pool = None
        self.heavyThreadLoaderStatus = 0
        
        #### CONST FOR Verify File Async Process ####
        self.verifyFileIPC = Queue()
        self.timerCheckVFIPC = QTimer(self)
        self.timerUpdateVerifyTable = QTimer(self)
        self._bufferVerifikasiFile = []
        self.doneVerifyCount = 0
        self.verifyFileCount = 0

        #### CONST FOR Compress File Async Process ####
        self.compressFileIPC = Queue()
        self.timerCheckCompressIPC = QTimer(self)
        self.timerUpdateCompressTable = QTimer(self)
        self._bufferCompressFile = []
        self.doneCompressionCount = 0
        self.compressionFileCount = 0

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

        #### SIGNAL AND SLOT FOR startCompression
        self.timerUpdateCompressTable.timeout.connect(self.forceUpdateTable)
        self.timerCheckCompressIPC.timeout.connect(self.checkQueueStartCompression)

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
        self.startVerify.clicked.connect(self.startVerifyFile)
        self.compressSettings.clicked.connect(self.openCompressSettings)
        self.startCompress.clicked.connect(self.startCompression)
        self.revealFile.clicked.connect(self.revealFileOnFE)
        self.reloadTable.clicked.connect(self.forceUpdateTable)

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
    
    #####=====================APPS INTERNAL FUNCTION=========================######
    #####===================== FUNGSI UNTUK NAVIGASI HALAMAN =========================#####
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
        """Merespons ketika pengguna menekan tree page navigator untuk berpindah halaman"""
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

    #####====================== FUNGSI KHUSUS DI QAction (CPU Settings) ========================#####
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

    #####===================== FUNGSI KHUSUS DI QAction (Auto Start) =============================######
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
    
    #####=========================== FUNGSI TOMBOL NEON (DIURUTKAN) =================================#####
    #####=========================== FUNGSI TOMBOL TAMBAH FILE/FOLDER ===============================#####
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

    #####=========================== FUNGSI TOMBOL TONG SAMPAH ===============================#####
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
    
    #####=================================== FUNGSI TOMBOL RECYCLE =================================#####
    def cancelDelete(self):
        """Saat pengguna menekan row dan memencet cancel delete (file restored)"""
        if self.currentRowClicked != None:
            currentFileDir = self.sqlTableModel.record(self.currentRowClicked).value("fileDir")

            hasil = self.sqlDb.selectQuery(querySQL="SELECT fileDir FROM fileJobTable")
            allFileDir = {file[0] for file in hasil if os.path.isfile(file[0])}
            if currentFileDir not in allFileDir and os.path.isfile(currentFileDir):
                self.sqlDb.executeQuery(
                    querySQL="INSERT INTO fileJobTable(fileName, fileDir, fileExt) SELECT fileName, fileDir, fileExt FROM photoCancelledTable WHERE fileDir = ?",
                    params=[currentFileDir]
                )
                showInfo(self, "Informasi: File Direstorasi",
                        f"File {os.path.basename(currentFileDir)} telah dipindahkan menuju tabel 'Foto Baru'!", 'info')

            else:
                showInfo(self, "Informasi: File Gagal Direstorasi",
                        f"File {os.path.basename(currentFileDir)} sudah ada pada tabel 'Foto Baru' atau file tersebut sudah dihapus. Lakukan verifikasi mandiri!", 'warning')
                
            self.sqlDb.executeQuery(querySQL="DELETE FROM photoCancelledTable WHERE fileDir = ?", params=[currentFileDir])
            self.currentRowClicked = None
            self.universalTableView.clearSelection()
            self.universalTableView.clearFocus()
            self.sqlTableModel.select()

    #####================================== FUNGSI TOMBOL MULAI VERIFIKASI FILE ==================================#####
    def startVerifyFile(self):
        """Mulai proses verifikasi file secara asinkron"""
        if self.currentTableModel == 0:
            if self.heavyThreadLoaderStatus == 0:
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
                    self.changePage("Siap Diproses", 1)
                    self.verifyFileCount = len(allFileToProcess)
                    self.pool = Pool(processes=self.numWorkers)
                    self.heavyThreadLoaderStatus = 1
                    for file in allFileToProcess:
                        self.pool.apply_async(backend.verifyImageFile,
                                            args=(file,), callback=self.verifyFileIPC.put)
                    self.timerCheckVFIPC.start(100)
                    self.timerUpdateVerifyTable.start(1000)

                else:
                    showInfo(self, "Oops.. Ada Yang Tidak Beres",
                            "Tidak ada file baru yang harus diverifikasi!", 'info')
            
            else:
                showInfo(self, "CPU: (sambil berkeringat) 'Udah Bang...'",
                         "Proses berat sedang berjalan dan memakan banyak sumber daya perangkat Anda. Kami tidak ingin menyebabkan perangkat Anda crash dengan menjalankan lebih dari 2 proses berat tersebut.",
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
                self.pool.close()
                if len(self._bufferVerifikasiFile) > 0:
                    self.sqlDb.executeQuery(
                    querySQL="UPDATE verifyFileTable SET fileExt = ?, fileFormat = ?, isSupported = ?, isNotCorrupted = ?, isNotVirus = ?, fileSize0 = ? WHERE fileName = ?",
                    params=self._bufferVerifikasiFile, isMultipleParams=True
                    )
                    self._bufferVerifikasiFile.clear()
                self.startVerify.setText("Verifikasi\nFile")
                self.doneVerifyCount = 0
                self.heavyThreadLoaderStatus = 0 
                QTimer.singleShot(1000, self.forceUpdateTable)

    #####========================================== FUNGSI TOMBOL BUKA PENGATURAN KOMPRESI ==========================================#####
    def openCompressSettings(self):
        """Buka pengaturan kompresi"""
        window = WM_.openWindow(PengaturanKompresi, self.userPersonalization)
        window.show()

    #####========================================== FUNGSI TOMBOL KOMPRESI FILE ===========================================#####
    def startCompression(self):
        """Fungsi untuk menampilkan summary kompresi sebelum sistem memulai"""
        if self.heavyThreadLoaderStatus == 0:
            _compressconfirm = WM_.openWindow(CompressConfirmation, self.userPersonalization, self.sqlDb)
            _compressconfirm.show()
            _compressconfirm.doneAction.connect(self.compressionJob)

        else:
            showInfo(self, "CPU: (keringatan) 'Udah Bang.. jangan'",
                "Proses berat sedang berjalan dan memakan banyak sumber daya perangkat Anda. Kami tidak ingin menyebabkan perangkat Anda crash dengan menjalankan lebih dari 2 proses berat tersebut.",
                'warning')

    def compressionJob(self):
        """Mulai kompresi file"""
        if self.currentTableModel == 1:
            if self.heavyThreadLoaderStatus == 0:
                self.sqlDb.executeQuery(
                    querySQL="""INSERT INTO compressedFileTable(fileName, fileDir, fileExt, fileFormat, isSupported, isNotCorrupted, isNotVirus, fileSize0)
SELECT fileName, fileDir, fileExt, fileFormat, isSupported, isNotCorrupted, isNotVirus, fileSize0 FROM verifyFileTable
WHERE isSupported = 1 AND isNotCorrupted = 1 AND isNotVirus = 1"""
                )
                self.sqlDb.executeQuery(
                    querySQL="""INSERT INTO photoRejectedTable(fileName, fileDir, fileExt, fileFormat, isSupported, isNotCorrupted, isNotVirus)
SELECT fileName, fileDir, fileExt, fileFormat, isSupported, isNotCorrupted, isNotVirus FROM verifyFileTable
WHERE isSupported != 1 OR isNotCorrupted != 1 OR isNotVirus != 1"""
                )
                hariIni = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.sqlDb.executeQuery(
                    querySQL="UPDATE photoRejectedTable SET dateRejected = ?",
                    params=(hariIni,)
                )
                self.sqlDb.executeQuery(
                    querySQL="DELETE FROM verifyFileTable"
                )
                hasil = self.sqlDb.selectQuery(
                    querySQL="SELECT fileDir FROM compressedFileTable"
                )
                allFileToCompress = [file[0] for file in hasil
                                     if os.path.isfile(file[0])]
                if len(allFileToCompress) > 0:
                    self.compressionFileCount = len(allFileToCompress)
                    mpSettings = 1_000_000*self.userPersonalization.getUserConfig('compressSettings',0)
                    photoQualitySettings = self.userPersonalization.getUserConfig('compressSettings',1)
                    saveLocation = self.userPersonalization.getUserConfig('compressSettings',2)
                    saveFormat = self.userPersonalization.getUserConfig('compressSettings',3)
                    deleteOriFile = self.userPersonalization.getUserConfig('compressSettings', 4)
                    resamplingAlgorithm = self.userPersonalization.getUserConfig('compressSettings', 5)

                    self.changePage("Selesai Diproses", 2)
                    self.heavyThreadLoaderStatus = 1
                    self.pool = Pool(processes=self.numWorkers)
                    for file in allFileToCompress:
                        self.pool.apply_async(compressModule.compressImage,
                                              args=(file, saveLocation, resamplingAlgorithm,
                                                    mpSettings, photoQualitySettings, saveFormat,
                                                    bool(deleteOriFile)), callback=self.compressFileIPC.put)
                    self.timerCheckCompressIPC.start(100)
                    self.timerUpdateVerifyTable.start(1000)

                else:
                    showInfo(self, "Oops.. Kami Menemukan Sesuatu",
                             "Tidak ada file yang siap untuk dikompresi. Silahkan cek kembali, ya!", 'info')

            else:
                showInfo(self, "CPU: (keringatan) 'Udah Bang.. jangan'",
                         "Proses berat sedang berjalan dan memakan banyak sumber daya perangkat Anda. Kami tidak ingin menyebabkan perangkat Anda crash dengan menjalankan lebih dari 2 proses berat tersebut.",
                         'warning')

    def checkQueueStartCompression(self):
        """Fungsi untuk mengecek IPC dari hasil async startCompression"""
        while not self.compressFileIPC.empty():
            hasil = self.compressFileIPC.get()
            self._bufferCompressFile.append(hasil)
            self.doneCompressionCount += 1
            if len(self._bufferCompressFile) >= 5:
                self.sqlDb.executeQuery(
                    querySQL="update compressedFileTable SET compressStatus = ?, fileSize1 = ?, sizeReduced = ?, savePath = ?, isDeleted = ? WHERE fileName = ?", 
                    params=self._bufferCompressFile, isMultipleParams=True
                )
                self._bufferCompressFile.clear()
            self.startCompress.setText(f"Mengompresi:\n{self.doneCompressionCount}/{self.compressionFileCount} File")

            if self.doneCompressionCount == self.compressionFileCount:
                self.timerCheckCompressIPC.stop()
                self.timerUpdateCompressTable.stop()
                self.pool.close()
                if len(self._bufferCompressFile) > 0:
                    self.sqlDb.executeQuery(
                        querySQL="update compressedFileTable SET compressStatus = ?, fileSize1 = ?, sizeReduced = ?, savePath = ?, isDeleted = ? WHERE fileName = ?", 
                        params=self._bufferCompressFile, isMultipleParams=True
                    )
                    self._bufferCompressFile.clear()
                self.startCompress.setText("Mulai\nKompresi")
                self.doneCompressionCount = 0
                self.heavyThreadLoaderStatus = 0
                QTimer.singleShot(1000, self.forceUpdateTable)
    
    #####===================================== FUNGSI TOMBOL TUNJUKKAN FILE ====================================#####
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

    #####============================= FUNGSI REFRESH TABLE ==========================#####
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
        self.universalTableView.setItemDelegateForColumn(11, self.delegateTableInterpret) 
        self.universalTableView.setItemDelegateForColumn(12, self.delegateTableCenterAlign)
        self.universalTableView.setItemDelegateForColumn(13, self.delegateTableInterpret) 

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
                     "Maaf, kami tidak diizinkan untuk memakai seluruh " \
                     "Core CPU perangkat Anda untuk mencegah instabilitas sistem! Perangkat Anda membutuhkan minimal 1 Core untuk tetap berfungsi secara stabil.",
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
        self.validExt = {'.jpg', '.jpeg', '.png', '.webp', 'mpo', '.heic', '.heif'}

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
    """Kelas Window untuk Pengaturan kompresi, akses melalui tombol yang bisa dihover"""
    def __init__(self, UPPassThrough:backend.UserPersonalization):
        super().__init__()
        self.setupUi(self)

        #### Window Const
        self.appIcon = ':/ai_appDefaultIcon'
        self.chooseDirIcon = ':/cs_chooseFolderIcon'
        self.recommendedSettingsIcon = ':/cs_recommenddedSettingsIcon'
        self.openSamplePhotoIcon = ':/cs_openSamplePhotoIcon'

        self.userPersonalization = UPPassThrough
        self.defaultSavePath = os.path.join(os.environ["USERPROFILE"], "Downloads")
        self.allSettings = [self.megaPixel, self.photoQuality, self.chooseDir, self.recommendedSettings, 
                            self.deleteOriginalFile, self.saveFormat, self.resamplingAlgorithm]
        self.lineEditFilter = LineEditDragnDropFolder(self.saveLocation, self)

        self.allResamplingTip = {
            0: "Metode paling dasar dan cepat. Hasil gambar sangat tajam secara kasar dan memunculkan efek kotak-kotak (pixelated). Sangat ideal untuk pixel art, elemen UI, atau kebutuhan komputasi instan.",
            1: "Algoritma standar industri. Mempertahankan detail mikroskopis dengan ketajaman yang sangat tinggi. Menjadi pilihan utama untuk memperbesar (upscaling), tetapi memiliki kelemahan berupa ringing (garis halo).",
            2: "Metode yang meratakan warna sehingga menghasilkan batas bergerigi dengan efek samping sedikit kabur (soft/blur). Hasilnya sedikit lebih baik dari algoritma Nearest.",
            3: "Standar umum fotografi. Gambar dihasilkan dengan warna yang lebih halus dan mendetail dibanding Bilinear. Pilihan tengah yang sangat baik (lebih lambat dari Bilinear, tetapi lebih cepat dari Lanczos).",
            4: "Algoritma untuk mengecilkan gambar (downscaling). Jika digunakan untuk memperbesar gambar (upscaling), hasilnya akan terlihat pecah seperti algoritma Nearest",
            5: "Algoritma unggulan untuk mengecilkan gambar karena kemampuannya untuk mempertahankan ketajaman garis, namun tetap beroperasi dengan kecepatan yang nyaris sama cepatnya dengan Bilinear.",
            6: "Pesaing berat Lanczos untuk membasmi artefak ringing meskipun menghasilkan beban komputasi yang lebih berat. Menghasilkan gambar yang sangat tajam dan natural secara visual dengan performa multithreading CPU yang sangat efisien.",
            7: "Algoritma terbaik dengan beban komputasi yang paling berat, tetapi dapat mematikan seluruh artefak ringing tanpa menipu mata dengan kontras buatan. Ideal untuk citra saintifik, medis, atau arsip penting."
        }
        self.allSaveFormat = (
            "JPEG", "JPG", "JPEG2000", "PNG",
            "HEIF", "HEIC", "WEBP", "BMP",
            "TIFF", "ICO", "AVIF"
        )

        #### Init Code
        self.initGUI()
        self.initUPSettings()
        self.onResamplingChanged()

        #### Signal & Slots
        self.chooseDir.clicked.connect(self.chooseSaveFolder)
        self.deleteOriginalFile.clicked.connect(self.onDeleteFileCheck)
        self.resamplingAlgorithm.currentIndexChanged.connect(self.onResamplingChanged)
        self.openSamplePhoto.clicked.connect(self.samplePhoto)
        self.recommendedSettings.clicked.connect(self.useRecommendedSettings)
        self.simpanDanTutup.clicked.connect(self.commitAllSettings)
        self.batal.clicked.connect(lambda: self.closeWindow())
    
    def initGUI(self):
        """Persiapkan GUI"""
        self.setWindowIcon(QIcon(self.appIcon))
        self.setWindowTitle("Pengaturan Kompresi")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.chooseDir.setIcon(QIcon(self.chooseDirIcon))
        self.recommendedSettings.setIcon(QIcon(self.recommendedSettingsIcon))
        self.openSamplePhoto.setIcon(QIcon(self.openSamplePhotoIcon))

        self.saveLocation.setReadOnly(True)
        self.saveLocation.installEventFilter(self.lineEditFilter)
    
    def initUPSettings(self):
        """Persiapkan pengaturan pengguna yang sebelumnya (kalau ada)"""
        self.megaPixel.setValue(self.userPersonalization.getUserConfig('compressSettings',0))
        self.photoQuality.setValue(self.userPersonalization.getUserConfig('compressSettings',1))
        self.deleteOriginalFile.setChecked(bool(self.userPersonalization.getUserConfig('compressSettings',4)))
        self.saveFormat.setCurrentIndex(self.allSaveFormat.index(self.userPersonalization.getUserConfig('compressSettings', 3)))
        self.resamplingAlgorithm.setCurrentIndex(self.userPersonalization.getUserConfig('compressSettings', 5))

        if self.userPersonalization.getUserConfig('compressSettings',2) == "default" or self.defaultSavePath:
            self.saveLocation.setText(self.defaultSavePath)
            self.defaultFolderToolTip()

        else:
            self.saveLocation.setText(self.userPersonalization.getUserConfig('compressSettings',2))
            self.saveLocation.setToolTip("")
    
    def chooseSaveFolder(self):
        """Fungsi bagi user supaya bisa milih folder untuk simpan file lewat metode klik tombol"""
        choosedFolder = chooseFolder(self, "Pilih Folder Untuk Menyimpan")
        if choosedFolder != None:
            fDirNormPath = os.path.normpath(choosedFolder)
            self.saveLocation.setText(fDirNormPath)
            if fDirNormPath == self.defaultSavePath:
                self.defaultFolderToolTip()
            else:
                self.saveLocation.setToolTip("")

    def defaultFolderToolTip(self):
        self.saveLocation.setToolTip("Folder default di 'Downloads/[Compressed-Tanggal]' untuk menyimpan hasil kompresi.")

    def onDeleteFileCheck(self):
        """Respons ketika pengguna ngecheck delete original file"""
        self.deleteOriginalFile.setChecked(False)
        jawaban = bringQuestion(self, "AREA BERBAHAYA: KONFIRMASI DIBUTUHKAN",
                                "Apakah Anda YAKIN UNTUK MENGHAPUS FILE FOTO ASLI setelah dikompresi? Penghapusan ini bersifat irreversible.",
                                'warning', 'yes', 'no')
        if jawaban == QMessageBox.Yes:
            self.deleteOriginalFile.setChecked(True)
            showInfo(self, "Informasi", "File Foto asli AKAN DIHAPUS sesaat setelah proses kompresi selesai", 'info')
        else:
            self.deleteOriginalFile.setChecked(False)
    
    def onResamplingChanged(self):
        """Respons saat pengguna mengubah mode resampling"""
        self.resamplingDesc.setText(
            self.allResamplingTip[self.resamplingAlgorithm.currentIndex()]
        )
    
    def useRecommendedSettings(self):
        """Paling direkomendasikan hehe"""
        _confirm = bringQuestion(self, "Pengaturan Akan Ditimpa",
                                 """Anda yakin ingin menimpa pengaturan saat ini dengan pengaturan yang direkomendasikan? Perubahan yang akan terjadi
1. Resolusi akan diubah menjadi 12Mp
2. Kualitas Dipertahankan menjadi 85%,
3. Opsi hapus file foto asli akan diunchecked
Konfirmasi YES bila Anda yakin!""", 'question', 'yes', 'no')
        if _confirm == QMessageBox.Yes:
            self.megaPixel.setValue(12)
            self.photoQuality.setValue(85)
            self.deleteOriginalFile.setChecked(False)

    def samplePhoto(self):
        _wmInstanceOpenWindow = WM_.openWindow(PCompressSampleTest)
        _wmInstanceOpenWindow.show()

    def commitAllSettings(self):
        """Simpan semua pengaturan pengguna"""
        for qObject in self.allSettings:
            qObject.setDisabled(True)
        getSettings = (self.megaPixel.value(), self.photoQuality.value(), self.saveLocation.text(), self.saveFormat.currentText(), int(self.deleteOriginalFile.isChecked()), self.resamplingAlgorithm.currentIndex())
        for i, val in enumerate(getSettings):
            self.userPersonalization.editUserConfig('compressSettings', i, val)
        self.closeWindow(isQuestioned=False)

    def closeWindow(self, isQuestioned:bool=True):
        """Fungsi ramah yang bertanya (atau dioverride) saat jendela mau ditutup"""
        if isQuestioned:
            _konfirmasi = bringQuestion(self, "Tutup Jendela", "Apakah Anda yakin ingin menutup jendela ini? Data yang tidak tersimpan akan hilang!",
                                        'question', 'yes', 'no')
            if _konfirmasi == QMessageBox.Yes:
                self._closeWindowFunction()

        elif isQuestioned == False:
            self._closeWindowFunction()

    def _closeWindowFunction(self):
        """Fungsi untuk menutup jendela tanpa ampun"""
        WM_.closeWindow(PengaturanKompresi)

    def closeEvent(self, event):
        """Cegah penutupan jendela tanpa WindowManager Instance"""
        event.ignore()
        self.closeWindow()

class PCompressSampleTest(QMainWindow, pictureSample.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        #### Window CONST
        self.allScaleButton = {0: [self.beforeScaleUp, self.afterScaleUp],
                               1: [self.beforeScaleDown, self.afterScaleDown]}
        self.allUneditableLineEdit = [self.fileExt, self.fileFormat, self.compressStatus, 
                                      self.fileSize0, self.fileSize1, self.sizeReduced]

        #### Line Edit Below Graphics View
        self.samplePhotoDragDrop = LineEditDragnDropFile(self.samplePhotoDir, self)
        self.samplePhotoDir.setReadOnly(True)
        self.samplePhotoDir.setAcceptDrops(True)
        self.samplePhotoDir.installEventFilter(self.samplePhotoDragDrop)

        #### GRAPHICS VIEW AND SCENE CONST
        self.allImageView = [self.beforeImage, self.afterImage]
        for graphicsView in self.allImageView:
            graphicsView.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
            graphicsView.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            graphicsView.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.beforeImageScale = GraphicsViewScale(self.beforeImage, self)
        self.beforeScene = QGraphicsScene(self)
        self.beforeImage.setScene(self.beforeScene)
        self.beforeCurrentImage = None
        self.beforeImage.installEventFilter(self.beforeImageScale)

        self.afterImageScale = GraphicsViewScale(self.afterImage, self)
        self.afterScene = QGraphicsScene(self)
        self.afterImage.setScene(self.afterScene)
        self.afterCurrentImage = None
        self.afterImage.installEventFilter(self.afterImageScale)

        #### Concurrent Process (async) for pictureSample upload
        self.imgVerifyWorker = None
        self.imgVerifyErrorList = []
        
        #### Timer and MultiProcessing for processRealPicture CONST
        self.pConn, self.cConn = Pipe()
        self.compressSampleMP = None
        self.T_fetchSampleResult = QTimer(self)
        self.sampleResultTempDir = None

        self.currentPos = 0
        self.T_compressStatusAnim = QTimer(self)
        self.allInteractable = [self.choosePhotoFile, self.samplePhotoDir, 
                                 self.megaPixel, self.photoQuality, self.resamplingAlgorithm, self.startCompressSimulation]

        #### Init Code
        self.initGUI()

        #### Signal and Slots
        self.T_fetchSampleResult.timeout.connect(self.checkPipeCompressSample)
        self.T_compressStatusAnim.timeout.connect(self.compressStatusAnim)
        self.choosePhotoFile.clicked.connect(self.chooseSamplePhoto)
        self.beforeScaleUp.clicked.connect(self.beforeImageScale.manualZoomIn)
        self.beforeScaleDown.clicked.connect(self.beforeImageScale.manualZoomOut)
        self.afterScaleUp.clicked.connect(self.afterImageScale.manualZoomIn)
        self.afterScaleDown.clicked.connect(self.afterImageScale.manualZoomOut)
        self.startCompressSimulation.clicked.connect(self.startCompressSample)

    def initGUI(self):
        """Mempersiapkan UI agar siap ditampilkan dan digunakan oleh pengguna"""
        self.setWindowTitle("Sample Kompresi Foto")
        self.setWindowIcon(QIcon(":/ai_appDefaultIcon"))
        self.resamplingAlgorithm.setCurrentIndex(1)

        for key, buttons in self.allScaleButton.items():
            if key == 0:
                for button in buttons: 
                    button.setIcon(QIcon(":/is_scaleUp"))

            elif key == 1:
                for button in buttons:
                    button.setIcon(QIcon(":/is_scaleDown"))
        
        for qButton in self.allUneditableLineEdit:
            qButton.setReadOnly(True)

    def chooseSamplePhoto(self):
        """Memungkinkan pengguna untuk memilih sample foto menggunakan file dialog"""
        foto = chooseFiles(self, "Pilih Sebuah Foto untuk Dijadikan Sampel")
        if foto != None:
            self.samplePhotoDir.setText(foto[0])
            self.processBeforeImage()

    def processBeforeImage(self):
        """Algoritma untuk berkomunikasi dengan QThread untuk memverifikasi file gambar"""
        self.imgVerifyWorker = ImgVerifyWorker(self.samplePhotoDir.text())
        self.imgVerifyWorker.imgSuccess.connect(self.imgVerifyWorker_onSuccess)
        self.imgVerifyWorker.imgError.connect(self.imgVerifyWorker_onError)
        self.imgVerifyWorker.finished.connect(self.imgVerifyWorker_onFinished)
        self.imgVerifyWorker.start()

    def imgVerifyWorker_onSuccess(self, qImage, fileExt, fileFormat, imgSize):
        """Fungsi yang ditrigger imgVerifyWorker saat 
        verifyRealPicture mengalami imgSuccess"""
        pixMapPtr = QPixmap.fromImage(qImage)
        if self.beforeCurrentImage != None:
            self.beforeScene.removeItem(self.beforeCurrentImage)
        self.beforeCurrentImage = self.beforeScene.addPixmap(pixMapPtr)
        self.beforeImage.fitInView(self.beforeImage.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        self.fileSize0.setText(humanReadableSize(imgSize))
        self.fileExt.setText(fileExt)
        self.fileFormat.setText(fileFormat)
        self.compressStatus.setText("Belum Dilakukan!")
        self.fileSize1.setText("-")
        self.sizeReduced.setText("-")
    
    def imgVerifyWorker_onError(self, errMsg):
        """Fungsi yang ditrigger oleh ImgVerifyWorker saat verifyRealPicture
        mengalami imgError"""
        self.imgVerifyErrorList.append(errMsg)

    def imgVerifyWorker_onFinished(self):
        """Fungsi yang ditrigger ImgVerifyWorker saat proses concurrent
        berhasil dan exit (untuk menghapus gambar lama dan set yang baru)"""
        if not len(self.imgVerifyErrorList) <= 0:
            _baseText = "Ups, gambar yang Anda pilih memicu kesalahan sebagai berikut:\n"
            for i, errMsg in enumerate(self.imgVerifyErrorList,1):
                _baseText = _baseText + f"{i}. {errMsg}.\n"
            showInfo(self, "Kami Ingin Menyampaikan Kabar Buruk", _baseText, 'error')
            self.imgVerifyErrorList.clear()

    def startCompressSample(self):
        """Menjalankan rangkaian proses kompresi normal pada secondary thread"""
        beforeImDir = self.samplePhotoDir.text()
        if len(beforeImDir) > 0 and os.path.isfile(beforeImDir):
            self.T_fetchSampleResult.start(500)
            self.T_compressStatusAnim.start(500)
            for qObject in self.allInteractable:
                qObject.setDisabled(True)
            self.sampleResultTempDir = tempfile.TemporaryDirectory(prefix="compressFile_", suffix="temp")
            self.compressSampleMP = Process(
                target=compressModule.compressImageHelper,
                args=(beforeImDir, self.sampleResultTempDir.name, self.resamplingAlgorithm.currentIndex(),
                    self.megaPixel.value()*1000000, self.photoQuality.value(), self.cConn)
            )
            self.compressSampleMP.start()
        
        else:
            showInfo(self, "Foto Belum Dipilih/Tidak Ada", "Sepertinya Anda belum memilih file foto apapun untuk dijadikan sampel kompresi atau file foto yang Anda pilih tidak tersedia. Silahkan cek kembali!", 'info')

    def checkPipeCompressSample(self):
        """Cek apakah foto sudah selesai dikompresi apa belum"""
        if self.pConn.poll():
            compressStatus, fileSize1, sizeSaved, outPath, _, _ = self.pConn.recv()
            self.T_fetchSampleResult.stop()
            self.T_compressStatusAnim.stop()

            if self.compressSampleMP.is_alive():
                self.compressSampleMP.kill()

            if compressStatus == 1:
                if self.afterCurrentImage != None:
                    self.afterScene.removeItem(self.afterCurrentImage)
                self.afterCurrentImage = self.afterScene.addPixmap(QPixmap(outPath))
                self.afterImage.fitInView(self.afterImage.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

                self.compressStatus.setText("Kompresi Berhasil")
                self.fileSize1.setText(humanReadableSize(fileSize1))
                self.sizeReduced.setText(humanReadableSize(sizeSaved))

            elif compressStatus == 2:
                self.compressStatus.setText("Kompresi Gagal!")

            else:
                self.compressStatus.setText("Terjadi Kesalahan!")

            self.sampleResultTempDir.cleanup()
            for qObject in self.allInteractable:
                qObject.setDisabled(False)
    
    def postCompressSample(self):
        """Re-enable pengaturan lagi"""
        for qObject in self.allNeedToWatched:
            qObject.setEnabled(True)

    def compressStatusAnim(self):
        """Untuk animasi titik titik loading dinamis saat kompresi berlangsung"""
        self.currentPos += 1
        if self.currentPos > 3:
            self.currentPos = 0
        self.compressStatus.setText("Memproses Kompresi" + "."*self.currentPos)
    
    def closeWindow(self):
        """Fungsi resmi dari WM Instance untuk menutup jendela aplikasi"""
        WM_.closeWindow(PCompressSampleTest)

    def closeEvent(self, event):
        event.ignore()
        jawaban = bringQuestion(self, "Konfirmasi Keluar?", "Anda yakin ingin keluar dari jendela ini? Proses kompresi belum dimulai!", 'question', 'yes', 'no')
        if jawaban == QMessageBox.Yes:
            self.closeWindow()

class CompressConfirmation(QMainWindow, compressConfirmation.Ui_MainWindow):
    doneAction = Signal()
    def __init__(self, upPassThrough:backend.UserPersonalization, dbPassThrough:backend.QNativeFileDatabase):
        super().__init__()
        self.setupUi(self)

        ##### PASSTHROUGH CONST #####
        self.userPersonalization = upPassThrough
        self.sqlDb = dbPassThrough

        ##### CONST FOR USER PERSONALIZATION #####
        self.allSaveFormat = (
            "JPEG", "JPG", "JPEG2000", "PNG",
            "HEIF", "HEIC", "WEBP", "BMP",
            "TIFF", "ICO", "AVIF"
        )
        self.defaultSavePath = os.path.join(os.environ["USERPROFILE"], "Downloads")

        ##### CONST FOR FILE DETAIL #####
        self.photoCategoryTableModel = QStandardItemModel(self)
        self.photoCategoryHeaderLabel = ["Format", "Jumlah Foto"]
        self.photoCategoryHeaderWidth = [80, 95]

        ##### USER MUSN'T INTERACT WITH #####
        self.allLineEdit = [self.readyCompress, self.cancelledPhoto, self.rejectedPhoto, self.megaPixel, self.photoQuality, self.saveLocation]
        self.allComboBox = [self.deleteOriginalFile, self.saveFormat, self.resamplingAlgorithm]
        
        ##### Call Init First
        self.initGUI()
        self.initUserSettings()
        self.initPhotoSummary()

        ##### Signal & Slots #####
        self.changeSettings.clicked.connect(self.openPersonalizationSettings)
        self.continueCompression.clicked.connect(self.onFinishedReview)

    ##### INIT CODE #####
    def initGUI(self):
        """Persiapkan beberapa pengaturan GUI untuk meningkatkan fungsionalitas dan UX"""
        self.setWindowTitle("Konfirmasi Kompresi File")
        self.setWindowIcon(QIcon(":/ai_appDefaultIcon"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        for qObject in self.allLineEdit:
            qObject.setReadOnly(True)
        for qObject in self.allComboBox:
            qObject.setDisabled(True)

        self.photoCategory.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.photoCategory.setModel(self.photoCategoryTableModel)
        self.photoCategory.verticalHeader().setVisible(False)
        self.photoCategoryTableModel.setHorizontalHeaderLabels(self.photoCategoryHeaderLabel)
        for i, width in enumerate(self.photoCategoryHeaderWidth):
            self.photoCategory.setColumnWidth(i, width)
    
    def initUserSettings(self):
        """Persiapkan dan tampilkan pengaturan pengguna yang disettings"""
        self.megaPixel.setValue(self.userPersonalization.getUserConfig('compressSettings',0))
        self.photoQuality.setValue(self.userPersonalization.getUserConfig('compressSettings',1))
        self.saveLocation.setText(self.userPersonalization.getUserConfig('compressSettings',2))
        self.deleteOriginalFile.setChecked(bool(self.userPersonalization.getUserConfig('compressSettings',4)))
        self.saveFormat.setCurrentIndex(self.allSaveFormat.index(self.userPersonalization.getUserConfig('compressSettings', 3)))
        self.resamplingAlgorithm.setCurrentIndex(self.userPersonalization.getUserConfig('compressSettings', 5))

        if self.saveLocation.text() == self.defaultSavePath:
           self.saveLocation.setToolTip("Folder default di 'Downloads/[Compressed-Tanggal]' untuk menyimpan hasil kompresi.")

    def initPhotoSummary(self):
        """Persiapkan dan tampilkan ringkasan file foto yang ingin dikompresi"""
        _readyToCompress = self.sqlDb.selectQuery(
            querySQL="SELECT fileDir FROM verifyFileTable WHERE isSupported = 1 AND isNotCorrupted = 1 AND isNotVirus = 1"
        )
        _rejected0 = self.sqlDb.selectQuery(
            querySQL="SELECT COUNT(*) FROM photoRejectedTable"
        )
        _rejected1 = self.sqlDb.selectQuery(
            querySQL="SELECT COUNT(*) FROM verifyFileTable WHERE isSupported != 1 OR isNotCorrupted != 1 OR isNotVirus != 1"
        )
        _cancelled = self.sqlDb.selectQuery(
            querySQL="SELECT COUNT(*) FROM photoCancelledTable"
        )
        _fileFormat = self.sqlDb.selectQuery(
            querySQL="SELECT fileFormat FROM verifyFileTable WHERE isSupported = 1 AND isNotCorrupted = 1 AND isNotVirus = 1"
        )
        allFileToCompress = [file[0] for file in _readyToCompress if os.path.isfile(file[0])]
        _allFileFormat = dict(Counter([fExt[0] for fExt in _fileFormat]))
        rejectedFile = _rejected0[0][0] + _rejected1[0][0]
        cancelled = _cancelled[0][0]

        self.readyCompress.setText(f"{len(allFileToCompress)} Foto")
        self.rejectedPhoto.setText(f"{rejectedFile} Foto")
        self.cancelledPhoto.setText(f"{cancelled} Foto")
        for photoFormat, jumlah in _allFileFormat.items():
            self.photoCategoryTableModel.appendRow(
                [makeStandardItem(photoFormat),
                 makeStandardItem(str(jumlah))]
            )
    
    def openPersonalizationSettings(self):
        """Buka pengaturan personalisasi pengguna"""
        _w = WM_.openWindow(PengaturanKompresi, self.userPersonalization)
        _w.show()
        self.closeWindow()

    def onFinishedReview(self):
        """Saat pengguna sudah yakin ingin lanjut"""
        jawaban = bringQuestion(self, "Konfirmasi Anda... Silahkan!", "Apakah Anda yakin ingin melajutkan menuju proses kompresi foto? Proses kompresi tidak akan dapat dihentikan setelah dimulai.", 'question', 'yes', 'no')
        if jawaban == QMessageBox.Yes:
            self.doneAction.emit()
            self.closeWindow()

    def closeWindow(self):
        """Fungsi official Window Manager Instance untuk menutup jendela"""
        WM_.closeWindow(CompressConfirmation)

    def closeEvent(self, event):
        self.closeWindow()

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