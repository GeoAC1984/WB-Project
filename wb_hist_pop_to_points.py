import arcpy,os
from arcpy import env  
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

pop_path=r'T:\WorldBankProject\HistoricPop'
env.overwriteOutput = 1
grids_path=r'T:\WorldBankProject\HistoricPop\GPW_by_country'
env.workspace=grids_path
fcs= arcpy.ListFeatureClasses()

tif=r'T:\WorldBankProject\HistoricPop\gpw-v4-population-count-2010\gpw-v4-population-count_2010.tif'
year=tif.split('_')[1][0:4]
in_raster=tif
for country in fcs:         
    country_pop=ExtractByMask (tif, country)
    pop_points_out=os.path.join(r'T:\WorldBankProject\HistoricPop_points\All_countries_points', country[0:3]+'_'+year+'.shp')
    arcpy.RasterToPoint_conversion(country_pop, pop_points_out, "VALUE")
    print pop_points_out  


