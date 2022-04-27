from dash import dcc, html, Input, Output, callback
from app import app


Title = "Perfomance Testing of Auto-Segmentation Algorithms"
Authors = "Simon Rydder, Eskild Andersen & Alex Kolby"
Supervisors =  "Stine Korreman, Mathis xxxxxx & Asger Hobolt"


with open(f"Dash_app\\info\\Description_front_page.txt") as f:
        description =  f.read().replace("\n", "")

Style_title = {'textAlign': 'center', "border-bottom":"2px black solid"}

Style = {'textAlign': 'center'}



layout = html.Div([
    html.Br(),
    html.H1(Title,style=Style_title),
    html.Br(),
    html.H2(Authors,style=Style),
    html.Br(),
    html.H3("Supervisors: "+Supervisors,style=Style),
    html.Br(),
    description,
    html.Br(),
    html.Div(
    html.Img(src=app.get_asset_url('test1.png')), 
    style = Style)
])


