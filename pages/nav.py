from dash import html
import dash_bootstrap_components as dbc

def sidebar():
    layout = html.Div(id='sidebar', className='sidebar', children=
        [
            html.H5("BOQ Analysis:", style={'color':'orange'}),
            html.Hr(),
            html.Div(
            [
                dbc.Nav(className="navbar-nav bd-navbar-nav ", children=
                    [
                        dbc.NavLink(className='nav-link', children=["Home"], href="/", active="exact"),
                        dbc.NavLink(className='nav-link', children=["WBS"], href="/wbs", active="exact"),
                        dbc.NavLink(className='nav-link', children=["Query"], href="/query", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
                    html.Hr(),
            ]),
        ],
        # style={'background-color':'#696d71',}
    )
    return layout

def top_nav():
    layout = html.Div(id='top-nav', className='', children=[
        dbc.Row([
            dbc.Col([
                dbc.Nav(className="navbar-nav bd-navbar-nav ", children=
                    [
                        dbc.NavLink(className='nav-link-top', children=["Home"], href="/", active="exact"),
                        dbc.NavLink(className='nav-link-top', children=["WBS"], href="/wbs", active="exact",),
                        dbc.NavLink(className='nav-link-top', children=["Query"], href="/query", active="exact"),
                    ],
                    vertical=True,
                    pills=False,
                ),
            ])
        ]),      
    ])
    return layout

