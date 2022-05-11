# from DataPreparation import OAR_Image
# from DataReader import Path
import numpy as np
from progressbar import ProgressBar
import SimpleITK as ITK
import os
from itertools import islice

def getFileInfo(file):
    try:
        img = ITK.ReadImage(file)
    except RuntimeError:
        Size = (None, None, None)
        Origin = (None, None, None)
    else:
        Size = img.GetSize()
        Origin = img.GetOrigin()

    return {'Size' : Size, 'Origin' : Origin}


def fileNameGenerator(location = 'A:\\raw\\ATLAS'):
    yield from os.listdir(location)


def folderLoop(file, folders, root = 'A:\\raw'):
    mydict = dict()
    for folder in folders:
        location = '\\'.join([root, folder, file])
        info = getFileInfo(location)
        mydict[folder] = info
    
    return mydict


def dctstr(d):
    msg = ''
    for folder, info in d.items():
        msg += f'{folder}:'.ljust(10)
        for key, value in info.items():
            msg += f'{key} = {value}'.ljust(28)
        msg += '\n'

    return msg


def validFile(dct):
    m = list(dct.items())[::2]
    gt = list(dct.items())[1::2]

    for (_, a), (_, b) in zip(m, gt):
        for v1, v2 in zip(list(a.values()), list(b.values())):
            if v1 != v2:
                return False

    return True


def writeCorruptedFiles(d, location = 'A:\\raw\\', file = 'CorruptedInfo.txt', overwrite = True):
    mode = 'w' if overwrite else 'a'
    nFiles = 0
    msg = ''
    with open(location + file, mode) as f:
        for dFile, fInfo in d.items():
            if not validFile(fInfo):
                nFiles += 1
                msg += dFile + '\n'
                msg += dctstr(fInfo) + '\n'
                print(dctstr(fInfo))
            else:
                pass
        
        f.write(f'{nFiles} invalid file(s):\n\n')
        f.write(msg)


if __name__ == '__main__':
    dct = dict()
    for file in fileNameGenerator():
        print(file)
        fInfo = folderLoop(file, ['ATLAS', 'A_GT', 'DL', 'DL_GT', 'DLB', 'DLB_GT'])
        dct[file] = fInfo

    writeCorruptedFiles(dct)