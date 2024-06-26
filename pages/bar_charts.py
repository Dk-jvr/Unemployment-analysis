from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('unemployment_analysis.csv', sep=',')
population = pd.read_csv("World_Population_2020.csv", sep=',')

continents = {}
for index, row in df.iterrows():
    country_name = row['Country Name']
    continent = row['Continent']
    if continent in continents:
        continents[continent].append(country_name)
    else:
        continents[continent] = [country_name]


def get_top_countries_global(year):
    merged_df = df[['Country Name', 'Numeric code', str(year)]].merge(population[['Numeric code', str(year)]],
                                                                      how='left', on='Numeric code',
                                                                      suffixes=('', '_population'))

    merged_df = merged_df.sort_values(by=str(year), ascending=False).head(10)
    return merged_df


def get_top_countries_continent(continent, year):
    continent_countries = continents[continent]
    df_filtered = df[df['Country Name'].isin(continent_countries)]
    df_filtered = df_filtered[['Country Name', str(year)]]
    df_filtered = df_filtered.sort_values(by=str(year), ascending=False).head(10)
    return df_filtered


def get_layout():
    return html.Div([
        html.H1("Анализ уровня безработицы в странах по континентам"),

        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='continent-dropdown',
                    options=[{'label': continent, 'value': continent} for continent in continents.keys()],
                    value='Asia',
                    placeholder='Выберите континент',
                    clearable=False,
                    style={'width': '300px', 'margin-right': 'auto', 'margin-left': 'auto'}
                ),
            ], width={'size': 3, 'offset': 1}),

            dbc.Col([
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in range(1992, 2021)],
                    value=2020,
                    placeholder='Выберите год',
                    clearable=False,
                    style={'width': '300px', 'margin-left': 'auto', 'margin-right': 'auto'}
                ),
            ], width={'size': 3}),

        ], justify='center', style={'margin-bottom': '20px'}),

        dbc.Row([
            dbc.Col([
                html.H2('Топ-10 стран по безработице на планете', style={'text-align': 'center'}),
                html.Div(id='top-countries-global-table'),
            ], width={'size': 5, 'offset': 1}),

            dbc.Col([
                html.H2('Топ-10 стран по безработице на континенте', style={'text-align': 'center'}),
                html.Div(id='top-countries-continent-table'),
            ], width={'size': 5}),

        ]),

        dcc.Graph(id='deviation-bar-chart'),
        dcc.Graph(id='change-deviation-bar-chart'),
    ])


def register_callbacks(app):
    @app.callback(
        Output('top-countries-global-table', 'children'),
        Input('year-dropdown', 'value')
    )
    def update_top_countries_global_table(selected_year):
        if not selected_year:
            return []

        top_countries_df = get_top_countries_global(selected_year)
        table_rows = [
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th('Страна', style={'text-align': 'center'}),
                        html.Th('Население', style={'text-align': 'center'}),
                        html.Th('Уровень безработицы', style={'text-align': 'center'}),
                    ])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td(row['Country Name'], style={'text-align': 'center'}),
                        html.Td(f"{row[str(selected_year) + '_population'] / 10e2:.{1}f} млн.", style={'text-align': 'center'}),
                        html.Td(f'{row[str(selected_year)]}%', style={'text-align': 'center'})
                    ]) for index, row in top_countries_df.iterrows()
                ])
            ], className='table')
        ]
        return table_rows

    @app.callback(
        Output('top-countries-continent-table', 'children'),
        Input('continent-dropdown', 'value'),
        Input('year-dropdown', 'value')
    )
    def update_top_countries_continent_table(selected_continent, selected_year):
        top_countries_df = get_top_countries_continent(selected_continent, selected_year)
        table_rows = [
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th('Страна', style={'text-align': 'center'}),
                        html.Th('Уровень безработицы', style={'text-align': 'center'}),
                    ])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td(row['Country Name'], style={'text-align': 'center'}),
                        html.Td(f'{row[str(selected_year)]}%', style={'text-align': 'center'})
                    ]) for index, row in top_countries_df.iterrows()
                ])
            ], className='table')
        ]
        return table_rows

    @app.callback(
        Output('deviation-bar-chart', 'figure'),
        Input('continent-dropdown', 'value'),
        Input('year-dropdown', 'value')
    )
    def update_deviation_bar_chart(selected_continent, selected_year):
        continent_countries = continents[selected_continent]
        df_filtered = df[df['Country Name'].isin(continent_countries)]
        df_filtered = df_filtered[['Country Name', str(selected_year)]]
        continent_avg = df_filtered[str(selected_year)].mean()
        df_filtered['Deviation'] = round(df_filtered[str(selected_year)] - continent_avg, 2)

        fig = px.bar(df_filtered.sort_values(by='Deviation', ascending=True), x='Country Name', y='Deviation',
                     title=f'Отклонение от среднего уровня безработицы в {selected_year}')
        fig.update_layout(xaxis_title='Страна', yaxis_title='Отклонение')
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Отклонение: %{y}%')
        return fig

    @app.callback(
        Output('change-deviation-bar-chart', 'figure'),
        Input('continent-dropdown', 'value'),
        Input('year-dropdown', 'value')
    )
    def update_change_deviation_bar_chart(selected_continent, selected_year):
        continent_countries = continents[selected_continent]
        df_filtered = df[df['Country Name'].isin(continent_countries)]
        df_filtered = df_filtered[['Country Name', str(selected_year), str(selected_year - 1)]]
        df_filtered['Change'] = df_filtered[str(selected_year)] - df_filtered[str(selected_year - 1)]
        continent_avg_change = df_filtered['Change'].mean()
        df_filtered['Change Deviation'] = round(df_filtered['Change'] - continent_avg_change, 2)

        fig = px.bar(df_filtered.sort_values(by='Change Deviation', ascending=True), x='Country Name',
                     y='Change Deviation',
                     title=f'Отклонение от среднего изменения уровня безработицы в {selected_year}')
        fig.update_layout(xaxis_title='Страна', yaxis_title='Отклонение изменения')
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Отклонение изменения: %{y}%')
        return fig
