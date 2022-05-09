import os
import re
import SimpleITK as ITK
from progressbar import ProgressBar

def myJoin(*args):
    return '\\'.join(args)

def rename(location = 'A:\\data', folder = 'ATLAS', extension = '.nii.gz'):
    files = os.listdir(myJoin(location, folder))
    files = list(filter(re.compile('.*&OAR_merged.*').match, files))
    len(files)
    for file in files:
        id, date, _ = file.split('&')
        id = id.replace('.', '_')

        newfile = '&'.join([id, date]) + extension

        source = myJoin(location, folder, file)
        new = myJoin(location, folder, newfile)
        os.rename(source, new)

def findingIndex(A, D):
    zA, yA, xA = A.shape
    zD, yD, xD = D.shape
    z, y, x = 0, 0, 0
    print(A[z : z + zD, y : y + yD, x : x + xD].shape)

    print(zA - zD, yA - yD, xA - xD)
    for z in range(zA - zD + 1):
        pbar = ProgressBar()
        for y in pbar(range(yA - yD + 1)):
            for x in range(xA - xD + 1):
                if (A[z : z + zD, y : y + yD, x : x + xD] == D).all():
                    return (z, y, x)
    
    return (0, 0, 0)


def editATLAS(location = 'A:\\data'):
    shift = (198, 128, 0) # hardcoded 4Prj... (x, y, z)

    missingATLAS = []
    for file in os.listdir(myJoin(location, 'GT')):
        print(file)
        GT = myJoin(location, 'GT', file)
        ATLAS = myJoin(location, 'AGT', file)

        try:
            imgGT = ITK.ReadImage(GT)
        except FileNotFoundError:
            print(f'The GT file {file} does not exsists. Skipping..')
            continue

        try:
            imgATLAS = ITK.ReadImage(ATLAS)
        except FileNotFoundError:
            print(f'The ATLAS file {file} does not exsists. Skipping..')
            missingATLAS.append(file)
            continue
        
        size = imgGT.GetSize()
        to = [a + b for a, b in zip(shift, size)]
        
        array = ITK.GetArrayFromImage(imgATLAS)
        array = array[shift[2]:to[2], shift[1]:to[1], shift[0]:to[0]]
        imgA = ITK.GetImageFromArray(array)
        
        print(size, imgA.GetSize(), imgATLAS.GetSize())
        imgA.CopyInformation(imgGT)
        ITK.WriteImage(imgA, ATLAS)
    
    print(f'Total missing files: {len(missingATLAS)}')

if __name__ == '__main__':
    rename()
    # editATLAS()
    pass


location = 'A:\\data'
model = ['GT', 'DL', 'DLB', 'ATLAS', 'AGT']
file = '0ku1qeiExUvrl65s5bvTX5fKA&20140505.nii.gz'
for file in os.listdir(myJoin(location, 'GT'))[:3]:
    print(file)
    
    GT = myJoin(location, 'GT', file)
    ATLAS = myJoin(location, 'agt', file)

    imgGT = ITK.ReadImage(GT)
    imgA = ITK.ReadImage(ATLAS)

    oGT = imgGT.GetOrigin()
    oA = imgA.GetOrigin()
    diffO = [a - b for a, b in zip(oGT, oA)]
    print(oGT, oA, diffO)

    sGT = imgGT.GetSize()
    sA = imgA.GetSize()
    diffS = [b - a for a, b in zip(sGT, sA)]
    print(sGT, sA, diffS)

    spacing = [a - b for a, b in zip(imgGT.GetSpacing(), imgA.GetSpacing())]
    print('Spacing: ', spacing)
    

    totalDiff = [a - b for a, b in zip(diffO, diffS)]

    print(diffO, diffS, totalDiff)
    print()
        