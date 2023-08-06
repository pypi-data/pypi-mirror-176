#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 10:51:48 2022

@author: jma
"""

import numpy as np
from skimage import segmentation, measure, exposure, morphology
import scipy.ndimage as nd
from tqdm import tqdm
import skimage 

def fill_holes(label_img, size=10, connectivity=1):
    output_image = np.copy(label_img)
    props = measure.regionprops(np.squeeze(label_img.astype('int')), cache=False)
    for prop in props:
        if prop.euler_number < 1:

            patch = output_image[prop.slice]

            filled = morphology.remove_small_holes(
                ar=(patch == prop.label),
                area_threshold=size,
                connectivity=connectivity)

            output_image[prop.slice] = np.where(filled, prop.label, patch)

    return output_image

def watershed_post(distmaps, interiors, dist_thre=0.1, interior_thre=0.2):
    """
    Parameters
    ----------
    distmaps : float (N, H, W) N is the number of cells
        distance transform map of cell/nuclear [0,1].
    interiors : float (N, H, W)
        interior map of cell/nuclear [0,1].

    Returns
    -------
    label_images : uint (N, H, W)
        cell/nuclear instance segmentation.

    """
    
    label_images = []
    for maxima, interior in zip(distmaps, interiors):# in interiors[0:num]:
        interior = nd.gaussian_filter(interior.astype(np.float32), 2)
        # find marker based on distance map
        if skimage.__version__ > '0.18.2':
            markers = measure.label(morphology.h_maxima(image=maxima, h=dist_thre, footprint=morphology.disk(2)))
        else:
            markers = measure.label(morphology.h_maxima(image=maxima, h=dist_thre, selem=morphology.disk(2)))
        # print('distmap marker num:', np.max(markers), 'interior marker num:', np.max(makers_interior))
        
        label_image = segmentation.watershed(-1 * interior, markers,
                                mask=interior > interior_thre, # 0.2/0.3
                                watershed_line=0)

        label_image = morphology.remove_small_objects(label_image, min_size=15)
        # fill in holes that lie completely within a segmentation label
        label_image = fill_holes(label_image, size=15)

        # Relabel the label image
        label_image, _, _ = segmentation.relabel_sequential(label_image)
        label_images.append(label_image)
    label_images = np.stack(label_images, axis=0)
    return label_images



#%% test 









