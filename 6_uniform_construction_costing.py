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