import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from pages import Front_page, Metric_page, Performance_page, EPL_page
from dataloading import segments,metrics,comparisons, patients_slider, segments_slider, tolerances
import dash_daq as daq

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.config.serve_locally = False

# the style arguments for the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "white",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#Text at the top of the sidebar
sidebar_text = "Performance Testing of Auto- Segmentation Algorithms"

#Constructing the sidebar
sidebar = html.Div(
    [
        html.H3(sidebar_text),
        html.Hr(),
        html.P(
            dbc.Nav(dbc.NavLink("Home", href="/", active="exact"),vertical=True,
            pills=True,)
            ,className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Metric Overview", href="/Metric_page", active="exact"),
                dbc.NavLink("EPL Visualization", href="/EPL_page", active="exact"),
                dbc.NavLink("Performance Overview", href="/Performance_page", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    id = "sidebar"
)

# all components of the dashboard have to be pseudo created here to 
# avoid errors when loading

content = html.Div(id="page-content", style=CONTENT_STYLE, children= [
    dcc.Dropdown(id="slct_segment",value = [segments[0]]),
    dcc.Dropdown(id="slct_metrics",value = metrics),
    dcc.Dropdown(id="slct_comp",value = comparisons),
    dcc.Graph(id = "figure_perf"), #Initializing figure
    daq.Slider(id = "slider", value = 87),
    dcc.Dropdown(id = "patient",
                value = patients_slider[0]),
    dcc.Dropdown(id = "segment_slider", 
                value = segments_slider[0]),    
    dcc.Dropdown(id = "method_slider", 
                value = "GTvsDL"),
    dcc.Dropdown(id = "tolerance_slider", 
                value = "0"),
    dbc.Button("-", "minus"),
    dbc.Button("+", "plus"), 
    dcc.Graph(id = "figure_slider"),
    dcc.Graph(id = "figure_slider_perf"),
    dcc.Dropdown(id="boxplot_segment",
                value = [segments[0]]), 
    dcc.Dropdown(id="boxplot_comp",
                value = [tolerances[0]]),     
    dcc.Graph(id = "figure_violin"),
    dcc.Graph(id = "figure_boxplot"),
    dbc.Checklist(id="tolerance_toggle",value = [1]),
    dbc.Checklist(id="tolerance_toggle_scatter",value = [1]),
    dcc.Graph(id = "figure_scatter", figure = {}), 
    dcc.Dropdown(id="scatter_segments",
                value = segments[0]),
    dbc.Button("Download CSV", id = "btn"),
    dcc.Download(id="download")
])

# initializing the app
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


#Call back function to update the page based on the site
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return Front_page.layout
    elif pathname == "/Metric_page":
        return Metric_page.layout
    elif pathname == "/EPL_page":
        return EPL_page.layout
    elif pathname == "/Performance_page":
        return Performance_page.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)