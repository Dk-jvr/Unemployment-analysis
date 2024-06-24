from dash import dcc, html, Input, Output, State, ALL, callback_context
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

df = pd.read_csv("unemployment_analysis.csv", sep=',')

population = pd.read_csv("World_Population_2020.csv", sep=',')

continents_coordinates = {
    "Asia": [42.283914, 78.224456],
    "Africa": [16.918371, 19.168591],
    "Oceania": [-23.054063, 134.243439],
    "North America": [38.400949, -99.840222],
    "South America": [-9.080489, -57.800021],
    "Europe": [50.000885, 13.474729],
    "America": [None, None],
}

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

        dcc.Graph(id='world-map'),
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

        if 'add-button' in button_id:
            if selected_continent and selected_continent not in [continent['props']['children'][0]['props']['children']
                                                                 for continent in selected_continents]:
                selected_continents.append(
                    html.Div([
                        html.Span(selected_continent, style={'margin-right': '10px'}),
                        dbc.Button('Удалить', id={'type': 'remove-button', 'index': selected_continent}, color='danger',
                                   size='sm', n_clicks=0, style={'font-size': '10px', 'padding': '2px 5px'})
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-right': '10px',
                              'margin-bottom': '5px'})
                )
        else:
            button_index = eval(button_id)['index']
            selected_continents = [continent for continent in selected_continents if
                                   continent['props']['children'][0]['props']['children'] != button_index]

        return selected_continents

    @app.callback(
        Output('world-map', 'figure'),
        Input('view-mode', 'value'),
        Input('selected-continents', 'children'),
        Input('year-dropdown', 'value'),
    )
    def update_map(view_mode, selected_continents, selected_year):

        selected_continents = [continent['props']['children'][0]['props']['children'] for continent in
                               selected_continents]

        merged_df = df.merge(population[['Numeric code', selected_year]], how='left', on='Numeric code',
                             suffixes=('', '_population'))
        if view_mode == 'countries':
            filtered_df = merged_df
            if selected_continents:
                filtered_df = merged_df[merged_df['Continent'].isin(selected_continents)]
            text = [
                f"Страна: {filtered_df['Country Name'][i]}<br>" \
                f"Население: {filtered_df[f'{selected_year}_population'][i] / 10e2:.{1}f} млн<br>" \
                f"Континент: {filtered_df['Continent'][i]}"
                for i in filtered_df['Country Name'].index]

            return show_map(selected_year, filtered_df['Country Name'], filtered_df['Country Code'],
                            filtered_df[selected_year], text, view_mode)
        else:
            # Группировка по континентам и расчет процентной безработицы
            merged_df['Unemployment_Count'] = merged_df[selected_year] * merged_df[f'{selected_year}_population'] / 100
            continent_df = merged_df.groupby('Continent').agg(
                Total_Unemployment=pd.NamedAgg(column='Unemployment_Count', aggfunc='sum'),
                Total_Population=pd.NamedAgg(column=f'{selected_year}_population', aggfunc='sum')
            ).reset_index()
            continent_df['Unemployment_Rate'] = round(
                (continent_df['Total_Unemployment'] / continent_df['Total_Population']) * 100, 2)

            # Дублирование данных континентов для каждой страны в них
            continent_countries = merged_df[['Continent', 'Country Code', 'Country Name', selected_year,
                                             f'{selected_year}_population']].drop_duplicates()
            continent_df = pd.merge(continent_countries, continent_df, on='Continent')

            text = [
                f"Страна: {continent_df['Country Name'][i]}<br>" \
                f"Локальная безработица: {continent_df[selected_year][i]}%<br>" \
                f"Население страны: {continent_df[f'{selected_year}_population'][i] / 10e2:.{1}f} млн<br>"
                f"Континент: {continent_df['Continent'][i]}<br>" \
                f"Население континента: {continent_df['Total_Population'][i] / 10e2:.{1}f} млн<br>" \
                for i in continent_df['Country Name'].index]
            return show_map(selected_year, continent_df['Continent'].unique(), continent_df['Country Code'],
                            continent_df['Unemployment_Rate'], text, view_mode)

    def show_map(selected_year, country_column, location_column, coloring_column, text_column, view_mode):

        fig = go.Figure(data=go.Choropleth(
            locations=location_column,
            z=coloring_column,
            text=text_column,
            hoverinfo='location+text',
            colorscale='plasma',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_ticksuffix='%',
            colorbar_title='Процент <br>безработицы %',
        ))

        fig.update_geos(
            visible=True,
            projection=dict(
                type='conic conformal',
                parallels=[0, 0],
                rotation={'lat': 15, 'lon': 0},
                scale=2 if view_mode == 'countries' else 0.7,
            ),
            lonaxis={'range': [30, 180]},
            lataxis={'range': [15, 75]}
        )

        if view_mode == 'countries':
            fig.add_trace(go.Scattergeo(
                locations=location_column,
                mode='text',
                hoverinfo='skip',
                text=['{}<br>{}%'.format(k, v) for k, v in zip(country_column, coloring_column)],
                textfont={'color': 'black'},
                hoverlabel=dict(namelength=0),
                name='',
            ))
        else:
            fig.add_trace(go.Scattergeo(
                lon=[continents_coordinates[continent][1] for continent in country_column],
                lat=[continents_coordinates[continent][0] for continent in country_column],
                mode='text',
                hoverinfo='skip',
                text=['{}<br>{}%'.format(k, v) for k, v in zip(country_column, coloring_column)],
                textfont={'size': 18, 'color': 'black'},
                hoverlabel=dict(namelength=0),
                name='',
            ))

        fig.update_layout(
            title_text=f'Уровень безработицы в {selected_year} году',
            width=1380,
            height=720,
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            annotations=[dict(
                x=0.5,
                y=-0.05,
                xref='paper',
                yref='paper',
                text='Source: <a href="https://www.kaggle.com/datasets/pantanjali/unemployment-dataset">Country\'s '
                     'unemployment rate from past 31 years</a>',
                showarrow=False
            )],
        )

        return fig
