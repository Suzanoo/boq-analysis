# https://dash.plotly.com/dash-core-components/upload
import base64
import io
from dash import dcc, html
import pandas as pd

def upload_file():
    layout = html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div(children=[
                'Drag & Drop or ',
                html.A(children=['Click'], style={"color":"blue"}),
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),
        html.Div(id='output-data-upload'),
    ])
    return layout

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=",")

        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return None

    return df












