'''
Find descriptive statistics of the metrics like mean and so on. 
CURRENTLY ONLY WORKS WHEN INPUTTING TWO TYPES OF METHODS. 
'''
import Main
from eskildmetric import Metrics
import DataReader
import DataPreparation
import numpy as np


def statistics(methods, segment, metrics):

    #Statistics we are interested in:
    mean = {}
    var = {}
    median = {}

    for metric in metrics:
        if metric == "DICE":
            DICE_Values = []
            for Patient in Main.PatientGenerator(73):       #73 is the size of test-set
                MET = Metrics(Patient, Segment, Methods)
                DICE_Values.append(list(MET.getDICE().values()))
            mean[metric] = np.mean(np.array(DICE_Values))
            var[metric] = np.var(np.array(DICE_Values))
            median[metric] = np.median(np.array(DICE_Values))

        if metric == "Hausdorff":
            Hausdorff_Values = []
            for Patient in Main.PatientGenerator(73):
                MET = Metrics(Patient, Segment, Methods)
                Hausdorff_Values.append(list(MET.getHausdorff().values()))
            mean[metric] = np.mean(np.array(Hausdorff_Values))
            var[metric] = np.var(np.array(Hausdorff_Values))
            median[metric] = np.median(np.array(Hausdorff_Values))
        
        if metric == "MSD":
            MSD_values = []
            for Patient in Main.PatientGenerator(73):
                MET = Metrics(Patient, Segment, Methods)
                MSD_values.append(list(MET.getMSD().values()))
            mean[metric] = np.mean(np.array(MSD_values))
            var[metric] = np.var(np.array(MSD_values))
            median[metric] = np.median(np.array(MSD_values))

        # if metric == "APL":
        #     APL_Values = []
        #     for Patient in Main.PatientGenerator(73):
        #         MET = Metrics(Patient, Segment, Methods)
        #         Hausdorff_Values.append(list(MET.getHausdorff().values()))
        #     mean[metric] = np.mean(np.array(Hausdorff_Values))
        #     var[metric] = np.var(np.array(Hausdorff_Values))
        #     median[metric] = np.median(np.array(Hausdorff_Values))
    
    print(f'{Segment}-statistics for all test-patients is equal to:\nMean: {mean},\nVariance: {var},\nMedian: {median}')

    return mean, var, median

Segment = "BrainStem"
#Methods = ["GT", "DL", "DLB"]
Methods = ["GT", "DL"]
metrics = ["DICE", "Hausdorff", "MSD"]

values = statistics(Methods, Segment, metrics)

Segment = "BrainStem"
Methods = ["GT", "DL", "DLB"]
Methods = ["GT", "DL"]
metrics = ["DICE", "Hausdorff"]