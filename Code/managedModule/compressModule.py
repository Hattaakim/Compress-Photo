import os, math, io
from PIL import Image, ImageFile, ImageOps
import pillow_heif

#antisipasi file rusak
ImageFile.LOAD_TRUNCATED_IMAGES = True
#untuk gambar HEIF/HEIC
pillow_heif.register_heif_opener()

def compressImageHelper(filePath, outDir, resamplingAlgorithm,
                  megaPixel, quality, cConn):
    """Helper function to access compressImage when doing compressSample"""
    if isinstance(filePath, bytes):
        filePath = io.BytesIO(filePath)
    cConn.send(compressImage(filePath, outDir, resamplingAlgorithm, megaPixel, quality, False))
    cConn.close()

def compressImage(filePath, outDir, resamplingAlgorithm=1,
                  megaPixel:int=12_000_000, quality:int=85,
                  saveFormat:str='JPEG',deleteOriginal:bool=False):
    ##### Variable
    fileName = ""
    outPath = ""
    processStats = {"compressionStatus": 0,
                    "fileSizeAwal": 0.00,
                    "fileSizeAkhir": 0.00,
                    "penghematanUkuran": 0.00,
                    "fileDeleted": 2 if deleteOriginal == False else 0}
    allResampling = {0: Image.Resampling.NEAREST,
                   1: Image.Resampling.LANCZOS,
                   2: Image.Resampling.BILINEAR,
                   3: Image.Resampling.BICUBIC,
                   4: Image.Resampling.BOX,
                   5: Image.Resampling.HAMMING,
                   6: Image.Resampling.MKS2013,
                   7: Image.Resampling.MKS2021}

    #### Process the file identity
    if os.path.isfile(filePath) and os.path.isdir(outDir):
        fileName = os.path.basename(filePath)
        outPath = os.path.join(outDir, f"{os.path.splitext(fileName)[0]}-Compressed.{saveFormat.lower()}")
        processStats["fileSizeAwal"] = os.path.getsize(filePath)

    else:
        processStats['compressionStatus'] = 2
        return (processStats['compressionStatus'], processStats['fileSizeAkhir'], processStats['penghematanUkuran'], outPath, processStats['fileDeleted'], fileName)

    try:
        imgObj = Image.open(filePath)
        imgObj = ImageOps.exif_transpose(imgObj)
        if imgObj.mode in ('RGBA', 'LA') or (imgObj.mode == 'P' and 'transparency'
                                                in imgObj.info):
            alpha = imgObj.convert('RGBA').split()[-1]
            emptyBg = Image.new("RGB", imgObj.size, (255,255,255))
            emptyBg.paste(imgObj, mask=alpha)
            imgObj = emptyBg
        elif imgObj.mode != 'RGB':
            imgObj = imgObj.convert('RGB')

        w,h = imgObj.size
        currentPixels = w*h
        if currentPixels > megaPixel:
            rasio = math.sqrt(megaPixel/currentPixels)
            widthBaru = int(w*rasio)
            heightBaru = int(h*rasio)
            imgObj = imgObj.resize((widthBaru, heightBaru), resample=allResampling[resamplingAlgorithm])

        imgObj.save(outPath, saveFormat,
                    quality=quality, optimize=True)
        imgObj.close()
        processStats['compressionStatus'] = 1
        processStats['fileSizeAkhir'] = os.path.getsize(outPath)
        processStats['penghematanUkuran'] = processStats['fileSizeAwal'] - processStats['fileSizeAkhir']

        if deleteOriginal:
            os.remove(filePath)
            processStats['fileDeleted'] = 1

        return (processStats['compressionStatus'], processStats['fileSizeAkhir'], processStats['penghematanUkuran'], outPath, processStats['fileDeleted'], fileName)

    except Exception:
        processStats['compressionStatus'] = 2
        return (processStats['compressionStatus'], processStats['fileSizeAkhir'], processStats['penghematanUkuran'], outPath, processStats['fileDeleted'], fileName)