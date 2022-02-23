import pandas as pd
import numpy as np
import csv

from datetime import datetime, timedelta


confirmados = pd.read_csv('data/inputs/Casos_Diarios_Estado_Nacional_Confirmados.csv')
confirmados = pd.melt(confirmados, id_vars=['cve_ent', 'poblacion', 'nombre'], var_name='fecha', value_name='confirmados')
confirmados['fecha'] = pd.to_datetime(confirmados['fecha'], format='%d-%m-%Y')
confirmados = confirmados.drop(columns=['poblacion'])

print(confirmados.head(3))
print('\n')


defunciones = pd.read_csv('data/inputs/Casos_Diarios_Estado_Nacional_Defunciones.csv')
defunciones = pd.melt(defunciones, id_vars=['cve_ent', 'poblacion', 'nombre'], var_name='fecha', value_name='defunciones')
defunciones['fecha'] = pd.to_datetime(defunciones['fecha'], format='%d-%m-%Y')
defunciones = defunciones.drop(columns=['poblacion'])

print(defunciones.head(3))
print('\n')


negativos = pd.read_csv('data/inputs/Casos_Diarios_Estado_Nacional_Negativos.csv')
negativos = pd.melt(negativos, id_vars=['cve_ent', 'poblacion', 'nombre'], var_name='fecha', value_name='negativos')
negativos['fecha'] = pd.to_datetime(negativos['fecha'], format='%d-%m-%Y')
negativos = negativos.drop(columns=['poblacion'])

print(negativos.head(3))
print('\n')

consolidado = confirmados.merge(negativos, how='outer', on=['cve_ent', 'nombre', 'fecha'])
consolidado = consolidado.merge(defunciones, how='outer', on=['cve_ent', 'nombre', 'fecha'])
consolidado['confirmados'] = consolidado['confirmados'].fillna(0)
consolidado['negativos'] = consolidado['negativos'].fillna(0)
consolidado['defunciones'] = consolidado['defunciones'].fillna(0)

consolidado['casos'] = consolidado['confirmados'] + consolidado['defunciones']
consolidado = consolidado.loc[consolidado['cve_ent'] != 0]
consolidado['pais'] = 'MEXICO'

consolidado = consolidado[['pais', 'nombre', 'fecha', 'confirmados', 'negativos', 'casos', 'defunciones']]
consolidado = consolidado.rename(columns={'nombre': 'estado'})

fecha_max = consolidado['fecha'].max()
fecha_estable = fecha_max + timedelta(days = -7)

print('Fecha máxima original:', fecha_max)
consolidado = consolidado.loc[consolidado['fecha'] <= fecha_estable]
print('Fecha de corte establecida:', consolidado['fecha'].max())

consolidado['ola'] = 'ola_1'
consolidado.loc[consolidado['fecha'] >= '2020-11-01', 'ola'] = 'ola_2'  
consolidado.loc[consolidado['fecha'] >= '2021-06-01', 'ola'] = 'ola_3'
consolidado.loc[consolidado['fecha'] >= '2021-12-01', 'ola'] = 'ola_4' 

consolidado = consolidado.sort_values(by=['pais', 'estado', 'fecha'])

print('\n')
print(consolidado.head(3))

consolidado.to_csv('data/processed/casos_covid.csv', index=False)

print('\n')
print('Proceso de extracción terminado')
