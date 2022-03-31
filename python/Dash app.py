import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from DataReader import Path
from DataPreparation import OAR_Image
import numpy as np
from ast import literal_eval
from plotly.subplots import make_subplots
import dash_daq as daq

app = dash.Dash(__name__)

# Read data and prep it
df = pd.read_csv("data_perform.csv")
metrics = df["Metric"].unique().tolist()
df = df.drop(["Date"], axis = 1).round(2)
df = df.groupby(["Comparison","Metric"]).mean().reset_index()
df = df.melt(id_vars=["Comparison", "Metric"], 
    var_name="Segment", 
    value_name="value") 

df_organs = pd.read_csv("data_organ_test.csv")
df_slices = pd.read_csv("data_slices_test.csv")

cols_to_change = ["xA","yA","xB","yB","VA","HA","VB","HB"]

for col in cols_to_change:
    df_organs[col] = df_organs[col].apply(literal_eval)
    df_slices[col] = df_slices[col].apply(literal_eval)

#options for dropdowns
segments = df["Segment"].unique().tolist()
comparisons = df["Comparison"].unique().tolist()
organs = df_organs["Segment"].unique().tolist()
patients_slider = df_slices["Patient"].unique().tolist()
segments_slider = df_slices["Segment"].unique().tolist()

#defining Plot theme

plot_theme = "seaborn"

### creating layout

app.layout = html.Div([
    #Performance plot
    html.H1("Dashboard", style ={"text-align": "center"}), #creates a header
    html.Div([dcc.Dropdown(id="slct_metrics", # dropdown for metrics
                    options =metrics,
                    multi = True,
                    value = [metrics[0]],
                    style = {"width": 800},
                    clearable = False),
    dcc.Dropdown(id="slct_segment", # Dropdown for segments
                    options =segments,
                    multi = True,
                    value = [segments[0]],
                    style = {"width": 400,"display": "inline-block"},
                    clearable = False),
    dcc.Dropdown(id="slct_comp", #Dropdown for comparisons
                    options =comparisons,
                    multi = True,
                    value = [comparisons[0]],
                    style = {"width": 400,"display": "inline-block"},
                    clearable = False)]),
    html.Br(),
    dcc.Graph(id = "figure_perf", figure = {}), #Initializing figure
    html.Br(),
    # Plot for one organ
    dcc.Dropdown(id="segment_organ", #Dropdown for organs
                    options =organs,
                    multi = False,
                    value = organs[0],
                    style = {"width": 400},
                    clearable = False),

    html.Br(),
    dcc.Graph(id = "figure_organ", figure = {}, #Initializing figure
                style={ 'height': 900}), 
    html.Br(),

    # Slider plot
    html.Div(id='slider-container', children=[
        daq.Slider(id = "slider", # Slider to switch slice (z)
                    min = 0, 
                   max = 18,
                   value = 0, 
                   step = 1, 
                   size = 900,
                   handleLabel="slice",
                   marks={'18': 'mark'}),

        dcc.Dropdown(id = "patient", # Dropdown for Patient
                    options = patients_slider, 
                    multi = False,
                    value = patients_slider[0],
                    style = {"width": 450, 
                    "display": "inline-block"},
                    clearable = False),

        dcc.Dropdown(id = "segment_slider", #Dropdown for segments
                    options = segments_slider,
                    multi = False,
                    value = segments_slider[0],
                    style = {"width": 450,
                    "display": "inline-block"},
                    clearable = False)
        ]),

    dcc.Graph(id = "figure_slider", figure = {}, #Initializing figure
             style={'width': 900, 
             'height': 600,'display': 'inline-block'}),

    # html.Div(id = "performance", children = [], #Initializing Peformance box
    #          style={'width': '30%',
    #                 'display': 'inline-block', 
    #                 'verticalAlign': 'top',
    #                 'margin-left': 10,
    #                 "border":"2px black solid"})


])

### connections

##Performance plot

#defining where output should go and where input is from
@app.callback(
    [Output(component_id="figure_perf", component_property="figure")],
    [Input(component_id="slct_metrics", component_property="value"),
    Input(component_id="slct_segment", component_property="value"),
    Input(component_id="slct_comp", component_property="value")]
)

# Function to update performance plot
def update_graph(slct_metrics, slct_segment,slct_comp):

    # Finds the matching data
    df_perf = df[df["Metric"].isin(slct_metrics)]
    df_perf = df_perf[df_perf["Segment"].isin(slct_segment)]
    df_perf = df_perf[df_perf["Comparison"].isin(slct_comp)]
    
    
    fig = px.bar(df_perf, #Creates barplot
                x = "Comparison", 
                y = "value", 
                color = "Segment", 
                barmode = "group",
                facet_col = "Metric",
                title = "Performance",
                template = plot_theme)

    fig.update_yaxes(matches=None) #Creates individual yaxis for subplots
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True)) # shows labels for all yaxis
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # changes subplot title

    #Changes range of yaxis to [0,1] for "DICE", "MSD", "APL_L", "APL_V"
    plots = []
    axes = ["yaxis","yaxis2","yaxis3","yaxis4","yaxis5","yaxis6"]
    fig.for_each_annotation(lambda trace: plots.append(trace.text))
    
    for idx,plot in enumerate(plots):
        if plot not in ["APL","Hausdorff","MSD"]:
            fig["layout"][axes[idx]].update(range = [0,1])

    # #Changes width of bars
    # for data in fig.data:
    #     data["width"] = 0.15

    return [fig]


# @app.callback(
#     Output(component_id="slct_metrics", component_property="value"),
#     [
#     Input(component_id="slct_metrics", component_property="value"),
#     ],
# )
# def update_dropdown_options(values):
#     if len(values) > 4:
#         return ["APL","DICE"]
#     else:
#         return ()

## Organ plot

#defining where output should go and where input is from
@app.callback(
    [Output(component_id="figure_organ", component_property="figure")],
    [Input(component_id="segment_organ", component_property="value")]
)

#Function to update organ plot
def update_segment_plot(segment_organ):

    #Finding them matching data
    df_organ = df_organs[df_organs["Segment"]==segment_organ]
    patients = df_organ["Patient"].unique().tolist()

    fig2 = go.Figure() #initializing figure

    rows = 2
    cols = 3
    N = rows*cols

    fig2 = make_subplots(rows,cols, subplot_titles=tuple(patients[:N])) #creates subplots

    for idx,row in enumerate(range(rows)):
        for col in range(cols):
            xA = df_organ[df_organ["Patient"] == patients[idx]]["xA"].tolist()[0]
            yA = df_organ[df_organ["Patient"] == patients[idx]]["yA"].tolist()[0]
            xB = df_organ[df_organ["Patient"] == patients[idx]]["xB"].tolist()[0]
            yB = df_organ[df_organ["Patient"] == patients[idx]]["yB"].tolist()[0]

            if row == 0 and col == 0:
                fig2.add_trace( #adds points for A to subplot 1,idx+1
                    go.Scatter(x=xA, 
                                y=yA, 
                                mode = "markers",
                                name = "GT",
                                marker=dict(color='red',size=8)),
                                row+1, col+1)
                
                fig2.add_trace( #adds points for B to subplot 1,idx+1
                    go.Scatter(x=xB, 
                                y=yB, 
                                mode = "markers", 
                                name = "Guess",
                                marker=dict(color='LightSkyBlue',size=6)),
                                row+1, col+1)
            else:
                fig2.add_trace( #adds points for A to subplot 1,idx+1
                    go.Scatter(x=xA, 
                                y=yA,
                                mode = "markers", 
                                name = "GT", 
                                showlegend = False,
                                marker=dict(color='red',size=8)), 
                                row+1, col+1)
                
                fig2.add_trace( #adds points for B to subplot 1,idx+1
                    go.Scatter(x=xB,
                                y=yB, 
                                mode = "markers", 
                                name = "Guess",     
                                showlegend = False,
                                marker=dict(color='LightSkyBlue',size=6)),
                                row+1, col+1)   

    fig2.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=1.15,
    xanchor="left"),font = dict(size = 20))
   
    fig2.update_layout(template=plot_theme) # set the theme

    fig2.for_each_yaxis(lambda yaxis: yaxis.update(matches = None, #scale yaxes to match xaxes
    scaleanchor = "x", scaleratio = 1, visible = False))

    fig2.for_each_xaxis(lambda xaxis: xaxis.update(visible = False))

    return [fig2]


# @app.callback(
#    Output(component_id='slider', component_property="max"),
#    [Input(component_id='patient', component_property='value')])

# def myfunc(patient):
#     df_slice = df_slices[df["patient"==patient]]
#     return [df_slice["idx"].max()]
    
## Slider plot

#defining where output should go and where input is from
@app.callback(
    [Output(component_id="figure_slider", component_property="figure")],
    [Input(component_id="slider", component_property="value"),
    Input(component_id="patient", component_property="value"),
    Input(component_id="segment_slider", component_property="value")])

#Function to update slider plot
def update_slider(slider, patient,segment_slider):
    
    #Finding the matching data
    df_slice = df_slices[df_slices["idx"]==slider]
    df_slice = df_slice[df_slice["Patient"]==patient]
    df_slice = df_slice[df_slice["Segment"]==segment_slider]
    xA = df_slice["xA"].tolist()[0]
    yA = df_slice["yA"].tolist()[0]
    xB = df_slice["xB"].tolist()[0]
    yB = df_slice["yB"].tolist()[0]


    fig3 = go.Figure()
    fig3.add_trace( #adds points for A to the figure
        go.Scatter(x=xA,
                    y=yA,
                    mode = "markers", 
                    name = "GT",
                    marker=dict(color='red',size=8)))
            
    fig3.add_trace( #adds points for B to the figure
        go.Scatter(x=xB, 
                    y=yB, mode = "markers", 
                    name = "Guess",
                    marker=dict(color='LightSkyBlue',size=6)))
                    
    fig3.update_layout(template=plot_theme) #set theme

    fig3.update_yaxes(scaleanchor = "x", scaleratio = 1) #scales yaxes to xaxes

    #Finding matching data
    df_perf = df_slice[df_slice["idx"]==slider]
    df_perf = df_perf.iloc[0]

    metrics = ["APL","APL_L","APL_V","DICE","Hausdorff","MSD"] #all metrics
    title =  ""# initializing title

    #creating output string
    for idx, metric in enumerate(metrics):
        value = np.round(df_perf[metric],2)
        title += f"{metric}: {value}  "
        if idx == 2:
            title += "<br>"
        

    fig3.update_layout(title = title)
                    
    return [fig3]

# Changing Options for dropdown when changing patient
@app.callback(
    [Output(component_id="segment_slider", component_property="options"),
    Output(component_id="segment_slider", component_property="value")],
    [Input(component_id="patient", component_property="value"),
    Input(component_id="segment_slider", component_property="value")])

def change_options(patient,current):
    options = df_slices[df_slices["Patient"]==patient] \
                            ["Segment"].unique().tolist()
    if current in options:
        value = current
    else:
         value = options[0]
    return [options,current]


#Change slider range and reset the value of the slider
@app.callback(
    [Output(component_id="slider", component_property="max"),
    Output(component_id="slider", component_property="value")],
    [Input(component_id="patient", component_property="value"),
    Input(component_id="segment_slider", component_property="value")])

def change_slider_range(patient,segment):
    df_plot = df_slices[df_slices["Patient"]==patient]
    df_plot = df_plot[df_plot["Segment"]==segment]
    return [df_plot["idx"].max(),0]
    


# Run the app:
if __name__ == "__main__":
    app.run_server(debug=True)





