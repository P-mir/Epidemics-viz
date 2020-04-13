import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

import gunicorn

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Epidemics over time"
server = app.server
df = pd.read_csv('data/epidemics.csv', sep=';', encoding='latin1')
df.dropna(inplace=True)
df['Death toll'] = df['Death toll'].astype("int32")


app.layout = html.Div([
    dcc.Graph(
        id='graph-with-slider'#,
        # figure=fig
    ),
    dcc.RangeSlider(
            id='year-slider',
            min=df['Date'].min(),
            max=df['Date'].max(),
            value=[df['Date'].min(),df['Date'].max()],
            marks={str(year): str(year) for year in df['Date'].unique() if year%3==0},
            step=2,
            updatemode='drag'
    )
])#, style={'columnCount': 2})

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(range):
    filtered_df = df[(df.Date >= range[0]) & (df.Date <= range[1])]
    fig = px.treemap(filtered_df, path=['Event'], values='Death toll', color='Disease', title="Epidemic diseases landscape from {} to {}".format(range[0],range[1]))
    return fig



if __name__ == '__main__':
    app.run_server()