import arcpy,os
from arcpy import env  


env.overwriteOutput = 1
grids_path=r'T:\WorldBankProject\Regions'
regions=os.listdir(grids_path)## all the regions
for region in regions:
    print 'Processing region: ', region
    for country in os.listdir(os.path.join(grids_path,region)):
        if country=='Chad':
            pass
        shapes=[shp for shp in os.listdir(os.path.join(grids_path,region,country,'CountryGrids')) if shp.endswith('shx')]
        cell025=shapes[0]
        shp025=os.path.join(grids_path,region,country, 'CountryGrids',cell025)
        out_name=os.path.join(grids_path,region,country, 'CountryGrids',cell025[0:3]+'_cells0125.shx')
        if not arcpy.Exists(out_name):
            arcpy.Rename_management (shp025, out_name)
