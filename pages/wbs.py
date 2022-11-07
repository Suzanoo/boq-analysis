import pandas as pd
import dash
import dash_bootstrap_components as dbc

from dash import html, dcc, callback, Input, Output, State
from dash import dcc

from pages.nav import sidebar, top_nav
from tools.utils import bar_plot, df_preprocessing

dash.register_page(__name__)

content = html.Div(id='content', children=[
    html.H5('Working Breakdown Structure Level 3:'),
    dcc.Dropdown(options=[], id='wbs2-dropdown', className='ddb1'),
    html.Button('Submit', id='button2', n_clicks=0, className='btn1'),
    dcc.Graph(id='wbs3-render', className='pb-4', figure={}),

    html.Hr(),
    html.H5('Working Breakdown Structure Level 4:'),
    dcc.Dropdown(options=[], id='wbs3-dropdown', className='ddb1'),
    html.Button('Submit', id='button3', n_clicks=0, className='btn1'),  
    dcc.Graph(id='wbs4-render', className='pb-4', figure={}),

    html.Hr(),
    html.H5('Item Description:'),
    dcc.Dropdown(options=[], id='wbs4-dropdown', className='ddb1'),
    html.Button('Submit', id='button4', n_clicks=0, className='btn1'),  
    dcc.Graph(id='desc-render', className='pb-4', figure={}),  
])

layout = html.Div(children=[ 
    dbc.Col([sidebar()]),
    dbc.Col([top_nav(), content]), 
]
)

# =================================
# update dropdown options
@callback(
    Output('wbs2-dropdown', 'options'),
    Output('wbs3-dropdown', 'options'),
    Output('wbs4-dropdown', 'options'),
    Input('stored-data', 'data'),
    )
def update_dropdown_options(data):
    df = pd.DataFrame.from_dict(data) 
    df = df_preprocessing(df)
    ddf = df[(df['WBS_1'] != 'PRELIMINARIES')].copy()

    options2 = ddf['WBS_2'].unique()
    options3 = ddf['WBS_3'].unique()
    options4 = ddf['WBS_4'].unique()

    return options2, options3, options4

# render graph wbs_3
@callback(
    Output('wbs3-render', 'figure'),
    Input('button2', 'n_clicks'),
    Input("stored-data", "data"),
    State('wbs2-dropdown', 'value'),# used State instead of Input since, value did not update value click
    prevent_initial_call=True) 
def render_wbs3(n, data, value):
    df = pd.DataFrame.from_dict(data) 
    df = df_preprocessing(df)

    fig = bar_plot(df, 'WBS_2', 'WBS_3', value)
    return fig

# render graph wbs_4
@callback(
    Output('wbs4-render', 'figure'),
    Input('button3', 'n_clicks'),
    Input("stored-data", "data"),
    State('wbs3-dropdown', 'value'),
    prevent_initial_call=True) 
def render_wbs4(n, data, value):
    df = pd.DataFrame.from_dict(data) 
    df = df_preprocessing(df)

    fig = bar_plot(df, 'WBS_3', 'WBS_4', value)
    return fig

# render graph of items
@callback(
    Output('desc-render', 'figure'),
    Input('button4', 'n_clicks'),
    Input("stored-data", "data"),
    State('wbs4-dropdown', 'value'),
    prevent_initial_call=True) 
def render_desc(n, data, value):
    df = pd.DataFrame.from_dict(data) 
    df = df_preprocessing(df)

    fig = bar_plot(df, 'WBS_4', 'DESCRIPTION', value)
    return fig