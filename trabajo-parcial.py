#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 19:53:51 2019

@author: israelyance
"""

# TRABAJO PARCIAL
##############################################


# Importar librerías
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Cargar dataset
gdp = pd.read_csv('countryGDP.csv')
fire = pd.read_csv('GlobalFirePower.csv')
happy = pd.read_csv('happy2015.csv')
lang = pd.read_csv('endangeredLang.csv')


# 1. ANALIZANDO DATA
###################################

# gdp
gdp.head(5)
gdp.info()
gdp.describe(include='all')
np.sum(gdp.isnull())

# fire
fire.head(5)
fire.info()
fire.describe(include='all')
np.sum(fire.isnull())

# happy
happy.head(5)
happy.info()
happy.describe(include='all')
np.sum(happy.isnull())

# lang
lang.head(5)
lang.info()
lang.describe(include='all')
np.sum(lang.isnull())




# 2. TRANSFORMANDO DATA
###################################


# Fire: Transformando valores object
# Analizando Coastline (km)
fire_coastline = fire['Coastline (km)'].value_counts()
fire_coastline[fire_coastline > 1]
# Asignando un nuevo valor en 'Coastline (km)'
fire.loc[fire['Coastline (km)'] == 'Landlocked', 'Coastline (km)'] = '0'
fire['Coastline (km)'] = fire['Coastline (km)'].astype(int)
# Analizando Waterways (km)
fire_waterways = fire['Waterways (km)'].value_counts()
fire_waterways[fire_waterways > 1]
# Asignando un nuevo valor en 'Waterways (km)'
fire.loc[fire['Waterways (km)'] == 'Minimum not met.', 'Waterways (km)'] = '0'
fire['Waterways (km)'] = fire['Waterways (km)'].astype(int)


# Crear nueva columna a Happy: Code
happy_code_missing = []
for i in range(0, happy.shape[0]):
    happy_country = happy.loc[i, 'Country']
    gdp_country = gdp[gdp['Country'] == happy_country]
    if gdp_country.empty:
        happy_code_missing.append([i, happy_country])
    else:
        index = gdp_country.index[0]
        happy.loc[i, 'Code'] = gdp.loc[index, 'Code']
happy_code_missing

# Asignar valores a los países faltantes
happy.loc[46, 'Code'] = 'KOR' #South Korea
#happy.loc[65, 'Code'] = '' #North Cyprus
happy.loc[68, 'Code'] = 'KOS' #Kosovo
happy.loc[71, 'Code'] = 'HKG' #Hong Kong
happy.loc[82, 'Code'] = 'MNE' #Montenegro
#happy.loc[90, 'Code'] = '' #Somaliland region
happy.loc[107, 'Code'] = 'PLE' #Palestinian Territories
happy.loc[128, 'Code'] = 'MMR' #Myanmar
happy.loc[119, 'Code'] = 'COD' #Congo (Kinshasa)
happy.loc[138, 'Code'] = 'CGO' #Congo (Brazzaville)
happy.loc[150, 'Code'] = 'CIV' #Ivory Coast


# Asignar index
# Colocamos en los dataframes el código COI como index
gdp.index = gdp['Code']
gdp.drop(columns = ['Code'], axis = 1, inplace = True)
fire.index = fire['ISO3']
fire.drop(columns = ['ISO3'], axis = 1, inplace = True)
happy.index = happy['Code']
happy.drop(columns = ['Code'], axis = 1, inplace = True)


# Analizando las correlaciones
# Correlaciones en gdp
gdp_corr = gdp.corr()
gdp_corr
# Correlaciones en fire
fire_corr = fire.corr()
fire_corr = fire_corr[(fire_corr > 0.75) | (fire_corr < -0.75)]
fire_corr
# Correlaciones en happy
happy_corr = happy.corr()
happy_corr = happy_corr[(happy_corr > 0.75) | (happy_corr < -0.75)]
happy_corr


# Eliminando data para analizar
# Basado en las correlaciones eliminamos las siguientes variables 
# Eliminando columnas en fire
fire_drop = ['Fit-for-Service', 'Reaching Military Age', 'Active Personnel',
             'Reserve Personnel', 'Labor Force', 'Purchasing Power Parity',
             'Fighter Aircraft', 'Attack Aircraft', 'Transport Aircraft',
             'Trainer Aircraft', 'Total Helicopter Strength', 'Attack Helicopters',
             'Roadway Coverage (km)', 'Railway Coverage (km)', 'Serivecable Airports',
             'Aircraft Carriers', 'Armored Fighting Vehicles', 'Destroyers',
             'Self-Propelled Artillery', 'Rocket Projectors', 'Consumption (bbl/dy)',
             'Corvettes', 'Submarines', 'Towed Artillery',
             'Defense Budget', 'External Debt', 'Patrol Craft',
             'Shared Borders (km)']
fire.drop(columns = fire_drop, axis = 1, inplace = True)
# Eliminando columnas en happy
happy_drop = ['Happiness Rank', 'Economy (GDP per Capita)']
happy.drop(columns = happy_drop, axis = 1, inplace = True)


# Concatenamos los dataframes:
gdp.columns
gdp.columns = ['Country GDP', 'Population', 'GDP per Capita']
happy.columns
happy.columns = ['Country Happy', 'Region', 'Happiness Score',
                 'Standard Error', 'Family', 'Health (Life Expectancy)',
                 'Freedom', 'Trust (Government Corruption)', 'Generosity',
                 'Dystopia Residual']
data_total = pd.concat([gdp, fire, happy], join = 'inner', axis = 1)
data_total.drop( columns = ['Country', 'Country Happy'], axis = 1, inplace = True)



# 3. VISUALIZACIÓN
###################################


# El GDP per Capita por cada Region
sns.set(style='whitegrid')
f, ax = plt.subplots(figsize=(6, 6))
sns.set_color_codes('pastel')
sns.barplot(x = 'GDP per Capita', y = 'Region', data = data_total,
            label = 'GSP', color = "b")
plt.show()


# Visualización de las principales variables 
sns.set(style="ticks",color_codes=True)
data_total_plus = data_total[['Region','Happiness Score', 'GDP per Capita',
                       'Health (Life Expectancy)', 'Trust (Government Corruption)']]
sns.pairplot(data_total_plus, hue = 'Region', palette = 'Spectral')
plt.show()


# 'GDP per Capita' vs 'Happiness Score' por Región 
sns.lmplot(x = 'GDP per Capita', y = "Happiness Score", data = data_total,
           fit_reg = False, hue = 'Country GDP', legend = False, palette = 'Paired')
plt.show()
