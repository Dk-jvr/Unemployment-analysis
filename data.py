import pandas as pd

df = pd.read_csv('unemployment_analysis.csv', sep=',')
all_countries = df['Country Name'].unique()
print(all_countries)