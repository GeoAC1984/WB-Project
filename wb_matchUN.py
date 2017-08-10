# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 21:01:56 2017

@author: AClark
"""

import pandas as pd
import geopandas as gpd
from simpledbf import Dbf5
import os

#pop_points=[shp for shp in os.listdir(r'T:\WorldBankProject\HistoricPop_points\All_countries_points') if shp.endswith('shp')]
pop_path=r'T:\WorldBankProject\HistoricPop_points\All_countries_points'
pop_points=[shp for shp in os.listdir(pop_path) if shp.endswith('.shp')]
done=[shp for shp in os.listdir(r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points') if shp.endswith('.shp')]
to_process=[s for s in pop_points if s not in done]

for pop_point in to_process:
    print(pop_point)
    if 'RUS' not in pop_point:
    
        #pop_point='arg_2000.dbf'
        updated_points_out=r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points\{}'.format(pop_point)
        rural_out=pop_point.split('.shp')[0]+'rur.shp'
        urban_out=pop_point.split('.shp')[0]+'urb.shp'
        country_code=pop_point[0:3].upper()
        year=pop_point.split('_')[1][0:4]
        pop=gpd.read_file(os.path.join(pop_path,pop_point))
        print('read in')
        urb_rates=pd.read_excel(r'T:\WorldBankProject\HistoricPop\UrbanizationRates.xlsx',skiprows=[0,1,2],index_col=1)
        country_rate=urb_rates[year].ix[country_code]
        rural=pop[pop['UR']=='R']
        right_urban=pop.GRID_CODE.sum()*(country_rate/100)## this is total urban pop that should be according to UN urb rate
        diff=right_urban-pop[pop['UR']=='U'].GRID_CODE.sum()
        
        if diff>5000:    
            print (diff)
            surrounding_cells=1 ## how many surrounding cells is nessesary to select
            pad=rural[rural.NEAR_DIST2<0.0083333333*surrounding_cells]## cell resolution is 0.0083333333

            while pad.GRID_CODE.sum()<diff:## while n-cell padding is still smaller than urban pop diff, select next cell and check again
                surrounding_cells+=1
                pad=rural[rural.NEAR_DIST22<0.0083333333*surrounding_cells]
            print ('Need to pad with ', surrounding_cells,' cells')

            if surrounding_cells==1:
                pad.sort_values(by=['NEAR_DIST22','GRID_CODE'],ascending=[True,False],inplace=True)
                pad['cumsum']=pad.GRID_CODE.cumsum()
                final_flip=pad[pad['cumsum']<right_urban-pop[pop['UR']=='U'].GRID_CODE.sum()]
                final_flip['UR']='U'
                pop.update(final_flip)
                urban=pop[pop['UR']=='U']
                rural=pop[pop['UR']=='R']
                rural.to_file(r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points\{}'.format(rural_out))
                urban.to_file(r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points\{}'.format(urban_out))
            else:
                ## get the subset where all cells can be flipped    
                flipp_them=rural[rural.NEAR_DIST2<(0.0083333333*(surrounding_cells-1))]
                flipp_them['UR']='U'
                pop.update(flipp_them)## update to urban surronding cells up to -1
                #create new rural subset
                rural=pop[pop['UR']=='R']
                final_flip=rural[rural.NEAR_DIST2<0.0083333333*(surrounding_cells)]
                sorted_rural=final_flip.sort_values(by=['NEAR_DIST2','GRID_CODE'],ascending=[True,False])
                sorted_rural['cumsum']=sorted_rural.GRID_CODE.cumsum()
                final_flip= sorted_rural[sorted_rural['cumsum']<right_urban-pop[pop['UR']=='U'].GRID_CODE.sum()]
                final_flip['UR']='U'
                pop.update(final_flip)
                urban=pop[pop['UR']=='U']
                rural=pop[pop['UR']=='R']
                rural.to_file(r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points\{}'.format(rural_out))
                urban.to_file(r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points\{}'.format(urban_out))
            
        elif diff<0:
            print (diff)
            ## if urban pop is latger than UN's estimate, flipp urban cells to rural
            urban=pop[pop['UR']=='U']
            urban.sort_values(by=['NEAR_DIST','GRID_CODE'],ascending=[False,True],inplace=True)## here we want largest distance from urban core with smallest pop
            urban['cumsum']=urban.GRID_CODE.cumsum()
            final_flip=urban[urban['cumsum']<abs(diff)]
            final_flip['UR']='R'
            pop.update(final_flip)
            rural=pop[pop['UR']=='R']
            urban=pop[pop['UR']=='U']    
            rural.to_file(r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points\{}'.format(rural_out))
            urban.to_file(r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points\{}'.format(urban_out))
        
