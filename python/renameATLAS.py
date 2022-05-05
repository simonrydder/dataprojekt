import os
import re


def main(location = 'A:\\data', folder = 'ATLAS', extension = '.nii.gz'):
    files = os.listdir('\\'.join([location, folder]))
    files = list(filter(re.compile('.*&OAR_merged.*').match, files))
    len(files)
    for file in files:
        id, date, _ = file.split('&')
        id = id.replace('.', '_')

        newfile = '&'.join([id, date]) + extension

        source = '\\'.join([location, folder, file])
        new = '\\'.join([location, folder, newfile])
        os.rename(source, new)

if __name__ == '__main__':
    main()
