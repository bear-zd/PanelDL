from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import session
from PanelDL.easySql import sql_query
import plotly.graph_objs as go
from pprint import pprint
import plotly.express as px
import pandas as pd
import threading
from pandas import DataFrame
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import math

change_user_event = threading.Event()

def dbg(a:str):
    print("\033[43m {}\033[0m".format(a))


class userProject:
    def change_user(self, user_id):
        query = sql_query()
        self.user_id = user_id
        self.first_name = query.get_user_first_name(user_id) 
        self.menu.layout["Menu"]["title"].children = "Hello, {}!".format(self.first_name)

    def __init__(self, server, router='/menu/'):
        self.user_id = None
        self.project_id = None
        self.df = None
        self.run_id_to_name_dict = None
        self.run_name_to_id_dict = None
        self.first_name = None
        self.key_total = None
        self.charts = None
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

        graphbar = html.Div(id="graphbar", style={"padding": "10%"})

        menu.layout = html.Div([
                dcc.Location(id='url', refresh=False),
                navbar, 
                sidebar, 
                graphbar
            ])

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
            print("click menu")
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
                                    dbc.DropdownMenuItem("{}".format(runs_name[i][j]), href = "/run_id={}".format(runs_id[i][j])) for j in range(len(runs_id[i]))
                                ],
                            )
                    )
            ret.append(dbc.Nav(
                    nav, 
                    vertical=True,
                    pills=True,
                ))
            return ret


        @menu.callback(
            Output("graphbar", "children"), 
            Output("open-Menu", "n_clicks"),
            Input("url", "pathname"), 
            State("open-Menu", "n_clicks"),
        )
        def switch_page(pathname, n_clicks):
            print("change_url")
            if("/run_id=" in pathname):
                run_id = int(pathname[8:])
                print("run_id",run_id)
                query = sql_query()
                user_of_run = query.get_user_id_by_run_id(run_id)
                print("user_of_run")
                if (user_of_run == None) | (user_of_run != self.user_id):
                    return [], n_clicks
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################

                # 非堆砌版本图
                # fig_list = []
                # data = query.get_log(run_id)
                # data_df = DataFrame(data)
                # data_df["step"] = data_df.index
                # fig_list = []
                # key_list = []
                # for key in data.keys():
                #     if key == "step":
                #         continue
                #     fig = go.Scatter(x=data_df["step"].values,y=data_df[key].values)
                #     print(data_df["step"],data_df[key])
                #     fig_list.append(fig)
                #     key_list.append(key)
                #
                # fig = make_subplots(rows=math.ceil(len(fig_list) / 3), cols=3, subplot_titles=key_list)
                #
                # for idx,sub_fig in enumerate(fig_list):
                #     x = (idx)//3 + 1
                #     y = (idx)%3 + 1
                #     print(x,y)
                #     fig.append_trace(sub_fig,x,y)
                #
                # dcc_fig = dcc.Graph(figure=fig)
                # ret.append(dcc.Graph(figure=fig))

                ret = []

                #CONFIG部分
                config_dict = query.get_config_by_run_id(run_id)
                self.project_id = config_dict["project_id"]
                config = [(key, value) for key, value in config_dict.items() if value is not None]
                df = pd.DataFrame(config, columns=["Name", "Value"])
                table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
                ret.append(table)
                #print(config)

                #绘图部分
                data = query.get_log(run_id)
                data_df = DataFrame(data)
                data_df["step"] = data_df.index
                for key in data.keys():
                    title = html.H2(key)
                    fig = px.line(data_df,x="step",y=key)
                    ret.append(title)
                    ret.append(dcc.Graph(figure=fig))

                #绘制总图部分

                key_total = query.get_unique_key(self.project_id)
                self.key_total = key_total
                run_name_all = query.get_runs_name_list( project_id = self.project_id)
                run_name_all = np.unique(run_name_all)

                check_list = dcc.Checklist(id="check_list", options=[{"label": x, "value": x} for x in run_name_all],labelStyle={'display': 'inline-block'},value=run_name_all)
                ret.append(check_list)

                charts = []

                data = query.get_all_log_data(project_id=self.project_id,key="val_acc")
                # print("data:",data)
                if len(data)!=0:
                    self.df = DataFrame(data)
                    self.run_id_to_name_dict = query.get_run_id_to_name_dict(project_id=self.project_id)
                    self.run_name_to_id_dict = {value: key for key, value in self.run_id_to_name_dict.items()}
                    self.df["run_name"] = [self.run_id_to_name_dict[x] for x in self.df["run_id"]]
                    # print(self.df)

                    # # print(self.key_total)
                    # for idx, key in enumerate(self.key_total):
                    #     charts.append(dcc.Graph(id="line-chart-" + key))
                    # self.charts = charts
                    charts_div = html.Div(children = charts, id = "charts")
                    ret.append(charts_div)


                #     # ret.append(html.Div([check_list,dcc.Graph(id="line-chart")]))
                ret.append(html.H5("END"))

                return ret, n_clicks + 1


        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

            return [], n_clicks

        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        @menu.callback(
            Output("charts", "children"),
            Input("check_list", "value")
        )
        def update_line_chart(run_names):
            print("run_names",run_names)
            local_charts = []
            if run_names is None:
                print("empty")
                #return html.Div(children = [None], id = "charts")
                return [None]
            i = 0
            print(self.key_total)
            for idx, key in enumerate(self.key_total):
                try:
                    run_ids = [self.run_name_to_id_dict[name] for name in run_names]
                except:
                    run_ids = []
                mask1 = self.df.run_id.isin(run_ids)
                mask2 = self.df.key.isin([key])
                mask = mask1&mask2

                fig = px.line(self.df[mask], x="step", y="value", color='run_name')
                local_charts.append(dcc.Graph(figure=fig))
                #self.charts[i].figure = fig
                i += 1
            #return html.Div(children = [self.charts], id = "charts")
            return local_charts
        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################