from dash import dcc, html, Input, Output, callback
from dataloading import segments, metrics, comparisons, plot_theme, \
                        df, df_violin, boxplot_segments, df_scatter
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

Style = {'textAlign': 'center', "border-bottom":"2px black solid"}
Styletitles = {'textAlign': 'left'}
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
            html.H3('Barplot of mean performance', style = Styletitles),
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
            html.H3('Violinplots', style = Styletitles),
            #Defining subplots for violin plots
            dcc.Graph(id = "figure_boxplot", figure = {},style = {"height": 700}),
            html.Br(),

#This part is still under construction 
###         
            html.H3('Scatterplot', style = Style),
            dbc.Row([
                dbc.Col([
                        dcc.Dropdown(id="scatter_segments", # dropdown for 
                            options = segments,
                            multi = False,
                            value = segments[0],
                            clearable = False),

                ],width = 7),
                dbc.Col([
                        dbc.Checklist(options =  #Toggle option for tolerance
                        [{"label": "Show Tolerance options", "value": 1}],
                        value=[1],
                        id="tolerance_toggle_scatter",
                        switch=True)
                ], width={"size": 3, "offset": 1})

            ],className="g-0"),
            dcc.Graph(id = "figure_scatter", figure = {},style = {"height": 700}),

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
    [Input(component_id="scatter_segments", component_property="value")])

def update_scatter(segments):
    
    df = df_scatter[df_scatter["Segment"].isin([segments])]
    
    rows = 2
    cols = 3

    fig = make_subplots(rows,cols,
                        x_title="Deep learning",
                        y_title="Deep learning bounded",
                        subplot_titles = metrics)


    scale = [
        [0, "darkcyan"],
        [0.5, "darkcyan"],
        [0.5, "red"],
        [1.0, "red"]
        ]

    i = 0
    for row in range(1,rows+1):
        for col in range(1,cols+1):
            df_metric = df[df["Metric"] == metrics[i]]
            x = df_metric["GTvsDL"]
            y = df_metric["GTvsDLB"]
            x_min = np.nanmin(x)*0.95
            x_max = np.nanmax(x)*1.05
            x_line = np.linspace(x_min,x_max,100)
            if i == 0:
                fig.add_trace(
                        go.Scatter(
                            x = x_line, 
                            y = x_line, 
                            mode = "lines",
                            name = "Identity line",
                            opacity  = 0.5,
                            line = dict(color = "black")),
                            row = row, col = col)
                fig.add_trace(
                        go.Scatter(
                            x = x,
                            y = y,
                            mode = "markers",
                            name = "DLB outperforms DL",
                            marker = dict(color = 
                            ["darkcyan" if x > y 
                            else "red" for x,y in zip(x,y)])),
                            row = row, col = col)
                            
            else:
                fig.add_trace(
                        go.Scatter(
                            x = x_line, 
                            y = x_line, 
                            mode = "lines",
                            name = "Identity line",
                            opacity  = 0.5,
                            line = dict(color = "black"),
                            showlegend = False),
                            row = row, col = col)

                fig.add_trace(
                        go.Scatter(
                            x = x,
                            y = y,
                            mode = "markers",
                            name = segments,
                            showlegend = False,
                            marker = dict(color = 
                            ["red" if x > y else 
                            "darkcyan" for x,y in zip(x,y)])),
                            row = row, col = col)
           
            i+=1
        

    fig.update_layout(template=plot_theme,
    title_text="Performance between ATLAS and Deep Learning model",
    title_x = 0.05,
    title_y = 0.97,
    legend=dict(
                        orientation="h",
                        y=1.1  
                        ))
    return [fig]

@callback(
    [Output("scatter_segments", "options"),
    Output("scatter_segments", "value")],
    [Input("tolerance_toggle_scatter", "value"),
    Input("scatter_segments", "value")])

def toggle_tolerance_Scatter(toggle,current):
    # When turned on return the all segments and value is the current
    if len(toggle) == 1:
        options = segments
        value = current
    else: # When turned off, return only Tolerance 0
        options = [segment for segment in segments if not segment.endswith(("1","2","3","4"))]
        if current in options:
            value = current
        else:
            value = options[0]
    
    # if No 0 Tolerance was in the values set the value equal to the first segment

    return [options,value]

###


@callback(
    [Output(component_id="figure_boxplot", component_property="figure")],
    [Input(component_id="boxplot_comp", component_property="value"),
    Input(component_id="boxplot_segment", component_property="value")])

def update_scatter(comps,segment):
    
    metrics = ["DICE","LineRatio","VolumeRatio","EPL","MSD","Hausdorff"]
    rows = 2
    cols = 3

    fig = make_subplots(rows,cols,
                        x_title="Tolerance",
                        y_title="Value",
                        subplot_titles = metrics)

    i = 0
    color_dict = {"GTvsDL": "cornflowerblue", "GTvsDLB": "orange"}
    legend_show = [True]+[False]*5

    for row in range(1,rows+1):
        for col in range(1,cols+1):
            df = df_violin[df_violin["Metric"]==metrics[i]]
            for comp in comps:
                df_comp = df[df["Comparison"]==comp]
                x = df_comp["Tolerance"].squeeze()
                y = df_comp[segment].squeeze()
                if i == 0:
                    fig.add_trace(go.Violin(x = x,
                                y = y,line_color = color_dict.get(comp),
                                name = comp),row = row, col = col)
                else:
                    fig.add_trace(go.Violin(x = x,
                                y = y,line_color = color_dict.get(comp),
                                showlegend = False),row = row, col = col)

                        
        
           
            i+=1

    fig.update_layout(violinmode='overlay',
    template=plot_theme,
    legend=dict(
                        orientation="h",
                        y=1.1  
                        ))
        
    return [fig]
