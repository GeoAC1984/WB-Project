'''This is the first part of labeling population cells as urban or rural;
its purpose is to initially label cells that intersect Urban Extents (from GRUMP)
as urban and the rest as rural; in part 2 urban population is compared
against UN urbanization rates and rural cells closest to UE are flipped to urban
to match UN projections'''

import arcpy,os
from arcpy import env  

arcpy.env.workspace=r'T:\WorldBankProject\HistoricPop_points\All_countries_points'
ue1=r'T:\WorldBankProject\HistoricPop\ue2000.shp'
ue2=r'T:\WorldBankProject\HistoricPop\ue2000_centroids.shp'
env.overwriteOutput = 1

exp="!NEAR_DIST!"

country_points=arcpy.ListFeatureClasses()
cntry_point1='bra_2000.shp'
cntry_point2='bra_2010.shp'
brazil=[cntry_point1,cntry_point2]
for cntry_point in brazil:
    arcpy.AddField_management(cntry_point, "UR","SHORT")
    arcpy.MakeFeatureLayer_management(cntry_point, "test_lyr")
    arcpy.SelectLayerByLocation_management("test_lyr","INTERSECT",ue1)
    arcpy.CalculateField_management("test_lyr","UR",1,"PYTHON_9.3","")
    arcpy.Near_analysis (cntry_point, ue1)
    arcpy.AddField_management(cntry_point, "NEAR_DIST2","DOUBLE")
    arcpy.CalculateField_management(cntry_point,"NEAR_DIST2",exp,"PYTHON_9.3","")
    arcpy.Near_analysis (cntry_point, ue2)        
    print 'done',cntry_point

