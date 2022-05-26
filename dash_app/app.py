from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
from pages import Front_page, Metric_page, Performance_page, EPL_page
import dash_daq as daq
import os

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions = True
)

server = app.server

style = {'textAlign': 'center', "border-bottom":"2px black solid"}
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
                dbc.NavLink("Overview", href="/Metric_page", active="exact"),
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


content = html.Div(id ="page-content",children = [],style=CONTENT_STYLE)

# initializing the app
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

def pagenotfound(pathname):
    layout_ = html.Div(
        [
            html.H1('404: Not found', className='text-danger'),
            html.Br(),
            html.P(f'The pathname {pathname} was not recognised..'),
            html.P(
                [
                    f'Try open {pathname[1:]} in a new tab by ctrl pressing ',
                    html.A('here', href = pathname[1:],)
                ])
        ], CONTENT_STYLE
    )

    return layout_


#Call back function to update the page based on the site
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return Front_page.layout(app,CONTENT_STYLE,style)
    elif pathname == "/Metric_page":
        return Metric_page.layout(app,CONTENT_STYLE,style)
    elif pathname == "/EPL_page":
        return EPL_page.layout(CONTENT_STYLE,style)
    elif pathname == "/Performance_page":
        return Performance_page.layout(CONTENT_STYLE,style)
    # If the user tries to reach a different page, return a 404 message
    return pagenotfound(pathname)

if __name__ == '__main__':
    app.run_server(debug=True)