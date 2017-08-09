# -*- coding: utf-8 -*-
"""
@author: AClark
"""
import pandas as pd
import geopandas as gpd
import os

#pop_points=[shp for shp in os.listdir(r'T:\WorldBankProject\HistoricPop_points\All_countries_points') if shp.endswith('shp')]
server='/Volumes/cidr_fs/Projects/NFS_SEES/WorldBankProject'
pop_path='/Volumes/cidr_fs/Projects/NFS_SEES/WorldBankProject/HistoricPop_points/All_countries_points'
pop_points=[shp for shp in os.listdir(pop_path) if shp.endswith('.shp')]
done=[shp for shp in os.listdir(os.path.join(server,'HistoricPop_points', 'urban_rural_pop_points')) if shp.endswith('.shp')]
to_process=[s for s in pop_points if s.split('.shp')[0]+'rur.shp' not in done]

for pop_point in to_process:
    print(pop_point)
    if 'RUS'.lower() not in pop_point and 'chn' not in pop_point:
        try:
            updated_points_out=os.path.join(server,'HistoricPop_points', 'urban_rural_pop_points','{}'.format(pop_point))
            rural_out=pop_point.split('.shp')[0]+'rur.shp'
            urban_out=pop_point.split('.shp')[0]+'urb.shp'
            country_code=pop_point[0:3].upper()
            year=pop_point.split('_')[1][0:4]
            pop=gpd.read_file(os.path.join(pop_path,pop_point))
            print('reading in')
            urb_rates=pd.read_excel(os.path.join(server,'HistoricPop','UrbanizationRates.xlsx'),skiprows=[0,1,2],index_col=1)
            country_rate=urb_rates[year].iloc[country_code]
            rural=pop[pop['UR']==0].copy()
            urban=pop[pop['UR']==1].copy()
            right_urban=pop.GRID_CODE.sum()*(country_rate/100)## this is total urban pop that should be according to UN urb rate
            diff=right_urban-urban.GRID_CODE.sum()
            
            if diff>1000:    
                print (diff)
                rural.sort_values(by=['NEAR_DIST2','GRID_CODE'],ascending=[True,False],inplace=True)
                rural['cumsum']=rural.GRID_CODE.cumsum()
                final_flip=rural[rural['cumsum']<diff].copy()
                final_flip['UR']=1
                pop.update(final_flip)
                rural=pop[pop['UR']==0]
                urban=pop[pop['UR']==1]            
                rural.to_file(os.path.join(server,'HistoricPop_points', 'urban_rural_pop_points','{}'.format(rural_out)))
                urban.to_file(os.path.join(server,'HistoricPop_points', 'urban_rural_pop_points','{}'.format(urban_out)))             
                    
            elif diff<0:
                print (diff)
                ## if urban pop is latger than UN's estimate, flipp urban cells to rural
                urban=pop[pop['UR']==1]
                urban.sort_values(by=['NEAR_DIST','GRID_CODE'],ascending=[False,True],inplace=True)## here we want largest distance from urban core with smallest pop
                urban['cumsum']=urban.GRID_CODE.cumsum()
                final_flip=urban[urban['cumsum']<abs(diff)].copy()
                final_flip['UR']=0
                pop.update(final_flip)
                rural=pop[pop['UR']==0]
                urban=pop[pop['UR']==1]    
                rural.to_file(os.path.join(server,'HistoricPop_points', 'urban_rural_pop_points','{}'.format(rural_out)))
                urban.to_file(os.path.join(server,'HistoricPop_points', 'urban_rural_pop_points','{}'.format(urban_out)))
            else:
                rural.to_file(os.path.join(server,'HistoricPop_points', 'urban_rural_pop_points','{}'.format(rural_out)))
                urban.to_file(os.path.join(server,'HistoricPop_points', 'urban_rural_pop_points','{}'.format(urban_out)))
        except Exception:
            print ("An exception was thrown! for ", pop_point)
            continue

