from dash import dcc, html, Input, Output, State, ALL, callback_context
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv("unemployment_analysis.csv", sep=',')

years = [str(year) for year in range(1991, 2021)]
continents = df['Continent'].unique()

def get_layout():
    return html.Div([
        html.H1("Карта мира по показателям безработицы"),
        
        dcc.RadioItems(
            id='view-mode',
            options=[
                {'label': 'Страны', 'value': 'countries'},
                {'label': 'Континенты', 'value': 'continents'}
            ],
            value='countries',
            labelStyle={'display': 'inline-block'}
        ),
        
        html.Div(id='continent-form', children=[
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': continent, 'value': continent} for continent in continents],
                placeholder='Выберите континент',
                clearable=True
            ),
            dbc.Button('Добавить континент', id='add-button', color='primary', n_clicks=0),
            html.Div(id='selected-continents', children=[], style={'display': 'flex', 'flex-wrap': 'wrap'})
        ], style={'display': 'block'}),
        
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in years],
            value='2020',
            clearable=False
        ),
        
        dcc.Graph(id='world-map')
    ])

def register_callbacks(app):
    @app.callback(
        Output('continent-form', 'style'),
        Input('view-mode', 'value')
    )
    def toggle_continent_filter(view_mode):
        if view_mode == 'countries':
            return {'display': 'block'}
        else:
            return {'display': 'none'}
    
    @app.callback(
        Output('selected-continents', 'children'),
        Input('add-button', 'n_clicks'),
        Input({'type': 'remove-button', 'index': ALL}, 'n_clicks'),
        State('continent-dropdown', 'value'),
        State('selected-continents', 'children')
    )
    def manage_continents(add_clicks, remove_clicks, selected_continent, selected_continents):
        ctx = callback_context
        if not ctx.triggered:
            return selected_continents

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if 'add-button' in button_id and selected_continent:
            if selected_continent not in [continent['props']['children'][0]['props']['children'] for continent in selected_continents]:
                selected_continents.append(
                    html.Div([
                        html.Span(selected_continent, style={'margin-right': '10px'}),
                        dbc.Button('Удалить', id={'type': 'remove-button', 'index': selected_continent}, color='danger', size='sm', n_clicks=0, style={'font-size': '10px', 'padding': '2px 5px'})
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-right': '10px', 'margin-bottom': '5px'})
                )
        else:
            button_index = eval(button_id)['index']
            selected_continents = [continent for continent in selected_continents if continent['props']['children'][0]['props']['children'] != button_index]
        
        return selected_continents

    @app.callback(
        Output('world-map', 'figure'),
        Input('view-mode', 'value'),
        Input('selected-continents', 'children'),
        Input('year-dropdown', 'value')
    )
    def update_map(view_mode, selected_continents, selected_year):
        selected_continents = [continent['props']['children'][0]['props']['children'] for continent in selected_continents]

        if view_mode == 'countries':
            filtered_df = df
            if selected_continents:
                filtered_df = df[df['Continent'].isin(selected_continents)]
            
            fig = px.choropleth(
                filtered_df,
                locations="Country Code",
                color=selected_year,
                hover_name="Country Name",
                hover_data={
                    "Country Code": True,
                    "Population": True,
                    selected_year: True,
                },
                color_continuous_scale=px.colors.sequential.Plasma,
                labels={selected_year: 'Процент безработицы'},
                title=f"Уровень безработицы по странам в {selected_year} году",
                projection='equirectangular'
            )
        else:
            # Группировка по континентам и расчет процентной безработицы
            df['Unemployment_Count'] = (df[selected_year] * df['Population'] / 100).astype(int)
            continent_df = df.groupby('Continent').agg(
                Total_Unemployment=pd.NamedAgg(column='Unemployment_Count', aggfunc='sum'),
                Total_Population=pd.NamedAgg(column='Population', aggfunc='sum')
            ).reset_index()
            continent_df['Unemployment_Rate'] = (continent_df['Total_Unemployment'] / continent_df['Total_Population']) * 100

            # Дублирование данных континентов для каждой страны в них
            continent_countries = df[['Continent', 'Country Code', 'Country Name']].drop_duplicates()
            continent_df = pd.merge(continent_countries, continent_df, on='Continent')

            fig = px.choropleth(
                continent_df,
                locations="Country Code",
                color='Unemployment_Rate',
                hover_name="Continent",
                hover_data={
                    "Total_Unemployment": True,
                    "Total_Population": True,
                    "Unemployment_Rate": True,
                },
                color_continuous_scale=px.colors.sequential.Plasma,
                labels={'Unemployment_Rate': 'Процент безработицы'},
                title=f"Уровень безработицы по континентам в {selected_year} году",
                projection='equirectangular'
            )
        
        fig.update_geos(
            showcoastlines=True, coastlinecolor="Black",
            showland=True, landcolor="white",
            showocean=True, oceancolor="LightBlue"
        )

        fig.update_layout(
            width=1280,
            height=720,
            margin={"r":0,"t":50,"l":0,"b":0},
            geo=dict(
                projection_scale=1,
                center=dict(lat=0, lon=0)
            )
        )
        
        return fig