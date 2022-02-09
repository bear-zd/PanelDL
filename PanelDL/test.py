# from dash import Dash, html, dcc
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
# from flask import session
# from PanelDL.easySql import sql_query
# import plotly.graph_objs as go
# from pprint import pprint
# import plotly.express as px
# import pandas as pd
# import threading
# from pandas import DataFrame
# from plotly.subplots import make_subplots
# import plotly.graph_objs as go
# import math
# from collections import defaultdict
# import dash
#
# data = defaultdict(list,{'train_acc': [0.94, 0.94],'val_acc': [0.23, 0.23]})
# data_df = DataFrame(data)
# data_df["step"] = data_df.index
# print(data_df)
# #sub_fig = px.line(data_df,x="step",y="val_acc",markers="*")
# sub_fig = go.Scatter(x=data_df["step"],y=data_df["val_acc"])
#
# from plotly.subplots import make_subplots
#
# trace0 = sub_fig
# trace1 = sub_fig
# trace2 = sub_fig
# trace3 = sub_fig
#
# fig = make_subplots(rows=2,  # 将画布分为两行
#                     cols=2,  # 将画布分为两列
#                     subplot_titles=["trace0的标题",
#                                     "trace1的标题",
#                                     "trace3的标题"],  # 子图的标题
#                     x_title="x轴标题",
#                     y_title="y轴标题"
#                    )
# # 添加轨迹
# fig.append_trace(trace0, 1, 1)  # 将trace0添加到第一行第一列的位置
# fig.append_trace(trace1, 1, 2)  # 将trace1添加到第一行第二列的位置
# fig.append_trace(trace2, 2, 1)  # 将trace2添加到第二行第一列的位置
# fig.append_trace(trace3, 2, 2)  # 将trace3添加到第二行第二列的位置
# fig.show()
#
# # print(type(fig))
# #
# # for idx, sub_fig in enumerate(list(range(8))):
# #     x = (idx) // 3 + 1
# #     y = (idx) % 3 + 1
# #     print(idx+1 ,x, y)
# #
# #
# #
# # app = dash.Dash(__name__)
# #
# # app.layout = html.Div([
# #     dcc.Graph(figure=fig)
# # ])
# #
# # app.run_server(debug=True)
#
# import dash_bootstrap_components as dbc
# import pandas as pd
#
# df = pd.DataFrame(
#     {
#         "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"],
#         "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
#     }
# )
#
# table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)


import dash_bootstrap_components as dbc
import pandas as pd

config = {'config': None, 'project_id': 25, 'project_name': 'PetFinder', 'last_activate_date': None, 'privacy': 'privacy'}
# df = pd.DataFrame(config,index=[0])
# print(df)
config = [(key,value) for key,value in config.items()]
df = pd.DataFrame(config,columns=["Name","Value"])
table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)