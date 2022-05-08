from dash import dcc, html, Input, Output, callback
from dataloading import segments, metrics, comparisons, plot_theme, \
                        df, df_violin, boxplot_segments, df_scatter
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd

Style = {'textAlign': 'center', "border-bottom":"2px black solid"}

#Defining layout for the site 

layout = html.Div([
    html.H1('Performance', style = Style),
    html.Br(),
            dbc.Row([
                dbc.Col([
                        dcc.Dropdown(id="slct_segment", # dropdown for segment for mean performance
                        options =segments,
                        multi = True,
                        value = [segments[0]],
                        clearable = True)

                ], width = 9),
                dbc.Col([
                        dbc.Checklist(options =  #Toggle option for tolerance
                        [{"label": "Show Tolerance options", "value": 1}],
                        value=[1],
                        id="tolerance_toggle",
                        switch=True)
                ],width = 3)
            ]),

            dbc.Row([
                dbc.Col([
                        dcc.Dropdown(id="slct_metrics", # Dropdown for metrics for mean performance 
                        options =metrics,
                        multi = True,
                        value = metrics,
                        clearable = True)
                ],width = 6),
                dbc.Col([ dcc.Dropdown(id="slct_comp", #Dropdown for comparisons for mean performance
                            options =comparisons,
                            multi = True,
                            value = comparisons,
                            clearable = True)
                ],width = 6)
            ],className="g-0"),

            html.Br(),
            dcc.Graph(id = "figure_perf", figure = {}), #Initializing mean performance figure,
            html.Br(),

            dbc.Row([
                dbc.Col([ 
                    dcc.Dropdown(id="boxplot_segment", # dropdown for metrics for violin plot
                        options =boxplot_segments, 
                        multi = False,
                        value = [boxplot_segments[0]],
                        clearable = False)
                ], width = 4),
                dbc.Col([
                    dcc.Dropdown(id="boxplot_comp", # dropdown for comparisons for violin plot
                        options = comparisons,
                        multi = True,
                        value = [comparisons[0]],
                        clearable = True)
                ], width = 4)
            ],className="g-0"),

            html.Br(),

            #Defining subplots for violin plots
             dbc.Row([
                dbc.Col([
                    dcc.Graph(id = "figure_DICE", 
                              figure = {}, 
                              style = {"height": 350})
                ],width = 4),
                dbc.Col([
                    dcc.Graph(id = "figure_Line", 
                             figure = {}, 
                             style = {"height": 350})
                ],width = 4),
                dbc.Col([ 
                    dcc.Graph(id = "figure_Volume", 
                              figure = {}, 
                              style = {"height": 350})
                ],width = 4)
            ],className="g-0"),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id = "figure_EPL", 
                              figure = {}, 
                              style = {"height": 350})
                ],width = 4),
                dbc.Col([  
                    dcc.Graph(id = "figure_MSD",
                              figure = {}, 
                              style = {"height": 350})
                ],width = 4),
                dbc.Col([ 
                    dcc.Graph(id = "figure_Haus", 
                              figure = {}, 
                            style = {"height": 350})
                ],width = 4)
            ],className="g-0"),
            html.Br(),

#This part is still under construction 
### 
            dbc.Row([
                dbc.Col([
                        dcc.Dropdown(id="scatter_metric", # dropdown for metrics
                        options =metrics,
                        multi = True,
                        value = [metrics[0]],
                        clearable = True)],
                        width = 5),
                dbc.Col([
                        dcc.Dropdown(id="scatter_segments", # dropdown for 
                            options = segments,
                            multi = True,
                            value = [segments[0]],
                            clearable = False),

                ],width = 7)

            ],className="g-0"),
            dcc.Graph(id = "figure_scatter", figure = {}),

            # Download button csv for performance data:

            html.Br(),
            dbc.Button("Download CSV", id="btn"),
            dcc.Download(id="download")
###
]) # End of layout


#Update graph for mean performance
@callback(
  [Output(component_id="figure_perf", component_property="figure")],
    [Input(component_id="slct_metrics", component_property="value"),
    Input(component_id="slct_segment", component_property="value"),
    Input(component_id="slct_comp", component_property="value")])

# Function to update performance plot
def update_graph(slct_metrics, slct_segment,slct_comp):
    
    # Filtering Data
    df_perf = df[df["Metric"].isin(slct_metrics)]
    df_perf = df_perf[df_perf["Segment"].isin(slct_segment)]
    df_perf = df_perf[df_perf["Comparison"].isin(slct_comp)]

    
    
    fig = px.bar(df_perf, #Creates barplot
                x = "Comparison", 
                y = "value", 
                color = "Segment", 
                barmode = "group",
                facet_col = "Metric",
                template = plot_theme,
                facet_col_spacing=0.04
            )

    fig.update_yaxes(matches=None) #Creates individual yaxis for subplots
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True)) # shows labels for all yaxis
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # changes subplot title


    #Changes range of yaxis to [0,1] for "DICE", "LineRatio", "VolumeRatio"
    plots = []
    axes = ["yaxis","yaxis2","yaxis3","yaxis4","yaxis5","yaxis6"]
    fig.for_each_annotation(lambda trace: plots.append(trace.text))
    
    for idx,plot in enumerate(plots):
        if plot not in ["EPL","Hausdorff","MSD"]:
            fig["layout"][axes[idx]].update(range = [0,1])

    return [fig]


# Make metrics dropdown non clearable
@callback(
    [Output(component_id="slct_metrics", component_property="value")],
    [Input(component_id="slct_metrics", component_property="value")])
def update_dropdown_options_metric(values):
    if len(values) == 0:
        return [[metrics[0]]]
    else:
        return [values]

# Make comp dropdown non clearable
@callback(
    [Output(component_id="slct_comp", component_property="value")],
    [Input(component_id="slct_comp", component_property="value")])
def update_dropdown_options_comp(values):
    if len(values) == 0:
        return[[comparisons[0]]]
    else:
        return [values]

# Toggle tolerance options on and off
@callback(
    [Output("slct_segment", "options"),
    Output("slct_segment", "value")],
    [Input("tolerance_toggle", "value"),
    Input("slct_segment", "value")])

def toggle_tolerance(toggle,current):
    # When turned on return the all segments and value is the current
    if len(toggle) == 1:
        options = segments
        values = current
    else: # When turned off, return only Tolerance 0
        options = [segment for segment in segments if not segment.endswith(("1","2","3","4"))]
        values = [segment for segment in current if segment in options]
    
    # if No 0 Tolerance was in the values set the value equal to the first segment
    if len(values) == 0:
        values = [segments[0]]

    return [options,values]

    
# Creating Violinplot
@callback(
    [Output(component_id="figure_DICE", component_property="figure"),
    Output(component_id="figure_Line", component_property="figure"),
    Output(component_id="figure_Volume", component_property="figure"),
    Output(component_id="figure_EPL", component_property="figure"),
    Output(component_id="figure_MSD", component_property="figure"),
    Output(component_id="figure_Haus", component_property="figure")],
    [Input(component_id="boxplot_comp", component_property="value"),
    Input(component_id="boxplot_segment", component_property="value")])

def update_violin_plots(comps,segment):
    metrics = ["DICE","LineRatio","VolumeRatio","EPL","MSD","Hausdorff"]
    figs = [] #Initializing a list of figs to return

    # For each metric create a violin plot
    for metric in metrics:
        #Filtering data
        df = df_violin[df_violin["Metric"]==metric]
        df = df[df["Comparison"].isin(comps)]
        fig = px.violin(df,
                        x = "Tolerance",
                        y = segment,
                        facet_col = "Metric",
                        color = "Comparison",
                        violinmode="overlay",
                        template = plot_theme
                )

        # If it is the first metric add a legend in the upper left corner
        if metric == metrics[0]:
            fig.update_layout(legend=dict(
                        orientation="h",
                        y=1.25,  
                        ),margin=dict(l=0, r=10, b=0))
        else:
            fig.update_layout(showlegend = False,
             margin=dict(l=0, r=10, b=0)
            )

        #Change titles
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        #Append to the figs list
        figs.append(fig)

    return figs

# make comparisons for violin plots non clearable
@callback(
    [Output(component_id="boxplot_comp", component_property="value")],
    [Input(component_id="boxplot_comp", component_property="value")])
def update_dropdown_options_comp(values):
    if len(values) == 0:
        return[[comparisons[0]]]
    else:
        return [values]


# Load the correct csv file and make it downloadable:

result_file = pd.read_csv("..\\data\\results\\total_merged.csv", index_col=0)

@callback(
    Output("download", "data"),
    Input("btn", "n_clicks"),
    prevent_initial_call =True,
)

def generate_csv(n_clicks):
    return dcc.send_data_frame(result_file.to_csv, "results.csv")

# Still under construction

###
@callback(
    [Output(component_id="figure_scatter", component_property="figure")],
    [Input(component_id="scatter_segments", component_property="value"),
    Input(component_id="scatter_metric", component_property="value")])

def update_scatter(segments,metric):
    df = df_scatter[df_scatter["Metric"].isin(metric)]
    df = df[df["Segment"].isin(segments)]
    
    x = np.linspace(0,1,100)

    fig = go.Figure()
    x = df["GTvsDL"]
    y = df["GTvsDLB"]
    color = df["Segment"]
    facet_col = df["Metric"]
    fig.add_trace(go.Scatter(
                    x = x,
                    y = y,
                    mode = "markers",
                    name = "segment"))

    fig.add_trace(
        go.Scatter(
            x = x, 
            y = x, 
            mode = "lines",
            name = "identity line"))

    return [fig]

###