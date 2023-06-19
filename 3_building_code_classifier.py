__author__ = "Sachindra Singh"
__copyright__ = "Copyright 2023, The Pacific Community (SPC)"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "sachindras@spc.int"
__status__ = "Development"

import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd

country_code = "to"
path = "/home/sachin/Projects/pcrafi_alignment/"
data_file = f"{path}{country_code}_merged.gpkg"
gdf = gpd.read_file(data_file)
print(list(gdf.columns))

#code (old) = WallMaterial_RoofMaterial_Levels(H, M, L)_Location(U, P, R) eg: WO_OT_LR
#code = WallMaterial_RoofMaterial_Levels(H, M, L)_Residential/NonResidenial(R/NR) eg: WO_OT_LR
code_wm, code_rm, level_type, residential = "", "", "", ""

#wall
wm = {
    'SM': ['Fibre-cement sheet', 'Fibre-cement board', "Metal sheet", "Fibre"],
    'CB': ['Masonry', 'Concrete', 'Concrete Block'],
    'WO': ['Plywood sheet'],
    'WC': ['Timber Cement', 'Timber', "Timber board"],
    'TR': ['Traditional'],
    'OT': ['Unknown', 'None', 'Other']
}
for k, v in wm.items():    
    for v1 in v:              
        gdf.loc[gdf["wall_material"].str.startswith(v1), "code_wm"] = k

#roof
rm = {
    'SM': ['Unknown', "Metal Sheet"],
    'CO': ['Concrete', 'Fibre-cement Sheets'],
    #'OT': ['*'],
}
for k, v in rm.items():    
    for v1 in v:              
        gdf.loc[gdf["roof_material"] == v1, "code_rm"] = k
            
gdf.loc[gdf['code_rm'].isnull(), 'code_rm'] = 'OT'

#level_type
gdf.loc[gdf["levels"] == 1, "level_type"] = "L"
gdf.loc[gdf["levels"] == 2, "level_type"] = "M"
gdf.loc[gdf["levels"] == 3, "level_type"] = "M"
gdf.loc[gdf["levels"] > 3, "level_type"] = "H"

#residential (R/NR)
gdf.loc[gdf["use"] == "Residential", "residential"] = "R"
gdf.loc[gdf["use"] == "Unknown", "residential"] = "R"
gdf.loc[gdf["subuse"] == "Residential", "residential"] = "R"
gdf.loc[gdf["subuse"] == "Unknown", "residential"] = "R"
gdf.loc[gdf['residential'].isnull(), 'residential'] = 'NR'

gdf['class_code'] = gdf['code_wm'] + "_" + gdf['code_rm'] + "_" + gdf['level_type'] + "_" +  gdf['residential']
print(gdf['class_code'])

gdf0 = gdf[['id', 'class_code', 'wall_material', 'roof_material', 'levels', 'use', 'floor_area', 'geometry']]
print(gdf0)

gdf0.to_file(country_code.lower() + "_classified.gpkg", layer=country_code.lower() + "_buildings_classified", driver="GPKG")

print("Finished.")