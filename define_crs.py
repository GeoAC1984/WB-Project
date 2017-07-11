# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 23:45:40 2017

@author: AClark
"""
import pandas as pd
import geopandas as gpd
import os

path=r'T:\WorldBankProject\HistoricPop\pop_fishnets'
fishnets=[grid for grid in os.listdir(path) if grid.endswith('.shp')]
col_order=[  u'geometry', u'iso', u'urbpop2000',u'rurpop2000', u'urbpop2010', u'rurpop2010']
for shape in fishnets:
    shape_out=os.path.join(path, shape)
    gdf=gpd.read_file(os.path.join(path,shape))
    gdf=gdf[col_order]
    gdf.crs={'init': u'epsg:4326'}
    gdf.to_file(shape_out)
    print shape
