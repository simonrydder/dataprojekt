import pandas as pd
import numpy as np

max_tol = 2
dfs = []

for i in range(0,max_tol+1):
    df  = pd.read_csv(f"..\\data\\results\\total_tolerance{i}.csv")
    df = df.drop("Date",axis = 1)
    if i != 0:
        df = df.add_suffix(f"_{i}")
        df = df.drop([f"ID_{i}",f"Comparison_{i}",f"Metric_{i}"],axis = 1)
    dfs.append(df)



df = pd.concat(dfs, axis = 1)


segments = df.columns[3:]

df = pd.melt(df,id_vars=["ID","Metric", "Comparison"],value_vars = segments, var_name="Segment")

df = pd.pivot(df,index = ["ID","Metric","Segment"], columns = "Comparison",values = "value")


for method1,method2 in [("DL","DLB"),("DL","ATLAS"),("ATLAS","DLB")]:
    df["Color_Dice_"+method1 + method2] = ["darkcyan" if x > y 
                                    else "red" if x < y else "black" for x,y in zip(df["GTvs" + method1],df["GTvs"+ method2])]

    df["Color_"+method1 + method2] = ["red" if x > y 
                                    else "darkcyan" if x < y else "black" for x,y in zip(df["GTvs" + method1],df["GTvs" + method2])]
    
    df["Color_Dice_"+method2 + method1] = ["darkcyan" if x > y 
                                    else "red" if x < y else "black" for x,y in zip(df["GTvs" + method2],df["GTvs" + method1])]

    df["Color_"+method2 + method1] = ["red" if x > y 
                                    else "darkcyan" if x < y else "black" for x,y in zip(df["GTvs" + method2],df["GTvs" + method1])]

for method in ["DL","DLB","ATLAS"]:
    df["Color_Dice_"+method + method] = ["darkcyan" if x > y 
                                    else "red" if x < y else "black" for x,y in zip(df["GTvs" + method1],df["GTvs"+ method2])]

    df["Color_"+method + method] = ["red" if x > y 
                                    else "darkcyan" if x < y else "black" for x,y in zip(df["GTvs" + method1],df["GTvs" + method2])]
    


df.to_csv("..\\data\\results\\scatter_data.csv")

df = pd.read_csv("..\\data\\results\\scatter_data.csv")

for color in ["darkcyan","red","black"]:
    for segment in segments:
        new = {'ID': "Dummy", 'Metric': "DICE", 'Segment': segment, 'GTvsATLAS': None, 'GTvsDL': None, 'GTvsDLB': None,
       'Color_Dice_DLDLB': color, 'Color_DLDLB': color, 'Color_Dice_DLBDL': color, 'Color_DLBDL':color,
       'Color_Dice_DLATLAS':color, 'Color_DLATLAS':color, 'Color_Dice_ATLASDL': color,
       'Color_ATLASDL': color, 'Color_Dice_ATLASDLB': color, 'Color_ATLASDLB': color,
       'Color_Dice_DLBATLAS': color, 'Color_DLBATLAS': color,'Color_DLDL': color,'Color_DLBDLB': color,'Color_ATLASATLAS': color}
        df = df.append(new, ignore_index = True)

df.to_csv("..\\data\\results\\scatter_data.csv")
