import pandas as pd
from ast import literal_eval

df = pd.read_csv("..\\data\\results\\merged.csv", index_col = 0)
metrics = sorted(df["Metric"].unique().tolist())
df = df.drop(["Date"], axis = 1).round(2)
df = df.groupby(["Comparison","Metric"]).mean().reset_index()
df = df.melt(id_vars=["Comparison", "Metric"], 
    var_name="Segment", 
    value_name="value") 

segments = sorted(df["Segment"].unique().tolist())
comparisons = sorted(df["Comparison"].unique().tolist())

plot_theme = "seaborn"


patients_slider = ["4Prj3A5sMvSv1sK4u5ihkzlnU","PHbmDBLzKFUqHWIbGMTmUFSmO", 
                    "HNCDL_340","HNCDL_447","HNCDL_141"]

segments_slider = ["brainstem","spinalcord",
                    "lips", "esophagus", "pcm_low",
                    "pcm_mid", "pcm_up", "mandible"]