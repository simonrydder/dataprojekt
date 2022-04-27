"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        25/03/2022

File name:      ResultManager.py

Description:    Contains 5 functions: 
                - GenerateResults(Segments, Comparisons, Patients, Tolerance = 0, Overwrite = False, root = '')
                - MergeResults()
"""

# Initialization
print(f"Running {__name__}")


# Imports
import os
from functools import reduce
import pandas as pd
import SimpleITK as ITK


# Imports from other files
from Metrics2 import Metrics_Info
from DataReader2 import Path
from DataPreparation2 import OAR_Image
from EditedPathLength2 import EPL_Metric


# Classes and functions
def GenerateResults(
    Segments,           # Iterable object of segment names
    Comparisons,        # Iterable object of tuples with comparison methods
    Patients,           # Iterable object of tuples with ID and Date
    Tolerance = 0,      
    overwrite = False,  # True : Will calculate new values for files loaded.
    root = '..\\data\\results\\dataframes\\'):

    for Segment in Segments:

        for MethodA, MethodB in Comparisons:
            file = f'{MethodA}vs{MethodB}&{Segment}&Tolerance{Tolerance}.csv'

            try:
                if overwrite:
                    print(f'{file} will be overwritten')
                    raise FileNotFoundError

                df = pd.read_csv(root + file)
                print(f'{file} loaded')

            except FileNotFoundError:
                MI0 = Metrics_Info()
                df = pd.DataFrame(columns = MI0.getAttributes().keys())

            IterTuple = df[['ID', 'Date']].itertuples(index = False)
            cur_Patients = {(ID, str(Date)) for ID, Date in IterTuple}
            patient_dfs = []
            # print(len(cur_Patients), file)

            for ID, Date in Patients - cur_Patients:
                PA = Path(ID, Date, MethodA)
                PB = Path(ID, Date, MethodB)

                ImgA = OAR_Image(PA, Segment)
                ImgB = OAR_Image(PB, Segment)

                MI = Metrics_Info(ImgA, ImgB, Tolerance)

                metrics = MI.getAttributes()
                patient_dfs.append(pd.DataFrame(metrics))

            if len(patient_dfs):
                df = pd.concat([df, *patient_dfs])
                df.to_csv(root + file, index = False)
                print(f'{file} saved')


def MergeResults(filename,
    location = '..\\data\\results\\', folder = 'dataframes\\'):
    
    files = os.listdir(location + folder)

    dfs = []
    for file in files:
        comparison, segment, tol = file.split('.')[0].split('&')
        if tol[-1] == filename.split('.')[0][-1]:
            df = pd.read_csv(location + folder + file)
            df['Comparison'] = [comparison] * len(df)
            df['Segment'] = [segment] * len(df)
            dfs.append(df)

    merged = pd.concat([*dfs])
    idx = list(merged.columns[:2]) + [merged.columns[-2]]
    metrics = merged.columns[2:-2]
    val = merged.columns[-1]

    merged = pd.melt(merged,
        id_vars = idx + [val],
        value_vars = metrics,
        var_name = 'Metric'
    )
 
    merged = pd.pivot(merged,
        index = idx + ['Metric'],
        columns = val,
        values = 'value'
    )

    merged.to_csv(location + filename)
    print(f'Merged completed: {filename} saved in {location}\n')


def GetMetricSlice(IMGA : OAR_Image, IMGB : OAR_Image, Tolerance):
    _, _, Z = IMGA.Shape

    A = IMGA.GetArray()
    B = IMGB.GetArray()

    D, H, M = [], [], []

    for z in range(Z):
        sliceA = A[z]
        SliceAImg = ITK.GetImageFromArray(sliceA)

        sliceB = B[z]
        SliceBImg = ITK.GetImageFromArray(sliceB)

        dicecomputer = ITK.LabelOverlapMeasuresImageFilter()
        try:
            dicecomputer.Execute(SliceAImg > 0.5, SliceBImg > 0.5)
            DICE = dicecomputer.GetDiceCoefficient()
        except:
            DICE = None
        finally:
            D.append(DICE)

        hauscomputer = ITK.HausdorffDistanceImageFilter()
        try:
            hauscomputer.Execute(SliceAImg > 0.5, SliceBImg > 0.5)
            HAUS = hauscomputer.GetHausdorffDistance()
            MEAN = hauscomputer.GetAverageHausdorffDistance()
        except:
            HAUS = None
            MEAN = None
        finally:
            H.append(HAUS)
            M.append(MEAN)
    
    return D, H, M


def GenerateSliceResults(
    Segments,           # Iterable object of segment names
    Comparisons,        # Iterable object of tuples with comparison methods
    Patients,           # Iterable object of tuples with ID and Date
    Tolerance = 0,      
    overwrite = False,  # True : Will calculate new values for files loaded.
    root = '..\\data\\sliceresults\\dataframes\\'):

    for Segment in Segments:

        for MethodA, MethodB in Comparisons:
            file = f'{MethodA}vs{MethodB}&{Segment}&Tolerance{Tolerance}.csv'

            MI = Metrics_Info()
            colNames = ['Index'] + list(MI.getAttributes().keys())

            try:
                if overwrite:
                    print(f'{file} will be overwritten')
                    raise FileNotFoundError

                df = pd.read_csv(root + file)
                print(f'{file} loaded')

            except FileNotFoundError:
                df = pd.DataFrame(columns = colNames)

            IterTuple = df[['ID', 'Date']].itertuples(index = False)
            cur_Patients = {(ID, str(Date)) for ID, Date in IterTuple}
            patient_dfs = []

            for ID, Date in Patients - cur_Patients:
                PA = Path(ID, Date, MethodA)
                PB = Path(ID, Date, MethodB)

                ImgA = OAR_Image(PA, Segment)
                ImgB = OAR_Image(PB, Segment)
                Z = ImgA.Shape[2]

                EPL_Info = EPL_Metric(ImgA, ImgB, Tolerance)
                DICE, Haus, MSD = GetMetricSlice(ImgA, ImgB, Tolerance)

                EPL = EPL_Info.SliceEPL
                LineRatio = EPL_Info.SliceLR
                VolumeRatio = EPL_Info.SliceVR
                pModel = EPL_Info.SlicePointsModel
                pGT = EPL_Info.SlicePointsGT
                LinesModel = EPL_Info.SliceLinesModel
                LinesChanged = EPL_Info.SliceLinesChanged

                df = pd.DataFrame({'Index' : list(range(Z)),
                                   'ID' : [ID]*Z,
                              'Date' : [Date]*Z,
                              'DICE' : DICE,
                              'Haus' : Haus,
                              'MSD' : MSD,
                              'EPL' : EPL,
                              'LineRatio' : LineRatio,
                              'VolumeRatio' : VolumeRatio,
                              'PointsModel' : pModel,
                              'PointsGT' : pGT,
                              'LinesModel' : LinesModel,
                              'LinesChanged' : LinesChanged})

                patient_dfs.append(df)

            if len(patient_dfs):
                df = pd.concat([df, *patient_dfs])
                df.to_csv(root + file, index = False)
                print(f'{file} saved')


# def MergeSliceResults(filename,
#     location = '..\\data\\sliceresults\\', folder = 'dataframes\\'):
    
#     files = os.listdir(location + folder)

#     dfs = []
#     Tolerances = {int(file.split('.')[0].split('&')[-1][-1]) for file in files}

#     for Tolerance in Tolerances:

#         tempdfs = []
#         for file in files:
#             comparison, segment, tol = file.split('.')[0].split('&')

#             if int(tol[-1]) == Tolerance:
#                 df = pd.read_csv(location + folder + file)
#                 df = df.reset_index(drop = True)
#                 N = len(df)
#                 df['Comparison'] = [comparison] * N
#                 df['Segment'] = [segment] * N
#                 tempdfs.append(df)

#         tempdf = pd.concat([*tempdfs])
#         cols = tempdf.columns
#         newnames = [f'{col}_{Tolerance}' for col in cols[3:13]]
        
#         tempdf.columns = list(cols[:3]) + newnames + list(cols[-2:])
#         dfs.append(tempdf)

#     df_final = reduce(lambda left,right: pd.merge(left, right, 'left', on = list(cols[:3]) + list(cols[-2:])), dfs)
#     df_final.drop_duplicates()

#     df_final.to_csv(location + filename, index = False)

def MergeSliceResults(filename,
    location = '..\\data\\sliceresults\\', folder = 'dataframes\\'):
    
    files = os.listdir(location + folder)

    dfs = []
    for file in files:
        comparison, segment, tol = file.split('.')[0].split('&')

        df = pd.read_csv(location + folder + file)
        df = df.reset_index(drop = True)
        N = len(df)
        df['Comparison'] = [comparison] * N
        df['Segment'] = [segment] * N
        df['Tolerance'] = [int(tol[-1])] * N
        
        cols = list(df.columns)
        df = df[cols[:3] + cols[-3:] + cols[3:-3]]

        dfs.append(df)

    df_final = pd.concat([*dfs])

    df_final.to_csv(location + filename, index = False)
    print(f'Merged completed: {filename} saved in {location}\n')


def PatientKeys(n = "All"):
    dir = "A:\\data\\GT"
    files = os.listdir(dir)
    if isinstance(n, int):
        files = files[:n]
    keys = {(ID, Date[:8]) for ID, Date in [file.split('&') for file in files]}

    return keys


# Test
if __name__ == "__main__":
    Segments = list(OAR_Image.OARs.keys())[2:]
    Comparisons = {('GT', 'DL'), ('GT', 'DLB')}
    Patients = PatientKeys()
    for Tolerance in {0, 1, 2, 3}:
        print(f'{Tolerance = }')
        GenerateResults(Segments, Comparisons, Patients, Tolerance)
        MergeResults(f'total_tolerance{Tolerance}.csv')

    Segments = list(OAR_Image.OARs.keys())[2:11]
    Comparisons = {('GT', 'DL'), ('GT', 'DLB')}
    Patients = PatientKeys(3)
    Patients = {('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129'),
                ('HNCDL_447', '20170421'),
                ('HNCDL_340', '20180723'),
                ('HNCDL_141', '20160926'),
                ('PHbmDBLzKFUqHWIbGMTmUFSmO', '20200212')}
    for Tolerance in {0, 1, 2, 3}:
        print(f'\n{Tolerance = }')
        GenerateSliceResults(Segments, Comparisons, Patients, Tolerance)
    
    MergeSliceResults('total.csv')