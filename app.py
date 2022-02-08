from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import session
from PanelDL.easySql import sql_query

import plotly.express as px
import pandas as pd
import threading

change_user_event = threading.Event()

class userProject:
    def change_user(self, user_id):
        query = sql_query()
        self.user_id = user_id
        self.first_name = query.get_user_first_name(user_id) 
        self.menu.layout["Menu"]["title"].children = "Hello, {}!".format(self.first_name)

    def __init__(self, server, router='/menu/'):
        self.user_id = None
        self.first_name = None;
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
        menu = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server, url_base_pathname=router)
        
        navbar = dbc.NavbarSimple(
            children=[
                dbc.Button("Menu", id="open-Menu", n_clicks=0),
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
                    html.H2("Hello, PanelDL!", id = "title", className="display-5"),
                    html.Hr(),
                    html.P(
                        "Select your favourite project 😊", className="lead"
                    ),
                    dbc.Nav(
                        dbc.DropdownMenu(
                            label = "project 1", 
                            children = [
                                dbc.Button("run 1", color="primary", className="me-1"), 
                                dbc.Button("run 2", color="primary", className="me-1"), 
                            ],
                        ),
                        vertical=True,
                        pills=True,
                    ), 
                ], 
                id = "user box", 
            ),
            id="Menu",
            is_open=False,
            style=SIDEBAR_STYLE,
        )
        menu.layout = html.Div([navbar, sidebar])

        self.menu = menu
        @menu.callback(
            Output("navbar-collapse", "is_open"),
            [Input("navbar-toggler", "n_clicks")],
            [State("navbar-collapse", "is_open")],
        )
        def toggle_navbar_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        @menu.callback(
            Output("Menu", "is_open"),
            Input("open-Menu", "n_clicks"),
            [State("Menu", "is_open")],
        )
        def toggle_offcanvas(n1, is_open):
            if n1:
                return not is_open
            return is_open

        @menu.callback(
            Output("user box", "children"), 
            Input("title", "children"), 
        )
        def toggle_Project_Nav(text):
            query = sql_query()
            projects_name = query.get_projects_name_list(self.user_id)
            projects_id = query.get_projects_id_list(self.user_id)
            assert(len(projects_id) == len(projects_name))
            runs_name = []
            runs_id = []
            for project_id in projects_id:
                ls1 = query.get_runs_name_list(project_id)
                ls2 = query.get_runs_id_list(project_id)
                runs_name.append(ls1)
                runs_id.append(ls2)

            ret =  [
                        html.H2("Hello, {}!".format(self.first_name), id = "title", className="display-5"),
                        html.Hr(),
                        html.P(
                            "Select your favourite project 😊", className="lead"
                        ),
                ]
            nav = []
            for i in range(len(projects_id)):
                if len(runs_id[i]) == 0:
                    nav.append(
                            dbc.NavLink("{}".format(projects_name[i]), active = "exact", style = {"padding-left": "12px"})
                    )
                else:
                    nav.append(
                            dbc.DropdownMenu(
                                label = "{}".format(projects_name[i]), 
                                toggle_style={
                                    "background": "transparent",
                                    "color": "#0d6efd", 
                                    "display": "block", 
                                    "border-color": "transparent", 
                                    "border-left": "5px", 
                                    },
                                children = [
                                    dbc.DropdownMenuItem("{}".format(runs_name[i][j])) for j in range(len(runs_id[i]))
                                ],
                            )
                    )
            ret.append(dbc.Nav(
                    nav, 
                    vertical=True,
                    pills=True,
                ))
            return ret
             
    

# if __name__ == '__main__':
#     menu.run_server(debug=True)
