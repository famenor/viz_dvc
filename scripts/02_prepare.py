import pandas as pd
import numpy as np
import csv


casos = pd.read_csv('data/processed/casos_covid.csv')
casos['fecha'] = pd.to_datetime(casos['fecha'], format='%Y-%m-%d')

casos['anio_semana'] = casos['fecha'].dt.strftime('%G-%V')
casos['conteo'] = 1

print('\n')
print(casos.head(3))


grupo = casos.groupby(by=['estado', 'anio_semana'], as_index=False).agg({'confirmados': 'sum',
                                                                         'negativos': 'sum',
                                                                         'defunciones': 'sum',
                                                                         'conteo': 'sum'})
grupo['confirmados'] = grupo['confirmados'] * (7 / grupo['conteo']) 
grupo['negativos'] = grupo['negativos'] * (7 / grupo['conteo']) 
grupo['defunciones'] = grupo['defunciones'] * (7 / grupo['conteo']) 
grupo = grupo.drop(columns='conteo')

print('\n')
print(grupo.head(3))

grupo.to_csv('data/processed/covid_prepared.csv', index=False)
print('\n')
print('Proceso de preparación terminado')