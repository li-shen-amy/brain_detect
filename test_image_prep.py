import image_prep
import os


# section_id = 71724696
# section_axis = 'sagittal'

section_id = 73818754
section_axis = 'coronal'

savepath = ''


# # downloading image sections...
# print('Downloading image sections...')
# downsample = 2
# image_prep.download_section(savepath, section_id, downsample)


# image_path = os.path.join(savepath, str(section_id) + '_input')
# padding_value = 255

image_path = os.path.join(savepath, str(section_id) + '_output')
padding_value = 0

# get image size
# image_prep.get_imsize(image_path)


# resize images
wh_ratio = 1.38
h = 400
w = round(h*wh_ratio)
image_prep.save_resize(image_path, h, w, padding_value)


