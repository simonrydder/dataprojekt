from dash import dcc, html, Input, Output, callback
from dataloading import segments, metrics, comparisons, plot_theme, df, df_violin, boxplot_segments
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
Style = {'textAlign': 'center', "border-bottom":"2px black solid"}

layout = html.Div([
    html.H1('Performance', style = Style),
    html.Br(),
            dbc.Row([
                dbc.Col([
                        dcc.Dropdown(id="slct_segment", # dropdown for metrics
                        options =segments,
                        multi = True,
                        value = [segments[0]],
                        clearable = True)

                ], width = 9),
                dbc.Col([
                        dbc.Checklist(
                        options=[
                        {"label": "Show Tolerance options", "value": 1}],
                        value=[1],
                        id="tolerance_toggle",
                        switch=True)
                ],width = 3)
            ]),

            dbc.Row([
                dbc.Col([
                        dcc.Dropdown(id="slct_metrics", # Dropdown for segments
                        options =metrics,
                        multi = True,
                        value = [metrics[0]],
                        clearable = True)

                ],width = 6),
                dbc.Col([ dcc.Dropdown(id="slct_comp", #Dropdown for comparisons
                            options =comparisons,
                            multi = True,
                            value = [comparisons[0]],
                            clearable = True)

                ],width = 6)
            ],className="g-0"),
            html.Br(),
            dcc.Graph(id = "figure_perf", figure = {}), #Initializing figure,
            html.Br(),
            dcc.Dropdown(id="boxplot_segment", # dropdown for metrics
                            options =boxplot_segments,
                            multi = False,
                            value = [boxplot_segments[0]],
                            style = {"width": 500},
                            clearable = False),
            dcc.Dropdown(id="boxplot_comp", # dropdown for 
                            options = ["GTvsDL","GTvsDLB"],
                            multi = True,
                            value = ["GTvsDL"],
                            style = {"width": 500},
                            clearable = False),
            html.Br(),
             dbc.Row([
                dbc.Col([
                            dcc.Graph(id = "figure_DICE", figure = {}, style = {"height": 350})


                ],width = 4),
                dbc.Col([  dcc.Graph(id = "figure_Line", figure = {}, style = {"height": 350})

                ],width = 4),
                dbc.Col([ dcc.Graph(id = "figure_Volume", figure = {}, style = {"height": 350})

                ],width = 4)
            ],className="g-0"),

            dbc.Row([
                dbc.Col([
                            dcc.Graph(id = "figure_EPL", figure = {}, style = {"height": 350})


                ],width = 4),
                dbc.Col([  dcc.Graph(id = "figure_MSD", figure = {}, style = {"height": 350})

                ],width = 4),
                dbc.Col([ dcc.Graph(id = "figure_Haus", figure = {}, style = {"height": 350})

                ],width = 4)
            ],className="g-0")



            #Initializing figure,
])

#Update graph for performance
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
                template = plot_theme)

    fig.update_yaxes(matches=None) #Creates individual yaxis for subplots
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True)) # shows labels for all yaxis
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # changes subplot title


    #Changes range of yaxis to [0,1] for "DICE", "MSD", "APL_L", "APL_V"
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
    old_values = values
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


@callback(
    Output("slct_segment", "options"),
    Output("slct_segment", "value"),
    [Input("tolerance_toggle", "value"),
    Input("slct_segment", "value")])
def toggle_tolerance(toggle,current):
    if len(toggle) == 1:
        options = segments
        values = current
    else:
        options = [segment for segment in segments if not segment.endswith(("1","2","3","4"))]
        values = [segment for segment in current if segment in options]
    
    if len(values) == 0:
        values = [segments[0]]

    return [options,values]

    

@callback(
    [Output(component_id="figure_DICE", component_property="figure"),
    Output(component_id="figure_Line", component_property="figure"),
    Output(component_id="figure_Volume", component_property="figure"),
    Output(component_id="figure_EPL", component_property="figure"),
    Output(component_id="figure_MSD", component_property="figure"),
    Output(component_id="figure_Haus", component_property="figure")],
    [Input(component_id="boxplot_comp", component_property="value"),
    Input(component_id="boxplot_segment", component_property="value")])
def update_dropdown_options_metric(comps,segment):
    metrics = ["DICE","LineRatio","VolumeRatio","EPL","MSD","Hausdorff"]
    figs = []
    for metric in metrics:
        df = df_violin[df_violin["Metric"]==metric]
        #df = df[df["Comparison"].isin(comps)]
        fig = px.violin(df,
                        x = "Tolerance",
                        y = segment,
                        facet_col = "Metric",
                        color = "Comparison",
                        violinmode="overlay",
                         template = plot_theme)

        if metric == metrics[0]:
            fig.update_layout(legend=dict(
                        orientation="h",
                        y=1.25,
                        
                        ),margin=dict(l=0, r=10, b=0))
        else:
            fig.update_layout(showlegend = False,
             margin=dict(l=0, r=10, b=0)
            )

        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        figs.append(fig)

    return figs