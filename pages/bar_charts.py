from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('unemployment_analysis.csv', sep=',')

continents = {}
for index, row in df.iterrows():
    country_name = row['Country Name']
    continent = row['Continent']
    if continent in continents:
        continents[continent].append(country_name)
    else:
        continents[continent] = [country_name]

def get_top_countries_global(year):
    df_filtered = df[['Country Name', str(year)]]
    df_filtered = df_filtered.sort_values(by=str(year), ascending=False).head(10)
    return df_filtered

def get_top_countries_continent(continent, year):
    continent_countries = continents[continent]
    df_filtered = df[df['Country Name'].isin(continent_countries)]
    df_filtered = df_filtered[['Country Name', str(year)]]
    df_filtered = df_filtered.sort_values(by=str(year), ascending=False).head(10)
    return df_filtered

def get_layout():
    return html.Div([
        html.H1("Анализ уровня безработицы в странах по континентам"),

        html.Div([
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': continent, 'value': continent} for continent in continents.keys()],
                value='Asia',
                placeholder='Выберите континент',
                style={'width': '300px', 'margin-right': '20px', 'margin-left': 'auto', 'margin-right': 'auto'}
            ),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in range(1992, 2022)],
                value=2020,
                placeholder='Выберите год',
                style={'width': '120px', 'margin-left': '20px', 'margin-right': 'auto'}
            ),
        ], style={'display': 'grid', 'grid-template-columns': 'auto auto', 'justify-content': 'center', 'margin-bottom': '20px'}),

        html.Div([
            html.H2('Топ-10 стран по безработице на планете'),
            html.Table(id='top-countries-global-table', className='table'),
        ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '20px'}),

        html.Div([
            html.H2('Топ-10 стран по безработице на континенте'),
            html.Table(id='top-countries-continent-table', className='table'),
        ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),

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
        table_rows = []
        for index, row in top_countries_df.iterrows():
            table_rows.append(
                html.Tr([
                    html.Td(row['Country Name']),
                    html.Td(row[str(selected_year)])
                ])
            )
        return table_rows

    @app.callback(
        Output('top-countries-continent-table', 'children'),
        Input('continent-dropdown', 'value'),
        Input('year-dropdown', 'value')
    )
    def update_top_countries_continent_table(selected_continent, selected_year):
        if not selected_continent or not selected_year:
            return []

        top_countries_df = get_top_countries_continent(selected_continent, selected_year)
        table_rows = []
        for index, row in top_countries_df.iterrows():
            table_rows.append(
                html.Tr([
                    html.Td(row['Country Name']),
                    html.Td(row[str(selected_year)])
                ])
            )
        return table_rows

    @app.callback(
        Output('deviation-bar-chart', 'figure'),
        Input('continent-dropdown', 'value'),
        Input('year-dropdown', 'value')
    )
    def update_deviation_bar_chart(selected_continent, selected_year):
        if not selected_continent or not selected_year:
            return {}

        continent_countries = continents[selected_continent]
        df_filtered = df[df['Country Name'].isin(continent_countries)]
        df_filtered = df_filtered[['Country Name', str(selected_year)]]
        continent_avg = df_filtered[str(selected_year)].mean()
        df_filtered['Deviation'] = df_filtered[str(selected_year)] - continent_avg

        fig = px.bar(df_filtered, x='Country Name', y='Deviation', title=f'Отклонение от среднего уровня безработицы в {selected_year}')
        fig.update_layout(xaxis_title='Страна', yaxis_title='Отклонение')
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Отклонение: %{y}')
        return fig

    @app.callback(
        Output('change-deviation-bar-chart', 'figure'),
        Input('continent-dropdown', 'value'),
        Input('year-dropdown', 'value')
    )
    def update_change_deviation_bar_chart(selected_continent, selected_year):
        if not selected_continent or not selected_year or selected_year == 1991:
            return {}

        continent_countries = continents[selected_continent]
        df_filtered = df[df['Country Name'].isin(continent_countries)]
        df_filtered = df_filtered[['Country Name', str(selected_year), str(selected_year - 1)]]
        df_filtered['Change'] = df_filtered[str(selected_year)] - df_filtered[str(selected_year - 1)]
        continent_avg_change = df_filtered['Change'].mean()
        df_filtered['Change Deviation'] = df_filtered['Change'] - continent_avg_change

        fig = px.bar(df_filtered, x='Country Name', y='Change Deviation', title=f'Отклонение от среднего изменения уровня безработицы в {selected_year}')
        fig.update_layout(xaxis_title='Страна', yaxis_title='Отклонение изменения')
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Отклонение изменения: %{y}')
        return fig
