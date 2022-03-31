
from numpy import iterable
import pandas as pd
import os
from Metrics2 import Metrics_Info
from DataReader2 import Path
from DataPreparation2 import OAR_Image

def PatientKeys(n = "All"):
    dir = "A:\\data\\GT"
    files = os.listdir(dir)
    if isinstance(n, int):
        files = files[:n]
    keys = {(ID, Date[:8]) for ID, Date in [file.split('&') for file in files]}

    return keys

# d1 = {'ID' : [1, 1, 1, 1, 1, 1, 1, 1],
#       'Metric' : ['D', 'A', 'D', 'A', 'D', 'A', 'D', 'A'],
#       'Comparison' : ['C1', 'C1', 'C1', 'C1', 'C2', 'C2', 'C2', 'C2'],
#       'Segment' : ['brain', 'brain', 'core', 'core', 'brain', 'brain', 'core', 'core'],
#       'Value' : [1, 2, 3, 4, 5, 6, 7, 8]}
# df1 = pd.DataFrame(d1)
# print(df1)

# d2 = {'ID' : [2, 2, 2, 2, 2, 2, 2, 2],
#       'Metric' : ['D', 'A', 'D', 'A', 'D', 'A', 'D', 'A'],
#       'Comparison' : ['C1', 'C1', 'C1', 'C1', 'C2', 'C2', 'C2', 'C2'],
#       'Segment' : ['brain', 'brain', 'core', 'core', 'brain', 'brain', 'core', 'core'],
#       'Value' : [11, 12, 13, 14, 15, 16, 17, 18]}
# df2 = pd.DataFrame(d2)
# print(df2)

# df = df1.pivot(index = ['ID', 'Metric', 'Comparison'], columns = 'Segment', values = 'Value')
# print(df)

# df = pd.concat([df1, df2])
# print(df)

# dfs = []
# root = "dataframes\\"
# for file in os.listdir(root):
#     # Get
#     file_info = file[:-4].split('&')
#     Metric = file_info[0]
#     Comparison = tuple(file_info[1].split(' vs '))
#     Segment = file_info[2]
#     print(f'{Metric = }\n{Comparison = }\n{Segment = }')

#     df_in = pd.read_csv(root + file)
#     N = len(df_in)
#     df_in['Metric'] = [Metric for _ in range(N)]
#     df_in['Comparison'] = [file_info[1] for _ in range(N)]
#     df_in['Segment'] = [file_info[2] for _ in range(N)]
#     print(df_in)
#     dfs.append(df_in)

# df = pd.concat([*dfs])
# df = df.pivot(index = ['ID', 'Metric', 'Comparison'], columns = 'Segment', values = 'Value')
# print(df)

# df.to_csv('test1.csv')

# from Metrics import Metrics_Info
overwrite = False
Segments = {'brainstem', 'parotid_merged', 'pcm_low', 'pcm_mid', 'pcm_up'}
Comparisons = {('GT', 'DL'), ('GT', 'DLB')}
Patients = PatientKeys()

for Segment in Segments:
    for MethodA, MethodB in Comparisons:
        file = f'{MethodA}vs{MethodB}&{Segment}.csv'
        try: 
            if overwrite:
                raise FileNotFoundError
            
            df = pd.read_csv('dataframes\\' + file)
        except FileNotFoundError:
            MI0 = Metrics_Info()
            df = pd.DataFrame(columns = MI0.getAttributes().keys())
        
        IterTuple = df[['ID', 'Date']].itertuples(index = False)
        cur_Patients = {(ID, str(Date)) for ID, Date in IterTuple}
        # print(len(cur_Patients), file)
        patient_dfs = []
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
            print(f'Gemmer {file}')
            df.to_csv('dataframes\\' + file, index = False)