from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.express as px
import pandas as pd

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20% 10%'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

    
navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Menu", id = "open-Menu",  n_clicks=0),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            id="navbar-collapse",
            is_open=False,
            navbar=True,
        ),
    ],
    brand="PanelDL",
    brand_href="https://github.com/bear-zd/PanelDL", 
    color="dark",
    dark=True,
)

sidebar = dbc.Offcanvas(
dbc.Container(
        [
            html.H2("Hello, PanelDL!", className = "display-4"), 
            html.Hr(), 
            html.P(
                "Select your favourite project 😊" , className = "lead"
                ), 
            dbc.Nav(
                [
                    dbc.NavLink("project 1", href = "/project=4", active = "exact"), 
                    dbc.NavLink("project 2", href = "/project=2", active = "exact"), 
                    dbc.NavLink("project 3", href = "/project=3", active = "exact"), 
                ], 
                vertical = True, 
                pills = True, 
            ), 

            ]
        ), 
    id="Menu",
    is_open=False, 
    style = SIDEBAR_STYLE, 
)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([navbar, sidebar])

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open 

@app.callback(
    Output("Menu", "is_open"),
    Input("open-Menu", "n_clicks"),
    [State("Menu", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
