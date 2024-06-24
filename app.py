import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from pages import worldmap, charts, bar_charts, index_page

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Главная", href="/")),
            dbc.NavItem(dbc.NavLink("Карта безработицы", href="/world-map")),
            dbc.NavItem(dbc.NavLink("Динамика безработицы", href="/line-chart")),
            dbc.NavItem(dbc.NavLink("Отклонения по континентам", href="/bar-charts"))
        ],
        brand="Дашборд по безработице во всем мире",
        color="primary",
        dark=True,
        fluid=True
    ),
    dbc.Container([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/world-map':
        return worldmap.get_layout()
    elif pathname == '/line-chart':
        return charts.get_layout()
    elif pathname == '/bar-charts':
        return bar_charts.get_layout()
    else:
        return index_page.index_page

worldmap.register_callbacks(app)
charts.register_callbacks(app)
bar_charts.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
