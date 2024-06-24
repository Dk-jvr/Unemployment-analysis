import json
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

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

index_page = html.Div([
    html.H1("Главная страница"),
    html.P("Добро пожаловать на дашборд по анализу уровня безработицы по странам мира. Этот дашборд предоставляет всесторонний анализ данных по безработице, охватывающих период с 1991 по 2020 годы. Вы можете исследовать различные аспекты уровня безработицы через интерактивные диаграммы и визуализации, включая:"),
    html.Ul([
        html.Li("Карта мира по безработице: Позволяет визуализировать уровень безработицы по странам и континентам за выбранный год. Это дает возможность быстро оценить глобальное распределение безработицы и выявить региональные тенденции."),
        html.Li("Линейная диаграмма по динамике безработицы: Демонстрирует изменения уровня безработицы в разных странах за выбранный временной промежуток. Эта диаграмма помогает отслеживать тенденции и сравнивать динамику безработицы между странами."),
        html.Li("Тепловая карта по уровню безработицы: Визуализирует уровень безработицы по странам за выбранный период. Темные оттенки указывают на более высокий уровень безработицы, позволяя легко выявлять проблемные области."),
        html.Li("Изменение уровня безработицы по годам: Представляет собой столбчатую диаграмму, показывающую изменения уровня безработицы в различных странах по годам. Это полезно для анализа ежегодных изменений и оценки эффективности экономических политик."),
        html.Li("Топ 10 стран по безработице: Сортирует страны по уровню безработицы и отображает десять стран с самым высоким уровнем за выбранный год. Это помогает выявить наиболее пострадавшие от безработицы страны."),
        html.Li("Столбчатые диаграммы по отклонению уровня безработицы: Эти диаграммы показывают отклонение уровня безработицы в странах и изменения уровня безработицы по годам. Это позволяет более детально анализировать изменения и выявлять тренды."),
    ]),
    html.P("Датасет содержит данные об уровне безработицы по странам мира с 1991 по 2020 годы. Каждый год представлен отдельной колонкой, где указаны значения уровня безработицы для каждой страны. Данные позволяют проводить глубокий анализ и выявлять как долгосрочные, так и краткосрочные тренды в уровне безработицы."),
    html.P("Дашборд разработали:"),
    html.Div([
    html.Div([
        html.Span("Кива Дмитрий БСБО-14-21 "),
        dbc.Button("GitHub", href="https://github.com/Dk-jvr", color="secondary", size="sm", className="mr-2", style={'margin-top': '5px'}),
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'width': '25%'}),
    html.Div([
        html.Span("Годин Иван     БСБО-14-21 "),
        dbc.Button("GitHub", href="https://github.com/CyberN00b", color="secondary", size="sm", className="mr-2", style={'margin-top': '5px'}),
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'width': '25%'}),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-bottom': '20px'}),

    html.Div([
        dbc.Button("Репозиторий дашборда", href="https://github.com/Dk-jvr/Unemployment-analysis", color="primary", className="mr-2")
    ], style={'display': 'flex', 'justify-content': 'center'}) 
])

from pages import worldmap, charts, bar_charts

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
        return index_page


worldmap.register_callbacks(app)
charts.register_callbacks(app)
bar_charts.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
