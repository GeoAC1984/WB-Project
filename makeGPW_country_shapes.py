# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:43:37 2017

@author: AClark
"""

import pandas as pd
import geopandas as gpd
import os

path_out=r'T:\WorldBankProject\HistoricPop\GPW_by_country'
grids=r'T:\WorldBankProject\HistoricPop_points\All_countries_grids'

all_countries=gpd.read_file(r'T:\WorldBankProject\HistoricPop\GPWCountries.shp')

clip_by=[c[0:3] for c in os.listdir(grids) if c.endswith('.shp')]
for iso in clip_by:
    if iso in all_countries.ISO3V10.tolist():
        one_country=all_countries[all_countries.ISO3V10==iso]
        one_country.to_file(os.path.join(path_out,'{}.shp'.format(iso)))
        print ('done', iso)