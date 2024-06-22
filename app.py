from dash import Dash, html, dash_table
import pandas as pd

df = pd.read_csv("unemployment_analysis.csv", sep=',')


app = Dash(__name__)
app.layout = html.Div([
    html.H1(children='Мое первое приложение с данными'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

if __name__ == '__main__':
    app.run_server(debug=True)