import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.layout = html.Div([
    dcc.Store(
        id='stored-data',
        storage_type='session',
     ),
	dash.page_container,
])

if __name__ == "__main__":
    app.run_server(debug=True)

# TODO file without floor name : OK 3.11.2022
# TODO query word comes with underscore mean contain together : OK 4.11.2022
# TODO 4 case in query : OK 4.11.2022
# TODO for each graph reder vbox of total amount : NG --> show in graph title instead
# TODO styling for table : OK 7.11.2022
# TODO export table : OK 7.11.2022
# TODO ignore id error
# TODO select graph type
# TODO redirect from 404 not found
# TODO hide legend


# Reference:
'''
- upload data in home page & share it to another pages
https://github.com/AnnMarieW/dash-multi-page-app-demos/tree/main/multi_page_store/pages

- 6 method to folter pandas rows
https://blog.hubspot.com/website/filter-rows-pandas#

## solve method to return whole table
## https://stackoverflow.com/questions/55269763/return-a-pandas-dataframe-as-a-data-table-from-a-callback-with-plotly-dash-for-p

- 
https://stackoverflow.com/questions/55392776/hide-sidebar-on-medium-and-small-screen-devices

## slove bug float type of date cannot iterate(It is 'list_of_dates' argument)
## https://stackoverflow.com/questions/74145275/float-object-not-iterable-dcc-upload-in-dash

'''