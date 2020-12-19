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
#%matplotlib inline


def verify_image(file_path, figsize=(18, 22)):
    image = imread(file_path)

    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(image)
    
    
def verify_svg(file_path, width_scale, height_scale):
    # we're using this function to display scaled svg in the rendered notebook.
    # we suggest that in your own work you use a tool such as inkscape or illustrator to view svg
    
    with open(file_path, 'rb') as svg_file:
        svg = svg_file.read()
    encoded_svg = b64encode(svg)
    decoded_svg = encoded_svg.decode('ascii')
    
    st = r'<img class="figure" src="data:image/svg+xml;base64,{}" width={}% height={}%></img>'.format(decoded_svg, width_scale, height_scale)
    display(HTML(st))


image_api = ImageDownloadApi()
svg_api = SvgApi()


#Downloading all of the images from a section data set

section_data_set_id = 71724696
downsample = 4
expression = 1

section_image_directory = str(section_data_set_id) + '_section_images'
format_str = '.jpg'

section_images = image_api.section_image_query(section_data_set_id)
section_image_ids = [si['id'] for si in section_images]

print(len(section_image_ids))

# You have probably noticed that the AllenSDK has a logger which notifies you of file downloads. 
# Since we are downloading ~300 images, we don't want to see messages for each one.
# The following line will temporarily disable the download logger.(optional)
logging.getLogger('allensdk.api.api.retrieve_file_over_http').disabled = True 

for section_image_id in section_image_ids:
    
    file_name = str(section_image_id) + format_str
    file_path = os.path.join(section_image_directory, file_name)
    
    Manifest.safe_make_parent_dirs(file_path)
    image_api.download_section_image(section_image_id, file_path=file_path, downsample=downsample,expression = expression, view='expression', colormap='expression')
    
# re-enable the logger (optional)
logging.getLogger('allensdk.api.api.retrieve_file_over_http').disabled = False


file_names = os.listdir(section_image_directory)
print(len(file_names))


















