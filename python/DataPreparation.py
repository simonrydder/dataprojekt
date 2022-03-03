"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        27/02/2022

File name:      DataPreparation.py

Discribtion:    Implements the class OAR. The class takes the inputs: file (complete path of seleced patient) 
                and OAR_name (name of the OAR in focus). The class creates an images of only the wanted OAR 
                with the same origin, direction, spacing and shape. The class also includes functions: GetArray
                (to get the images as an array) and SaveArrayAsImage (to save a given array with the same pro-
                perties as the original image).
"""

# Imports
import SimpleITK as ITK
import numpy as np
 
# Import of other files


# Classes and functions
class OAR_Image():
    def __init__(self, file, OAR_name):
        self.File = file
        self.Name = OAR_name.lower()
        self.PatientID = self.File.split('\\')[-1].split('&')[0]
        self.Date = self.File.split('\\')[-1].split('&')[1].split('.')[0]
        self.OARs = {"background" : 0, "brain" : 1, "brainstem" : 2, "spinalcord" : 3,
                     "lips" : 4, "esophagus" : 5, "parotid_merged" : 6, "pcm_low" : 7,
                     "pcm_mid" : 8, "pcm_up" : 9, "mandible" : 10, "submandibular_merged" : 11,
                     "thyroid" : 12, "opticNerve_merged" : 13, "eyefront_merged" : 14, "eyeback_merged" :15}
        self.SegmentNo = self.GetSegment()
        self.Origin = None
        self.Direction = None
        self.Spacing = None
        self.Shape = None
        self.Image = self.GetImage()

    def __str__(self):
        OARprint = f'Name: {self.Name}\nSegment#: {self.SegmentNo}\nImage (x, y, z): {self.Shape}'
        return OARprint

    def GetSegment(self):
        return self.OARs.get(self.Name)
    
    def GetImage(self):
        # Read image and important properties.
        img = ITK.ReadImage(self.File)
        self.Origin = img.GetOrigin()
        self.Direction = img.GetDirection()
        self.Spacing = img.GetSpacing()
        self.Shape = img.GetSize()

        # Transform Image to Array
        array = ITK.GetArrayFromImage(img)

        # Replace all values unequal to SegmentNo with 0.
        array = np.where(array == self.SegmentNo, array, 0)

        # Retransform Array to Image
        img = ITK.GetImageFromArray(array)
        img.SetDirection(self.Direction)
        img.SetOrigin(self.Origin)
        img.SetSpacing(self.Spacing)

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

# Run file (optional)


# Test
import time

file = "A:\\Task5041_OARBoundsMergedDSCTOnly\\fold_0\\1cbDrFdyzAXjFICMJ58Hmja9U&20130521.nii.gz"
segment = 'BraiNSteM'

t0 = time.time()
OAR1 = OAR_Image(file, segment)
t1 = time.time()
print(t1-t0)
print(OAR1)

print(OAR1.PatientID)
print(OAR1.Date)

array = OAR1.GetArray()
OAR1.SaveArrayAsImage(array, 'A:\\myFinalArrayTest.nii.gz')

OAR1.SaveImage('A:\\myFinalTest.nii.gz')