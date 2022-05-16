import pandas as pd

#Dataframe for mean plot
df = pd.read_csv("..\\data\\results\\performance_median.csv")
metrics = sorted(df["Metric"].unique().tolist())


#Dataframe for slice plots
df_slices = pd.read_csv("..\\data\\sliceresults\\total.csv")
df_slices = df_slices.drop(df_slices[df_slices["DICE"] > 10].index)
cols_to_change = ["PointsModel","PointsGT","LinesModel","LinesChanged"]

for col in cols_to_change:
    df_slices[col] = df_slices[col].replace(["set()"],["[]"])


#Dataframe for violin plots
df_violin = pd.read_csv("..\\data\\results\\total_merged.csv", index_col = 0).reset_index(drop = True)

df_boxplot =pd.read_csv("..\\data\\results\\total_merged_no_outliers.csv", index_col = 0)





# Defining options for dropdowns
segments = sorted(df["Segment"].unique().tolist())
comparisons = sorted(df["Comparison"].unique().tolist())
tolerances = sorted(df_violin["Tolerance"].unique().tolist())
boxplot_segments = [segment for segment in segments if not segment.endswith(("1","2","3","4"))]

patients_slider = ["4Prj3A5sMvSv1sK4u5ihkzlnU","PHbmDBLzKFUqHWIbGMTmUFSmO", 
                    "HNCDL_340","HNCDL_447","HNCDL_141"]

segments_slider = ["brainstem","spinalcord",
                    "lips", "esophagus", "pcm_low",
                    "pcm_mid", "pcm_up", "mandible"]

df_scatter = pd.read_csv("..\\data\\results\\scatter_data.csv")

#Setting plot theme
plot_theme = "seaborn"