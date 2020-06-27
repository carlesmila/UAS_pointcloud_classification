#############################################################################
#                    Tools for point cloud classification                   #      
#############################################################################

from laspy.file import File
import numpy as np
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

# Import las file and convert to geopandas

def readlas_convertgpd(file, epsg, luclass):
    """Reads a las file and converts it to a geopandas object"""
    
    # Read file
    pcloud = File(file, mode = "r")
    
    # Convert to numpy
    pcloud_np = np.array((pcloud.x, pcloud.y, pcloud.z, 
                          pcloud.red, pcloud.green, pcloud.blue, 
                          pcloud.raw_classification)).transpose()
    # Transform to pandas DataFrame
    pcloud_df = pd.DataFrame(pcloud_np)
    pcloud_df.columns = ['x', 'y', 'z', 'red', 'green', 'blue', 'ground']
    pcloud_df['ground'] = pcloud_df['ground'].apply(int).apply(str)
    pcloud_df['class'] = luclass

    # Transform to geopandas GeoDataFrame
    crs = None
    geometry = [Point(xyz) for xyz in zip(pcloud.x, pcloud.y, pcloud.z)]
    pcloud_geodf = gpd.GeoDataFrame(pcloud_df, crs=crs, geometry=geometry)
    epsg_str = 'epsg:'+ epsg
    pcloud_geodf.crs = {'init' :epsg_str} 
    
    # Close file
    pcloud.close()
    
    return pcloud_geodf
