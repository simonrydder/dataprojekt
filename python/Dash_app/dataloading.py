import pandas as pd
from ast import literal_eval

df = pd.read_csv("..\\data\\results\\performance_mean.csv")
metrics = sorted(df["Metric"].unique().tolist())

df_slices = pd.read_csv("..\\data\\sliceresults\\total.csv")
df_slices = df_slices.drop(df_slices[df_slices["DICE"] > 10].index)
cols_to_change = ["PointsModel","PointsGT","LinesModel","LinesChanged"]

for col in cols_to_change:
    df_slices[col] = df_slices[col].replace(["set()"],["[]"])

df_violin = pd.read_csv("..\\data\\results\\total_merged.csv")

segments = sorted(df["Segment"].unique().tolist())
comparisons = sorted(df["Comparison"].unique().tolist())

boxplot_segments = [segment for segment in segments if not segment.endswith(("1","2","3","4"))]

plot_theme = "seaborn"


patients_slider = ["4Prj3A5sMvSv1sK4u5ihkzlnU","PHbmDBLzKFUqHWIbGMTmUFSmO", 
                    "HNCDL_340","HNCDL_447","HNCDL_141"]

segments_slider = ["brainstem","spinalcord",
                    "lips", "esophagus", "pcm_low",
                    "pcm_mid", "pcm_up", "mandible"]