# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 16:29:38 2020

@author: Li Shen
"""
from skimage.io import imread, imsave
from skimage.transform import resize
import os
import numpy as np
from allensdk.api.queries.image_download_api import ImageDownloadApi
from allensdk.config.manifest import Manifest
import matplotlib.pyplot as plt
import logging
from base64 import b64encode
# from IPython.display import HTML, display

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

    st = r'<img class="figure" src="data:image/svg+xml;base64,{}" width={}% height={}%></img>'.format(decoded_svg,
                                                                                                      width_scale,
                                                                                                      height_scale)
    display(HTML(st))

def download_section(savepath, section_id, downsample):
    # Downloading all of the images from a section data set

    image_api = ImageDownloadApi()

    input_directory = str(section_id) + '_input'
    output_directory = str(section_id) + '_output'
    format_str = '.jpg'

    section_images = image_api.section_image_query(section_id)
    section_image_ids = [si['id'] for si in section_images]

    # You have probably noticed that the AllenSDK has a logger which notifies you of file downloads.
    # Since we are downloading ~300 images, we don't want to see messages for each one.
    # The following line will temporarily disable the download logger.(optional)
    logging.getLogger('allensdk.api.api.retrieve_file_over_http').disabled = True

    for section_image_id in section_image_ids:
        file_name = str(section_image_id) + format_str
        input_file_path = os.path.join(savepath, input_directory, file_name)
        output_file_path = os.path.join(savepath, output_directory, file_name)
        Manifest.safe_make_parent_dirs(input_file_path)
        image_api.download_section_image(section_image_id, file_path=input_file_path, downsample=downsample,
                                         expression=0)
        Manifest.safe_make_parent_dirs(output_file_path)
        image_api.download_section_image(section_image_id, file_path=output_file_path, downsample=downsample,
                                         expression=1)
    # re-enable the logger (optional)
    logging.getLogger('allensdk.api.api.retrieve_file_over_http').disabled = False

    file_names = os.listdir(os.path.join(savepath, input_directory))
    print(len(file_names))


def get_imsize(image_path):
    file_names = os.listdir(image_path)
    nfiles = len(file_names)

    pic_size = []
    for i in range(nfiles):
        file_name = file_names[i]
        file_path = os.path.join(image_path, file_name)
        image = imread(file_path)
        pic_size.append(image.shape)
        print(str(i) + file_name + ' original size:' + str(image.shape))


def save_resize(image_path, h, w, padding_value):
    wh_ratio = w/h
    file_names = os.listdir(image_path)
    nfiles = len(file_names)

    pic_size = []
    save_path0 = image_path + '_resize'
    if not os.path.exists(save_path0):
        os.mkdir(save_path0)
    for i in range(nfiles):
        file_name = file_names[i]
        file_path = os.path.join(image_path, file_name)
        save_path = os.path.join(save_path0, file_name)
        image = imread(file_path)
        image = np.uint8(image)
        pic_size.append(image.shape)
        image = padding(image, wh_ratio, padding_value)
        print(str(i) + ': ' + save_path + ' after padding size:' + str(image.shape))
        image_resized = resize(image, (h, w, 3), anti_aliasing=True)
        imsave(save_path, image_resized, check_contrast=False)


def padding(image, wh_ratio, padding_value):
    h, w, c = image.shape
    w_new = round(h * wh_ratio)
    if w < w_new:
        new_image = np.concatenate((image, padding_value * np.ones((h, w_new-w, c))), axis=1)
    else:
        new_image = np.concatenate((image, padding_value * np.ones((round(w/wh_ratio) - h, w, c))), axis=0)
    return new_image


def read_pos(image, threshold):
    pos_red_x_tmp, pos_red_y_tmp = np.where(image[:, :, 0] > threshold)
    pos_green_x_tmp, pos_green_y_tmp = np.where(image[:, :, 1] > threshold)
    pos_blue_x_tmp, pos_blue_y_tmp = np.where(image[:, :, 2] > threshold)
    pos_x = np.concatenate((pos_red_x_tmp,pos_green_x_tmp,pos_blue_x_tmp), axis = 0)
    pos_y = np.concatenate((pos_red_y_tmp,pos_green_y_tmp,pos_blue_y_tmp), axis = 0)
    return [pos_x,pos_y]