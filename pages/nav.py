from dash import html, dcc
import dash_bootstrap_components as dbc

def sidebar():
    layout = html.Div(id='sidebar', className='sidebar', children=
        [
            html.H5("BOQ Analysis:", style={'color':'orange'}),
            html.Hr(),
            html.Div(
            [
                html.A(),
                dbc.Nav(className="navbar-nav bd-navbar-nav ", children=
                    [
                        dbc.NavItem([
                            dbc.NavLink("_Home", href="/", active="exact",
                                        className='nav-link bi bi-house me-2')
                        ]),
                        dbc.NavItem([
                            dbc.NavLink('_WBS', href="/wbs", active="exact",
                                        className='nav-link bi bi-bar-chart me-2')
                        ]),
                        dbc.NavItem([
                            dbc.NavLink('_Query', href="/query", active="exact",
                                        className='nav-link bi bi-funnel-fill me-2')
                        ]),
                    ],
                    vertical=True,
                    pills=True,
                ),
                    html.Hr(),
                    html.Div([
                        html.Button("Download Example File", id="download-btn"),
                        dcc.Download(id="example")
                    ])
            ]),
        ]
    )
    return layout

def top_nav():
    layout = html.Div(id='top-nav', className='', children=[
        dbc.Row([
            dbc.Col([
                dbc.Nav(className="navbar-nav bd-navbar-nav ", children=
                    [
                        dbc.NavItem([
                            dbc.NavLink("_Home", href="/", active="exact",
                                        className='top-nav bi bi-house me-2 d-flex justify-content-center text-white')
                        ]),
                        dbc.NavItem([
                            dbc.NavLink('_WBS', href="/wbs", active="exact",
                                        className='top-nav bi bi-bar-chart me-2 d-flex justify-content-center text-white')
                        ]),
                        dbc.NavItem([
                            dbc.NavLink('_Query', href="/query", active="exact",
                                        className='top-nav bi bi-funnel-fill me-2 d-flex justify-content-center text-white')
                        ]),
                    ],
                    vertical=True,
                    pills=False,
                ),
                html.Div([
                        html.Button("Download Example File", id="download-btn"),
                        dcc.Download(id="example")
                    ], className='me-2 d-flex justify-content-center ')
            ])
        ]),      
    ])
    return layout

