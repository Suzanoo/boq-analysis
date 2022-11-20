import re
import plotly.express as px
import dash_bootstrap_components as dbc

from dash import dash_table

def df_preprocessing(df):
    # print(f"shape before: {df.shape}")
    df = df.fillna(0)
    df = df.query('AMOUNT != 0')
    # print(f"shape before: {df.shape}")
    return df

def make_card(id, color='orange',):
    return dbc.Card(
                    id=id, className='card1', children=[],
                    style={'background-color':color,})

def query_(text):
    # text = 'formwork concrete_320 rebar_20mm'
    # text = 'concrete 320'
    all = re.split(r'\s', text)
    underscore = re.findall(r'[\w|\d]+_+[\w|\d]*', text) # ['concrete_320', 'rebar_20mm']

    first = [s for s in all if s not in underscore] # ['formwork']

    second = [] #['(?=.*concrete)(?=.*320)', '(?=.*rebar)(?=.*20mm)']
    for x in underscore:
        y = re.split(r'_', x) #['concrete', '320'], ['rebar', '20mm']
        a = ''
        for z in y:
            a += f"(?=.*{z})"
        second.append(a)

    if len(second) != 0:
        reg = first + second 
        query = '|'.join(reg) # 'formwork|(?=.*concrete)(?=.*320)|(?=.*rebar)(?=.*20mm)'
    else:
        query = '|'.join(first) 
    print(query)
    return query

PALLETE = ['#99BFB4', '#A2D989', '#F2CF63', '#F2762E', '#BF491F']

def create_color(x):
    COLORS = []
    j = 0
    for i in range(len(x)):
        if i == len(PALLETE):
            j = 0 # loop back
        COLORS.append(PALLETE[j])
        j+=1       
    return COLORS

def bar_plot(df, inn, out, ddb_value):
    dff = df[(df['WBS_1'] != 'PRELIMINARIES')]
    dff = dff[dff[inn] == ddb_value].groupby(out)['AMOUNT'].sum().reset_index()
    dff.columns = ['Description', 'Amount']

    value = f"{dff['Amount'].copy().sum():,.2f}"
    
    fig = px.bar(
        dff, x='Description', y='Amount', text='Amount',
        color='Description', title=ddb_value+' WORK : Total '+value+' THB', log_y=True,
        )
                
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(title='Amount(log-scale)')
    fig.update_traces(texttemplate='%{text:.2s}')

    return fig

# https://dash.plotly.com/datatable/width
def table_generated(df, columns):
    return dash_table.DataTable(
                style_table={'overflowX': 'auto'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'lineHeight': '15px'
                },
                data=df,
                columns=columns,
                
                export_format='xlsx',
                export_headers='display',
                )