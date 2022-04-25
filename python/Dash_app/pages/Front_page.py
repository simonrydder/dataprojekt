from dash import dcc, html, Input, Output, callback


Title = "Perfomance Testing of Auto-Segmentation Algorithms"
Authors = "Simon Rydder, Eskild Andersen & Alex Kolby"
Supervisors =  "Stine Korreman, Mathis xxxxxx & Asger Hobolt"
description = "Some usefull blablabla about the dashboard"
Style = {'textAlign': 'center'}


layout = html.Div([
    html.Br(),
    html.H1(Title,style=Style),
    html.Br(),
    html.H2(Authors,style=Style),
    html.Br(),
    html.H3("Supervisors: "+Supervisors,style=Style),
    html.Br(),
    description
])


