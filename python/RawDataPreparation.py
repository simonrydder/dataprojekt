"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      RawDataPreparation.py

Description:    Script to prepare the raw data and move it to the data folder in
                the dataprojekt folder. The main point is to align (slice) the 
                ATLAS segmentation dimentions to the 'ground truth' data.
                
                The script creates a indices.txt file which saves the starting
                indicis for chopping ATLAS segmentations. This file takes a very
                long time to generate, so don't delete it.
"""

# Initialization
print(f"Running {__name__}")


# Imports
import os, shutil, re
import SimpleITK as ITK
from progressbar import ProgressBar
from sys import exit

def myJoin(*args):
    return '\\'.join(args)


def copy(fro = 'A:\\raw', to = '..\\data\\data', vera = '..\\data\\projectdata.hc'):
    """
    Moves the raw data to datafolder on github.
    """
    mounted = False
    while not mounted:
        try: 
            folders = os.listdir(fro)
            mounted = True
        except FileNotFoundError:
            print('Unable to find directory: ' + fro)
            print('Opening VeraCrypt')            
            os.startfile(vera)
            str_input = input('Is data mounted? [N / Y]: ')
            mounted = True if str_input.lower() == 'y' else False
            if mounted:
                folders = os.listdir(fro)

    for folder in folders:
        src = myJoin(fro, folder)
        dst = myJoin(to, folder)
        if os.path.exists(dst):
            shutil.rmtree(dst)
            print(f'{dst} overwrited')
        shutil.copytree(src, dst)
    print()


def rename(location = '..\\data\\data', folder = 'ATLAS', extension = '.nii.gz'):
    """
    Renames the raw files to match the ID&Date.nii.gz standard.
    """

    files = os.listdir(myJoin(location, folder))
    files = list(filter(re.compile('.*&OAR_merged.*').match, files))

    ren = 0
    for file in files:
        id, date, _ = file.split('&')
        id = id.replace('.', '_')

        newfile = '&'.join([id, date]) + extension

        src = myJoin(location, folder, file)
        new = myJoin(location, folder, newfile)
        if src != new:
            os.rename(src, new)
            ren += 1
    
    print(f'{ren} files renamed of {len(files)} needing renaming\n')


def remove(root = '..\\data\\data'):
    """
    Remove files where model dimentions don't match GT.
    """

    def getFileInfo(file):
        try:
            img = ITK.ReadImage(file)
        except RuntimeError:
            Size = (None, None, None)
            Origin = (None, None, None)
        else:
            Size = img.GetSize()
            Origin = img.GetOrigin()

        return Size, Origin
    

    def validFile(file1, file2):
        i1 = getFileInfo(file1)
        i2 = getFileInfo(file2)

        for val1, val2 in zip(i1, i2):
            if val1 != val2:
                return False

        return True

    rem = 0
    with open(myJoin(root, 'removed.txt'), mode = 'w') as f:

        for method in ['ATLAS', 'DL', 'DLB']:
            f.write(method + ':\n')
            m = myJoin(root, method)
            gt = myJoin(root, method + '_GT')

            if len(os.listdir(m)) > len(os.listdir(gt)):
                files = os.listdir(m)
            else:
                files = os.listdir(gt)

            for file in files:
                f1 = myJoin(m, file)
                f2 = myJoin(gt, file)
                if not validFile(f1, f2):
                    f.write(file + '\n')
                    try:
                        os.remove(f1)
                        rem += 1
                    except FileNotFoundError:
                        pass
            
            f.write('\n')
    print(f"{rem} files removed.. file names saved to 'removed.txt'\n")


def findingIndex(A, D):
    """
    A is the array of the too large ATLAS (GT) segmentation and D is the array
    of a correct size DL or DLB (GT) segmentation.
    Returns (None, None, None) if the two arrays don't overlap.
    """
    zA, yA, xA = A.shape
    zD, yD, xD = D.shape
    # z, y, x = 0, 0, 0
    # print(A[z : z + zD, y : y + yD, x : x + xD].shape)
    for z in range(zA - zD + 1):
        print(f'{z}/{zA - zD} z iterations')
        pbar = ProgressBar()
        for y in pbar(range(yA - yD + 1)):
            for x in range(xA - xD + 1):
                if (A[z : z + zD, y : y + yD, x : x + xD] == D).all():
                    return (z, y, x)
    
    return (None, None, None)


def saveindices(root = '..\\data\\data', out = 'indices.txt', overwrite = False):
    """
    Saves the indices of where to chop the ATLAS for each file in indices.txt.
    """

    dir = myJoin(root, out)
    exit_now = False
    try:
        if overwrite:
            raise FileNotFoundError

        with open(dir) as f:
            lines = f.readlines()
            saved = {line.split(',')[0] for line in lines}

    except FileNotFoundError:
        saved = set()
        with open(dir, 'w') as f:
            pass

    notsaved = {file for file in os.listdir(myJoin(root, 'ATLAS'))} - saved
    notsaved = sorted(list(notsaved))

    with open(dir,'a') as f:
        for file in notsaved:
            pA = myJoin(root, 'ATLAS_GT', file)
            pD = myJoin(root, 'DL_GT', file)

            A = ITK.GetArrayFromImage(ITK.ReadImage(pA))
            D = ITK.GetArrayFromImage(ITK.ReadImage(pD))

            print(file)
            try:
                z, y, x = findingIndex(A, D)
            except KeyboardInterrupt:
                print('Shutdown requested.. exiting')
                exit_now = True
                break
            
            line = f'{file},{x},{y},{z}\n'
            f.write(line)
            print()

    if exit_now == True:
        exit()
        

def getindices(root = '..\\data\\data'):
    with open(myJoin(root, 'indices.txt')) as f:
        lines = f.readlines()
        dct = {}
        for line in lines:
            file, x, y, z = line[:-1].split(',')
            dct[file] = (int(x), int(y), int(z))
        
    return dct


def chop(root = '..\\data\\data\\ATLAS', correct = '..\\data\\data\\DL'):
    print('Chopping data')
    dct = getindices()

    for file in os.listdir(root):
        dst = myJoin(root, file)

        img = ITK.ReadImage(dst)
        src = ITK.ReadImage(myJoin(correct, file))
        
        if src.GetSize() != img.GetSize() or src.GetOrigin() != src.GetOrigin():
            x, y, z = dct[file]
            x_, y_, z_ = src.GetSize()
            
            arr = ITK.GetArrayFromImage(img)
            arr = arr[z : z + z_, y : y + y_, x : x + x_]
            img = ITK.GetImageFromArray(arr)
            img.CopyInformation(src)

            ITK.WriteImage(img, dst)
        else:
            print(f'{file} already correct dimensions and origin')


def finalize(root = '..\\data\\data', gt_folder = 'DL_GT'):
    for folder in os.listdir(root):
        src = root + '\\' + folder
        if '_GT' in folder:
            if folder == gt_folder:
                os.rename(src, root + '\\GT')
            else:
                shutil.rmtree(src)


if __name__ == '__main__':
    copy()
    rename()
    remove()
    saveindices()
    chop()
    finalize()
    pass




# location = 'A:\\data'
# model = ['GT', 'DL', 'DLB', 'ATLAS', 'AGT']
# file = '0ku1qeiExUvrl65s5bvTX5fKA&20140505.nii.gz'
# for file in os.listdir(myJoin(location, 'GT'))[:3]:
#     print(file)
    
#     GT = myJoin(location, 'GT', file)
#     ATLAS = myJoin(location, 'agt', file)

#     imgGT = ITK.ReadImage(GT)
#     imgA = ITK.ReadImage(ATLAS)

#     oGT = imgGT.GetOrigin()
#     oA = imgA.GetOrigin()
#     diffO = [a - b for a, b in zip(oGT, oA)]
#     print(oGT, oA, diffO)

#     sGT = imgGT.GetSize()
#     sA = imgA.GetSize()
#     diffS = [b - a for a, b in zip(sGT, sA)]
#     print(sGT, sA, diffS)

#     spacing = [a - b for a, b in zip(imgGT.GetSpacing(), imgA.GetSpacing())]
#     print('Spacing: ', spacing)
    

#     totalDiff = [a - b for a, b in zip(diffO, diffS)]

#     print(diffO, diffS, totalDiff)
#     print()
        