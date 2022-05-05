from dash import dcc, html, Input, Output
from app import app 
Style = {'textAlign': 'center', "border-bottom":"2px black solid"}


metrics = {"Dice": "Dice Coefficient","Hausdorff": "Hausdorff Distance",
            "MSD": "Mean Surface Distance","EPL": "Edited Path Length",
            "EPL_Line": "Edited Path Length Line Ratio",
            "EPL_Volume": "Edited Path Length Volume Ratio"}
    

content = [html.H1("Info Regarding Metrics", style = Style),html.Br()]

for metric in metrics.keys():
    content.append(html.H3(metrics.get(metric)))
    content.append(html.Br())
    with open(f"Dash_app\\info\\{metric}.txt") as f:
        content.append(dcc.Markdown(f.read(),mathjax= True))
    try:
        content.append(html.Img(src = app.get_asset_url(f'{metric}.png'), width="520", height="260"))
        content.append(html.Br())
    except Exception:
        print('error')


CONTENT_STYLE = {
    "margin-left": "5rem",
    "margin-right": "5rem",
    "padding": "2rem 1rem",
}

layout = html.Div(content, style = CONTENT_STYLE)

