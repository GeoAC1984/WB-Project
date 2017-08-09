import pandas as pd
import geopandas as gpd
import os

grids_path=r'T:\WorldBankProject\Regions'

regions=os.listdir(grids_path)
regions_w_countries=[r for r in regions if os.listdir(os.path.join(grids_path,r))!=[]]
#regions_w_countries.pop(1)

CropModels=[m for m in os.listdir(r'T:\WorldBankProject\Glob_Points\CropModels_8dec') if m.endswith('shp')]
WaterModels=[m for m in os.listdir(r'T:\WorldBankProject\Glob_Points\WaterModels_8dec') if m.endswith('shp')]

for region in regions_w_countries:
    if region=='CentralAfrica':
        print ('Processing region: ', region)  
        for country in os.listdir(os.path.join(grids_path,region)):
            if os.listdir(os.path.join(grids_path,region,country,'WaterOutput'))==[]:
                print ('working on ',country)
                shapes=[shp for shp in os.listdir(os.path.join(grids_path,region,country,'CountryGrids')) if shp.endswith('shp')]
                country_prefix=shapes[0].split('Cells')[0]
                cell05=shapes[1]
                cell025=shapes[0]
                shp05=gpd.read_file(os.path.join(grids_path,region,country, 'CountryGrids',cell05))
                shp025=gpd.read_file(os.path.join(grids_path,region,country, 'CountryGrids',cell025))
                centers=gpd.GeoDataFrame(geometry=shp025.centroid)
                for water_model in WaterModels:
                    shape_out=country_prefix+'_'+water_model
                    model=gpd.read_file(os.path.join(r'T:\WorldBankProject\Glob_Points\WaterModels_8dec',water_model))
                    try:
                        data_grid05=gpd.sjoin(shp05,model, how='left',op="contains").drop(['index_right','ID',],1)
                        centroids_data=gpd.sjoin(centers,data_grid05, how='left',op='within').drop(['index_right'],1)
                        data_grid025=gpd.sjoin(shp025,centroids_data, how='left',op='intersects').drop(['index_right'],1)
                        drop_cols=[c for c in data_grid025.columns if c.startswith('GRIDCODE') or c.startswith('ID')]
                        data_grid025.drop(drop_cols,1,inplace=True)
                        first_years=[c for c in data_grid025.columns if c.endswith('_75',) or c.endswith('_85') or c.endswith('_95')]        
                        the_rest=[c for c in data_grid025.columns if c not in first_years]
                        new_order=first_years+the_rest
                        water_out=gpd.GeoDataFrame(data_grid025[new_order],geometry=data_grid025.geometry)
                        water_out.to_file(os.path.join(grids_path,region,country,'WaterOutput',shape_out))
                        print ('done with',shape_out)
                    except ValueError:
                        print ("There is no ", water_model," points for this country: ", country)
                        break
                for crop_model in CropModels:
                    shape_out=country_prefix+'_'+crop_model
                    model=gpd.read_file(os.path.join(r'T:\WorldBankProject\Glob_Points\CropModels_8dec',crop_model))
                    try:                
                        data_grid05=gpd.sjoin(shp05,model, how='left',op="contains").drop(['index_right','ID',],1)       
                        centroids_data=gpd.sjoin(centers,data_grid05, how='left',op='within').drop(['index_right'],1)
                        data_grid025=gpd.sjoin(shp025,centroids_data, how='left',op='intersects').drop(['index_right'],1)
                        drop_cols=[c for c in data_grid025.columns if c.startswith('GRIDCODE') or c.startswith('ID')]
                        data_grid025.drop(drop_cols,1,inplace=True)
                        first_years=[c for c in data_grid025.columns if c.endswith('_75',) or c.endswith('_85') or c.endswith('_95')]        
                        the_rest=[c for c in data_grid025.columns if c not in first_years]
                        new_order=first_years+the_rest
                        crop_out=gpd.GeoDataFrame(data_grid025[new_order],geometry=data_grid025.geometry)
                        crop_out.to_file(os.path.join(grids_path,region,country,'CropOutput',shape_out))  
                        print ('done with',shape_out)
                    except ValueError:
                        print ("There is no ", crop_model," points for this country: ", country)
                        break
            else:
                print  (country,' in the ',region, ' region is completed')
    


