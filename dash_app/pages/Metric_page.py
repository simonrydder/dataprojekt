from dash import dcc, html, Input, Output

def layout(app, cont_style, header_style):

    # Helper function
    def get_content(type, name):
        assert type == 'txt' or type == 'png', 'Not an implemented type'
        
        nonlocal app

        if type == 'txt':
            with open(f'Info/{name}.{type}', encoding = 'UTF-8') as f:
                return dcc.Markdown(f.read(), mathjax= True)
        if type == 'png':
            return html.Center(html.Img(
                src = app.get_asset_url(f'{name}.png'),
                style = {'height':'40%', 'width':'40%'}
            ))
    
    def section(section_name, *args):
        out = [html.H3(section_name)]
        for arg in args:
            out.append(arg)
        out.append(html.Br())
        
        return out

    title1 = 'Introduction',
    title2 = 'Metric Definitions',

    layout_ = html.Div(
        [   
            # Introduction part
            html.Br(),
            html.H1(title1, style = header_style),
            html.Br(),
            get_content('txt', 'introduction'),

            # Metric Definitions part
            html.Br(),
            html.H1(title2, style = header_style),

            ## DICE
            html.Br(),
            *section(
                'Dice Coefficient',
                get_content('txt', 'Dice'),
                get_content('png', 'Dice')
            ),

            ## Hausdorff
            html.Br(),
            *section(
                'Hausdorff Distance',
                get_content('txt', 'Hausdorff'),
                get_content('png', 'Hausdorff'),
            ),

            ## MSD
            html.Br(),
            *section(
                'Mean Surface Distance',
                get_content('txt', 'MSD'),
                get_content('png', 'MSD')
            ),

            ## EPL
            html.Br(),
            *section(
                'Edited Path Length',
                get_content('txt', 'EPL'),
                get_content('png', 'EPL3'),
                get_content('txt', 'EPL2'),
                get_content('png', 'EPL2'),
            ),

            ## LineRatio
            html.Br(),
            *section(
                'Edited Path Length Line Ratio',
                get_content('txt', 'EPL_Line'),
                get_content('png', 'EPL_Line')
            ),

            ## VolumeRatio
            html.Br(),
            *section(
                'Edited Path Length Volume Ratio',
                get_content('txt', 'EPL_Volume'),
                get_content('png', 'EPL_Volume')
            ),
            
        ],
        cont_style
    )

    return layout_