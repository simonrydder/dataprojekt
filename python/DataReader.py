"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: DataReader.py


description: Class to find the path for all relevant segmentations related to a specific patient ID

Datareader requires one patient ID to be specified and has the following attributes

GT: The path to "Ground Truth" segmentations
DL: The path to Deep learning without bounds segmentations
DLB: The path to Deep learning with bounds segmentations
ATLAS: The path to ATLAS based segmentations

"""
# Imports
import os
from time import sleep

# Classes and functions
class Path():
    def __init__(self, ID, method):
        self.ID = ID
        self.Root = "A:\\data\\"
        self.Method = method    # "GT", "DL", "DLB", "ATLAS"
        self.VeraCryptLocation = '..\\data\\projectdata.hc'
        self.File = self.getPath()
        

    def getPath(self):
        notMounted = True
        while notMounted:
            try:
                files = os.listdir(self.Root + self.Method)
                notMounted = False
            except FileNotFoundError:
                print('Unable to find directory: ' + self.Root)
                print('Opening VeraCrypt')            
                os.startfile(self.VeraCryptLocation)
                str_input = input('Is data mounted? [N / Y]: ')
                notMounted = False if str_input.lower() == 'y' else True
                if notMounted == False:
                    files = os.listdir(self.Root + self.Method)
        

        for file in files:
            if self.ID in file:
                return self.Root + self.Method + "\\" + file
            
        raise FileNotFoundError(f'File not found for {self.ID}, {self.Method}')


# Test
ID = "1cbDrFdyzAXjFICMJ58Hmja9U"     
print(Path(ID, "GT").File)