"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        25/03/2022

File name:      ResultManager.py

Description:
"""

# Initialization
print(f"Running {__name__}")


# Imports
import os
import pandas as pd


# Imports from other files
from Metrics2 import Metrics_Info
from DataReader2 import Path
from DataPreparation2 import OAR_Image


# Classes and functions
def GenerateResults(
    Segments,           # Iterable object of segment names
    Comparisons,        # Iterable object of tuples with comparison methods
    Patients,           # Iterable object of tuples with ID and Date
    overwrite = False,  # True : Will calculate new values for files loaded.
    root = '..\\data\\results\\dataframes'):

    for Segment in Segments:

        for MethodA, MethodB in Comparisons:
            file = f'{MethodA}vs{MethodB}&{Segment}.csv'

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

                MI = Metrics_Info(ImgA, ImgB)

                metrics = MI.getAttributes()
                patient_dfs.append(pd.DataFrame(metrics))

            if len(patient_dfs):
                df = pd.concat([df, *patient_dfs])
                df.to_csv(root + file, index = False)
                print(f'{file} saved')

def MergeResults(file = 'total.csv',
    location = '..\\data\\results\\', folder = 'dataframes\\'):
    files = os.listdir(location + folder)

    dfs = []
    for file in files:
        comparison, segment = file.split('.')[0].split('&')
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

    merged.to_csv(location + 'merged.csv')

# Test
if __name__ == "__main__":
    MergeResults()