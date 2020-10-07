#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:10:05 2020

@author: francoishervier
"""

import os, csv
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

# Load data
os.chdir("./Data Paris/Appartements")
df_apts = pd.DataFrame(pd.read_csv('Data_appartements_reprojete.csv', delimiter=',', dtype = str))
os.chdir("./Data Paris/Stations")
df_metro = pd.DataFrame(pd.read_excel('stations_data_clean.xlsx'))
df_apts["annee"]=df_apts.id_mutation.str.split('-')
df_apts["annee"]=df_apts.id_mutation.str.split('-',expand=True)
df_apts.valeur_fonciere_vraie = df_apts.valeur_fonciere_vraie.str.replace(",", ".")
df_apts = df_apts.astype({'longitude': float, 'latitude': float, 'surface_reelle_bati': float, 'valeur_fonciere_vraie': float})

# calcul des prix au m2
df_apts["Prix_m2"]= df_apts.valeur_fonciere_vraie / df_apts.surface_reelle_bati
df_apts.to_csv('Data_apts_avec_prix.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')

# nettoyage de la base
df_apts=df_apts[df_apts["Prix_m2"] > 1000]
df_apts=df_apts[df_apts["Prix_m2"] < 60000]

# transformation de la DB en tableaux numpy
apts = df_apts.to_numpy()
df_metro = df_metro.sort_values(by=['gares_id'],axis=0)
df_metro = df_metro.reset_index()
metros = df_metro.to_numpy()
metros_coord = metros[:,[7,8]]
apts_coord = apts[:,[28,29]]
apts_prix = apts[:,[31]]
apts_annee = apts[:,[30]]
            
# detection pour chaque station des appartements les plus proches (dans un rayon de dist_mean entre 2 stations)
dist_mean = 571
mat_distances = cdist(apts_coord, metros_coord, metric='euclidean')
mat_prix = np.nan * mat_distances
for i in range(len(mat_distances)): #par appartement
    for j in range(len(mat_distances[0])): #par station
        if mat_distances[i,j] < dist_mean: #si l'appartement se trouve à - de dist_mean, on rempli la matrice de prix avec le prix/m2 de l'apt
            mat_prix[i,j] = apts_prix[i]
        else:
            mat_distances[i,j] = np.nan
        
# On repasse le calcul dans une Database et on réassocie les années aux appartements    
df_mat_prix = pd.DataFrame(mat_prix)
df_apts_annee = pd.DataFrame(apts_annee).rename(columns={0:'annee'})
df_mat_prix = pd.concat([df_mat_prix,df_apts_annee], axis=1)

# Calcul des moyennes de prix par station de métro et par année  
df_prix_2014 = df_mat_prix[df_mat_prix["annee"] == '2014'].mean().to_frame().rename(columns={0:'prix_moyen_2014'})
df_prix_2015 = df_mat_prix[df_mat_prix["annee"] == '2015'].mean().to_frame().rename(columns={0:'prix_moyen_2015'})
df_prix_2016 = df_mat_prix[df_mat_prix["annee"] == '2016'].mean().to_frame().rename(columns={0:'prix_moyen_2016'})
df_prix_2017 = df_mat_prix[df_mat_prix["annee"] == '2017'].mean().to_frame().rename(columns={0:'prix_moyen_2017'})
df_prix_2018 = df_mat_prix[df_mat_prix["annee"] == '2018'].mean().to_frame().rename(columns={0:'prix_moyen_2018'})
df_prix_2019 = df_mat_prix[df_mat_prix["annee"] == '2019'].mean().to_frame().rename(columns={0:'prix_moyen_2019'})
df_prix_moyen = (df_prix_2014.prix_moyen_2014 + df_prix_2015.prix_moyen_2015 + df_prix_2016.prix_moyen_2016 + df_prix_2017.prix_moyen_2017 + df_prix_2018.prix_moyen_2018 + df_prix_2019.prix_moyen_2019) / 6
df_prix_moyen = df_prix_moyen.to_frame().rename(columns={0:'prix_moyen_global'})

# Re-concaténation des matrices de prix avec la matrice métro initiale
df_resultats = pd.concat([df_metro,df_prix_2014,df_prix_2015,df_prix_2016,df_prix_2017,df_prix_2018,df_prix_2019, df_prix_moyen], axis=1)
df_resultats = df_resultats[df_resultats["prix_moyen_global"] > 0]

# Création d'une base regroupé par station de métro
df_station_groupees_global=df_resultats.groupby("nomlong")["prix_moyen_global"].mean().to_frame('prix_moyen_global').reset_index()
df_station_groupees_2014=df_resultats.groupby("nomlong")["prix_moyen_2014"].mean().to_frame('prix_moyen_2014').reset_index()
df_station_groupees_2015=df_resultats.groupby("nomlong")["prix_moyen_2015"].mean().to_frame('prix_moyen_2015').reset_index()
df_station_groupees_2016=df_resultats.groupby("nomlong")["prix_moyen_2016"].mean().to_frame('prix_moyen_2016').reset_index()
df_station_groupees_2017=df_resultats.groupby("nomlong")["prix_moyen_2017"].mean().to_frame('prix_moyen_2017').reset_index()
df_station_groupees_2018=df_resultats.groupby("nomlong")["prix_moyen_2018"].mean().to_frame('prix_moyen_2018').reset_index()
df_station_groupees_2019=df_resultats.groupby("nomlong")["prix_moyen_2019"].mean().to_frame('prix_moyen_2019').reset_index()
df_station_groupees = pd.concat([df_station_groupees_2014,df_station_groupees_2015.prix_moyen_2015,df_station_groupees_2016.prix_moyen_2016,df_station_groupees_2017.prix_moyen_2017,df_station_groupees_2018.prix_moyen_2018, df_station_groupees_2019.prix_moyen_2019,df_station_groupees_global.prix_moyen_global], axis=1)

# sauvegarde des db
df_resultats.to_csv('Data_metro_avec_prix.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')
df_station_groupees.to_csv('Data_stations_groupees_avec_prix.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')


#test

#df_resultats = df_resultats[0:1000]
#df_save = pd.DataFrame(distances)
#df_save.to_csv('distances.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')

