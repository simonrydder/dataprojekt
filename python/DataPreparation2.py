"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        27/02/2022

File name:      DataPreparation.py

Discribtion:    Implements the class OAR. The class takes the inputs: 
                - Path <class 'Path'>, 
                - OAR_name <class 'str'>
                and creates an image of only the needed OAR with the same origin,
                direction, spacing and shape. The class also includes functions:
                - GetArray (to get the images as an array)
                - SaveArrayAsImage (to save a given array with the same proper-
                ties as the original image).
"""

# Initialization
print(f"Running {__name__}")


# Imports
import SimpleITK as ITK
import numpy as np
 

# Import of other files
from DataReader2 import Path


# Classes and functions
class OAR_Image():
    # Class static attribute
    OARs = {"background" : 0,
            "brain" : 1,
            "brainstem" : 2,
            "spinalcord" : 3,
            "lips" : 4,
            "esophagus" : 5,
            "parotid_merged" : 6,
            "pcm_low" : 7,
            "pcm_mid" : 8,
            "pcm_up" : 9,
            "mandible" : 10,
            "submandibular_merged" : 11,
            "thyroid" : 12,
            "opticNerve_merged" : 13,
            "eyefront_merged" : 14,
            "eyeback_merged" :15}

    def __init__(self, Path : Path = Path(), OAR_name : str = ''):
        self.Path = Path
        self.OAR = OAR_name.lower()
        self.Origin = None
        self.Direction = None
        self.Spacing = None
        self.Shape = None       # x, y, z
        self.Exists = False
        self.Image = self.GetImage()
        

    def __str__(self):
        exists = f'exists' if self.Exists else f'does not exist'
        msg = (
            f'OAR: {self.OAR} {exists}\n'
            f'Image (x, y, z): {self.Shape}'
        )
        return msg


    def GetSegment(self):
        return self.OARs.get(self.OAR)
    

    def GetImage(self):

        try: 
            # Read image
            img = ITK.ReadImage(self.Path.File)
        
        except:
            # Create empty array if file don't exists
            array = np.zeros((3,3,3))
            img = ITK.GetImageFromArray(array)

        
        # Read properties
        self.Origin = img.GetOrigin()
        self.Direction = img.GetDirection()
        self.Spacing = img.GetSpacing()
        self.Shape = img.GetSize()

        # Transform Image to Array
        array = ITK.GetArrayFromImage(img)

        # Retransform Array to Image
        img = ITK.GetImageFromArray(array)
        img.SetDirection(self.Direction)
        img.SetOrigin(self.Origin)
        img.SetSpacing(self.Spacing)

    
        # Replace all values unequal to SegmentNo with 0.
        array = np.where(array == self.GetSegment(), array, 0)

        # Check if segment exists
        if not np.all(array == 0):
            self.Exists = True

        return img


    def GetArray(self):
        return ITK.GetArrayFromImage(self.Image)


    def SaveImage(self, path):
        ITK.WriteImage(self.Image, path)


    def SaveArrayAsImage(self, array, path):
        # Creating image from array
        img = ITK.GetImageFromArray(array)

        # Implementing original image info to array image.
        img.SetDirection(self.Direction)
        img.SetOrigin(self.Origin)
        img.SetSpacing(self.Spacing)

        # Writing Image to file
        ITK.WriteImage(img, path)


# Test
if __name__ == "__main__":
    from time import time

    PI1 = Path('1cbDrFdyzAXjFICMJ58Hmja9U', '20130521','GT') # Without pcm
    PI2 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129','GT') # With pcm

    tests = {'Test1' : [PI1, 'brain'],
             'Test2' : [PI1, 'BrAiNsTeM'],
             'Test3' : [PI1, 'pcm_low'],
             'Test4' : [PI2, 'pcm_low'],
             'Test5' : [PI2, 1],
            }

    for test, args in tests.items():
        try:
            t0 = time()
            OAR = OAR_Image(*args)
            t1 = time()
            print(f'{test} succeded in {t1-t0:.3f} sec')
            print(OAR.Path)
            print(OAR)
        except:
            print(f'{test} failed')
            for arg in args:
                print(f'Argument: "{arg}" : {type(arg)}', end = '\n')
        finally:
            print()

    OAR1 = OAR_Image()
    print(OAR1)