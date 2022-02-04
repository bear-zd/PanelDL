import dash
import dash_html_components as html



app = dash.Dash(__name__)
app.config[''] # 可以使用config属性保存浏览属性
app.index_string = '''

'''

app.layout = html.Div('Simple Dash App')

if __name__ == '__main__':
    app.run_server(debug=True)
