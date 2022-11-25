import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq

from dash import html, dcc, callback, Input, Output, State
from dash import dcc
from dash.exceptions import PreventUpdate

from pages.nav import sidebar, top_nav
from tools.utils import bar_plot, df_preprocessing

BG_COLORS = {
    'background': '#202020',
    'text': '#7FDBFF'
}

GRAPH_LAYOUT = {
    'plot_bgcolor': BG_COLORS['background'],
    'paper_bgcolor': BG_COLORS['background'],
    'font': {
        'color': BG_COLORS['text']
    }
}

dash.register_page(__name__)

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
            html.H5('Working Breakdown Structure Level 3:'),
            dcc.Dropdown(id='wbs2-dropdown', className='ddb1',
                        persistence=True, # allow initial value
                        persistence_type='session', # kept when reload, clear on close browser & new tab
                        persisted_props=['value']
            ),
            html.Button('Submit', id='button2', n_clicks=0, className='btn1 mb-2'),
            dcc.Graph(id='wbs3-render', className='pb-4', figure={}),
            dcc.RadioItems(id='radio3',
                options = [
                    {'label':'Show Legend', 'value':True},
                    {'label':'Hide Legend', 'value':False}
                ], value=True,  inline=True
            ),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.H5('Working Breakdown Structure Level 4:'),
            dcc.Dropdown(options=[], id='wbs3-dropdown', className='ddb1',
            persistence=True, # allow initial value
            persistence_type='session', # kept when reload, clear on close browser & new tab
            persisted_props=['value']
            ),
            html.Button('Submit', id='button3', n_clicks=0, className='btn1 mb-2'),  
            dcc.Graph(id='wbs4-render', className='pb-4', figure={}),
            dcc.RadioItems(id='radio4',
                options = [
                    {'label':'Show Legend', 'value':True},
                    {'label':'Hide Legend', 'value':False}
                ], value=True,  inline=True
            ),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.H5('Item Description:'),
            dcc.Dropdown(options=[], id='wbs4-dropdown', className='ddb1',
                        persistence=True, # allow initial value
                        persistence_type='session', # kept when reload, clear on close browser & new tab
                        persisted_props=['value']),
            html.Button('Submit', id='button4', n_clicks=0, className='btn1 mb-2'),  
            dcc.Graph(id='desc-render', className='pb-4', figure={}), 
            dcc.RadioItems(id='radio5',
                options = [
                    {'label':'Show Legend', 'value':True},
                    {'label':'Hide Legend', 'value':False}
                ], value=True,  inline=True
            ),
        ])
    ]),
])

layout = html.Div(id='wbs-page', children=[ 
    dbc.Col([sidebar()]),
    dbc.Col([top_nav(), content]), 
])

# =================================
# switch theme
@callback(
    Output('wbs-page', 'className'),
    Input('toggle-theme', 'on'),
    State('wbs-page', 'className'),
)
def switch_bg(dark, name):
    if(dark):
        name = 'dark'
    else:
        name = ''
    return name

# update dropdown options
@callback(
    Output('wbs2-dropdown', 'options'),
    Output('wbs3-dropdown', 'options'),
    Output('wbs4-dropdown', 'options'),
    Input('stored-data', 'data'),
    )
def update_dropdown_options(data):
    if data is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)
        ddf = df[(df['WBS_1'] != 'PRELIMINARIES')].copy()

        options2 = ddf['WBS_2'].unique()
        options3 = ddf['WBS_3'].unique()
        options4 = ddf['WBS_4'].unique()

        return options2, options3, options4
    else:
        raise PreventUpdate

# render graph wbs_3
@callback(
    Output('wbs3-render', 'figure'),
    Input('button2', 'n_clicks'),
    State("stored-data", "data"),
    State('wbs2-dropdown', 'value'),# used State instead of Input since, value did not update value click
    Input('toggle-theme', 'on'),
    Input('radio3', 'value'),
    prevent_initial_call=True) 
def render_wbs3(n, data, value, theme, legend):
    if value is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)
        fig = bar_plot(df, 'WBS_2', 'WBS_3', value)
        fig.update_layout(showlegend=legend)
        if theme:
            fig.update_layout(dict1=GRAPH_LAYOUT)
        else:
            pass
        return fig
    else:
        raise PreventUpdate

# render graph wbs_4
@callback(
    Output('wbs4-render', 'figure'),
    Input('button3', 'n_clicks'),
    State("stored-data", "data"),
    State('wbs3-dropdown', 'value'),
    Input('toggle-theme', 'on'),
    Input('radio4', 'value'),
    prevent_initial_call=True) 
def render_wbs4(n, data, value, theme, legend):
    if value is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)
        fig = bar_plot(df, 'WBS_3', 'WBS_4', value)
        fig.update_layout(showlegend=legend)
        if theme:
            fig.update_layout(dict1=GRAPH_LAYOUT)
        else:
            pass
        return fig
    else:
        raise PreventUpdate

# render graph of items
@callback(
    Output('desc-render', 'figure'),
    Input('button4', 'n_clicks'),
    State("stored-data", "data"),
    State('wbs4-dropdown', 'value'),
    Input('toggle-theme', 'on'),
    Input('radio5', 'value'),
    prevent_initial_call=True) 
def render_desc(n, data, value, theme, legend):
    if value is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)
        fig = bar_plot(df, 'WBS_4', 'DESCRIPTION', value)
        fig.update_layout(showlegend=legend)
        if theme:
            fig.update_layout(dict1=GRAPH_LAYOUT)
        else:
            pass
        return fig
    else:
        raise PreventUpdate