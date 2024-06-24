from dash import dcc, html, Input, Output, State, ALL, callback_context
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

df = pd.read_csv("unemployment_analysis.csv", sep=',')

def get_layout():
    return html.Div([
        html.H1("Анализ уровня безработицы по странам"),
        
        html.Div([
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in df['Country Name'].unique()],
                value=None,
                placeholder='Выберите страну',
                clearable=False,
                style={'flex': '1'}
            ),
            dbc.Button('Добавить страну', id='add-country-button', color='primary', n_clicks=0, style={'margin-left': '10px'}),
        ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),
        
        html.Div(id='selected-countries', children=[
            html.Div([
                html.Span('Russian Federation', style={'margin-right': '10px'}),
                dbc.Button('Удалить', id={'type': 'remove-country-button', 'index': 'Russian Federation'}, color='danger', size='sm', n_clicks=0, style={'font-size': '10px', 'padding': '2px 5px'})
            ], style={'display': 'flex', 'align-items': 'center', 'margin-right': '10px', 'margin-bottom': '5px'}),
            html.Div([
                html.Span('Poland', style={'margin-right': '10px'}),
                dbc.Button('Удалить', id={'type': 'remove-country-button', 'index': 'Poland'}, color='danger', size='sm', n_clicks=0, style={'font-size': '10px', 'padding': '2px 5px'})
            ], style={'display': 'flex', 'align-items': 'center', 'margin-right': '10px', 'margin-bottom': '5px'})
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'margin-bottom': '20px'}),

        dcc.RangeSlider(
            id='year-range-slider',
            min=1991,
            max=2020,
            value=[1991, 2020],
            marks={str(year): str(year) for year in range(1991, 2021)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}
        ),

        html.Div([
            dcc.Graph(id='line-chart'),
        ], style={'margin-bottom': '20px'}),

        html.Div([
            dcc.Graph(id='heatmap', style={'flex': '1'}),
        ], style={'margin-bottom': '20px'}),

        html.Div([
            dcc.Graph(id='bar-chart', style={'flex': '1'}),
        ], style={'margin-bottom': '20px'}),
    ])


def register_callbacks(app):
    @app.callback(
        Output('selected-countries', 'children'),
        Output('country-dropdown', 'value'),
        Input('add-country-button', 'n_clicks'),
        Input({'type': 'remove-country-button', 'index': ALL}, 'n_clicks'),
        State('country-dropdown', 'value'),
        State('selected-countries', 'children')
    )
    def manage_countries(add_clicks, remove_clicks, selected_country, selected_countries):
        ctx = callback_context
        if not ctx.triggered:
            return selected_countries, selected_country

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if 'add-country-button' in button_id and selected_country:
            if selected_country not in [item['props']['children'][0]['props']['children'] for item in selected_countries]:
                selected_countries.append(
                    html.Div([
                        html.Span(selected_country, style={'margin-right': '10px'}),
                        dbc.Button('Удалить', id={'type': 'remove-country-button', 'index': selected_country}, color='danger', size='sm', n_clicks=0, style={'font-size': '10px', 'padding': '2px 5px'})
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-right': '10px', 'margin-bottom': '5px'})
                )
            selected_country = None
        else:
            button_index = eval(button_id)['index']
            selected_countries = [country for country in selected_countries if country['props']['children'][0]['props']['children'] != button_index]
        
        return selected_countries, selected_country

    @app.callback(
        Output('line-chart', 'figure'),
        Output('heatmap', 'figure'),
        Output('bar-chart', 'figure'),
        Input('selected-countries', 'children'),
        Input('year-range-slider', 'value')
    )
    def update_charts(selected_countries, year_range):
        countries = [item['props']['children'][0]['props']['children'] for item in selected_countries]
        if not countries:
            return {}, {}, {}
        
        df_filtered = df[df['Country Name'].isin(countries)]
        df_long = pd.melt(df_filtered, id_vars=['Country Name'], value_vars=[str(year) for year in range(1991, 2022)], var_name='Year', value_name='Unemployment Rate')
        df_long['Year'] = df_long['Year'].astype(int)
        df_long = df_long[(df_long['Year'] >= year_range[0]) & (df_long['Year'] <= year_range[1])]
        
        line_fig = px.line(df_long, x='Year', y='Unemployment Rate', color='Country Name', title='Динамика уровня безработицы по странам')
        line_fig.update_traces(mode='lines+markers', hovertemplate='Год: %{x}<br>Безработица: %{y}%')
        line_fig.update_layout(
            xaxis_title='Год', 
            yaxis_title='Уровень безработицы',
            legend_title='Страна'
        )

        heatmap_data = df_long.pivot(index='Country Name', columns='Year', values='Unemployment Rate')
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Plasma_r'
        ))
        heatmap_fig.update_layout(
            title='Тепловая карта уровня безработицы по годам', 
            xaxis_title='Год', 
            yaxis_title='Страна',
            legend_title='Страна'
        )

        df_long['Previous Year Unemployment Rate'] = df_long.groupby('Country Name')['Unemployment Rate'].shift(1)
        df_long['Change'] = df_long['Unemployment Rate'] - df_long['Previous Year Unemployment Rate']
        
        bar_fig = go.Figure()
        for country in df_long['Country Name'].unique():
            country_data = df_long[df_long['Country Name'] == country]
            bar_fig.add_trace(go.Bar(
                x=country_data['Year'],
                y=country_data['Change'],
                name=country,
                text=country_data['Country Name'],
                hovertemplate='Год: %{x}<br>Страна: %{text}<br>Изменение уровня безработицы: %{y}%',
            ))

        bar_fig.update_layout(
            title='Изменение уровня безработицы по годам',
            xaxis_title='Год',
            yaxis_title='Изменение уровня безработицы',
            legend_title='Страна',
            barmode='group'
        )
        
        return line_fig, heatmap_fig, bar_fig
