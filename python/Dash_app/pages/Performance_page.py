from dash import dcc, html, Input, Output, callback
from dataloading import segments, metrics, comparisons, plot_theme, \
                        df, df_violin, df_boxplot, boxplot_segments, df_scatter, tolerances
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from numpy import isnan

Style = {'textAlign': 'center', "border-bottom":"2px black solid"}
Styletitles = {'textAlign': 'left'}
#Defining layout for the site 

layout = html.Div([
    html.H1('Performance', style = Style),
    html.Br(),
            html.Br(),
            html.H3('Barplot of median performance', style = Styletitles),
            dbc.Row([
                dbc.Col(["Segments"],width = 1, align = "center"),
                dbc.Col([
                        dcc.Dropdown(id="slct_segment", # dropdown for segment for mean performance
                        options =segments,
                        multi = True,
                        value = [segments[0]],
                        clearable = True)

                ], width = 8),
                dbc.Col([
                        dbc.Checklist(options =  #Toggle option for tolerance
                        [{"label": "Show Tolerance options", "value": 1}],
                        value=[1],
                        id="tolerance_toggle",
                        switch=True)
                ],width = 3, align = "center")
            ]),

            dbc.Row([
                dbc.Col(["Metrics"],width = 1, align = "center"),
                dbc.Col([
                        dcc.Dropdown(id="slct_metrics", # Dropdown for metrics for mean performance 
                        options =metrics,
                        multi = True,
                        value = metrics,
                        clearable = True)
                ],width = 8)]),
            dbc.Row([
                dbc.Col(["Methods"],width = 1, align = "center"),
                dbc.Col([ dcc.Dropdown(id="slct_comp", #Dropdown for comparisons for mean performance
                            options =comparisons,
                            multi = True,
                            value = comparisons,
                            clearable = True)
                ],width = 8)]),
            html.Br(),
            dcc.Graph(id = "figure_perf", figure = {}), #Initializing mean performance figure

            # Download button csv for performance data:
            html.Br(),
            dbc.Button("Download CSV", id="btn"),
            dcc.Download(id="download"),
            html.Br(),
            html.Br(),
            html.H3('Violinplots', style = Styletitles),
            dbc.Row([
                dbc.Col(["Segment"], width = 1),
                dbc.Col([ 
                    dcc.Dropdown(id="violin_segment", # dropdown for metrics for violin plot
                        options =boxplot_segments, 
                        multi = False,
                        value = [boxplot_segments[0]],
                        clearable = False)
                ], width = 4)
            ]),
            dbc.Row([
                dbc.Col(["Tolerance"], width = 1),
                dbc.Col([
                    dcc.Dropdown(id="violin_comp", # dropdown for comparisons for violin plot
                        options = tolerances,
                        multi = True,
                        value = [tolerances[0]],
                        clearable = True)
                ], width = 4)
            ]),
            #Defining subplots for violin plots
            html.Br(),
            dcc.Graph(id = "figure_violin", figure = {},style = {"height": 700}),
            html.Br(),
            html.H3('Boxplots', style = Styletitles),
            dbc.Row([
                dbc.Col(["Segment"], width = 1),
                dbc.Col([ 
                    dcc.Dropdown(id="boxplot_segment", # dropdown for metrics for violin plot
                        options =boxplot_segments, 
                        multi = False,
                        value = [boxplot_segments[0]],
                        clearable = False)
                ], width = 4)
            ]),
            dbc.Row([
                dbc.Col(["Tolerance"], width = 1),
                dbc.Col([
                    dcc.Dropdown(id="boxplot_comp", # dropdown for comparisons for violin plot
                        options = tolerances,
                        multi = True,
                        value = [tolerances[0]],
                        clearable = True)
                ], width = 4)
            ]),
            #Defining subplots for boxplots
            html.Br(),
            dcc.Graph(id = "figure_boxplot", figure = {},style = {"height": 700}),
            html.Br(),

#This part is still under construction 
###         
            html.H3('Scatterplots', style = Styletitles),
            dbc.Row([
                dbc.Col(["Segment"], width = 1,align = "center"),
                dbc.Col([
                        dcc.Dropdown(id="scatter_segments", # dropdown for 
                            options = segments,
                            multi = False,
                            value = segments[0],
                            clearable = False),

                ],width = 3),
                dbc.Col([
                        dbc.Checklist(options =  #Toggle option for tolerance
                        [{"label": "Show Tolerance options", "value": 1}],
                        value=[1],
                        id="tolerance_toggle_scatter",
                        switch=True)
                ], width={"size": 3, "offset": 1}, align = "center")

            ],className="g-0"),
            dbc.Row([
                dbc.Col(["x-axis"], width = 1,align = "center"),
                dbc.Col([
                        dcc.Dropdown(id="x-axis", # dropdown for 
                            options = ["DL","DLB","ATLAS"],
                            multi = False,
                            value = "DL",
                            clearable = False)],width = 2),
                dbc.Col(["y-axis"], width = 1,align = "center"),
                dbc.Col([
                        dcc.Dropdown(id="y-axis", # dropdown for 
                            options = ["DL","DLB","ATLAS"],
                            multi = False,
                            value = "DLB",
                            clearable = False)],width = 2),

            ]),
            html.Br(),
            dcc.Graph(id = "figure_scatter", figure = {},style = {"height": 700})
            
###
]) # End of layout


#Update graph for median performance
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
    # When turned on return all segments and value is the current
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
    [Output(component_id="violin_comp", component_property="value")],
    [Input(component_id="violin_comp", component_property="value")])
def update_dropdown_options_comp(values):
    if len(values) == 0:
        return[[tolerances[0]]]
    else:
        return [values]

# make comparisons for boxplots non clearable
@callback(
    [Output(component_id="boxplot_comp", component_property="value")],
    [Input(component_id="boxplot_comp", component_property="value")])
def update_dropdown_options_comp(values):
    if len(values) == 0:
        return[[tolerances[0]]]
    else:
        return [values]


# Load the correct csv file and make it downloadable:

result_file = pd.read_csv("..\\data\\results\\performance_median.csv", index_col=0)

@callback(
    Output("download", "data"),
    Input("btn", "n_clicks"),
    prevent_initial_call =True,
)

def generate_csv(n_clicks):
    return dcc.send_data_frame(result_file.to_csv, "results.csv")

# Still under construction (scatter plot)

###
@callback(
    [Output(component_id="figure_scatter", component_property="figure")],
    [Input(component_id="scatter_segments", component_property="value"),
    Input(component_id="y-axis", component_property="value"),
    Input(component_id="x-axis", component_property="value")])

def update_scatter(segments,yaxis,xaxis):
    n_points = {"DICE":[],"EPL":[],"MSD":[],"LineRatio":[],"VolumeRatio": [],"Hausdorff": []}
    legend_plottet = {"red": False, "darkcyan": False, "black": False}
    df = df_scatter[df_scatter["Segment"].isin([segments])]
    rows = 2
    cols = 3
    title = {"DL": "Deep Learning", 
            "DLB": "Deep Learning Bounded", 
            "ATLAS": "ATLAS"}

    fig = make_subplots(rows,cols,
                        x_title=title.get(xaxis),
                        y_title=title.get(yaxis),
                        subplot_titles = metrics)
    
    legend_text = {"darkcyan": f"{xaxis} outperforms {yaxis}",
                    "black": "Equal performance", 
                    "red": f"{yaxis} outperforms {xaxis}"}
    
    i = 0
    for row in range(1,rows+1):
        for col in range(1,cols+1):
            df_metric = df[df["Metric"] == metrics[i]]
            x_temp = df_metric[f"GTvs{xaxis}"]
            y_temp = df_metric[f"GTvs{yaxis}"]
            x_min = np.nanmin(x_temp)*0.7
            x_max = np.nanmax(x_temp)*1.05
            y_min = np.nanmin(y_temp)*0.7
            y_max = np.nanmax(y_temp)*1.05
            # if metrics[i] in ["DICE","LineRatio","VolumeRatio"]:
            #     max_range = x_max if x_max > y_max else y_max
            #     min_range = x_min if x_min < y_min else y_min
            # else:
            max_range = x_max if x_max > y_max else y_max
            min = x_min if x_min < y_min else y_min
            min_range = min-0.1*max_range
            x_line = np.linspace(min_range,max_range,100)
            fig.update_xaxes(range=[min_range,max_range], col = col, row = row)
            fig.update_yaxes(range=[min_range,max_range], col = col, row = row)
            if i == 0:
                fig.add_trace(
                                    go.Scatter(
                                        x = x_line, 
                                        y = x_line, 
                                        mode = "lines",
                                        name = "Identity line",
                                        opacity  = 0.5,
                                        legendgroup = "group1",
                                        line = dict(color = "black")),
                                        row = row, col = col)
            else:
                fig.add_trace(
                                    go.Scatter(
                                        x = x_line, 
                                        y = x_line, 
                                        mode = "lines",
                                        name = "Identity line",
                                        opacity  = 0.5,
                                        showlegend = False,
                                        legendgroup = "group1",
                                        line = dict(color = "black")),
                                        row = row, col = col)

            for color in ["darkcyan","black","red"]:
                if metrics[i] == "DICE":
                    df_col = df_metric[df_metric[f"Color_Dice_{xaxis}{yaxis}"]==color]
                    colors = [x for x,comp1,comp2 in 
                    zip(df_col[f"Color_Dice_{xaxis}{yaxis}"],
                        df_col["GTvs" + xaxis],
                        df_col["GTvs" + yaxis]) 
                        if not isnan(comp1) and not isnan(comp2)]
                    n_color = len(colors)
                else:
                    df_col = df_metric[df_metric[f"Color_{xaxis}{yaxis}"]==color]
                    colors = [x for x,comp1,comp2 in 
                    zip(df_col[f"Color_{xaxis}{yaxis}"],
                        df_col["GTvs" + xaxis],
                        df_col["GTvs" + yaxis]) 
                        if not isnan(comp1) and not isnan(comp2)]
                    n_color = len(colors)
                    
                n_points[metrics[i]].append(n_color)
                
                x = df_col["GTvs" + xaxis]
                y = df_col["GTvs" + yaxis]
                if not legend_plottet.get(color) and n_color != 0:
                    fig.add_trace(
                            go.Scatter(
                                x = x,
                                y = y,
                                mode = "markers",
                                name = legend_text.get(color),
                                legendgroup = color,
                                marker = dict(color = 
                                colors)),
                                row = row, col = col)
                    legend_plottet[color] = True
                                
                else:
                    fig.add_trace(
                            go.Scatter(
                                x = x,
                                y = y,
                                mode = "markers",
                                name = legend_text.get(color),
                                showlegend = False,
                                legendgroup = color,
                                marker = dict(color = 
                                colors)),
                                row = row, col = col)
            
            i+=1
        
    fig.update_layout(template=plot_theme,
                        legend=dict(
                        orientation="h",
                        y=1.15  
                        ))

    fig.for_each_annotation(lambda a: a.update(text = a.text + '<br>' +
                            f"{xaxis} best: " + str(n_points.get(a.text)[0]) + 
                            "   Equal: " + str(n_points.get(a.text)[1]) + 
                            f"   {yaxis} best: " + str(n_points.get(a.text)[2])) 
                            if a.text not in 
                            title.values()
                            else None)

    return [fig]

# Swap x and y axis if x == y
@callback(
    [Output("x-axis", "value"),
    Output("y-axis", "value")],
    [Input("x-axis", "value"),
    Input("y-axis", "value")])

def swap_xaxis_yaxis(x,y):
    global old_x_axis
    global old_y_axis 
    if x == y and old_x_axis != x:
        value_y = old_x_axis
        value_x = x
    elif x == y and old_y_axis != y:
        value_y = y
        value_x = old_y_axis
    else:
        value_y = y
        value_x = x
    
    old_x_axis = value_x
    old_y_axis = value_y

    return [value_x,value_y]



# Tolerance Toggle Scatter plots
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
    

    return [options,value]

### Make violin plots
@callback(
    [Output(component_id="figure_violin", component_property="figure")],
    [Input(component_id="violin_comp", component_property="value"),
    Input(component_id="violin_segment", component_property="value")])

def update_violin(tols,segment):
    
    metrics = ["DICE","LineRatio","VolumeRatio","EPL","MSD","Hausdorff"]
    rows = 2
    cols = 3

    fig = make_subplots(rows,cols,
                        x_title="Comparison",
                        y_title="Value",
                        subplot_titles = metrics)

    i = 0
    # color_dict = {"GTvsDL": "cornflowerblue", "GTvsDLB": "orange", "GTvsATLAS" : "lightgreen"}
    color_dict= {0 : "cornflowerblue", 1 : "orange", 2 : "lightgreen"}
    legend_show = [True]+[False]*5

    for row in range(1,rows+1):
        for col in range(1,cols+1):
            df = df_violin.drop(df_violin[(df_violin['Tolerance'].isin([1,2])) & (df_violin['Metric'].isin(['DICE', 'Hausdorff', 'MSD']))].index) #Hotfix to remove DICE,haus, MSD for tol 1,2
            df = df[df["Metric"]==metrics[i]]
            for tol in tols:
                df_tol = df[df["Tolerance"]==tol]
                x = df_tol["Comparison"].squeeze()
                y = df_tol[segment].squeeze()
                if i == 1: # 0 has DICE metric, which do NOT have tol but i = 1 (Line_Ratio) has. 
                    fig.add_trace(go.Violin(x = x,
                                y = y,line_color = color_dict.get(tol),
                                name = f"Tolerance {tol}", hoverinfo = 'none'),row = row, col = col)
                else:
                    fig.add_trace(go.Violin(x = x,
                                y = y,line_color = color_dict.get(tol),
                                showlegend = False,hoverinfo = 'none'),row = row, col = col)

            i+=1

    fig.update_layout(violinmode='overlay',
    template=plot_theme,
    legend=dict(
                        orientation="h",
                        y=1.1  
                        ))


        
    return [fig]


# Make boxplots:
@callback(
    [Output(component_id="figure_boxplot", component_property="figure")],
    [Input(component_id="boxplot_comp", component_property="value"),
    Input(component_id="boxplot_segment", component_property="value")])

def update_boxplot(tols,segment):
    
    metrics = ["DICE","LineRatio","VolumeRatio","EPL","MSD","Hausdorff"]
    rows = 2
    cols = 3

    fig = make_subplots(rows,cols,
                        x_title="Comparison",
                        y_title="Value",
                        subplot_titles = metrics)

    i = 0
    # color_dict = {"GTvsDL": "cornflowerblue", "GTvsDLB": "orange", "GTvsATLAS" : "lightgreen"}
    color_dict = {0 : "cornflowerblue", 1 : "orange", 2 : "lightgreen"}

    for row in range(1,rows+1):
        for col in range(1,cols+1):
            df = df_boxplot.drop(df_boxplot[(df_boxplot['Tolerance'].isin([1,2])) & (df_boxplot['Metric'].isin(['DICE', 'Hausdorff', 'MSD']))].index)
            df = df[df["Metric"]==metrics[i]]
            for tol in tols:
                df_tol = df[df["Tolerance"]==tol]
                x = df_tol["Comparison"].squeeze()
                y = df_tol[segment].squeeze()
                if i == 1: # 0 has DICE metric, which do NOT have tol but i = 1 (Line_Ratio) has. 
                    fig.add_trace(go.Box(x = x,
                                y = y,line_color = color_dict.get(tol),
                                name = f"Tolerance {tol}", boxpoints = False),row = row, col = col)
                else:
                    fig.add_trace(go.Box(x = x,
                                y = y,line_color = color_dict.get(tol),
                                showlegend = False, boxpoints = False),row = row, col = col)

                                

            i+=1

    fig.update_layout(violinmode='overlay',
                        template=plot_theme,
                        legend=dict(orientation="h", y=1.1))


        
    return [fig]
