__author__ = "Sachindra Singh"
__copyright__ = "Copyright 2023, The Pacific Community (SPC)"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "sachindras@spc.int"
__status__ = "Development"

import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#define country
#country = "Vanuatu"
#country_code = "VU"
#country = "Tonga"
#country_code = "TO"
#country = "Samoa"
#country_code = "WS"
country = "Solomon"
country_code = "SB"

gdf1 = gpd.read_file(country_code + "/1/" + country_code + "_PCRAFI_I_Buildings.gpkg")
gdf2 = gpd.read_file(country_code + "/2/PCRAFI_II_"+ country +"_Buildings.shp")
if country_code == "VU":
    gdf2 = gpd.read_file(country_code + "/2/VU_PCRAFI_II_Buildings.gpkg")
gdf2.columns = gdf2.columns.str.lower()
    
#crs
gdf1 = gdf1.to_crs(4326)
gdf2 = gdf2.to_crs(4326)

#year
gdf1['survey_year'] = 2012
gdf2['survey_year'] = 2022

#resolve age conflict
gdf1.rename(columns={"age": "age1"}, inplace=True)
gdf2.rename(columns={"age": "age2"}, inplace=True)

#merge only geometries
#gdf =  pd.concat([gdf1[['geometry']] , gdf2[['geometry']]])

#merge/combine all attributes
gdf = pd.concat([gdf1, gdf2])
gdf = gdf.to_crs(4326)
#gdf.drop(columns=['fid'], inplace=True)

#generate id
gdf['id'] =  gdf.index + 1

#drop duplicate indexes
#gdf = gdf.loc[~gdf.index.duplicated(), :]
gdf = gdf.reset_index(drop=True)
gdf.fillna(0, inplace=True)
print(gdf.index.is_unique)

#output combined
#print(gdf)
#gdf.to_file(country_code.lower() + "_combined.gpkg", layer=country_code.lower() + "_buildings", driver="GPKG")

#Final Variable = P2, P1
#Use = Use_Grp, Usage #Commercial
gdf['use'] = gdf['usage'].str.capitalize()
gdf.loc[gdf['use'].isnull(), 'use'] = gdf['USE_GRP'].str.capitalize()
gdf.loc[gdf['use'] == 'Commercial/industrial', 'use'] = 'Commercial'
gdf.loc[gdf['use'].isnull(), 'use'] = 'Unknown'
gdf.loc[gdf['use'].str.startswith("Public"), 'use'] = "Public"
gdf.loc[gdf['use'].str.startswith("Education"), 'use'] = "Education"

#SubUse = SubUse1, SubUse
gdf['subuse'] = gdf['subuse'].str.capitalize()
gdf.loc[gdf['subuse'].isnull(), 'subuse'] = gdf['SUBUSE1'].str.capitalize()
gdf.loc[gdf['subuse'].isnull(), 'subuse'] = 'None'
gdf.loc[gdf['subuse'].str.startswith('Other'), 'subuse'] = 'Other'
gdf.loc[gdf['subuse'].str.startswith('None'), 'subuse'] = 'None'
gdf.loc[gdf['subuse'].str.contains('manufacturing'), 'subuse'] = 'Manufacturing'

#Structure = B_Frame, Structure
gdf['structure'] = gdf['structure'].str.capitalize()
gdf.loc[gdf['structure'].isnull(), 'structure'] = gdf['B_FRAME1'].str.capitalize()
gdf.loc[gdf['structure'].isnull(), 'structure'] = gdf['B_FRAME2'].str.capitalize()
gdf.loc[gdf['structure'].isnull(), 'structure'] = "Unknown"
gdf.loc[gdf['structure'].str.startswith("Unknown"), 'structure'] = "Unknown"
gdf.loc[gdf['structure'].str.startswith("Tilt"), 'structure'] = "Tilt-Up Slab"
gdf.loc[gdf['structure'].str.startswith("Concrete"), 'structure'] = "Concrete column"

#Wall_Material = Wall_MatX, Wall_Mater 
gdf['wall_material'] = gdf['wall_mater'].str.capitalize()
gdf.loc[gdf['wall_material'].isnull(), 'wall_material'] = gdf['WALL_MAT1'].str.capitalize()
#gdf.loc[gdf['wall_material'].isnull(), 'wall_material'] = gdf['WALL_MAT2'].str.capitalize()
#gdf.loc[gdf['wall_material'].isnull(), 'wall_material'] = gdf['WALL_MAT3'].str.capitalize()
#gdf.loc[gdf['wall_material'].isnull(), 'wall_material'] = gdf['WALL_MAT4'].str.capitalize()
gdf.loc[gdf['wall_material'].isnull(), 'wall_material'] = "Unknown"
gdf.loc[gdf['wall_material'].str.startswith('Unknown'), 'wall_material'] = "Unknown"
gdf.loc[gdf['wall_material'].str.startswith('Other'), 'wall_material'] = "Other"
gdf.loc[gdf['wall_material'].str.startswith('None'), 'wall_material'] = "None"
gdf.loc[gdf['wall_material'].str.startswith('none'), 'wall_material'] = "None"

#Foundation_Type = Found1, Foundation_Type (Wooden/Concrete)
gdf['foundation_type'] = gdf['foundation'].str.capitalize()
gdf.loc[gdf['foundation_type'].isnull(), 'foundation_type'] = gdf['FOUND1'].str.capitalize()
gdf.loc[gdf['foundation_type'].isnull(), 'foundation_type'] = gdf['FOUND2'].str.capitalize()
gdf.loc[gdf['foundation_type'].isnull(), 'foundation_type'] = gdf['FOUND3'].str.capitalize()
gdf.loc[gdf['foundation_type'].isnull(), 'foundation_type'] = "Unknown"
gdf.loc[gdf['foundation_type'].str.startswith('Unknown'), 'foundation_type'] = "Unknown"
gdf.loc[gdf['foundation_type'].str.startswith('Concrete'), 'foundation_type'] = "Concrete column"
gdf.loc[gdf['foundation_type'].str.startswith('Wood/steel'), 'foundation_type'] = "Wooden/steel pole"

#Foundation_Bracing = Found_BR1x, Found_Brac
gdf['foundation_bracing'] = gdf['found_brac'].str.capitalize()
gdf.loc[gdf['foundation_bracing'].isnull(), 'foundation_bracing'] = gdf['FOUND_BR1'].str.capitalize()
gdf.loc[gdf['foundation_bracing'].isnull(), 'foundation_bracing'] = gdf['FOUND_BR2'].str.capitalize()
gdf.loc[gdf['foundation_bracing'].isnull(), 'foundation_bracing'] = gdf['FOUND_BR3'].str.capitalize()
gdf.loc[gdf['foundation_bracing'].isnull(), 'foundation_bracing'] = "Unknown"

#Age = Age, Age (5, 15, 30) (New, Medium, Old) from P2
gdf['age'] = gdf['age2']
gdf.loc[gdf['age'].isnull(), 'age'] = 'Unknown'
gdf.loc[gdf['age'] == 0, 'age'] = 'Unknown'
gdf.loc[gdf['age'].str.startswith('New'), 'age'] = "5"
gdf.loc[gdf['age'].str.startswith("Medium"), 'age'] = "15"
gdf.loc[gdf['age'].str.startswith("Old"), 'age'] = "30"

#Levels = Occ_Level + UnOcc_level, No_Stories
gdf['levels'] = gdf['storeys']
gdf.loc[gdf['levels'] == 0, 'levels'] = gdf['OCC_LEV'] + gdf['UNOCC_LEV']
gdf.loc[gdf['levels'] == 0, 'levels'] = 1.0

#F_Area = P2, P1 
gdf['floor_area'] = gdf['geometry'].to_crs(4326).area * 10000000000
gdf['floor_area'] = gdf['floor_area'].round(2)

#Roof_Material = Roof_Mat_1, Roof_Material
gdf['roof_material'] = gdf['roof_mater']
gdf.loc[gdf['roof_material'].isnull(), 'roof_material'] = gdf['ROOF_MAT_1'].str.capitalize()
gdf.loc[gdf['roof_material'].isnull(), 'roof_material'] = gdf['ROOF_MAT_2'].str.capitalize()
gdf.loc[gdf['roof_material'].isnull(), 'roof_material'] = "Unknown"
gdf.loc[gdf['roof_material'] == 0, 'roof_material'] = "Unknown"

#Roof_Pitch = RoofPitch, Roof_Pitch
#Roof_Shape = RoofPitch1, Roof_Shape

#F_MinHt = Midpoint Of P1 Values, [0.5, 1.5] 
#F_MaxHt = Midpoint Of P1 Values, [0.5, 1.5] 
#Window_Type = P2
#Window_Protection = Shutter1, Boolean  
#Defects = Foundation_Condition, Wall_Condition, Roof_Condition {5-1} //Excellent, Good, Fair, Poor, Very Poor

#unfragment
#gdf = gdf.copy()

#retain new attributes
gdf = gdf[['id', 'use', 'subuse', 'structure', 'wall_material', 'foundation_type', 'foundation_bracing', 'roof_material', 'levels', 'age', 'floor_area', 'survey_year', 'geometry']]

#output merged/aligned
print(sorted(gdf['foundation_type'].unique()))
gdf.to_file(country_code.lower() + "_merged.gpkg", layer=country_code.lower() + "_buildings", driver="GPKG")
#gdf.to_file(country_code.lower() + "_merged.geojson", driver="GeoJSON")
print("Finished.")

