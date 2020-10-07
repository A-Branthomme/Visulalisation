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
os.chdir("/Users/francoishervier/Documents/GitHub/Visulalisation/Projet web/Data Paris/Stations")
df_metro = pd.DataFrame(pd.read_excel('stations_data_clean.xlsx'))
os.chdir("/Users/francoishervier/Documents/GitHub/Visulalisation/Projet web/Data Paris/Appartements")
df_apts = pd.DataFrame(pd.read_csv('2014.csv', delimiter=',', dtype = str))

# calcul pour chaque appartement de la station la plus proche
apts = df_apts.to_numpy()
metros = df_metro.to_numpy()
apts = apts[:,[23,24]]
metros = metros[:,[1,0]]
test = cdist(metros, apts, metric='euclidean')
test = test[0:1000,0:1000]