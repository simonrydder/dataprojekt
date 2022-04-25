from dash import dcc, html, Input, Output, callback
from dataloading import segments, metrics, comparisons, plot_theme, df
import plotly.express as px

Style = {'textAlign': 'center'}
layout = html.Div([
    html.H3('Performance', style = Style),
    html.Br(),
    #html.Div([
           dcc.Dropdown(id="slct_segment", # dropdown for metrics
                            options =segments,
                            multi = True,
                            value = [segments[0]],
                            style = {"width": 1000},
                            clearable = True),
            dcc.Dropdown(id="slct_metrics", # Dropdown for segments
                            options =metrics,
                            multi = True,
                            value = [metrics[0]],
                            style = {"width": 500, "display": "inline-block"},
                            clearable = True),
            dcc.Dropdown(id="slct_comp", #Dropdown for comparisons
                            options =comparisons,
                            multi = True,
                            value = [comparisons[0]],
                            style = {"width": 500,"display": "inline-block"},
                            clearable = True),
            html.Br(),
            dcc.Graph(id = "figure_perf", figure = {}), #Initializing figure
        #])
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




# Make segment dropdown non clearable
@callback(
    [Output(component_id="slct_segment", component_property="value")],
    [Input(component_id="slct_segment", component_property="value")])
def update_dropdown_options_segment(values):
    if len(values) == 0:
        return [[segments[0]]]
    else:
        return [values]

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
    