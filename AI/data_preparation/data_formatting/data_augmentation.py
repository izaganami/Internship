#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""

import numpy as np
import tensorflow.keras.preprocessing.image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt


def data_augmentation(imgs,outputFolder, frameFolder):
    nb_augmentation = 1
    
    aug = ImageDataGenerator(
            
            rotation_range=3,
            zoom_range=0.005,
            width_shift_range=0.05,
            height_shift_range=0.01,
            shear_range=0.02,
            horizontal_flip=True,
            fill_mode="nearest")
    

    for n in range(nb_augmentation):
        #on récupère aléatoirement les paramètres d'une transformation
        param = aug.get_random_transform(imgs[0].shape[0:2])

        #on l'applique à la séquence d'image
        for i in range(len(imgs)):
            output = aug.apply_transform(imgs[i],param)
            plt.imsave(outputFolder + "output/frames_augmented/" + frameFolder+ "/frame" + str(i) + "_transfo_" + str(n) + ".jpg",output)
    

