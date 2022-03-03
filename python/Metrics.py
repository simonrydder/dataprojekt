"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      Metrics.py

Discribtion:    Skabelon for nye filer.
"""

# Imports
import os
from DataPreparation import OAR_Image

# Import other files


# Classes and functions
class Metrics():
    def __inti__(self, ID, segment):
        self.PatientID = ID     # As id-type
        self.OAR = segment      # As string i.e. "Brainstem"
        self.Path = Path(self.PatientID)
        self.GT     = getImage("GT")    # Type OAR_Image from DataPreparation
        self.DL     = getImage("DL")    # Type OAR_Image from DataPreparation
        self.DLB    = getImage("DLB")   # Type OAR_Image from DataPreparation
        self.ATLAS  = getImage("ATLAS") # Type OAR_Image from DataPreparation
        self.DICE       = getVALUE("dice")     # Dictionary
        self.Hausdorff  = getHausdorff()     # Dictionary 
        self.MSD        = getMDS() # Dictionary
        self.APL        = getAPL() # Dictionary

    def getImage(self, method):
        File = datareader(self.PatientID, method)
        image = OAR_Image(File.getpath(), self.OAR)
        return image
    
    def getDICE(self):
        for img in [self.GT, self.DL, self.DLB, self.ATLAS]:
            # Create dictionary as {key : value} = {GT_DL = calculateDICE(self.GT, self.DL), GT_DLB = calculateDICE(self.GT, self.DLB)}
            
        return None # Created dictionary

    def getHausdorff(self):
        # Same priciple as getDICE() 
        return None

# Run file (optional)
