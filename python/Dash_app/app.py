import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from pages import Front_page, Metric_page, Performance_page, EPL_page
from dataloading import segments,metrics,comparisons


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
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

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            dbc.Nav(dbc.NavLink("Home", href="/", active="exact"),vertical=True,
            pills=True,)
            ,className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Metric overview", href="/Metric_page", active="exact"),
                dbc.NavLink("EPL visualization", href="/EPL_page", active="exact"),
                dbc.NavLink("Performance overview", href="/Performance_page", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    id = "sidebar"
)

# all components has to be pseudo created here to avoid errors when loading
content = html.Div(id="page-content", style=CONTENT_STYLE, children= [
    dcc.Dropdown(id='page-1-dropdown'),
    dcc.Dropdown(id='page-3-dropdown'),
    dcc.Dropdown(id='page-2-dropdown'),
    html.Div(id='page-1-display-value'),
    html.Div(id='page-2-display-value'),
    html.Div(id='page-3-display-value'),
    dcc.Dropdown(id="slct_segment",value = [segments[0]]),
    dcc.Dropdown(id="slct_metrics",value = [metrics[0]]),
    dcc.Dropdown(id="slct_comp",value = [comparisons[0]]),
    dcc.Graph(id = "figure_perf"), #Initializing figure
])

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


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