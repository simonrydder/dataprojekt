from dash import dcc, html, Input, Output, callback
import os

def layout(app,cont_style, header_style):
    title = 'Performance Testing of Auto-Segmentation Algorithms',
    authors = 'Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder',
    supervisors = 'Stine Korreman, Mathis Ersted Rasmussen & Asger Hobolt'

    name_style = {'textAlign': 'center'}

    front_image = html.Img(
                src = app.get_asset_url('frontpage.PNG'),
                style = {'height':'60%', 'width':'60%'}
            )

    with open('Info/Description_front_page.txt') as f:
        content = dcc.Markdown(f.read(), mathjax= True)



    layout_ = html.Div(
        [
            html.Br(),
            html.H1(title, style = header_style),
            html.Br(),
            html.H2(authors, style = name_style),
            html.Br(),
            html.H3("Supervisors: "+ supervisors, style = name_style),
            html.Br(),
            content,
            html.A(
                "Here is a link to our GitHub Page!", 
                href = "https://www.github.com/simonrydder/dataprojekt"
            ),
            html.Br(),
            html.Br(),
            html.Center(front_image,),
            html.Center(html.A('Charlotte L. Brouwer et al, "CT-based delineation of organs at risk in the head and neck region"', href = 'https://www.thegreenjournal.com/article/S0167-8140(15)00401-6/fulltext?fbclid=IwAR1-QFxHK-EOAx8g8B9lBx7iVKYzk71TEPadv0LIZDzJ1MbsDw8Rsp57KqE'))
        ],
        cont_style
    )

    return layout_





