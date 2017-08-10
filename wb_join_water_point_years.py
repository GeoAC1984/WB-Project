# -*- coding: utf-8 -*-
"""
Created on Thur May  4 10:58:11 2017

@author: AClark
"""
import pandas as pd
import geopandas as gpd
import os

path=r'T:\WorldBankProject\Regions'
test='T:\WorldBankProject\Regions\CentralAmerica\Mexico\CountryGrids'

water=[shape for shape in os.listdir('T:\WorldBankProject\Glob_Points\WaterModels') if shape.endswith('.shp')]
need_years=[y for y in water if int(y[-8:-4])<2055]

wg_hgm26=[i for i in need_years if 'watergap_hadgem' in i and 'rcp2p6' in i]
wg_hgm85=[i for i in need_years if 'watergap_hadgem' in i and 'rcp8p5' in i]
lpjml_hgm26=[i for i in need_years if 'lpjml_hadgem' in i and 'rcp2p6' in i]
lpjml_hgm85=[i for i in need_years if 'lpjml_hadgem' in i and 'rcp8p5' in i]

wg_ipsl26=[i for i in need_years if 'watergap_ipsl' in i and 'rcp2p6' in i]
wg_ipsl85=[i for i in need_years if 'watergap_ipsl' in i and 'rcp8p5' in i]
lpjml_ipsl26=[i for i in need_years if 'lpjml_ipsl' in i and 'rcp2p6' in i]
lpjml_ipsl85=[i for i in need_years if 'lpjml_ipsl' in i and 'rcp8p5' in i]

hgms26=[wg_hgm26,lpjml_hgm26]
for hgm in hgms26:
    years=[]
    for name in hgm:
        if 'watergap' in name:
            col_name=name.split('_')[0][0]+name.split('_')[0][5]+'_'+name.split('_')[1][0]+name.split('_')[1][3]+name.split('_')[1][5]+'_'+name.split('_')[3][2:4]
        else:
            col_name=name.split('_')[0][0:3]+'_'+name.split('_')[1][0]+name.split('_')[1][3]+name.split('_')[1][5]+'_'+name.split('_')[3][2:4]
            
        points=gpd.read_file(os.path.join('T:\WorldBankProject\Glob_Points','WaterModels',name))
        points=points.rename(columns={'GRID_CODE':col_name}).drop('POINTID',1)
        years.append(points)
    aggr_y = reduce(lambda left,right: gpd.sjoin(left,right,op='intersects').drop('index_right',1), years)
    aggr_y.to_file(os.path.join('T:\WorldBankProject\Glob_Points\WaterModels_8dec',name[0:-9]+'.shp'))
    
print 'done with hgms'

hgms85=[wg_hgm85,lpjml_hgm85]
for hgm in hgms85:
    years=[]
    for name in hgm:
        if 'watergap' in name:
            col_name=name.split('_')[0][0]+name.split('_')[0][5]+'_'+name.split('_')[1][0]+name.split('_')[1][3]+name.split('_')[1][5]+'_'+name.split('_')[3][2:4]
        else:
            col_name=name.split('_')[0][0:3]+'_'+name.split('_')[1][0]+name.split('_')[1][3]+name.split('_')[1][5]+'_'+name.split('_')[3][2:4]
        
        points=gpd.read_file(os.path.join('T:\WorldBankProject\Glob_Points','WaterModels',name))
        points=points.rename(columns={'GRID_CODE':col_name}).drop('POINTID',1)
        years.append(points)
    aggr_y = reduce(lambda left,right: gpd.sjoin(left,right,op='intersects').drop('index_right',1), years)
    aggr_y.to_file(os.path.join('T:\WorldBankProject\Glob_Points\WaterModels_8dec',name[0:-9]+'.shp'))

print 'done with hgms'

ipsls26=[wg_ipsl26,lpjml_ipsl26]
for ipsl in ipsls26:
    years=[]
    for name in ipsl:
        if 'watergap' in name:
             col_name=name.split('_')[0][0]+name.split('_')[0][5]+'_'+name.split('_')[1][0:3]+'_'+name.split('_')[3][2:4]
        else:
            col_name=name.split('_')[0][0:3]+'_'+name.split('_')[1][0:3]+'_'+name.split('_')[3][2:4]
        print col_name
            
        points=gpd.read_file(os.path.join('T:\WorldBankProject\Glob_Points','WaterModels',name))
        points=points.rename(columns={'GRID_CODE':col_name}).drop('POINTID',1)
        years.append(points)
    aggr_y = reduce(lambda left,right: gpd.sjoin(left,right,op='intersects').drop('index_right',1), years)
    aggr_y.to_file(os.path.join('T:\WorldBankProject\Glob_Points\WaterModels_8dec',name[0:-9]+'.shp'))

print 'done with ipsls'

ipsls85=[wg_ipsl85,lpjml_ipsl85]
for ipsl in ipsls85:
    years=[]
    for name in ipsl:
        if 'watergap' in name:
             col_name=name.split('_')[0][0]+name.split('_')[0][5]+'_'+name.split('_')[1][0:3]+'_'+name.split('_')[3][2:4]
        else:
            col_name=name.split('_')[0][0:3]+'_'+name.split('_')[1][0:3]+'_'+name.split('_')[3][2:4]

        points=gpd.read_file(os.path.join('T:\WorldBankProject\Glob_Points','WaterModels',name))
        points=points.rename(columns={'GRID_CODE':col_name}).drop('POINTID',1)
        years.append(points)
    aggr_y = reduce(lambda left,right: gpd.sjoin(left,right,op='intersects').drop('index_right',1), years)
    aggr_y.to_file(os.path.join('T:\WorldBankProject\Glob_Points\WaterModels_8dec',name[0:-9]+'.shp'))

print 'done with ipsls'


