#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:10:05 2020

@author: francoishervier
"""

import os, csv
import pandas as pd
import numpy as np
import math
from scipy.spatial.distance import cdist

# Load data
# dir_path = os.path.dirname(os.path.abspath(__file__))
dir_path = "/Users/francoishervier/Documents/GitHub/Visulalisation/Projet web/humanresources/humanresources"
os.chdir(dir_path + "/Data Paris/Appartements")
df_apts = pd.DataFrame(pd.read_csv('Data_appartements_reprojete.csv', delimiter=',', dtype = str))
os.chdir(dir_path + "/Data Paris/Stations")
df_metro = pd.DataFrame(pd.read_excel('stations_data_clean.xlsx'))
df_lignes_metro = pd.DataFrame(pd.read_csv('Data_lignes_metro.csv', delimiter=';', dtype = str))

# Petites manipulations de la db
df_apts["annee"]=df_apts.id_mutation.str.split('-')
df_apts["annee"]=df_apts.id_mutation.str.split('-',expand=True)
df_apts.valeur_fonciere_vraie = df_apts.valeur_fonciere_vraie.str.replace(",", ".")
df_apts = df_apts.astype({'longitude': float, 'latitude': float, 'surface_reelle_bati': float, 'valeur_fonciere_vraie': float})

# calcul des prix au m2
df_apts["Prix_m2"]= df_apts.valeur_fonciere_vraie / df_apts.surface_reelle_bati
#df_apts.to_csv('Data_apts_avec_prix.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')

# nettoyage des bases
df_apts=df_apts[df_apts["Prix_m2"] > 1000]
df_apts=df_apts[df_apts["Prix_m2"] < 60000]
df_lignes_metro = df_lignes_metro.sort_values(by=['Station'],axis=0)
df_lignes_metro = df_lignes_metro[['Station','Correspondance_1','Correspondance_2','Correspondance_3','Correspondance_4','Correspondance_5', 'Trafic']]

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

# Création d'une nouvelle dbase regroupé par station de métro
df_station_groupees_x = df_resultats.groupby("nomlong")["x"].mean().to_frame('x').reset_index().drop(columns={'nomlong'})
df_station_groupees_y = df_resultats.groupby("nomlong")["y"].mean().to_frame('y').reset_index().drop(columns={'nomlong'})
df_station_groupees_global = df_resultats.groupby("nomlong")["prix_moyen_global"].mean().to_frame('prix_moyen_global').reset_index()
df_station_groupees_2014 = df_resultats.groupby("nomlong")["prix_moyen_2014"].mean().to_frame('prix_moyen_2014').reset_index()
df_station_groupees_2015 = df_resultats.groupby("nomlong")["prix_moyen_2015"].mean().to_frame('prix_moyen_2015').reset_index()
df_station_groupees_2016 = df_resultats.groupby("nomlong")["prix_moyen_2016"].mean().to_frame('prix_moyen_2016').reset_index()
df_station_groupees_2017 = df_resultats.groupby("nomlong")["prix_moyen_2017"].mean().to_frame('prix_moyen_2017').reset_index()
df_station_groupees_2018 = df_resultats.groupby("nomlong")["prix_moyen_2018"].mean().to_frame('prix_moyen_2018').reset_index()
df_station_groupees_2019 = df_resultats.groupby("nomlong")["prix_moyen_2019"].mean().to_frame('prix_moyen_2019').reset_index()
df_station_groupees = pd.concat([df_station_groupees_x, df_station_groupees_y, df_station_groupees_2014,df_station_groupees_2015.prix_moyen_2015,df_station_groupees_2016.prix_moyen_2016,df_station_groupees_2017.prix_moyen_2017,df_station_groupees_2018.prix_moyen_2018, df_station_groupees_2019.prix_moyen_2019,df_station_groupees_global.prix_moyen_global], axis=1)
df_station_groupees = df_station_groupees.rename(columns={'nomlong':'Station'})

# réassociation des lignes de métro aux stations de métro + Création d'une base de donnée Lignes
df_station_groupees = pd.merge(df_station_groupees, df_lignes_metro, how = 'left', on = "Station")
df_station_groupees["nb_lignes"]=5
df_station_groupees["nb_lignes"][df_station_groupees["Correspondance_5"].isnull()==True]=4
df_station_groupees["nb_lignes"][df_station_groupees["Correspondance_4"].isnull()==True]=3
df_station_groupees["nb_lignes"][df_station_groupees["Correspondance_3"].isnull()==True]=2
df_station_groupees["nb_lignes"][df_station_groupees["Correspondance_2"].isnull()==True]=1

# Création de la DB BartChart
## 2014
df_resultats_2014 = pd.concat([df_metro,df_prix_2014], axis=1)
df_resultats_2014["annee"]=2014
df_resultats_2014 = df_resultats_2014.rename(columns={'prix_moyen_2014':'prix_moyen'})
df_resultats_prix_2014 = df_resultats_2014.groupby("nomlong")["prix_moyen"].mean().to_frame('prix_moyen').reset_index().drop(columns={'nomlong'})
df_resultats_annee_2014 = df_resultats_2014.groupby("nomlong")["annee"].mean().to_frame('annee').reset_index()
df_resultats_groupes_2014 = pd.concat([df_resultats_annee_2014, df_resultats_prix_2014], axis=1)
df_resultats_groupes_2014 = df_resultats_groupes_2014[df_resultats_groupes_2014["prix_moyen"] > 0]
df_resultats_groupes_2014 = df_resultats_groupes_2014.rename(columns={'nomlong':'Station'})
df_resultats_groupes_2014 = pd.merge(df_resultats_groupes_2014, df_lignes_metro, how = 'left', on = "Station")
df_resultats_groupes_2014["nb_lignes"]=5
df_resultats_groupes_2014["nb_lignes"][df_resultats_groupes_2014["Correspondance_5"].isnull()==True]=4
df_resultats_groupes_2014["nb_lignes"][df_resultats_groupes_2014["Correspondance_4"].isnull()==True]=3
df_resultats_groupes_2014["nb_lignes"][df_resultats_groupes_2014["Correspondance_3"].isnull()==True]=2
df_resultats_groupes_2014["nb_lignes"][df_resultats_groupes_2014["Correspondance_2"].isnull()==True]=1

## 2015
df_resultats_2015 = pd.concat([df_metro,df_prix_2015], axis=1)
df_resultats_2015["annee"]=2015
df_resultats_2015 = df_resultats_2015.rename(columns={'prix_moyen_2015':'prix_moyen'})
df_resultats_prix_2015 = df_resultats_2015.groupby("nomlong")["prix_moyen"].mean().to_frame('prix_moyen').reset_index().drop(columns={'nomlong'})
df_resultats_annee_2015 = df_resultats_2015.groupby("nomlong")["annee"].mean().to_frame('annee').reset_index()
df_resultats_groupes_2015 = pd.concat([df_resultats_annee_2015, df_resultats_prix_2015], axis=1)
df_resultats_groupes_2015 = df_resultats_groupes_2015[df_resultats_groupes_2015["prix_moyen"] > 0]
df_resultats_groupes_2015 = df_resultats_groupes_2015.rename(columns={'nomlong':'Station'})
df_resultats_groupes_2015 = pd.merge(df_resultats_groupes_2015, df_lignes_metro, how = 'left', on = "Station")
df_resultats_groupes_2015["nb_lignes"]=5
df_resultats_groupes_2015["nb_lignes"][df_resultats_groupes_2015["Correspondance_5"].isnull()==True]=4
df_resultats_groupes_2015["nb_lignes"][df_resultats_groupes_2015["Correspondance_4"].isnull()==True]=3
df_resultats_groupes_2015["nb_lignes"][df_resultats_groupes_2015["Correspondance_3"].isnull()==True]=2
df_resultats_groupes_2015["nb_lignes"][df_resultats_groupes_2015["Correspondance_2"].isnull()==True]=1

## 2016
df_resultats_2016 = pd.concat([df_metro,df_prix_2016], axis=1)
df_resultats_2016["annee"]=2016
df_resultats_2016 = df_resultats_2016.rename(columns={'prix_moyen_2016':'prix_moyen'})
df_resultats_prix_2016 = df_resultats_2016.groupby("nomlong")["prix_moyen"].mean().to_frame('prix_moyen').reset_index().drop(columns={'nomlong'})
df_resultats_annee_2016 = df_resultats_2016.groupby("nomlong")["annee"].mean().to_frame('annee').reset_index()
df_resultats_groupes_2016 = pd.concat([df_resultats_annee_2016, df_resultats_prix_2016], axis=1)
df_resultats_groupes_2016 = df_resultats_groupes_2016[df_resultats_groupes_2016["prix_moyen"] > 0]
df_resultats_groupes_2016 = df_resultats_groupes_2016.rename(columns={'nomlong':'Station'})
df_resultats_groupes_2016 = pd.merge(df_resultats_groupes_2016, df_lignes_metro, how = 'left', on = "Station")
df_resultats_groupes_2016["nb_lignes"]=5
df_resultats_groupes_2016["nb_lignes"][df_resultats_groupes_2016["Correspondance_5"].isnull()==True]=4
df_resultats_groupes_2016["nb_lignes"][df_resultats_groupes_2016["Correspondance_4"].isnull()==True]=3
df_resultats_groupes_2016["nb_lignes"][df_resultats_groupes_2016["Correspondance_3"].isnull()==True]=2
df_resultats_groupes_2016["nb_lignes"][df_resultats_groupes_2016["Correspondance_2"].isnull()==True]=1
df_resultats_groupes_2016 = df_resultats_groupes_2016[df_resultats_groupes_2016["Station"] != "PORTE D'IVRY"]

## 2017
df_resultats_2017 = pd.concat([df_metro,df_prix_2017], axis=1)
df_resultats_2017["annee"]=2017
df_resultats_2017 = df_resultats_2017.rename(columns={'prix_moyen_2017':'prix_moyen'})
df_resultats_prix_2017 = df_resultats_2017.groupby("nomlong")["prix_moyen"].mean().to_frame('prix_moyen').reset_index().drop(columns={'nomlong'})
df_resultats_annee_2017 = df_resultats_2017.groupby("nomlong")["annee"].mean().to_frame('annee').reset_index()
df_resultats_groupes_2017 = pd.concat([df_resultats_annee_2017, df_resultats_prix_2017], axis=1)
df_resultats_groupes_2017 = df_resultats_groupes_2017[df_resultats_groupes_2017["prix_moyen"] > 0]
df_resultats_groupes_2017 = df_resultats_groupes_2017.rename(columns={'nomlong':'Station'})
df_resultats_groupes_2017 = pd.merge(df_resultats_groupes_2017, df_lignes_metro, how = 'left', on = "Station")
df_resultats_groupes_2017["nb_lignes"]=5
df_resultats_groupes_2017["nb_lignes"][df_resultats_groupes_2017["Correspondance_5"].isnull()==True]=4
df_resultats_groupes_2017["nb_lignes"][df_resultats_groupes_2017["Correspondance_4"].isnull()==True]=3
df_resultats_groupes_2017["nb_lignes"][df_resultats_groupes_2017["Correspondance_3"].isnull()==True]=2
df_resultats_groupes_2017["nb_lignes"][df_resultats_groupes_2017["Correspondance_2"].isnull()==True]=1

## 2018
df_resultats_2018 = pd.concat([df_metro,df_prix_2018], axis=1)
df_resultats_2018["annee"]=2018
df_resultats_2018 = df_resultats_2018.rename(columns={'prix_moyen_2018':'prix_moyen'})
df_resultats_prix_2018 = df_resultats_2018.groupby("nomlong")["prix_moyen"].mean().to_frame('prix_moyen').reset_index().drop(columns={'nomlong'})
df_resultats_annee_2018 = df_resultats_2018.groupby("nomlong")["annee"].mean().to_frame('annee').reset_index()
df_resultats_groupes_2018 = pd.concat([df_resultats_annee_2018, df_resultats_prix_2018], axis=1)
df_resultats_groupes_2018 = df_resultats_groupes_2018[df_resultats_groupes_2018["prix_moyen"] > 0]
df_resultats_groupes_2018 = df_resultats_groupes_2018.rename(columns={'nomlong':'Station'})
df_resultats_groupes_2018 = pd.merge(df_resultats_groupes_2018, df_lignes_metro, how = 'left', on = "Station")
df_resultats_groupes_2018["nb_lignes"]=5
df_resultats_groupes_2018["nb_lignes"][df_resultats_groupes_2018["Correspondance_5"].isnull()==True]=4
df_resultats_groupes_2018["nb_lignes"][df_resultats_groupes_2018["Correspondance_4"].isnull()==True]=3
df_resultats_groupes_2018["nb_lignes"][df_resultats_groupes_2018["Correspondance_3"].isnull()==True]=2
df_resultats_groupes_2018["nb_lignes"][df_resultats_groupes_2018["Correspondance_2"].isnull()==True]=1

## 2019
df_resultats_2019 = pd.concat([df_metro,df_prix_2019], axis=1)
df_resultats_2019["annee"]=2019
df_resultats_2019 = df_resultats_2019.rename(columns={'prix_moyen_2019':'prix_moyen'})
df_resultats_prix_2019 = df_resultats_2019.groupby("nomlong")["prix_moyen"].mean().to_frame('prix_moyen').reset_index().drop(columns={'nomlong'})
df_resultats_annee_2019 = df_resultats_2019.groupby("nomlong")["annee"].mean().to_frame('annee').reset_index()
df_resultats_groupes_2019 = pd.concat([df_resultats_annee_2019, df_resultats_prix_2019], axis=1)
df_resultats_groupes_2019 = df_resultats_groupes_2019[df_resultats_groupes_2019["prix_moyen"] > 0]
df_resultats_groupes_2019 = df_resultats_groupes_2019.rename(columns={'nomlong':'Station'})
df_resultats_groupes_2019 = pd.merge(df_resultats_groupes_2019, df_lignes_metro, how = 'left', on = "Station")
df_resultats_groupes_2019["nb_lignes"]=5
df_resultats_groupes_2019["nb_lignes"][df_resultats_groupes_2019["Correspondance_5"].isnull()==True]=4
df_resultats_groupes_2019["nb_lignes"][df_resultats_groupes_2019["Correspondance_4"].isnull()==True]=3
df_resultats_groupes_2019["nb_lignes"][df_resultats_groupes_2019["Correspondance_3"].isnull()==True]=2
df_resultats_groupes_2019["nb_lignes"][df_resultats_groupes_2019["Correspondance_2"].isnull()==True]=1

df_bartchart = pd.concat([df_resultats_groupes_2014,df_resultats_groupes_2015,df_resultats_groupes_2016,df_resultats_groupes_2017,df_resultats_groupes_2018,df_resultats_groupes_2019], axis=0)
df_bartchart["annee_temp"]=df_bartchart["annee"].astype({'annee': str})
df_bartchart["annee_date"]=df_bartchart["annee_temp"] + "-01-01"
df_bartchart=df_bartchart.drop(columns={'annee_temp'})
df_bartchart = df_bartchart.astype({'annee': int, 'prix_moyen': int})

# Filtrage de données abérantes
df_bartchart = df_bartchart[df_bartchart["Station"] != "PIERRE CURIE"]
df_station_groupees = df_station_groupees[df_station_groupees["Station"] != "PIERRE CURIE"]
df_resultats = df_resultats[df_resultats["nomlong"] != "PIERRE CURIE"]

# sauvegarde des db
df_resultats.to_csv('Data_metro_avec_prix.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')
df_station_groupees.to_csv('Data_stations_groupees_avec_prix.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')
df_bartchart.to_csv('Data_bartchart.csv', sep=',', encoding = "utf-8-sig", index = False, decimal = '.', quoting=csv.QUOTE_ALL, quotechar= ' ')

#test

#df_resultats = df_resultats[0:1000]
#df_save = pd.DataFrame(distances)
#df_save.to_csv('distances.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')

