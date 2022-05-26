from dash import dcc, html, Input, Output, callback, callback_context as ctx
import dataloading as dl
import dash_daq as daq
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def layout(cont_style,header_style):
    title = "EPL Visualization"

    with open('Info/EPL_Visualization.txt') as f:
        content = dcc.Markdown(f.read(),mathjax= True)


    layout_ = html.Div(
        [
                html.Br(),
                html.H1("EPL Visualization", style = header_style),
                html.Br(),
                content,
                dbc.Row([            
                    dbc.Col([
                        daq.Slider(id = "slider", # Slider to switch slice (z)
                            min = 0, 
                            max = 0,
                            value = 0, 
                            step = 1, 
                            size = 500,
                            handleLabel={"label":"slice","showCurrentValue": True})
                    ])
                ],className="g-0"),


                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(id = "patient", # Dropdown for Patient for EPL plot
                            options = dl.dd_epl_patients, 
                            multi = False,
                            value = None,
                            style = {"cursor": "pointer"},
                            clearable = False,
                            placeholder = "Select a Patient")
                    ],width = 3),

                    dbc.Col([ 
                        dcc.Dropdown(id = "segment_slider", #Dropdown for segments for EPL plot
                            options = dl.dd_epl_segments,
                            multi = False,
                            value = None,
                            style = {"cursor": "pointer"},
                            clearable = False,
                            placeholder = "Select a segment")
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
                            options = dl.dd_epl_comparisons,
                            multi = False,
                            value = None,
                            style = {"cursor": "pointer"},
                            clearable = False,
                            placeholder = "Select a method")
                    ],width = 3),

                    
                    dbc.Col([
                        dcc.Dropdown(id = "tolerance_slider", #Dropdown for Tolerance for EPL plot
                            options = dl.dd_epl_tolerances,
                            multi = False,
                            value = None,
                            style = {"cursor": "pointer"},
                            clearable = False,
                            placeholder = "Select a tolerance")
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
                        dcc.Graph(
                            id = 'epl_vis', 
                            figure = {}, 
                            style = {'height':600},
                            config= dl.optionbar
                        ) # Initializing double graph
                    ])
                ])

        ],
        cont_style
    ) # End of the layout  

    return layout_



#initiliazing global values for later use

# Double EPL Visualization plot
# Output and inputs to Double EPL Visualization plot

@callback(
    [
        Output(component_id='epl_vis', component_property='figure'),
        Output(component_id='slider', component_property='max'),
        Output(component_id='slider', component_property='min'),
        Output(component_id="slider", component_property="value")
    ],
    [
        Input(component_id='slider', component_property='value'),
        Input(component_id="patient", component_property="value"),
        Input(component_id="segment_slider", component_property="value"),
        Input(component_id="method_slider", component_property="value"),
        Input(component_id="tolerance_slider", component_property="value"),
        Input('plus', 'n_clicks'),
        Input('minus', 'n_clicks')
    ]
)

def update_epl_vis(slider, patient, segment, method, tolerance,plus, minus):

    color = 'Darkcyan'
    axes = ["xaxis2","xaxis3","xaxis4","xaxis5","xaxis6", "xaxis7"]
    metrics = ["EPL","LineRatio","VolumeRatio","DICE","Haus","MSD"]
    bar = 3


    # Specify subplots
    fig = make_subplots(
        rows = 6, cols = 3,
        column_widths = [0.63, 0.02, 0.35],
        specs = [
            [{'type':'scatter', 'rowspan':6}, None, {'type':'bar'}],
            [           None                , None, {'type':'bar'}],
            [           None                , None, {'type':'bar'}],
            [           None                , None, {'type':'bar'}],
            [           None                , None, {'type':'bar'}],
            [           None                , None, {'type':'bar'}]
        ],
        subplot_titles = (
            f'{segment} on {patient} with tolerance {tolerance}<br> ',
            f'Performance of slice {slider}<br>{metrics[0]}',*metrics[1:]
        )
    )

    fig.update_yaxes(dtick=1,showticklabels=False)
    fig.update_xaxes(dtick=1,showticklabels=False)


    # Defining plot before all 4 options are selected
    if patient == None or segment == None or method == None or tolerance == None:
        new_slice = 0
        # Add slice plot
        fig.add_trace(
            go.Scatter(x = [], y = []),
            row = 1, col = 1
        )

        # Add bar plots
        for idx, metric in enumerate(metrics):
            fig.add_trace(
                go.Bar(
                    x = [0], y = [metric],
                    orientation = 'h', # Horizontal plot
                    showlegend = False
                ),
                row = idx + 1, col = bar
            )

            fig['layout'][axes[idx]].update(
                showticklabels = True,
                visible = False
            )

            _max = 0
            _min = 0            

        return [fig, _max, _min,new_slice]

    triggered_button = ctx.triggered[0]["prop_id"]

    # Getting data with correct tolerance
    df_slice = eval(f'dl.df_slice_{tolerance}')
    # exec(f'df_slice = dl.df_slice_{tolerance}')

    df_slice = df_slice[df_slice["ID"]==patient]
    df_slice = df_slice[df_slice["Segment"]==segment]
    range_max = {
        metric : df_slice[metric].max()
        if metric not in ['DICE', 'LineRatio', 'VolumeRatio']
        else 1
        for metric in metrics
    }
    df_slice = df_slice[df_slice["Comparison"]==method]
    
    _max = df_slice['Index'].max()      # Ranfe for slider
    _min = df_slice['Index'].min()      # Range for slider
  
    new_slice = slider

    if plus == None and minus == None and new_slice == 0:
        new_slice = _min
    # applying plus button if still less than max index
    elif triggered_button == "plus.n_clicks" and new_slice < _max:
        new_slice += 1
    # applying minus button if still higher than min index
    elif triggered_button == "minus.n_clicks" and new_slice > _min:
        new_slice -= 1
    elif triggered_button =="method_slider.value":
        if  new_slice <= _min: 
            new_slice = _min
        elif new_slice >= _max:
            new_slice = _max
    elif triggered_button in ["patient.value","segment_slider.value"]:
        new_slice = _min
        


    # Dict to lookup the length of bar plots in the preformance plot


    # Final filtering 
    df_slice = df_slice[df_slice["Index"] == new_slice]
    df_pref = df_slice[df_slice["Index"]==new_slice].round(3)


    # Getting GT points
    pointsGT = df_slice["PointsGT"].tolist()[0]
    pointsGT = eval(pointsGT)

    # Check if the slice contains points
    try:
        xA, yA = zip(*pointsGT)
    except ValueError:
        xA, yA = ([],[])

    
    # Prepare model lines and EPL lines to plot
    lines_model = df_slice['LinesModel'].tolist()[0]
    lines_model = eval(lines_model)

    lines_changed = df_slice["LinesChanged"].tolist()[0]
    lines_changed = eval(lines_changed)

    # Slice plot (row = 1, col = 1)
    fig.add_trace(
        go.Scatter(
            x = xA, y = yA,
            mode = 'markers',
            name = 'GT',
            marker = {'color':'black', 'size':8}
        ),
        row = 1, col = 1
    )

    def plotLines(figure, lines, color, dash = 'dot'):
        for (x0, y0), (x1, y1) in lines:
            x = [x0, x1]
            y = [y0, y1]
            figure.add_trace(
                go.Scatter(
                    x = x, y = y,
                    mode = 'lines',
                    line = {'dash':dash},
                    showlegend = False,
                    marker = {'color':color}
                ),
                row = 1, col = 1
            )
    
    plotLines(fig, lines_model, 'orange')
    plotLines(fig, lines_changed, 'darkcyan')

    #Showing the correct legend
    if fig["data"][1]['marker']["color"] == "orange":
        fig['data'][1]['showlegend'] = True
        fig['data'][1]['name'] = 'Guess'

    if fig["data"][-1]['marker']["color"] == "darkcyan":
        fig['data'][-1]['showlegend'] = True
        fig['data'][-1]['name'] = 'EPL'

    
    # Set theme and margin of the plot  
    fig.update_layout(
        template = dl.plot_theme,
        legend = dict(
            # orientation = 'h',
            yanchor = 'top',
            y = 1,
            xanchor = 'left',
            x = 0.55
        ),
        title_text = f'{method}'
    )
    fig.update_yaxes(scaleanchor = "x", scaleratio = 1) #scale yaxes to xaxes


    # Performance plot
    for idx, metric in enumerate(metrics):
        value = df_pref[metric].iloc[0]
        try:
            text = f"{value} {dl.units.get(metric)}"
        except TypeError:
            text = value
        # Plotting bar subplot
        fig.add_trace(
            go.Bar(
                x = [value], y = [metric],
                orientation = 'h',  # Horizontal plot
                showlegend = False,
                text = text,
                marker = {'color' : color}
            ),
            row = idx + 1, col = bar
        )

        range_upper = range_max.get(metric)

        fig['layout'][axes[idx]].update(
            range = [0, range_upper],
            matches = None,
            showticklabels = True,
            visible = False
        )
    
        fig.for_each_annotation(lambda a: a.update(text = f'Performance of slice {new_slice}') 
                                            if a.text==f'Performance of slice {slider}'
                                            else None)

    return [fig, _max, _min, new_slice]

#Connections

