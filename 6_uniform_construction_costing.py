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

path = "/home/sachin/Projects/pcrafi_alignment/"
gdf = gpd.read_file(path + country_code.lower() + "_exposure_grid.gpkg")

#classification code listing
cols = gdf.columns.to_list()
remove = ['country', 'code', 'gid', 'gsize', 'total_floor_area', 'total_buildings', 'geometry']
cols = [i for i in cols if i not in remove]
cols.sort()
#for c in cols: print(c)

ucc_df = gpd.read_file("data/ucc_table.csv")
print(ucc_df)

gdf['replacement_cost'] = 0 #ucc_df.loc[uuc_df['building_code'] == ]gdf['']]
print(gdf)

#output
gdf.to_file(path + country_code.lower() + "_exposure_grid.gpkg", layer=country_code.lower() + "_exposure", driver="GPKG")
print("Finished.")