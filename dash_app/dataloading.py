import pandas as pd
import urllib

_git_url = 'https://raw.githubusercontent.com/'
_branch = 'simon'
_main_url = f'simonrydder/dataprojekt/{_branch}/data/results/'
_base_url = _git_url + _main_url
_max_tol = 10
_suffix = tuple([str(i) for i in range(_max_tol)])


# Dataframes for EPL Visualization
_tolerances_epl = []
for tol in range(_max_tol):
    try:
        _df = pd.read_csv(_base_url + f'total_merged_slice_{tol}.csv')

    except:
        pass

    else:
        exec(f'df_slice_{tol} = _df')
        _tolerances_epl.append(tol)


# Dataframe for median bar plot
df_median = pd.read_csv(_base_url + 'performance_median.csv')


# Datafram for violin plot
df_violin = pd.read_csv(_base_url + 'total_merged.csv')


# Dataframes for box plot
df_no_outliers = pd.read_csv(_base_url + 'total_merged_no_outliers.csv')
df_outliers = pd.read_csv(_base_url + 'total_merged_outliers.csv')


# Datafreams for scatter plot
df_scatter = pd.read_csv(_base_url + 'scatter_data.csv')


# Functions for dropdown genration
def _get_bar_tolerances(segments, tol):

    suffix = tuple([str(i) for i in range(tol)])
    no_tol_segments = [seg for seg in segments if seg.endswith(suffix)]

    if len(no_tol_segments) != 0:
        tolerances = [0]
    else:
        tolerances = []
    
    tols = {int(seg.split('_')[-1]) for seg in segments if seg.endswith(suffix)}
    for tol in sorted(list(tols)):
        tolerances.append(tol)

    return tolerances


def _get_box_segments(df):
    otherCols = {'ID', 'Date', 'Comparison', 'Metric', 'Tolerance'}
    segments = [c for c in df.columns if c not in otherCols]
    return sorted(segments)


# Defining dropdowns for median bar plot
dd_bar_metrics = sorted(df_median['Metric'].unique().tolist())
dd_bar_segments = sorted(df_median["Segment"].unique().tolist())
dd_bar_segments_notol = [seg for seg in dd_bar_segments if not seg.endswith(_suffix)]
dd_bar_comparisons = sorted(df_median["Comparison"].unique().tolist())
dd_bar_tolerances = _get_bar_tolerances(dd_bar_segments, _max_tol)


# Defining dropdowns for violin/box plot
dd_box_segments = _get_box_segments(df_violin)
dd_box_tolerances = sorted(df_violin['Tolerance'].unique().tolist())
dd_box_metrics = dd_bar_metrics[0::2] + dd_bar_metrics[1::2]


# Defining dropdowns for scatter
dd_scatter_methods = [c.split('vs')[-1] for c in df_scatter.columns if 'vs' in c]
dd_scatter_segments = dd_bar_segments
dd_scatter_segments_notol = dd_bar_segments_notol
dd_scatter_metrics = dd_box_metrics


# Defining dropdowns for EPL Visualization
for tol in range(_max_tol):
    try:
        exec(f'df = df_slice_{tol}')

    except NameError:
        df = None

    else:
        dd_epl_patients = sorted(df['ID'].unique().tolist())
        dd_epl_segments = sorted(df['Segment'].unique().tolist())
        dd_epl_comparisons = sorted(df['Comparison'].unique().tolist())
        break

dd_epl_tolerances = _tolerances_epl


# Other constants
units = {"DICE": "%","EPL": "mm", "Hausdorff": "mm", 
            "MSD": "mm","LineRatio": "%", "VolumeRatio": "%", "Haus": "mm"}
plot_theme = "seaborn"

optionbar = {'displaylogo': False,
        'modeBarButtonsToRemove': 
        ['zoomIn', 'zoomOut','autoScale','select','lasso2d']}