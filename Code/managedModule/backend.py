import os, sys, json
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PIL import Image

class fileDatabase:
    def __init__(self):
        self.fileDatabase = QSqlDatabase.addDatabase("QSQLITE")
        self.fileDatabase.setDatabaseName(":memory:")
        self.fileDatabase.open()

        self.dbQuery = QSqlQuery(db=self.fileDatabase)
        self.qCreateTable = [
############################ ADA YANG SALAH NJIR NJIR BUKAN SEG-FAULT TAPI.... BIKIN SAKIT HATI
############################ BESOK PAS MATA UDAH MELEK, DICEK LAGI YA GAUSAH BURU BURU 
############################ HUFFFFF CAPEK KODING, TAPI ASIK SIH?! CAPEK TAPI 
"""CREATE TABLE IF NOT EXISTS newFileTable(id INTEGER PRIMARY KEY, fileName TEXT NOT NULL, fileDir TEXT NOT NULL, fileExt TEXT NOT NULL)""",

"""CREATE TABLE IF NOT EXISTS newFolderTable(id INTEGER PRIMARY KEY, folderName TEXT NOT NULL, folderPath TEXT NOT NULL)""",

"""CREATE TABLE IF NOT EXISTS fileJobTable(id INTEGER PRIMARY KEY, fileName TEXT NOT NULL, fileDir TEXT NOT NULL, fileExt TEXT NOT NULL)""",

"""CREATE TABLE IF NOT EXISTS verifyFileTable(id INTEGER PRIMARY KEY, fileName TEXT NOT NULL, fileDir TEXT NOT NULL, fileExt TEXT NOT NULL,
fileFormat TEXT DEFAULT '-', isSupported INTEGER DEFAULT 0, isNotCorrupted INTEGER DEFAULT 0, isNotVirus INTEGER DEFAULT 0, fileSize0 FLOAT DEFAULT 0.00)""",

"""CREATE TABLE IF NOT EXISTS compressedFileTable(
id INTEGER PRIMARY KEY, fileName TEXT NOT NULL, fileDir TEXT NOT NULL, fileExt TEXT NOT NULL, fileFormat TEXT NOT NULL, isSupported INTEGER NOT NULL,
isNotCorrupted INTEGER NOT NULL, isNotVirus INTEGER NOT NULL, fileSize0 FLOAT NOT NULL, fileSize1 FLOAT DEFAULT 0.00, sizeReduced FLOAT DEFAULT 0.00,
savePath TEXT DEFAULT '-', isDeleted INTEGER DEFAULT 0)""",

"""CREATE TRIGGER IF NOT EXISTS onFileJobInserted
AFTER INSERT ON fileJobTable
BEGIN
    INSERT INTO verifyFileTable(fileName, fileDir, fileExt)
    VALUES (NEW.fileName, NEW.fileDir, NEW.fileExt);
END;""",

"""CREATE TRIGGER IF NOT EXISTS verifyFile_isUpdated
AFTER UPDATE OF fileFormat on verifyFileTable
FOR EACH ROW
BEGIN
    UPDATE compressedFileTable
    SET fileFormat = NEW.fileFormat,
        isSupported = NEW.isSupported,
        isNotCorrupted = NEW.isNotCorrupted,
        isNotVirus = NEW.isNotVirus,
        fileSize0 = NEW.fileSize0
    WHERE fileName = NEW.fileName;
END;"""
        ]
        for qSql in self.qCreateTable:
            self.dbQuery.exec(qSql)

    def executeQuery(self, querySQL, params=None, isMultipleParams=False):
        self.fileDatabase.transaction()
        self.dbQuery.prepare(querySQL)

        def runExec():
            if self.dbQuery.exec():
                self.fileDatabase.commit()
                return True

            else:
                self.fileDatabase.rollback()
                return False

        if params:
            if isMultipleParams:
                for nPrm in params:
                    for v in nPrm:
                        self.dbQuery.addBindValue(v)
                    if not runExec():
                        raise Exception(f"DB Rollback Success: {self.dbQuery.lastError().text()}")

            elif not isMultipleParams:
                for v in params:
                    self.dbQuery.addBindValue(v)
                if not runExec():
                    raise Exception(f"DB Rollback Success: {self.dbQuery.lastError().text()}")

        else:
            if not runExec():
                raise Exception(f"DB Rollback Success: {self.dbQuery.lastError().text()}")

    def selectQuery(self, querySQL):
        self.dbQuery.prepare(querySQL)
        if not self.dbQuery.exec():
            raise Exception(f"Select Error: {self.dbQuery.lastError().text()}")
        _result = []
        while self.dbQuery.next():
            _result.append(tuple(
                self.dbQuery.value(i) for i in range(self.dbQuery.record().count())
            ))
        return _result

def verifyImageFile(filePath):
    """return nama file, ukuran awal, ekstensi file, format file, dukungan, tidak corrupt, bukan virus (0 uncheck 1 true 2 false)"""
    namaFile = ""
    ukuranAwal = 0
    ekstensiFile = "!"
    formatFile = "!"
    dukunganFile = 0
    tidakCorrupt = 0
    bukanVirus = 0

    ###### Constant ######
    supportedExtension = ['.jpg', '.jpeg', '.png', '.webp', 'mpo', '.heic', '.heif']
    supportedFormat = ['JPG', 'JPEG', 'PNG', 'WEBP', 'MPO', 'HEIC', 'HEIF']

    ###### First Step adalah Cek Nama dan Ukuran File ######
    namaFile = os.path.basename(filePath)
    ukuranAwal = os.path.getsize(filePath)

    try:
        imgPtr = Image.open(filePath)
        imgFormat = imgPtr.format

        ###### Second Step adalah PIL.Image.Load() dengan .verify() #######
        imgPtr.verify()
        if imgPtr:
            imgPtr.close()
        tidakCorrupt = 1

        imgPtr = Image.open(filePath)
        imgPtr.load()
        bukanVirus = 1

        ###### Third Step adalah cek Format gambar ######
        fExtension = os.path.splitext(filePath)[1].lower()
        if fExtension in supportedExtension:
            if imgFormat in supportedFormat:
                ekstensiFile = fExtension
                formatFile = imgFormat
                dukunganFile = 1

            else:
                formatFile = "✗ (Tidak Didukung)"
        else:
            ekstensiFile = "✗ (Tidak Didukung)"

    except (IOError, SyntaxError) as e:
        tidakCorrupt = 2

    except (Image.DecompressionBombWarning, Image.DecompressionBombError) as e:
        bukanVirus = 2

    if imgPtr:
        imgPtr.close()
        del imgPtr
    return (ekstensiFile, formatFile, ukuranAwal, dukunganFile, tidakCorrupt, bukanVirus, namaFile)

def returnAllFileFromPath(dirs:list, conn):
    """Return a list of file from a dir, also verify is file exists and file in valid image extension"""
    allFile = []
    validExt = [".jpg", ".jpeg", ".png"]
    for dir in dirs:
        for root, _, files in os.walk(dir):
            for file in files:
                fullPath = os.path.join(root, file)
                if os.path.isfile(fullPath) and os.path.splitext(fullPath)[1].lower() in validExt:
                    allFile.append(os.path.normpath(os.path.join(root, file)))
                else:
                    pass
    conn.send(allFile)
    conn.close()

def onFirstRun():
    defaultConfig = {
        "appSettings" : {"threadUsage": 0, "threadUsageUserDefinied": 0, "isAutoStartup": 0}
    }
    maindir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    configFile = os.path.join(maindir, "config.json")
    if not os.path.isfile(configFile): # rewrite the config if not found
        fPtr = open(configFile, "w")
        json.dump(defaultConfig, fPtr)
        fPtr.close()
    pass