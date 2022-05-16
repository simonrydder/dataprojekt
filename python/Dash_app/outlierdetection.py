'''
outlier detection script to filter out outliers for violin/boxplots and storing them for later inspection
'''

#packages
#from dataloading import df_violin
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pandas as pd
from sklearn.ensemble import IsolationForest


def outlierDectection(original_df):
    # Creating temporary lists to store dataframes
    temp = []
    outliers = []
    # A nice n^4 loop right here boy:
    for comparison in original_df['Comparison'].unique().tolist():
        for metric in original_df['Metric'].unique().tolist():
            for tol in original_df['Tolerance'].unique().tolist():
                for segment in original_df.columns[4:18].tolist():
                    print(comparison, metric, tol, segment)


                    #Filtering
                    df = original_df[original_df['Comparison'] == comparison]
                    df = df[df["Metric"]== metric]
                    df = df[df["Tolerance"]==tol]

                
                    # Define new df with all the filtered data including one segment and drop na. 
                    df =  df[['ID', 'Date', 'Comparison', 'Metric', 'Tolerance', segment]].dropna()


                    # Initialize decisiontree model. Contamination is the sensitive parameter.
                    model=IsolationForest(n_estimators=100, max_samples='auto', contamination=float(0.05),max_features=1.0)

                    # No interesting outliers in metrics with range(0,1)
                    if metric not in ['MSD', 'EPL', 'Hausdorff']:
                        temp.append(df)
                    else:
                        try:
                            # Fit the model if possible
                            model.fit(df[[segment]])

                            # New columns with scores and true/false anomaly. 
                            df['scores']=model.decision_function(df[[segment]])
                            df['anomaly']=model.predict(df[[segment]])


                            # Filter anomalies and append to temporary lists
                            outlier_df=df.loc[df['anomaly']==-1].drop(['anomaly', 'scores'], axis = 1)

                            df = df.loc[df['anomaly']==1].drop(['anomaly','scores'], axis = 1)
                            
                            temp.append(df)
                            outliers.append(outlier_df)


                        except ValueError:
                            temp.append(df)

            

    # Concatenate the temporary lists. 
    df = pd.concat(temp).reset_index(drop = True)
    outliers = pd.concat(outliers).reset_index(drop = True)

    # Merge na rows inside the dataframe
    df = df.groupby(['ID', 'Comparison', 'Date', 'Metric', 'Tolerance'],as_index=False).first()
    outliers = outliers.groupby(['ID', 'Comparison', 'Date', 'Metric', 'Tolerance'],as_index=False).first()

    df = df.sort_values(by = ['ID', 'Date', 'Comparison'])
    outliers = outliers.sort_values(by = 'ID')
    
    # Save df's
    df.to_csv("..\\data\\results\\total_merged_no_outliers.csv")
    outliers.to_csv("..\\data\\results\\total_merged_outliers.csv")
    
    return df, outliers

df_violin = pd.read_csv("..\\data\\results\\total_merged.csv", index_col = 0)
df, outliers = outlierDectection(df_violin)


