import pandas as pd

df = pd.read_csv("..\\data\\results\\performance_mean.csv")
metrics = sorted(df["Metric"].unique().tolist())

segments = sorted(df["Segment"].unique().tolist())
comparisons = sorted(df["Comparison"].unique().tolist())

plot_theme = "seaborn"


patients_slider = ["4Prj3A5sMvSv1sK4u5ihkzlnU","PHbmDBLzKFUqHWIbGMTmUFSmO", 
                    "HNCDL_340","HNCDL_447","HNCDL_141"]

segments_slider = ["brainstem","spinalcord",
                    "lips", "esophagus", "pcm_low",
                    "pcm_mid", "pcm_up", "mandible"]