#############################################################################
#                    Import data and pre-processing                         #      
#############################################################################

import os
import pandas as pd
import geopandas as gpd
from tools_uav import readlas_convertgpd
import rasterio as rio
from rasterio.plot import plotting_extent
import numpy as np
import earthpy.plot as ep
import matplotlib.pyplot as plt

# Tracking message
print("Pre-processing data...")

# Import training point clouds
direct = os.path.join('C:\\', 'Users', 'carle', 'Documents','GEOTECH',
                      'large_data', 'UAV_data',  '2020', 'Processed',
                      'classified_pointclouds', 'training')

barren = readlas_convertgpd(os.path.join(direct, 'barren.las'), '32632',
                            'barren')
crop = readlas_convertgpd(os.path.join(direct, 'cropland.las'), '32632', 
                          'cropland')
grass = readlas_convertgpd(os.path.join(direct, 'grassland.las'), '32632',
                           'grassland')
road = readlas_convertgpd(os.path.join(direct, 'road.las'), '32632', 
                          'road')
shadow = readlas_convertgpd(os.path.join(direct, 'shadow.las'), '32632',
                            'shadow')
shrubland = readlas_convertgpd(os.path.join(direct, 'shrubland.las'), '32632',
                               'shrubland')
trees = readlas_convertgpd(os.path.join(direct, 'trees.las'), '32632',
                           'trees')
water = readlas_convertgpd(os.path.join(direct, 'water.las'), '32632',
                           'water')
water_veg = readlas_convertgpd(os.path.join(direct, 'water_vegetation.las'),
                               '32632', 'waterveg')

# Create training dataframe
training_list = [barren, crop, grass, road, shadow, shrubland, trees, 
                 water, water_veg]
training = gpd.GeoDataFrame(pd.concat(training_list, ignore_index=True))

# Extract raster predictors
coords = [(x,y) for x, y in zip(training.x, training.y)]
direct = os.path.join('C:\\', 'Users', 'carle', 'Documents','GEOTECH',
                      'large_data', 'UAV_data',  '2020', 'Processed',
                      'classified_pointclouds', 'raster_preds')

with rio.open(os.path.join(direct, 'dsm_sd9.tif')) as src:
    # Masked = True sets no data values to np.nan if they are in the metadata
    dsm_sd9 = src.read(1, masked=True)
    training['dsm_sd9'] = [x[0] for x in src.sample(coords)]

## Sample map
#fig, ax = plt.subplots(figsize=(10, 10))
#ep.plot_bands(dsm_sd9,
#              extent=plotting_extent(src),
#              cmap='viridis',
#              scale=False,
#              ax=ax)
#training.plot(ax=ax,
#              marker='s',
#              markersize=1,
#              color='yellow')
#ax.set_axis_off()
#plt.show()

# training.plot(column = 'class', markersize = 1, legend = True)

# Clean
del direct, barren, crop, grass, road, shadow, shrubland, trees, water
del water_veg, training_list, coords
