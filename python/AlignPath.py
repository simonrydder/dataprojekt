"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: AlignPath.ipynb

Discribtion: Aligns the working directory for the users.
"""

# Imports
import os

# Classes and functions
class AlignPath():
    def __init__(self):
        self.FileName = "AlignPath.py"
        self.OriginalWD = self.OriginalPath()
        self.CurrentWD = self.OriginalWD
        self.VeraCryptLocation = '..\\data\\projectdata.hc' #'..\\data\\readme.txt'
    
    def __str__(self):
        if self.OriginalWD == self.CurrentWD:
            return 'CurrentWD:\t' + self.CurrentWD
        else:
            return 'OriginalWD:\t' + self.OriginalWD + '\n' + 'CurrentWD:\t' + self.CurrentWD
    
    def OriginalPath(self):

        for root, dirs, files in os.walk(r'C:\\'):
            for name in files:
                if name == self.FileName:
                    return os.path.abspath(root)

    def GetWD(self):
        return os.getcwd()
    
    def SetWD(self, path = "A:\\"):
        notMounted = True
        while notMounted:
            try: 
                os.chdir(path)
                notMounted = False
            except FileNotFoundError:
                print('Unable to find directory: ' + path)
                print('Opening VeraCrypt')            
                os.startfile(self.VeraCryptLocation)
                str_input = input('Is data mounted? [N / Y]: ')
                notMounted = False if str_input.lower() == 'y' else True
                if notMounted == False:
                    os.chdir(path)
        # End while   
        
        print('Path have been updated')
        self.CurrentWD = self.GetWD()
        print(self)

# Run file
print(os.getcwd())
myPath = AlignPath()
print(myPath)
myPath.SetWD()


