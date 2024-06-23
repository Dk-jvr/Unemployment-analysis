from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("unemployment_analysis.csv", sep=',')

years = [str(year) for year in range(1991, 2022)]

def get_layout():
    return html.Div([
        html.H1("Карта мира по показателям безработицы"),
        
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
        Output('world-map', 'figure'),
        Input('year-dropdown', 'value')
    )
    def update_map(selected_year):
        fig = go.Figure(data=go.Choropleth(
            locations=df['Country Code'],
            z=df[selected_year],
            text=df['Country Name'],
            colorscale='plasma',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_ticksuffix='%',
            colorbar_title='Процент <br>безработицы %',
        ))

        fig.update_layout(
            title_text=f'Уровень безработицы в {selected_year} году',
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

        '''fig = px.choropleth(
            df,
            locations="Country Code",
            color=selected_year,
            hover_name="Country Name",
            hover_data={
                "Country Code": True,
                "Population": True,
                selected_year: True,
            },
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"Уровень безработицы в {selected_year} году",
            projection='equirectangular',
        )
        
        fig.update_geos(
            showcoastlines=True, coastlinecolor="Black",
            showland=True, landcolor="white",
            showocean=True, oceancolor="LightBlue"
        )'''

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
