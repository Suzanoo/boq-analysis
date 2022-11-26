import base64
import io
import pandas as pd
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_daq as daq

from dash import dcc, html, Input, Output, State, callback
from dash.exceptions import PreventUpdate

from pages.nav import sidebar, top_nav
from tools.upload import upload_file
from tools.utils import bar_plot, df_preprocessing

DICT= {
    'background': '#202020',
    'text': '#7FDBFF'
}

GRAPH_LAYOUT = {
    'plot_bgcolor': DICT['background'],
    'paper_bgcolor': DICT['background'],
    'font': {
        'color': DICT['text']
    }
}

MASK = ['WBS_1', 'WBS_2', 'WBS_3', 'WBS_4', 'DESCRIPTION',
        'UNIT','QTY', 'MAT', 'LAB', 'TOTAL', 'AMOUNT']

# ==================
dash.register_page(
    __name__,
    path='/',
    title='home', name='home'),

content = html.Div(id='content', children=[ 
    dbc.Row([
        dbc.Col([
            daq.BooleanSwitch(
            on=False,
            id='toggle-theme',
            className='float-end mt-3'),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('Upload File:'),
            upload_file(),
            html.Hr()
        ]),
        
    dbc.Row([
        dbc.Col([
            html.H5('BOQ Summary:'),
            html.Br(),
            html.Br(),
            dcc.RadioItems(id='radio1',
                options={
                    'pie': 'Pie Chart',
                    'bar': 'Bar Chart'
                    },
                value='pie',  inline=True),
            dcc.Graph(id='wbs1-render', className='pb-4', figure={}),
        ],className='col-lg-6 col-mb-12'),

        dbc.Col([
            html.H5('Floor Filter:'),
            dcc.Dropdown(id='floor-filter-dropdown', className='ddb1',
                        placeholder='Select...', multi=True, clearable=True,
                        persistence=True, # allow initial value
                        persistence_type='session', # kept when reload, clear on close browser & new tab
                        persisted_props=['value']
            ), 
                  
            html.Button('Submit', id='button0', n_clicks=0, className='btn1 mb-2'),
            dcc.Graph(id='floor-filter-render', className='pb-4')
        ],className='col-lg-6 col-mb-12')
    ])
    ]),

    dbc.Row([
        dbc.Col([
            html.H5('Working Breakdown Structure Level 2:'),
            dcc.Dropdown(id='wbs1-dropdown', className='ddb1',
                        persistence=True, # allow initial value
                        persistence_type='session', # kept when reload, clear on close browser & new tab
                        persisted_props=['value']
            ),

            html.Button('Submit', id='button1', n_clicks=0, className='btn1 mb-2'),
            dcc.Graph(id='wbs2-render', className='pb-4'),
            dcc.RadioItems(id='radio2',
                options = [
                    {'label':'Show Legend', 'value':True},
                    {'label':'Hide Legend', 'value':False}
                ], value=True,  inline=True
            ),
        ]),
    ]),
])

layout = html.Div(id='home-page', children=[ 
    html.Div(id="trigger"), # hidden div use to trigger on refresh page
    dbc.Col([sidebar()]),
    dbc.Col([top_nav(), content]),
])

# ==================
# switch theme
@callback(
    Output('home-page', 'className'),
    Input('toggle-theme', 'on'),
    State('home-page', 'className'),
)
def switch_bg(dark, name):
    if(dark):
        return 'dark'
    else:
        return ''

# uploaded data
@callback(
    Output('output-data-upload', 'children'),
    Output('stored-data', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
    )
    
## slove bug float type of date cannot iterate(It is 'list_of_dates' argument)
## https://stackoverflow.com/questions/74145275/float-object-not-iterable-dcc-upload-in-dash
def update_output(list_of_contents, list_of_names, list_of_dates):
    contents = list_of_contents
    filename = list_of_names
    
    if contents is not None:
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
            return html.Div([
                'There was an error processing this file.'
            ]), None

        block = html.Div([
            html.P(filename),
        ])
        return block, df.to_dict('records') 
    else:
        raise PreventUpdate

# update dropdown
@callback(
    Output('floor-filter-dropdown', 'options'),
    Output('wbs1-dropdown', 'options'),
    Input('stored-data', 'data'),
    Input('trigger', 'children'), # hidden div use to trigger on refresh page
    prevent_initial_call=False
    )
def update_dropdown_options(data, trigger):
    if data is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)
        FLOORS = [{'label':x, 'value':x} for x in df.columns if x not in MASK]

        ddf = df[(df['WBS_1'] != 'PRELIMINARIES')].copy()
        options1 = ddf['WBS_1'].unique()
        return FLOORS, options1
    else:
        raise PreventUpdate

# render graph wbs_1
@callback(
    Output('wbs1-render', 'figure'),
    Input('stored-data', 'data'),
    Input('radio1', 'value'),
    Input('toggle-theme', 'on'),
    prevent_initial_call=False
    )
def render_wbs1(data, choice, theme):
    if data is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)
        ddf = df.groupby('WBS_1')['AMOUNT'].sum().reset_index()
        ddf.columns = ['Description', 'Amount']

        if choice == 'pie':
            fig = px.pie(ddf, values='Amount', names='Description', hole=.5)
        else:
            fig = px.bar(ddf, x='Description', y='Amount', color='Description')
            fig.update_xaxes(showticklabels=False)

        if theme:
            fig.update_layout(dict1=GRAPH_LAYOUT)
        else:
            pass
        return fig
    else:
        raise PreventUpdate

# --------------------
# render graph by floor filte
@callback(
    Output('floor-filter-render', 'figure'),
    Input('button0', 'n_clicks'),
    State('stored-data', 'data'),
    State('floor-filter-dropdown', 'value'),
    Input('toggle-theme', 'on'),
    prevent_initial_call=True
)
def update_fig(n, data, floors, theme):
    if floors is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)
        floor = [x for x in floors]

        columns = MASK+floor
        ddf = df[columns].copy()
    
        # compute 'QTY' and 'AMOUNT' depend on selected floor 
        ddf['QTY'] = ddf[floor].copy().sum(axis=1)
        ddf['AMOUNT'] = ddf[['QTY', 'TOTAL']].copy().prod(axis=1) 

        # cut off zero in selected floor
        ddf = ddf[~(ddf[floor]==0).all(axis=1)]

        reorder = MASK[0:6]+floor+MASK[6:]
        ddf2 = ddf[reorder].copy()

        ddf2 = ddf2.groupby('WBS_1')['AMOUNT'].sum().reset_index()
        ddf2.columns = ['Description', 'Amount']# rename

        fig = px.bar(
            ddf2, x='Description', y='Amount',
            text='Amount',
            color='Description', log_y=True)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(title='Amount(log-scale)')
        fig.update_traces(texttemplate='%{text:.2s}')

        if theme:
            fig.update_layout(dict1=GRAPH_LAYOUT)
        else:
            pass
    else:
        raise PreventUpdate

    return fig

# render graph wbs_2
@callback(
    Output('wbs2-render', 'figure'),
    Input('button1', 'n_clicks'),
    State('stored-data', 'data'),
    State('wbs1-dropdown', 'value'),
    Input('toggle-theme', 'on'),
    Input('radio2', 'value'),
    prevent_initial_call=True)
def render_wbs2(n, data, value, theme, legend):
    if value is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)

        fig = bar_plot(df, 'WBS_1', 'WBS_3', value)
        fig.update_layout(showlegend=legend)
        if theme:
            fig.update_layout(dict1=GRAPH_LAYOUT)
        else:
            pass
    else:
        raise PreventUpdate

    return fig

@callback(
    Output('example', 'data'),
    Input('download-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def download(n):
    return dcc.send_file('./example_file.png')