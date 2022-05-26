from dash import dcc, html, Input, Output, callback, callback_context as ctx
import dataloading as dl
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots


def layout(cont_style,header_style):
    title = 'Performance Overview'

    layout_ = html.Div(
        [
            html.Br(),
            html.H1(title, style = header_style),
            html.Br(),
            *bar_layout(
                dl.dd_bar_segments,
                dl.dd_bar_metrics,
                dl.dd_bar_comparisons
            ),
            html.Br(),
            dbc.Button("Download CSV", id="btn"),
            dcc.Download(id="download"),
            html.Br(),
            html.Br(),
            *boxplot_layout(dl.dd_box_segments, dl.dd_box_tolerances),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label='Violinplots', 
                        children=[
                            dcc.Graph(
                                id = "figure_violin", 
                                figure = {},
                                style = {"height": 700},
                                config= dl.optionbar
                            )
                        ]
                    ),
                    dcc.Tab(
                        label='Boxplots', 
                        children=[
                            dcc.Graph(
                                id = "figure_boxplot", 
                                figure = {},
                                style = {"height": 700},
                                config= dl.optionbar
                            )
                        ]
                    )
                ],
            ),        
            html.Br(),      
            *layout_scatter(dl.dd_scatter_segments, dl.dd_scatter_methods)

        ],
        cont_style
    )
    return layout_

def bar_layout(segments, metrics, comparisons):
    with open('Info/bar_text.txt') as f:
            text = dcc.Markdown(f.read(), mathjax= True)
    bar_content = [
        html.Br(),
        html.H3('Barplot of median performance'),
        html.Br(),
        text,
        html.Br(),
        dbc.Row([
                    dbc.Col(
                        ["Segments"],
                        width = 1, 
                        align = "center"),
                    dbc.Col([
                        dcc.Dropdown(id="slct_segment", # dropdown for segment for mean performance
                            options =segments,
                            multi = True,
                            value = [segments[0]],
                            clearable = True)

                    ], 
                    width = 8
                    ),
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
                dcc.Graph(id = "figure_perf", figure = {}, 
                config= dl.optionbar), #Initializing mean performance figure
        ]

    return bar_content
               
def violin_layout(segments,tolerances):
    with open('Info/violin_text.txt') as f:
        text = dcc.Markdown(f.read(), mathjax= True)
    violin_content = [
        html.Br(),
        html.H3('Violinplots'),
        html.Br(),
        text,
        html.Br(),
        dbc.Row(
        [
            dbc.Col(
                ["Segment"], 
            width = 1),
            dbc.Col([ 
                dcc.Dropdown(
                    id="violin_segment", # dropdown for metrics for violin plot
                    options =segments, 
                    multi = False,
                    value = segments[0],
                    clearable = False
                )
            ], 
                width = 4)
        ]
        ),
        dbc.Row([
            dbc.Col(
                ["Tolerance"], 
            width = 1),
            dbc.Col([
                dcc.Dropdown(
                    id="violin_comp", # dropdown for comparisons for violin plot
                    options = tolerances,
                    multi = True,
                    value = [tolerances[0]],
                    clearable = True)
            ],  
            width = 4)
        ]
        ),
        html.Br(),
        dcc.Graph(id = "figure_violin", figure = {},style = {"height": 700},
        config= dl.optionbar),
        html.Br()
    ]
   
    return violin_content

def boxplot_layout(segments,tolerances):
    with open('Info/boxplot_text.txt') as f:
        text = dcc.Markdown(f.read(), mathjax= True)
    boxplot_content = [
        html.Br(),
        html.H3('Violinplots & Boxplots'),
        html.Br(),
        text,
        html.Br(),
        dbc.Row([
            dbc.Col(
                ["Segment"], 
            width = 1),
            dbc.Col([ 
                dcc.Dropdown(
                    id="boxplot_segment", # dropdown for metrics for violin plot
                    options =segments, 
                    multi = False,
                    value = segments[0],
                    clearable = False)
            ], 
            width = 4
            )
        ]
        ),
        dbc.Row([
            dbc.Col(
                ["Tolerance"], 
            width = 1
            ),
            dbc.Col([
                dcc.Dropdown(
                    id="boxplot_comp", # dropdown for comparisons for violin plot
                    options = tolerances,
                    multi = True,
                    value = [tolerances[0]],
                    clearable = True)
            ], 
            width = 4
            )
        ]
        ),
        html.Br(),
    ]
    return boxplot_content

def layout_scatter(segments,methods):
    with open('Info/scatter_text.txt') as f:
        text = dcc.Markdown(f.read(), mathjax= True)
    scatter_content = [
        html.Br(),
        html.H3('Scatterplots'),
        html.Br(),
        text,
        html.Br(),
        dbc.Row([
            dbc.Col(
                ["Segment"], 
                width = 1,
                align =
                "center"),
            dbc.Col([
                dcc.Dropdown(id="scatter_segments", # dropdown for 
                    options = segments,
                    multi = False,
                    value = segments[0],
                    clearable = False),
                ],
                width = 3),
            dbc.Col([
                dbc.Checklist(
                    options = [{"label": "Show Tolerance options", "value": 1}],
                    value=[1],
                    id="tolerance_toggle_scatter",
                    switch=True)
                ], 
                width={"size": 3, "offset": 1}, 
                align = "center")
        ],
        className="g-0"),
        dbc.Row([
            dbc.Col(
                ["x-axis"], 
                width = 1,
                align = "center"),
            dbc.Col([
                dcc.Dropdown(id="x-axis", # dropdown for 
                    options = methods,
                    multi = False,
                    value = methods[1],
                    clearable = False)
                ],
                width = 2
            ),
            dbc.Col(
                ["y-axis"], 
                width = 1,
                align = "center"
            ),
            dbc.Col([
                dcc.Dropdown(id="y-axis", # dropdown for 
                    options = methods,
                    multi = False,
                    value = methods[2],
                    clearable = False)
                ],
            width = 2),

        ]
        ),
        html.Br(),
        dcc.Graph(
            id = "figure_scatter", 
            figure = {},
            style = {"height": 700},
            config= dl.optionbar
        )
    ]
    return scatter_content


#Update graph for median performance
@callback(
  [Output(component_id="figure_perf", component_property="figure")],
    [Input(component_id="slct_metrics", component_property="value"),
    Input(component_id="slct_segment", component_property="value"),
    Input(component_id="slct_comp", component_property="value")])

# Function to update performance plot
def update_graph(slct_metrics, slct_segment,slct_comp):


    # Filtering Data
    df_perf = dl.df_median
    df_perf = df_perf[df_perf["Metric"].isin(slct_metrics)]
    df_perf = df_perf[df_perf["Segment"].isin(slct_segment)]
    df_perf = df_perf[df_perf["Comparison"].isin(slct_comp)]

    try: 
        fig = px.bar(df_perf, #Creates barplot
                    x = "Comparison", 
                    y = "value", 
                    color = "Segment", 
                    barmode = "group",
                    facet_col = "Metric",
                    template = dl.plot_theme,
                    facet_col_spacing=0.04,
                    title = "Median performance"
                )
    except UnboundLocalError:
        fig = px.bar(x = ["GTvsATLAS"]*len(slct_metrics), 
                    y = [0]*len(slct_metrics), 
                    facet_col = slct_metrics,
                    facet_col_spacing=0.04,
                    template = dl.plot_theme,
                    title = "Median performance")

    
    fig.update_yaxes(matches=None) #Creates individual yaxis for subplots
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True)) # shows labels for all yaxis
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1] +
                                        f"({dl.units.get(a.text.split('=')[-1])})"
                                        )) # changes subplot title
    fig.update_xaxes(title = "Comparison")
    fig.update_yaxes(title = "Value", row = 1, col = 1)



    #Changes range of yaxis to [0,1] for "DICE", "LineRatio", "VolumeRatio"
    plots = []
    axes = ["yaxis","yaxis2","yaxis3","yaxis4","yaxis5","yaxis6"]
    fig.for_each_annotation(lambda trace: plots.append(trace.text))
    
    for idx,plot in enumerate(plots):
        if plot not in ["EPL(mm)","Hausdorff(mm)","MSD(mm)"]:
            fig["layout"][axes[idx]].update(range = [0,1])


    return [fig]


# Make metrics dropdown non clearable
@callback(
    [Output(component_id="slct_metrics", component_property="value")],
    [Input(component_id="slct_metrics", component_property="value")])
def update_dropdown_options_metric(values):
    if len(values) == 0:
        return [[dl.dd_bar_metrics[0]]]
    else:
        return [values]

# Make comp dropdown non clearable
@callback(
    [Output(component_id="slct_comp", component_property="value")],
    [Input(component_id="slct_comp", component_property="value")])
def update_dropdown_options_comp(values):
    if len(values) == 0:
        return[[dl.dd_bar_comparisons[0]]]
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
        options = dl.dd_bar_segments
        values = current
    else: # When turned off, return only Tolerance 0
        options = dl.dd_bar_segments_notol
        values = [segment for segment in current if segment in options]
    
    # if No 0 Tolerance was in the values set the value equal to the first segment
    if len(values) == 0:
        values = [dl.dd_bar_segments[0]]

    return [options,values]


# make comparisons for violin plots non clearable
# @callback(
#     [Output(component_id="violin_comp", component_property="value")],
#     [Input(component_id="violin_comp", component_property="value")])
# def update_dropdown_options_comp(values):
#     if len(values) == 0:
#         return[[dl.dd_box_tolerances[0]]]
#     else:
#         return [values]

# make comparisons for boxplots non clearable
@callback(
    [Output(component_id="boxplot_comp", component_property="value")],
    [Input(component_id="boxplot_comp", component_property="value")])
def update_dropdown_options_comp(values):
    if len(values) == 0:
        return[[dl.dd_box_tolerances[0]]]
    else:
        return [values]


# Load the correct csv file and make it downloadable:

result_file = dl.df_median

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
    df = dl.df_scatter[dl.df_scatter["Segment"].isin([segments])]
    rows = 2
    cols = 3
    title = {"DL": "Deep Learning", 
            "DLB": "Deep Learning Bounded", 
            "ATLAS": "ATLAS",
            "title": f"Compared performance for {segments} between {yaxis} and {xaxis}"}

    fig = make_subplots(rows,cols,
                        x_title=title.get(xaxis),
                        y_title=title.get(yaxis),
                        subplot_titles = dl.dd_scatter_metrics,
                        vertical_spacing = 0.15,
                        horizontal_spacing = 0.15)
    
    legend_text = {"darkcyan": f"{xaxis} outperforms {yaxis}",
                    "black": "Equal performance", 
                    "red": f"{yaxis} outperforms {xaxis}"}
    
    i = 0
    for row in range(1,rows+1):
        for col in range(1,cols+1):
            df_metric = df[df["Metric"] == dl.dd_scatter_metrics[i]]
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
                if dl.dd_scatter_metrics[i] == "DICE":
                    df_col = df_metric[df_metric[f"Color_Dice_{xaxis}{yaxis}"]==color]
                    colors = [x for x,comp1,comp2 in 
                    zip(df_col[f"Color_Dice_{xaxis}{yaxis}"],
                        df_col["GTvs" + xaxis],
                        df_col["GTvs" + yaxis]) 
                        if not np.isnan(comp1) and not np.isnan(comp2)]
                    n_color = len(colors)
                else:
                    df_col = df_metric[df_metric[f"Color_{xaxis}{yaxis}"]==color]
                    colors = [x for x,comp1,comp2 in 
                    zip(df_col[f"Color_{xaxis}{yaxis}"],
                        df_col["GTvs" + xaxis],
                        df_col["GTvs" + yaxis]) 
                        if not np.isnan(comp1) and not np.isnan(comp2)]
                    n_color = len(colors)
                    
                n_points[dl.dd_scatter_metrics[i]].append(n_color)
                
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
        
    fig.update_layout(template=dl.plot_theme,
                        legend=dict(
                        orientation="h",
                        y=1.13),
                        title={
                            'text': title.get("title"),
                            'y':0.99,
                            'x':0.1,
                            'xanchor': 'left',
                            'yanchor': 'top'}  
                            )

    fig.for_each_annotation(lambda a: a.update(text = a.text + f"({dl.units.get(a.text)})" + '<br>' +
                            f"{xaxis} best: " + str(n_points.get(a.text)[0]) + 
                            "   Equal: " + str(n_points.get(a.text)[1]) + 
                            f"   {yaxis} best: " + str(n_points.get(a.text)[2]),
                            font=dict(size=14)) 
                            if a.text not in 
                            title.values()
                            else None)

    return [fig]



# Tolerance Toggle Scatter plots
@callback(
    [Output("scatter_segments", "options"),
    Output("scatter_segments", "value")],
    [Input("tolerance_toggle_scatter", "value"),
    Input("scatter_segments", "value")])

def toggle_tolerance_Scatter(toggle,current):
    # When turned on return the all segments and value is the current
    if len(toggle) == 1:
        options = dl.dd_scatter_segments
        value = current
    else: # When turned off, return only Tolerance 0
        options = dl.dd_scatter_segments_notol
        if current in options:
            value = current
        else:
            value = options[0]
    

    return [options,value]


@callback(
    [Output("x-axis", "options"),
    Output("y-axis", "options")],
    [Input("x-axis", "value"),
    Input("y-axis", "value")])

def fix_axes(x,y):
    options = ["DL","DLB","ATLAS"]
    x_options = [option for option in options if option != y]
    y_options = [option for option in options if option != x]

    return [x_options,y_options]

### Make violin plots
@callback(
    [Output(component_id="figure_violin", component_property="figure")],
    [Input(component_id="boxplot_comp", component_property="value"),
    Input(component_id="boxplot_segment", component_property="value")])

def update_violin(tols,segment):
    
    #metrics = ["DICE","LineRatio","VolumeRatio","EPL","MSD","Hausdorff"]
    rows = 2
    cols = 3
    subtitles = [f"{metric}({unit})" for metric, unit 
                    in zip(dl.dd_box_metrics, dl.units.values())]

    fig = make_subplots(rows,cols,
                        x_title="Comparison",
                        y_title="Value",
                        subplot_titles = subtitles)

    i = 0
    # color_dict = {"GTvsDL": "cornflowerblue", "GTvsDLB": "orange", "GTvsATLAS" : "lightgreen"}
    color_dict= {0 : "cornflowerblue", 1 : "orange", 2 : "lightgreen"}

    for row in range(1,rows+1):
        for col in range(1,cols+1):
            df = dl.df_violin.drop(dl.df_violin[(dl.df_violin['Tolerance'].isin([1,2])) & (dl.df_violin['Metric'].isin(['DICE', 'Hausdorff', 'MSD']))].index) #Hotfix to remove DICE,haus, MSD for tol 1,2
            df = df[df["Metric"]==dl.dd_box_metrics[i]]
            for tol in tols:
                df_tol = df[df["Tolerance"]==tol]
                x = df_tol["Comparison"].squeeze()
                y = df_tol[segment].squeeze()
                if i == 3: # 0 has DICE metric, which do NOT have tol but i = 3 (Hausdorff) has. 
                    fig.add_trace(go.Violin(x = x,
                                y = y,line_color = color_dict.get(tol),
                                name = f"Tolerance {tol}",hoverinfo = 'none',  legendgroup = tol),row = row, col = col)
                else:
                    fig.add_trace(go.Violin(x = x,
                                y = y,line_color = color_dict.get(tol),
                                showlegend = False, hoverinfo = 'none', legendgroup = tol),row = row, col = col)

            i+=1

    fig.update_layout(violinmode='overlay',
                    template=dl.plot_theme,
                    legend=dict(
                        orientation="h",
                        y=1.1  
                        ), 
                        title={
                            'text': f"Violinplot of performance for {segment}",
                            'y':0.95,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'}
                        )


        
    return [fig]


# Make boxplots:
@callback(
    [Output(component_id="figure_boxplot", component_property="figure")],
    [Input(component_id="boxplot_comp", component_property="value"),
    Input(component_id="boxplot_segment", component_property="value")])

def update_boxplot(tols,segment):
    
    #metrics = ["DICE","LineRatio","VolumeRatio","EPL","MSD","Hausdorff"]
    rows = 2
    cols = 3
    subtitles = [f"{metric}({unit})" for metric, unit 
                    in zip(dl.dd_box_metrics, dl.units.values())]

    fig = make_subplots(rows,cols,
                        x_title="Comparison",
                        y_title="Value",
                        subplot_titles = subtitles)

    i = 0
    # color_dict = {"GTvsDL": "cornflowerblue", "GTvsDLB": "orange", "GTvsATLAS" : "lightgreen"}
    color_dict = {0 : "cornflowerblue", 1 : "orange", 2 : "lightgreen"}

    for row in range(1,rows+1):
        for col in range(1,cols+1):
            df = dl.df_violin.drop(dl.df_violin[(dl.df_violin['Tolerance'].isin([1,2])) & (dl.df_violin['Metric'].isin(['DICE', 'Hausdorff', 'MSD']))].index)
            df = df[df["Metric"]==dl.dd_box_metrics[i]]
            for tol in tols:
                df_tol = df[df["Tolerance"]==tol]
                x = df_tol["Comparison"].squeeze()
                y = df_tol[segment].squeeze()
                if i == 3: # 0 has DICE metric, which do NOT have tol but i = 3 (Hausdorff) has. 
                    fig.add_trace(go.Box(x = x,
                                y = y,line_color = color_dict.get(tol),
                                name = f"Tolerance {tol}", boxpoints = 'suspectedoutliers', 
                                legendgroup = tol),row = row, col = col)
                else:
                    fig.add_trace(go.Box(x = x,
                                y = y,line_color = color_dict.get(tol),
                                showlegend = False, boxpoints = 'suspectedoutliers',
                                legendgroup = tol),row = row, col = col)

                                

            i+=1

    fig.update_layout(violinmode='overlay',
                        template=dl.plot_theme,
                        legend=dict(orientation="h", y=1.1),
                        
                        title={
                            'text': f"Boxplot of performance for {segment}",
                            'y':0.95,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})


        
    return [fig]
