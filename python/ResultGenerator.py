"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        18/05/2022

File name:      ResultGenerator.py

Description:    Generates the following 5 .csv files:
                - total_merged.csv
                - total_merged_sliced.csv
                - preformance_median.csv
                - scatter_data.csv
                - total_merged_no_outliers.csv
                and places them in the folder 'results'
"""

# Initialization
print(f"Running {__name__}")


# Settings
output_folder = 'results'
outfile1 = 'total_merged.csv'
outfile2 = 'total_merged_sliced.csv'
outfile3 = 'preformance_median.csv'
outfile4 = 'scatter_data.csv'
outfile5 = 'total_merged_no_outliers.csv'


# Imports
import os
import re
import pandas as pd
import SimpleITK as ITK
from progressbar import ProgressBar


# Imports from other files
from Metrics import Metrics_Info
from DataReader import Path
from DataPreparation import OAR_Image
from EditedPathLength import EPL_Metric

def PatientKeys(n = None):
    dir = "../data/data/GT"
    files = os.listdir(dir)
    if isinstance(n, int):
        files = files[:n]
    keys = {(ID, Date[:8]) for ID, Date in [file.split('&') for file in files]}

    return keys

# Functions
def generate_total_merged(
    Patients : set,
    Segments : list, 
    Comparisons : set,
    Tolerances : set,
    overwrite = False, # True only if implementation of metrics have been changed
    root = '../data/dataframes/complete/',
    location = '../data/results/'
):

    def generate_result(Tolerance : int):

        assert isinstance(Tolerance, int), f'Incorrect Tolerance given to generate_result()'

        nonlocal Patients, Segments, Comparisons, overwrite, root

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
                
                missing_Patients = Patients - cur_Patients
                if len(missing_Patients) != 0:
                    print(f'Calculating missing data for {file}')
                pbar = ProgressBar()
                for ID, Date in pbar(missing_Patients):
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

    
    def merge_results( 
        filename = 'total_merged.csv',
    ):

        nonlocal Tolerances, root, location

        tolerance_dfs = []
        for Tolerance in Tolerances:
            folder = f'Tolerance{Tolerance}/'
            files = os.listdir(root + folder)

            dfs = []
            for file in files:
                comparison, segment, _ = file.split('.')[0].split('&')
        
                df = pd.read_csv(root + folder + file)
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

            merged['Tolerance'] = Tolerance
            tolerance_dfs.append(merged)

        total = pd.concat([*tolerance_dfs])
        if not os.path.exists(location):
            os.makedirs(location)
            print(f'{location} created\n')

        total.to_csv(location + filename)
        print(f'Merged completed: {filename} saved in {location}\n')

    # Checks for correct slicing
    assert isinstance(Segments, list), 'Incorrect slicing - not a list'
    assert isinstance(Comparisons, set), 'Incorrect slicing - not a set'
    assert isinstance(Patients, set), 'Incorrect slicing - not a set'

    for Tolerance in Tolerances:
        generate_result(Tolerance)
    
    merge_results()

    # end of generate_total_merged


def generate_slice(
    Segments : list,
    Patients : set, 
    Comparisons : set,
    Tolerances : set,
    overwrite = False, # True only if implementation of metrics have been changed
    root = '../data/dataframes/slice/',
    location = '../data/results/'
):
    
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


    def generate_result(Tolerance : int):

        assert isinstance(Tolerance, int), f'Incorrect Tolerance given to generate_result()'

        nonlocal Patients, Segments, Comparisons, overwrite, root

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

                missing_Patients = Patients - cur_Patients
                if len(missing_Patients) != 0:
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

                    df = pd.DataFrame({
                        'Index' : list(range(Z)),
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
                        'LinesChanged' : LinesChanged
                    })

                    patient_dfs.append(df)

                if len(patient_dfs):
                    df = pd.concat([df, *patient_dfs])
                    df.to_csv(folder + file, index = False)
                    print(f'{file} saved to {folder}\n')


    def merge_results(Tolerance, filename = 'total_merged_slice'):
        
        nonlocal root, location

        folder = root + f'Tolerance{Tolerance}/'
        files = os.listdir(folder)

        dfs = []
        for file in files:
            comparison, segment, _ = file.split('.')[0].split('&')
    
            df = pd.read_csv(folder + file)
            df['Comparison'] = comparison
            df['Segment'] = segment
            cols = df.columns.to_list()
            df = df[cols[:3] + cols[-2:] + cols[3:-2]]

            dfs.append(df)

            
        merged = pd.concat([*dfs], ignore_index = True)
        merged['Tolerance'] = Tolerance
        
        merged = merged.drop(merged[merged['DICE'] > 10].index)
        
        for col in ["PointsModel", "PointsGT", "LinesModel", "LinesChanged"]:
            merged[col] = merged[col].replace(['set()'], ['[]'])
        
        filename = f'{filename}_{Tolerance}.csv'
        merged.to_csv(location + filename, index = False)
        print(f'Merged completed: {filename} saved in {location}\n')
       

    for Tolerance in Tolerances:
        generate_result(Tolerance)
        merge_results(Tolerance)



def generate_scatter(
    location = '../data/results/', # Output folder
    filename = 'scatter_data.csv', # Output file name
    file = 'total_merged.csv'   # Input file   
):
    df = pd.read_csv(location + file)
    df = df.drop('Date', axis = 1)
    
    segments = df.columns[3:-1]

    df = pd.melt(
        frame = df,
        id_vars = ['ID', 'Metric', 'Comparison', 'Tolerance'],
        value_vars = segments,
        var_name = 'Segment'
    )

    df['Segment'] = df['Segment'] + '_' + df['Tolerance'].astype(str)
    df = df.drop('Tolerance', axis = 1)

    df = pd.pivot(
        data = df,
        index = ['ID', 'Metric', 'Segment'],
        columns = 'Comparison',
        values = 'value'
    )

    for m1, m2 in [('DL', 'DLB'), ('DL', 'ATLAS'), ('ATLAS', 'DLB')]:
        df['Color_Dice_'+ m1 + m2] = [
            'darkcyan' if x > y else 
            'red' if x < y else 'black' 
            for x, y in zip(df['GTvs'+ m1], df['GTvs' + m2])
        ]
        
        df['Color_' + m1 + m2] = [
            'red' if x > y else
            'darkcyan' if x < y else 'black'
            for x, y in zip(df['GTvs'+ m1], df['GTvs' + m2])
        ]

        df['Color_Dice_'+ m2 + m1] = [
            'darkcyan' if x > y else 
            'red' if x < y else 'black' 
            for x, y in zip(df['GTvs'+ m2], df['GTvs' + m1])
        ]
        
        df['Color_' + m2 + m1] = [
            'red' if x > y else
            'darkcyan' if x < y else 'black'
            for x, y in zip(df['GTvs'+ m2], df['GTvs' + m1])
        ]

    for method in ['DL', 'DLB', 'ATLAS']:
        df['Color_Dice_' + method + method] = [
            'darkcyan' if x > y else 
            'red' if x < y else 'black' 
            for x, y in zip(df['GTvs'+ method], df['GTvs' + method])
        ]
        
        df['Color_' + method + method] = [
            'red' if x > y else
            'darkcyan' if x < y else 'black'
            for x, y in zip(df['GTvs'+ method], df['GTvs' + method])
        ]
    
    df.to_csv(location + filename)
    df = pd.read_csv(location + filename)

    df['Segment'] = df['Segment'].apply(lambda x : re.sub(r'_[0]', '', x))

    segments = df['Segment'].unique().tolist()

    dfs = []
    for color in ['darkcyan', 'red', 'black']:
        for segment in segments:
            new = {
                'ID': "Dummy", 
                'Metric': "DICE", 
                'Segment': segment, 
                'GTvsATLAS': None, 
                'GTvsDL': None, 
                'GTvsDLB': None,
                'Color_Dice_DLDLB': color, 
                'Color_DLDLB': color, 
                'Color_Dice_DLBDL': color, 
                'Color_DLBDL':color,
                'Color_Dice_DLATLAS':color, 
                'Color_DLATLAS':color, 
                'Color_Dice_ATLASDL': color,
                'Color_ATLASDL': color, 
                'Color_Dice_ATLASDLB': color, 
                'Color_ATLASDLB': color,
                'Color_Dice_DLBATLAS': color, 
                'Color_DLBATLAS': color,
                'Color_DLDL': color,
                'Color_DLBDLB': color,
                'Color_ATLASATLAS': color
            }
            dfs.append(pd.DataFrame(new, index = [0]))

    df = pd.concat([df, *dfs], ignore_index = True)
    df.to_csv(location + filename, index = False)
    print(f'Scatter data completed: {filename} saved in {location}\n')



def generate_performance(
    location = '../data/results/', # Output folder
    filename = 'performance_median.csv', # Output file name
    file = 'total_merged.csv'   # Input file
):
    df = pd.read_csv(location + file)
    df = df.drop('Date', axis = 1)
    
    segments = df.columns[3:-1]

    df = pd.melt(
        frame = df,
        id_vars = ['ID', 'Metric', 'Comparison', 'Tolerance'],
        value_vars = segments,
        var_name = 'Segment'
    )

    df['Segment'] = df['Segment'] + '_' + df['Tolerance'].astype(str)
    df = df.drop('Tolerance', axis = 1)

    df['Segment'] = df['Segment'].apply(lambda x : re.sub(r'_[0]', '', x))

    df = df.groupby(['Comparison', 'Metric', 'Segment']).median().reset_index()

    df.dropna(inplace = True)
    df = df.reset_index(drop = True)

    df.to_csv(location + filename, index = False)
    print(f'Performance median completed: {filename} saved in {location}\n')



def main():
    Segments = list(OAR_Image.OARs.keys())[2:]
    Comparisons = {('GT', 'DL'), ('GT', 'DLB'), ('GT', 'ATLAS')}

    generate_total_merged(
        Patients = PatientKeys(),
        Segments = Segments,
        Comparisons = Comparisons,
        Tolerances = {0, 1, 2}
    )

    generate_slice(
        Patients = {
            ('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129'),
            ('HNCDL_447', '20170421'),
            ('HNCDL_340', '20180723'),
            ('HNCDL_141', '20160926'),
            ('PHbmDBLzKFUqHWIbGMTmUFSmO', '20200212')
        },
        Segments = Segments,
        Comparisons = Comparisons,
        Tolerances = {0, 1, 2}
    )

    generate_scatter()

    generate_performance()


# Script
if __name__ == '__main__':
    main()