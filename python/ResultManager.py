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
import pandas as pd
import SimpleITK as ITK
from progressbar import ProgressBar


# Imports from other files
from Metrics import Metrics_Info
from DataReader import Path
from DataPreparation import OAR_Image
from EditedPathLength import EPL_Metric


# Classes and functions
def GenerateResults(
    Segments,           # Iterable object of segment names
    Comparisons,        # Iterable object of tuples with comparison methods
    Patients,           # Iterable object of tuples with ID and Date
    Tolerance = 0,      
    overwrite = False,  # True : Will create new files.
    root = '../data/results/dataframes/'):

    # Checks for correct slicing
    assert isinstance(Segments, list), 'Incorrect slicing - not a list'
    assert isinstance(Comparisons, set), 'Incorrect slicing - not a set'
    assert isinstance(Patients, set), 'Incorrect slicing - not a set'

    # Output folder
    folder = root + f'Tolerance{Tolerance}/'

    # Checks if output folder exists otherwise create
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f'{folder} created')

    # If folder exists and overwrite is true delete all files in folder
    elif overwrite:
        files = os.listdir(folder)
        for file in files:
            os.remove(folder + file)
        
        print(f'{len(files)} files in {folder} has been deleted')    

    # Creating data
    for Segment in Segments:

        for MethodA, MethodB in Comparisons:
            file = f'{MethodA}vs{MethodB}&{Segment}&Tolerance{Tolerance}.csv'

            try:
                df = pd.read_csv(folder + file)
                print(f'{file} loaded')

            except FileNotFoundError:
                MI0 = Metrics_Info()
                df = pd.DataFrame(columns = MI0.getAttributes().keys())

            IterTuple = df[['ID', 'Date']].itertuples(index = False)
            cur_Patients = {(ID, str(Date)) for ID, Date in IterTuple}
            patient_dfs = []
            
            print(f'Calculating missing data for {file}')
            pbar = ProgressBar()
            for ID, Date in pbar(Patients - cur_Patients):
                PA = Path(ID, Date, MethodA)
                PB = Path(ID, Date, MethodB)

                ImgA = OAR_Image(PA, Segment)
                ImgB = OAR_Image(PB, Segment)

                MI = Metrics_Info(ImgA, ImgB, Tolerance)

                metrics = MI.getAttributes()
                patient_dfs.append(pd.DataFrame(metrics))

            if len(patient_dfs):
                df = pd.concat([df, *patient_dfs])
                df.to_csv(folder + file, index = False)
                print(f'{file} saved to {folder}\n')


def MergeResults(Tolerance,
    location = '../data/results/', folder = 'dataframes/'):
    
    folder = folder + f'Tolerance{Tolerance}/'
    files = os.listdir(location + folder)

    dfs = []
    for file in files:
        comparison, segment, _ = file.split('.')[0].split('&')
        
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

    filename = f'total_tolerance{Tolerance}.csv'
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
    root = '../data/sliceresults/dataframes/'):

    # Checks for correct slicing
    assert isinstance(Segments, list), 'Incorrect slicing - not a list'
    assert isinstance(Comparisons, set), 'Incorrect slicing - not a set'
    assert isinstance(Patients, set), 'Incorrect slicing - not a set'

    # Output folder
    folder = root + f'Tolerance{Tolerance}/'

    # Checks if output folder exists otherwise create
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f'{folder} created')

    # If folder exists and overwrite is true delete all files in folder
    elif overwrite:
        files = os.listdir(folder)
        for file in files:
            os.remove(folder + file)
        
        print(f'{len(files)} files in {folder} has been deleted')    

    # Creating data
    for Segment in Segments:

        for MethodA, MethodB in Comparisons:
            file = f'{MethodA}vs{MethodB}&{Segment}&Tolerance{Tolerance}.csv'

            MI = Metrics_Info()
            colNames = ['Index'] + list(MI.getAttributes().keys())

            try:
                df = pd.read_csv(folder + file)
                print(f'{file} loaded')

            except FileNotFoundError:
                df = pd.DataFrame(columns = colNames)

            IterTuple = df[['ID', 'Date']].itertuples(index = False)
            cur_Patients = {(ID, str(Date)) for ID, Date in IterTuple}
            patient_dfs = []

            print(f'Calculating missing data for {file}')
            pbar = ProgressBar()
            for ID, Date in pbar(Patients - cur_Patients):
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
                df.to_csv(folder + file, index = False)
                print(f'{file} saved to {folder}\n')


def MergeSliceResults(Tolerance,
    location = '../data/sliceresults/', folder = 'dataframes/'):
    
    folder = folder + f'Tolerance{Tolerance}/'
    files = os.listdir(location + folder)

    dfs = []
    for file in files:
        comparison, segment, _ = file.split('.')[0].split('&')
        
        df = pd.read_csv(location + folder + file)
        df['Comparison'] = [comparison] * len(df)
        df['Segment'] = [segment] * len(df)
        cols = df.columns.to_list()
        df = df[cols[:3] + cols[-2:] + cols[3:-2]]
        dfs.append(df)

    merged = pd.concat([*dfs])
    
    filename = f'total_tolerance{Tolerance}.csv'
    merged.to_csv(location + filename)
    print(f'Merged completed: {filename} saved in {location}\n')


def TotalMerge(location = '../data/sliceresults/', names = 'total_tolerance'):

    files = os.listdir(location)

    dfs = []
    for file in files:
        if file.split('.')[-1] != 'csv':
            continue

        if file.split('.')[0][:-1] != names:
            continue

        tol = int(file.split('.')[0][-1])
        df = pd.read_csv(location + file)
        df['Tolerance'] = tol
        dfs.append(df)
    
    merged = pd.concat([*dfs])
    merged = merged.drop(merged[merged['DICE'] > 10].index)

    for col in ["PointsModel","PointsGT","LinesModel","LinesChanged"]:
        merged[col] = merged[col].replace(['set()'],['[]'])

    filename = f'total_merged.csv'
    merged.to_csv(location + filename)


def PatientKeys(n = None):
    dir = "../data/data/GT"
    files = os.listdir(dir)
    if isinstance(n, int):
        files = files[:n]
    keys = {(ID, Date[:8]) for ID, Date in [file.split('&') for file in files]}

    return keys


# Generating of results
if __name__ == "__main__":
    # Inputs
    overwrite = False
    Segments = list(OAR_Image.OARs.keys())[2:]
    Comparisons = {('GT', 'DL'), ('GT', 'DLB'), ('GT', 'ATLAS')}
    Patients = PatientKeys()
    Tolerances = {0, 1, 2}

    # Script
    if overwrite:
        msg = (
            f'Overwriting current files for Tolerance = {Tolerances}: '
            '[Press ENTER]\n'
        )
        ans = input(msg)
            
    for Tolerance in Tolerances:
        print(f'{Tolerance = }')
        GenerateResults(Segments, Comparisons, Patients, Tolerance, overwrite)
        MergeResults(Tolerance)


# Generating of sliceresults
if __name__ == "__main__":
    # Inputs
    overwrite = False
    Segments = list(OAR_Image.OARs.keys())[2:]
    Comparisons = {('GT', 'DL'), ('GT', 'DLB'), ('GT', 'ATLAS')}
    # Patients = PatientKeys(3)
    Patients = {('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129'),
                ('HNCDL_447', '20170421'),
                ('HNCDL_340', '20180723'),
                ('HNCDL_141', '20160926'),
                ('PHbmDBLzKFUqHWIbGMTmUFSmO', '20200212')}
    Tolerances = {0, 1, 2}

    # Script
    if overwrite:
        msg = (
            f'Overwriting current files for Tolerance = {Tolerances}: '
            '[Press ENTER]\n'
        )
        ans = input(msg)

    for Tolerance in Tolerances:
        print(f'\n{Tolerance = }')
        GenerateSliceResults(Segments, Comparisons, Patients, Tolerance, overwrite)
        MergeSliceResults(Tolerance, location = '../data/sliceresults/')
    
    TotalMerge()
