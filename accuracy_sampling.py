#############################################################################
#                          Derive features accuracy                         #      
#############################################################################

from laspy.file import File
import os
import pandas as pd
import geopandas as gpd
from tools_uav import readlas_convertgpd
import numpy as np

# Tracking message
print("Selecting features for accuracy assessment...")

# Import classified point cloud
file = os.path.join('C:\\', 'Users', 'carle', 'Documents','GEOTECH',
                    'IFGI', 'UAS',  'UAV_python', 'classified_pc.las')
preds = readlas_convertgpd(file, '32632', 'predict')

# Drop useless columns to facilitate management
preds = preds.drop(columns = ['x','y','z','red','green','blue','class'])

# Sample 30 points per class
np.random.seed(seed=1234)
size = 30
replace = False
fn = lambda obj: obj.loc[np.random.choice(obj.index, size, replace),:]
acc_sample = preds.groupby('ground', as_index=False).apply(fn)

# Write to disk
#acc_sample.to_file("acc_assessment.shp")