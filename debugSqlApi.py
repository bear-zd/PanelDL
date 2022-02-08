import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = px.data.gapminder()
all_continents = df.continent.unique()

app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Checklist(
        id="checklist",
        options=[{"label": x, "value": x}
                 for x in all_continents],
        value=all_continents[3:],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="line-chart"),
])


@app.callback(Output("line-chart", "figure"), [Input("checklist", "value")])

def update_line_chart(continents):
    mask = df.continent.isin(continents)
    fig = px.line(df[mask], x="year", y="lifeExp", color='country')
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)