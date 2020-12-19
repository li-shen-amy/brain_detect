# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 16:29:38 2020

@author: Li Shen
"""
# read expression images
# identified coordinate (x,y) in pixel of each expression spot in each image
# registrate each image and expression spots to reference atlas
# visualization and cluster/ focus on one region (say. PAG)
# from allensdk.api.queries.image_download_api import ImageDownloadApi
# import matplotlib.pyplot as plt
from skimage.io import imread, imsave
from skimage.transform import resize
# from skimage import img_as_bool
import os
import numpy as np

section_data_set_id = 74724760
# section_image_directory = str(section_data_set_id) + '_section_images'
section_image_directory = str(section_data_set_id) + '_5HT3a_section_images'
format_str = '.jpg'

file_names = os.listdir(section_image_directory)
nfiles = len(file_names)
# display_file_paths = [os.path.join(section_image_directory, dfn) for dfn in file_names[::nfiles]]

# image_api = ImageDownloadApi()
# section_images = image_api.section_image_query(section_data_set_id)
# section_image_ids = [si['id'] for si in section_images]

threshold = 127
pos_red_x = []
pos_red_y = []
pos_green_x = []
pos_green_y = []
pos_blue_x = []
pos_blue_y = []
# pos_z = []
pic_size = []
resized_filepath = 'D:/allen/'
save_path0 = os.path.join(resized_filepath, section_image_directory)
if not os.path.exists(save_path0):
    os.mkdir(save_path0)
for i in range(len(file_names)):
    file_name = file_names[i]
    # file_name = str(section_image_id) + format_str
    file_path = os.path.join(section_image_directory, file_name)
    image = imread(file_path)
    pic_size.append(image.shape)
    image_resized = resize(image, (1028, 1028, 3), anti_aliasing=True)
    save_path = os.path.join(save_path0, file_name)
    imsave(save_path, image_resized, check_contrast=False)
    # # figsize = (10, 8)
    # # fig, ax = plt.subplots(1, 3)
    # # ax.imshow(image)
    # # plt.show()
    #
    # # ax[0].hist(image[:, :, 0])
    # # ax[1].hist(image[:, :, 1])
    # # ax[2].hist(image[:, :, 2])
    # # plt.show()
    #
    # pos_red_x_tmp, pos_red_y_tmp = np.where(image[:, :, 0] > threshold)
    # pos_green_x_tmp, pos_green_y_tmp = np.where(image[:, :, 1] > threshold)
    # pos_blue_x_tmp, pos_blue_y_tmp = np.where(image[:, :, 2] > threshold)
    #
    # pos_red_x.append(pos_red_x_tmp)
    # pos_red_y.append(pos_red_y_tmp)
    # pos_green_x.append(pos_green_x_tmp)
    # pos_green_y.append(pos_green_y_tmp)
    # pos_blue_x.append(pos_blue_x_tmp)
    # pos_blue_y.append(pos_blue_y_tmp)
print(pic_size)
    # pos_z = pos_z.append(i * np.ones(pos_red_x_tmp.shape))

# image_bool = img_as_bool(image)
# ax.imshow(image_bool)
# plt.show()
