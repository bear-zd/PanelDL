from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from PanelDL.easySql import sql_query

middle_style = {"text-align": "center"}

login = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Login", id="open-Login", n_clicks=0),
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

login_box = html.Div([
        html.H1("Welcome to PanelDL!", style = {"font-size":"80px", "text-align": "center"}), 
        html.H2("Login", style = middle_style),
    ], 
    style = {"padding": "10%"}
)

first_name_input = html.Div(
    [
        dbc.Label("First Name", html_for="example-first-name"),
        dbc.Input(
            type="text",
            id="example-first-name",
            placeholder="Enter Your First Name",
        ),
        # dbc.FormText(
        #     "A password stops mean people taking your stuff", color="secondary"
        # ),
    ],
    className="mb-3",
)

last_name_input = html.Div(
    [
        dbc.Label("Last Name", html_for="example-last-name"),
        dbc.Input(
            type="text",
            id="example-last-name",
            placeholder="Enter Your Last Name",
        ),
        # dbc.FormText(
        #     "A password stops mean people taking your stuff", color="secondary"
        # ),
    ],
    className="mb-3",
)

email_input = html.Div(
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="example-email", placeholder="Enter email"),
        dbc.FormText(
            "Are you on email? You simply have to be these days",
            color="secondary",
        ),
    ],
    className="mb-3",
)

password_input = html.Div(
    [
        dbc.Label("Password", html_for="example-password"),
        dbc.Input(
            type="password",
            id="example-password",
            placeholder="Enter password",
        ),
        dbc.FormText(
            "A password stops mean people taking your stuff", color="secondary"
        ),
    ],
    className="mb-3",
)

form = dbc.Form([first_name_input, last_name_input, email_input, password_input])

login_box = html.Div([
        html.H1("Register", style = {"font-size":"80px", "text-align": "center"}), 
        html.Div(style = {"padding":"3%"}), 
        form, 
        dbc.Button("Submit", color="primary", className="me-1", style = {"margin-left": "93.5%", "scale":"1.1"}),
    ], 
    style = {"padding": "5% 15%"}
)

login.layout = html.Div(
        [
            dcc.Location(id='url', refresh=False),
            navbar, 
            login_box, 
        ]
)

@login.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
        )
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    login.run_server(debug=True)
