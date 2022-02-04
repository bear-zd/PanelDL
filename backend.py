from dash import Dash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, request, redirect, render_template, session
from werkzeug.serving import run_simple
import dash_html_components as html

server = Flask(__name__)
dash_app1 = Dash(__name__, server=server, url_base_pathname='/dashboard/')
dash_app2 = Dash(__name__, server=server, url_base_pathname='/reports/')
dash_app1.layout = html.Div([html.H1('Hi there, I am app1 for dashboards')])
dash_app2.layout = html.Div([html.H1('Hi there, I am app2 for reports')])


@server.route('/')
@server.route('/login', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'admin' and pwd == '123':  # 这里可以根据数据库里的用户和密码来判断，因为是最简单的登录界面，数据库学的不是很好，所有没用。
        session['user_info'] = user
        return redirect('/index')
    else:
        return render_template('login.html', msg='用户名或密码输入错误')


@server.route('/ping')
def ping():
    return 'pong'


@server.route('/dashboard')
def render_dashboard():
    return redirect('/dash1')


@server.route('/reports')
def render_reports():
    return redirect('/dash2')


app = DispatcherMiddleware(server, {
    '/dash1': dash_app1.server,
    '/dash2': dash_app2.server
})

run_simple('0.0.0.0', 8080, app, use_reloader=True, use_debugger=True)
# app.run('0.0.0.0', 8080, use_reloader=True, use_debugger=True)
