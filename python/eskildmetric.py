
from DataReader import Path
import DataPreparation

# Classes and functions
class Metrics():
    def __init__(self, ID, segment):
        self.PatientID = ID     # As id-type
        self.OAR = segment      # As string i.e. "Brainstem"
        #self.Path = Path(self.PatientID)
        self.GT     = self.getImage("GT")    # Type OAR_Image from DataPreparation
        self.DL     = self.getImage("DL")    # Type OAR_Image from DataPreparation
        self.DLB    = self.getImage("DLB")   # Type OAR_Image from DataPreparation
        #self.ATLAS  = self.getImage("ATLAS") # Type OAR_Image from DataPreparation
        self.DICE       = self.getDICE()     # Dictionary
        self.Hausdorff  = self.getHausdorff()     # Dictionary 
        self.MSD        = self.getMDS() # Dictionary
        self.APL        = self.getAPL() # Dictionary

    def getImage(self, method):
        x = Path(self.PatientID, method)
        image = DataPreparation.OAR_Image(x.File, self.OAR)
        return image
    
    def getDICE(self):
        for img in [self.GT, self.DL]:
            
            # Create dictionary as {key : value} = {GT_DL = calculateDICE(self.GT, self.DL), GT_DLB = calculateDICE(self.GT, self.DLB)}
            
        return None # Created dictionary

    def getHausdorff(self):
        # Same priciple as getDICE() 
        return None
    
    def getMDS(self):
        # Same priciple as getDICE() 
        return None

    def getAPL(self):
        # Same priciple as getDICE() 
        return None


# Run file (optional)

ID = "1cbDrFdyzAXjFICMJ58Hmja9U"     
segment = "bRainStem"
#x = Path(ID, "GT")
#x.File
x = Metrics(ID, segment)
