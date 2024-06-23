from dash import dcc, html, Input, Output, State, ALL, callback_context
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

df = pd.read_csv("unemployment_analysis.csv", sep=',')

lon_lat = pd.read_csv("countries_coordinates.csv", sep=',')
lon_lat = lon_lat.drop_duplicates(subset=['country_iso3'], keep='first')

lon_lat = lon_lat[lon_lat['country_iso3'].isin(df['Country Code'])]

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
            filtered_df = df.copy()
            if selected_continents:
                filtered_df = df[df['Continent'].isin(selected_continents)]
            text = [
                f"Страна: {filtered_df['Country Name'][i]}<br>" \
                f"Население: {filtered_df['Population'][i] / 10e5:.{1}f} млн<br>" \
                f"Континент: {filtered_df['Continent'][i]}"
                for i in filtered_df['Country Name'].index]

            return show_map(selected_year, filtered_df['Country Code'], filtered_df[selected_year], text)
        else:
            # Группировка по континентам и расчет процентной безработицы
            df['Unemployment_Count'] = (df[selected_year] * df['Population'] / 100).astype(int)
            continent_df = df.groupby('Continent').agg(
                Total_Unemployment=pd.NamedAgg(column='Unemployment_Count', aggfunc='sum'),
                Total_Population=pd.NamedAgg(column='Population', aggfunc='sum')
            ).reset_index()
            continent_df['Unemployment_Rate'] = round((continent_df['Total_Unemployment'] / continent_df['Total_Population']) * 100, 2)

            # Дублирование данных континентов для каждой страны в них
            continent_countries = df[['Continent', 'Country Code', 'Country Name']].drop_duplicates()
            continent_df = pd.merge(continent_countries, continent_df, on='Continent')

            text = [
                f"Страна: {continent_df['Country Name'][i]}<br>" \
                f"Население континента: {continent_df['Total_Population'][i] / 10e5:.{1}f} млн<br>" \
                f"Континент: {continent_df['Continent'][i]} index{i}"
                for i in continent_df['Country Name'].index]
            return show_map(selected_year, continent_df['Country Code'], continent_df['Unemployment_Rate'], text)

    def show_map(selected_year, location_column, coloring_column, text_column):

        fig = go.Figure(data=go.Choropleth(
            locations=location_column,
            z=coloring_column,
            text=text_column,
            colorscale='plasma',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_ticksuffix='%',
            colorbar_title='Процент <br>безработицы %',
        ))

        '''fig.update_geos(
            visible=True,
            projection=dict(
                type='conic conformal',
                parallels=[12.472944444, 35.172805555556],
                rotation={'lat': 24, 'lon': 80}
            ),
            lonaxis={'range': [68, 98]},
            lataxis={'range': [6, 38]}
        )'''

        fig.add_trace(go.Scattergeo(
            lon=lon_lat['Longitude'],
            lat=lon_lat['Latitude'],
            mode='text',
            # text=df['ST_NM'].str.title(),
            text=lon_lat['Country'],
            textfont={'color': 'Gray'},
            name='',
        ))

        '''fig.add_scattergeo(
            lon=lon_lat['Longitude'],
            lat=lon_lat['Latitude'],
            locations=lon_lat['Country'],
            featureidkey='properties.name',
            text=lon_lat['Country'],
            mode='text',
        )
        fig.update_geos(fitbounds='locations')'''
        fig.update_layout(
            title_text=f'Уровень безработицы в {selected_year} году',
            width=1280,
            height=720,
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            annotations=[dict(
                x=0.5,
                y=0,
                xref='paper',
                yref='paper',
                text='Source: TODO', #<a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                    #CIA World Factbook</a>',
                showarrow=False
            )]
        )

        return fig