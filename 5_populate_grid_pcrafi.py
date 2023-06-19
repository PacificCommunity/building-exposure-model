__author__ = "Sachindra Singh"
__copyright__ = "Copyright 2023, The Pacific Community (SPC)"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "sachindras@spc.int"
__status__ = "Development"

import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import numpy as np

#define country
country = "tonga"
country_code = "to"

gdf_grid = gpd.read_file(f"grid/grid_{country}.geojson")
gdf_grid.sort_values(by=['gid'], inplace=True)
gdf_classified_buildings = gpd.read_file(f"{country_code}_classified.gpkg")

#join
gdf_joined = gdf_grid.sjoin(gdf_classified_buildings, how="left")

#gdf_joined.to_file(country_code.lower() + "_test.gpkg", layer=country_code.lower() + "_test", driver="GPKG")

gid_list = set(gdf_grid['gid'].tolist())

#summarise and populate
#iterate gdf_grid, count/sum values from gdf_joined - class_code, floor_area X levels
for gid in gid_list:    
    group = gdf_joined.loc[gdf_joined['gid'] == gid] 
  
    total_floor_area = (group['floor_area'] * group['levels']).sum()
    gdf_grid.loc[gdf_grid['gid'] == gid, 'total_floor_area'] = np.round(total_floor_area, 2)
    
    total_buildings = len(group.index)
    gdf_grid.loc[gdf_grid['gid'] == gid, 'total_buildings'] = total_buildings   
    
    summary = group['class_code'].value_counts()    
    for code, count in summary.items():        
        gdf_grid.loc[gdf_grid['gid'] == gid, code] = count

#output
gdf_grid.loc[gdf_grid['total_floor_area'] == 0, 'total_buildings'] = 0
gdf_grid.to_file(country_code.lower() + "_exposure_grid.gpkg", layer=country_code.lower() + "_exposure", driver="GPKG")
print("Finished.")
