# # # from dash import Dash, html, dcc
# # # import dash_bootstrap_components as dbc
# # # from dash.dependencies import Input, Output, State
# # # from flask import session
# # # from PanelDL.easySql import sql_query
# # # import plotly.graph_objs as go
# # # from pprint import pprint
# # # import plotly.express as px
# # # import pandas as pd
# # # import threading
# # # from pandas import DataFrame
# # # from plotly.subplots import make_subplots
# # # import plotly.graph_objs as go
# # # import math
# # # from collections import defaultdict
# # # import dash
# # #
# # # data = defaultdict(list,{'train_acc': [0.94, 0.94],'val_acc': [0.23, 0.23]})
# # # data_df = DataFrame(data)
# # # data_df["step"] = data_df.index
# # # print(data_df)
# # # #sub_fig = px.line(data_df,x="step",y="val_acc",markers="*")
# # # sub_fig = go.Scatter(x=data_df["step"],y=data_df["val_acc"])
# # #
# # # from plotly.subplots import make_subplots
# # #
# # # trace0 = sub_fig
# # # trace1 = sub_fig
# # # trace2 = sub_fig
# # # trace3 = sub_fig
# # #
# # # fig = make_subplots(rows=2,  # 将画布分为两行
# # #                     cols=2,  # 将画布分为两列
# # #                     subplot_titles=["trace0的标题",
# # #                                     "trace1的标题",
# # #                                     "trace3的标题"],  # 子图的标题
# # #                     x_title="x轴标题",
# # #                     y_title="y轴标题"
# # #                    )
# # # # 添加轨迹
# # # fig.append_trace(trace0, 1, 1)  # 将trace0添加到第一行第一列的位置
# # # fig.append_trace(trace1, 1, 2)  # 将trace1添加到第一行第二列的位置
# # # fig.append_trace(trace2, 2, 1)  # 将trace2添加到第二行第一列的位置
# # # fig.append_trace(trace3, 2, 2)  # 将trace3添加到第二行第二列的位置
# # # fig.show()
# # #
# # # # print(type(fig))
# # # #
# # # # for idx, sub_fig in enumerate(list(range(8))):
# # # #     x = (idx) // 3 + 1
# # # #     y = (idx) % 3 + 1
# # # #     print(idx+1 ,x, y)
# # # #
# # # #
# # # #
# # # # app = dash.Dash(__name__)
# # # #
# # # # app.layout = html.Div([
# # # #     dcc.Graph(figure=fig)
# # # # ])
# # # #
# # # # app.run_server(debug=True)
# # #
# # # import dash_bootstrap_components as dbc
# # # import pandas as pd
# # #
# # # df = pd.DataFrame(
# # #     {
# # #         "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"],
# # #         "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
# # #     }
# # # )
# # #
# # # table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
# #
# #
# # # import dash_bootstrap_components as dbc
# # # import pandas as pd
# # #
# # # config = {'config': None, 'project_id': 25, 'project_name': 'PetFinder', 'last_activate_date': None, 'privacy': 'privacy'}
# # # # df = pd.DataFrame(config,index=[0])
# # # # print(df)
# # # config = [(key,value) for key,value in config.items()]
# # # df = pd.DataFrame(config,columns=["Name","Value"])
# # # table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
# # #
# # #
# # # import plotly.express as px
# # # df = px.data.tips()
# # # print(df)
# # # fig = px.parallel_categories(df, color="size", color_continuous_scale=px.colors.sequential.Inferno)
# # # fig.show()
#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.express as px
#
# df = px.data.gapminder()
# print(df["lifeExp"])
# all_continents = df.continent.unique()
# print(all_continents)
#
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     dcc.Checklist(
#         id="checklist",
#         options=[{"label": x, "value": x}
#                  for x in all_continents],
#         value=all_continents[3:],
#         labelStyle={'display': 'inline-block'}
#     ),
#     html.Div(children=[dcc.Graph(id="line-chart"),dcc.Graph(id="line-chart-1")],id="LINE")
# ])
#
# @app.callback(
#     Output("LINE", "children"),
#     [Input("checklist", "value")])
# def update_line_chart(continents):
#     mask = df.continent.isin(continents)
#     fig = px.line(df[mask],x="year", y="lifeExp", color='country')
#     return [dcc.Graph(figure=fig),dcc.Graph(figure=fig),html.H2("END!")]
#
# app.run_server(debug=True)

# import json
# config = {'batch_size': 58, 'epochs': 40, 'lr': 0.004653869786938217, 'model': 'resnet34', 'optimizer': 'sgd', 'root': '/home/cth/medical/pic_trans_1', 'weight_decay': 0.02930755111027491}
# config = {}
# config = {'batch_size': 9, 'epochs': 40, 'lr': 0.005949914039660319, 'model': 'small_swin', 'optimizer': 'sgd', 'root': '/home/cth/medical/pic_trans_1', 'weight_decay': 0.004414406943967377}
# config_json = json.dumps(config)
# print(config_json)
#
# config = {'batch_size': 27, 'epochs': 40, 'lr': 0.0018898441910914455, 'model': 'resnet34', 'optimizer': 'sgd', 'root': '/home/cth/medical/pic_trans_1', 'weight_decay': 0.01292644501976178}
# print(json.dumps(config))
# #INSERT INTO enroll_run(user_id,project_id,run_create_date,run_name,run_id) VALUES(-1,31,'2022-02-15 18:16:16.933563','swin_transformer1',155)

from pandas import DataFrame
import plotly.express as px
import random
import numpy as np

key = ["lr","root","model","epoch"]
#config_list = [{'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.106681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}]
config_list = []
for epo in range(30):
    dic = dict()
    for key_ele in key:
        dic[key_ele] = random.random()
        dic["test"] = random.choice(("a","b"))
    config_list.append(dic)
#config_list = [{'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.106681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}, {'lr': 0.006681114660920741, 'root': '/home/cth/medical/pic_trans_1', 'model': 'convnext_base', 'epochs': 40, 'optimizer': 'sgd', 'batch_size': 9, 'weight_decay': 0.026987313080480524}]
df = DataFrame(config_list)
color_col = df.columns[0]
print(df)
midpoint = np.average(df[color_col])
fig = px.parallel_coordinates(df, color=color_col,color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=midpoint)

fig.show()

