import pandas as pd
import dash
import dash_bootstrap_components as dbc

from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

from pages.nav import sidebar, top_nav
from tools.utils import df_preprocessing, make_card, query_, table_generated

dash.register_page(__name__)

content = html.Div(id='content', children=[
    dbc.Row([
        dbc.Col([
            html.H5('Material Query:'),
            dcc.Input(id="query-input", className='input1', value='all',
                        type="text", placeholder="Search...type 'all' for all materials query"),

            dcc.Dropdown(id='query-dropdown', className='ddb1',  value='all',
                        options=[], placeholder='Select...', multi=True),
            html.Button('Submit', id='button5', n_clicks=0, className='btn1 mb-2'),
            html.Hr(),
        ])
    ]),
    dbc.Row([
        dbc.Col([make_card('card1', color='orange'),])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='table1')
        ], style={'margin-left':'5px'})
    ]),
],
)

layout = html.Div(children=[ 
    dbc.Col([sidebar()]),
    dbc.Col([top_nav(), content]),
])

# ===============================
# columns name
MASK = ['WBS_1', 'WBS_2', 'WBS_3', 'WBS_4', 'DESCRIPTION',
        'UNIT','QTY', 'MAT', 'LAB', 'TOTAL', 'AMOUNT']

# update dropdown options
@callback(
    Output('query-dropdown', 'options'),
    Input('stored-data', 'data'),
    )
def update_dropdown_options(data):
    if data is not None:
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)

        FLOOR = [{'label':x, 'value':x} for x in df.columns if x not in MASK] + [
                    {'label': 'Select all', 'value': 'all'}]

        return FLOOR
    else:
        raise PreventUpdate

# render table
## solve method to return whole table
## https://stackoverflow.com/questions/55269763/return-a-pandas-dataframe-as-a-data-table-from-a-callback-with-plotly-dash-for-p
@callback(
    Output('table1', 'children'),
    Output('card1', 'children'),
    Input('button5', 'n_clicks'),
    Input("stored-data", "data"),
    State('query-input', 'value'),
    State('query-dropdown', 'value') ,
    prevent_initial_call=True  
)
def update_table(n, data, text, floors):
    '''
    - fetch dataframe from Store
    - there're 4 case to be query
        1.whole table
        2.whole material vs query floors
        3.query material vs every floors
        4.query material vs query floors
    - for case 1 & 3 don't render columns of all floors (use 'QTY' instead)
    
    '''
    # print(f'text: {text}') # string statement
    # print(f'floors: {floors}') # list
    if (n != 0) & (data is not None):
        df = pd.DataFrame.from_dict(data) 
        df = df_preprocessing(df)
        FLOOR = [x for x in df.columns if x not in MASK] # get floors name
        # render whole table
        if (text == 'all') & ('all' in floors):
            ddf = df.copy()
            # render value box
            total = ddf['AMOUNT'].copy().sum()
             # reder table
            columns = [{"name": x, "id": x} for x in MASK] # do not render column floor name
            ddf = ddf.to_dict('records') 
            return table_generated(ddf, columns), dbc.CardBody([
                                                                html.H4(f"Total {text} in {floors}:"),
                                                                html.H5(f'{total:,.2f} : THB')
                                                                ])
        # whole material vs specify floors
        elif (text == 'all') & ('all' not in floors):
            floor = [x for x in floors if x != 'all'] # if user select include 'all' --> cut it off
            columns = MASK+floor
            ddf = df[columns].copy()

            # compute 'QTY' and 'AMOUNT' depend on selected floor 
            ddf['QTY'] = ddf[floor].copy().sum(axis=1)
            ddf['AMOUNT'] = ddf[['QTY', 'TOTAL']].copy().prod(axis=1) 

            ddf = ddf[~(ddf[floor]==0).all(axis=1)] # cut off zero in selected floor

            reorder = MASK[0:6]+floor+MASK[6:]
            ddf = ddf[reorder].copy()

            # render value box
            total = ddf['AMOUNT'].copy().sum() # sum series
            # reder table
            columns = [{"name": x, "id": x} for x in ddf.columns]
            ddf = ddf.to_dict('records')

            return table_generated(ddf, columns), dbc.CardBody([
                                                                html.H4(f"Total {text} in {floors}:"),
                                                                html.H5(f'{total:,.2f} : THB')
                                                                ])
        # query material vs every floors
        elif (text != 'all') & ('all' in floors):
            query = query_(str(text)) # TODO solve text come with '_' is one word (a_b, c_d) OK
            print(f'Query: {query}')
            ddf = df[df['DESCRIPTION'].str.contains(query, case=False, regex=True)].copy().drop(FLOOR, axis=1)

            # check query did not match
            if ddf.shape[0] == 0:
                return None, dbc.CardBody([
                                html.H4(f"No have {text} in BOQ"),
                                ])
            else:
                # render value box
                total = ddf['AMOUNT'].copy().sum() # sum series
                # reder table
                columns = [{"name": x, "id": x} for x in MASK]# do not render column floor name
                ddf = ddf.to_dict('records') 

                return table_generated(ddf, columns), dbc.CardBody([
                                                                    html.H4(f"Total {text} in {floors}:"),
                                                                    html.H5(f'{total:,.2f} : THB')
                                                                    ])
        else: #(text != 'all') & ('all' not in floors)
            floor = [x for x in floors if x != 'all'] # if user select include 'all' --> cut it off
            columns = MASK+floor
            ddf = df[columns].copy()

            # compute 'QTY' and 'AMOUNT' depend on selected floor 
            ddf['QTY'] = ddf[floor].copy().sum(axis=1) # sum df
            ddf['AMOUNT'] = ddf[['QTY', 'TOTAL']].copy().prod(axis=1) # multiply df
            ddf = ddf[~(ddf[floor]==0).all(axis=1)] # cut off zero in selected floor

            query = query_(str(text))
            ddf = ddf[ddf['DESCRIPTION'].str.contains(query, case=False, regex=True)].copy()

            # check query did not match
            if ddf.shape[0] == 0:
                return None, dbc.CardBody([
                                html.H4(f"No have {text} in BOQ"),
                                ])
            else:
                reorder = MASK[0:6]+floor+MASK[6:]
                ddf = ddf[reorder].copy()

                # render value box
                value = ddf['AMOUNT'].copy().sum() # sum series
                # reder table
                columns = [{"name": x, "id": x} for x in ddf.columns]
                ddf = ddf.to_dict('records')

                return table_generated(ddf, columns), dbc.CardBody([
                                                                    html.H4(f"Total {text} in {floors}:"),
                                                                    html.H5(f'{value:,.2f} : THB')
                                                                    ])
    else:
        raise PreventUpdate