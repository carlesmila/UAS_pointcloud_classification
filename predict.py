#############################################################################
#                          Predict new observations                         #      
#############################################################################

from laspy.file import File
import os
import rasterio as rio
import pandas as pd
import geopandas as gpd
from tools_uav import readlas_convertgpd
import matplotlib.pyplot as plt

# Tracking message
print("Making predictions...")

# Import point clouds for prediction
direct = os.path.join('C:\\', 'Users', 'carle', 'Documents','GEOTECH',
                    'large_data', 'UAV_data',  '2020', 'Processed',
                    'classified_pointclouds')
pred_data = readlas_convertgpd(os.path.join(direct,
                                            'binary_classification.las'),
                               '32632', 'predict')

# Filter data in boundary
bound = gpd.read_file(os.path.join(direct, 'boundary', 'boundary.shp'))
bound_mask = pred_data.within(bound.loc[0, 'geometry'])
pred_data = pred_data.loc[bound_mask]

# Fetch raster values
coords = [(x,y) for x, y in zip(pred_data.x, pred_data.y)]
with rio.open(os.path.join(direct, 'raster_preds', 'dsm_sd9.tif')) as src:
    # Masked = True sets no data values to np.nan if they are in the metadata
    dsm_sd9 = src.read(1, masked=True)
    pred_data['dsm_sd9'] = [x[0] for x in src.sample(coords)]
    
#pred_data.dsm_sd9.isna().sum()

# Prepare data for prediction
prednames = ['z', 'red', 'green', 'blue', 'ground', 'dsm_sd9']
pred_X = pred_data.loc[:, prednames]

# Predict
preds = rf.predict(pred_X)
pred_data = pred_data.assign(preds = preds)

## Figure predictions
#f, ax = plt.subplots(1, figsize=(8, 10))
#ax = pred_data.plot(column = 'preds', markersize = 1, legend = True, ax=ax)
#plt.show()

# Prepare data for writing
pred_data = pred_data.assign(preds_write = 0)
pred_data.loc[pred_data['preds'] == 'barren', 'preds_write'] = 1  
pred_data.loc[pred_data['preds'] == 'cropland', 'preds_write'] = 2  
pred_data.loc[pred_data['preds'] == 'grassland', 'preds_write'] = 3  
pred_data.loc[pred_data['preds'] == 'road', 'preds_write'] = 4  
pred_data.loc[pred_data['preds'] == 'shadow', 'preds_write'] = 5  
pred_data.loc[pred_data['preds'] == 'shrubland', 'preds_write'] = 6  
pred_data.loc[pred_data['preds'] == 'trees', 'preds_write'] = 7  
pred_data.loc[pred_data['preds'] == 'water', 'preds_write'] = 8 
pred_data.loc[pred_data['preds'] == 'waterveg', 'preds_write'] = 9 

pred_data['preds_write'].value_counts() 

# Save to las
headfile = File(os.path.join(direct, '0-0-0-0.las'), mode="r")
header = headfile.header
outfile = File("classified_pc.las", mode="w", header=header)
outfile.x = pred_data['x'].to_numpy()
outfile.y = pred_data['y'].to_numpy()
outfile.z = pred_data['z'].to_numpy()
outfile.red = pred_data['red'].to_numpy()
outfile.green = pred_data['green'].to_numpy()
outfile.blue = pred_data['blue'].to_numpy()
outfile.classification = pred_data['preds_write'].to_numpy()
outfile.close()

# Clean
del bound, bound_mask, coords, direct, dsm_sd9, pred_X, pred_data, prednames
del preds