# -*- coding: utf-8 -*-
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

DF_DIRECTORY = os.getenv(
    "TRANSIT_DIR_PATH", '/data/transit')


def get_state_df(state='rs'):
    try:
        df = pd.read_csv(os.path.join(DF_DIRECTORY, f'{state.lower()}.csv'))
    except Exception as ex:
        print(ex)
        raise PreventUpdate(
            f"Os dados para o estado {state} não estao disponívels")
    return df


def get_chart_state(state='rs'):
    try:
        df = get_state_df(state)
    except PreventUpdate:
        return html.Div(children='- sem dados deste estado -', style={'text-align': 'center'})

    df = get_state_df(state.lower())
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=2, label="2m", step="month", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=15, label="15d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.add_trace(
        go.Scatter(x=df.date, y=df.last_available_confirmed,
                   name="confirmados"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df.date, y=df.last_available_deaths, name="mortos"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"Número de contaminados e mortos por Covid-19 no estado: {state.upper()}"
    )

    fig.update_xaxes(title_text="Dia")

    fig.update_yaxes(title_text="quantidade de <b>mortos</b>",
                     secondary_y=False)
    fig.update_yaxes(
        title_text="quantidade de <b>contaminados</b>", secondary_y=True)

    return dcc.Graph(
        id='chart-state',
        figure=fig
    )


def get_states():
    try:
        df = get_state_df('all')
    except PreventUpdate:
        return('nenhum estado disponivel',)
    return df.state.unique()


def get_chart_all():
    try:
        df = get_state_df('all')
    except PreventUpdate:
        return html.Div(children='- sem dados disponiveis -', style={'text-align': 'center'})

    fig = px.line(
        df,
        x="date",
        y="last_available_confirmed",
        color='state',
        title="Nro de casos confirmados por dia - Todos estados")

    return dcc.Graph(
        id='chart-all',
        figure=fig
    )


app.layout = html.Div(children=[
    html.Div(children=[
        html.H2(children='Jornada Colaborativa - Python',
                style={'width': '80%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='state-filter',
                options=[{'label': i, 'value': i} for i in get_states()],
                value='SC',
                clearable=False,
            )
        ], style={'width': '120px', 'display': 'inline-block'})

    ]),
    dcc.Loading(
        id="loading-state",
        type="default",
        children=get_chart_state()
    ),
    dcc.Loading(
        id="loading-all",
        type="default",
        children=get_chart_all()
    )
])


@app.callback(
    dash.dependencies.Output('loading-state', 'children'),
    [dash.dependencies.Input('state-filter', 'value'),
     ])
def update_graph(state_value):
    fig = get_chart_state(state_value)
    return fig


app.title = 'Jornada Python - Deploy'

# Expose server, that is a Flask app, to run production
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
