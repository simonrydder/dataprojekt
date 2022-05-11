"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      DataReader.py

Description:    Class to find the path for all relevant segmentations related to
                a specific patient ID on a specific Date.
                
                Datareader requires one patient ID and the date of scan to be 
                specified and has the following attributes:
                - GT:   The path to "Ground Truth" segmentations
                - DL:   The path to Deep learning without bounds segmentations
                - DLB:  The path to Deep learning with bounds segmentations
                - ATLAS:The path to ATLAS based segmentations
"""

# Initialization
print(f"Running {__name__}")


# Imports
import os


# Classes and functions
class Path():
    def __init__(self, ID : str = '',
                 Date : str = '',
                 Method : str = '',
                 Root = '..\\data\\data'):

        assert isinstance(ID, str), 'ID not <class str>'
        assert isinstance(Date, str), 'Data not <class str>'
        assert isinstance(Method, str), 'Method not <class str>'
        assert isinstance(Root, str), 'Root not <class str>'

        self.ID = ID
        self.Date = Date    # yyyymmdd
        self.Root = Root    # location of encrypted data
        self.Method = Method.upper()    # "GT", "DL", "DLB", "ATLAS"
        self.File = self.GetFile()

    def __str__(self):
        msg = (
            f'ID: {self.ID}\n'
            f'Date: {self.Date}\n'
            f'Method: {self.Method}\n'
            f'File: {self.File}'
        ) 
        return msg


    def GetFile(self):
        try:
            files = os.listdir(self.Root + '\\' + self.Method)

        except FileNotFoundError:
            return 'NA'
            
        for file in files:
            if self.ID + '&' + self.Date in file:
                return self.Root +'\\' + self.Method + "\\" + file
            
        return 'NA'


# Class tester
if __name__ == "__main__":
    tests = {'Test1' : ["1cbDrFdyzAXjFICMJ58Hmja9U",
                        20130521,
                        'GT'],
             'Test2' : ["1cbDrFdyzAXjFICMJ58Hmja9U",
                        '20130521',
                        'GT'],
             'Test3' : ["1cbDrFdyzAXjFICMJ58Hmja9U",
                        '20130521',
                        'DL'],
             'Test4' : ["1cbDrFdyzAXjFICMJ58Hmja9U",
                        '20130521',
                        'DLB'],
             'Test5' : ["1cbDrFdyzAXjFICMJ58Hmja9U",
                        '20130521',
                        'ATLAS'],
             'Test6' : ["notExsisting",
                        '20130521',
                        'ATLAS']
            }

    for test, args in tests.items():
        try:
            PI = Path(*args)
            print(f'{test} succeded')
            print(PI)
        except:
            print(f'{test} failed')
            for arg in args:
                print(f'Argument: {arg} : {type(arg)}', end = '\n')
        finally:
            print()

    print("Test Path():")
    P = Path()
    print(P)