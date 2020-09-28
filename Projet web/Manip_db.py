# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os, csv
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

# Load data
os.chdir("/Users/francoishervier/Documents/GitHub/Visulalisation/Projet web/Data Paris/Stations")
df_metro = pd.DataFrame(pd.read_excel('stations_data_clean.xlsx'))
os.chdir("/Users/francoishervier/Documents/GitHub/Visulalisation/Projet web/Data Paris/Appartements")
df_Apts_2014 = pd.DataFrame(pd.read_csv('2014.csv', delimiter=',', dtype = str))
df_Apts_2015 = pd.DataFrame(pd.read_csv('2015.csv', delimiter=',', dtype = str))
df_Apts_2016 = pd.DataFrame(pd.read_csv('2016.csv', delimiter=',', dtype = str))
df_Apts_2017 = pd.DataFrame(pd.read_csv('2017.csv', delimiter=',', dtype = str))
df_Apts_2018 = pd.DataFrame(pd.read_csv('2018.csv', delimiter=',', dtype = str))
df_Apts_2019 = pd.DataFrame(pd.read_csv('2019.csv', delimiter=',', dtype = str))

# creation de la table appartements
df_apts = pd.concat([df_Apts_2014,df_Apts_2015,df_Apts_2016,df_Apts_2017,df_Apts_2018,df_Apts_2019],sort=False). \
    drop(columns={'numero_disposition','adresse_code_voie','code_commune','nom_commune','code_departement','ancien_code_commune', \
                  'ancien_nom_commune','id_parcelle', 'ancien_id_parcelle', 'numero_volume', 'code_nature_culture', 'nature_culture', \
                      'code_nature_culture_speciale', 'nature_culture_speciale', 'surface_terrain'})

df_apts = df_apts.astype({'longitude': float, 'latitude': float, 'valeur_fonciere': float, 'code_type_local': float, 'surface_reelle_bati': float, \
                          'nombre_pieces_principales': float})

# filtrage sur les appartements uniquement
df_apts = df_apts[df_apts['code_type_local'] == 2]
#df_apts = df_apts[1:1000]

# creation de la colonne valeur_fonciere_vraie (pour retrouver le prix unitaire des appartements achetés en lots)
df_surface_apt_lots = df_apts.groupby('id_mutation')['surface_reelle_bati'].sum().to_frame('surface_tot_lot')
df_apts = pd.merge(df_apts, df_surface_apt_lots, how = 'left', on = "id_mutation")
df_apts["valeur_fonciere_vraie"] = df_apts.valeur_fonciere * (df_apts.surface_reelle_bati / df_apts.surface_tot_lot)

# creation d'un unique ID pour chaque appartement
df_apts["Apt_ID"] = "Apt_" + df_apts.index.astype(str)

# sauvegarde de la db
df_apts.to_csv('Data_appartements.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')
