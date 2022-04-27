from dash import dcc, html, Input, Output, callback
from dataloading import patients_slider,segments_slider, plot_theme
import dash_daq as daq
import pandas as pd
from ast import literal_eval
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

Style = {'textAlign': 'center', "border-bottom":"2px black solid"}


layout = html.Div([
            html.H1("EPL visulization", style = Style),
            html.Br(),
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
                        "display": "inline-block", "cursor": "pointer"},
                        clearable = False),

            dcc.Dropdown(id = "segment_slider", #Dropdown for segments
                        options = segments_slider,
                        multi = False,
                        value = segments_slider[0],
                        style = {"width": 450,
                        "display": "inline-block","cursor": "pointer"},
                        clearable = False),
                        
            dcc.Dropdown(id = "method_slider", #Dropdown for Method
                        options = ["GTvsDL","GTvsDLB"],
                        multi = False,
                        value = "GTvsDL",
                        style = {"width": 450,
                        "display": "inline-block","cursor": "pointer"},
                        clearable = False),
            dcc.Dropdown(id = "tolerance_slider", #Dropdown for Tolerance
                        options = ["0","1","2","3",],
                        multi = False,
                        value = "0",
                        style = {"width": 450,
                        "display": "inline-block","cursor": "pointer"},
                        clearable = False),
            html.Br(),
       
            dbc.Button("-", "minus",style ={'display': 'inline-block'},
            outline=True, color="success"), # plus button
            dbc.Button("+", "plus",style ={'display': 'inline-block'},
            outline=True, color="success"), # minus button
            html.Br(),

            dcc.Graph(id = "figure_slider", figure = {}, #Initializing slider figure
                    style={'width': 700, 
                    'height': 600,'display': 'inline-block'}),

            dcc.Graph(id = "figure_slider_perf", figure = {}, #Initializing perf_slider figure
                    style={'width': 450, 
                    'height': 600,'display': 'inline-block'})
        
        ])   


#initiliazing global values for later usages

old_patient = 0
old_segment = 0
old_method = 0
old_tolerance = 0
df_slices = 0

#Connections


@callback(
    [Output(component_id="figure_slider", component_property="figure"),
     Output(component_id="figure_slider_perf", component_property="figure"),
     Output(component_id="slider", component_property="max"),
    Output(component_id="slider", component_property="min")],
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
    max = df_slice["Index"].max() #range for slider
    min = df_slice["Index"].min() #range for slider

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
        fig4["layout"][axes[idx]].update(range = [0,range_upper],matches=None,showticklabels=True, 
                                                    visible = False)
        print(fig4["annotation"][axes[idx]])

    fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # changes subplot title

    return [fig3,fig4,
    max,min]


old_slice = 0
old_plus_clicks = None
old_minus_clicks = None

#Change slider value dynamically when chancing tolerance,method,segment and patient
@callback(
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
    

    # applying plus button
    if plus != old_plus_clicks and  new_slice < df_slices["Index"].max():
        new_slice += 1
    
    # applying minus button
    if minus != old_minus_clicks and df_slices["Index"].min() < new_slice:
        new_slice -= 1
        
    old_plus_clicks = plus
    old_minus_clicks = minus
    old_slice = new_slice
    
    return [new_slice]
