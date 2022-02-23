import pandas as pd
import numpy as np
import csv


casos = pd.read_csv('data/processed/covid_prepared.csv')
print(casos.head(3))


semanas = casos[['anio_semana']].drop_duplicates().sort_values(by='anio_semana', ascending=False)

semana_base = semanas['anio_semana'].values[0]
semana_ref = semanas['anio_semana'].values[2]

print('\n')
print('Semana base:', semana_base)
print('Semana referencia:', semana_ref)


base = casos[['estado', 'confirmados']].loc[casos['anio_semana'] == semana_base].copy()
referencia = casos[['estado', 'confirmados']].loc[casos['anio_semana'] == semana_ref].copy()

union = base.merge(referencia, how='inner', on='estado')
union.columns = ['estado', 'confirmados_base', 'confirmados_ref']
union['resultado'] = 'B'
union.loc[union['confirmados_base'] >= union['confirmados_ref'], 'resultado'] = 'A'

print(union.head(32))


union.to_csv('data/processed/covid_trend.csv', index=False)
print('\n')
print('Proceso de generación de tendencias terminado')