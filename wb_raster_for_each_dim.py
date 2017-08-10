import arcpy,os
from arcpy import env  
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

env.overwriteOutput = 1

NetCDF_path=r'T:\WorldBankProject\GlobalData\Climate-NetCDF'
##env.workspace=NetCDF_path
arcpy.env.scratchWorkspace = r'T:\WorldBankProject\Glob_Rasters'

variable = "index2"
x_dimension = "lon"
y_dimension = "lat"
band_dimension = ""
dimension = "time"
valueSelectionMethod = "BY_VALUE"


models=[i for i in os.listdir(NetCDF_path)]
for model in models:
    outLoc = r'T:\WorldBankProject\Glob_Rasters\{}'.format(model)
    rcps=[rcp for rcp in os.listdir(os.path.join(NetCDF_path,model))]
    for rcp in rcps:
        print "Outputig for RCP",rcp
        cdfs=os.listdir(os.path.join(NetCDF_path,model,rcp))
        for cdf  in cdfs:
            inNetCDF=os.path.join(NetCDF_path,model,rcp,cdf)
            print inNetCDF
            model_prefix=inNetCDF.split('_')[1]+'_'+inNetCDF.split('_')[2][0:-3]+'_'+inNetCDF.split('_')[3]
            nc_FP = arcpy.NetCDFFileProperties(inNetCDF)
            nc_Dim = nc_FP.getDimensions()
            for dimension in nc_Dim:
                if dimension == "time":
                    top = nc_FP.getDimensionSize(dimension)
                    for i in range(0, top):
                        dimension_values = nc_FP.getDimensionValue(dimension, i)
                        out_raster=model_prefix+'_'+dimension_values.split('/')[2][0:4]
                        dv1 = ["time", dimension_values]
                        dimension_values = [dv1]
                        raster_layer=arcpy.MakeNetCDFRasterLayer_md(inNetCDF, variable, x_dimension, y_dimension,out_raster, band_dimension, dimension_values, valueSelectionMethod)
                        print "success", raster_layer            
                        outname =os.path.join(outLoc, out_raster+'.tif')
                        arcpy.CopyRaster_management(out_raster, outname, "", "", "", "NONE", "NONE", "")
                        print 'done raster',out_raster
               
                
