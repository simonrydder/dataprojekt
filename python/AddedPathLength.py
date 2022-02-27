"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: AddedPathLength.py

Discription: 

Python Script
"""

# Imports
import os
import numpy as np
import nilearn.image as ni_img


# Import other files


# Classes and functions

def loadNiftiReturnNumpy(filepath):
    '''
    filepath: path to nifti file
    '''
    niftiFile = ni_img.load_img(filepath)
    niftiArr = niftiFile.get_fdata()
    
    return niftiArr

def getEdgeOfMask(mask):
    '''
    Computes and returns edge of a segmentation mask
    '''
    # edge has the pixels which are at the edge of the mask
    edge = np.zeros_like(mask)
    
    # mask_pixels has the pixels which are inside the mask of the automated segmentation result
    mask_pixels = np.where(mask > 0)

    for idx in range(0,mask_pixels[0].size):

        x = mask_pixels[0][idx]
        y = mask_pixels[1][idx]
        z = mask_pixels[2][idx]

        # Count # pixels in 3x3 neighborhood that are in the mask
        # If sum < 27, then (x, y, z) is on the edge of the mask
        if mask[x-1:x+2, y-1:y+2, z-1:z+2].sum() < 27:
            edge[x,y,z] = 1
            
    return edge

def AddedPathLength(P1, P2):
    '''
    Returns the added path length, in pixels
    
    Steps:
    1. Find pixels at the edge of the mask for both auto and gt
    2. Count # pixels on the edge of gt that are not in the edge of auto
    '''
    
    # Check if auto and gt have same dimensions. If not, then raise a ValueError
    if P1.shape != P2.shape:
        raise ValueError('Shape of Picture 1 and Picture 2 must be identical!')

    # edge_auto has the pixels which are at the edge of the automated segmentation result
    edge_P1 = util.getEdgeOfMask(P1)
    # edge_gt has the pixels which are at the edge of the ground truth segmentation
    edge_P2 = util.getEdgeOfMask(P2)
    
    # Count # pixels on the edge of gt that are on not in the edge of auto
    APL = (edge_P2 > edge_P1).astype(int).sum()
    
    return APL

# Run file (optional)



