'''
Data visualization

'''

# Imports
import os
import SimpleITK as ITK
from DataReader import Path
from DataPreparation import OAR_Image
from eskildmetric import Metrics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


Patients = ["1cbDrFdyzAXjFICMJ58Hmja9U", "cha4gqrSUuXC70qTTZOsnoWmp", "Gn0PuEdJvjaCFRvy4af0pbKvd"]


Segments = ["mandible", "brainstem", "spinalcord"]
Methods = ["GT", "DL", "DLB"]

def SimilarityPlot(Segments, Methods, Patients):
    
    data = []
    DICE_data = []
    Haus_data = []
    MSD_data = []

    for Patient in Patients:
        for segment in Segments:
            MET = Metrics(Patient, segment, Methods)
            DICE_data.append(list(MET.getDICE().values()))
            Haus_data.append(MET.getHausdorff())
            MSD_data.append(MET.getMSD())
    
    if len(DICE_data[Segments[0]].keys()) == 3:
        colors = ["b", "r", "g"]
    else:
        colors = ["b", "r", "g", "y", "p", "o"] #We have atlas too. 

    # DICE_data[::len(Segments)] får hver organ
    # [x[0] for x in DICE:data[::len(Segments)] giver alle GT vs DL fx. 

    #Plot DICE:
    def DICE_plot(DICE_data):



        for i in range(len(Segments)):
            organs = DICE_data[i::len(Segments)]
            methods = [x[i] for x in DICE_data[i::len(Segments)]]

            for xe, ye in zip([i], methods):
                print(xe,ye)
                plt.scatter(xe, ye)
                plt.ylabel("Dice Coefficient")
                plt.title("DICE MOTHERFUCKER")
                plt.ylim(0, 1)
        ax = plt.gca()
        loc = plticker.MultipleLocator(base=1)
        ax.xaxis.set_major_locator(loc)
        ax.set_aspect(1)
        #plt.xticks([i for i in range(len(Segments))], Methods, rotation='horizontal')
        plt.show()
        
    
          

            for j, el in enumerate([item for sublist in DICE_data[i::3] for item in sublist]):
                plt.scatter(, el, c = colors[j], s=12)
                plt.legend(Methods)
                plt.ylabel("Dice Coefficient")
                plt.title("DICE MOTHERFUCKER")
                plt.ylim(0, 1)
                #plt.xlim(0, 10)
        
        ax = plt.gca()
        loc = plticker.MultipleLocator(base=1)
        ax.xaxis.set_major_locator(loc)
        ax.set_aspect(1)
        plt.xticks([i for i in range(len(Segments))], Methods, rotation='horizontal')
        plt.show()
    
    #Plot Haus
    def Haus_plot()

        for j, el in enumerate(data[k]):
            for i, (method, val) in enumerate(data[j].items()):
                plt.scatter(k, val, c = colors[j])
                plt.legend(el)
                plt.ylabel("Dice Coefficient")
                plt.ylim(0, 1)
    
    ax = plt.gca()
    loc = plticker.MultipleLocator(base=1)
    ax.xaxis.set_major_locator(loc)
    ax.set_aspect(1)
    plt.xticks([i for i in range(len(Segments))], Segments, rotation='horizontal')

    plt.show()

SimilarityPlot(Segments, Methods, Patients)
