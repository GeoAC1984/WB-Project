import arcpy,os
from arcpy import env  
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

path=r'T:\WorldBankProject\Glob_Rasters'
path_out=r'T:\WorldBankProject\Glob_Points'
env.overwriteOutput = 1
folders=['CropModels','WaterModels']
for folder in folders:
    rasters=[tif for tif in os.listdir(os.path.join(path,'{}'.format(folder))) if tif.endswith('tif')]
    raster_field="VALUE"
    for in_raster in rasters:
        points_name=in_raster[0:-4]+'.shp'
        out_point_features=os.path.join(path_out,folder,points_name)
        print out_point_features
        arcpy.RasterToPoint_conversion (os.path.join(path,folder,in_raster), out_point_features, raster_field)
        print 'done',points_name
