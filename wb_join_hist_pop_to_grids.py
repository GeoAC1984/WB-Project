### test before running!!!!

import pandas as pd
import geopandas as gpd
import os

all_points=r'T:\WorldBankProject\HistoricPop_points\urban_rural_pop_points'
grids_path=r'T:\WorldBankProject\HistoricPop_points\All_countries_grids'
country_grids=[grid for grid in os.listdir(grids_path) if grid.endswith('.shp')]
rural_points=[p for p in os.listdir(all_points) if 'rur.shp' in p and p.endswith('.shp')]
urban_points=[p for p in os.listdir(all_points) if 'urb.shp' in p and p.endswith('.shp')]
combined=rural_points+urban_points
spj_dict={}
for grid in  country_grids:
    spj_dict[grid]=[f for f in combined if f[0:3].upper()==grid[0:3].upper()] 


#test={'AFG_cells0125.shp':['afg_2000rur.shp', 'afg_2010rur.shp', 'afg_2000urb.shp', 'afg_2010urb.shp']}
for k,v in spj_dict.items():
    pop_grid_out=os.path.join(r'T:\WorldBankProject\HistoricPop\pop_fishnets',k[0:3]+'_fishnet.shp')
    pop_years=[]
    grid_shape=gpd.read_file(os.path.join(grids_path,k))
    grid_shape.crs={'init': u'epsg:4326'}
    grid_shape['uid']=grid_shape.index
    grid_shape['iso']=k[0:3]
    grid_shape=grid_shape[['uid','iso','geometry']]
    if v!=[] and len(v)==4:
        try:
            for i in v:            
                year_point_shape=gpd.read_file(os.path.join(all_points,i))
                year_point_shape.crs={'init': u'epsg:4326'}
                year=i.split('_')[1][0:4]
                ur=i[8:11]
                pop_col_name='{0}pop{1}'.format(ur,year)
                print (k, i, pop_col_name)
                year_point_shape.rename(columns={'GRID_CODE':pop_col_name},inplace=True)
                year_point_shape=year_point_shape[[pop_col_name,'geometry']]
                point_grid=gpd.sjoin(year_point_shape,grid_shape, how='left',op='intersects').drop(['index_right'],1)
                pop_by_grid=point_grid.groupby(['uid']).sum()
                pop_years.append(pop_by_grid)
            all_pop=result = pd.concat(pop_years, axis=1)
            grid_pop=grid_shape.merge(all_pop, left_on='uid',right_index=True, how='outer')
            grid_pop.to_file(pop_grid_out)
           
        except Exception:
            print ("An exception was thrown! for ", k,v)
            continue
    else:
        print (k, "needs to be done later")
        
            
       
           
