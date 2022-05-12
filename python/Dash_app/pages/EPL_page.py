from dash import dcc, html, Input, Output, callback
from dataloading import patients_slider,segments_slider, plot_theme, df_slices
import dash_daq as daq
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

Style = {'textAlign': 'center', "border-bottom":"2px black solid"}

#Defining layout
layout = html.Div([
            html.H1("EPL Visualization", style = Style),
            html.Br(),
            dbc.Row([            
                dbc.Col([
                    daq.Slider(id = "slider", # Slider to switch slice (z)
                        min = 50, 
                        max = 100,
                        value = 87, 
                        step = 1, 
                        size = 500,
                        handleLabel={"label":"slice","showCurrentValue": True})
                ])
            ],className="g-0"),


            dbc.Row([

                dbc.Col([
                    dcc.Dropdown(id = "patient", # Dropdown for Patient for EPL plot
                        options = patients_slider, 
                        multi = False,
                        value = patients_slider[0],
                        style = {"cursor": "pointer"},
                        clearable = False)
                ],width = 3),

                dbc.Col([ 
                    dcc.Dropdown(id = "segment_slider", #Dropdown for segments for EPL plot
                        options = segments_slider,
                        multi = False,
                        value = segments_slider[0],
                        style = {"cursor": "pointer"},
                        clearable = False)
                ],width = 2),

                dbc.Col([
                    dbc.Button("+", "plus", # Plus button to go to next slice
                        color="info",
                        className="d-grid gap-2 col-6 mx-auto",
                        size = "sm")
                    ],width = 2, align = "Top")
            ],className="g-0"),

            dbc.Row([
                dbc.Col([            
                    dcc.Dropdown(id = "method_slider", #Dropdown for Method for EPL plot
                        options = ["GTvsDL","GTvsDLB"],
                        multi = False,
                        value = "GTvsDL",
                        style = {"cursor": "pointer"},
                        clearable = False)
                ],width = 3),

                
                dbc.Col([
                    dcc.Dropdown(id = "tolerance_slider", #Dropdown for Tolerance for EPL plot
                        options = ["0","1","2","3",],
                        multi = False,
                        value = "0",
                        style = {"cursor": "pointer"},
                        clearable = False)
                ],width = 2),

                dbc.Col([
                    dbc.Button("-", "minus",
                        color="info",
                        className="d-grid gap-2 col-6 mx-auto",
                        size = "sm")
                    ],width = 2, align = "Top")
                ],className="g-0"),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id = "figure_slider", figure = {}) #Initializing slider figure
                ],width = 7),
                dbc.Col([
                    dcc.Graph(id = "figure_slider_perf", figure = {}) #Initializing performance slider figure
                ],width = 5)
            ])
        ]) # End of the layout   


#initiliazing global values for later use

old_patient = 0
old_segment = 0
old_method = 0
old_tolerance = 0
old_slice = 0

#Connections

#Output and inputs to slider plot, component_id refers to components in the layout above
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

#Function to update slider plot and performance plot
def update_slider(slider,patient,segment,method,tolerance):
    global old_segment
    global old_method
    global old_tolerance
    global old_slice
    metrics = ["EPL","LineRatio","VolumeRatio","DICE","Haus","MSD"]
    
    #filtering data
    df_slice = df_slices[df_slices["ID"]==patient]
    df_slice = df_slice[df_slice["Segment"]==segment]
    df_slice = df_slice[df_slice["Comparison"]==method]
    df_slice = df_slice[df_slice["Tolerance"]==int(tolerance)]
    max = df_slice["Index"].max() #range for slider
    min = df_slice["Index"].min() #range for slider

    #Dict to lookup the length of bar plots in the performance plot
    range_max = {metric: df_slice[metric].max()*1.1
                if metric not in ["DICE", "LineRatio","VolumeRatio"] 
                else 1 for metric in metrics}
    df_slice = df_slice[df_slice["Index"]==slider] # Final df for slice plot
    df_perf = df_slice[df_slice["Index"]==slider].round(3) # Final df for performance plot

    # changing global variables
    old_segment = segment
    old_method = method
    old_tolerance = tolerance
    old_slice = slider

    pointsGT = df_slice["PointsGT"].tolist()[0]
    pointsGT = eval(pointsGT)

    # Checking if their is points to plot for the slice
    try:
        xA,yA = zip(*pointsGT)
    except ValueError:
        xA,yA = ([],[])


    #Prepping Model lines and EPL lines to plot

    lines_model = df_slice["LinesModel"].tolist()[0]
    lines_model = eval(lines_model)

    lines_changed = df_slice["LinesChanged"].tolist()[0]
    lines_changed = eval(lines_changed)

    # Slice plot

    fig3 = go.Figure() #Initializing figure 
    #Add GT points to the plot
    fig3.add_trace( 
            go.Scatter(x=xA,
                    y=yA,
                    mode = "markers", 
                    name = "GT",
                    marker=dict(color='black',size=8)
            )
    )

    #Plotting the Lines of the model
    for (x0,y0),(x1,y1) in lines_model:
                x = [x0,x1]
                y = [y0,y1]
                fig3.add_trace(
                    go.Scatter(x = x, 
                               y = y, 
                               mode = "lines",
                               line = dict(dash = "dot"),
                               showlegend = False, 
                               marker = dict(color = "orange")
                    )
                )

    #Plotting the EPL lines
    for (x0,y0),(x1,y1) in lines_changed:
                x = [x0,x1]
                y = [y0,y1]
                fig3.add_trace(
                    go.Scatter(x = x, 
                               y = y, 
                               mode = "lines",
                               line = dict(dash = "dot"),
                               showlegend = False, 
                               marker = dict(color = "darkcyan")
                    )
                )

    #Showing the correct legend
    if fig3["data"][1]['marker']["color"] == "orange":
        fig3['data'][1]['showlegend'] = True
        fig3['data'][1]['name'] = 'Guess'

    if fig3["data"][-1]['marker']["color"] == "darkcyan":
        fig3['data'][-1]['showlegend'] = True
        fig3['data'][-1]['name'] = 'EPL'

    #set theme and margin of the plot
    fig3.update_layout(template=plot_theme, 
                        margin = dict(l=10, r = 10, t = 10, b = 10)
    ) 

    fig3.update_yaxes(scaleanchor = "x", scaleratio = 1) #scale yaxes to xaxes

    # Performance plot

    fig4 = make_subplots(6,1)  #Initialzing subplots
    
    color = "Darkcyan"
    axes = ["xaxis","xaxis2","xaxis3","xaxis4","xaxis5","xaxis6"]
    #plotting for each metric
    for idx, metric in enumerate(metrics):
        value = df_perf[metric].iloc[0] #The value for for metric
        
        #adding bar plot at subplot idx+1,1
        fig4.add_trace(
                go.Bar(x = [value], 
                y = [metric], 
                orientation = "h", # Horizontal plot
                showlegend = False,
                text = value,
                marker=dict(color = color)
                ),
        idx+1,1)
        range_upper = range_max.get(metric) # getting the range of the plot 

        # Updating current subplot with correct range etc.
        fig4["layout"][axes[idx]].update(range = [0,range_upper],
                                         matches=None,
                                         showticklabels=True, 
                                         visible = False)

    fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # changes the subplot title
    fig4.update_layout(title = f"Performance for the slice")

    return [fig3,fig4,max,min]

# Global variables initialized 
old_slice = 0
old_plus_clicks = None
old_minus_clicks = None

#Change slider value dynamically when chancing tolerance,method,segment and patient

# Output and input is defined
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
    #Finding correct data
    df_patient = df_slices[df_slices["ID"]==patient] 
    df_patient = df_patient[df_patient["Segment"]==segment]
    df_patient = df_patient[df_patient["Comparison"]==method]
    df_patient = df_patient[df_patient["Tolerance"]==int(tolerance)]

    # Checking if the former slice index is in the range when changing patient, segment etc.
    if df_patient["Index"].min() <= old_slice <=  df_patient["Index"].max():
        new_slice = old_slice
    else:
        new_slice = df_patient["Index"].min()
    

    # applying plus button if still less than max index
    if plus != old_plus_clicks and  new_slice < df_patient["Index"].max():
        new_slice += 1
    
    # applying minus button if still higher than min index
    if minus != old_minus_clicks and df_patient["Index"].min() < new_slice:
        new_slice -= 1
        
    # Assigning global variables new values
    old_plus_clicks = plus
    old_minus_clicks = minus
    old_slice = new_slice
    
    return [new_slice]
