import pandas as pd

dfs = []
max_tol = 2 #set the max number of tolerance

#Creating median performance csv file (median more robust to outliers)
for i in range(0,max_tol+1):
    df  = pd.read_csv(f"..\\data\\results\\total_tolerance{i}.csv")
    df = df.drop("Date",axis = 1)
    if i != 0:
        df = df.add_suffix(f"_{i}")
    dfs.append(df)
    

df = pd.concat(dfs, axis = 1)
df = df.groupby(["Comparison","Metric"]).median().reset_index()
df = df.melt(id_vars=["Comparison", "Metric"], 
    var_name="Segment", 
    value_name="value")

df.dropna(inplace=True)
df = df.reset_index(drop = True)

df.to_csv("..\\data\\results\\performance_median.csv")

#Create violin plot results csv
dfs = []
for i in range(max_tol + 1):
    df  = pd.read_csv(f"..\\data\\results\\total_tolerance{i}.csv")
    df["Tolerance"] = i
    dfs.append(df)


df = pd.concat(dfs)
df.to_csv("..\\data\\results\\total_merged.csv")






