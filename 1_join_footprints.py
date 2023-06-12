import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd

country_code = "SB" #WS, TO, VU

gdf_points = gpd.read_file(country_code + "/1/" + country_code.lower() + "_buildings.shp")
gdf_footprints = gpd.read_file(country_code + "/1/" + country_code.lower() + "_building_footprints.shp")

#attribute join with id
#gdf_joined = pd.merge(gdf_points, gdf_footprints, on="ID")

## spatial join, without id
gdf_joined = gdf_footprints.sjoin(gdf_points, how="inner")#, predicate="within")

print(gdf_joined)

gdf_joined.to_file(country_code + "_PCRAFI_I_Buildings.gpkg", layer= country_code.lower() + "_buildings", driver="GPKG")

print("Finished.")
