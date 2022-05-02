import pandas as pd

dfs = []

for i in range(0,5):
    df  = pd.read_csv(f"..\\data\\results\\total_tolerance{i}.csv")
    df = df.drop("Date",axis = 1)
    if i != 0:
        df = df.add_suffix(f"_{i}")
    dfs.append(df)
    

df = pd.concat(dfs, axis = 1)
df = df.groupby(["Comparison","Metric"]).mean().reset_index()
df = df.melt(id_vars=["Comparison", "Metric"], 
    var_name="Segment", 
    value_name="value")

df.to_csv("..\\data\\results\\performance_mean.csv")






