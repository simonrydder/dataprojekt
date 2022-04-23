import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from ast import literal_eval
from plotly.subplots import make_subplots
import dash_daq as daq

app = Dash(__name__)

# Read data and prep it

df = pd.read_csv("..\\data\\results\\merged.csv", index_col = 0)
metrics = sorted(df["Metric"].unique().tolist())
df = df.drop(["Date"], axis = 1).round(2)
df = df.groupby(["Comparison","Metric"]).mean().reset_index()
df = df.melt(id_vars=["Comparison", "Metric"], 
    var_name="Segment", 
    value_name="value") 

df_organs = pd.read_csv("data_organ_test.csv")
cols_to_change = ["xA","yA","xB","yB","VA","HA","VB","HB"]

for col in cols_to_change:
    df_organs[col] = df_organs[col].apply(literal_eval)

#options for dropdowns
segments = sorted(df["Segment"].unique().tolist())
comparisons = sorted(df["Comparison"].unique().tolist())
organs = sorted(df_organs["Segment"].unique().tolist())

patients_slider = ["4Prj3A5sMvSv1sK4u5ihkzlnU","PHbmDBLzKFUqHWIbGMTmUFSmO", 
                    "HNCDL_340","HNCDL_447","HNCDL_141"]

segments_slider = ["brainstem","spinalcord",
                    "lips", "esophagus", "pcm_low",
                    "pcm_mid", "pcm_up", "mandible"]


#defining Plot theme

plot_theme = "seaborn"

### creating layout

app.layout = html.Div([
    #Performance plot
    dcc.Tabs(id="tabs", value='tab-perf', children=[
        dcc.Tab(label='Performance overview', value='tab-perf'),
        dcc.Tab(label='View per slice', value='tab-slices'),
    ]),
    # initializing tabs content to contain all ID's used for connections, 
    # to avoid errors when loading the page. this Div's children will be 
    # dynamically changed in the connections section
    html.Div(id='tabs-content', children = [

        html.Div([
           dcc.Dropdown(id="slct_segment", # dropdown for metrics
                    options =segments,
                    multi = True,
                    value = [segments[0]],
                    style = {"width": 1200},
                    clearable = True),
            dcc.Dropdown(id="slct_metrics", # Dropdown for segments
                            options =metrics,
                            multi = True,
                            value = [metrics[0]],
                            style = {"width": 600, "display": "inline-block"},
                            clearable = True),
            dcc.Dropdown(id="slct_comp", #Dropdown for comparisons
                            options =comparisons,
                            multi = True,
                            value = [comparisons[0]],
                            style = {"width": 600,"display": "inline-block"},
                            clearable = True),
            html.Br(),
            dcc.Graph(id = "figure_perf", figure = {}), #Initializing figure
        ]),

        html.Div(id='slider-container', children=[
            daq.Slider(id = "slider", # Slider to switch slice (z)
                        min = 50, 
                    max = 100,
                    value = 87, 
                    step = 1, 
                    size = 900,
                    handleLabel={"label":"slice","showCurrentValue": True}),

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
                        clearable = False),
                        
            dcc.Dropdown(id = "method_slider", #Dropdown for Method
                        options = ["GTvsDL","GTvsDLB"],
                        multi = False,
                        value = "GTvsDL",
                        style = {"width": 450,
                        "display": "inline-block"},
                        clearable = False),
            dcc.Dropdown(id = "tolerance_slider", #Dropdown for Tolerance
                        options = ["0","1","2","3"],
                        multi = False,
                        value = "0",
                        style = {"width": 450,
                        "display": "inline-block"},
                        clearable = False),
        html.Div([
            html.Button("-", "minus",style ={'display': 'inline-block'}), # plus button
            html.Button("+", "plus",style ={'display': 'inline-block'})]), # minus button

        dcc.Graph(id = "figure_slider", figure = {}, #Initializing slider figure
                style={'width': 900, 
                'height': 600,'display': 'inline-block'}),

        dcc.Graph(id = "figure_slider_perf", figure = {}, #Initializing perf_slider figure
                style={'width': 600, 
                'height': 600,'display': 'inline-block'})])
    ]) # end of tabs content     
]) # end of app layout


### connections


@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))

def render_content(tab):
    if tab == 'tab-perf':
        return html.Div([
                    dcc.Dropdown(id="slct_segment", # dropdown for metrics
                                options =segments,
                                multi = True,
                                value = [segments[0]],
                                style = {"width": 1200},
                                clearable = True),
                    dcc.Dropdown(id="slct_metrics", # Dropdown for segments
                                    options =metrics,
                                    multi = True,
                                    value = [metrics[0]],
                                    style = {"width": 600, "display": "inline-block"},
                                    clearable = True),
                    dcc.Dropdown(id="slct_comp", #Dropdown for comparisons
                                    options =comparisons,
                                    multi = True,
                                    value = [comparisons[0]],
                                    style = {"width": 600,"display": "inline-block"},
                                    clearable = True),
                    html.Br(),
                    dcc.Graph(id = "figure_perf", figure = {}), #Initializing figure
                        ])
    elif tab == 'tab-slices':
        return html.Div(id='slider-container', children=[
                    daq.Slider(id = "slider", # Slider to switch slice (z)
                                min = 50, 
                            max = 100,
                            value = 87, 
                            step = 1, 
                            size = 900,
                            handleLabel={"label":"slice","showCurrentValue": True}),

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
                                clearable = False),
                    html.Br(),
                    dcc.Dropdown(id = "method_slider", #Dropdown for Method
                                options = ["GTvsDL","GTvsDLB"],
                                multi = False,
                                value = "GTvsDL",
                                style = {"width": 450,
                                "display": "inline-block"},
                                clearable = False),

                    dcc.Dropdown(id = "tolerance_slider", #Dropdown for Tolerance
                                options = ["0","1","2","3"],
                                multi = False,
                                value = "0",
                                style = {"width": 450,
                                "display": "inline-block"},
                                clearable = False),

                html.Div([
                    html.Button("-", "minus",style ={'display': 'inline-block'}), #plus button
                    html.Button("+", "plus",style ={'display': 'inline-block'})]), # minus button

                dcc.Graph(id = "figure_slider", figure = {}, #Initializing slider figure 
                        style={'width': 900, 
                        'height': 600,'display': 'inline-block'}),

                dcc.Graph(id = "figure_slider_perf", figure = {}, #Initializing slider_perf figure
                        style={'width': 600, 
                        'height': 600,'display': 'inline-block'})])
                    


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
        if plot not in ["EPL","Hausdorff","MSD"]:
            fig["layout"][axes[idx]].update(range = [0,1])

    #Changes width of bars
    for data in fig.data:
        data["width"] = 0.15

    return [fig]

# Make metrics dropdown non clearable
@app.callback(
    [Output(component_id="slct_metrics", component_property="value")],
    [Input(component_id="slct_metrics", component_property="value")])
def update_dropdown_options_metric(values):
    old_values = values
    if len(values) == 0:
        return [metrics[0]]
    else:
        return [values]

# Make segment dropdown non clearable
@app.callback(
    [Output(component_id="slct_segment", component_property="value")],
    [Input(component_id="slct_segment", component_property="value")])
def update_dropdown_options_segment(values):
    if len(values) == 0:
        return [[segments[0]]]
    else:
        return [values]

# Make comp dropdown non clearable
@app.callback(
    [Output(component_id="slct_comp", component_property="value")],
    [Input(component_id="slct_comp", component_property="value")])
def update_dropdown_options_comp(values):
    if len(values) == 0:
        return[[comparisons[0]]]
    else:
        return [values]
    
 
## Slider plot
#initializing global values for later calls
old_patient = 0
old_segment = 0
old_method = 0
old_tolerance = 0
df_slices = 0
#defining where output should go and where input is from
@app.callback(
    [Output(component_id="figure_slider", component_property="figure"),
     Output(component_id="figure_slider_perf", component_property="figure")],
    [Input(component_id="slider", component_property="value"),
    Input(component_id="patient", component_property="value"),
    Input(component_id="segment_slider", component_property="value"),
    Input(component_id="method_slider", component_property="value"),
    Input(component_id="tolerance_slider", component_property="value")])

#Function to update slider plot
def update_slider(slider, patient,segment,method,tolerance):
    global old_segment
    global old_method
    global old_tolerance
    global df_slices
    #Finding the matching data
    if any([segment != old_segment,
    method != old_method,tolerance != old_tolerance]): # loading data if new file is needed

        file = method + "&" + segment + "&Tolerance" + tolerance
        df_slices = pd.read_csv(f"..\\data\\sliceresults\\dataframes2\\{file}.csv")
        df_slices = df_slices.drop(df_slices[df_slices["DICE"] > 10].index)

        cols_to_change = ["PointsA","PointsB","Vlines","Hlines"]

        for col in cols_to_change:
            df_slices[col] = df_slices[col].replace(["set()"],["[]"])
            df_slices[col] = df_slices[col].apply(literal_eval)

    metrics = ["EPL","EPL_Line","EPL_Volume","DICE","Haus","MSD"]
    df_slice = df_slices[df_slices["ID"]==patient]
    range_max = {metric: df_slice[metric].max()*1.1
                if metric not in ["DICE"] 
                else 1 for metric in metrics}
    df_slice = df_slice[df_slice["Index"]==slider]
    df_perf = df_slice[df_slice["Index"]==slider].round(3)

    # changing global variables
    old_segment = segment
    old_method = method
    old_tolerance = tolerance

    # Checking if their is points to plot for the slice
    try:
        xA,yA = zip(*df_slice["PointsA"].tolist()[0])
    except ValueError:
        xA,yA = ([],[])
    try:
        xB,yB = zip(*df_slice["PointsB"].tolist()[0])
    except ValueError:
        xB,yB = ([],[])

    # vertical and horizontal lines to plot
    Vlines = df_slice["Vlines"].tolist()[0]
    Hlines = df_slice["Hlines"].tolist()[0]


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


    #Plotting the boundary
    for (x0,y0),(x1,y1) in Vlines:
                x = [x0,x1]
                y = [y0,y1]
                fig3.add_trace(
                    go.Scatter(x = x, 
                                y = y, 
                                mode = "lines",
                                line = dict(dash = "dot"),
                                showlegend = False, marker = dict(color = "red")))

    for (x0,y0),(x1,y1) in Hlines:
                x = [x0,x1]
                y = [y0,y1]
                fig3.add_trace(
                    go.Scatter(x = x, 
                                y = y, 
                                mode = "lines",
                                line = dict(dash = "dot"),
                                showlegend = False, marker = dict(color = "red")))
    
                    
    fig3.update_layout(template=plot_theme) #set theme

    fig3.update_yaxes(scaleanchor = "x", scaleratio = 1) #scales yaxes to xaxes

    fig4 = make_subplots(6,1)  #creates subplots
    
    color = "blue"
    axes = ["xaxis","xaxis2","xaxis3","xaxis4","xaxis5","xaxis6"]
    #plotting for each metric
    for idx, metric in enumerate(metrics):
        value = df_perf[metric].iloc[0]
        
        #adding trace to subplot
        fig4.add_trace(
            go.Bar(x = [value], 
            y = [metric], 
            orientation = "h", 
            showlegend = False,
            text = value,
            marker=dict(color = color)),
            idx+1,1)
        range_upper = range_max.get(metric)
        fig4["layout"][axes[idx]].update(range = [0,range_upper])

    fig4.update_xaxes(matches=None) #Creates individual xaxis for subplots
    fig4.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True, 
                                                    visible = False)) # shows labels for all xaxis
    fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # changes subplot title

    return [fig3,fig4]

# # Changing Options for dropdown when changing patient
# @app.callback(
#     [Output(component_id="patient", component_property="options"),
#     Output(component_id="patient", component_property="value")],
#     [Input(component_id="segment_slider", component_property="value"),
#     Input(component_id="patient", component_property="value")])

# def change_options(segment,current_patient):
#     options = sorted(df_slices["ID"].unique().tolist())
#     if current_patient in options:
#         value = current_patient
#     else:
#          value = options[0]
#     return [options,current_patient]

# initializing global values for later usage
old_slice = 0
old_plus_clicks = None
old_minus_clicks = None

@app.callback(
    [Output(component_id="slider", component_property="max"),
    Output(component_id="slider", component_property="min")],
    [Input(component_id="patient", component_property="value"),
    Input(component_id="segment_slider", component_property="value"),
    Input(component_id="method_slider", component_property="value"),
    Input(component_id="tolerance_slider", component_property="value"),
    Input(component_id="slider", component_property="value")])

def change_slider_range(patient,segment,method,tolerance,slice):
    global old_slice
    file = method + "&" + segment + "&Tolerance" + tolerance
    df_slices = pd.read_csv(f"..\\data\\sliceresults\\dataframes2\\{file}.csv")
    df_slices = df_slices[df_slices["ID"]==patient] 
    df_slices = df_slices.drop(df_slices[df_slices["DICE"] > 10].index)
    old_slice = slice

    return [df_slices["Index"].max(),df_slices["Index"].min()]

#Change slider value dynamically when chancing tolerance,method,segment and patient
@app.callback(
    [Output(component_id="slider", component_property="value")],
    [Input(component_id="patient", component_property="value"),
    Input(component_id="segment_slider", component_property="value"),
    Input(component_id="method_slider", component_property="value"),
    Input(component_id="tolerance_slider", component_property="value"),
    Input('plus', 'n_clicks'),
    Input('minus', 'n_clicks')])

def change_slider_value(patient,segment,method,tolerance,plus,minus):
    global old_slice 
    global old_plus_clicks
    global old_minus_clicks
    file = method + "&" + segment + "&Tolerance" + tolerance
    df_slices = pd.read_csv(f"..\\data\\sliceresults\\dataframes2\\{file}.csv")
    df_slices = df_slices[df_slices["ID"]==patient] 
    df_slices = df_slices.drop(df_slices[df_slices["DICE"] > 10].index)

    if df_slices["Index"].min() <= old_slice <= df_slices["Index"].max():
        new_slice = old_slice
    else:
        new_slice = df_slices["Index"].min()
    old_slice = new_slice

    # applying plus button
    if plus != old_plus_clicks and  new_slice < df_slices["Index"].max():
        new_slice += 1
    
    # applying minus button
    if minus != old_minus_clicks and df_slices["Index"].min() < new_slice:
        new_slice -= 1
        
    old_plus_clicks = plus
    old_minus_clicks = minus
    
    return [new_slice]


# Run the app:
if __name__ == "__main__":
    app.run_server(debug=True)





