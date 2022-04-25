from dash import dcc, html, Input, Output, callback
from dataloading import patients_slider,segments_slider
import dash_daq as daq
import dash_bootstrap_components as dbc
Style = {'textAlign': 'center'}


layout = html.Div([
            html.H1("EPL visulization", style = Style),
            html.Br(),
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
            html.Br(),
       
            dbc.Button("-", "minus",style ={'display': 'inline-block'},
            outline=True, color="success", className="me-1"), # plus button
            dbc.Button("+", "plus",style ={'display': 'inline-block'},
            outline=True, color="success", className="me-1")]), # minus button
            html.Br(),

            dcc.Graph(id = "figure_slider", figure = {}, #Initializing slider figure
                    style={'width': 700, 
                    'height': 600,'display': 'inline-block'}),

            dcc.Graph(id = "figure_slider_perf", figure = {}, #Initializing perf_slider figure
                    style={'width': 450, 
                    'height': 600,'display': 'inline-block'})
        
        ])   

