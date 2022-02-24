"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: DataReader.py


description: Finds the paths to files related to a specific patient ID for specified segmentation methods

input:  ID: ID of patient 
        types: A list that's a subset of L where L=["GT","DL","DLB","ATLAS"]. By default types = "All", meaning all of L is the input.
               types should not consist of duplicates or strings not in L.

Output: A list consisting of the paths to images for the specified segmentation methods images for the specified patient ID. 
"""

# Imports
import os
import SimpleITK as ITK

def datareader(ID, types = "All"):

    All_types = ["GT","DL","DLB"] # add atlas
    All = True if types == "All" else False 
        
    if len(types) != len(set(types)) and not All:
        raise ValueError("types not of valid form, look at documentation")
    elif not all(type in All_types for type in types) and not All:
        raise ValueError("types has illegal entries, look at documentation")

    output = []
    root = "A:\\"
    paths = {"GT":"Task5041_OARBoundsMergedDSCTOnly\\cts\\labels",
              "DL":"Task5041_OARBoundsMergedDSCTOnly\\fold_0",
              "DLB":"Task5031_OARBoundsMergedDS\\fold_0"
              #add atlas
            }
    if types == "All":
        types = All_types

    for type in types:
        for f in os.listdir(root + paths.get(type)):
            if ID in f:
                file = root + paths.get(type) + "\\" + f
                output.append(file)
                break
        if len(output) == 0:
            raise ValueError("ID doesnt seem to match any patients")

    return output


ID = "4Prj3A5sMvSv1sK4u5ihkzlnU"

L = datareader(ID)

for img in L:
    print(img)
    ITK.ReadImage(img)






