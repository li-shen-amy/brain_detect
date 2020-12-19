from allensdk.api.queries.image_download_api import ImageDownloadApi
from allensdk.api.queries.svg_api import SvgApi
from allensdk.config.manifest import Manifest

import matplotlib.pyplot as plt
from skimage.io import imread
import pandas as pd

import logging
import os
from base64 import b64encode

from IPython.display import HTML, display

#product_id = 8
#file_name = str(product_id) + format_str
#file_path = os.path.join(section_image_directory, file_name)
    
#Manifest.safe_make_parent_dirs(file_path)
image_api = ImageDownloadApi()

print(image_api.get_section_data_sets_by_product(product_ids = 8))

