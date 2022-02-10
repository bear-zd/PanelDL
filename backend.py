from dash import Dash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, request, redirect, render_template, session
from werkzeug.serving import run_simple
# import dash_html_components as html
from dash import html
from PanelDL.utils.private import SECRET_KEY
from PanelDL import easySql

server = Flask(__name__, static_folder='static',static_url_path='')
server.secret_key = SECRET_KEY
from app import userProject

menu = userProject(server)
query = easySql.sql_query()


# dash_app1 = Dash(__name__, server=server, url_base_pathname='/dashboard/')
# dash_app2 = Dash(__name__, server=server, url_base_pathname='/reports/')
# dash_app1.layout = html.Div([html.H1('Hi there, I am app1 for dashboards')])
# dash_app2.layout = html.Div([html.H1('Hi there, I am app2 for reports')])


@server.route('/', methods=["GET", "POST"], endpoint='/')
@server.route('/login/', methods=["GET", "POST"], endpoint='/')  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('example-email')
    pwd = request.form.get('example-password')
    global query
    user_id = query.get_user_id(user, pwd)
    if user_id != None:
        menu.change_user(user_id)
        return redirect('/menu')
    else:
        return render_template('login.html', msg='用户名或密码输入错误')


@server.route('/ping')
def ping():
    return 'pong'


@server.route('/menu')
def render_dashboard():
    if session.get('user_info') == None:
        return redirect('/login')
    else:
        return redirect('/dash1')


@server.route('/reports')
def render_reports():
    return redirect('/dash2')


app = DispatcherMiddleware(server, {
    '/dash1': menu.menu.server
    # '/dash2': dash_app2.server
})
# session['secret_key'] = 'paneldlllldlenap'
run_simple('0.0.0.0', 8080, app, use_reloader=True, use_debugger=True)
