import pandas as pd
import numpy as np
import csv

import json


trend = pd.read_csv('../data/processed/covid_trend.csv')
print(trend.head(3))

resultados = trend.groupby(by='resultado', as_index=False).agg({'estado': 'count'})
print(resultados.head(3))


results = {}
results['Alza'] = 0
results['Baja'] = 0

for index, row in resultados.iterrows():
    if row['resultado'] == 'A':
        results['Alza'] = row['estado']
    elif row['resultado'] == 'B':
        results['Baja'] = row['estado']
        
print(results)


with open('../data/processed/metrics/results.json', 'w') as outfile:
    print('Test')
    json.dump(results, outfile)
    
print('File processed')