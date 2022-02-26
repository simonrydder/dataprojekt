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
import SimpleITK as ITK


class datareader:
    def __init__(self, ID):
        self.ID = ID
        self.root = "A:\\"
        self.paths = {"GT":"Task5041_OARBoundsMergedDSCTOnly\\cts\\labels",
                      "DL":"Task5041_OARBoundsMergedDSCTOnly\\fold_0",
                      "DLB":"Task5031_OARBoundsMergedDS\\fold_0"} # Add atlas
        
        for key, path in self.paths.items():
            self.exists = False 
            for f in os.listdir(self.root + path):
                if ID in f:
                    setattr(self,key,self.root + path + "\\" + f)
                    self.exists = True
                    break
            if not self.exists:
                raise ValueError("No image found for " + key + ", Check patient ID is correct")




ID = "1cbDrFdyzAXjFICMJ58Hmja9U"     

x = datareader(ID)
x.DL
x.DLB
x.GT

