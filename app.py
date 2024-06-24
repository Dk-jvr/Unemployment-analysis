import json

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Главная", href="/")),
            dbc.NavItem(dbc.NavLink("Карта безработицы", href="/world-map"))
        ],
        brand="Дашборд по безработице во всем мире",
        color="primary",
        dark=True,
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.H1("Главная страница"),
    html.P("Выберите страницу из меню выше.")
])

from pages import worldmap

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/world-map':
        return worldmap.get_layout()
    else:
        return index_page


worldmap.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
