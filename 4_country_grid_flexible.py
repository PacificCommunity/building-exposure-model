# coding: utf-8
__author__ = "Sachindra Singh"
__copyright__ = "Copyright 2023, The Pacific Community (SPC)"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "sachindras@spc.int"
__status__ = "Development"

import os
os.environ['USE_PYGEOS'] = '0'
import pandas as pd
import geopandas as gpd
import numpy as np
from fiona.crs import from_epsg
import shapely
import warnings
warnings.filterwarnings('ignore')


BUFFER_SIZE = 0.01 #1km
COUNTRY = "Tonga"


gdf = gpd.read_file("data/pacific_admin_polygon.geojson")
gdf = gdf[gdf.country == COUNTRY]
gid = gdf.iloc[0]['gid']
gid


buffer_df_01km = gdf.geometry.buffer(-BUFFER_SIZE * 1, cap_style = 3)
buffer_df_01km = gdf - buffer_df_01km
buffer_df_02km = gdf.geometry.buffer(-(BUFFER_SIZE * 2), cap_style = 3)
buffer_df_02km = gdf - buffer_df_02km
buffer_df_05km = gdf.geometry.buffer(-(BUFFER_SIZE * 5), cap_style = 3)
buffer_df_05km = gdf - buffer_df_05km
buffer_df_10km = gdf.geometry.buffer(-BUFFER_SIZE * 10, cap_style = 3)
buffer_df_10km = gdf - buffer_df_10km

gdf_1km = buffer_df_01km
gdf_2km = buffer_df_02km - buffer_df_01km
gdf_5km = buffer_df_05km - buffer_df_02km
gdf_10km = buffer_df_10km - buffer_df_05km
#gdf_10km = gdf - buffer_df_10km

#
gdf = gdf_5km
gdf.explore()


#GRID_SIZE = 0.001 * 5 #100m2
buffer_list = [gdf_1km, gdf_2km, gdf_5km]#, gdf_10km]
size_list = [1, 2, 5]#, 10]

grid_cells = []
index = 0

grid_df_list = []

for gdf in buffer_list:
    xmin, ymin, xmax, ymax = gdf.total_bounds
    GRID_SIZE = 0.001 * size_list[index] #100m2

    cell_width = GRID_SIZE
    cell_height = GRID_SIZE

    max_region = max(gdf.geometry, key=lambda a: a.area)
    grid_area = max_region

    for x0 in np.arange(xmin, xmax + cell_width, cell_width):
        for y0 in np.arange(ymin, ymax + cell_height, cell_height):
            x1 = x0 - cell_width
            y1 = y0 + cell_height
            new_cell = shapely.geometry.box(x0, y0, x1, y1)
            if new_cell.intersects(grid_area):
                grid_cells.append(new_cell)
            else:
                pass

    # individual file outputs
    grid_df = gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs=from_epsg(4326))
    grid_df["country"] = COUNTRY
    grid_df["code"] = gid
    #grid_df["gid"] = (grid_df.index + 1) 
    #grid_df["gid"] = grid_df.index + 1 * (size_list[index] * 10000)
    grid_df["gid"] = (size_list[index] ** 10) + (grid_df.index + 1)
    grid_df["gsize"] = str(size_list[index] * 100)
    grid_df.to_file("grid_" + COUNTRY.lower() + "_" + str(size_list[index] * 100) + "m2.geojson", driver='GeoJSON')
    grid_df_list.append(grid_df)
    grid_cells = []
    index = index + 1
    # end


# combined output
gdf_final = gpd.pd.concat(grid_df_list)
gdf_final.to_file("grid_" + COUNTRY.lower() + ".geojson", driver='GeoJSON')
print("Processed.")





