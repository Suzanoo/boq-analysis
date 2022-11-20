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
            ])
        ]),      
    ])
    return layout

